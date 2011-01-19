#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, argparse, contextlib, errno

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
	def catone(urlread):
		if urlread.isdir():
			if args.recursive:
				for u in urlread.listdir():
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
							sys.stdout.write(data)
						else:
							break
			except Exception:
				if not args.ignoreerrors:
					raise

	p = argparse.ArgumentParser(description="print URL content on the screen")
	p.add_argument("urls", metavar="url", help="URLs to be printed", nargs="+", type=url.URL)
	p.add_argument("-v", "--verbose", dest="verbose", help="Be verbose? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-r", "--recursive", dest="recursive", help="Copy stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)
	with url.Context():
		for u in args.urls:
			catone(u)


if __name__ == "__main__":
	sys.exit(main())
