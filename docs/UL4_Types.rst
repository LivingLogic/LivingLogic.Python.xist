.. _UL4_Types:

Types
#####

A type object can be used for testing whether an object is an instance of that
type with the function :ref:`isinstance() <UL4_isinstance>`.  Some type objects
are callable to create new instances of that type (all of the following builtin
type objects are).

A type object has the attributes ``__module__``, ``__name__`` and ``__doc__``.


``bool(obj=False, /)``
======================

``bool(foo)`` converts ``foo`` to an boolean. I.e. ``True`` or ``False`` is
returned according to the truth value of ``foo``. Calling ``bool`` without
arguments returns ``False``.


``int(obj=0, /, base=None)``
============================

``int(foo)`` converts ``foo`` to an integer. ``foo`` can be a string, a float,
a boolean or an integer. ``int`` can also be called with two arguments. In this
case the first argument must be a string and the second is the number base for
the conversion. Calling ``int`` without arguments returns ``0``.


``float(obj=0.0, /)``
=====================

``float(foo)`` converts ``foo`` to a float. ``foo`` can be a string, a float,
a boolean or an integer. Calling ``float`` without arguments returns ``0.0``.


``str(obj="", /)``
==================

``str(foo)`` converts ``foo`` to a string. If ``foo`` is ``None`` or ``Undefined``
the result will be the empty string. For lists and dictionaries the exact format
is undefined, but should follow Python's repr format. For color objects the
result is a CSS expression (e.g. ``"#fff"``). Calling ``str`` without arguments
returns the empty string.


``date(year, month, day, hour=0, minute=0, second=0, microsecond=0)``
=====================================================================

``date()`` creates a date object from the parameter passed in. ``date()``
supports from three parameters (``year``, ``month``, ``day``) upto seven
parameters (``year``, ``month``, ``day``, ``hour``, ``minute``, ``second``,
``microsecond``).


``timedelta(days=0, seconds=0, microseconds=0)``
================================================

``timedelta`` returns an object that represents a timespan. ``timedelta``
allows from zero to three arguments specifying the numbers of days, seconds and
microseconds. Passing negative values or values that are out of bounds (e.g.
24*60*60+1 seconds) is allowed. Arguments default to 0, i.e. ``timedelta()``
returns the timespan for "0 days, 0 seconds, 0 microseconds". In a boolean
context this object is treated as false (i.e. ``bool(timedelta()))`` returns
``False``). The following arithmetic operations are supported:

*	``date`` + ``timedelta``
*	``date`` - ``timedelta``
*	``timedelta`` + ``timedelta``
*	``timedelta`` - ``timedelta``
*	``number`` * ``timedelta``
*	``timedelta`` * ``number``
*	``timedelta`` / ``number``
*	``timedelta`` // ``int``


``monthdelta(months=0, /)``
===========================

``monthdelta`` returns an object that represents a timespan of a number of
months. ``monthdelta`` allows zero or one arguments. With zero arguments
``monthdelta`` returns the timespan for "0 months". In a boolean context this
object is treated as false (i.e. ``bool(monthdelta()))`` or
``bool(monthdelta(0)))`` return ``False``). The following arithmetic operations
are supported:

*	``date + monthdelta``
*	``date - monthdelta``
*	``monthdelta + monthdelta``
*	``monthdelta - monthdelta``
*	``int * monthdelta``
*	``monthdelta // int``

For operations involving ``date`` objects, if the resulting day falls out of the
range of valid days for the target month, the last day for the target month
will be used instead, i.e. ``<?print @(2000-01-31) + monthdelta(1)?>`` prints
``2000-02-29``.


``color(r=0, g=0, b=0, a=255)``
===============================

``color`` returns a color object. Each argument must be an integer between
0 and 255. Values will be clipped accordingly. For example

.. sourcecode:: ul4

	<?print color(0x33, 0x66, 0x99)?>

prints ``#369`` and

.. sourcecode:: ul4

	<?print color(0x33, 0x66, 0x99, 0xcc)?>

prints ``rgba(51,102,153,0.800)``.



``list(iterable=[], /)``
========================

``list(foo)`` converts ``foo`` to a list. This works for lists, strings and all
iterable objects. Calling ``list`` without arguments returns an empty list.


``dict(*args, **kwargs)``
=========================

``dict(foo)`` converts ``foo`` to a dictionary. For this, ``foo`` must be either
a dictionary itself, or an iterable of (key, value) pairs. ``dict()`` supports
multiple positional arguments. Later entries overwrite earlier ones.
(i.e. ``dict({17: 23}, {17: 42})`` returns ``{17: 42}``). ``dict`` also supports
arbitrary keyword arguments, which create dictionary entries with the name of
the argument as a string key, so ``dict(foo=42)`` returns ``{'foo': 42}``.
Calling ``dict`` without arguments returns an empty dictionary.


``set(iterable=[], /)``
=======================

``set(foo)`` converts ``foo`` to a set. This works for lists, strings and all
iterable objects. Calling ``set`` without arguments returns an empty set.
