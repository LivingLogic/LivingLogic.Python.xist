# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import misc
from ll.xist import xsc


###
### Processing instructions for output
###

class print_(xsc.ProcInst):
	"""
	Prints the expression in the processing instruction data.
	"""
	xmlname = "print"


class printx(xsc.ProcInst):
	"""
	Prints the expression in the processing instruction data and escapes
	the characters ``&``, ``<``, ``>``, ``'`` and ``"``.
	"""


###
### Processing instruction for statements
###

class code(xsc.ProcInst):
	"""
	A :class:`code` processing instruction contains a statement (such as an
	assignment or augmented assignment).
	"""


###
### Processing instruction for calling sub-templates
###

class render(xsc.ProcInst):
	"""
	A :class:`render` processing instruction calls another template.
	"""


###
### Processing instructions for conditional attributes
###

class attr_ifnn(xsc.AttrProcInst):
	"""
	Conditional attribute: If this PI is used as the first in an attribute, it's
	value is treated as an expression. If this expression is not ``None`` it is
	output as the value of the attribute, otherwise the attribute itself will be
	skipped.
	"""

	def publishattr(self, publisher, attr):
		yield publisher.encode(u'<?if not isnone(%s)?> %s="<?printx %s?>"<?end if?>' % (self.content, attr._publishname(publisher), self.content))

	def publishboolattr(self, publisher, attr):
		name = attr._publishname(publisher)
		yield publisher.encode(u"<?if not isnone(%s)?> %s" % (self.content, name))
		if publisher.xhtml>0:
			yield publisher.encode(u'="%s"' % name)
		yield publisher.encode(u'<?end if?>')


class attr_if(xsc.AttrProcInst):
	"""
	Conditional attribute: If this PI is used as the first in an attribute, it's
	value is treated as an expression. If this expression is true, the attribute
	will be output normally, otherwise the attribute itself will be skipped.
	"""

	def publishattr(self, publisher, attr):
		publisher.inattr += 1
		yield publisher.encode(u'<?if %s?> %s="' % (self.content, attr._publishname(publisher)))
		publisher.pushtextfilter(misc.xmlescape_attr)
		for part in attr._publishattrvalue(publisher):
			yield part
		publisher.poptextfilter()
		yield publisher.encode(u'"<?end if?>')
		publisher.inattr -= 1

	def publishboolattr(self, publisher, attr):
		name = attr._publishname(publisher)
		yield publisher.encode(u"<?if %s?> %s" % (self.content, name))
		if publisher.xhtml>0:
			yield publisher.encode(u'="%s"' % name)
		yield publisher.encode(u'<?end if?>')


###
### Processing instructions for block structures (if/elif/else/for and def)
###

class if_(xsc.ProcInst):
	xmlname = "if"


class elif_(xsc.ProcInst):
	xmlname = "elif"


class else_(xsc.ProcInst):
	xmlname = "else"


class end(xsc.ProcInst):
	"""
	Ends an :class:`if_` or :class:`for_`. The PI value may be the type of the
	block (either ``"if"`` or ``"for"``). If the value is empty the innermost
	block will be closed without any checks for the type of block.
	"""


class for_(xsc.ProcInst):
	xmlname = "for"


class break_(xsc.ProcInst):
	xmlname = "break"


class continue_(xsc.ProcInst):
	xmlname = "continue"


class def_(xsc.ProcInst):
	xmlname = "def"
