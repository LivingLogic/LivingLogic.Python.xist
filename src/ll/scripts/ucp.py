#!/usr/local/bin/python
# -*- coding: utf-8 -*-


## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


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

	def copyone(urlread, urlwrite):
		strurlread = str(urlread)
		if urlread.isdir():
			if args.recursive:
				for u in urlread.listdir():
					copyone(urlread/u, urlwrite/u)
			else:
				if args.verbose:
					msg = astyle.style_default("ucp: ", astyle.style_url(strurlread), astyle.style_warn(" (directory skipped)"))
					stderr.writeln(msg)
		else:
			if match(urlread):
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
				except Exception, exc:
					if args.ignoreerrors:
						if args.verbose:
							excname = exc.__class__.__name__
							excmodule = exc.__class__.__module__
							if excmodule != "exceptions":
								excname = "{}.{}".format(excmodule, excname)
							excmsg = str(exc).replace("\n", " ").strip()
							msg = astyle.style_error(" (failed with {}: {})".format(excname, excmsg))
							stderr.writeln(msg)
					else:
						raise
				else:
					if args.verbose:
						msg = astyle.style_default(astyle.style_url(str(urlwrite)), " (", str(size), " bytes)")
						stderr.writeln(msg)
			else:
				if args.verbose:
					msg = astyle.style_default("ucp: ", astyle.style_url(strurlread), astyle.style_warn(" (skipped)"))
					stderr.writeln(msg)

	p = argparse.ArgumentParser(description="Copies URLs")
	p.add_argument("urls", metavar="url", help="either one source and one target file, or multiple source files and one target dir", nargs="*", type=url.URL)
	p.add_argument("-v", "--verbose", dest="verbose", help="Be verbose? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-u", "--user", dest="user", help="user id or name for target files")
	p.add_argument("-g", "--group", dest="group", help="group id or name for target files")
	p.add_argument("-r", "--recursive", dest="recursive", help="Copy stuff recursively? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--include", dest="include", metavar="PATTERN", help="Include only URLs matching PATTERN (default: %(default)s)", type=re.compile)
	p.add_argument("-e", "--exclude", dest="exclude", metavar="PATTERN", help="Exclude URLs matching PATTERN (default: %(default)s)", type=re.compile)
	p.add_argument("-a", "--all", dest="all", help="Include dot files? (default: %(default)s)", action=misc.FlagAction, default=False)

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
