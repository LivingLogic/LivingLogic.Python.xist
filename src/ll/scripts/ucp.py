#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, argparse, contextlib

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
	def copyone(urlread, urlwrite):
		if urlread.isdir():
			if args.recursive:
				for u in urlread.listdir():
					copyone(urlread/u, urlwrite/u)
			else:
				if args.verbose:
					msg = astyle.style_default("ucp: ", astyle.style_url(str(urlread)), " (directory skipped)")
					stderr.writeln(msg)
		else:
			if args.verbose:
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
				if args.ignoreerrors:
					if args.verbose:
						msg = astyle.style_error(" (failed)")
						stderr.writeln(msg)
				else:
					raise
			else:
				if args.verbose:
					msg = astyle.style_default(astyle.style_url(str(urlwrite)), " (", str(size), " bytes)")
					stderr.writeln(msg)

	p = argparse.ArgumentParser(description="Copies URLs")
	p.add_argument("urls", metavar="url", help="either one source and one target file, or multiple source files and one target dir", nargs="*", type=url.URL)
	p.add_argument("-v", "--verbose", dest="verbose", help="Be verbose? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-u", "--user", dest="user", help="user id or name for target files")
	p.add_argument("-g", "--group", dest="group", help="group id or name for target files")
	p.add_argument("-r", "--recursive", dest="recursive", help="Copy stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)

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
