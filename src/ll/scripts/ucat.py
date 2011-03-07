#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


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
								sys.stdout.write(data)
							else:
								break
				except Exception:
					if not args.ignoreerrors:
						raise

	p = argparse.ArgumentParser(description="print URL content on the screen")
	p.add_argument("urls", metavar="url", help="URLs to be printed", nargs="+", type=url.URL)
	p.add_argument("-r", "--recursive", dest="recursive", help="Copy stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
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
