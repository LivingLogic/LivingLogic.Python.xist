#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


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

Note that ``dtd2xsc`` requires lxml_ to work.

	.. _lxml: http://lxml.de/


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


import sys, os.path, argparse, io, operator

from ll import misc, url
from ll.xist import xsc, parse, xnd


__docformat__ = "reStructuredText"


def getxmlns(dtd):
	# Extract the value of all fixed ``xmlns`` attributes
	found = set()
	for elemdecl in dtd.iterelements(): # This requires ``lxml`` version 2.4
		for attrdecl in elemdecl.iterattributes():
			if attrdecl.name=="xmlns" or ":" in attrdecl.name:
				if attrdecl.default == "fixed":
					found.add(attrdecl.default_value)
					continue # skip a namespace declaration
	return found


def adddtd2xnd(ns, dtd):
	# Appends DTD information from :obj:`dtd` to the :class:`xnd.Module` object
	from lxml import etree # This requires lxml (http://lxml.de/)
	dtd = etree.DTD(dtd)

	# try to guess the namespace name from the dtd
	xmlns = getxmlns(dtd)
	if len(xmlns) == 1:
		xmlns = next(iter(xmlns))
	else:
		xmlns = None

	namegetter = operator.attrgetter("name")
	# Add element info
	elements = sorted(dtd.iterelements(), key=namegetter)
	for elemdecl in elements:
		e = xnd.Element(xmlns, elemdecl.name)

		# Add attribute info for this element
		attrs = sorted(elemdecl.iterattributes(), key=namegetter)
		for attrdecl in attrs:
			if attrdecl.name=="xmlns" or attrdecl.prefix:
				continue # skip namespace declarations and global attributes
			values = []
			if attrdecl.type == "id":
				type = "xsc.IDAttr"
			else:
				type = "xsc.TextAttr"
				values = attrdecl.values()
				if len(values) == 1:
					type = "xsc.BoolAttr"
					values = None
				elif not values:
					values = None
			default = attrdecl.default_value
			if attrdecl.default == "required":
				required = True
			else:
				required = None
			e += xnd.Attr(name=attrdecl.name, type=type, default=default, required=required, values=values)
		ns += e

	# Iterate through the elements a second time and add model information
	for elemdecl in elements:
		if elemdecl.type == "empty":
			modeltype = "sims.Empty"
			modelargs = None
		elif elemdecl.type == "any":
			modeltype = "sims.Any"
			modelargs = None
		else:
			def extractcont(model):
				content = set()
				if model is not None:
					content.update(extractcont(model.left))
					if model.name is not None:
						content.add(model.name)
					content.update(extractcont(model.right))
				return content
			elementcontent = extractcont(elemdecl.content)
			if elementcontent:
				modelargs = [ns.elements[(xmlns, name)] for name in elementcontent]
				if elemdecl.type == "mixed":
					modeltype = "sims.ElementsOrText"
				else:
					modeltype = "sims.Elements"
			else:
				modelargs = []
				if elemdecl.type == "mixed":
					modeltype = "sims.NoElements"
				else:
					modeltype = "sims.NoElementsOrText"
		e = ns.elements[(xmlns, elemdecl.name)]
		if ns.model == "simple":
			modeltype = modeltype == "sims.Empty"
			modelargs = None
		e.modeltype = modeltype
		e.modelargs = modelargs

	# Add entities
	entities = sorted(dtd.iterentities(), key=namegetter)
	for entdecl in entities:
		if entdecl.name not in ("quot", "apos", "gt", "lt", "amp") and entdecl.content and len(entdecl.content) == 1:
			ns += xnd.CharRef(entdecl.name, codepoint=ord(entdecl.content))


def urls2xnd(urls, shareattrs=None, **kwargs):
	ns = xnd.Module(**kwargs)
	with url.Context():
		if not urls:
			urls = [sys.stdin]
		for u in urls:
			if isinstance(u, url.URL):
				u = u.openread()
			elif isinstance(u, str):
				u = io.StringIO(u)
			adddtd2xnd(ns, u)

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
	print(urls2xnd(**args.__dict__))


if __name__ == "__main__":
	sys.exit(main())
