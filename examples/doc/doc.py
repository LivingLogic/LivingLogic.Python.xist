#! /usr/bin/env python

"""
A XSC module for generating documentation of Python modules.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

# register all the classes we've defined so far
xsc.registerAllElements(vars(),"doc")

if __name__ == "__main__":
	xsc.make()

