#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2011 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Purpose
-------

``dtd2xsc`` is a script that helps create XIST namespace modules from DTDs.
It reads one or more DTDs and outputs a skeleton namespace module.


Options
-------

``dtd2xsc`` supports the following options:

	``urls``
		Zero or more URLs (or filenames) of DTDs to be parsed. If no URL is
		given stdin will be read.

	``-x``, ``--xmlns``
		The default namespace name. All elements that don't belong to any
		namespace will be assigned to this namespace.

	``-s``, ``--shareattrs`` : ``none``, ``dupes``, ``all``
		Should attributes be shared among the elements? ``none`` means that each
		element will have its own standalone :class:`Attrs` class directly derived
		from :class:`ll.xist.Elements.Attrs`. For ``dupes`` each attribute that is
		used by more than one element will be moved into its own :class:`Attrs`
		class. For ``all`` this will be done for all attributes.

	``-m``, ``--model`` : ``no``, ``simple``, ``fullall``, ``fullonce``
		Add model information to the namespace. ``no`` doesn't add any model
		information. ``simple`` only adds ``model = False`` or ``model = True``
		(i.e. only the information whether the element must be empty or not).
		``fullall`` adds a :mod:`ll.xist.sims` model object to each element class.
		``fullonce`` adds full model information to, but reuses model objects for
		elements which have the same model.

	``-d``, ``--defaults`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Should default values for attributes specified in the DTD be added to the
		XIST namespace (as the ``default`` specification in the attribute class)?

	``--duplicates`` : ``reject``, ``allow``, ``merge``
		If more that one DTD is specified on the command line, some elements
		might be specified in more than one DTD. ``--duplicates`` specifies how
		to handle this case: ``reject`` doesn't allow multiple element
		specifications. ``allow`` allows them, but only if both specifications
		are identical (i.e. have the same attributes). ``merge`` allows them and
		adds the attribute specification of all element specifications to the
		resulting XIST namespace.

Note that ``dtd2xsc`` requires xmlproc_ to work.

	.. _xmlproc: http://www.garshol.priv.no/download/software/xmlproc/


Example
-------

Suppose we have the following DTD file (named ``foo.dtd``)::

	<?xml version="1.0" encoding="ISO-8859-1"?>
	<!ELEMENT persons (person*)>
	<!ELEMENT person (firstname?, lastname?)>
	<!ATTLIST person id CDATA #REQUIRED>
	<!ELEMENT firstname (#PCDATA)>
	<!ELEMENT lastname (#PCDATA)>

Then we can generate a skeleton XIST namespace from it with the following command::

	dtd2xsc ~/gurk.dtd -xhttp://xmlns.example.org/ -mfullall

The output will be::

	# -*- coding: ascii -*-


	from ll.xist import xsc, sims


	xmlns = 'http://xmlns.example.org/'


	class firstname(xsc.Element): xmlns = xmlns


	class lastname(xsc.Element): xmlns = xmlns


	class person(xsc.Element):
		xmlns = xmlns
		class Attrs(xsc.Element.Attrs):
			class id(xsc.TextAttr): required = True


	class persons(xsc.Element): xmlns = xmlns


	person.model = sims.Elements(lastname, firstname)
	persons.model = sims.Elements(person)
	firstname.model = sims.NoElements()
	lastname.model = sims.NoElements()
"""


import sys, os.path, argparse, cStringIO

try:
	from xml.parsers.xmlproc import dtdparser
except ImportError:
	try:
		from xmlproc import dtdparser
	except ImportError:
		dtdparser = None

from ll import misc, url
from ll.xist import xsc, parse, xnd


__docformat__ = "reStructuredText"


def getxmlns(dtd):
	# Extract the value of all fixed ``xmlns`` attributes
	found = set()
	for elemname in dtd.get_elements():
		element = dtd.get_elem(elemname)
		for attrname in element.get_attr_list():
			attr = element.get_attr(attrname)
			if attrname=="xmlns" or u":" in attrname:
				if attr.decl=="#FIXED":
					found.add(attr.default)
					continue # skip a namespace declaration
	return found


def adddtd2xnd(ns, dtd):
	# Appends DTD information from :var:`dtd` to the :class:`xnd.Module` object
	dtd = dtdparser.load_dtd_string(dtd) # This requires ``xmlproc``

	# try to guess the namespace name from the dtd
	xmlns = getxmlns(dtd)
	if len(xmlns) == 1:
		xmlns = iter(xmlns).next()
	else:
		xmlns = None

	# Add element info
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		dtd_e = dtd.get_elem(elemname)
		e = xnd.Element(elemname, xmlns=xmlns)

		# Add attribute info for this element
		attrs = dtd_e.get_attr_list()
		if len(attrs):
			attrs.sort()
			for attrname in attrs:
				dtd_a = dtd_e.get_attr(attrname)
				if attrname=="xmlns" or u":" in attrname:
					continue # skip namespace declarations and global attributes
				values = []
				if dtd_a.type == "ID":
					type = "xsc.IDAttr"
				else:
					type = "xsc.TextAttr"
					if isinstance(dtd_a.type, list):
						if len(dtd_a.type) > 1:
							values = dtd_a.type
						else:
							type = "xsc.BoolAttr"
				default = dtd_a.default
				if dtd_a.decl=="#REQUIRED":
					required = True
				else:
					required = None
				e += xnd.Attr(name=attrname, type=type, default=default, required=required, values=values)
		ns += e

	# Iterate through the elements a second time and add model information
	for elemname in elements:
		e = dtd.get_elem(elemname)
		model = e.get_content_model()
		if model is None:
			modeltype = "sims.Any"
			modelargs = None
		elif model == ("", [], ""):
			modeltype = "sims.Empty"
			modelargs = None
		else:
			def extractcont(model):
				if len(model) == 3:
					result = {}
					for cont in model[1]:
						result.update(extractcont(cont))
					return result
				else:
					return {model[0]: None}
			model = extractcont(model)
			modeltype = "sims.Elements"
			modelargs = []
			for cont in model:
				if cont == "#PCDATA":
					modeltype = "sims.ElementsOrText"
				elif cont == "EMPTY":
					modeltype = "sims.Empty"
				else:
					modelargs.append(ns.elements[(cont, xmlns)])
			if not modelargs:
				if modeltype == "sims.ElementsOrText":
					modeltype = "sims.NoElements"
				else:
					modeltype = "sims.NoElementsOrText"
		e = ns.elements[(elemname, xmlns)]
		if ns.model == "simple":
			modeltype = modeltype == "sims.Empty"
			modelargs = None
		e.modeltype = modeltype
		e.modelargs = modelargs

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			try:
				ent = parse.tree(dtd.resolve_ge(entname).value, parse.Encoder("utf-8"), parse.SGMLOP(encoding="utf-8"), parse.NS(), parse.Node())
			except xsc.IllegalEntityError:
				pass
			else:
				ns += xnd.CharRef(entname, codepoint=ord(unicode(ent[0])[0]))


def urls2xnd(urls, shareattrs=None, **kwargs):
	ns = xnd.Module(**kwargs)
	with url.Context():
		if not urls:
			urls = [sys.stdin]
		for u in urls:
			if isinstance(u, url.URL):
				u = u.openread()
			elif isinstance(u, str):
				u = cStringIO.StringIO(u)
			adddtd2xnd(ns, u.read())

	if shareattrs=="dupes":
		ns.shareattrs(False)
	elif shareattrs=="all":
		ns.shareattrs(True)
	return ns


def main(args=None):
	p = argparse.ArgumentParser(description="Convert DTDs to XIST namespace (on stdout)", epilog="For more info see http://www.livinglogic.de/Python/xist/scripts/dtd2xsc.html")
	p.add_argument("urls", metavar="urls", type=url.URL, help="Zero of more URLs of DTDs to be parsed (default stdin)", nargs="*")
	p.add_argument("-x", "--xmlns", dest="defaultxmlns", metavar="NAME", help="the namespace name for this module")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements? (default: %(default)s)", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", default="fullonce", help="Add sims information to the namespace (default: %(default)s)", choices=("no", "simple", "fullall", "fullonce"))
	p.add_argument("-d", "--defaults", dest="defaults", help="Output default values for attributes? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument(      "--duplicates", dest="duplicates", help="How to handle duplicate elements from multiple DTDs (default: %(default)s)", choices=("reject", "allow", "merge"), default="reject")

	args = p.parse_args(args)
	print urls2xnd(**args.__dict__)


if __name__ == "__main__":
	sys.exit(main())
