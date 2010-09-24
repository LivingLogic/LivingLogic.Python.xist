Requirements
============

To use XIST you need the following software packages:

	*	`Python 2.6`_;

	*	`cssutils`_;

	*	`Python Imaging Library`_ (if you want to use automatic image size
		calculation);

	*	`libxml2`_ and its Python wrapper (if you want to parse "broken" HTML);

	*	`elinks`_ (if you want want to use the function
		:func:`ll.xist.ns.html.astext`);

	*	`cx_Oracle`_ (if you want to use :mod:`ll.orasql`);

	*	`setuptools`_ (if you want to install this package as an egg);

	*	`py.test`_ (if you want to run the test suite; at least version 1.3.2)

	*	`execnet`_ (if you want to use ssh URLs)

	*	and a C compiler supported by distutils, if you want to install the
		source distribution.

	.. _Python 2.6: http://www.python.org/
	.. _cssutils: http://cthedot.de/cssutils/
	.. _Python Imaging Library: http://www.pythonware.com/products/pil/
	.. _libxml2: http://www.xmlsoft.org/
	.. _elinks: http://elinks.or.cz/
	.. _cx_Oracle: http://cx-oracle.sourceforge.net/
	.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
	.. _py.test: http://codespeak.net/py/current/doc/test.html
	.. _execnet: http://codespeak.net/execnet/


Installation
============

setuptools is used for installation so you can install this package with the
following command::

	$ easy_install ll-xist

If you want to install from source, you can download one of the
`distribution archives`__, unpack it, enter the directory and execute the
following command::

	$ python setup.py install

__ http://www.livinglogic.de/Python/Download.html#xist

This will copy ``*.py`` files, compile ``*.c`` files and install everything in
the ``site-packages`` directory as the :mod:`ll` and :mod:`ll.xist` packages.

For Windows a binary distribution is provided. To install it,
double click it, and follow the instructions.


Character encoding
==================

When you pass an 8bit string in the constructor of an XIST element, these
strings have to be converted to Unicode. XIST assumes that these 8bit strings
are in the system default encoding, which normally is ASCII.

If your strings contain non-ASCII characters you *must* pass them as unicode
strings to the XIST constructors and you *must* specify the encoding you're
using in your source code in the first or second line of your script (see
:pep:`263` for a detailed description).


IPython display hooks
=====================

If you're using XIST in an `IPython`_ shell, XIST allows you to browse through
your trees using any of the browsers provided by IPython's `ipipe module`_.

	.. _IPython: http://ipython.scipy.org/
	.. _ipipe module: http://ipython.scipy.org/moin/UsingIPipe

You can specify which format gets used by changing the value of the
``defaultpresenter`` variable in the module :mod:`ll.xist.present`::

	from ll.xist import present
	present.defaultpresenter = present.TreePresenter

Setting this value to ``None`` turns the display hook off.
