#! /usr/bin/env python

"""
A XSC module for generating documentation of Python modules.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import string
from Signature import Signature

from xist import xsc, parsers
from xist.ns import html, specials, docbooklite, abbr
import elements

def __isOnlyWhiteSpace(text):
	for c in text:
		if c not in string.whitespace:
			return 0
	else:
		return 1
	
def getDoc(text):
	lines = string.split(text,"\n")

	# find first nonempty line
	for i in xrange(len(lines)):
		if not __isOnlyWhiteSpace(lines[i]):
			if i:
				del lines[:i]
			break
	else:
		first = 0

	if len(lines):
		# find starting white space of this line
		startwhite = ""
		for c in lines[0]:
			if c in string.whitespace:
				startwhite = startwhite + c
			else:
				break

		# remove this whitespace from every line
		for i in xrange(len(lines)):
			if lines[i][:len(startwhite)] == startwhite:
				lines[i] = lines[i][len(startwhite):]

		# remove empty lines
		while len(lines) and lines[0] == "":
			del lines[0]
		while len(lines) and lines[-1] == "":
			del lines[-1]

	text = string.join(lines,"\n")

	try:
		e = parsers.parseString(text)
	except:
		e = html.pre(text)
	return elements.desc(e)

def explain(thing):
	"""
	returns a &xml; representation of the documentation of
	<pyref function="explain" arg="thing">thing</pyref>, which can be a function, method, class or module.
	"""

	t = type(thing)
	if t in (types.FunctionType,types.MethodType):
		if t is types.FunctionType:
			e = elements.function(name=thing.__name__)
		else:
			e = elements.method(name=thing.__name__)
		xmlsig = elements.signature()
		sig = Signature(thing)
		defaults = sig.defaults()
		specials = sig.special_args()
		for a in sig.ordinary_args():
			_a = elements.arg(name=a)
			if defaults.has_key(a):
				_a["default"] = repr(defaults[a])
			xmlsig.append(_a)
		if specials.has_key('positional'):
			xmlsig.append(elements.arg(name=specials['positional'], type="positional"))
		if specials.has_key('keyword'):
			xmlsig.append(elements.arg(name=specials['keyword'], type="keyword"))
		e.append(xmlsig)
		if thing.__doc__ is not None:
			e.append(getDoc(thing.__doc__))
		return e
	elif t is types.ClassType:
		e = elements.Class(name=thing.__name__)
		if thing.__doc__ is not None:
			e.append(getDoc(thing.__doc__))
		methods = []
		for varname in thing.__dict__.keys():
			test = getattr(thing,varname)
			if type(test) is types.MethodType:
				methods.append(test)
		if len(methods):
			e.append(elements.methods())
			for m in methods:
				e[-1].append(explain(m))
		return e
	elif t is types.ModuleType:
		e = elements.module(name=thing.__name__)
		if thing.__doc__ is not None:
			e.append(getDoc(thing.__doc__))

		functions = []
		classes   = []
		for varname in thing.__dict__.keys():
			obj = thing.__dict__[varname]
			t = type(obj)
			if t is types.FunctionType:
				functions.append(obj)
			elif t is types.ClassType:
				classes.append(obj)
		if len(functions):
			e.append(elements.functions())
			for f in functions:
				e[-1].append(explain(f))
		if len(classes):
			e.append(elements.classes())
			for c in classes:
				e[-1].append(explain(c))
		return e

	return xsc.Null

if __name__ == "__main__":
	e = explain(elements)
	print e.conv().asBytes()

