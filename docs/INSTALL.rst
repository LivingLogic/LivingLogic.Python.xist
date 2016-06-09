Installation
============

To use XIST you need the following software packages:

	*	`Python 3.5`_;

	*	`cssutils`_;

	*	`Pillow`_ (if you want to use automatic image size
		calculation);

	*	`lxml`_ (if you want to parse "broken" HTML; at least version 3.0);

	*	`cx_Oracle`_ (if you want to use :mod:`ll.orasql`);

	*	`pytest`_ (if you want to run the test suite)

	*	`execnet`_ (if you want to use ssh URLs)

	*	and a C compiler supported by pip, if you want to install the
		source distribution.

	.. _Python 3.5: http://www.python.org/
	.. _cssutils: http://cthedot.de/cssutils/
	.. _Pillow: http://python-pillow.org/
	.. _lxml: http://lxml.de/
	.. _links: http://links.twibright.com/
	.. _cx_Oracle: http://cx-oracle.sourceforge.net/
	.. _pytest: http://pytest.org/latest/
	.. _execnet: http://codespeak.net/execnet/

pip is used for installation so you can install this package
with the following command:

.. sourcecode:: bash

	$ pip install ll-xist

If you want to install from source, you can download one of the
`distribution archives`__, unpack it, enter the directory and execute the
following command:

.. sourcecode:: bash

	$ python setup.py install

__ http://www.livinglogic.de/Python/Download.html#xist

This will copy :file:`*.py` files, compile :file:`*.c` files and install everything in
the :file:`site-packages` directory as the :mod:`ll.xist` package.

For some versions a Windows distribution is provided. To install it, double
click it, and follow the instructions.
