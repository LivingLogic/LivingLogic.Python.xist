UL4 -- A templating language
############################

:mod:`ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.ul4c` compiles a template to an internal format, which makes it
possible to implement renderers for these templates in multiple programming
languages.

Apart from this Python implementation there are implementations for Java_ (both
a compiler and renderer) and Javascript_ (renderer only).

.. _Java: https://github.com/LivingLogic/LivingLogic.Java.ul4
.. _Javascript: https://github.com/LivingLogic/LivingLogic.Javascript.ul4


Embedding
=========

In the template source any text surrounded by ``<?`` and ``?>`` is a "template
tag". The first word inside the tag is the tag type. It defines what the tag
does. For example ``<?print foo?>`` is a print tag (it prints the value of the
variable ``foo``). A complete example template looks like this::

	<?if data?>
		<ul>
			<?for item in data?>
				<li><?print xmlescape(item)?></li>
			<?end for?>
		</ul>
	<?end if?>

(For text formats where the delimiters ``<?`` and ``?>`` collide with elements
that are used often or where using these delimiters is inconvenient it's
possible to specify a different delimiter pair when compiling the template.)

A complete Python program that compiles a template and renders it might look
like this::

	from ll import ul4c

	code = '''
		<?if data?>
			<ul>
				<?for item in data?>
					<li><?print item?></li>
				<?end for?>
			</ul>
		<?end if?>
	'''

	template = ul4c.Template(code)

	print(template.renders(data=["Python", "Java", "Javascript", "PHP"]))

The variables that should be available to the template code can be passed to the
method :meth:`~ll.ul4c.Template.renders` as keyword arguments.
:meth:`~ll.ul4c.Template.renders` returns the final rendered output as a string.
Alternatively the method :meth:`~ll.ul4c.Template.render` can be used, which is
a generator and returns the output piecewise.


Builtin types
=============

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
*	UL4 templates

Note that depending on the implementation language of the renderer additional
types might be supported, e.g. a Python renderer will probably support both
tuples and lists and anything supporting :meth:`__getitem__` (or :meth:`__iter__`
when the list is used in a loop) for lists, Java might support anything
implementing the ``List`` interface (or the ``Collection`` interface if the list
is used in a loop).

Objects of these types can either be passed to the template in the call to the
render function, or the template can create objects of thoses types itself. The
syntax for creating such a constant is very similar to Python's syntax.


The "null" constant
-------------------

The "null" constant can be referred to via ``None``.


Boolean constants
-----------------

The boolean constants can be referred to via ``True`` and ``False``.


Integer constants
-----------------

Integer constants can be written in decimal, hexadecimal, octal and binary:
``42``, ``0x2a``, ``0o52`` and ``0b101010`` all refer to the integer value 42.


Float constants
---------------

Float constants must contain a decimal point or an exponential specifier,
e.g. ``42.``, ``4e23``.


String constants
----------------

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


Date constants
--------------

Date objects have a date and time including microseconds. Date constants can be
created like this:

*	``@(2008-12-24)``

*	``@(2008-12-24T12:34)``

*	``@(2008-12-24T12:34:56)``

*	``@(2008-12-24T12:34:56.987654)``


Color constants
---------------

Color values are 8 bit red, green, blue and alpha values. Color constants can
be created like this:

*	``#fff``

*	``#fff8``

*	``#0063a8``

*	``#0063a880``

The variants with 3 or 6 hex digits will create a color object with an alpha
value of 255.


Lists
-----

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
------------

Dictionaries can be created like this:

*	``{}``

*	``{1: 2, 3: 4}``

*	``{"foo": 17, "bar": 23}``

``**`` expressions can be used to expand other dictionaries inplace, so::

	{"foo": 17, **{"bar": 23, "baz": 42}}

is equivalent to ::

	{"foo": 17, "bar": 23, "baz": 42}

The ``**`` must be a dictonary or a list of key/value pairs.

It is also possible to create a dictionary with a dictionary comprehension::

	{ c.upper() : "(" + c + ")" for c in "hurz" if c < "u"}

This will create the dictionary ::

	{ "H": "(h)", "R": "(r)"}

The ``if`` condition is optional, i.e. ::

	{ c.upper() : "(" + c + ")" for c in "hurz"}

will create the dictionary ::

	{ "H": "(h)", "U": "(u)", "R": "(r)", "Z": "(z)"}


Sets
----

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
------------------------

The object ``Undefined`` will be returned when a non-existant variable, a
non-existant dictionary entry or an index that is out of range for a list/string
is accessed.


Template code
=============

The template code tries to mimic Python syntax as far as possible, but is
limited to what is required for templates and does not allow executing arbitrary
Python statements. In some spots it also borrows Javascript semantics.

:mod:`ll.ul4c` supports the following tag types:


``print``
---------

The ``print`` tag outputs the value of a variable or any other expression. If
the expression doesn't evaluate to a string it will be converted to a string
first. The format of the string depends on the renderer, but should follow
Python's ``str()`` output as much as possible::

	<h1><?print person.lastname?>, <?print person.firstname?></h1>

Printing ``None`` or undefined objects produces no output.


``printx``
----------

The ``printx`` tag outputs the value of a variable or any other expression and
escapes the characters ``<``, ``>``, ``&``, ``'`` and ``"`` with the appropriate
character or entity references for XML or HTML output.


``for``
-------

The ``for`` tag can be used to loop over the items in a list, the characters in
a string, the keys in a dictionary or any other iterable object. The end of the
loop body must be marked with an ``<?end for?>`` tag::

	<ul>
		<?for person in data.persons?>
			<li><?print person.lastname?>, <?person.firstname?></li>
		<?end for?>
	</ul>

In ``for`` loops variable unpacking is supported, so you can do the following::

	<?for (key, value) in dict.items()?>

if ``dict`` is a dictionary.

This unpacking can be arbitrarily nested, i.e. the following is possible too::

	<?for (i, (key, value)) in enumerate(dict.items())?>


``break``
---------

The ``break`` tag can be used to break out of the innermost running loop.


``continue``
------------

The ``continue`` tag can be used to skip the rest of the loop body of the
innermost running loop and continue with the next iteration of the loop.


``if``
------

The ``if`` tag can be used to output a part of the template only when a
condition is true. The end of the ``if`` block must be marked with an
``<?end if?>`` tag. The truth value of an object is mostly the same as in Python:

*	``None`` is false.
*	The integer ``0`` and the float value ``0.0`` are false.
*	Empty strings, lists and dictionaries are false.
*	``timedelta`` and ``monthdelta`` objects for an empty timespan (i.e.
	``timedelta(0, 0, 0)`` and ``monthdelta(0)``) are false.
*	``False`` is false.
*	``Undefined`` is false.
*	Anything else is true.

For example we can output the person list only if there are any persons::

	<?if persons?>
		<ul>
			<?for person in persons?>
				<li><?print person.lastname?>, <?person.firstname?></li>
			<?end for?>
		</ul>
	<?end if?>

``elif`` and ``else`` are supported too::

	<?if persons?>
		<ul>
			<?for person in persons?>
				<li><?print person.lastname?>, <?person.firstname?></li>
			<?end for?>
		</ul>
	<?else?>
		<p>No persons found!</p>
	<?end if?>

or::

	<?if len(persons)==0?>
		No persons found!
	<?elif len(persons)==1?>
		One person found!
	<?else?>
		<?print len(persons)?> persons found!
	<?end if?>


``code``
--------

The ``code`` tag can contain statements that define or modify variables or
expressions which will be evaluated for their side effects. Apart from the
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


``render``
----------

The ``render`` tag allows one template to call other templates. The following
Python code demonstrates this::

	from ll import ul4c

	# Template 1
	source1 = """\
	<?if data?>\
	<ul>
	<?for i in data?><?render itemtmpl(item=i)?><?end for?>\
	</ul>
	<?end if?>\
	"""

	tmpl1 = ul4c.Template(source1)

	# Template 2
	source2 = "<li><?print xmlescape(item)?></li>\n"

	tmpl2 = ul4c.Template(source2)

	# Data object for the outer template
	data = ["Python", "Java", "Javascript", "PHP"]

	print(tmpl1.renders(itemtmpl=tmpl2, data=data))

This will output::

	<ul>
	<li>Python</li>
	<li>Java</li>
	<li>Javascript</li>
	<li>PHP</li>
	</ul>

I.e. templates can be passed just like any other object as a variable.
``<?render itemtmpl(item=i)?>`` renders the ``itemtmpl`` template and passes
the ``i`` variable, which will be available in the inner template under the
name ``item``.


``renderx``
-----------

The ``renderx`` tag works similar to the ``render`` tag, except that the output
of the template called will be XML escaped (like ``printx`` does). The following
Python code demonstrates this::

	from ll import ul4c

	# Template 1
	tmpl1 = ul4c.Template("<&>")

	# Template 2
	tmpl2 = ul4c.Template("<?renderx tmpl()?>\n")

	print(tmpl1.renders(tmpl=tmpl2))

This will output::

	&lt;&amp;&gt;


``def``
-------

The ``def`` tag defines a new template as a variable. Usage looks like this::

	<?def quote?>
		"<?print text?>"
	<?end def?>

This defines a local variable ``quote`` that is a template object. This template
can be rendered like any other template that has been passed to the outermost
template::

	<?render quote(text="foo")?>

It's also possible to include a signature in the definition of the template.
This makes it possible to define default values for template variables and to
call templates with positional arguments::

	<?def quote(text='foo')?>
		"<?print text?>"
	<?end def?>
	<?render quote()?> and <?render quote("bar")?>

This will output ``"foo" and "bar"``.

``*`` and ``**`` arguments are also supported::

	<?def weightedsum(*args)?>
		<?print sum(i*arg for (i, arg) in enumerate(args, 1))?>
	<?end def?>
	<?render weightedsum(17, 23, 42)?>

This will print ``189`` (i.e. ``1 * 17 + 2 * 23 + 3 * 42``).


``renderblocks``
----------------

The ``renderblocks`` tag is syntactic sugar for rendering a template and
passing other templates as arguments in the call. For example if we have the
following template::

	<?def page(head, body, lang="en", doctype=False)?>
		<?if doctype?>
			<!DOCTYPE html>
		<?end if?>
		<html lang="<?printx lang?>">
			<head>
				<?render head()?>
			</head>
			<body>
				<?render body()?>
			</body>
		</html>
	<?end def?>

then we can render this template in the following way::

	<?renderblocks page(lang="de", doctype=True)?>
		<?def head?>
			<title>Foo</title>
		<?end def?>
		<?def body?>
			<h1>Bar!</h1>
		<?end def?>
	<?end renderblocks?>

This is syntactic sugar for::

	<?def head?>
		<title>Foo</title>
	<?end def?>
	<?def body?>
		<h1>Bar!</h1>
	<?end def?>
	<?render page(lang="de", doctype=True, head=head, body=body)?>

In both cases the output will be::

	<!DOCTYPE html>
	<html lang="de">
		<head>
			<title>Foo</title>
		</head>
		<body>
			<h1>Bar!</h1>
		</body>
	</html>

All variables defined between ``<?renderblocks page(...)?>`` and
``<?end renderblocks?>`` are passed as additional keyword arguments in the
render call to ``page``. (But note that those variables will be local to the
``<?renderblocks?>`` block, i.e. they will not leak into the surrounding
code.)


``renderblock``
---------------

The ``renderblock`` is a special version of ``renderblocks``. The complete
content of the ``renderblock`` block will be wrapped in a signatureless template
named ``content`` and this template will be passed as the keyword argument
``content`` to the render call. With this we can define a generic template for
HTML links::

	<?def a(content, **attrs)?>
		<a<?for (an, av) in attrs.items()?> <?print an?>="<?printx av?>"<?end for?>>
			<?render content()?>
		</a>
	<?end def?>

and then use it like this::

	<?renderblock a(class="extern", href="http://www.python.org/")?>
		Link to the Python homepage
	<?end renderblock?>

The output will be::

	<a class="extern" href="http://www.python.org/">
		Link to the Python homepage
	</a>


``ul4``
-------

The ``ul4`` tag can be used to specify a name and a signature for the template
itself. This overwrites the name and signature specified in the
:class:`ul4c.Template` constructor::

	>>> from ll import ul4c
	>>> t = ul4c.Template("<?ul4 foo(x)?><?print x?>")
	>>> t.name
	'foo'
	>>> t.signature
	<Signature (x)>


``note``
--------

A ``note`` tag is a comment, i.e. the content of the tag will be completely
ignored.


``doc``
-------

A ``doc`` tag contains the documentation of the template itself. The content
of the ``<?doc?>`` tag is available as the ``doc`` attribute::

	>>> from ll import ul4c
	>>> t = ul4c.Template("<?doc foo?><?print x?>")
	>>> t.doc
	'foo'

Each ``<?doc?>`` contains the documentation for the template to which the
``<?doc?>`` tag belongs, i.e. if the ``<?doc?>`` tag is at the outermost
level, it belongs to the outermost template. If the ``<?doc?>`` tag is inside
a local template, it is the documentation for the local template. If multiple
``<?doc?>`` tags are given, only the first one will be used, all later ones will
be ignored.

Note that the template name, documentation and signature are accessible inside
the templates themselves, i.e. ::

	<?def f(x=17, y=23)?>
		<?doc return the sum of x and y?>
		<?return x+y?>
	<?end def?>
	<?print f.name?>
	<?print f.doc?>
	<?print f.signature?>

will output ::

	f
	return the sum of x and y
	(x=17, y=23)


``whitespace``
--------------
The ``whitespace`` tag can be used to overwrite the handling of whitespace in
the template. For more info see the chapter on whitespace handling at the end.


Nested scopes
-------------

UL4 templates support lexical scopes. This means that a template that is defined
(via ``<?def?>``) inside another template has access to the local variables
of the outer template. The inner template sees the state of the variables at
the point in time when the inner templates gets called. The following example
will output ``2``::

	<?code i = 1?>
	<?def x?>
		<?print i?>
	<?end def?>
	<?code i = 2?>
	<?render x()?>


Expressions
-----------

:mod:`ll.ul4c` supports many of the operators supported by Python. The following
subchapters describe all expression/operators that UL4 supports and are ordered
from highest precedence to lowest.


Generator expressions
"""""""""""""""""""""

UL4 supports generator expressions with look like list comprehensions without
the square brackets. Generator expression do not create lists in memory but
instead return an iterable that can be iterated once. Function and methods
that require an iterable argument can directly consume such iterables::

	<?print ", ".join("(" + c + ")" for c in "gurk")?>

will output::

	(g), (u), (r), (k)

Outside of function/method arguments (or when more that one argument is passed)
parentheses are required around generator expressions::

	<?code ge = ("(" + c + ")" for c in "gurk")?>
	<?print ", ".join(ge)?>


Index/slice access
""""""""""""""""""

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
of bounds are simply clipped:

*	``<?print "Hello, World!"[7:-1]?>`` prints ``World``.

*	``<?print "Hello, World!"[:-8]?>`` prints ``Hello``.


Attribute access
""""""""""""""""

For string keys it's also possible to access dictionary entries via the
attribute access operator ``.``, i.e. ``foo.key`` is the same as ``foo["key"]``
if ``foo`` is a dictionary.


Function calls
""""""""""""""

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
positional or keyword arguments. For example::

	<?code args = [2014, 10, 9, 17, 29]?>
	<?code d = date(*args)?>

is the same as::

	<?code d = date(2014, 10, 9, 17, 29)?>

The same can also be done with a keyword dictionary and the ``**`` syntax::

	<?code kwargs = {"day": 9, "month": 10, "year": 2014, "hour": 17: "minute": 29}?>
	<?code d = date(**kwargs)?>

Of course it's also possible to mix argument passing mechanics::

	<?code d = date(2014, *[10, 9], **{"hour": 17, "minute": 29})?>

or::

	<?code d = date(2014, month=10, day=9, **{'hour': 17, 'minute': 29})?>

However the ``*`` and ``**`` arguments can only be use at the end of the
argument list and positional arguments must always be before keyword arguments.

A list of builtin functions can be found in a later chapter.


Unary operators
"""""""""""""""

Arithmetic negation
+++++++++++++++++++

The unary operator ``-`` inverts the sign of its operand, which must be an
integer, float of boolean value::

	<?code x = 42?><?print -x?>

prints ``-42``. For ``-`` boolean values are treated as the numbers ``0`` and
``1``, i.e.::

	<?code x = True?><?print -x?>

prints ``-1``.


Binary negation
+++++++++++++++

The unary operator ``~`` inverts the bits of an integer or boolean value.
Non-negative numbers are interpreted as having an unlimited number of leading
``0`` bits and negative numbers are interpreted as having an unlimited number
of leading ``1`` bits. The means that ``~x`` will be negative if ``x`` is
non-negative and vice versa.


Multiplicative binary operators
"""""""""""""""""""""""""""""""

Multiplication
++++++++++++++

The multiplication operator ``*`` returns the arithmetic product of its
operands (which must be integer, float or boolean values). Furthermore it's
possible to multiply a sequence (i.e. a string or list) with a non-negative
integer to get a new sequences that repeats the items of the original sequence a
number of times, e.g. ``"foo" * 2`` returns ``"foofoo"`` and ``[1, 2, 3] * 3``
return ``[1, 2, 3, 1, 2, 3, 1, 2, 3]``. Multiplying with ``0`` returns an empty
string or list.

True division
+++++++++++++

The true division operator ``/`` returns the quotient of its operands (which
must be integer, float or boolean values). The result is always a float value.
``1/2`` returns ``0.5``.


Floor division
++++++++++++++

The float division operator ``//`` returns the quotient of its operands (which
must be integer, float or boolean values) rounded down to an integer. If any of
the operands is a float the result is a float too, otherwise it's an integer.

``1//2`` returns ``0``.


Modulo
++++++

The modulo operator ``%`` returns the remainder from the division of the first
operand by the second, e.g. ``15 % 7`` returns ``1``.


Additive binary operators
"""""""""""""""""""""""""

Addition
++++++++

The addition operator ``+`` returns the sum of its operands (which must be
integer, float or boolean values). Furthermore sequences of the same type can be
added, so ``"foo" + "bar"`` returns ``"foobar"`` and ``[1, 2] + [3, 4]`` returns
``[1, 2, 3, 4]``.


Substraction
++++++++++++

The substraction operator ``-`` returns the difference of its operands (which
must be integer, float or boolean values).


Bit shift operators
"""""""""""""""""""

Binary left shift operator
++++++++++++++++++++++++++

The binary left shift operator ``<<`` shifts the bits of its first operand (an
integer or boolean) to the left by the number of positions given by the second
operand (which must also be an integer or boolean).

Binary right shift operator
+++++++++++++++++++++++++++

The binary right shift operator ``>>`` shifts the bits of its first operand (an
integer or boolean) to the right by the number of positions given by the second
operand (which must also be an integer or boolean).


Binary bitwise and operator
"""""""""""""""""""""""""""

The bitwise and operator ``&`` returns the bitwise "and" combination of its
operands (which must be integer of boolean values). E.g. ``6 & 3`` returns ``2``.

As with the unary operator ``~``, negative numbers are interpreted as having an
unlimited number of leading ``1`` bits.


Binary bitwise exclusive or operator
""""""""""""""""""""""""""""""""""""

The bitwise exclusive or operator ``^`` returns the bitwise exclusive "or"
combination of its operands (which must be integer of boolean values).
E.g. ``6 ^ 3`` returns ``5``.

Negative numbers are again interpreted as having an unlimited number of leading
``1`` bits.


Binary bitwise inclusive or operator
""""""""""""""""""""""""""""""""""""

The bitwise inclusive or operator ``|`` returns the bitwise inclusive "or"
combination of its operands (which must be integer of boolean values).
E.g. ``6 | 3`` returns ``7``.

Negative numbers are again interpreted as having an unlimited number of leading
``1`` bits.


Binary comparison operators
"""""""""""""""""""""""""""

The comparison operators ``==``, ``!=``, ``<``, ``<=``, ``>`` and ``>=`` compare
the value of the two operands. ``==`` and ``!=`` support comparison of all
types of object. All others support comparison of "compatible" objects, which
means all "number" objects (integer, float and boolean) can be compared with
each other, all other objects can only be compared to objects of the same type.


Identify comparison operators
"""""""""""""""""""""""""""""

The comparison operators ``is`` and ``is not`` test whether both operands refer
to the same object or not.

Note that the behaviour of these operators for "atomic" immutable objects
(like integers, floats and strings) is implementation defined.


Containment tests
"""""""""""""""""

The ``in`` operator
+++++++++++++++++++

The ``in`` operator tests whether the first operand is contained in the second
operand. In the expression ``a in b`` the following type combinations are
supported:

*	string, string: Checks whether ``a`` is a substring of ``b``.
*	any object, list: Checks whether the object ``a`` is in the list ``b``
	(comparison is done by value not by identity)
*	string, dict: Checks whether the key ``a`` is in the dictionary ``b``.
	(Note that some implementations might support keys other than strings too.
	E.g. Python and Java do, Javascript doesn't.)

The ``not in`` operator
+++++++++++++++++++++++

The ``not in`` operator returns the inverted result of the ``in`` operator, i.e.
it tests whether the first operand is not contained in the second operand.


Boolean negation
""""""""""""""""

The unary operator ``not`` inverts the truth value of its operand. I.e.
``not x`` is ``True`` for ``None``, ``False``, the undefined value, ``0``,
``0.0``, empty lists, strings, dictionaries and other empty container and
``False`` for everything else.


Boolean "and" operator
""""""""""""""""""""""

The binary operator ``and`` returns whether both of its operands are true.
It work like in Python by short-circuiting operand evaluation, i.e. if the
result is clear from the first operand the seconds won't be evaluated.

Furthermore ``and``  always return one of the operands.

So ``a and b`` first evaluates ``a``; if ``a`` is false, its value is returned;
otherwise, ``b`` is evaluated and the resulting value is returned.


Boolean "or" operator
"""""""""""""""""""""

The binary operator ``or`` returns whether any of its operands is true. Like
``and`` evaluation is short-circuited and one of the operands is returned.

For example, the following code will output the ``data.title`` object if it's
true, else ``data.id`` will be output::

	<?printx data.title or data.id?>


Conditional expressions
"""""""""""""""""""""""

The conditional expression (also called an "inline if") ``a if c else b`` first
evaluates the condition ``c``. If it is true ``a`` is evaluated and returned
else ``b`` is evaluated and returned.


Functions
---------

:mod:`ll.ul4c` supports a number of functions.


``now``
"""""""

``now()`` returns the current date and time as a date object.


``utcnow``
""""""""""

``utcnow()`` returns the current date and time as a date object in UTC.


``date``
""""""""

``date()`` creates a date object from the parameter passed in. ``date()``
supports from three parameters (``year``, ``month``, ``day``) upto seven
parameters (``year``, ``month``, ``day``, ``hour``, ``minute``, ``second``,
``microsecond``).


``timedelta``
"""""""""""""

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


``monthdelta``
""""""""""""""

``monthdelta`` returns an object that represents a timespan of a number of
months. ``monthdelta`` allows zero or one arguments. With zero arguments
``monthdelta`` returns the timespan for "0 months". In a boolean context this
object is treated as false (i.e. ``bool(monthdelta()))`` or
``bool(monthdelta(0)))`` return ``False``). The following arithmetic operations
are supported:

*	``date`` + ``monthdelta``
*	``date`` - ``monthdelta``
*	``monthdelta`` + ``monthdelta``
*	``monthdelta`` - ``monthdelta``
*	``int`` * ``monthdelta``
*	``monthdelta`` // ``int``

For operations involving ``date`` objects, if the resulting day falls out of the
range of valid days for the target month, the last day for the target month
will be used instead, i.e. ``<?print @(2000-01-31) + monthdelta(1)?>`` prints
``2000-02-29 00:00:00``.


``isundefined``
"""""""""""""""

``isundefined(foo)`` returns ``True`` if ``foo`` is ``Undefined``, else
``False`` is returned::

	data is <?if isundefined(data)?>undefined<?else?>defined<?end if?>!


``isdefined``
"""""""""""""

``isdefined(foo)`` returns ``False`` if ``foo`` is ``Undefined``, else
``True`` is returned::

	data is <?if isdefined(data)?>defined<?else?>undefined<?end if?>!


``isnone``
""""""""""

``isnone(foo)`` returns ``True`` if ``foo`` is ``None``, else ``False`` is
returned::

	data is <?if isnone(data)?>None<?else?>something else<?end if?>!


``isbool``
""""""""""

``isbool(foo)`` returns ``True`` if ``foo`` is ``True`` or ``False``, else
``False`` is returned.


``isint``
"""""""""

``isint(foo)`` returns ``True`` if ``foo`` is an integer object, else ``False``
is returned.


``isfloat``
"""""""""""

``isfloat(foo)`` returns ``True`` if ``foo`` is a float object, else ``False``
is returned.


``isstr``
"""""""""

``isstr(foo)`` returns ``True`` if ``foo`` is a string object, else ``False``
is returned.


``isdate``
""""""""""

``isdate(foo)`` returns ``True`` if ``foo`` is a date object, else ``False``
is returned.


``istimedelta``
"""""""""""""""

``istimedelta(foo)`` returns ``True`` if ``foo`` is a timedelta object, else
``False`` is returned.


``ismonthdelta``
""""""""""""""""

``ismonthdelta(foo)`` returns ``True`` if ``foo`` is a monthdelta object, else
``False`` is returned.


``islist``
""""""""""

``islist(foo)`` returns ``True`` if ``foo`` is a list object, else ``False``
is returned.


``isdict``
""""""""""

``isdict(foo)`` returns ``True`` if ``foo`` is a dictionary object, else
``False`` is returned.


``isset``
"""""""""

``isset(foo)`` returns ``True`` if ``foo`` is a set object, else
``False`` is returned.


``isexception``
"""""""""""""""

``isexception(foo)`` returns ``True`` if ``foo`` is an exception object, else
``False`` is returned.


``iscolor``
"""""""""""

``iscolor(foo)`` returns ``True`` if ``foo`` is a color object, else ``False``
is returned.


``istemplate``
""""""""""""""

``istemplate(foo)`` returns ``True`` if ``foo`` is a template object, else
``False`` is returned.


``bool``
""""""""

``bool(foo)`` converts ``foo`` to an boolean. I.e. ``True`` or ``False`` is
returned according to the truth value of ``foo``. Calling ``bool`` without
arguments returns ``False``.


``int``
"""""""

``int(foo)`` converts ``foo`` to an integer. ``foo`` can be a string, a float,
a boolean or an integer. ``int`` can also be called with two arguments. In this
case the first argument must be a string and the second is the number base for
the conversion. Calling ``int`` without arguments returns ``0``.


``float``
"""""""""

``float(foo)`` converts ``foo`` to a float. ``foo`` can be a string, a float,
a boolean or an integer. Calling ``float`` without arguments returns ``0.0``.


``str``
"""""""

``str(foo)`` converts ``foo`` to a string. If ``foo`` is ``None`` or ``Undefined``
the result will be the empty string. For lists and dictionaries the exact format
is undefined, but should follow Python's repr format. For color objects the
result is a CSS expression (e.g. ``"#fff"``). Calling ``str`` without arguments
returns the empty string.


``repr``
""""""""

``repr(foo)`` converts ``foo`` to a string representation that is useful for
debugging proposes. The output in most cases looks that the UL4 constant that
could be used to recreate the object.


``ascii``
"""""""""

``ascii(foo)`` produces the same output as ``repr(foo)`` except that all
non-ASCII characters in the output for strings will be escaped.


``format``
""""""""""

``format`` formats a value. Its signature is ``format(value, spec, lang="en")``.
Currently ``format`` supports the following types for ``value``: ``date``,
``int`` and ``float`` (``float`` is only supported in the Python version).

The second argument ``spec`` is a format specification string (whose format is
specific to the type of ``value``).

The third (optional) argument ``lang`` is the target language.

So for example ``format(@(2000-02-29), "%a, %d. %b. %Y", "de")`` outputs
``Di, 29. Feb. 2000`` and ``format(42, "08b")`` outputs ``00101010``.

UL4 tries to follow Pythons convention for the format string specification,
so for more information see the documentation for Pythons :func:`format`
function.




``list``
""""""""

``list(foo)`` converts ``foo`` to a list. This works for lists, strings and all
iterable objects. Calling ``list`` without arguments returns an empty list.


``set``
"""""""

``set(foo)`` converts ``foo`` to a set. This works for lists, strings and all
iterable objects. Calling ``set`` without arguments returns an empty set.


``slice``
"""""""""
``slice`` returns a slice from a sequence or iterator. You can either pass the
stop index (i.e. ``slice(foo, 10)`` is an iterator over the first 10 items from
``foo``), or a start and stop index (``slice(foo, 10, 20)`` return the 11th upto
to 20th item from ``foo``) or a start and stop index and a step size. If given
start and stop must be non-negative and step must be positive.


``asjson``
""""""""""

``asjson(foo)`` returns a JSON representation of the object ``foo``.
(Date objects, color objects and templates are not supported by JSON, but
``asjson`` will output the appropriate Javascript code for those objects).


``fromjson``
""""""""""""

``fromjson(foo)`` decodes the JSON string ``foo`` and returns the resulting
object. (Date objects, color objects and templates are not supported by
``fromjson``).


``asul4on``
"""""""""""

``asul4on(foo)`` returns the UL4ON representation of the object ``foo``.


``fromul4on``
"""""""""""""

``fromul4on(foo)`` decodes the UL4ON string ``foo`` and returns the resulting
object.


``csv``
"""""""

``csv(foo)`` formats the value ``foo`` for output into a CSV file.


``len``
"""""""

``len(foo)`` returns the length of a string, or the number of items in a list
or dictionary.


``any``
"""""""

``any(foo)`` returns ``True`` if any of the items in the iterable ``foo`` is
true. Otherwise ``False`` is returns. If ``foo`` is empty ``False`` is returned.


``all``
"""""""

``all(foo)`` returns ``True`` if all of the items in the iterable ``foo`` are
true. Otherwise ``False`` is returns. If ``foo`` is empty ``True`` is returned.


``enumerate``
"""""""""""""

Enumerates the items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and for each item in the original iterable returns a two
item list containing the item position and the item itself. For example the
following code::

	<?for (i, c) in enumerate("foo")?>
		(<?print c?>=<?print i?>)
	<?end for?>

prints::

	(f=0)(o=1)(o=2)


``isfirstlast``
"""""""""""""""

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the first
and/or last in the iterable. For example the following code::

	<?for (first, last, c) in isfirstlast("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>)
		<?if last?>]<?end if?>
	<?end for?>

prints::

	[(f)(o)(o)]


``isfirst``
"""""""""""

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the first
in the iterable. For example the following code::

	<?for (first, c) in isfirst("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>)
	<?end for?>

prints::

	[(f)(o)(o)


``islast``
""""""""""

Iterates through items of the argument (which must be iterable, i.e. a string,
a list or dictionary) and gives information about whether the item is the last
in the iterable. For example the following code::

	<?for (last, c) in islast("foo")?>
		(<?print c?>)
		<?if last?>]<?end if?>
	<?end for?>

prints::

	(f)(o)(o)]


``enumfl``
""""""""""

This function is a combination of ``enumerate`` and ``isfirstlast``. It iterates
through items of the argument (which must be iterable, i.e. a string, a list
or dictionary) and gives information about whether the item is the first
and/or last in the iterable and its position. For example the following code::

	<?for (index, first, last, c) in enumfl("foo")?>
		<?if first?>[<?end if?>
		(<?print c?>=<?print index?>)
		<?if last?>]<?end if?>
	<?end for?>

prints::

	[(f=0)(o=1)(o=2)]


``first``
"""""""""

``first`` returns the first element produced by an iterable object. If the
iterable is empty the default value (which is the second parameter and defaults
to ``None``) is returned.


``last``
""""""""

``last`` returns the last element produced by an iterable object. If the
iterable is empty the default value (which is the second parameter and defaults
to ``None``) is returned.


``xmlescape``
"""""""""""""

``xmlescape`` takes a string as an argument. It returns a new string where the
characters ``&``, ``<``, ``>``, ``'`` and ``"`` have been replaced with the
appropriate XML entity or character reference. For example::

	<?print xmlescape("<'foo' & 'bar'>")?>

prints::

	&lt;&#39;foo&#39; &amp; ;&#39;bar&#39&gt;

If the argument is not a string, it will be converted to a string first.

``<?printx foo?>`` is a shortcut for ``<?print xmlescape(foo)?>``.


``min``
"""""""

``min`` returns the minimum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``min`` returns the
minimum value of this argument.


``max``
"""""""

``max`` returns the maximum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``max`` returns the
maximum value of this argument.


``sum``
"""""""

``sum`` returns the sum of the number from the iterable passed in. The second
parameter is the start value (i.e. the value that will be added to the total sum)
and defaults to 0. For example the template ``<?print sum(range(101))?>`` will
output ``5050``.


``sorted``
""""""""""

``sorted`` returns a sorted list with the items from its argument. For example::

	<?for c in sorted('abracadabra')?><?print c?><?end for?>

prints::

	aaaaabbcdrr

Supported arguments are iterable objects, i.e. strings, lists, dictionaries
and colors.


``chr``
"""""""

``chr(x)`` returns a one-character string containing the character with the
code point ``x``. ``x`` must be an integer. For example ``<?print chr(0x61)?>``
outputs ``a``.


``ord``
"""""""

This is the inverse function to ``chr`` The argument for ``ord`` must be a
one-character string. ``ord`` returns the code point of that character as an
integer. For example ``<?print ord('a')?>`` outputs ``97``.


``hex``
"""""""

Return the hexadecimal representation of the integer argument (with a leading
``0x``). For example ``<?print hex(42)?>`` outputs ``0x2a``.


``oct``
"""""""

Return the octal representation of the integer argument (with a leading ``0o``).
For example ``<?print oct(42)?>`` outputs ``0o52``.


``bin``
"""""""

Return the binary representation of the integer argument (with a leading ``0b``).
For example ``<?print bin(42)?>`` outputs ``0b101010``.


``range``
""""""""""

``range`` returns an object that can be iterated and will produce consecutive
integers up to the specified argument. With two arguments the first is the start
value and the second is the stop value. With three arguments the third one is
the step size (which can be negative). For example the following template::

	<?for i in range(4, 10, 2)?>(<?print i?>)<?end for?>

outputs::

	(4)(6)(8)


``type``
""""""""

``type`` returns the type of the object as a string. Possible return values are
``"undefined"``, ``"none"``, ``"bool"``, ``"int"``, ``"float"``, ``"str"``,
``"list"``, ``"dict"``, ``"date"``, ``"timedelta"``, ``"monthdelta"``,
``"color"``, ``"template"`` and ``"function"``. (If the type isn't recognized
``None`` is returned.)


``rgb``
"""""""

``rgb`` returns a color object. It can be called with

*	three arguments, the red, green and blue values. The alpha value will be
	set to 255;
*	four arguments, the red, green, blue and alpha values.

Arguments are treated as values from 0 to 1 and will be clipped accordingly. For
example::

	<?print rgb(1, 1, 1)?>

prints ``#fff``.


``md5``
"""""""

``md5(str)`` returns the MD5 hash of the string ``str``.


``random``
""""""""""

``random()`` returns a random float value between 0 (included) and 1 (excluded).


``randrange``
"""""""""""""

``randrange(start, stop, step)`` returns a random integer value between ``start``
(included) and ``stop`` (excluded). ``step`` specifies the step size (i.e.
when ``r`` is the random value, ``(r-start) % step`` will always be ``0``).
``step`` and ``start`` can be omitted.


``randchoice``
""""""""""""""

``randchoice(seq)`` returns a random item from the sequence ``seq``.


``urlquote``
""""""""""""

``urlquote`` escaped special characters for including the output in URLs. For
example::

	<?print urlquote("/\xff")?>

outputs::

	%2F%C3%BF

``urlunquote``
""""""""""""""

``urlunquote`` is the inverse function to ``urlquote``. So::

	<?print urlunquote("%2F%C3%BC")?>

outputs::

	/ü


Methods
-------

Objects in :mod:`ll.ul4c` support some methods too (depending on the type of the
object).


``upper``
"""""""""

The ``upper`` method of strings returns an uppercase version of the string for
which it's called::

	<?print 'foo'.upper()?>

prints::

	FOO


``lower``
"""""""""

The ``lower`` method of strings returns an lowercase version of the string for
which it's called.


``capitalize``
""""""""""""""

The ``capitalize`` method of strings returns a copy of the string with its first
letter capitalized.


``startswith``
""""""""""""""

``x.startswith(y)`` returns ``True`` if the string ``x`` starts with the string
``y`` and ``False`` otherwise. ``y`` may also be a list of string. In this case
``x.startswith(y)`` returns ``True`` if ``x`` starts with any of the strings in
``y``.


``endswith``
""""""""""""""

``x.endswith(y)`` returns ``True`` if the string ``x`` ends with the string
``y`` and ``False`` otherwise. ``y`` may also be a list of string. In this case
``x.endswith(y)`` returns ``True`` if ``x`` ends with any of the strings in
``y``.


``strip``
"""""""""

The string method ``strip`` returns a copy of the string with leading and
trailing whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``lstrip``
""""""""""

The string method ``lstrip`` returns a copy of the string with leading
whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``rstrip``
""""""""""

The string method ``rstrip`` returns a copy of the string with trailing
whitespace removed. If an argument ``chars`` is given and not ``None``,
characters in ``chars`` will be removed instead.


``split``
"""""""""
The string method ``split`` splits the string into separate "words" and returns
the resulting list. Without any arguments, the string is split on whitespace
characters. With one argument the argument specifies the separator to use. The
second optional argument specifies the maximum number of splits to do.


``rsplit``
""""""""""
The string method ``rsplit`` works like ``split``, except that splitting starts
from the end (which is only relevant when the maximum number of splits is
given).


``splitlines``
""""""""""""""
The string method ``splitlines`` splits the string into a list of lines,
using Unicode line ending characters, i.e. the following character sequences
terminate a line:  ``"\n"``, ``"\r"``, ``"\r\n"``, ``"\x0b"``, ``"\x0c"``,
``"\x1c"``, ``"\x1d"``, ``"\x1e"``, ``"\x85"``, ``"\u2028"`` and ``"\u2029"``.
Line breaks are not included in the resulting list unless a second parameter is
given and true.


``count``
"""""""""

This method counts non-overlapping occurrences of a substring in a string or
occurrences of an item in a list. For example ``"abababa".count("aba")``
returns 2. The optional second and third argument specify the start and end
position for the search.


``find``
""""""""

This method searches for a substring of the string or an item in a list
and returns the position of the first appearance of the substring/item or -1 if
the string/item can't be found. For example ``"foobar".find("bar")`` returns 3.
The optional second and third argument specify the start and end position for
the search.


``rfind``
"""""""""

This method works like ``find`` but searches from the end.


``replace``
"""""""""""

The string method ``replace`` has two arguments. It returns a new string where
each occurrence of the first argument is replaced by the second argument, i.e.
``"abracadabra".replace("ab", "ba")`` returns ``"baracadbara"``


``get``
"""""""

``get`` is a dictionary method. ``d.get(k, v)`` returns ``d[k]`` if the key
``k`` is in ``d``, else ``v`` is returned. If ``v`` is not given, it defaults
to ``None``.


``join``
""""""""

``join`` is a string method. It returns a concatentation of the strings in the
argument sequence with the string itself as the separator, i.e.::

	<?print "+".join("1234")?>

outputs::

	1+2+3+4


``renders``
"""""""""""

The ``renders`` method of template objects renders the template and returns the
output as a string. The parameters can be passed via keyword arguments or via the
``**`` syntax::

	<?code output = template.renders(a=17, b=23)?>
	<?code data = {'a': 17, 'b': 23)?>
	<?code output = template.renders(**data)?>

(Also if the template has a signature, positional arguments and the ``*`` syntax
are supported.)


``isoformat``
"""""""""""""

``isoformat`` is a date method. It returns the date object in ISO 8601 format,
i.e.::

	<?print now().isoformat()?>

might output::

	2010-02-22T18:30:29.569639


``mimeformat``
""""""""""""""

``mimeformat`` is a date method. It returns the date object in MIME format
(assuming the date object is in UTC), i.e.::

	<?print utcnow().mimeformat()?>

might output::

	Mon, 22 Feb 2010 17:38:40 GMT


``day``, ``month``, ``year``, ``hour``, ``minute``, ``second``, ``microsecond``, ``weekday``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Those methods are date methods. They return a specific attribute of a date
object. For example the following reproduces the ``mimeformat`` output from
above (except for the linefeeds of course)::

	<?code weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']?>
	<?code months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']?>
	<?code t = @(2010-02-22T17:38:40.123456)?>
	<?print weekdays[t.weekday()]?>,
	<?print format(t.day(), '02')?>
	<?print months[t.month()-1]?>
	<?print format(t.year(), '04')?>
	<?print format(t.hour(), '02')?>:
	<?print format(t.minute(), '02')?>:
	<?print format(t.second(), '02')?>.
	<?print format(t.microsecond(), '06')?> GMT


``yearweek``
""""""""""""

``yearweek`` is a date method. The signature is
``yearweek(day, firstweekday=0, mindaysinfirstweek=4)``. It returns the calendar
week number of the date ``day`` and the calendar year it belongs to. (A day
might belong to a different calender year, if it is in week 1 but before
January 1, or if belongs to week 1 of the following year).

``firstweekday`` defines what a week is (i.e. which weekday is considered
the start of the week, ``0`` is Monday and ``6`` is Sunday).
``mindaysinfirstweek`` defines how many days must be in a week to be
considered the first week in the year.

For example for the ISO week number (according to
https://en.wikipedia.org/wiki/ISO_week_date) the week starts on Monday
(i.e. ``firstweekday == 0``) and a week is considered the first week if
it's the first week that contains a Thursday (which means that this week
contains at least four days in January, so ``mindaysinfirstweek == 4``).

For the US ``firstweekday == 6`` and ``mindaysinfirstweek == 1``, i.e.
the week starts on Sunday and January the first is always in week 1.

There's also the convention that the week 1 is the first complete week
in January. For this ``mindaysinfirstweek == 7``.

``week``
""""""""

``week`` is a date method. The signature is
``week(day, firstweekday=0, mindaysinfirstweek=4)``. It returns the calendar
week number of the date ``day``. For more information see the method ``yearweek``.


``yearday``
"""""""""""

``yearday`` is a date method. It returns the number of days since the beginning
of the year, so::

	<?print @(2010-01-01).yearday()?>

prints ``1`` and::

	<?print @(2010-12-31).yearday()?>

prints ``365``.


``append``
""""""""""

``append`` is a list method. It adds its arguments to the end of the list for
which it is called::

	<?code v = [1, 2]?>
	<?code v.append(3, 4)?>
	<?print v?>

prints ``[1, 2, 3, 4]``.


``insert``
""""""""""

``insert`` is a list method. Its first argument in the insert position, the
remaining arguments are the items that will be inserted at that position, so::

	<?code v = [1, 4]?>
	<?code v.insert(1, 2, 3)?>
	<?print v?>

prints ``[1, 2, 3, 4]``.


``pop``
"""""""

``pop`` is a list method. It removes the last item of the list and returns it.
If an index is passed the item at that position is removed and returned.
A negative index is treated as relative to the end of the list.


``update``
""""""""""

``update`` is a dictionary method. It supports an arbitrary number of positional
and keyword arguments. Each positional argument may be a dictionary, all the
items in the dictionary will be copied to the target dictionary. A positional
argument may also be an iterable of ``(key, value)`` pairs. These will also be
copied to the target dictionary. After each positional argument is copied over
in a last step the keyword arguments will be copied to the target dictionary.


``clear``
"""""""""

``clear`` is a dictionary and set method. It makes the dictionary/set empty.


Templates as functions
======================

UL4 templates can be used as functions too. Calling a template as a function
will ignore any output from the template. The return value will be the value of
the first ``<?return?>`` tag encountered::

	from ll import ul4c

	code = """
		<?for item in data?>
			<?if "i" in item?>
				<?return item?>
			<?end if?>
		<?end for?>
	"""

	function = ul4c.Template(code)

	output = function(data=["Python", "Java", "Javascript", "PHP"]))

With this, ``output`` will be the string ``"Javascript"``.

When no ``<?return?>`` tag is encountered, ``None`` will be returned.

When a ``<?return?>`` tag is encountered when the template is used as a
template, output will simply stop and the return value will be ignored.


Exposing attributes
===================

It is possible to expose attributes of an object to UL4 templates. This is done
by setting the class attribute ``ul4attrs``::

	from ll import ul4c

	class Person:
		ul4attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``Doe, John``.

Attributes not in ``ul4attrs`` will not be visible::

	template = ul4c.Template("<?print type(p.age)?>")
	print(template.renders(p=p))

This will output ``undefined``. Exposing attributes via ``ul4attrs`` also makes
it possible to use dictionary access to the object, i.e. iterating over the
object, using ``in`` and ``not in`` tests and using the methods ``items`` and
``values``.


Exposing methods
================

It is also possible to expose methods of an object to UL4 templates. This is
done by including the method name in the ``ul4attrs`` class attribute::

	from ll import ul4c

	class Person:
		ul4attrs = {"fullname"}

		def __init__(self, firstname, lastname):
			self.firstname = firstname
			self.lastname = lastname

		def fullname(self):
			return self.firstname + " " + self.lastname

	p = Person("John", "Doe")

	template = ul4c.Template("<?print p.fullname()?>")
	print(template.renders(p=p))

This will output ``John Doe``.

Furthermore it's possible to specify that the method needs access to the
rendering context (which stores the local variables and the UL4 call stack)::

	class Person:
		ul4attrs = {"fullname", "varcount"}

		@ul4c.withcontext
		def varcount(self):
			return len(context.vars)


Custom attributes
=================

To customize getting and setting object attributes from UL4 templates the
methods :meth:`ul4getattr` and :meth:`ul4setattr` can be implemented::

	from ll import ul4c

	class Person:
		ul4attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

		def ul4getattr(self, name):
			return getattr(self, name).upper()

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``DOE, JOHN``.

If the object has an attribute ``ul4attrs`` :meth:`ul4getattr` will only be
called for the attributes in ``ul4attrs``, otherwise :meth:`ul4getattr` will
be called for all attributes (and should raise an :exc:`AttributeError` for
non-existant attributes)

Attributes can be made writable by implemention the method :meth:`ul4setattr`::

	from ll import ul4c

	class Person:
		ul4attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

		def ul4setattr(self, name, value):
			return setattr(self, name, value.upper())

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?code p.lastname = 'Doe'?><?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``DOE, John``.

If the object has an attribute ``ul4attrs`` :meth:`ul4setattr` will only be
called for the attributes in ``ul4attrs``, otherwise :meth:`ul4setattr` will
be called for all attributes (and should raise an :exc:`AttributeError` for
non-existant or readonly attributes)

Without a :meth:`ul4setattr` method, attributes will never be made writable.


Exceptions
==========

Exception objects can not be created directly by UL4 templates, but UL4
templates can work with exceptions and access their attributes. The function
``isexception`` returns ``True`` if the argument is an exception object and
exception objects have an attribute ``context`` that exposed the ``__cause__``
or ``__context__`` attribute of the Python exception object.

Exceptions that happen in UL4 templates use exception chaining to add
information about the location of the error while the exception bubbles up the
Python call stack. So the exception will be e.g. a :class:`TypeError` object
and its ``__cause__`` attribute (which is accessible as the UL4 attribute
``context``) specifies the immediate location inside the UL4 source code where
the exception happened (and its ``__cause__`` is the location that called that
one etc.). So if we have the following UL4 template::

	<?def x(i)?>
		Print: <?print 1/i?>
		Render: <?render x(i-1)?>
	<?end def?>
	Initial render: <?render x(3)?>

Calling the template will result in a :class:`ZeroDivisionError` exception. We
can format a nice UL4 stacktrace (in HTML) for this exception with the
following UL4 code::

	<?def frame(exc)?>
		<?if exc.context?>
			<?render frame(exc.context)?>
		<?end if?>
		<?if exc.location?>
			<li>
				<p>
					<b><?printx type(exc)?></b>
					in template <b><?printx exc.location.template.name?></b>
					: line <?printx exc.location.line?>
					; col <?printx exc.location.col?>
				</p>
				<p>
					<?print exc.location.sourceprefix?>
					<b><?print exc.location.source?></b>
					<?print exc.location.sourcesuffix?>
				</p>
			</li>
		<?else?>
			<li>
				<p>
					<b><?printx type(exc)?></b><?if str(exc)?>: <?print str(exc)?>
				</p>
			</li>
		<?end def?>
	<?end def?>

	<ul>
		<?render frame(exc)?>
	</ul>


Delimiters
==========

It is possible to specify alternative delimiters for the template tags::

	>>> from ll import ul4c
	>>> t = ul4c.Template(
	... 	"{{for i in range(10)}}{{print i}};{{end for}}",
	... 	startdelim="{{",
	... 	enddelim="}}"
	... )
	>>> t.renders()
	'0;1;2;3;4;5;6;7;8;9;'


Whitespace
==========

Normally the literal text between template tags will be output as it is. This
behaviour can be changed by passing a different value to the ``whitespace``
parameter in the constructor. The possible values are:

``"keep"``
	The default behaviour: literal text will be output as it is.

``"strip"``
	Linefeeds and the following indentation in literal text will be ignored::

		>>> from ll import ul4c
		>>> t = ul4c.Template("""
		... 	<?for i in range(10)?>
		... 		<?print i?>
		... 		;
		... 	<?end for?>
		... """, whitespace="strip")
		>>> t.renders()
		'0;1;2;3;4;5;6;7;8;9;'

	However trailing whitespace at the end of the line will still be honored.

``"smart"``
	If a line contains only indentation and one tag that isn't a ``print``,
	``printx`` or ``render`` tag, the indentation and the linefeed after the tag
	will be stripped from the text. Furthermore the additional indentation that
	might be introduced by a ``for``, ``if``, ``elif``, ``else`` or ``def``
	block will be ignored. So for example the output of::

		<?code langs = ["Python", "Java", "Javascript"]?>
		<?if langs?>
			<?for lang in langs?>
				<?print lang?>
			<?end for?>
		<?end if?>

	will simply be::

		Python
		Java
		Javascript

	without any additional empty lines or indentation.

	Rendering a template ``B`` inside an template ``A`` will reindent the output
	of ``B`` to the indentation level of the ``<?render?>`` tag in the template
	``A``.

It is also possible to specify the whitespace behaviour in the template itself
with the ``<?whitespace?>`` tag, so::

	<?whitespace smart?>

anywhere in the template source will switch on smart whitespace handling.

A ``<?whitespace?>`` tag overwrites the ``whitespace`` parameter specified
in the constructor.

API
===

.. automodule:: ll.ul4c
