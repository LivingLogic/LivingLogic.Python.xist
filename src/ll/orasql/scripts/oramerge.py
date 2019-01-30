#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
=======

:program:`oramerge` can be used for merging the changes between two Oracle
database schemas into a third one. Depending on the existance/non-existance
of schema objects in the three schemas :program:`oramerge` does the right thing.
If a schema objects exists in all three schemas, the external tool
:command:`merge3` will be used for creating a merged version of the object
(except for tables where the appropriate ``ALTER TABLE`` statements will be
output if possible).


Options
=======

:program:`oramerge` supports the following options:

.. program:: oramerge

.. option:: connectstring1

	Old version of database schema

.. option:: connectstring2

	New version of database schema

.. option:: connectstring3

	Schema into which changes should be merged

.. option:: -v <flag>, --verbose <flag>

	Produces output (on stderr) while the database is read or written.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -c <mode>, --color <mode>

	Should the output (when the :option:`-v` option is used) be colored?
	If ``auto`` is specified (the default) then the output is colored if stderr
	is a terminal. Valid modes are ``yes``, ``no`` or ``auto``.

.. option:: -k <flag>, --keepjunk <flag>

	If false (the default), database objects that have ``$`` or
	``SYS_EXPORT_SCHEMA_`` in their name will be skipped (otherwise these
	objects will be considered as merge candidates).
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)


Example
=======

Output a script that merges the changes between ``user@db`` and ``user2@db2``
into ``user3@db3``:

.. sourcecode:: bash

	$ oramerge user/pwd@db user2/pwd2@db2 user3/pwd3@db3 -v >db.sql
"""


import sys, os, difflib, argparse, tempfile, subprocess

from ll import misc, orasql, astyle


__docformat__ = "reStructuredText"


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4comment = astyle.Style.fromenv("LL_ORASQL_REPRANSI_COMMENT", "black:black:bold")
s4addedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ADDEDFILE", "black:green")
s4addedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ADDEDLINE", "green:black")
s4removedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_REMOVEDFILE", "black:red")
s4removedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_REMOVEDLINE", "red:black")
s4changedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CHANGEDFILE", "black:blue")
s4changedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CHANGEDLINE", "blue:black")
s4pos = astyle.Style.fromenv("LL_ORASQL_REPRANSI_POS", "black:black:bold")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4connid = astyle.Style.fromenv("LL_ORASQL_REPRANSI_NOTE", "yellow:black:bold")
s4action = astyle.Style.fromenv("LL_ORASQL_REPRANSI_NOTE", "magenta:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")



def cs(connection):
	return s4connectstring(connection.connectstring())


def df(obj):
	return s4object(str(obj))


def connid(name):
	return s4connid(f"[{name}]")


def showcomment(out, *texts):
	out.writeln(s4comment("-- ", *texts))


def conflictmarker(prefix, *text):
	return astyle.style_default(s4error(prefix), " ", *text)


def showreport(out, type, countcreate, countdrop, countcollision, countmerge, countmergeconflict):
	first = True
	data = (("added", countcreate), ("dropped", countdrop), ("collided", countcollision), ("merged", countmerge), ("mergeconflict", countmergeconflict))
	for (name, count) in data:
		if count:
			if first:
				out.write(" => ")
				first = False
			else:
				out.write("; ")
			if name in ("collided", "mergeconflict"):
				cls = s4error
			else:
				cls = s4action
			if count > 1:
				msg = f"{count:,} {type}s {name}"
			else:
				msg = f"1 {type} {name}"
			out.write(cls(msg))
	if first:
		out.write(" => identical")
	out.writeln()


def gettimestamp(obj, cursor, format):
	try:
		timestamp = obj.udate(cursor)
	except orasql.SQLObjectNotFoundError:
		return "doesn't exist"
	if timestamp is not None:
		timestamp = timestamp.strftime(format)
	else:
		timestamp = "without timestamp"
	return timestamp


def main(args=None):
	# Merge changes between oldsource and newsource into destination
	p = argparse.ArgumentParser(description="output info for merging the changes between two Oracle database schemas into a third")
	p.add_argument("connectstring1", help="Old version of database schema")
	p.add_argument("connectstring2", help="New version of database schema")
	p.add_argument("connectstring3", help="Schema into which changes should be merged")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' in their name? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	connection1 = orasql.connect(args.connectstring1)
	connection2 = orasql.connect(args.connectstring2)
	connection3 = orasql.connect(args.connectstring3)

	def fetch(connection, name):
		objects = set()

		for (i, obj) in enumerate(connection.objects(owner=None, mode="flat")):
			keep = ("$" not in obj.name and not obj.name.startswith("SYS_EXPORT_SCHEMA_")) or args.keepjunk
			if args.verbose:
				msg = astyle.style_default("oramerge.py: ", cs(connection), connid(name), f" fetching #{i+1:,} ", df(obj))
				if not keep:
					msg += s4error(" (skipped)")
				stderr.writeln(msg)
			if keep:
				objects.add(obj)
		return objects

	def write(file, data):
		try:
			file.write(data)
			file.write("\n")
		finally:
			file.close()

	objects1 = fetch(connection1, 1)
	objects2 = fetch(connection2, 2)
	objects3 = fetch(connection3, 3)

	retcode = 0

	def inmesg(flag, name):
		if flag:
			return astyle.style_default("in ", connid(name))
		else:
			return astyle.style_default("not in ", connid(name))

	countcreate = 0
	countdrop = 0
	countmerge = 0
	countcollision = 0
	countmergeconflict = 0
	allobjects = objects1 | objects2 | objects3
	for (i, obj) in enumerate(allobjects):
		action = None
		in1 = obj in objects1
		in2 = obj in objects2
		in3 = obj in objects3
		if args.verbose:
			stderr.write("oramerge.py: ", df(obj), " #", str(i+1), "/", str(len(allobjects)), ": ")
			first = True
			for (nr, flag) in enumerate((in1, in2, in3)):
				if flag:
					if first:
						stderr.write("in ")
						first = False
					else:
						stderr.write("+")
					stderr.write(connid(nr+1))
		comm = s4comment("-- ", df(obj), " ")
		if in1 != in2: # ignore changes from in2 to in3, because only if something changed in the sources we have to do something
			if not in1 and in2 and not in3: # added in in2 => copy it to db3
				if args.verbose:
					stderr.writeln(" => ", s4action("new (create it)"))
				countcreate += 1
				action = "create"
			elif not in1 and in2 and in3: # added in both in2 and in3 => collision?
				if obj.createsql(connection2) != obj.createsql(connection3):
					if args.verbose:
						stderr.writeln(" => ", s4error("collision"))
					countcollision += 1
					action = "collision"
					retcode = 2
				else:
					if args.verbose:
						stderr.writeln(" => already created (keep it)")
			elif in1 and not in2 and not in3: # removed in in2 and in3 => not needed
				if args.verbose:
					stderr.writeln(" => removed (not needed)")
			elif in1 and not in2 and in3: # removed in in2 => remove in db3
				if args.verbose:
					stderr.writeln(" => ", s4action("drop it"))
				countdrop += 1
				action = "drop"
			else:
				raise ValueError("the boolean world is about to end")
		elif in1 and in2 and in3: # in all three => merge it
			sql1 = obj.createsql(connection1)
			sql2 = obj.createsql(connection2)
			sql3 = obj.createsql(connection3)

			if args.verbose:
				stderr.write(" => diffing")

			if sql1 != sql2: # ignore changes between sql2 and sql3 here too
				# If it's a table, we do not output a merged "create table" statement, but the appropriate "alter table" statements
				if isinstance(obj, orasql.Table):
					fields1 = set(obj.columns(connection1))
					fields2 = set(obj.columns(connection2))
					fields3 = set(obj.columns(connection3))
					fieldcountcreate = 0
					fieldcountdrop = 0
					fieldcountmerge = 0
					fieldcountcollision = 0
					fieldcountmergeconflict = 0
					for field in fields1 | fields2 | fields3:
						in1 = field in fields1
						in2 = field in fields2
						in3 = field in fields3
						if in1 != in2: # ignore changes between in2 and in3 here too
							if not in1 and in2 and not in3: # added in in2 => copy it to db3
								fieldcountcreate += 1
								countcreate += 1
								showcomment(stdout, "add ", df(field))
								stdout.writeln(field.addsql(connection2))
							elif not in1 and in2 and in3: # added in both in2 and in3 => collision?
								fieldcountcollision += 1
								countcollision += 1
								showcomment(stdout, "collision ", df(field))
								stdout.writeln(conflictmarker(7*"<", "added in ", cs(connection2), " and ", cs(connection3), " with different content"))
							elif in1 and not in2 and not in3: # removed in in2 and in3 => not needed
								pass
							elif in1 and not in2 and in3: # removed in in2 => remove in db3
								fieldcountdrop += 1
								countdrop += 1
								showcomment(stdout, "drop ", df(field))
								stdout.writeln(field.dropsql(connection3))
						elif in1 and in2 and in3: # in all three => modify field
							sql1 = field.addsql(connection1)
							sql2 = field.addsql(connection2)
							sql3 = field.addsql(connection3)
							if sql1 != sql2 or sql2 != sql3:
								try:
									sql = field.modifysql(connection3, connection1.cursor(), connection2.cursor()) # add changes from db1 to db2
								except orasql.ConflictError as exc:
									fieldcountmergeconflict += 1
									countmergeconflict += 1
									showcomment(stdout, "merge conflict ", df(field))
									stdout.writeln(conflictmarker(7*"<", str(exc)))
								else:
									fieldcountmerge += 1
									countmerge += 1
									showcomment(stdout, "merged ", df(field))
									stdout.writeln(sql)
					if args.verbose:
						showreport(stderr, "field", fieldcountcreate, fieldcountdrop, fieldcountcollision, fieldcountmerge, fieldcountmergeconflict)
				else:
					if args.verbose:
						stderr.write(" => merge them")
					action = "merge"
			else:
				if args.verbose:
					stderr.writeln(" => identical")
		elif in3:
			if args.verbose:
				stderr.writeln(" => keep it")
		else:
			if args.verbose:
				stderr.writeln(" => not needed")

		if action is not None:
			if action == "collision":
				showcomment(stdout, "collision ", df(obj))
				stdout.writeln(conflictmarker(7*"<", "added in ", cs(connection2), " and ", cs(connection3), " with different content"))
			elif action == "create":
				showcomment(stdout, "create ", df(obj))
				stdout.writeln(obj.createsql(connection2, term=True))
			elif action == "drop":
				showcomment(stdout, "drop ", df(obj))
				stdout.writeln(obj.dropsql(connection3, term=True))
			elif action == "merge":
				filename1 = tempfile.mktemp(suffix=".sql", prefix="oramerge_1_")
				filename2 = tempfile.mktemp(suffix=".sql", prefix="oramerge_2_")
				filename3 = tempfile.mktemp(suffix=".sql", prefix="oramerge_3_")

				file1 = open(filename1, "wb")
				try:
					write(file1, sql1)

					file2 = open(filename2, "wb")
					try:
						write(file2, sql2)

						file3 = open(filename3, "wb")
						try:
							write(file3, sql3)

							# do the diffing
							proc = subprocess.Popen(["diff3", "-m", filename3, filename1, filename2], stdout=subprocess.PIPE)
							data = []
							while True:
								chunk = proc.stdout.read(8192)
								if chunk:
									data.append(chunk)
								else:
									break
							diffretcode = proc.returncode
							if diffretcode is None:
								diffretcode = proc.wait()
								while True:
									chunk = proc.stdout.read(8192)
									if chunk:
										data.append(chunk)
									else:
										break
							data = "".join(data)
							if diffretcode == 0: # no conflict
								showcomment(stdout, "merge ", df(obj))
								# Check if anything has changed
								finalsql = data
								# diff3 seems to append a "\n"
								if finalsql != sql3 and (not finalsql.endswith("\n") or finalsql[:-1] != sql3):
									if args.verbose:
										stderr.writeln(" => ", s4action("merged"))
									stdout.write(finalsql)
							elif diffretcode == 1: # conflict
								showcomment(stdout, "merge conflict ", df(obj))
								if args.verbose:
									stderr.writeln(" => ", s4error("merge conflict"))
								retcode = 2
								for line in data.splitlines():
									line = line.rstrip("\n")
									if line.startswith(7*"<") or line.startswith(7*"|") or line.startswith(7*"=") or line.startswith(7*">"):
										(prefix, line) = (line[:7], line[7:])
										line = line.strip()
										if line == filename1:
											line = conflictmarker(prefix, cs(connection1))
										elif line == filename2:
											line = conflictmarker(prefix, cs(connection2))
										elif line == filename3:
											line = conflictmarker(prefix, cs(connection3))
										else:
											line = conflictmarker(prefix, line)
									stdout.writeln(line)
							else:
								raise OSError(f"Trouble from diff3: {diffretcode}")
						finally:
							os.remove(filename3)
					finally:
						os.remove(filename2)
				finally:
					os.remove(filename1)
	if args.verbose:
		stderr.write("oramerge.py: ", cs(connection3))
		showreport(stderr, "object", countcreate, countdrop, countcollision, countmerge, countmergeconflict)
	return retcode


if __name__ == "__main__":
	sys.exit(main())
