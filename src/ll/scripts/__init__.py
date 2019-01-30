# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license

"""
This package contains the following scripts:

:program:`rul4`
	:program:`rul4` renders an UL4 template. The available template variables
	allow system commands and database access. Supported databases are Oracle,
	SQLite, MySQL and Redis.

:program:`uls`
	:program:`uls` is an URL-enabled version of the :command:`ls` command for
	listing directory content. It uses :mod:`ll.url` and supports ``ssh`` and
	``oracle`` URLs (via :mod:`ll.orasql`).

:program:`ucp`
	:program:`ucp` is an URL-enabled version of the :command:`cp` command for
	copying files (and file-like objects). It supports ``ssh`` and ``oracle``
	URLs for both source and target files.

:program:`ucat`
	:program:`ucat` is an URL-enabled version of the :command:`cat` command for
	printing files (and file-like objects).

:program:`udiff`
	:program:`udiff` is an URL-enabled version of the :command:`diff` command
	for showing differences between two files or directories.

These scripts can either be called via Pythons :option:`-m` option:

.. sourcecode:: bash

	python -mll.scripts.rul4 --help

or as a simple script installed in the search path:

.. sourcecode:: bash

	rul4 --help
"""


__docformat__ = "reStructuredText"
