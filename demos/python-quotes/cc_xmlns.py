# -*- coding: utf-8 -*-


from ll.xist import xsc, sims


class xmlns(xsc.Namespace):
	xmlname = "cc"
	xmlurl = "http://web.resource.org/cc/"


class license(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()


class Work(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(license)


class permits(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()


class requires(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()


class License(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(permits, requires)
