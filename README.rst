Purpose
-------

XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
"object oriented XSLT".

XIST also includes the following modules and packages:

*	``ll.ul4c`` is compiler for a cross-platform templating language with
	similar capabilities to `Django's templating language`__. UL4 templates
	are compiled to an internal format, which makes it possible to implement
	template renderers in other languages and makes the template code "secure"
	(i.e. template code can't open or delete files).

	__ http://www.djangoproject.com/documentation/templates/

	There are implementations for Python, Java, Javascript and PHP.

*	``ll.ul4on`` provides functions for encoding and decoding a lightweight
	machine-readable text-based format for serializing the object types supported
	by UL4. It is extensible to allow encoding/decoding arbitrary instances
	(i.e. it is basically a reimplementation of ``pickle``, but with string
	input/output instead of bytes and with an eye towards cross-plattform
	support).

	There are implementations for Python, Java, Javascript and PHP.

*	``ll.orasql`` provides utilities for working with cx_Oracle_:

	-	It allows calling functions and procedures with keyword arguments.

	-	Query results will be put into Record objects, where database fields
		are accessible as object attributes.

	-	The ``Connection`` class provides methods for iterating through the
		database metadata.

	-	Importing the modules adds support for URLs with the scheme ``oracle`` to
		``ll.url``.

	.. _cx_Oracle: http://cx-oracle.sourceforge.net/

*	``ll.make`` is an object oriented make replacement. Like make it allows
	you to specify dependencies between files and actions to be executed
	when files don't exist or are out of date with respect to one
	of their sources. But unlike make you can do this in a object oriented
	way and targets are not only limited to files.

*	``ll.color`` provides classes and functions for handling RGB color values.
	This includes the ability to convert between different color models
	(RGB, HSV, HLS) as well as to and from CSS format, and several functions
	for modifying and mixing colors.

*	``ll.sisyphus`` provides classes for running Python scripts as cron jobs.

*	``ll.url`` provides classes for parsing and constructing RFC 2396
	compliant URLs.

*	``ll.nightshade`` can be used to serve the output of PL/SQL
	functions/procedures with CherryPy__.

*	``ll.misc`` provides several small utility functions and classes.

*	``ll.astyle`` can be used for colored terminal output (via ANSI escape
	sequences).

*	``ll.daemon`` can be used on UNIX to fork a daemon process.

*	``ll.xml_codec`` contains a complete codec for encoding and decoding XML.

__ http://www.cherrypy.org/


Documentation
-------------

For documentation read the files in the ``docs/`` directory or the
`web pages`__.

__ http://www.livinglogic.de/Python/xist/

For installation instructions read ``INSTALL.rst`` or the
`installation web page`__.

__ http://www.livinglogic.de/Python/xist/Installation.html

For a history of XIST and a list of new features in this version,
read ``NEWS.rst`` or the `history web page`__.

__ http://www.livinglogic.de/Python/xist/History.html

For a list of old features and bugfixes read ``OLDNEWS`` or the
`old history web page`__.

__ http://www.livinglogic.de/Python/xist/OldHistory.html

For the license read ``xist/__init__.py``.


Download
--------

XIST is available via FTP_, HTTP_ or from the Cheeseshop_.

.. _FTP: ftp://ftp.livinglogic.de/pub/livinglogic/xist/
.. _HTTP: http://ftp.livinglogic.de/xist/
.. _Cheeseshop: http://cheeseshop.python.org/pypi/ll-xist


Source
------

Sourcecode is available on GitHub_.

.. _GitHub: https://github.com/LivingLogic/LivingLogic.Python.xist


Mailing lists
-------------

A discussion mailing list is available. For more info go to
https://mail.livinglogic.de/mailman/listinfo/xist-discuss. You can subscribe
from these webpages as well as read the mailing list archives.

An announcement mailing list is available too. For info go to
https://mail.livinglogic.de/mailman/listinfo/xist-announce


Author
------

* Walter Dörwald <walter@livinglogic.de>
