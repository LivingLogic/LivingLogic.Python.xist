#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from ll.xist import xsc, parsers
from ll.xist.ns import xml, html, meta


import qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns

urls = ("python-quotes.xml", "http://www.amk.ca/quotations/python-quotes.xml")


if __name__ == "__main__":
	nspool = xsc.NSPool(html, xml, qel_xmlns, rdf_xmlns, rdfs_xmlns, cc_xmlns, dc_xmlns)
	prefixes = xsc.Prefixes(xml=xml)
	base = "root:python-quotes.html"
	e = None
	for url in urls:
		try:
			e = parsers.parseURL(url, base=base, saxparser=parsers.ExpatParser, nspool=nspool, prefixes=prefixes, validate=False)
		except IOError:
			pass
	if e is not None:
		e = e[qel_xmlns.quotations][0]
		e = e.compact().conv()
		e.write(open("python-quotes.html", "wb"), base=base, encoding="iso-8859-1", validate=False)
	else:
		raise IOError("can't load XML")
