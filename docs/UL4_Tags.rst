Tags
####

The template code tries to mimic Python syntax as far as possible, but is
limited to what is required for templates and does not allow executing arbitrary
Python statements. In some spots it also borrows Javascript semantics.

:mod:`ll.ul4c` supports the following tag types:


``<?print?>``
=============

The ``print`` tag outputs the value of a variable or any other expression. If
the expression doesn't evaluate to a string it will be converted to a string
first. The format of the string depends on the renderer, but should follow
Python's ``str()`` output as much as possible::

	<h1><?print person.lastname?>, <?print person.firstname?></h1>

Printing ``None`` or undefined objects produces no output.

.. hint::
	The ``<?print?>`` tag is implemented by :class:`ll.ul4c.PrintAST`.


``<?printx?>``
==============

The ``printx`` tag outputs the value of a variable or any other expression and
escapes the characters ``<``, ``>``, ``&``, ``'`` and ``"`` with the appropriate
character or entity references for XML or HTML output.

.. hint::
	The ``<?printx?>`` tag is implemented by :class:`ll.ul4c.PrintXAST`.


``<?for?>``
===========

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

.. hint::
	The ``<?for?>`` tag is implemented by :class:`ll.ul4c.ForBlockAST`.


``<?break?>``
=============

The ``break`` tag can be used to break out of the innermost running loop.

.. hint::
	The ``<?break?>`` tag is implemented by :class:`ll.ul4c.BreakAST`.


``<?continue?>``
================

The ``continue`` tag can be used to skip the rest of the loop body of the
innermost running loop and continue with the next iteration of the loop.

.. hint::
	The ``<?continue?>`` tag is implemented by :class:`ll.ul4c.ContinueAST`.


``<?if?>``
==========

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

.. hint::
	The ``<?if?>``, ``<?elif?>`` and ``<?else?>`` tags are implemented by
	:class:`ll.ul4c.ConditionalBlocksAST`, :class:`ll.ul4c.IfBlockAST`,
	:class:`ll.ul4c.ElIfBlockAST` and :class:`ll.ul4c.ElseBlockAST`.


``<?code?>``
============

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
*	``%=`` (Does a modulo operation and replaces the variable value with the
	result)
*	``<<=`` (Does bitwise "shift left" operation and replaces the variable value
	with the result)
*	``>>=`` (Does bitwise "shift right" operation and replaces the variable value
	with the result)
*	``&=`` (Does bitwise "and" operation and replaces the variable value with
	the result)
*	``|=`` (Does bitwise "or" operation and replaces the variable value with
	the result)
*	``^=`` (Does bitwise "exclusive-or" operation and replaces the variable
	value with the result)

For example the following template will output ``40``::

	<?code x = 17?>
	<?code x += 23?>
	<?print x?>

.. hint::
	The content of ``<?code?>`` tags is implemented as
	:ref:`UL4 expressions <UL4_expressions>`.


``<?render?>``
==============

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

.. hint::
	The ``<?render?>`` tag is implemented by :class:`ll.ul4c.RenderAST`.


``<?renderx?>``
===============

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

.. hint::
	The ``<?renderx?>`` tag is implemented by :class:`ll.ul4c.RenderXAST`.


``<?def?>``
===========

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

.. hint::
	The ``<?def?>`` tag simply creates a :class:`~ll.ul4c.Template` object inside
	another :class:`~ll.ul4c.Template` object.


``<?renderblocks?>``
====================

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

.. hint::
	The ``<?renderblocks?>`` tag is implemented by
	:class:`ll.ul4c.RenderBlocksAST`.


``<?renderblock?>``
===================

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

.. hint::
	The ``<?renderblock?>`` tag is implemented by :class:`ll.ul4c.RenderBlockAST`.


``<?return?>``
==============

The ``return`` tag returns a value from the template when the template is
called as a function. For more info see :ref:`UL4_TemplatesAsFunctions`.

.. hint::
	The ``<?return?>`` tag is implemented by :class:`ll.ul4c.ReturnAST`.


``<?ul4?>``
===========

The ``ul4`` tag can be used to specify a name and a signature for the template
itself. This overwrites the name and signature specified in the
:class:`ul4c.Template` constructor::

	>>> from ll import ul4c
	>>> t = ul4c.Template("<?ul4 foo(x)?><?print x?>")
	>>> t.name
	'foo'
	>>> t.signature
	<Signature (x)>

.. hint::
	The ``<?ul4?>`` tag has no corresponding AST nodes. Its content will set
	attributes of the template instead.


``<?note?>``
============

A ``note`` tag is a comment, i.e. the content of the tag will be completely
ignored.

.. hint::
	A ``<?note?>`` tag has no corresponding AST nodes.


``<?doc?>``
===========

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

.. hint::
	A ``<?doc?>`` tag has no corresponding AST nodes. Its content will set the
	``doc`` property of the template instead.


``<?whitespace?>``
==================

The ``whitespace`` tag can be used to overwrite the handling of whitespace in
the template. For more info see :ref:`UL4_Whitespace`.

.. hint::
	A ``<?whitespace?>`` tag has no corresponding AST nodes. Its content will
	set the ``whitespace`` attribute of the template instead.
