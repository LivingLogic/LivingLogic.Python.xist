#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


"""
Purpose
-------

``oradiff`` can be used to find the difference between two Oracle database schemas.


Options
-------

``oradiff`` supports the following options:

	``connectstring1``
		Oracle connectstring for the first database schema.

	``connectstring2``
		Oracle connectstring for the second database schema.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Produces output (on stderr) while to database is read.

	``-c``, ``--color`` : ``yes``, ``no`` or ``auto``
		Should the output (when the ``-v`` option is used) be colored. If ``auto``
		is specified (the default) then the output is colored if stderr is a
		terminal.

	``-m``, ``--mode`` : ``brief``, ``udiff`` or ``full``
		Specifies how the differences should be shown. ``brief`` only prints
		whether objects are different (or which ones exist in one of the databases);
		``udiff`` outputs the differences in "unified diff" format and ``full``
		outputs the object from the second schema if they differ (i.e. it outputs
		the script that must be executed to copy the differences from schema 2
		to schema 1).

	``-n``, ``--context`` : integer
		The number of context lines in unified diff mode (i.e. the number of
		unchanged lines above and below each block of changes; the default is 2)

	``-k``, ``--keepjunk`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If true (the default), database objects that have ``$`` or
		``SYS_EXPORT_SCHEMA_`` in their name will be skipped (otherwise these
		objects will be included in the output).

	``-b``, ``--blank`` : ``literal``, ``trail``, ``lead``, ``both`` or ``collapse``
		The ``-b`` option specifies how whitespace in the database objects should
		be compared. With ``literal`` all whitespace is significant, with ``trail``
		trailing whitespace will be ignore, with ``lead`` leading whitespace will
		be ignored, with ``both`` trailing and leading whitespace will be ignored
		and with ``collapse`` trailing and leading whitespace will be ignored and
		stretches of whitespace will be treated as a single space.

Example
-------

Compare the schemas ``user@db`` and ``user2@db2``, collapsing whitespace and
using unified diff mode with 5 context lines::

	$ oradiff user/pwd@db user2/pwd2@db2 -bcollapse -mudiff -n5 -v >db.diff
"""


import sys, os, difflib, argparse

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
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def cs(connection):
	return s4connectstring(connection.connectstring())


def df(obj):
	return s4object(str(obj))


def comment(*texts):
	return s4comment("-- ", *texts)


def gettimestamp(obj, connection, format):
	try:
		timestamp = obj.udate(connection)
	except orasql.SQLObjectNotFoundError:
		return "doesn't exist"
	if timestamp is not None:
		timestamp = timestamp.strftime(format)
	else:
		timestamp = "without timestamp"
	return timestamp


def getcanonicalddl(ddl, blank):
	return [Line(line, blank) for line in ddl.splitlines()]


class Line(object):
	__slots__ = ("originalline", "compareline")

	def __init__(self, line, blank):
		self.originalline = line
		if blank == "literal":
			self.compareline = line
		elif blank == "trail":
			self.compareline = line.rstrip()
		elif blank == "lead":
			self.compareline = line.lstrip()
		elif blank == "both":
			self.compareline = line.strip()
		elif blank == "collapse":
			self.compareline = " ".join(line.strip().split())
		else:
			raise ValueError("unknown blank value {!r}".format(blank))

	def __eq__(self, other):
		return self.compareline == other.compareline

	def __ne__(self, other):
		return self.compareline != other.compareline

	def __hash__(self):
		return hash(self.compareline)


def showudiff(out, obj, ddl1, ddl2, connection1, connection2, context=3, timeformat="%c"):
	def header(prefix, style, connection):
		return style("{} {!r} in {}: {}".format(prefix, obj, connection.connectstring(), gettimestamp(obj, connection, timeformat)))

	started = False
	for group in difflib.SequenceMatcher(None, ddl1, ddl2).get_grouped_opcodes(context):
		if not started:
			out.writeln(header("---", s4removedfile, connection1))
			out.writeln(header("+++", s4addedfile, connection2))
			started = True
		(i1, i2, j1, j2) = group[0][1], group[-1][2], group[0][3], group[-1][4]
		out.writeln(s4pos("@@ -{},{} +{},{} @@".format(i1+1, i2-i1, j1+1, j2-j1)))
		for (tag, i1, i2, j1, j2) in group:
			if tag == "equal":
				for line in ddl1[i1:i2]:
					out.writeln(" {}".format(line.originalline))
				continue
			if tag == "replace" or tag == "delete":
				for line in ddl1[i1:i2]:
					out.writeln(s4removedline("-", line.originalline))
			if tag == "replace" or tag == "insert":
				for line in ddl2[j1:j2]:
					out.writeln(s4addedline("+", line.originalline))


def filteredenumerate(sequence, objset):
	i = 0
	for obj in sequence:
		if obj in objset:
			yield (i, obj)
			i += 1


def main(args=None):
	p = argparse.ArgumentParser(description="compare two Oracle database schemas", epilog="For more info see http://www.livinglogic.de/Python/orasql/scripts/oradiff.html")
	p.add_argument("connectstring1", help="First schema")
	p.add_argument("connectstring2", help="Second schema")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-m", "--mode", dest="mode", help="Output mode (default %(default)s)", default="udiff", choices=("brief", "udiff", "full"))
	p.add_argument("-n", "--context", dest="context", help="Number of context lines (default %(default)s)", type=int, default=2)
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' or 'SYS_EXPORT_SCHEMA_' in their name? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-b", "--blank", dest="blank", help="How to treat whitespace (default %(default)s)", default="literal", choices=("literal", "trail", "lead", "both", "collapse"))

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

	def fetch(connection, mode="flat"):
		objectset = set()
		objectlist = []

		def keep(obj):
			if obj.owner is not None:
				return False
			if args.keepjunk:
				return True
			if "$" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_"):
				return False
			return True

		for (i, obj) in enumerate(connection.iterobjects(owner=None, mode=mode)):
			keepdef = keep(obj)
			if args.verbose:
				msg = astyle.style_default("oradiff.py: ", cs(connection), ": fetching #{} ".format(i+1), df(obj))
				if not keepdef:
					msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
				stderr.writeln(msg)
			if keepdef:
				objectset.add(obj)
				objectlist.append(obj)
		return (objectset, objectlist)

	(objectset1, objectlist1) = fetch(connection1, mode="drop")
	(objectset2, objectlist2) = fetch(connection2, mode="create")

	# If we output in full mode the resulting SQL script should be usable, so
	# we try to iterate the object in approprate order

	# Objects only in database 1
	onlyin1 = objectset1 - objectset2
	for (i, obj) in filteredenumerate(objectlist1, onlyin1):
		if args.verbose:
			stderr.writeln("oradiff.py: only in ", cs(connection1), " #{}/{} ".format(i+1, len(onlyin1)), df(obj))
		if args.mode == "brief":
			stdout.writeln(df(obj), ": only in ", cs(connection1))
		elif args.mode == "full":
			stdout.writeln(comment(df(obj), ": only in ", cs(connection1)))
			ddl = obj.dropddl(connection1, term=True)
			if ddl:
				stdout.write(ddl)
		elif args.mode == "udiff":
			ddl = getcanonicalddl(obj.createddl(connection1), args.blank)
			showudiff(stdout, obj, ddl, [], connection1, connection2, args.context)

	# Objects only in database 2
	onlyin2 = objectset2 - objectset1
	for (i, obj) in filteredenumerate(objectlist2, onlyin2):
		if args.verbose:
			stderr.writeln("oradiff.py: only in ", cs(connection2), " #{}/{} ".format(i+1, len(onlyin2)), df(obj))
		if args.mode == "brief":
			stdout.writeln(df(obj), ": only in ", cs(connection2))
		elif args.mode == "full":
			stdout.writeln(comment(df(obj), ": only in ", cs(connection2)))
			ddl = obj.createddl(connection2, term=True)
			if ddl:
				stdout.write(ddl)
		elif args.mode == "udiff":
			ddl = getcanonicalddl(obj.createddl(connection2), args.blank)
			showudiff(stdout, obj, [], ddl, connection1, connection2, args.context)

	# Objects in database 1 and database 2
	common = objectset1 & objectset2
	for (i, obj) in filteredenumerate(objectlist2, common):
		if args.verbose:
			stderr.writeln("oradiff.py: diffing #{}/{} ".format(i+1, len(common)), df(obj))
		ddl1 = obj.createddl(connection1)
		ddl2 = obj.createddl(connection2)
		ddl1c = getcanonicalddl(ddl1, args.blank)
		ddl2c = getcanonicalddl(ddl2, args.blank)
		if ddl1c != ddl2c:
			if args.mode == "brief":
				stdout.writeln(df(obj), ": different")
			elif args.mode == "full":
				stdout.writeln(comment(df(obj), ": different"))
				stdout.write(obj.createddl(connection2))
			elif args.mode == "udiff":
				showudiff(stdout, obj, ddl1c, ddl2c, connection1, connection2, args.context)


if __name__ == "__main__":
	sys.exit(main())
