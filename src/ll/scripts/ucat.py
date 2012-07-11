#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Purpose
-------

``ucat`` is a script for printing files. It is an URL-enabled version of the
``cat`` system command. Via :mod:`ll.url` and :mod:`ll.orasql` ``ucat`` supports
``ssh`` and ``oracle`` URLs too.


Options
-------

``ucat`` supports the following options:

	``urls``
		One or more URLs to be printed.

	``-r``, ``--recursive`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Prints directory content recursively.

	``-x``, ``--ignoreerrors`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Ignores file i/o errors occuring during the output process. (Otherwise
		the script will be aborted.)

	``-i``, ``--include`` : regular expression
		Only print files that contain the regular expression.

	``-e``, ``--exclude`` : regular expression
		Don't print files that contain the regular expression.

	``-a``, ``--all`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Include dot files (i.e. files whose name starts with a ``.``). Not that
		the content of directories whose name starts with a dot will still be
		printed.


Examples
--------
Print a file::

	$ ucat foo.txt

Print a remote file::

	$ ucat ssh://user@www.example.org/~/foo.txt

Print the SQL source code of the procedure ``FOO`` in an Oracle database::

	$ ucat oracle://user:pwd@oracle.example.org/procedure/FOO

"""


import sys, re, argparse, contextlib, errno

from ll import misc, url

try:
	import astyle
except ImportError:
	from ll import astyle

try:
	from ll import orasql # activate the oracle scheme
except ImportError:
	pass


__docformat__ = "reStructuredText"


def main(args=None):
	def match(url):
		strurl = str(url)
		if args.include is not None and args.include.search(strurl) is None:
			return False
		if args.exclude is not None and args.exclude.search(strurl) is not None:
			return False
		if not args.all:
			if url.file:
				name = url.file
			elif len(url.path) >=2:
				name = url.path[-2]
			else:
				name = ""
			if name.startswith("."):
				return False
		return True

	def catone(urlread):
		if urlread.isdir():
			if args.recursive:
				for u in urlread.listdir():
					catone(urlread/u)
			else:
				raise IOError(errno.EISDIR, "Is a directory", str(urlread))
		else:
			if match(urlread):
				try:
					with contextlib.closing(urlread.open("rb")) as fileread:
						size = 0
						while True:
							data = fileread.read(262144)
							if data:
								sys.stdout.buffer.write(data)
							else:
								break
				except Exception:
					if not args.ignoreerrors:
						raise

	p = argparse.ArgumentParser(description="print URL content on the screen", epilog="For more info see http://www.livinglogic.de/Python/scripts/ucat.html")
	p.add_argument("urls", metavar="url", help="URLs to be printed", nargs="+", type=url.URL)
	p.add_argument("-r", "--recursive", dest="recursive", help="Print stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN (default: %(default)s)", type=re.compile)
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN (default: %(default)s)", type=re.compile)
	p.add_argument("-a", "--all", dest="all", help="Include dot files? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)
	with url.Context():
		for u in args.urls:
			catone(u)


if __name__ == "__main__":
	sys.exit(main())
