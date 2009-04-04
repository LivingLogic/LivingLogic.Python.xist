#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2009 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from __future__ import with_statement

import sys, optparse, contextlib, datetime, pwd, grp, stat, curses

from ll import url

try:
	import astyle
except ImportError:
	from ll import astyle

style_pad = astyle.Style.fromstr("black:black:bold")

def rpad(s, l):
	s = str(s)
	if len(s) < l:
		return astyle.style_default(s, style_pad("."*(l-len(s))))
	return s

def lpad(s, l):
	s = str(s)
	if len(s) < l:
		return astyle.style_default(style_pad("."*(l-len(s))), s)
	return s

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
	def printone(url, long):
		if long:
			stat = url.stat()
			if stat.st_uid not in uids:
				user = uids[stat.st_uid] = pwd.getpwuid(stat.st_uid)[0]
			else:
				user = uids[stat.st_uid]
			if stat.st_gid not in gids:
				group = gids[stat.st_gid] = grp.getgrgid(stat.st_gid)[0]
			else:
				group = gids[stat.st_gid]
			mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
			mode = "".join([text[bool(stat.st_mode&bit)] for (bit, text) in modedata])
			stdout.write(mode, sep, rpad(user, 8), sep, rpad(group, 8), sep, lpad(stat.st_size, 10), sep, lpad(stat.st_nlink, 3), sep, mtime, sep)
		if url.isdir():
			stdout.writeln(astyle.style_dir(str(url)))
		else:
			stdout.writeln(astyle.style_file(str(url)))

	def printall(base, url, one, long, recursive):
		if url.isdir():
			if url.path.segments[-1][0]:
				url.path.segments.append(("",))
			if recursive:
				for child in url.listdir():
					printone(url/child, long)
					printall(base, url/child, one, long, recursive)
			else:
				for child in url.listdir():
					printone((url/child).relative(base), long)
		else:
			printone(url, long)

	colors = ("yes", "no", "auto")
	p = optparse.OptionParser(usage="usage: %prog [options] [url] [url] ...")
	p.add_option("-c", "--color", dest="color", help="Color output (%s)" % ", ".join(colors), default="auto", choices=colors)
	p.add_option("-1", "--one", dest="one", help="One entry per line?", action="store_true")
	p.add_option("-l", "--long", dest="long", help="Long format?", action="store_true")
	p.add_option("-r", "--recursive", dest="recursive", help="Recursive listing?", action="store_true")
	
	(options, args) = p.parse_args(args)

	if options.color == "yes":
		color = True
	elif options.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	if not args:
		args = ["."]

	with url.Context():
		for u in args:
			u = url.URL(u)
			printall(u, u, options.one, options.long, options.recursive)


if __name__ == "__main__":
	sys.exit(main())
