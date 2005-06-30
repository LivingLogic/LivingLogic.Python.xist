# -*- coding: iso-8859-1 -*-


from ll.xist import xsc


class type(xsc.Element):
	pass


class __ns__(xsc.Namespace):
	xmlname = "dc"
	xmlurl = "http://purl.org/dc/elements/1.1/"
__ns__.makemod(vars())
