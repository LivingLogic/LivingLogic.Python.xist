# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2004-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2004-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license

"""
This package contains the following scripts:

	``oracreate``
		``oracreate`` prints (or executes in another schema) the SQL of all objects
		in an Oracle database schema (i.e. all tables, procedures, functions,
		views, etc.)

	``oradrop``
		``oradrop`` prints (or executes) drop statements for all objects in an
		Oracle database schema.

	``oradelete``
		``oradelete`` prints (or executes) SQL for deleting all records from all
		tables in an Oracle database schema.

	``oragrant``
		``oragrant`` prints (or executes) grants statements from an Oracle
		database schema.

	``orafind``
		``orafind`` can be used to search for a string in all fields of all
		tables in an Oracle database schema.

	``oradiff``
		``oradiff`` can be used for finding the differences between two Oracle
		database schemas.

	``oramerge``
		``oramerge`` can be used for merging the changes between two Oracle
		database schemas into a third one.

These scripts can either be called via Pythons :option:`-m` option::

	python -mll.orasql.scripts.oracreate --help

or as a simple script installed in the search path::

	oracreate --help
"""


__docformat__ = "reStructuredText"

