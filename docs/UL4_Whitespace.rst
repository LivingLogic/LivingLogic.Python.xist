.. _UL4_Whitespace:

Whitespace handling
===================

Normally the literal text between template tags will be output as it is. This
behaviour can be changed by passing a different value to the ``whitespace``
parameter in the constructor. The possible values are:

``"keep"``
	The default behaviour: literal text will be output as it is.

``"strip"``
	Linefeeds and the following indentation in literal text will be ignored:

	.. sourcecode:: pycon

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
	will be stripped from the text.

	Furthermore the additional indentation that might be introduced by a ``for``,
	``if``, ``elif``, ``else`` or ``def`` block will be ignored. So for example
	the output of:

	.. sourcecode:: ul4

		<?code langs = ["Python", "Java", "Javascript"]?>
		<?if langs?>
			<?for lang in langs?>
				<?print lang?>
			<?end for?>
		<?end if?>

	will simply be

	.. sourcecode:: output

		Python
		Java
		Javascript

	without any additional empty lines or indentation.

	Rendering a template ``B`` inside an template ``A`` will reindent the output
	of ``B`` to the indentation level of the ``<?render?>`` tag in the template
	``A``.

It is also possible to specify the whitespace behaviour in the template itself
with the ``<?whitespace?>`` tag, so:

.. sourcecode:: ul4

	<?whitespace smart?>

anywhere in the template source will switch on smart whitespace handling.

A ``<?whitespace?>`` tag overwrites the ``whitespace`` parameter specified
in the constructor.
