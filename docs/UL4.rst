UL4 -- A templating language
############################

:mod:`ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.ul4c` compiles a template to an internal format, which makes it
possible to implement renderers for these templates in multiple programming
languages.

.. note::
	Apart from this Python implementation there are implementations for Java_ (both
	a compiler and renderer) and Javascript_ (renderer only).

	.. _Java: https://github.com/LivingLogic/LivingLogic.Java.ul4
	.. _Javascript: https://github.com/LivingLogic/LivingLogic.Javascript.ul4

In the template source any text surrounded by ``<?`` and ``?>`` is a "template
tag". The first word inside the tag is the tag type. It defines what the tag
does. For example ``<?print foo?>`` is a print tag (it prints the value of the
variable ``foo``). A complete example template looks like this:

.. sourcecode:: xml+ul4

	<?if data?>
		<ul>
			<?for item in data?>
				<li><?print xmlescape(item)?></li>
			<?end for?>
		</ul>
	<?end if?>

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

For more information see the following chapters:

.. toctree::
   :maxdepth: 1
   :caption: Content
   :name: ul4_content

   UL4_Literals
   UL4_Tags
   UL4_NestedScopes
   UL4_Expressions
   UL4_Functions
   UL4_Types
   UL4_Modules
   UL4_Methods
	UL4_TemplatesAsFunctions
	UL4_GlobalVariables
	UL4_InterfacingWithPython
   UL4_Exceptions
   UL4_Whitespace
   UL4_API
