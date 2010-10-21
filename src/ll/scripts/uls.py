#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, argparse, contextlib, datetime, pwd, grp, stat, curses

from ll import url

try:
	import astyle
except ImportError:
	from ll import astyle

try:
	from ll import orasql # Activate oracle URLs
except ImportError:
	pass


style_file = astyle.Style.fromstr("white:black")
style_dir = astyle.Style.fromstr("yellow:black")
style_pad = astyle.Style.fromstr("black:black:bold")
style_sizeunit = astyle.Style.fromstr("cyan:black")


def rpad(s, l):
	meas = str(s)
	if not isinstance(s, (basestring, astyle.Text)):
		s = str(s)
	if len(meas) < l:
		return astyle.style_default(s, style_pad("."*(l-len(meas))))
	return s


def lpad(s, l):
	meas = str(s)
	if not isinstance(s, (basestring, astyle.Text)):
		s = str(s)
	if len(meas) < l:
		return astyle.style_default(style_pad("."*(l-len(meas))), s)
	return s


def findcolcount(urls, width, spacing):
	def width4cols(numcols, spacing):
		cols = [0]*numcols
		rows = (len(urls)+numcols-1)//numcols
		for (i, (u, su)) in enumerate(urls):
			cols[i//rows] = max(cols[i//rows], len(su))
		return (sum(cols) + (numcols-1)*spacing, rows, cols)

	numcols = len(urls)
	while True:
		(s, rows, cols) = width4cols(numcols, spacing)
		if s <= width or numcols == 1:
			return (rows, cols)
		numcols -=1


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
	sep = style_pad("|")
	curses.setupterm()
	width = curses.tigetnum('cols')
	def printone(url, long, human):
		if long:
			stat = url.stat()
			owner = url.owner()
			group = url.group()
			mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
			mode = "".join([text[bool(stat.st_mode&bit)] for (bit, text) in modedata])
			size = stat.st_size
			if human:
				s = "BKMGTP"
				for c in s:
					if size < 2048:
						if c == "B":
							size = str(int(size))
						else:
							size = astyle.style_default(str(int(size)), style_sizeunit(c))
						break
					size /= 1024.
			stdout.write(mode, sep, rpad(owner, 8), sep, rpad(group, 8), sep, lpad(size, 5 if human else 12), sep, lpad(stat.st_nlink, 3), sep, mtime, sep)
		if url.isdir():
			stdout.writeln(style_dir(str(url)))
		else:
			stdout.writeln(style_file(str(url)))

	def printblock(url, urls, width, spacing):
		if url is not None:
			stdout.writeln(style_dir(str(url)), ":")
		(rows, cols) = findcolcount(urls, width, spacing)
		for i in xrange(rows):
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
						su = rpad(su, w+spacing)
					stdout.write(su)
			stdout.writeln()

	def printall(base, url, one, long, recursive, human, spacing):
		if url.isdir():
			if url.path.segments[-1]:
				url.path.segments.append("")
			if not long and not one:
				if recursive:
					urls = [(url/child, str(child)) for child in url.files()]
					if urls:
						printblock(url, urls, width, spacing)
					for child in url.dirs():
						printall(base, url/child, one, long, recursive, human, spacing)
				else:
					urls = [(url/child, str(child)) for child in url.listdir()]
					printblock(None, urls, width, spacing)
			else:
				for child in url.listdir():
					printone(url/child, long, human)
					if recursive:
						printall(base, url/child, one, long, recursive, human, spacing)
		else:
			printone(url, long, human)

	p = argparse.ArgumentParser(description="List the content of one or more URLs")
	p.add_argument("urls", metavar="url", help="URLs to be listed (default: current dir)", nargs="*", default=url.here(), type=url.URL)
	p.add_argument("-c", "--color", dest="color", help="Color output", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-1", "--one", dest="one", help="One entry per line?", action="store_true")
	p.add_argument("-l", "--long", dest="long", help="Long format?", action="store_true")
	p.add_argument("-s", "--human-readable-sizes", dest="human", help="Human readable file sizes?", action="store_true")
	p.add_argument("-r", "--recursive", dest="recursive", help="Recursive listing?", action="store_true")
	p.add_argument("-w", "--spacing", dest="spacing", metavar="N", help="Number of spaces between columns", type=int, default=3)

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
		for u in args.urls:
			printall(u, u, args.one, args.long, args.recursive, args.human, args.spacing)


if __name__ == "__main__":
	sys.exit(main())
