# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True


from ll.xist import xsc


xmlns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


class RDF(xsc.Element):
	xmlns = xmlns


class Attrs(xsc.Attrs):
	class about(xsc.TextAttr):
		xmlns = xmlns
	class resource(xsc.TextAttr):
		xmlns = xmlns
