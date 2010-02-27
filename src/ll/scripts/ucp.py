#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, optparse, contextlib

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
	def copyone(urlread, urlwrite):
		if urlread.isdir():
			if options.recursive:
				for u in urlread.listdir():
					copyone(urlread/u, urlwrite/u)
			else:
				if options.verbose:
					msg = astyle.style_default("ucp: ", astyle.style_url(str(urlread)), " (directory skipped)")
					stderr.writeln(msg)
		else:
			if options.verbose:
				msg = astyle.style_default("ucp: ", astyle.style_url(str(urlread)), " -> ")
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
			except Exception:
				if options.ignoreerrors:
					if options.verbose:
						msg = astyle.style_error(" (failed)")
						stderr.writeln(msg)
				else:
					raise
			else:
				if options.verbose:
					msg = astyle.style_default(astyle.style_url(str(urlwrite)), " (", str(size), " bytes)")
					stderr.writeln(msg)
				


	colors = ("yes", "no", "auto")
	p = optparse.OptionParser(usage="usage: %prog [options] source-file-url target-file-url\n   or: %prog [options] source-file-url(s) target-dir-url")
	p.add_option("-v", "--verbose", dest="verbose", help="Be verbose?", action="store_true", default=False)
	p.add_option("-c", "--color", dest="color", help="Color output (%s)" % ", ".join(colors), default="auto", choices=colors)
	p.add_option("-u", "--user", dest="user", help="user id or name for target files")
	p.add_option("-g", "--group", dest="group", help="group id or name for target files")
	p.add_option("-r", "--recursive", dest="recursive", help="Copy stuff recursively?", action="store_true", default=False)
	p.add_option("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors?", action="store_true", default=False)
	
	(options, args) = p.parse_args(args)
	if len(args) < 2:
		p.error("need at least one source url and one target url")
		return 1

	if options.color == "yes":
		color = True
	elif options.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	user = options.user
	try:
		user = int(user)
	except (TypeError, ValueError):
		pass

	group = options.group
	try:
		group = int(group)
	except (TypeError, ValueError):
		pass

	with url.Context():
		args = [url.URL(arg) for arg in args]
		if len(args) > 2 or args[-1].isdir(): # treat target as directory
			for arg in args[:-1]:
				copyone(arg, args[-1]/arg.file)
		else:
			copyone(args[0], args[-1])


if __name__ == "__main__":
	sys.exit(main())
