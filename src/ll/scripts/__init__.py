# -*- coding: utf-8 -*-

## Copyright 1999-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license

"""
This package contains the following scripts:

	``db2ul4``
		``db2ul4`` renders an UL4 template. The available template variables
		allow system commands and database access. Supported databases are Oracle,
		sqllite and MySQL.

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

These scripts can either be called via Pythons :option:`-m` option::

	python -mll.scripts.db2ul4 --help

or as a simple script installed in the search path::

	db2ul4 --help
"""


__docformat__ = "reStructuredText"
