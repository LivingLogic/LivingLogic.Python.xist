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

	``rul4``
		``rul4`` renders an UL4 template. The available template variables
		allow system commands and database access. Supported databases are Oracle,
		SQLite and MySQL.

	``uls``
		``uls`` is an URL-enabled version of the ``ls`` command for listing
		directory content. It uses :mod:`ll.url` and supports ``ssh`` and
		``oracle`` URLs (via :mod:`ll.orasql`).

	``ucp``
		``ucp`` is an URL-enabled version of the ``cp`` command for copying files
		(and file-like objects). It supports ``ssh`` and ``oracle`` URLs for both
		source and target files.

	``ucat``
		``ucat`` is an URL-enabled version of the ``cat`` command for printing
		files (and file-like objects).

	``udiff``
		``udiff`` is an URL-enabled version of the ``diff`` command for showing
		differences between two files or directories.

These scripts can either be called via Pythons :option:`-m` option::

	python -mll.scripts.rul4 --help

or as a simple script installed in the search path::

	rul4 --help
"""


__docformat__ = "reStructuredText"
