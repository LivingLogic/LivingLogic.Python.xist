#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, optparse, contextlib, errno

from ll import url

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
			if options.recursive:
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
				if not options.ignoreerrors:
					raise

	colors = ("yes", "no", "auto")
	p = optparse.OptionParser(usage="usage: %prog [options] source-file-url target-file-url\n   or: %prog [options] source-file-url(s) target-dir-url")
	p.add_option("-v", "--verbose", dest="verbose", help="Be verbose?", action="store_true", default=False)
	p.add_option("-r", "--recursive", dest="recursive", help="Copy stuff recursively?", action="store_true", default=False)
	p.add_option("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors?", action="store_true", default=False)
	
	(options, args) = p.parse_args(args)
	if len(args) < 1:
		p.error("need at least one url")
		return 1

	with url.Context():
		for arg in args:
			catone(url.URL(arg))


if __name__ == "__main__":
	sys.exit(main())
