#! /usr/bin/env python

"""
A XSC module for generating documentation of Python modules.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import string
from Signature import Signature

from xist import xsc,html,specials

class module(xsc.Element):
	empty = 0

class function(xsc.Element):
	empty = 0

class name(xsc.Element):
	empty = 0

class signature(xsc.Element):
	empty = 0

class desc(xsc.Element):
	empty = 0

class positional(xsc.Element):
	empty = 0

class keyword(xsc.Element):
	empty = 0

class arg(xsc.Element):
	empty = 0

# register all the classes we've defined so far
xsc.registerAllElements(vars(),"doc")

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
		e = xsc.xsc.parseString(text)
	except:
		e = xsc.Text(text)
	return desc(e)

def explain(thing):
	"""
	returns a XML representation of the documentation of
	<arg>thing</arg>, which can be a function, class or module.
	"""

	if type(thing) == types.FunctionType:
		e = function()
		e.append(name(thing.__name__))
		xmlsig = signature()
		sig = Signature(thing)
		defaults = sig.defaults()
		specials = sig.special_args()
		for a in sig.ordinary_args():
			if defaults.has_key(a):
				xmlsig.append(a + '=' + str(defaults[a]))
			else:
				xmlsig.append(arg(a))
		if specials.has_key('positional'):
			xmlsig.append(positional(specials['positional']))
		if specials.has_key('keyword'):
			xmlsig.append(keyword(specials['keyword']))
		e.append(xmlsig)
		if thing.__doc__ is not None:
			e.append(getDoc(thing.__doc__))
		return e
	elif type(thing) == types.ModuleType:
		return explain(thing.__dict__)
	elif type(thing) == types.DictType:
		e = module()
		try:
			e.append(name(thing["__name__"]))
			if thing["__doc__"] is not None:
				e.append(getDoc(thing["__doc__"]))
		except:
			pass
		for varname in thing.keys():
			if type(thing[varname]) is not types.ModuleType:
				e.append(explain(thing[varname]))
		return e

	return xsc.Null

if __name__ == "__main__":
	e = explain(vars())
	print "Tree:"
	print e.reprtree()
	print "Flat:"
	print e.repr()

