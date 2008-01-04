# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>This module ontains functions related to the handling of &css;.</par>
"""

from __future__ import with_statement

import contextlib, operator

try:
	import cssutils
	from cssutils import css, stylesheets
except ImportError:
	cssutils = None
else:
	import logging
	cssutils.log.setloglevel(logging.FATAL)

from ll import misc, url
from ll.xist import xsc, xfind
from ll.xist.ns import html


def _isstyle(path):
	if path:
		node = path[-1]
		return (isinstance(node, html.style) and unicode(node.attrs["type"]) == "text/css") or (isinstance(node, html.link) and unicode(node.attrs["rel"]) == "stylesheet")
	return False


def replaceurls(stylesheet, replacer):
	"""
	Replace all &url;s appearing in the <class>CSSStyleSheet<class>
	<arg>stylesheet</arg>. For each &url; the function <arg>replacer</arg> will
	be called and the &url; will be replaced with the result.
	"""
	def newreplacer(u):
		return unicode(replacer(url.URL(u)))
	stylesheet.replaceUrls(newreplacer) # This needs at least r242 of cssutils


def _getmedia(stylesheet):
	while stylesheet is not None:
		if stylesheet.media is not None:
			return set(mq.mediaType for mq in stylesheet.media)
		stylesheet = stylesheet.parentStyleSheet
	return None


def _doimport(wantmedia, parentsheet, base):
	def prependbase(u):
		if base is not None:
			u = base/u
		return u

	havemedia = _getmedia(parentsheet)
	if wantmedia is None or not havemedia or wantmedia in havemedia:
		for rule in parentsheet.cssRules:
			if rule.type == css.CSSRule.IMPORT_RULE:
				href = url.URL(rule.href)
				if base is not None:
					href = base/href
				havemedia = rule.media
				with contextlib.closing(href.open("rb")) as r:
					href = r.finalurl()
					text = r.read()
				sheet = css.CSSStyleSheet(href=str(href), media=havemedia, parentStyleSheet=parentsheet)
				sheet.cssText = text
				replaceurls(sheet, prependbase)
				for rule in _doimport(wantmedia, sheet, href):
					yield rule
			elif rule.type == css.CSSRule.MEDIA_RULE:
				if wantmedia in (mq.mediaType for mq in rule.media):
					for subrule in rule.cssRules:
						yield subrule
			elif rule.type == css.CSSRule.STYLE_RULE:
				yield rule


def iterrules(node, base=None, media=None):
	"""
	<par>Return an iterator for all &css; rules defined in the &html; tree <arg>node</arg>.
	This will parse the &css; defined in any <class>html.style</class> or
	<class>html.link</class> element (and recursively in those stylesheets imported
	via the <lit>@import</lit> rule). The rules will be returned as
	<class>CSSStyleRule</class> objects from the <module>cssutils</module> package
	(so this requires <module>cssutils</module>).</par>

	<par>The <arg>base</arg> argument will be used as the base &url; for parsing
	the stylesheet references in the tree (so <lit>None</lit> means the &url;s
	will be used exactly as they appear in the tree). All &url;s in the style
	properties will be resolved.</par>

	<par>If <arg>media</arg> is given, only rules that apply to this media type
	will be produced.</par>
	"""
	if base is not None:
		base = url.URL(base)

	def doiter(node, base, media):
		for cssnode in node.walknode(_isstyle):
			if isinstance(cssnode, html.style):
				href = str(self.base) if base is not None else None
				if cssnode.attrs.media.hasmedia(media):
					stylesheet = cssutils.parseString(unicode(cssnode.content), href=href, media=unicode(cssnode.attrs.media))
					for rule in _doimport(media, stylesheet, base):
						yield rule
			else: # link
				if "href" in cssnode.attrs:
					href = cssnode.attrs["href"].asURL()
					if base is not None:
						href = self.base/href
					if cssnode.attrs.media.hasmedia(media):
						with contextlib.closing(href.open("rb")) as r:
							s = r.read()
						stylesheet = cssutils.parseString(unicode(s), href=str(href), media=unicode(cssnode.attrs.media))
						for rule in _doimport(media, stylesheet, href):
							yield rule
	return misc.Iterator(doiter(node, base, media))


def applystylesheets(node, base=None, media=None):
	"""
	<par><function>applystylesheets</function> modifies the &xist; tree <arg>node</arg>
	by removing all &css; (from <class>html.link</class> and <class>html.style</class>
	elements and their <lit>@import</lit>ed stylesheets) and puts the resulting
	styles properties into the <lit>style</lit> attribute of the every affected
	element instead.</par>
	
	<par>The <arg>base</arg> argument will be used as the base &url; for parsing
	the stylesheet references in the tree (so <lit>None</lit> means the &url;s
	will be used exactly as they appear in the tree). All &url;s in the style
	properties will be resolved.</par>

	<par>If <arg>media</arg> is given, only rules that apply to this media type
	will be applied.</par>
	"""
	def iterstyles(node, rules):
		if "style" in node.attrs:
			style = node.attrs["style"]
			if not style.isfancy():
				styledata = (
					xfind.CSSWeight(1, 0, 0),
					xfind.IsSelector(node),
					cssutils.parseString(u"*{%s}" % style).cssRules[0].style # parse the style out of the style attribute
				)
				# put the style attribute into the order as the last of the selectors with ID weight (see http://www.w3.org/TR/REC-CSS1#cascading-order)
				def doiter():
					done = False
					for data in rules:
						if not done and data[0] > styledata[0]:
							yield styledata
							done = True
						yield data
					if not done:
						yield styledata
				return doiter()
		return rules

	rules = []
	for (i, rule) in enumerate(iterrules(node, base=base, media=media)):
		for sel in rule.selectorList:
			sel = selector(sel)
			rules.append((sel.cssweight(), sel, rule.style))
	rules.sort(key=operator.itemgetter(0))
	count = 0
	for path in node.walk(xsc.Element):
		del path[-1][_isstyle] # drop style sheet nodes
		if path[-1].Attrs.isallowed("style"):
			styles = {}
			for (weight, sel, style) in iterstyles(path[-1], rules):
				if sel.matchpath(path):
					for prop in style.seq:
						if not isinstance(prop, css.CSSComment):
							styles[prop.name] = (count, prop.name, prop.cssValue.cssText)
							count += 1
					style = " ".join("%s: %s;" % (name, value) for (count, name, value) in sorted(styles.itervalues()))
					if style:
						path[-1].attrs["style"] = style


###
### Selector helper functions
###

def _is_nth_node(iterator, node, index):
	# Return whether node is the index'th node in iterator (starting at 1)
	# index is an int or int string or "even" or "odd"
	if index == "even":
		for (i, child) in enumerate(iterator):
			if child is node:
				return i % 2 == 1
		return False
	elif index == "odd":
		for (i, child) in enumerate(iterator):
			if child is node:
				return i % 2 == 0
		return False
	else:
		if not isinstance(index, (int, long)):
			try:
				index = int(index)
			except ValueError:
				raise ValueError("illegal argument %r" % index)
			else:
				if index < 1:
					return False
		try:
			return iterator[index-1] is node
		except IndexError:
			return False


def _is_nth_last_node(iterator, node, index):
	# Return whether node is the index'th last node in iterator
	# index is an int or int string or "even" or "odd"
	if index == "even":
		pos = None
		for (i, child) in enumerate(iterator):
			if child is node:
				pos = i
		return pos is None or (i-pos) % 2 == 1
	elif index == "odd":
		pos = None
		for (i, child) in enumerate(iterator):
			if child is node:
				pos = i
		return pos is None or (i-pos) % 2 == 0
	else:
		if not isinstance(index, (int, long)):
			try:
				index = int(index)
			except ValueError:
				raise ValueError("illegal argument %r" % index)
			else:
				if index < 1:
					return False
		try:
			return iterator[-index] is node
		except IndexError:
			return False


def _children_of_type(node, type):
	for child in node:
		if isinstance(child, xsc.Element) and child.xmlname == type:
			yield child


###
### Selectors
###

class CSSWeightedSelector(xfind.Selector):
	"""
	Base class for all &css; pseudo-class selectors.
	"""
	def cssweight(self):
		return xfind.CSSWeight(0, 1, 0)


class CSSHasAttributeSelector(CSSWeightedSelector):
	"""
	A <class>CSSHasAttributeSelector</class> selector selects all element nodes
	that have an attribute with the specified &xml; name.
	"""
	def __init__(self, attributename):
		self.attributename = attributename

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				return node.attrs.has_xml(self.attributename)
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.attributename)


class CSSAttributeListSelector(CSSWeightedSelector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				attr = node.attrs.get_xml(self.attributename)
				return self.attributevalue in unicode(attr).split()
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)


class CSSAttributeLangSelector(CSSWeightedSelector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				attr = node.attrs.get_xml(self.attributename)
				parts = unicode(attr).split("-", 1)
				if parts:
					return parts[0] == self.attributevalue
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)


class CSSFirstChildSelector(CSSWeightedSelector):
	def matchpath(self, path):
		return len(path) >= 2 and _is_nth_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return "CSSFirstChildSelector()"


class CSSLastChildSelector(CSSWeightedSelector):
	def matchpath(self, path):
		return len(path) >= 2 and _is_nth_last_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return "CSSLastChildSelector()"


class CSSFirstOfTypeSelector(CSSWeightedSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			return isinstance(node, xsc.Element) and _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
		return False

	def __str__(self):
		return "CSSFirstOfTypeSelector()"


class CSSLastOfTypeSelector(CSSWeightedSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			return isinstance(node, xsc.Element) and _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
		return False

	def __str__(self):
		return "CSSLastOfTypeSelector()"


class CSSOnlyChildSelector(CSSWeightedSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in path[-2][xsc.Element]:
					if child is not node:
						return False
				return True
		return False

	def __str__(self):
		return "CSSOnlyChildSelector()"


class CSSOnlyOfTypeSelector(CSSWeightedSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in _children_of_type(path[-2], node.xmlname):
					if child is not node:
						return False
				return True
		return False

	def __str__(self):
		return "CSSOnlyOfTypeSelector()"


class CSSEmptySelector(CSSWeightedSelector):
	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in path[-1].content:
					if isinstance(child, xsc.Element) or (isinstance(child, xsc.Text) and child):
						return False
				return True
		return False

	def __str__(self):
		return "CSSEmptySelector()"


class CSSRootSelector(CSSWeightedSelector):
	def matchpath(self, path):
		return len(path) == 1 and isinstance(path[-1], xsc.Element)

	def __str__(self):
		return "CSSRootSelector()"


class CSSLinkSelector(CSSWeightedSelector):
	def matchpath(self, path):
		if path:
			node = path[-1]
			return isinstance(node, xsc.Element) and node.xmlns=="http://www.w3.org/1999/xhtml" and node.xmlname=="a" and "href" in node.attrs
		return False

	def __str__(self):
		return "%s()" % self.__class__.__name__


class CSSInvalidPseudoSelector(CSSWeightedSelector):
	def matchpath(self, path):
		return False

	def __str__(self):
		return "%s()" % self.__class__.__name__


class CSSHoverSelector(CSSInvalidPseudoSelector):
	pass


class CSSActiveSelector(CSSInvalidPseudoSelector):
	pass


class CSSVisitedSelector(CSSInvalidPseudoSelector):
	pass


class CSSFocusSelector(CSSInvalidPseudoSelector):
	pass


class CSSAfterSelector(CSSInvalidPseudoSelector):
	pass


class CSSBeforeSelector(CSSInvalidPseudoSelector):
	pass


class CSSFunctionSelector(CSSWeightedSelector):
	def __init__(self, value=None):
		self.value = value

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.value)


class CSSNthChildSelector(CSSFunctionSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_node(path[-2][xsc.Element], node, self.value)
		return False


class CSSNthLastChildSelector(CSSFunctionSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_last_node(path[-2][xsc.Element], node, self.value)
		return False


class CSSNthOfTypeSelector(CSSFunctionSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, self.value)
		return False


class CSSNthLastOfTypeSelector(CSSFunctionSelector):
	def matchpath(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, self.value)
		return False


class CSSTypeSelector(xfind.Selector):
	def __init__(self, type="*", xmlns="*", *selectors):
		self.type = type
		self.xmlns = xsc.nsname(xmlns)
		self.selectors = [] # id, class, attribute etc. selectors for this node

	def matchpath(self, path):
		if path:
			node = path[-1]
			if self.type == "*" or node.xmlname == self.type:
				if self.xmlns == "*" or node.xmlns == self.xmlns:
					for selector in self.selectors:
						if not selector.matchpath(path):
							return False
					return True
		return False

	def __str__(self):
		v = [self.__class__.__name__, "("]
		if self.type != "*" or self.xmlns != "*" or self.selectors:
			v.append(repr(self.type))
		if self.xmlns != "*" or self.selectors:
			v.append(", ")
			v.append(repr(self.xmlns))
		for selector in self.selectors:
			v.append(", ")
			v.append(str(selector))
		v.append(")")
		return "".join(v)

	def cssweight(self):
		result = xfind.CSSWeight(0, 0, int(self.type != "*"))
		for selector in self.selectors:
			result += selector.cssweight()
		return result


class CSSAdjacentSiblingCombinator(xfind.BinaryCombinator):
	"""
	<par>A <class>CSSAdjacentSiblingCombinator</class> work similar to an
	<class>AdjacentSiblingCombinator</class> except that only preceding elements
	are considered.</par>
	"""

	def matchpath(self, path):
		if len(path) >= 2 and self.right.matchpath(path):
			# Find sibling
			node = path[-1]
			sibling = None
			for child in path[-2][xsc.Element]:
				if child is node:
					break
				sibling = child
			if sibling is not None:
				return self.left.matchpath(path[:-1]+[sibling])
		return False

	def __str__(self):
		return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)


class CSSGeneralSiblingCombinator(xfind.BinaryCombinator):
	"""
	<par>A <class>CSSGeneralSiblingCombinator</class> work similar to an
	<class>GeneralSiblingCombinator</class> except that only preceding elements
	are considered.</par>
	"""

	def matchpath(self, path):
		if len(path) >= 2 and self.right.matchpath(path):
			node = path[-1]
			for child in path[-2][xsc.Element]:
				if child is node: # no previous element siblings
					return False
				if self.left.matchpath(path[:-1]+[child]):
					return True
		return False

	def __str__(self):
		return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)


_attributecombinator2class = {
	"=": xfind.attrhasvalue_xml,
	"~=": CSSAttributeListSelector,
	"|=": CSSAttributeLangSelector,
	"^=": xfind.attrstartswith_xml,
	"$=": xfind.attrendswith_xml,
	"*=": xfind.attrcontains_xml,
}

_combinator2class = {
	" ": xfind.DescendantCombinator,
	">": xfind.ChildCombinator,
	"+": CSSAdjacentSiblingCombinator,
	"~": CSSGeneralSiblingCombinator,
}

_pseudoname2class = {
	"first-child": CSSFirstChildSelector,
	"last-child": CSSLastChildSelector,
	"first-of-type": CSSFirstOfTypeSelector,
	"last-of-type": CSSLastOfTypeSelector,
	"only-child": CSSOnlyChildSelector,
	"only-of-type": CSSOnlyOfTypeSelector,
	"empty": CSSEmptySelector,
	"root": CSSRootSelector,
	"hover": CSSHoverSelector,
	"focus": CSSFocusSelector,
	"link": CSSLinkSelector,
	"visited": CSSVisitedSelector,
	"active": CSSActiveSelector,
	"after": CSSAfterSelector,
	"before": CSSBeforeSelector,
}

_function2class = {
	"nth-child": CSSNthChildSelector,
	"nth-last-child": CSSNthLastChildSelector,
	"nth-of-type": CSSNthOfTypeSelector,
	"nth-last-of-type": CSSNthLastOfTypeSelector,
}


def selector(selectors, prefixes=None):
	"""
	Create a walk filter that will yield all nodes that match the specified
	&css; expression. <arg>selectors</arg> can be a string or a
	<class>cssutils.css.selector.Selector</class> object. <arg>prefixes</arg>
	may be a mapping mapping namespace prefixes to namespace names.
	"""

	if isinstance(selectors, basestring):
		if prefixes is not None:
			prefixes = dict((key, xsc.nsname(value)) for (key, value) in prefixes.iteritems())
			selectors = "%s\n%s{}" % ("\n".join("@namespace %s %r;" % (key if key is not None else "", value) for (key, value) in prefixes.iteritems()), selectors)
		else:
			selectors = "%s{}" % selectors
		for rule in cssutils.CSSParser().parseString(selectors).cssRules:
			if isinstance(rule, css.CSSStyleRule):
				selectors = rule.selectorList.seq
				break
		else:
			raise ValueError("can't happen")
	elif isinstance(selectors, css.CSSStyleRule):
		selectors = selectors.selectorList.seq
	elif isinstance(selectors, css.Selector):
		selectors = [selectors]
	else:
		raise TypeError("can't handle %r" % type(selectors))
	orcombinators = []
	for selector in selectors:
		rule = root = CSSTypeSelector()
		prefix = None
		attributename = None
		attributevalue = None
		combinator = None
		inattr = False
		for (t, v) in zip(selector.seq.types, selector.seq.values):
			if t == "namespace_prefix":
				prefix = v.rstrip("|")
				if prefix != "*":
					try:
						xmlns = prefixes[prefix]
					except KeyError:
						raise xsc.IllegalPrefixError(prefix)
					rule.xmlns = xmlns
				prefix = None
			elif t == "IDENT":
				if inattr:
					attributename = v
				else:
					rule.type = v
			elif t == "universal":
				rule.type = "*"
			elif t == "HASH":
				rule.selectors.append(xfind.hasid(v.lstrip("#")))
			elif t == "class":
				rule.selectors.append(xfind.hasclass(v.lstrip(".")))
			elif t is None:
				if v == "[":
					inattr = True
					combinator = None
				elif v == "]":
					if combinator is None:
						rule.selectors.append(CSSHasAttributeSelector(attributename))
					else:
						try:
							rule.selectors.append(_attributecombinator2class[combinator](attributename, attributevalue))
						except KeyError:
							raise ValueError("unknown combinator %s" % attributevalue)
					inattr = False
				elif v in _attributecombinator2class:
					combinator = v
			elif t == "pseudo-class":
				if v.endswith("("):
					try:
						rule.selectors.append(_function2class[v.lstrip(":").rstrip("(")]())
					except KeyError:
						raise ValueError("unknown function %s" % v)
					rule.function = v
				else:
					try:
						rule.selectors.append(_pseudoname2class[v.lstrip(":")]())
					except KeyError:
						raise ValueError("unknown pseudo-class %s" % v)
			elif t == "NUMBER":
				# can only appear in a function => set the function value
				rule.selectors[-1].value = v
			elif t == "STRING":
				if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
					v = v[1:-1]
				# can only appear in a attribute selector => set the attribute value
				attributevalue = v
			elif t == "combinator":
				if inattr:
					combinator = v
				else:
					try:
						rule = CSSTypeSelector()
						root = _combinator2class[v](root, rule)
					except KeyError:
						raise ValueError("unknown combinator %s" % v)
					xmlns = "*"
		orcombinators.append(root)
	return orcombinators[0] if len(orcombinators) == 1 else xfind.OrCombinator(*orcombinators)
