# -*- coding: iso-8859-1 -*-


from ll.xist import xsc, sims
from ll.xist.ns import html, meta


class RDF(xsc.Element):
	pass


class __ns__(xsc.Namespace):
	xmlname = "rdf"
	xmlurl = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

	class Attrs(xsc.Namespace.Attrs):
		class about(xsc.TextAttr): pass
		class resource(xsc.TextAttr): pass

__ns__.makemod(vars())
