#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import sys, optparse

from xml.sax import sax2exts, handler, xmlreader

from ll.xist import xsc, xnd, sims


class Handler(handler.ErrorHandler, handler.ContentHandler, handler.DTDHandler, handler.EntityResolver):
	def __init__(self, name, url, sims):
		self.name = name
		self.url = url
		self.sims = sims
		self.xnd = None # will be set by startDocument()
		self.stack = None # will be set by startDocument()
		self.elements = {} # maps name to (xnd.Element, content set, attrname->xnd.Attr map)
		self.entities = {} # maps name to xnd.Entity
		self.procinsts = {} # maps name to xnd.ProcInst

	def error(self, exception):
		print "error: %r" % exception
		raise exception

	def fatalError(self, exception):
		print "fatalError: %r" % exception
		raise exception

	def warning(self, exception):
		print "warning: %r" % exception

	def startDocument(self):
		self.xnd = xnd.Namespace(self.name, url=self.url)
		self.stack = []

	def endDocument(self):
		# Put sims info into the element definitions
		if self.sims == "none":
			pass
		elif self.sims == "simple":
			for entry in self.elements.itervalues():
				entry[0].modeltype = bool(entry[1])
		elif self.sims == "full":
			for entry in self.elements.itervalues():
				if not entry[1]:
					entry[0].modeltype = "sims.Empty"
				else:
					elements = [el for el in entry[1] if not el.startswith("#")]
					if not elements:
						if "#text" in entry[1]:
							entry[0].modeltype = "sims.NoElements"
						else:
							entry[0].modeltype = "sims.NoElementsOrText"
					else:
						if "#text" in entry[1]:
							entry[0].modeltype = "sims.ElementsOrText"
						else:
							entry[0].modeltype = "sims.Elements"
						entry[0].modelargs = [self.xnd.element(el) for el in elements]
		else:
			raise ValueError("unknown sims mode %r" % self.sims)

	def startElement(self, name, attrs):
		if name not in self.elements:
			element = xnd.Element(name)
			entry = self.elements[name] = (element, set(), {})
			self.xnd(element)
		else:
			entry = self.elements[name]
		for attrname in attrs.keys():
			if attrname != "xmlns" and not attrname.startswith("xmlns:") and attrname not in entry[2]:
				attr = xnd.Attr(attrname, type=xsc.TextAttr)
				entry[0](attr)
				entry[2][attrname] = attr
		if self.stack:
			self.stack[-1][1].add(name)
		self.stack.append(entry)

	def endElement(self, name):
		self.stack.pop(-1)

	#def startPrefixMapping(self, prefix, uri):

	#def endPrefixMapping(self, prefix):

	#def startElementNS(self, name, qname, attrs):

	#def endElementNS(self, name, qname):

	def characters(self, content):
		if self.stack and content:
			if content.isspace():
				self.stack[-1][1].add("#whitespace")
			else:
				self.stack[-1][1].add("#text")

	def entity(self, name):
		self.skippedEntity(name)

	def ignorableWhitespace(self, whitespace):
		if self.stack:
			self.stack[-1][1].add("#whitespace")

	def comment(self, content):
		if self.stack:
			self.stack[-1][1].add("#comment")

	def processingInstruction(self, target, data):
		if self.stack:
			self.stack[-1][1].add("#procinst")
		if target not in self.procinsts:
			procinst = xnd.ProcInst(target)
			self.procinsts[name] = procinst
			self.xnd(procinst)

	def skippedEntity(self, name):
		if self.stack:
			self.stack[-1][1].add("#entity")
		if name not in self.entities:
			entity = xnd.Entity(name)
			self.entities[name] = entity
			self.xnd(entity)


def stream2xnd(stream, name="foo", url="http://www.example.com/foons", sims="simple", parser=None):
	if parser is None or parser==[]:
		from ll.xist import parsers
		parser = parsers.SGMLOPParser()
	elif isinstance(parser, list):
		parser = sax2exts.make_parser(parser)
	
	app = Handler(name, url, sims)

	parser.setErrorHandler(app)
	parser.setContentHandler(app)
	parser.setDTDHandler(app)
	parser.setEntityResolver(app)

	#parser.setFeature(handler.feature_namespaces, 1)
	parser.setFeature(handler.feature_external_ges, False) # Don't process external entities, but pass them to skippedEntity
	
	source = xmlreader.InputSource()
	source.setByteStream(stream)

	parser.parse(source)
	
	return app.xnd


def main():
	p = optparse.OptionParser(usage="usage: %prog [options] <input.xml >output.py")
	p.add_option("-n", "--name", dest="name", help="xmlname for the new namespace", default="foo")
	p.add_option("-u", "--url", dest="url", help="xmlurl for the new namespace", default="http://www.example.com/foons")
	p.add_option("-p", "--parser", dest="parser", help="parser module to use for XML parsing", action="append", default=[])
	choices = ["none", "simple", "full"]
	p.add_option("-s", "--sims", dest="sims", help="Create sims info? (%s)" % ", ".join(choices), metavar="MODE", default="simple")

	(options, args) = p.parse_args()
	if len(args) != 0:
		p.error("incorrect number of arguments")
		return 1
	print stream2xnd(sys.stdin, name=options.name, url=options.url, sims=options.sims, parser=options.parser).aspy()


if __name__ == "__main__":
	sys.exit(main())
