Overview
--------

XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
"object oriented XSLT".

XIST also includes the following modules and packages:

*	:mod:`ll.ul4c` is compiler for a cross-platform templating language with
	similar capabilities to `Django's templating language`__. UL4 templates
	are compiled to an internal format, which makes it possible to implement
	template renderers in other languages and makes the template code "secure"
	(i.e. template code can't open or delete files).

	__ https://docs.djangoproject.com/en/2.0/ref/templates/language/

	There are implementations for Python, Java and Javascript.

*	:mod:`ll.ul4on` provides functions for encoding and decoding a lightweight
	machine-readable text-based format for serializing the object types supported
	by UL4. It is extensible to allow encoding/decoding arbitrary instances
	(i.e. it is basically a reimplementation of :mod:`pickle`, but with string
	input/output instead of bytes and with an eye towards cross-plattform
	support).

	There are implementations for Python, Java and Javascript.

*	:mod:`ll.orasql` provides utilities for working with cx_Oracle_:

	-	It allows calling functions and procedures with keyword arguments.

	-	Query results will be put into :class:`~ll.orasql.Record` objects,
		where database fields are accessible as object attributes.

	-	The :class:`~ll.orasql.Connection` class provides methods for iterating
		through the database metadata.

	-	Importing the modules adds support for URLs with the scheme ``oracle`` to
		:mod:`ll.url`.

	.. _cx_Oracle: https://oracle.github.io/python-cx_Oracle/

*	:mod:`ll.make` is an object oriented make replacement. Like make it allows
	you to specify dependencies between files and actions to be executed
	when files don't exist or are out of date with respect to one
	of their sources. But unlike make you can do this in a object oriented
	way and targets are not only limited to files.

*	:mod:`ll.color` provides classes and functions for handling RGB color values.
	This includes the ability to convert between different color models
	(RGB, HSV, HLS) as well as to and from CSS format, and several functions
	for modifying and mixing colors.

*	:mod:`ll.sisyphus` provides classes for running Python scripts as cron jobs.

*	:mod:`ll.url` provides classes for parsing and constructing RFC 2396
	compliant URLs.

*	:mod:`ll.nightshade` can be used to serve the output of PL/SQL
	functions/procedures with CherryPy__.

*	:mod:`ll.misc` provides several small utility functions and classes.

*	:mod:`ll.astyle` can be used for colored terminal output (via ANSI escape
	sequences).

*	:mod:`ll.daemon` can be used on UNIX to fork a daemon process.

*	:mod:`ll.xml_codec` contains a complete codec for encoding and decoding XML.

__ http://www.cherrypy.org/


Documentation
-------------

For documentation read the files in the :file:`docs/` directory or the
`web pages`__ generated from those.

__ http://python.livinglogic.de/

For installation instructions read :file:`docs/INSTALL.rst`.

For a history of XIST and a list of new features in this version,
read :file:`docs/NEWS.rst`.

For a list of old features and bugfixes read :file:`docs/OLDNEWS.rst`.

For the license read :file:`xist/__init__.py`.


Download
--------

XIST is available for download from the `download directory`_ or from the
Cheeseshop_.

.. _download directory: http://python-downloads.livinglogic.de/download/
.. _Cheeseshop: https://pypi.org/project/ll-xist/


Source
------

Sourcecode is available on GitHub_.

.. _GitHub: https://github.com/LivingLogic/LivingLogic.Python.xist


Author
------

Walter Dörwald <walter@livinglogic.de>
