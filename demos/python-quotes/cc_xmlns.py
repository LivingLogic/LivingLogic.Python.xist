# -*- coding: iso-8859-1 -*-


from ll.xist import xsc, sims


class license(xsc.Element):
	model = sims.Empty()


class Work(xsc.Element):
	model = sims.Elements(license)


class permits(xsc.Element):
	model = sims.Empty()


class requires(xsc.Element):
	model = sims.Empty()


class License(xsc.Element):
	model = sims.Elements(permits, requires)


class __ns__(xsc.Namespace):
	xmlname = "cc"
	xmlurl = "http://web.resource.org/cc/"
__ns__.makemod(vars())
