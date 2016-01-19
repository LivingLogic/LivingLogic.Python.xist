#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``ucat`` is a script for printing files. It is an URL-enabled version of the
``cat`` system command. Via :mod:`ll.url` and :mod:`ll.orasql` ``ucat`` supports
``ssh`` and ``oracle`` URLs.


Options
-------

``ucat`` supports the following options:

	``urls``
		One or more URLs to be printed.

	``-r``, ``--recursive`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Prints directory content recursively.

	``-x``, ``--ignoreerrors`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Ignores file i/o errors occuring during the output process (otherwise
		the script will be aborted).

	``-i``, ``--include`` : pattern(s)
		Only print files whose name matches one of the specified patterns.

	``-e``, ``--exclude`` : pattern(s)
		Don't print files whose name matches one of the specified patterns.

	``--enterdir`` : pattern(s)
		Only enter directories whose name matches one of the specified patterns.

	``--skipdir`` : pattern(s)
		Don't enter directories whose name matches one of the specified patterns.


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
	def catone(urlread):
		if urlread.isdir():
			if args.recursive:
				for u in urlread.walkfiles(include=args.include, exclude=args.exclude, enterdirs=args.enterdir, skipdirs=args.skipdir):
					catone(urlread/u)
			else:
				raise IOError(errno.EISDIR, "Is a directory", str(urlread))
		else:
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
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN", action="append")
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN", action="append")
	p.add_argument(      "--enterdir", dest="enterdir", metavar="PATTERN", help="Only enter directories matching PATTERN", action="append")
	p.add_argument(      "--skipdir", dest="skipdir", metavar="PATTERN", help="Skip directories matching PATTERN", action="append")

	args = p.parse_args(args)
	with url.Context():
		for u in args.urls:
			catone(u)


if __name__ == "__main__":
	sys.exit(main())
