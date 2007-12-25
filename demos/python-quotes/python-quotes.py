#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ll.xist import xsc, parsers
from ll.xist.ns import xml, html, meta


import qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns

url = "http://www.amk.ca/quotations/python-quotes.xml"


if __name__ == "__main__":
	pool = xsc.Pool(html, xml, qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns)
	base = "root:python-quotes.html"
	e = parsers.parseurl(url, base=base, parser=parsers.ExpatParser(), pool=pool, validate=False)
	e = e[qel_xmlns.quotations][0]
	e = e.compact().conv()
	print e.bytes(base=base, encoding="iso-8859-1", validate=False)
