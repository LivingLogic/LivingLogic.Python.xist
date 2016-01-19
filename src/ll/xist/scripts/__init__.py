# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license

"""
This package contains the following scripts:

	``dtd2xsc``
		``dtd2xsc`` creates a skeleton XIST namespace module from a DTD.

	``xml2xsc``
		``xml2xsc`` is a script that generates a skeleton XIST namespace module
		from one or more XML files.

	``tld2xsc``
		``tld2xsc`` converts a Java tag library description XML file to a skeleton
		XIST namespace.

	``doc2txt``
		``doc2txt`` creates a plain text file from a XML file using XISTs doc
		XML vocabulary.

	``uhpp``
		``uhpp`` is a script for pretty printing HTML files. It is URL-enabled,
		so you can specify local file names and URLs (and remote files via
		``ssh`` URLs).

These scripts can either be called via Pythons :option:`-m` option::

	python -mll.xist.scripts.xml2xsc --help

or as a simple script installed in the search path::

	xml2xsc --help
"""


__docformat__ = "reStructuredText"
