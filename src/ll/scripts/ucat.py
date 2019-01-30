#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
=======

:program:`ucat` is a script for printing files. It is an URL-enabled version of
the :command:`cat` system command. Via :mod:`ll.url` and :mod:`ll.orasql`
:program:`ucat` supports ``ssh`` and ``oracle`` URLs.


Options
=======

:program:`ucat` supports the following options:

.. program:: ucat

.. option:: urls

	One or more URLs to be printed.

.. option:: -r <flag>, --recursive <flag>

	Prints directory content recursively.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -x <flag>, --ignoreerrors <flag>

	Ignores file i/o errors occurring during the output process (otherwise
	the script will be aborted).
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -i <pattern(s)>, --include <pattern(s)>

	Only print files whose name matches one of the specified patterns.

.. option:: -e <pattern(s)>, --exclude <pattern(s)>

	Don't print files whose name matches one of the specified patterns.

.. option:: --enterdir <pattern(s)>

	Only enter directories whose name matches one of the specified patterns.

.. option:: --skipdir <pattern(s)>

	Don't enter directories whose name matches one of the specified patterns.


Examples
========

Print a file:

.. sourcecode:: bash

	$ ucat foo.txt

Print a remote file:

.. sourcecode:: bash

	$ ucat ssh://user@www.example.org/~/foo.txt

Print the SQL source code of the procedure ``FOO`` in an Oracle database:

.. sourcecode:: bash

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

	p = argparse.ArgumentParser(description="print URL content on the screen", epilog="For more info see http://python.livinglogic.de/scripts_ucat.html")
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
