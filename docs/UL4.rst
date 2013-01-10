:mod:`ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.ul4c` compiles a template to an internal format, which makes it
possible to implement renderers for these templates in multiple programming
languages.

Apart from this Python implementaion there are implementations for Java_ (both a
compiler and renderer), Javascript_ (renderer only) and PHP_ (renderer only).

.. _Java: http://hg.livinglogic.de/LivingLogic.Java.ul4/
.. _Javascript: http://hg.livinglogic.de/LivingLogic.Javascript.ul4/
.. _PHP: http://hg.livinglogic.de/LivingLogic.PHP.ul4/


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

	code = '''<?if data?>
	<ul>
	<?for item in data?>
	<li><?print xmlescape(item)?></li>
	<?end for?>
	</ul>
	<?end if?>'''

	tmpl = ul4c.Template(code)

	print(tmpl.renders(data=["Python", "Java", "Javascript", "PHP"]))

The variables that should be available to the template code can be passed to the
method :meth:`Template.renders` as keyword arguments. :meth:`renders` returns
the final rendered output as a string. Alternatively the method :meth:`render`
can be used, which is a generator and returns the output piecewise.


Supported data types
====================

The following object types can be passed as variables to be used by the template
code:

*	strings
*	integers
*	floats
*	date objects
*	color objects
*	The "null" value (``None``)
*	boolean values (``True`` and ``False``)
*	the ``Undefined`` variable
*	lists
*	dictionaries
*	templates

This is similar to what JSON_ supports (except for date objects, color objects
and templates).

	.. _JSON: http://www.json.org/

Note that depending on the implementation language of the renderer additional
types might be supported, e.g. a Python renderer will probably support tuples
and lists and anything supporting :meth:`__getitem__` (or :meth:`__iter__` when
the list is used in a loop) for lists, Java might support anything implementing
the ``List`` interface (or the ``Collection`` interface if the list is used in a
loop).

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
sequences that Python supports (except ``\N{}``). Strings constants are always
unicode objects, so ``\uXXXX`` escaping is possible. Examples:

* ``"abc"`` and ``'abc'``;

*	``"'"`` and ``'\''`` are single quotes;

*	``'"'`` and ``"\""`` are double quotes;

*	``"\n"`` is a line feed and ``"\t"`` is a tab;

*	``"\x61"`` and ``"\u0061"`` are lowercase "a"s;


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

It is also possible to create a list with a list comprehension::

	["(" + c.upper() + ")" for c in "hurz" if c < "u"]

This will create the list::

	["(H)", "(R)"]

The ``if`` condition is optional, i.e.::

	["(" + c.upper() + ")" for c in "hurz"]

will create the list::

	["(H)", "(U)", "(R)", "(Z)"]


Dictionaries
------------

Dictionaries can be created like this:

*	``{}``

*	``{1: 2, 3: 4}``

*	``{"foo": 17, "bar": 23}``

Also Python ``**`` syntax for passing keyword arguments is supported for
creating dictionaries::

	{"foo": 17, "bar": 23, **{1: 2, 3: 4}}

With this it's possible to copy the content of one dictionary into another new
one. Keys are set from left to right, so later values overwrite former ones, so
``{1: 2, 1: 3}[1]`` and ``{1: 2, **{1: 3}}[1]`` will both return ``3`` not ``2``.

It is also possible to create a dictionary with a dictionary comprehension::

	{ c.upper() : "(" + c + ")" for c in "hurz" if c < "u"}

This will create the dictionary::

	{ "H": "(h)", "R": "(r)"}

The ``if`` condition is optional, i.e.::

	{ c.upper() : "(" + c + ")" for c in "hurz"}

will create the dictionary::

	{ "H": "(h)", "R": "(r)", "U": "(u)", "Z": "(z)"}


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
Python's ``str()`` output as much as possible (except that for ``None`` no
output may be produced)::

	<h1><?print person.lastname?>, <?print person.firstname?></h1>


``printx``
----------

The ``printx`` tag outputs the value of a variable or any other expression and
escapes the characters ``<``, ``>``, ``&``, ``'`` and ``"`` with the appropriate
character or entity references for XML or HTML output.


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
innermost running loop.


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


``render``
----------

The ``render`` tag allows one template to call other templates. The following Python
code demonstrates this::

	from ll import ul4c

	# Template 1
	source1 = """\
	<?if data?>\
	<ul>
	<?for i in data?><?render itemtmpl.render(item=i)?><?end for?>\
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
``<?render itemtmpl.render(item=i)?>`` renders the ``itemtmpl`` template and
passes the ``i`` variable, which will be available in the inner template under
the name ``item``.


``def``
-------
The ```def`` tag defined a new template as a variable. Usage looks like this::

	<?def quote?>"<?print text?>"<?end def?>

This template can be called like any other template, that has been passed to
the outermost template::

	<?render quote.render(text="foo")?>


``note``
--------

A ``note`` tag is a comment, i.e. the content of the tag will be completely ignored.


The variable ``stack``
----------------------

A UL4 template can use the variable ``stack``, which is a call stack of the
currently executing template. So ``stack[-1]`` for example is the template itself.


Nested scopes
-------------

UL4 templates support lexical scopes. This means that a template that is defined
(via ``<?def?>``) inside another template has access to the local variables of
the outer template. The inner template sees that state of the variables at the
point in time when the ``<?def?>`` tag was executed. The following example will
output ``1``::

	<?code i = 1?>
	<?def x?>
		<?print i?>
	<?end def?>
	<?code i = 2?>
	<?render x.render()?>


Expressions
-----------

:mod:`ll.ul4c` supports many of the operators supported by Python. Getitem style
element access is available, i.e. in the expression ``a[b]`` the following type
combinations are supported:

*	string, integer: Returns the ``b``\th character from the string ``a``.
	Note that negative ``b`` values are supported and are relative to the end,
	so ``a[-1]`` is the last character.

*	list, integer: Returns the ``b``\th list entry of the list ``a``. Negative
	``b`` values are supported too.

*	dict, string: Return the value from the dictionary ``a`` corresponding to
	the key ``b``. Note that some implementations might support keys other
	than strings too. (The Python and Java renderer do for example.)

If the specified key doesn't exist or the index is out of range for the string
or list, the special object ``Undefined`` is returned.

Slices are also supported (for list and string objects). As in Python one or
both of the indexes may be missing to start at the first or end at the last
character/item. Negative indexes are relative to the end. Indexes that are out
of bounds are simply clipped:

*	``<?print "Hello, World!"[7:-1]?>`` prints ``World``.

*	``<?print "Hello, World!"[:-8]?>`` prints ``Hello``.

The following binary operators are supported: ``+``, ``-``, ``*``, ``/`` (true
division), ``//`` (truncating division) and ``&`` (modulo).

The usual boolean operators ``not``, ``and`` and ``or`` are supported. ``and``
and ``or`` work like in Python, i.e. they short-circuit, i.e. if they result is
clear from the first operand the seconds won't be evaluated, Furthermore they
always return one of the operands). For example, the following code will output
the ``data.title`` object if it's true, else ``data.id`` will be output::

	<?print xmlescape(data.title or data.id)?>

The comparison operators ``==``, ``!=``, ``<``, ``<=``, ``>`` and ``>=`` are
supported.

Containment test via the ``in`` operator can be done, in the expression
``a in b`` the following type combinations are supported:

*	string, string: Checks whether ``a`` is a substring of ``b``.
*	any object, list: Checks whether the object ``a`` is in the list ``b``
	(comparison is done by value not by identity)
*	string, dict: Checks whether the key ``a`` is in the dictionary ``b``.
	(Note that some implementations might support keys other than strings too.)

The inverted containment test (via ``not in``) is available too.

Attribute access in the template code maps to dictionary style getitem access
in the data object::

	from ll import ul4c
	tmpl = ul4c.Template("<?print data.foo?>")
	print(tmpl.renders(data=dict(foo="bar")))

However getitem style access in the template is still possible::

	from ll import ul4c
	tmpl = ul4c.Template("<?print data['foo']?>")
	print(tmpl.renders(data=dict(foo="bar")))

UL4 also supports generator expressions::

	<?print ", ".join("(" + c + ")" for c in "gurk")?>

will output::

	(g), (u), (r), (k)

Outside of function/method arguments brackets are required around generator
expressions::

	<?code ge = ("(" + c + ")" for c in "gurk")?>
	<?print ", ".join(ge)?>


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
supports from three parameters (year, month, day) upto seven parameters
(year, month, day, hour, minute, second, microsecond).


``timedelta``
"""""""""""""

``timedelta`` returns an object that represents a timespan. ``timedelta``
allows from zero to three arguments specifying the numbers of days, seconds and
microseconds. Passing negative values or values that are out of bounds (e.g.
24*60*60+1 seconds) is allowed. Arguments default to 0, i.e. ``timedelta()``
returns the timespan for "0 days, 0 seconds, 0 microseconds". In a boolean
context this object is treated as false (i.e. ``bool(timedelta()))`` returns
``False``). The following arithmetic operations are supported::

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
are supported::

*	``date`` + ``monthdelta``
*	``date`` - ``monthdelta``
*	``monthdelta`` + ``monthdelta``
*	``monthdelta`` - ``monthdelta``
*	``int`` * ``monthdelta``
*	``monthdelta`` // ``int``

For the operations involving ``date`` objects, if the resulting day falls out of
the range of valid days for the target month, the last day for the target month
will be used instead, i.e. ``<?print @(2000-01-31) + monthdelta(1)?>`` prints
``2000-02-29 00:00:00``.


``vars``
""""""""

``vars()`` returns a dictionary containing all currently defined variables
(i.e. variables passed to the template, defined via ``<?code?>`` tags or as
loop variables). This does include variables from the encoding scope and the
global variable ``stack``.


``random``
""""""""""

``random()`` returns a random float value between 0 (included) and 1 (excluded).


``randrange``
"""""""""""""

``randrange(start, stop, step)`` returns a random integer value between ``start``
(included) and ``stop`` (excluded). ``step`` specifies the step size (i.e.
when ``r`` is the random value, ``(r-start) % step`` will always be ``0``.
``step`` and ``start`` can be ommitted.


``randchoice``
""""""""""""""

``randchoice(seq)`` returns a random item from the sequence ``seq``.


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


``iscolor``
"""""""""""

``iscolor(foo)`` returns ``True`` if ``foo`` is a color object, else ``False``
is returned.


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
debugging proposes. The output is a constant expression that could be used to
recreate the object.


``asjson``
""""""""""

``asjson(foo)`` returns a JSON representation of the object ``foo``.


``fromjson``
""""""""""""

``fromjson(foo)`` decodes the JSON string ``foo`` and returns the resulting
object.


``asul4on``
"""""""""""

``asul4on(foo)`` returns the UL4ON representation of the object ``foo``.


``fromul4on``
"""""""""""""

``fromul4on(foo)`` decodes the UL4ON string ``foo`` and returns the resulting
object.


``get``
"""""""

``get(k, v)`` returns the global variable named ``k`` if it exists, else ``v``
is returned. If ``v`` is not given, it defaults to ``None``.


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


``enumerate``
"""""""""""""

Enumerates the items of the argument (which must be iterable, i.e. a string,
a list or dictionary). For example the following code::

	<?for (i, c) in enumerate("foo")?>
		(<?print c?>=<?print i?>)
	<?end for?>

prints::

	(f=0)(o=1)(o=2)


``enumfl``
""""""""""

This function is a combination of ``isfirstlast`` and ``enumerate``. It iterates
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


``xmlescape``
"""""""""""""

``xmlescape`` takes a string as an argument. It returns a new string where the
characters ``&``, ``<``, ``>``, ``'`` and ``"`` are replaced with the
appropriate XML entity or character references. For example::

	<?print xmlescape("<'foo' & 'bar'>")?>

prints::

	``&lt;&#39;foo&#39; &amp; ;&#39;bar&#39&gt;``

If the argument is not a string, it will be converted to a string first.

``<?printx foo?>`` is a shortcut for ``<?print xmlescape(foo)?>``.


``min``
"""""""

``min`` returns the minimum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``min`` returns the minimum
value of this argument.


``max``
"""""""

``max`` returns the maximum value of its two or more arguments. If it's called
with one argument, this argument must be iterable and ``max`` returns the maximum
value of this argument.


``sorted``
""""""""""

``sorted`` returns a sorted list with the items from it's argument. For
example::

	<?for c in sorted('bar')?><?print c?><?end for?>

prints::

	abr

Supported arguments are iterable objects, i.e. strings, lists, dictionaries
and colors.


``chr``
"""""""

``chr(x)`` returns a one-character string with a character with the codepoint
``x``. ``x`` must be an integer. For example ``<?print chr(0x61)?>`` outputs
``a``.


``ord``
"""""""

The argument for ``ord`` must be a one-character string. ``ord`` returns the
codepoint of that character as an integer. For example ``<?print ord('a')?>``
outputs ``97``.


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

	<?for i in range(2, 10, 2)?>(<?print i?>)<?end for?>

outputs::

	(2)(4)(6)(8)


``type``
""""""""

``type`` returns the type of the object as a string. Possible return values are
``"none"``, ``"bool"``, ``"int"``, ``"float"``, ``"str"``, ``"list"``,
``"dict"``, ``"date"``, ``"color"`` and ``"template"``. (If the type isn't
recognized ``None`` is returned.)


``rgb``
"""""""

``rgb`` returns a color object. It can be called with

*	three arguments, the red, green and blue values. The alpha value will be
	set to 255;
*	four arguments, the red, green, blue and alpha values.


``random``
""""""""""

``random`` returns a random floating point number between 0 and 1.


``randchoice``
""""""""""""""

``randchoice`` returns a random item from its argument (which must be list or
string)


``randchoice``
""""""""""""""

``random`` returns a random item from its argument (which must be list or string).


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

The ``capitalize`` method of strings returns a copy of the string for with its
first letter capitalized.


``startswith``
""""""""""""""

``x.startswith(y)`` returns ``True`` if the string ``x`` starts with the string
``y`` and ``False`` otherwise.


``endswith``
""""""""""""""

``x.endswith(y)`` returns ``True`` if the string ``x`` ends with the string
``y`` and ``False`` otherwise.


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

This string method replace has two arguments. It returns a new string where
each occurrence of the first argument is replaced by the second argument.


``get``
"""""""

``get`` is a dictionary method. ``d.get(k, v)`` returns ``d[k]`` if the key
``k`` is in ``d``, else ``v`` is returned. If ``v`` is not given, it defaults
to ``None``.


``join``
""""""""

``join`` is a string method. It returns a concatentation of the strings in the
argument sequence with the string itself as the separator, i.e.::

	<?print "+".join(["1", "2", "3", "4"])?>

outputs::

	1+2+3+4


``renders``
"""""""""""

The ``renders`` method of template objects renders the template and returns the
output as a string. The parameter can be passed via keyword argument or via the
``**`` syntax::

	<?code output = template.renders(a=17, b=23)?>
	<?code data = {'a': 17, 'b': 23)?>
	<?code output = template.renders(**data)?>


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


``week``
""""""""

``week`` is a date method. This method returns the week number of the year.
It supports one argument: the weekday number (0 for Monday, ... 6 for Sunday)
that should be considered the start day of the week. All days in a new year
preceding the first week start day are considered to be in week 0. The week
start day defaults to 0 (Monday).


``yearday``
"""""""""""

``yearday`` is a date method. It returns the number of days since the beginning
of the year, so::

	<?print @(2010-01-01).yearday()?>

prints ``1`` and::

	<?print @(2010-12-31).yearday()?>

prints ``365``.
