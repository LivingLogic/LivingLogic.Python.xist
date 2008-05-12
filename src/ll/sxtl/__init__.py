# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.sxtl` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.sxtl` compiles a template to a bytecode format, which makes it possible
to implement renderers for these templates in multiple programming languages.


Data objects
============

To render a template the renderer gets passed a data object. What :mod:`ll.sxtl`
supports in this data object is very similar to what JSON_ supports.

	.. _JSON: http://www.json.org/

Supported types are:

	*	strings
	*	integers
	*	floats
	*	The "null" value (``None``)
	*	boolean values (``True`` and ``False``)
	*	lists
	*	dictionaries

Note that depending on the implementation language of the renderer additional
types might be supported, e.g. a Python renderer will probably support tuples
and lists and anything supporting :meth:`__getitem__` (or :meth:`__iter__ when
the list is used in a loop) for lists, Java might support anything implementing
the ``List`` interface (or the ``Collection`` interface if the list is used in a
loop).

The data object itself will be available inside the template code under the name
``data``.

The template code tries to mimic Python syntax as far as possible, but is
limited to what is required for template and does not allow executing arbitrary
Python statements.


Embedding
=========

In the template any text surrounded by ``<?`` and ``?>`` is a "template tag".
The first word inside the template is the tag type. It defines what the tag
does. For example ``<?print foo?>`` is a print tag (it prints the value of the
variable ``foo``). A complete example template looks like this::

	<?if data?>
	<ul>
	<?for lang in data?>
	<li><?print xmlescape(lang)?></li>
	<?end for?>
	</ul>
	<?end if?>

(For text formats where the delimiters ``<?`` and ``?>`` collide with elements
that are used often or where using these delimiters is inconvenient it's
possible to specify a different delimiter pair when compiling the template.)

A complete Python program that renders the template might look like this::

	from ll.sxtl import renderers

	tmpl = '''<?if data?>
	<ul>
	<?for lang in data?>
	<li><?print xmlescape(lang)?></li>
	<?end for?>
	</ul>
	<?end if?>'''

	f = renderers.PythonCode(tmpl).function()

	data = [u"Python", u"Java", u"PHP"]

	print u"".join(f(data))

The method :meth:`PythonCode.function` returns a Python generator that renders
the template with the data object passed in.


Template code
=============

:mod:`ll.sxtl` supports the following tag types:


``print``
---------

The ``print`` tag outputs the value of a variable or any other expression. If
the expression doesn't evaluate to a string it will be converted to a string
first. The format of the string depends on the renderer, but should follow
Python's ``unicode()`` output as much as possible (except that for ``None`` no
output may be produced)::

	<h1><?print person.lastname?>, <?print person.firstname?></h1>


``for``
-------

The ``for`` tag can be used to loop over the items in a list, the characters in
a string or the keys in a dictionary. The end of the loop body must be marked
with an ``<?end for?>`` tag::

	<ul>
	<?for person in data.persons?>
	<li><?print person.lastname?>, <?person.firstname?></li>
	<?end for?>
	</ul>

In ``for`` loops tuple unpacking is supported for tuples of length 1 and 2, so
you can do the following::

	<?for (key, value) in data.items?>

if ``items`` is an iterable containing lists with two elements.


``if``
------

The ``if`` tag can be used to output a part of the template only when a
condition is true. The end of the ``if`` block must be marked with an
``<?end if?>`` tag. The truth value of an object is the same as in Python:

	*	``None`` is false.
	*	The integer ``0`` and the float value ``0.0`` are false.
	*	Empty strings, lists and dictionaries are false.
	*	``False`` is false.
	*	Anything else is true.

For example we can output the person list only if there are any persons::

	<?if data.persons?>
	<ul>
	<?for person in data.persons?>
	<li><?print person.lastname?>, <?person.firstname?></li>
	<?end for?>
	</ul>
	<?end if?>

``elif`` and ``else`` are supported too::

	<?if data.persons?>
	<ul>
	<?for person in data.persons?>
	<li><?print person.lastname?>, <?person.firstname?></li>
	<?end for?>
	</ul>
	<?else?>
	<p>No persons found!</p>
	<?end if?>

or::

	<?if len(data.persons)==0?>
	No persons found!
	<?elif len(data.persons)==1?>
	One person found!
	<?else?>
	<?print len(data.persons)?> persons found!
	<?end if?>


``code``
--------

The ``code`` tag can be used to define or modify variables. Apart from the
assigment operator ``=``, the following augmented assignment operators are
supported:

	*	``+=`` (adds a value to the variable)
	*	``-=`` (subtracts a value from the variable)
	*	``*=`` (multiplies the variable by a value)
	*	``/=`` (divides the variable by a value)
	*	``//=`` (divides the variable by a value, rounding down to the next
		smallest integer)
	*	``&=`` (Does a modulo operation and replaces the variable value with the
		result)

For example the following template will output ``40``::

	<?code x = 17?>
	<?code x += 23?>
	<?print x?>


Expressions
-----------

:mod:`ll.sxtl` supports many of the operators supported by Python. Getitem style
element access is available, i.e. in the expression ``a[b]`` the following type
combinations are supported:

	*	string, integer: Returns the ``b``th character from the string ``a``. Note
		that negative ``b`` values are supported and are relative to the end, so
		``a[-1]`` is the last character.

	*	list, integer: Returns the ``b``th list entry of the list ``a``. Negative
		``b`` values are supported too.

	*	dict, string: Return the value from the dictionary ``a`` corresponding to
		the key ``b``. (Note that some implemenations might support keys other
		than strings too.)

Slices are also supported (for list and string objects). As in Python one or
both of the indexes may be missing to start at the first or end at the last
character/item. Negative indexes are relative to the end. Indexes that are out
of bounds are simply clipped::

	*	``<?print "Hello, World!"[7:-1]?>`` prints ``World``.

	*	``<?print "Hello, World!"[:-1]?>`` prints ``Hello, World``.

The following binary operators are supported: ``+``, ``-``, ``*``, ``/``,
``//`` (truncating division) and ``&`` (modulo).

The usual boolean operators ``not``, ``and`` and ``or`` are supported. However
``and`` and ``or`` don't short-circuit and always return ``True`` or ``False``
(instead of one of the operators).

The two comparison operators ``==`` and ``!=`` are supported.

Containment test via the ``in`` operator can be done, in the expression
``a in b`` the following type combinations are supported:

	*	string, string: Checks whether ``a`` is a substring of ``b``.
	*	any object, list: Checks whether the object ``a`` is in the list ``b``
		(comparison is done by value not by identity)
	*	string, dict: Checks whether the key ``a`` is in the dictionary ``b``.
		(Note that some implementations might support keys other than strings too.)

The inverted containment test (via ``not in``) is available too.


Functions
---------

:mod:`ll.sxtl` supports a number of functions.

``isnone``
::::::::::

``isnone(foo)`` returns ``True`` if ``foo`` is ``None``, else ``False`` is
returned.

``isbool``
::::::::::

``isbool(foo)`` returns ``True`` if ``foo`` is ``True`` or ``False``, else
``False`` is returned.

``isint``
:::::::::

``isint(foo)`` returns ``True`` if ``foo`` is an integer object, else ``False``
is returned.

``isfloat``
::::::::::::

``isfloat(foo)`` returns ``True`` if ``foo`` is a float object, else ``False``
is returned.

``isstr``
::::::::::::

``isstr(foo)`` returns ``True`` if ``foo`` is a string object, else ``False``
is returned.

``islist``
::::::::::::

``islist(foo)`` returns ``True`` if ``foo`` is a list object, else ``False``
is returned.

``isdict``
::::::::::::

``isdict(foo)`` returns ``True`` if ``foo`` is a dictionary object, else
``False`` is returned.

``int``
:::::::

``int(foo)`` converts ``foo`` to an integer. ``foo`` can be a string, a float
a boolean or an integer.

``str``
:::::::

``str(foo)`` converts ``foo`` to a string. If ``foo`` is ``None`` the result
will be the empty string. For lists and dictionaries the exact format is
undefined, but should follow Python's repr format.

``repr``
:::::::

``repr(foo)`` converts ``foo`` to a string representation that is useful for
debugging proposes. The output is the same as for Python's :func:`repr` function.

``len``
:::::::

``len(foo)`` returns the length of a string, or the number of items in a list
or dictionary.

``enumerate``
:::::::::::::

Enumerates the items of the argument (which must be iterable, i.e. a string,
a list or dictionary). For example the following code::

	<?for (i, c) in "foo"?><?print i?>=<?print c?>;<?end for?>

prints::

	``0=f;1=o;2=o``
	

``xmlescape``
:::::::::::::

``xmlescape`` replaces the characters ``&``, ``<``, ``>``, ``'`` and ``"``
with the appropriate XML entity references in the argument. For example::

	<?print xmlescape("<'foo' & 'bar'>")?>

prints:

	``&lt;&apos;foo&apos; &amp; ;&apos;bar&apos&gt;``


``chr``
:::::::

``chr(x)`` returns a one-character string with a character with the codepoint
``x`` which must be an integer.


``ord``
:::::::

The argument for ``ord`` must be a one-character string. ``ord`` returns the
codepoint of that character as an integer.


``hex``
:::::::

Return the hexadecimal representation of the integer argument (with a leading
``0x``).


``oct``
:::::::

Return the octal representation of the integer argument (with a leading ``0o``).


``bin``
:::::::

Return the binary representation of the integer argument (with a leading ``0b``).


Methods
-------

"""

