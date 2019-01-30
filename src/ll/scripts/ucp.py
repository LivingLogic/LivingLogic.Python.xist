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

:program:`ucp` is a script that copies files or directories. It is an
URL-enabled version of the :command:`cp` system command. Via :mod:`ll.url` and
:mod:`ll.orasql` :program:`ucp` supports ``ssh`` and ``oracle`` URLs.


Options
=======

:program:`ucp` supports the following options:

.. program:: ucp

.. option:: urls

	Two or more URLs. If more than two URLs are given or the last URL refers
	to an existing directory, the last URL is the target directory. All other
	sources are copied into this target directory. Otherwise one file is
	copied to another file.

.. option:: -v <flag>, --verbose <flag>

	Give a report during the copy process about the files copied and their
	sizes?
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -c <mode>, --color <mode>

	Should the output be colored? If ``auto`` is specified (the default) then
	the output is colored if stdout is a terminal. Valid modes are ``yes``,
	``no`` or ``auto``.

.. option:: -u <user>, --user <user>

	A user id or name. If given :program:`ucp` will change the owner of the
	target files.

.. option:: -g <group>, --group <group>

	A group id or name. If given :program:`ucp` will change the group of the
	target files.

.. option:: -r <flag>, --recursive <flag>

	Copies files recursively.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -x <flag>, --ignoreerrors <flag>

	Ignores errors occurring during the copy process (otherwise the copy
	process is aborted).
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -i <pattern(s)>, --include <pattern(s)>

	Only copy files that match one of the specified patterns.

.. option:: -e <pattern(s)>, --exclude <pattern(s)>

	Don't copy files that match one of the specified patterns.

.. option:: --enterdir <pattern(s)>

	Only enter directories that match one of the specified patterns.

.. option:: --skipdir <pattern(s)>

	Skip directories that match one of the specified patterns.

.. option:: --ignorecase <flag>

	Perform case-insensitive pattern matching?
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)


Examples
========

Copy one file to another:

.. sourcecode:: bash

	$ ucp foo.txt bar.txt

Copy a file into an existing directory:

.. sourcecode:: bash

	$ ucp foo.txt dir/

Copy multiple files into a new or existing directory (and give a progress
report):

.. sourcecode:: bash

	$ ucp foo.txt bar.txt baz.txt dir/ -v
	ucp: foo.txt -> dir/foo.txt (1,114 bytes)
	ucp: bar.txt -> dir/bar.txt (2,916 bytes)
	ucp: baz.txt -> dir/baz.txt (35,812 bytes)

Recursively copy the schema objects in an Oracle database to a local directory:

.. sourcecode:: bash

	ucp oracle://user:pwd@oracle.example.org/ db/ -r

Recursively copy the schema objects in an Oracle database to a remote directory:

.. sourcecode:: bash

	ucp oracle://user:pwd@oracle.example.org/ ssh://user@www.example.org/~/db/ -r
"""


import sys, re, argparse, contextlib

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
	def copyone(urlread, urlwrite):
		strurlread = str(urlread)
		if urlread.isdir():
			if args.recursive:
				for u in urlread.walkfiles(include=args.include, exclude=args.exclude, enterdir=args.enterdir, skipdir=args.skipdir, ignorecase=args.ignorecase):
					copyone(urlread/u, urlwrite/u)
			else:
				if args.verbose:
					msg = astyle.style_default("ucp: ", astyle.style_url(strurlread), astyle.style_warn(" (directory skipped)"))
					stderr.writeln(msg)
		else:
			if args.verbose:
				msg = astyle.style_default("ucp: ", astyle.style_url(strurlread), " -> ")
				stderr.write(msg)
			try:
				with contextlib.closing(urlread.open("rb")) as fileread:
					with contextlib.closing(urlwrite.open("wb")) as filewrite:
						size = 0
						while True:
							data = fileread.read(262144)
							if data:
								filewrite.write(data)
								size += len(data)
							else:
								break
				if user or group:
					urlwrite.chown(user, group)
			except Exception as exc:
				if args.ignoreerrors:
					if args.verbose:
						exctype = misc.format_class(exc)
						excmsg = str(exc).replace("\n", " ").strip()
						msg = astyle.style_error(f" (failed with {exctype}: {excmsg})")
						stderr.writeln(msg)
				else:
					raise
			else:
				if args.verbose:
					msg = astyle.style_default(astyle.style_url(str(urlwrite)), f" ({size:,} bytes)")
					stderr.writeln(msg)

	p = argparse.ArgumentParser(description="Copies URLs", epilog="For more info see http://python.livinglogic.de/scripts_ucp.html")
	p.add_argument("urls", metavar="url", help="either one source and one target file, or multiple source files and one target dir", nargs="*", type=url.URL)
	p.add_argument("-v", "--verbose", dest="verbose", help="Be verbose? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-u", "--user", dest="user", help="user id or name for target files")
	p.add_argument("-g", "--group", dest="group", help="group id or name for target files")
	p.add_argument("-r", "--recursive", dest="recursive", help="Copy stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN", action="append")
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN", action="append")
	p.add_argument(      "--enterdir", dest="enterdir", metavar="PATTERN", help="Only enter directories matching PATTERN", action="append")
	p.add_argument(      "--skipdir", dest="skipdir", metavar="PATTERN", help="Skip directories matching PATTERN", action="append")
	p.add_argument(      "--ignorecase", dest="ignorecase", help="Perform case-insensitive name matching? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)
	if len(args.urls) < 2:
		p.error("need at least one source url and one target url")
		return 1

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	user = args.user
	try:
		user = int(user)
	except (TypeError, ValueError):
		pass

	group = args.group
	try:
		group = int(group)
	except (TypeError, ValueError):
		pass

	with url.Context():
		urls = args.urls
		if len(urls) > 2 or urls[-1].isdir(): # treat target as directory
			for u in urls[:-1]:
				copyone(u, urls[-1]/u.file)
		else:
			copyone(urls[0], urls[-1])


if __name__ == "__main__":
	sys.exit(main())
