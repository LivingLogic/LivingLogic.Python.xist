Literals
########

The following object types can be created and used insided templates:

*	strings
*	integers
*	floats
*	date objects
*	color objects
*	The "null" value (``None``)
*	boolean values (``True`` and ``False``)
*	lists
*	dictionaries
*	sets

Note that depending on the implementation language of the renderer additional
types might be supported, e.g. a Python renderer will probably support both
tuples and lists and anything supporting :meth:`__getitem__` (or :meth:`__iter__`
when the list is used in a loop) for lists, Java might support anything
implementing the ``List`` interface (or the ``Collection`` interface if the list
is used in a loop).

Objects of these types can either be passed to the template in the call to the
render function, or the template can create objects of thoses types itself. The
syntax for creating such a constant is very similar to Python's syntax.


The "null" object
=================

The "null" object can be referred to via ``None``.


Boolean literals
================

The boolean constants can be referred to via ``True`` and ``False``.


Integer literals
================

Integer constants can be written in decimal, hexadecimal, octal and binary:
``42``, ``0x2a``, ``0o52`` and ``0b101010`` all refer to the integer value 42.


Float literals
==============

Float constants must contain a decimal point or an exponential specifier,
e.g. ``42.``, ``4e23``.


String literals
===============

Strings are delimited with single or double quotes and support all escape
sequences that Python supports (except ``\N{}``). Strings constants allow
``\uXXXX`` escaping. Examples:

* ``"abc"`` and ``'abc'``;

*	``"'"`` and ``'\''`` are single quotes;

*	``'"'`` and ``"\""`` are double quotes;

*	``"\n"`` is a line feed and ``"\t"`` is a tab;

*	``"\x61"`` and ``"\u0061"`` are lowercase "a"s;

Strings can also be delimited with triple single or double quotes like in Python.
These strings support embedded line feeds.


Date literals
=============

Date objects have a year, month and day component and can be created like this:

*	``@(2008-12-24)``


Datetime literals
=================

Datetime objects have a date and time including microseconds and can be
created like this:

*	``@(2008-12-24T12:34)``

*	``@(2008-12-24T12:34:56)``

*	``@(2008-12-24T12:34:56.987654)``


Color literals
==============

Color values are 8 bit red, green, blue and alpha values. Color constants can
be created like this:

*	``#fff``

*	``#fff8``

*	``#0063a8``

*	``#0063a880``

The variants with 3 or 6 hex digits will create a color object with an alpha
value of 255.


Lists
=====

Lists can be created like this:

*	``[]``

*	``[1, 2, 3]``

*	``[None, 42, "foo", [False, True]]``

``*`` expressions can be used to expand other lists inplace, so ::

	[1, *[2, 3], 4, *[5, 6]]

is equivalent to ::

	[1, 2, 3, 4, 5, 6]

It is also possible to create a list with a list comprehension::

	["(" + c.upper() + ")" for c in "hurz" if c < "u"]

This will create the list ::

	["(H)", "(R)"]

The ``if`` condition is optional, i.e. ::

	["(" + c.upper() + ")" for c in "hurz"]

will create the list ::

	["(H)", "(U)", "(R)", "(Z)"]


Dictionaries
============

Dictionaries can be created like this:

*	``{}``

*	``{1: 2, 3: 4}``

*	``{"foo": 17, "bar": 23}``

``**`` expressions can be used to expand other dictionaries inplace, so::

	{"foo": 17, **{"bar": 23, "baz": 42}}

is equivalent to ::

	{"foo": 17, "bar": 23, "baz": 42}

The ``**`` expression must be a dictionary or a list of key/value pairs.

It is also possible to create a dictionary with a dictionary comprehension::

	{ c.upper() : "(" + c + ")" for c in "hurz" if c < "u"}

This will create the dictionary ::

	{ "H": "(h)", "R": "(r)"}

The ``if`` condition is optional, i.e. ::

	{ c.upper() : "(" + c + ")" for c in "hurz"}

will create the dictionary ::

	{ "H": "(h)", "U": "(u)", "R": "(r)", "Z": "(z)"}


Sets
====

Sets can be created like this:

*	``{/}`` (this is the empty set)

*	``{1, 2, 3}``

*	``{"foo", "bar"}``

The empty set can also be created with the function ``set``::

	set()

``*`` expressions are also supported::

	{1, *[2, 3], 4, *[5, 6]}

It is also possible to create a set with a set comprehension::

	{c.upper() for c in "hurz" if c < "u"}

This will create the set ::

	{"H", "R"}

The ``if`` condition is optional, i.e. ::

	{c.upper() for c in "hurz"}

will create the dictionary ::

	{"H", "R", "U", "Z"}


The ``Undefined`` object
========================

The object ``Undefined`` will be returned when a nonexistent variable, a
nonexistent dictionary entry or an index that is out of range for a list/string
is accessed.
