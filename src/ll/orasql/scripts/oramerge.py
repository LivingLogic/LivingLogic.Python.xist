#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


import sys, os, difflib, optparse, tempfile, subprocess

from ll import orasql, astyle


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
	return s4connid("[%d]" % name)


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
				msg = "%d %ss %s" % (count, type, name)
			else:
				msg = "1 %s %s" % (type, name)
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
	colors = ("yes", "no", "auto")
	blanks = ("literal", "trail", "lead", "both", "collapse")
	# Merge changes between oldsource and newsource into destination
	p = optparse.OptionParser(usage="usage: %prog [options] oldsourceconnectstring newsourceconnectstring destinationconnectstring")
	p.add_option("-v", "--verbose", dest="verbose", help="Give a progress report?", default=False, action="store_true")
	p.add_option("-c", "--color", dest="color", help="Color output (%s)" % ", ".join(colors), default="auto", choices=colors)
	p.add_option("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' in their name?", default=False, action="store_true")
	p.add_option("-e", "--encoding", dest="encoding", help="Encoding for output", default="utf-8")

	(options, args) = p.parse_args(args)
	if len(args) != 3:
		p.error("incorrect number of arguments")
		return 1

	if options.color == "yes":
		color = True
	elif options.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	connection1 = orasql.connect(args[0])
	connection2 = orasql.connect(args[1])
	connection3 = orasql.connect(args[2])

	def fetch(connection, name):
		objects = set()

		for (i, obj) in enumerate(connection.iterobjects(mode="flat", schema="user")):
			keep = ("$" not in obj.name and not obj.name.startswith("SYS_EXPORT_SCHEMA_")) or options.keepjunk
			if options.verbose:
				msg = astyle.style_default("oramerge.py: ", cs(connection), connid(name), " fetching #%d " % (i+1), df(obj))
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
		if options.verbose:
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
				if options.verbose:
					stderr.writeln(" => ", s4action("new (create it)"))
				countcreate += 1
				action = "create"
			elif not in1 and in2 and in3: # added in both in2 and in3 => collision?
				if obj.createddl(connection2) != obj.createddl(connection3):
					if options.verbose:
						stderr.writeln(" => ", s4error("collision"))
					countcollision += 1
					action = "collision"
					retcode = 2
				else:
					if options.verbose:
						stderr.writeln(" => already created (keep it)")
			elif in1 and not in2 and not in3: # removed in in2 and in3 => not needed
				if options.verbose:
					stderr.writeln(" => removed (not needed)")
			elif in1 and not in2 and in3: # removed in in2 => remove in db3
				if options.verbose:
					stderr.writeln(" => ", s4action("drop it"))
				countdrop += 1
				action = "drop"
			else:
				raise ValueError("the boolean world is about to end")
		elif in1 and in2 and in3: # in all three => merge it
			ddl1 = obj.createddl(connection1)
			ddl2 = obj.createddl(connection2)
			ddl3 = obj.createddl(connection3)

			if options.verbose:
				stderr.write(" => diffing")

			if ddl1 != ddl2: # ignore changes between ddl2 and ddl3 here too
				# If it's a table, we do not output a merged "create table" statement, but the appropriate "alter table" statements
				if isinstance(obj, orasql.Table):
					fields1 = set(obj.itercolumns(connection1))
					fields2 = set(obj.itercolumns(connection2))
					fields3 = set(obj.itercolumns(connection3))
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
								stdout.writeln(field.addddl(connection2))
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
								stdout.writeln(field.dropddl(connection3))
						elif in1 and in2 and in3: # in all three => modify field
							ddl1 = field.addddl(connection1)
							ddl2 = field.addddl(connection2)
							ddl3 = field.addddl(connection3)
							if ddl1 != ddl2 or ddl2 != ddl3:
								try:
									ddl = field.modifyddl(connection3, connection1.cursor(), connection2.cursor()) # add changes from db1 to db2
								except orasql.ConflictError, exc:
									fieldcountmergeconflict += 1
									countmergeconflict += 1
									showcomment(stdout, "merge conflict ", df(field))
									stdout.writeln(conflictmarker(7*"<", str(exc)))
								else:
									fieldcountmerge += 1
									countmerge += 1
									showcomment(stdout, "merged ", df(field))
									stdout.writeln(ddl)
					if options.verbose:
						showreport(stderr, "field", fieldcountcreate, fieldcountdrop, fieldcountcollision, fieldcountmerge, fieldcountmergeconflict)
				else:
					if options.verbose:
						stderr.write(" => merge them")
					action = "merge"
			else:
				if options.verbose:
					stderr.writeln(" => identical")
		elif in3:
			if options.verbose:
				stderr.writeln(" => keep it")
		else:
			if options.verbose:
				stderr.writeln(" => not needed")

		if action is not None:
			if action == "collision":
				showcomment(stdout, "collision ", df(obj))
				stdout.writeln(conflictmarker(7*"<", "added in ", cs(connection2), " and ", cs(connection3), " with different content"))
			elif action == "create":
				showcomment(stdout, "create ", df(obj))
				stdout.writeln(obj.createddl(connection2, term=True))
			elif action == "drop":
				showcomment(stdout, "drop ", df(obj))
				stdout.writeln(obj.dropddl(connection3, term=True))
			elif action == "merge":
				filename1 = tempfile.mktemp(suffix=".sql", prefix="oramerge_1_")
				filename2 = tempfile.mktemp(suffix=".sql", prefix="oramerge_2_")
				filename3 = tempfile.mktemp(suffix=".sql", prefix="oramerge_3_")

				lines = []
				file1 = open(filename1, "wb")
				try:
					write(file1, ddl1.encode(options.encoding))

					file2 = open(filename2, "wb")
					try:
						write(file2, ddl2.encode(options.encoding))

						file3 = open(filename3, "wb")
						try:
							write(file3, ddl3.encode(options.encoding))

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
								finalddl = data
								# diff3 seems to append a "\n"
								if finalddl != ddl3 and (not finalddl.endswith("\n") or finalddl[:-1] != ddl3):
									if options.verbose:
										stderr.writeln(" => ", s4action("merged"))
									stdout.write(finalddl)
							elif diffretcode == 1: # conflict
								showcomment(stdout, "merge conflict ", df(obj))
								if options.verbose:
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
								raise OSError("Trouble from diff3: %d" % diffretcode)
						finally:
							os.remove(filename3)
					finally:
						os.remove(filename2)
				finally:
					os.remove(filename1)
	if options.verbose:
		stderr.write("oramerge.py: ", cs(connection3))
		showreport(stderr, "object", countcreate, countdrop, countcollision, countmerge, countmergeconflict)
	return retcode


if __name__ == "__main__":
	sys.exit(main())
