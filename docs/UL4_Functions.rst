.. _UL4_functions:

Functions
#########

:mod:`ll.ul4c` supports a number of functions.


``today()``
===========

``today()`` returns the current date as a date object.


``now()``
=========

``now()`` returns the current date and time as a datetime object.


``utcnow()``
============

``utcnow()`` returns the current date and time as a datetime object in UTC.


``isundefined(obj, /)``
=======================

``isundefined(foo)`` returns ``True`` if ``foo`` is ``Undefined``, else
``False`` is returned:

.. sourcecode:: ul4

	data is <?if isundefined(data)?>undefined<?else?>defined<?end if?>!


``isdefined(obj, /)``
=====================

``isdefined(foo)`` returns ``False`` if ``foo`` is ``Undefined``, else
``True`` is returned:

.. sourcecode:: ul4

	data is <?if isdefined(data)?>defined<?else?>undefined<?end if?>!


``isnone(obj, /)``
==================

``isnone(foo)`` returns ``True`` if ``foo`` is ``None``, else ``False`` is
returned:

.. sourcecode:: ul4

	data is <?if isnone(data)?>None<?else?>something else<?end if?>!


``isbool(obj, /)``
==================

``isbool(foo)`` returns ``True`` if ``foo`` is ``True`` or ``False``, else
``False`` is returned.


``isint(obj, /)``
=================

``isint(foo)`` returns ``True`` if ``foo`` is an integer object, else ``False``
is returned.


``isfloat(obj, /)``
===================

``isfloat(foo)`` returns ``True`` if ``foo`` is a float object, else ``False``
is returned.


``isstr(obj, /)``
=================

``isstr(foo)`` returns ``True`` if ``foo`` is a string object, else ``False``
is returned.


``isdate(obj, /)``
==================

``isdate(foo)`` returns ``True`` if ``foo`` is a date object, else ``False``
is returned.


``istimedelta(obj, /)``
=======================

``istimedelta(foo)`` returns ``True`` if ``foo`` is a timedelta object, else
``False`` is returned.


``ismonthdelta(obj, /)``
========================

``ismonthdelta(foo)`` returns ``True`` if ``foo`` is a monthdelta object, else
``False`` is returned.


``islist(obj, /)``
==================

``islist(foo)`` returns ``True`` if ``foo`` is a list object, else ``False``
is returned.


``isdict(obj, /)``
==================

``isdict(foo)`` returns ``True`` if ``foo`` is a dictionary object, else
``False`` is returned.


``isset(obj, /)``
=================

``isset(foo)`` returns ``True`` if ``foo`` is a set object, else
``False`` is returned.


``isexception(obj, /)``
=======================

``isexception(foo)`` returns ``True`` if ``foo`` is an exception object, else
``False`` is returned.


``iscolor(obj, /)``
===================

``iscolor(foo)`` returns ``True`` if ``foo`` is a color object, else ``False``
is returned.


``istemplate(obj, /)``
======================

``istemplate(foo)`` returns ``True`` if ``foo`` is a template object, else
``False`` is returned.


.. _UL4_isinstance:

``isinstance(obj, type, /)``
============================

``istemplate(obj, type)`` returns ``True`` if ``obj`` is a instance of the
type ``type``. ``type`` must be a type object. For type objects see
:ref:`UL4_Types`. For example

.. sourcecode:: ul4

	<?print isinstance("gurk", str)?>

prints ``True``.


``repr(obj, /)``
================

``repr(foo)`` converts ``foo`` to a string representation that is useful for
debugging proposes. The output in most cases looks that the UL4 constant that
could be used to recreate the object.


``ascii(obj, /)``
=================

``ascii(foo)`` produces the same output as ``repr(foo)`` except that all
non-ASCII characters in the output for strings will be escaped.


``format(value, spec, lang="en")``
==================================

``format`` formats a value. Currently ``format`` supports the following types
for ``value``: ``date``, ``int`` and ``float`` (``float`` is only supported
in the Python version).

The second argument ``spec`` is a format specification string (whose format is
specific to the type of ``value``).

The third (optional) argument ``lang`` is the target language.

So for example

.. sourcecode:: ul4

	<?print format(@(2000-02-29), "%a, %d. %b. %Y", "de")?>

outputs ``Di, 29. Feb. 2000`` and

.. sourcecode:: ul4

	<?print format(42, "08b")?>

outputs ``00101010``.

UL4 tries to follow Pythons convention for the format string specification,
so for more information see the documentation for Pythons :func:`format`
function.


``slice(iterable, start=None, stop, step=None, /)``
===================================================

``slice`` returns a slice from a sequence or iterator. You can either pass the
stop index (i.e. ``slice(foo, 10)`` is an iterator over the first 10 items from
``foo``), or a start and stop index (``slice(foo, 10, 20)`` return the 11th upto
to 20th item from ``foo``) or a start and stop index and a step size. If given
start and stop must be non-negative and step must be positive.


``asjson(obj, /)``
==================

``asjson(foo)`` returns a JSON representation of the object ``foo``.
(Date objects, color objects and templates are not supported by JSON, but
``asjson`` will output the appropriate Javascript code for those objects).


``fromjson(string, /)``
=======================

``fromjson(foo)`` decodes the JSON string ``foo`` and returns the resulting
object. (Date objects, color objects and templates are not supported by
``fromjson``).


``asul4on(obj, /, indent=None)``
================================

``asul4on(foo)`` returns the UL4ON representation of the object ``foo``.


``fromul4on(dump, /)``
======================

``fromul4on(foo)`` decodes the UL4ON string ``foo`` and returns the resulting
object.


``csv(obj, /)``
===============

``csv(foo)`` formats the value ``foo`` for output into a CSV file.


``len(obj, /)``
===============

``len(foo)`` returns the length of a string, or the number of items in a list
or dictionary.


``round(number, /, digits=0)``
==============================
Returns ``number`` rounded to ``digits`` precision after the decimal point.
If ``digits`` is non-positive the returned value will always be of type ``int``.

For example ``round(42.123, 2)`` returns ``42.12`` and ``round(485, -2)``
returns 500.


``floor(number, /, digits=0)``
==============================
Returns ``number`` rounded down (i.e. towards -∞) to ``digits`` precision after
the decimal point. If ``digits`` is non-positive the returned value will always
be of type ``int``.

For example ``floor(42.567, 2)`` returns ``42.56`` and ``floor(485, -2)``
returns 400.


``ceil(number, /, digits=0)``
=============================
Returns ``number`` rounded up (i.e. towards ∞) to ``digits`` precision after
the decimal point. If ``digits`` is non-positive the returned value will always
be of type ``int``.

For example ``ceil(42.567, 2)`` returns ``42.57`` and ``ceil(485, -2)``
returns 500.


``any(iterable, /)``
====================

``any(foo)`` returns ``True`` if any of the items in the iterable ``foo`` is
true. Otherwise ``False`` is returns. If ``foo`` is empty ``False`` is returned.


``all(iterable, /)``
====================

``all(foo)`` returns ``True`` if all of the items in the iterable ``foo`` are
true. Otherwise ``False`` is returns. If ``foo`` is empty ``True`` is returned.


``enumerate(iterable, start=0)``
================================

Enumerates the items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and for each item in the original iterable returns a two
item list containing the item position and the item itself. For example the
following code:

.. sourcecode:: ul4

	<?for (i, c) in enumerate("foo")?>
		(<?print c?>=<?print i?>)
	<?end for?>

prints

.. sourcecode:: output

	(f=0)(o=1)(o=2)


``isfirstlast(iterable, /)``
============================

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the first
and/or last in the iterable. For example the following code:

.. sourcecode:: ul4

	<?for (first, last, c) in isfirstlast("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>)
		<?if last?>]<?end if?>
	<?end for?>

prints

.. sourcecode:: output

	[(f)(o)(o)]


``isfirst(iterable, /)``
========================

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the first
in the iterable. For example the following code:

.. sourcecode:: ul4

	<?for (first, c) in isfirst("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>)
	<?end for?>

prints

.. sourcecode:: output

	[(f)(o)(o)


``islast(iterable, /)``
=======================

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the last
in the iterable. For example the following code:

.. sourcecode:: ul4

	<?for (last, c) in islast("foo")?>
		(<?print c?>)
		<?if last?>]<?end if?>
	<?end for?>

prints

.. sourcecode:: output

	(f)(o)(o)]


``enumfl(iterable, /)``
=======================

This function is a combination of ``enumerate`` and ``isfirstlast``. It iterates
through items of the argument (which must be iterable, i.e. a string, a list
or dictionary) and gives information about whether the item is the first
and/or last in the iterable and its position. For example the following code:

.. sourcecode:: ul4

	<?for (index, first, last, c) in enumfl("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>=<?print index?>)
		<?if last?>]<?end if?>
	<?end for?>

prints

.. sourcecode:: output

	[(f=0)(o=1)(o=2)]


``first(iterable, /, default=None)``
====================================

``first`` returns the first element produced by an iterable object. If the
iterable is empty the default value (which is the second parameter and defaults
to ``None``) is returned.


``last(iterable, /, default=None)``
===================================

``last`` returns the last element produced by an iterable object. If the
iterable is empty the default value (which is the second parameter and defaults
to ``None``) is returned.


``xmlescape(obj, /)``
=====================

``xmlescape`` takes a string as an argument. It returns a new string where the
characters ``&``, ``<``, ``>``, ``'`` and ``"`` have been replaced with the
appropriate XML entity or character reference. For example:

.. sourcecode:: ul4

	<?print xmlescape("<'foo' & 'bar'>")?>

prints

.. sourcecode:: html

	&lt;&#39;foo&#39; &amp; ;&#39;bar&#39&gt;

If the argument is not a string, it will be converted to a string first.

``<?printx foo?>`` is a shortcut for ``<?print xmlescape(foo)?>``.


``min(*args, default=<nodefault>, key=None)``
=============================================

``min`` returns the minimum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``min`` returns the
minimum value of this argument. if called with one empty argument the value of
``default`` will be returned (if given, else an exception will be raised).

If ``key`` is given, it will be used for extracting comparison keys, i.e. those
keys will be compared instead of the items themselves for determining the
minimal item.

If multiple items are minimal, the function returns the first one encountered.


``max(*args, default=<nodefault>, key=None)``
=============================================

``max`` returns the maximum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``max`` returns the
maximum value of this argument. The arguments ``default`` and ``key`` work the
same way as for ``min()``.


``sum(iterable, /, start=0)``
=============================

``sum`` returns the sum of the number from the iterable passed in. The second
parameter is the start value (i.e. the value that will be added to the total sum)
and defaults to 0. For example the template ``<?print sum(range(101))?>`` will
output ``5050``.


``sorted(iterable, /, key=None, reverse=False)``
================================================

``sorted`` returns a sorted list with the items from its argument. For example:

.. sourcecode:: ul4

	<?for c in sorted('abracadabra')?><?print c?><?end for?>

prints

.. sourcecode:: output

	aaaaabbcdrr

Supported arguments are iterable objects, i.e. strings, lists, dictionaries
and colors.

If ``key`` is given, it will be used for extracting comparison keys, i.e. those
keys will be compared instead of the items themselves for determining the
final order.

If ``reverse`` is true, the sort order will be reversed.


``chr(i, /)``
=============

``chr(i)`` returns a one-character string containing the character with the
code point ``i``. ``i`` must be an integer. For example ``<?print chr(0x61)?>``
outputs ``a``.


``ord(c, /)``
=============

This is the inverse function to ``chr`` The argument for ``ord`` must be a
one-character string. ``ord`` returns the code point of that character as an
integer. For example ``<?print ord('a')?>`` outputs ``97``.


``hex(number, /)``
==================

Return the hexadecimal representation of the integer argument (with a leading
``0x``). For example ``<?print hex(42)?>`` outputs ``0x2a``.


``oct(number, /)``
==================

Return the octal representation of the integer argument (with a leading ``0o``).
For example ``<?print oct(42)?>`` outputs ``0o52``.


``bin(number, /)``
==================

Return the binary representation of the integer argument (with a leading ``0b``).
For example ``<?print bin(42)?>`` outputs ``0b101010``.


``range(start=None, stop, step=None, /)``
=========================================

``range`` returns an object that can be iterated and will produce consecutive
integers up to the specified argument. With two arguments the first is the start
value and the second is the stop value. With three arguments the third one is
the step size (which can be negative). For example the following template:

.. sourcecode:: ul4

	<?for i in range(4, 10, 2)?>(<?print i?>)<?end for?>

prints

.. sourcecode:: output

	(4)(6)(8)


``rgb(r, g, b, a=1.0)``
=======================

``rgb`` returns a color object. It can be called with

*	three arguments, the red, green and blue values. The alpha value will be
	set to 255;
*	four arguments, the red, green, blue and alpha values.

Arguments are treated as values from 0 to 1 and will be clipped accordingly. For
example:

.. sourcecode:: ul4

	<?print rgb(1, 1, 1)?>

prints ``#fff``.


``md5(string, /)``
==================

``md5(s)`` returns the MD5 hash of the string ``s``.


``scrypt(string, /, salt)``
===========================

``scrypt(str, salt)`` returns the scrypt hash of the string ``str`` using the
salt value ``salt``. The returned string contains 256 hex digits.

For more info on scrypt, see https://en.wikipedia.org/wiki/Scrypt

.. note::
	``scrypt`` is not implemented in the Javascript version of UL4.


``random()``
============

``random()`` returns a random float value between 0 (included) and 1 (excluded).


``randrange(start=None, stop, step=None, /)``
=============================================

``randrange(start, stop, step)`` returns a random integer value between ``start``
(included) and ``stop`` (excluded). ``step`` specifies the step size (i.e.
when ``r`` is the random value, ``(r-start) % step`` will always be ``0``).
``step`` and ``start`` can be omitted.


``randchoice(seq)``
===================

``randchoice(seq)`` returns a random item from the sequence ``seq``.


``urlquote(string)``
====================

``urlquote`` escaped special characters for including the output in URLs. For
example:

.. sourcecode:: ul4

	<?print urlquote("/\xff")?>

prints

.. sourcecode:: output

	%2F%C3%BF

``urlunquote(string)``
======================

``urlunquote`` is the inverse function to ``urlquote``. So:

.. sourcecode:: ul4

	<?print urlunquote("%2F%C3%BC")?>

prints

.. sourcecode:: output

	/ü


``type(obj, /)``
================

``type`` returns the type of an object as a type object. For type object see the
following description.


``getattr(obj, attrname, default=?, /)``
========================================

``getattr`` returns the attribute named ``attrname`` of the object ``obj``. If
``obj`` doesn't have an attribute with that name ``default`` will returned
(when passed, else an ``UndefinedKey`` object will returned).


``hasattr(obj, attrname, /)``
=============================

``hasattr`` returns whether the object ``obj`` has an attribute named
``attrname``.
