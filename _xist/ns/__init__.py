#! /usr/bin/env python

"""
This package contains all the modules that provide 
<dbl:pyref module="xist.xsc" class="Namespace">namespace objects</dbl:pyref>
to &xist;. For example the definition of &html; can 
be found in the module <dbl:pyref module="xist.ns.html">xist.ns.html</dbl:pyref>.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = ["html", "wml", "abbr", "cond", "docbook", "docbooklite", "form", "jsp", "meta", "ruby", "specials"]


