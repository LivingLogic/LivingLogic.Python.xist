#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``uls`` is a script that lists the content of directories. It is an URL-enabled
version of the ``ls`` system command. Via :mod:`ll.url` and :mod:`ll.orasql`
``uls`` supports ``ssh`` and ``oracle`` URLs.


Options
-------

``uls`` supports the following options:

	``urls``
		Zero or more URLs. If no URL is given the current directory is listed.

	``-c``, ``--color`` : ``yes``, ``no`` or ``auto``
		Should the output be colored? If ``auto`` is specified (the default) then
		the output is colored if stdout is a terminal.

	``-1``, ``--one`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Force output to be one URL per line. The default is to output URLs in
		multiple columns (as many as fit on the screen).

	``-l``, ``--long`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Ouput in long format: One URL per line containing the following information:
		file mode, owner name, group name, number of bytes in the file,
		number of links, URL.

	``-s``, ``--human-readable-sizes`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Output the file size in human readable form (e.g. ``42M`` for 42 megabytes).

	``-r``, ``--recursive`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		List directories recursively.

	``-w``, ``--spacing`` : integer
		The number of spaces (or padding characters) between columns (only
		relevant for multicolumn output, i.e. when neither ``--long`` nor
		``--one`` is specified).

	``-P``, ``--padding`` : characters
		The characters used for padding output in multicolumn or long format.

	``-i``, ``--include`` : pattern
		Only list files that match the pattern.

	``-e``, ``--exclude`` : pattern
		Don't list files that match the pattern.

	``--enterdir`` : pattern
		Only enter directories that match the pattern.

	``--skipdir`` : pattern
		Skip directories that match the pattern.

	``--ignorecase`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Perform case-insensitive pattern matching.


Examples
--------

List the current directory::

	$ uls
	CREDITS.rst   installer.bmp   NEWS.rst           scripts/    test/
	demos/        Makefile        OLDMIGRATION.rst   setup.cfg
	docs/         MANIFEST.in     OLDNEWS.rst        setup.py
	INSTALL.rst   MIGRATION.rst   README.rst         src/

List the current directory in long format with human readable file sizes::

	$ uls -s -l
	rw-r--r--  walter    staff      1114    1  2008-01-06 22:27:15  CREDITS.rst
	rwxr-xr-x  walter    staff       170    5  2007-12-03 23:35:33  demos/
	rwxr-xr-x  walter    staff       340   10  2010-12-08 16:48:53  docs/
	rw-r--r--  walter    staff        2K    1  2010-12-08 16:48:53  INSTALL.rst
	rw-r--r--  walter    staff       35K    1  2007-12-03 23:35:33  installer.bmp
	rw-r--r--  walter    staff      1763    1  2011-01-21 17:22:32  Makefile
	rw-r--r--  walter    staff       346    1  2011-02-25 11:13:18  MANIFEST.in
	rw-r--r--  walter    staff       34K    1  2011-03-04 13:48:35  MIGRATION.rst
	rw-r--r--  walter    staff      107K    1  2011-03-04 18:18:42  NEWS.rst
	rw-r--r--  walter    staff        8K    1  2010-12-08 16:48:53  OLDMIGRATION.rst
	rw-r--r--  walter    staff       75K    1  2010-12-08 16:48:53  OLDNEWS.rst
	rw-r--r--  walter    staff        3K    1  2010-12-08 16:48:53  README.rst
	rwxr-xr-x  walter    staff       578   17  2010-12-08 16:48:53  scripts/
	rw-r--r--  walter    staff        39    1  2010-12-08 16:48:53  setup.cfg
	rw-r--r--  walter    staff        7K    1  2011-03-03 13:33:21  setup.py
	rwxr-xr-x  walter    staff       136    4  2007-12-04 01:43:13  src/
	rwxr-xr-x  walter    staff        2K   68  2011-03-03 13:27:46  test/

Recursively list a remote directory::

	uls ssh://user@www.example.org/~/dir/ -r
	...

Recursively list the schema objects in an Oracle database::

	uls oracle://user:pwd@oracle.example.org/ -r
	...
"""


import sys, re, argparse, contextlib, datetime, pwd, grp, stat, curses

from ll import misc, url as url_

try:
	import astyle
except ImportError:
	from ll import astyle

try:
	from ll import orasql # Activate oracle URLs
except ImportError:
	pass


__docformat__ = "reStructuredText"


style_file = astyle.Style.fromstr("white:black")
style_dir = astyle.Style.fromstr("yellow:black")
style_pad = astyle.Style.fromstr("black:black:bold")
style_sizeunit = astyle.Style.fromstr("cyan:black")


def main(args=None):
	uids = {}
	gids = {}
	modedata = (
		(stat.S_IRUSR, "-r"),
		(stat.S_IWUSR, "-w"),
		(stat.S_IXUSR, "-x"),
		(stat.S_IRGRP, "-r"),
		(stat.S_IWGRP, "-w"),
		(stat.S_IXGRP, "-x"),
		(stat.S_IROTH, "-r"),
		(stat.S_IWOTH, "-w"),
		(stat.S_IXOTH, "-x"),
	)
	curses.setupterm()
	width = curses.tigetnum('cols')

	def rpad(s, l):
		meas = str(s)
		if not isinstance(s, (str, astyle.Text)):
			s = str(s)
		if len(meas) < l:
			size = l-len(meas)
			psize = len(args.padding)
			repeats = (size+psize-1)//psize
			padding = (args.padding*repeats)[-size:]
			return astyle.style_default(s, style_pad(padding))
		return s

	def lpad(s, l):
		meas = str(s)
		if not isinstance(s, (str, astyle.Text)):
			s = str(s)
		if len(meas) < l:
			size = l-len(meas)
			psize = len(args.padding)
			repeats = (size+psize-1)//psize
			padding = (args.padding*repeats)[:size]
			return astyle.style_default(style_pad(padding), s)
		return s

	def findcolcount(urls):
		def width4cols(numcols):
			cols = [0]*numcols
			rows = (len(urls)+numcols-1)//numcols
			for (i, (u, su)) in enumerate(urls):
				cols[i//rows] = max(cols[i//rows], len(su))
			return (sum(cols) + (numcols-1)*args.spacing, rows, cols)

		numcols = len(urls)
		if numcols:
			while True:
				(s, rows, cols) = width4cols(numcols)
				if s <= width or numcols == 1:
					return (rows, cols)
				numcols -= 1
		else:
			return (0, 0)

	def printone(url):
		if args.long:
			sep = style_pad(args.separator)
			stat = url.stat()
			owner = url.owner()
			group = url.group()
			mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
			mode = "".join([text[bool(stat.st_mode&bit)] for (bit, text) in modedata])
			size = stat.st_size
			if args.human:
				s = "BKMGTP"
				for c in s:
					if size < 2048:
						if c == "B":
							size = str(int(size))
						else:
							size = astyle.style_default(str(int(size)), style_sizeunit(c))
						break
					size /= 1024.
			stdout.write(mode, sep, rpad(owner, 8), sep, rpad(group, 8), sep, lpad(size, 5 if args.human else 12), sep, lpad(stat.st_nlink, 3), sep, mtime, sep)
		if url.isdir():
			stdout.writeln(style_dir(str(url)))
		else:
			stdout.writeln(style_file(str(url)))

	def printblock(url, urls):
		if url is not None:
			stdout.writeln(style_dir(str(url)), ":")
		(rows, cols) = findcolcount(urls)
		for i in range(rows):
			for (j, w) in enumerate(cols):
				index = i+j*rows
				try:
					(u, su) = urls[index]
				except IndexError:
					pass
				else:
					if u.isdir():
						su = style_dir(su)
					else:
						su = style_file(su)
					if index + rows < len(urls):
						su = rpad(su, w+args.spacing)
					stdout.write(su)
			stdout.writeln()

	def printall(base, url):
		if url.isdir():
			if url.path.segments[-1]:
				url.path.segments.append("")
			if not args.long and not args.one:
				if args.recursive:
					urls = [(url/child, str(child)) for child in url.files(include=args.include, exclude=args.exclude, ignorecase=args.ignorecase)]
					if urls:
						printblock(url, urls)
					for child in url.dirs():
						if url_.matchpatterns(child.path[-2], enterdir, skipdir):
							printall(base, url/child)
				else:
					urls = [(url/child, str(child)) for child in url.listdir(include=args.include, exclude=args.exclude, ignorecase=args.ignorecase)]
					printblock(None, urls)
			else:
				for child in url.listdir(include=args.include, exclude=args.exclude, ignorecase=args.ignorecase):
					child = url/child
					isdir = child.isdir()
					if not args.recursive or isdir: # For files the print call is done by the recursive call to ``printall``
						printone(child)
					if args.recursive and (not isdir or url_.matchpatterns(child.path[-2], enterdir, skipdir)):
						printall(base, child)
		else:
			printone(url)

	p = argparse.ArgumentParser(description="List the content of one or more URLs", epilog="For more info see http://www.livinglogic.de/Python/scripts/uls.html")
	p.add_argument("urls", metavar="url", help="URLs to be listed (default: current dir)", nargs="*", default=[url_.Dir("./", scheme=None)], type=url_.URL)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-1", "--one", dest="one", help="One entry per line? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-l", "--long", dest="long", help="Long format? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-s", "--human-readable-sizes", dest="human", help="Human readable file sizes? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-r", "--recursive", dest="recursive", help="Recursive listing? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-w", "--spacing", dest="spacing", metavar="INTEGER", help="Space between columns (default: %(default)s)", type=int, default=3)
	p.add_argument("-P", "--padding", dest="padding", metavar="CHARS", help="Characters used for column padding (default: %(default)s)", default=" ", type=str)
	p.add_argument("-S", "--separator", dest="separator", metavar="CHARS", help="Characters used for separating columns in long format (default: %(default)s)", default="  ", type=str)
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN", action="append")
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN", action="append")
	p.add_argument(      "--enterdir", dest="enterdir", metavar="PATTERN", help="Only enter directories matching PATTERN", action="append")
	p.add_argument(      "--skipdir", dest="skipdir", metavar="PATTERN", help="Skip directories matching PATTERN", action="append")
	p.add_argument(      "--ignorecase", dest="ignorecase", help="Perform case-insensitive name matching? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	enterdir = url_.compilepattern(args.enterdir, ignorecase=args.ignorecase)
	skipdir = url_.compilepattern(args.skipdir, ignorecase=args.ignorecase)

	with url_.Context():
		for u in args.urls:
			printall(u, u)


if __name__ == "__main__":
	sys.exit(main())
