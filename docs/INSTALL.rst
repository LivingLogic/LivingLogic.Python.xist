Installation
============

Requirements
------------

To use XIST you need the following software packages:

	*	`Python 3.6`_;

	*	`cssutils`_;

	*	`Pillow`_ (if you want to use automatic image size calculation);

	*	`lxml`_ (if you want to parse "broken" HTML; at least version 3.0);

	*	`cx_Oracle`_ (if you want to use :mod:`ll.orasql`);

	*	`pytest`_ (if you want to run the test suite)

	*	`execnet`_ (if you want to use ssh URLs)

	*	and a C compiler supported by pip, if you want to install the
		source distribution.

	.. _Python 3.6: http://www.python.org/
	.. _cssutils: http://cthedot.de/cssutils/
	.. _Pillow: http://python-pillow.org/
	.. _lxml: http://lxml.de/
	.. _links: http://links.twibright.com/
	.. _cx_Oracle: https://oracle.github.io/python-cx_Oracle/
	.. _pytest: http://pytest.org/latest/
	.. _execnet: http://codespeak.net/execnet/


Installation
------------

pip is used for installation so you can install this package
with the following command:

.. sourcecode:: bash

	$ pip install ll-xist

For some versions a Windows distribution is provided. To install it, double
click it, and follow the instructions.
