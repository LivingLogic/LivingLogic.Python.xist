Requirements
============

To use XIST you need the following software packages:

	*	`Python 3.3`_;

	*	`cssutils`_;

	*	`Python Imaging Library`_ (if you want to use automatic image size
		calculation); (As long as the PIL isn't ported to Python 3, you can use
		This`PIL port to Python 3`_)

	*	`lxml`_ (if you want to parse "broken" HTML; at least version 3.0);

	*	`cx_Oracle`_ (if you want to use :mod:`ll.orasql`);

	*	`distribute`_ (if you want to install this package as an egg);

	*	`pytest`_ (if you want to run the test suite)

	*	`execnet`_ (if you want to use ssh URLs)

	*	and a C compiler supported by distutils, if you want to install the
		source distribution.

	.. _Python 3.3: http://www.python.org/
	.. _cssutils: http://cthedot.de/cssutils/
	.. _Python Imaging Library: http://www.pythonware.com/products/pil/
	.. _PIL port to Python 3: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil
	.. _lxml: http://lxml.de/
	.. _links: http://links.twibright.com/
	.. _cx_Oracle: http://cx-oracle.sourceforge.net/
	.. _distribute: http://pypi.python.org/pypi/distribute
	.. _pytest: http://pytest.org/latest/
	.. _execnet: http://codespeak.net/execnet/


Installation
============

setuptools/distribute is used for installation so you can install this package
with the following command::

	$ easy_install ll-xist

or::

	$ pip install ll-xist

If you want to install from source, you can download one of the
`distribution archives`__, unpack it, enter the directory and execute the
following command::

	$ python setup.py install

__ http://www.livinglogic.de/Python/Download.html#xist

This will copy ``*.py`` files, compile ``*.c`` files and install everything in
the ``site-packages`` directory as the :mod:`ll.xist` package.

For some versions a Windows distribution is provided. To install it, double
click it, and follow the instructions.
