Purpose
-------

XIST is an extensible HTML and XML generator. XIST is also a XML parser with a
very simple and pythonesque tree API. Every XML element type corresponds to a
Python class and these Python classes provide a conversion method to transform
the XML tree (e.g. into HTML). XIST can be considered 'object oriented XSLT'.

XIST also includes the following modules:

*	``astyle`` can be used for colored terminal output (via ANSI escape
	sequences).

*	``color`` provides classes and functions for handling RGB color values.
	This includes the ability to convert between different color models
	(RGB, HSV, HLS) as well as to and from CSS format, and several functions
	for modifying and mixing colors.

*	``make`` is an object oriented make replacement. Like make it allows you
	to specify dependencies between files and actions to be executed
	when files don't exist or are out of date with respect to one
	of their sources. But unlike make you can do this in a object oriented
	way and targets are not only limited to files, but you can implement
	e.g. dependencies on database records.

*	``misc`` provides several small utility functions and classes.

*	``sisyphus`` provides classes for running Python scripts as cron jobs.

*	``daemon`` can be used on UNIX to fork a daemon process.

*	``url`` provides classes for parsing and constructing RFC 2396
	compliant URLs.

*	``xpit`` is a module that makes it possible to embed Python expressions
	in text (as XML style processing instructions).

*	``xml_codec`` contains a complete codec for encoding and decoding XML.


Documentation
-------------

For documentation read the files in the ``docs/`` directory or the
`web pages`__.

__ http://www.livinglogic.de/Python/xist/

For installation instruction read ``INSTALL.rst`` or the
`installation web page`__.

__ http://www.livinglogic.de/Python/xist/Installation.html

For a history of XIST and a list of new features in this version,
read ``NEWS.rst`` or the `history web page`__.

__ http://www.livinglogic.de/Python/xist/History.html

For a list of old features and bugfixes read ``OLDNEWS`` or the
`old history web page`__.

__ http://www.livinglogic.de/Python/xist/OldHistory.html

For the license read ``__init__.py``.


Download
--------

XIST is available via ftp_, http_, from the cheeseshop_ or as a
`debian package`_.

.. _ftp: ftp://ftp.livinglogic.de/pub/livinglogic/xist/
.. _http: http://ftp.livinglogic.de/xist/
.. _cheeseshop: http://cheeseshop.python.org/pypi/ll-xist
.. _debian package: http://packages.debian.org/python-ll-xist


Mailing lists
-------------

A discussion mailing list is available. To subscribe send an email
to xist-discuss-request@livinglogic.de with "subscribe" in the body.
For more information, send an email to xist-discuss-request@livinglogic.de
with "help" in the body. Post to the list by sending an email to
xist-discuss@livinglogic.de.

A announcement mailing list is also available. To subscribe send an email
to xist-announce-request@livinglogic.de with "subscribe" in the body.
For more information, send an email to xist-announce-request@livinglogic.de
with "help" in the body.

Archives of both mailing lists is available at
http://mlarchive.livinglogic.de/


-- Walter Dörwald <walter@livinglogic.de>
