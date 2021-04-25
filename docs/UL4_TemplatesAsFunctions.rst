.. _UL4_TemplatesAsFunctions:

Templates as functions
######################

UL4 templates can be called as functions too. Calling a template as a function
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
