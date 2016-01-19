#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``udiff`` is a script that can be used to show the differences between files
or directories. It is an URL-enabled version of the ``diff`` system command.
Via :mod:`ll.url` and :mod:`ll.orasql` ``udiff`` supports ``ssh`` and
``oracle`` URLs.


Options
-------

``udiff`` supports the following options:

	``url1``
		The first URL to be compared (Note that a trailing ``/`` is required for
		directories).

	``url2``
		The second URL to be compared (Note that a trailing ``/`` is required for
		directories).

	``--encoding`` : encoding name
		The encoding name to use for decoding files (default ``utf-8``).

	``--errors`` : encoding error handler name
		Encoding error handling to use for reading text files (e.g. ``strict``,
		``replace``, ``ignore``, ``xmlcharrefreplace`` or ``backslashreplace``;
		default ``replace``).

	``--color``: ``yes``, ``no`` or ``auto``
		Should the output of ``udiff`` be colored? The default ``auto`` uses
		coloring if ``stdout`` supports it.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Prints which files are compare before the comparison. Without ``-v1``
		``udiff`` will be silent as long as no differences are detected.

	``-r``, ``--recursive`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Compare directories recursively.

	``-i``, ``--include`` : pattern(s)
		Only compares files whose name matches one of the specified patterns.

	``-e``, ``--exclude`` : pattern(s)
		Don't compares files whose name matches one of the specified patterns.

	``--enterdir`` : pattern(s)
		Only enter directories whose name matches one of the specified patterns.

	``--skipdir`` : pattern(s)
		Don't enter directories whose name matches one of the specified patterns.

	``-n``, ``--context`` : integer
		How many lines of copied context to show (default 2).

	``-b``, ``--blank`` : ``literal``, ``trail``, ``lead``, ``both`` or ``collapse``
		How to compare whitespace within lines. ``literal`` compares whitespace
		literally. ``trail`` ignores differences in trailing whitespace, ``lead``
		ignores differences in leading whitespace, ``both`` ignores both leading
		and trailing whitespace and ``collapse`` collapses whitespace into a single
		space before comparing lines.


Examples
--------

Compare two files::

	$ udiff foo.txt bar.txt

Recursively compare two directories, but skip the ``.git`` directory::

	$ udiff foo/ bar/ -r --skipdir=.git

Recursively compare two Oracle schemas::

	$ udiff oracle://user1:pwd@database1  oracle://user2:pwd@database2 -r
"""


import sys, re, argparse, contextlib, datetime, pwd, grp, stat, curses, difflib

from ll import misc, url

try:
	import astyle
except ImportError:
	from ll import astyle

try:
	from ll import orasql # Activate oracle URLs
except ImportError:
	pass


__docformat__ = "reStructuredText"


s4comment = astyle.Style.fromstr("black:black:bold")
s4addedfile = astyle.Style.fromstr("black:green")
s4addedline = astyle.Style.fromstr("green:black")
s4removedfile = astyle.Style.fromstr("black:red")
s4removedline = astyle.Style.fromstr("red:black")
s4changedfile = astyle.Style.fromstr("black:blue")
s4changedline = astyle.Style.fromstr("blue:black")
s4pos = astyle.Style.fromstr("black:black:bold")


class Line:
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


def main(args=None):
	def comparedirs(url1, url2):
		if args.recursive:
			iter1 = url1.walkfiles(include=args.include, exclude=args.exclude, enterdirs=args.enterdir, skipdirs=args.skipdir)
			iter2 = url2.walkfiles(include=args.include, exclude=args.exclude, enterdirs=args.enterdir, skipdirs=args.skipdir)
		else:
			iter1 = iter(url1.files(include=args.include, exclude=args.exclude))
			iter2 = iter(url2.files(include=args.include, exclude=args.exclude))

		file1 = file2 = None
		while True:
			if file1 is None:
				try:
					file1 = next(iter1)
				except StopIteration:
					if file2 is not None:
						yield (None, None, url2, file2)
					for file2 in iter2:
						yield (None, None, url2, file2)
					break
			if file2 is None:
				try:
					file2 = next(iter2)
				except StopIteration:
					if file1 is not None:
						yield (url1, file1, None, None)
					for file1 in iter1:
						yield (url1, file1, None, None)
					break
			str1 = str(file1)
			str2 = str(file2)
			if str1 < str2:
				yield (None, None, url1, file1)
				file1 = None
			elif str1 > str2:
				yield (None, None, url2, file2)
				file2 = None
			else:
				yield (url1, file1, url2, file2)
				file1 = file2 = None

	def comparefiles(url1, url2):
		def header(prefix, style, url):
			if prefix:
				return style("{} {}".format(prefix, url))
			else:
				return style(str(url))

		lines1 = [Line(line[:-1], args.blank) for line in url1.open("r", encoding=args.encoding, errors=args.errors)]
		lines2 = [Line(line[:-1], args.blank) for line in url2.open("r", encoding=args.encoding, errors=args.errors)]

		if args.verbose:
			stderr.writeln(header("", s4comment, "diff {} {}".format(url1, url2)))
		started = False
		for group in difflib.SequenceMatcher(None, lines1, lines2).get_grouped_opcodes(args.context):
			if not started:
				stdout.writeln(header("---", s4removedfile, url1))
				stdout.writeln(header("+++", s4addedfile, url2))
				started = True
			(i1, i2, j1, j2) = group[0][1], group[-1][2], group[0][3], group[-1][4]
			stdout.writeln(s4pos("@@ -{},{} +{},{} @@".format(i1+1, i2-i1, j1+1, j2-j1)))
			for (tag, i1, i2, j1, j2) in group:
				if tag == "equal":
					for line in lines1[i1:i2]:
						stdout.writeln(" {}".format(line.originalline))
					continue
				if tag == "replace" or tag == "delete":
					for line in lines1[i1:i2]:
						stdout.writeln(s4removedline("-", line.originalline))
				if tag == "replace" or tag == "insert":
					for line in lines2[j1:j2]:
						stdout.writeln(s4addedline("+", line.originalline))

	p = argparse.ArgumentParser(description="Compare files line by line", epilog="For more info see http://www.livinglogic.de/Python/scripts/udiff.html")
	p.add_argument("url1", metavar="url1", help="first URL (directories require a trailing /)", type=url.URL)
	p.add_argument("url2", metavar="url2", help="second URL (directories require a trailing /)", type=url.URL)
	p.add_argument(      "--encoding", dest="encoding", help="Encoding to use for reading text files (default: %(default)s)", default="utf-8")
	p.add_argument(      "--errors", dest="errors", help="Encoding error handling to use for reading text files (default: %(default)s)", default="replace")
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-r", "--recursive", dest="recursive", help="Recursively compare directories? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN", action="append")
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN", action="append")
	p.add_argument(      "--enterdir", dest="enterdir", metavar="PATTERN", help="Only enter directories matching PATTERN", action="append")
	p.add_argument(      "--skipdir", dest="skipdir", metavar="PATTERN", help="Skip directories matching PATTERN", action="append")
	p.add_argument("-n", "--context", dest="context", help="Number of context lines (default %(default)s)", type=int, default=2)
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


	with url.Context():
		if not args.url1.exists():
			print("{} doesn't exist".format(args.url1))
			return 1
		if not args.url2.exists():
			print("{} doesn't exist".format(args.url2))
			return 1
		if args.url1.isfile():
			if args.url2.isfile():
				comparefiles(args.url1, args.url2)
			else:
				print("Can't compare file {} with directory {}".format(args.url1, args.url2))
				return 1
		else:
			if args.url2.isfile():
				print("Can't compare directory {} with file {}".format(args.url1, args.url2))
				return 1
			else:
				for (url1, file1, url2, file2) in comparedirs(args.url1, args.url2):
					if url1 is None:
						stdout.writeln(str(file2), ": only in ", str(url2))
					elif url2 is None:
						stdout.writeln(str(file1), ": only in ", str(url1))
					else:
						comparefiles(url1/file1, url2/file2)


if __name__ == "__main__":
	sys.exit(main())
