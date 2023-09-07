.. _UL4_expressions:

Expressions
###########

:mod:`ll.ul4c` supports many of the operators supported by Python. The following
subchapters describe all expressions/operators that UL4 supports and are ordered
from highest precedence to lowest.


Generator expressions
=====================

UL4 supports generator expressions with look like list comprehensions without
the square brackets. Generator expression do not create lists in memory but
instead return an iterable that can be iterated once. Function and methods
that require an iterable argument can directly consume such iterables:

.. sourcecode:: ul4

	<?print ", ".join("(" + c + ")" for c in "gurk")?>

will output

.. sourcecode:: output

	(g), (u), (r), (k)

Outside of function/method arguments (or when more that one argument is passed)
parentheses are required around generator expressions:

.. sourcecode:: ul4

	<?code ge = ("(" + c + ")" for c in "gurk")?>
	<?print ", ".join(ge)?>

.. hint::
	Generator expressions are implemented by
	:class:`ll.ul4c.GeneratorExpressionAST`.


Index/slice access
==================

Index and slice access is available for all container types, i.e. in the
expression ``a[b]`` the following type combinations are supported:

*	string, integer: Returns the ``b``\th character from the string ``a``.
	Note that negative ``b`` values are supported and are relative to the end,
	so ``a[-1]`` is the last character.

*	list, integer: Returns the ``b``\th list entry of the list ``a``. Negative
	``b`` values are supported too.

*	dict, string: Return the value from the dictionary ``a`` corresponding to
	the key ``b``. Note that some implementations might support keys other
	than strings too. (The Python and Java implementations do for example.
	The Javascript implementation does too, if ``Map`` is supported.)

If the specified key doesn't exist or the index is out of range for the string
or list, a special "undefined" object is returned.

Slices are also supported (for list and string objects). As in Python one or
both of the indexes may be missing to start at the first or end after the last
character/item. Negative indexes are relative to the end. Indexes that are out
of bounds are simply clipped, so

.. sourcecode:: ul4

	<?print "Hello, World!"[7:-1]?>

prints ``World`` and 

.. sourcecode:: ul4

	<?print "Hello, World!"[:-8]?>

prints ``Hello``.

.. hint::
	Index/slice access is implemented by :class:`ll.ul4c.ItemAST`.


Attribute access
================

For string keys it's also possible to access dictionary entries via the
attribute access operator ``.``, i.e. ``foo.key`` is the same as ``foo["key"]``
if ``foo`` is a dictionary.

.. hint::
	Attribute access is implemented by :class:`ll.ul4c.AttrAST`.


Function calls
==============

A function call in UL4 looks like this: ``date(2014, 10, 9, 17, 29)``.
(this returns the date object ``@(2014-10-09T17:29)``). Some of the trailing
arguments in a function call might be optional and have default values.
For example the first three arguments for the ``date`` function (``year``,
``month`` and ``day``) are required, the remaining four arguments (``hour``,
``minute``, ``second`` and ``microsecond``) are optional and default to ``0``.

Parameter values can also be passed via keyword arguments, i.e.
``date(2014, 10, 9)`` could also be written as
``date(day=9, month=10, year=2014)``.

Furthermore Python's ``*`` and ``**`` syntax is supported for passing additional
positional or keyword arguments. For example:

.. sourcecode:: ul4

	<?code args = [2014, 10, 9, 17, 29]?>
	<?code d = date(*args)?>

is the same as:

.. sourcecode:: ul4

	<?code d = date(2014, 10, 9, 17, 29)?>

The same can also be done with a keyword dictionary and the ``**`` syntax:

.. sourcecode:: ul4

	<?code kwargs = {"day": 9, "month": 10, "year": 2014, "hour": 17: "minute": 29}?>
	<?code d = date(**kwargs)?>

Of course it's also possible to mix argument passing mechanics:

.. sourcecode:: ul4

	<?code d = date(2014, *[10, 9], **{"hour": 17, "minute": 29})?>

or

.. sourcecode:: ul4

	<?code d = date(2014, month=10, day=9, **{'hour': 17, 'minute': 29})?>

However the ``*`` and ``**`` arguments can only be use at the end of the
argument list and positional arguments must always be before keyword arguments.

A list of builtin functions can be found in :ref:`UL4_functions`.

.. hint::
	This documentation uses Python's ``/`` and ``*`` notation to specify
	positional-only and keyword-only arguments. So

	.. sourcecode:: ul4

		<?ul4 f(x, /, y, *, z)?>

	means that the function ``f`` accepts the parameter ``x`` only when passed by
	position, ``y`` can be passed either by position or by keyword and ``z`` will
	only be accepted when passed by keyword.

.. hint::
	Function calls are implemented by :class:`ll.ul4c.CallAST`.


Unary operators
===============


Arithmetic negation
-------------------

The unary operator ``-`` inverts the sign of its operand, which must be an
integer, float of boolean value:

.. sourcecode:: ul4

	<?code x = 42?><?print -x?>

prints ``-42``. For ``-`` boolean values are treated as the numbers ``0`` and
``1``, i.e.:

.. sourcecode:: ul4

	<?code x = True?><?print -x?>

prints ``-1``.

.. hint::
	Arithmetic negation is implemented by :class:`ll.ul4c.NegAST`.


Binary negation
---------------

The unary operator ``~`` inverts the bits of an integer or boolean value.
Non-negative numbers are interpreted as having an unlimited number of leading
``0`` bits and negative numbers are interpreted as having an unlimited number
of leading ``1`` bits. The means that ``~x`` will be negative if ``x`` is
non-negative and vice versa.

.. hint::
	Arithmetic negation is implemented by :class:`ll.ul4c.BitNotAST`.


Multiplicative binary operators
===============================


Multiplication
--------------

The multiplication operator ``*`` returns the arithmetic product of its
operands (which must be integer, float or boolean values). Furthermore it's
possible to multiply a sequence (i.e. a string or list) with a non-negative
integer to get a new sequences that repeats the items of the original sequence a
number of times, e.g. ``"foo" * 2`` returns ``"foofoo"`` and ``[1, 2, 3] * 3``
return ``[1, 2, 3, 1, 2, 3, 1, 2, 3]``. Multiplying with ``0`` returns an empty
string or list.

.. hint::
	Multiplication is implemented by :class:`ll.ul4c.MulAST`.


True division
-------------

The true division operator ``/`` returns the quotient of its operands (which
must be integer, float or boolean values). The result is always a float value.
``1/2`` returns ``0.5``.

.. hint::
	True division is implemented by :class:`ll.ul4c.TrueDivAST`.


Floor division
--------------

The float division operator ``//`` returns the quotient of its operands (which
must be integer, float or boolean values) rounded down to an integer (rounding
is always done towards -infinity, i.e. ``(-25)/10`` returns ``-3``). If any of
the operands is a float the result is a float too, otherwise it's an integer.

.. hint::
	Floor division is implemented by :class:`ll.ul4c.FloorDivAST`.


Modulo
------

The modulo operator ``%`` returns the remainder from the division of the first
operand by the second, e.g. ``15 % 7`` returns ``1``.

.. hint::
	The modulo operator is implemented by :class:`ll.ul4c.ModAST`.


Additive binary operators
=========================


Addition
--------

The addition operator ``+`` returns the sum of its operands (which must be
integer, float or boolean values). Furthermore sequences of the same type can be
added, so ``"foo" + "bar"`` returns ``"foobar"`` and ``[1, 2] + [3, 4]`` returns
``[1, 2, 3, 4]``.

.. hint::
	Addition is implemented by :class:`ll.ul4c.AddAST`.


Subtraction
-----------

The subtraction operator ``-`` returns the difference of its operands (which
must be integer, float or boolean values).

.. hint::
	Subtraction is implemented by :class:`ll.ul4c.SubAST`.


Bit shift operators
===================


Binary left shift operator
--------------------------

The binary left shift operator ``<<`` shifts the bits of its first operand (an
integer or boolean) to the left by the number of positions given by the second
operand (which must also be an integer or boolean).

.. hint::
	The binary left shift operator is implemented by :class:`ll.ul4c.ShiftLeftAST`.


Binary right shift operator
---------------------------

The binary right shift operator ``>>`` shifts the bits of its first operand (an
integer or boolean) to the right by the number of positions given by the second
operand (which must also be an integer or boolean).

.. hint::
	The binary right shift operator is implemented by :class:`ll.ul4c.ShiftRightAST`.


Binary bitwise "and" operator
=============================

The bitwise and operator ``&`` returns the bitwise "and" combination of its
operands (which must be integer or boolean values). E.g. ``6 & 3`` returns ``2``.

As with the unary operator ``~``, negative numbers are interpreted as having an
unlimited number of leading ``1`` bits.

.. hint::
	The binary bitwise "and" operator is implemented by :class:`ll.ul4c.BitAndAST`.


Binary bitwise "exclusive or" operator
======================================

The bitwise exclusive or operator ``^`` returns the bitwise exclusive "or"
combination of its operands (which must be integer or boolean values).
E.g. ``6 ^ 3`` returns ``5``.

Negative numbers are again interpreted as having an unlimited number of leading
``1`` bits.

.. hint::
	The binary bitwise "exclusive or" operator is implemented by
	:class:`ll.ul4c.BitXOrAST`.


Binary bitwise "inclusive or" operator
======================================

The bitwise inclusive or operator ``|`` returns the bitwise inclusive "or"
combination of its operands (which must be integer or boolean values).
E.g. ``6 | 3`` returns ``7``.

Negative numbers are again interpreted as having an unlimited number of leading
``1`` bits.

.. hint::
	The binary bitwise "inclusive or" operator is implemented by
	:class:`ll.ul4c.BitOrAST`.


Binary comparison operators
===========================

The comparison operators ``==``, ``!=``, ``<``, ``<=``, ``>`` and ``>=`` compare
the value of the two operands. ``==`` and ``!=`` support comparison of all
types of object. All others support comparison of "compatible" objects, which
means all "number" objects (integer, float and boolean) can be compared with
each other, all other objects can only be compared to objects of the same type.

.. hint::
	These operators are implemented by :class:`ll.ul4c.EQAST`,
	:class:`ll.ul4c.NEAST`, :class:`ll.ul4c.LTAST`, :class:`ll.ul4c.LEAST`,
	:class:`ll.ul4c.GTAST` and :class:`ll.ul4c.GEAST`.


Identity comparison operators
=============================

The comparison operators ``is`` and ``is not`` test whether both operands refer
to the same object or not.

Note that the behaviour of these operators for "atomic" immutable objects
(like integers, floats and strings) is implementation defined.

.. hint::
	These operators are implemented by :class:`ll.ul4c.IsAST` and
	:class:`ll.ul4c.IsNotAST`.

Containment tests
=================

The ``in`` operator
-------------------

The ``in`` operator tests whether the first operand is contained in the second
operand. In the expression ``a in b`` the following type combinations are
supported:

*	string, string: Checks whether ``a`` is a substring of ``b``.
*	any object, list: Checks whether the object ``a`` is in the list ``b``
	(comparison is done by value not by identity)
*	string, dict: Checks whether the key ``a`` is in the dictionary ``b``.
	(Note that some implementations might support keys other than strings too.
	E.g. Python and Java do, Javascript does only for ``Map`` objects.)

.. hint::
	The ``in`` operator is implemented by :class:`ll.ul4c.ContainsAST`.


The ``not in`` operator
-----------------------

The ``not in`` operator returns the inverted result of the ``in`` operator, i.e.
it tests whether the first operand is not contained in the second operand.

.. hint::
	The ``not in`` operator is implemented by :class:`ll.ul4c.NotContainsAST`.


Boolean negation
================

The unary operator ``not`` inverts the truth value of its operand. I.e.
``not x`` is ``True`` for ``None``, ``False``, the undefined value, ``0``,
``0.0``, empty lists, strings, dictionaries and other empty containers and
``False`` for everything else.

.. hint::
	The boolean negation operator is implemented by :class:`ll.ul4c.NotAST`.


Boolean "and" operator
======================

The binary operator ``and`` returns whether both of its operands are true.
It works like Python ``and`` operator by short-circuiting operand evaluation,
i.e. if the result is clear from the first operand the seconds won't be
evaluated.

Furthermore ``and``  always return one of the operands.

So ``a and b`` first evaluates ``a``; if ``a`` is false, its value is returned;
otherwise, ``b`` is evaluated and the resulting value is returned.

.. hint::
	The boolean "and" operator is implemented by :class:`ll.ul4c.AndAST`.


Boolean "or" operator
=====================

The binary operator ``or`` returns whether any of its operands is true. Like
``and`` evaluation is short-circuited and one of the operands is returned.

For example, the following code will output the ``data.title`` object if it's
true, else ``data.id`` will be output:

.. sourcecode:: ul4

	<?printx data.title or data.id?>

.. hint::
	The boolean "or" operator is implemented by :class:`ll.ul4c.OrAST`.


Conditional expression
======================

The conditional expression (also called an "inline if") ``a if c else b`` first
evaluates the condition ``c``. If it is true ``a`` is evaluated and returned
else ``b`` is evaluated and returned.

.. hint::
	The "inline if" operator is implemented by :class:`ll.ul4c.IfAST`.
