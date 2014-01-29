#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

from ll.xist import xsc, parse
from ll.xist.ns import xml, html, meta


import qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns

url = "http://www.amk.ca/quotations/python-quotes.xml"


if __name__ == "__main__":
	pool = xsc.Pool(html, xml, qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns)
	base = "root:python-quotes.html"
	e = parse.tree(parse.URL(url), parse.Expat(ns=True), parse.Node(pool=pool, base=base), validate=False)
	e = e[qel_xmlns.quotations][0]
	e = e.compacted().conv()
	print(e.string(base=base, encoding="iso-8859-1", validate=False))
