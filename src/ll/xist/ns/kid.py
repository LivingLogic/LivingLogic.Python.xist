#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2005-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This module is an &xist; namespace for
<link href="http://kid.lesscode.org/">Kid</link> files.
"""

__version__ = "$Revision$".split()[1]
# $Source$


from ll.xist import xsc, sims


xmlns = "http://purl.org/kid/ns#"


class Attrs(xsc.Attrs):
	"""
	Global attributes.
	"""
	class for_(xsc.TextAttr):
		"""
		The <class>for_</class> attribute may appear on any element to signify
		that the element should be processed multiple times, once for each
		value in the sequence specified.
		"""
		xmlns = xmlns
		xmlname = "for"

	class if_(xsc.TextAttr):
		"""
		The <class>if_</class> attribute may appear on any element to signify
		that the element and its decendant items should be output only if the
		boolean expression specified evaluates to true in Python.
		"""
		xmlns = xmlns
		xmlname = "if"

	class content(xsc.TextAttr):
		"""
		This attribute may appear on any element to signify that the decendant
		items of the element are to be replaced with the result of evaluating
		the attribute content as a Python expression.
		"""
		xmlns = xmlns

	class replace(xsc.TextAttr):
		"""
		<class>replace</class> is shorthand for specifying a
		<class>content</class> and a <markup>strip="True"</markup>
		on the same element.
		"""
		xmlns = xmlns

	class strip(xsc.TextAttr):
		"""
		The <class>strip</class> attribute may apppear on any element to
		signify that the containing element should not be output.
		"""
		xmlns = xmlns

	class attrs(xsc.TextAttr):
		"""
		The <class>attrs</class> attribute may appear on any element to
		specify a set of attributes that should be set on the element
		when it is processed.
		"""
		xmlns = xmlns

	class def_(xsc.TextAttr):
		"""
		The <class>def_</class> attribute may appear on any element to
		create a <z>Named Template Function</z>.
		"""
		xmlns = xmlns
		xmlname = "def"

	class match(xsc.TextAttr):
		"""
		The <class>match</class> attribute may appear on any element to
		create a <z>Match Template</z>.
		"""
		xmlns = xmlns

	class extends(xsc.TextAttr):
		"""
		The <class>extends</class> attribute may appear on the root element
		to specify that the template should inherit the Named Template Functions
		and Match Templates defined in another template (or set of templates).
		"""
		xmlns = xmlns


class python(xsc.ProcInst):
	"""
	The <class>python</class> processing instruction contains Python code.
	"""
