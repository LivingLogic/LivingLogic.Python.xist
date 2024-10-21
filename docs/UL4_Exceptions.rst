Exceptions
##########

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
one etc.). So if we have the following UL4 template:

.. sourcecode:: xml+ul4

	<?def x(i)?>
		Print: <?print 1/i?>
		Render: <?render x(i-1)?>
	<?end def?>
	Initial render: <?render x(3)?>

Calling the template will result in a :class:`ZeroDivisionError` exception. We
can format a nice UL4 stacktrace (in HTML) for this exception with the
following UL4 code:

.. sourcecode:: xml+ul4

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
					<b><?printx type(exc).__name__?></b><?if str(exc)?>: <?print str(exc)?><?end if?>
				</p>
			</li>
		<?end if?>
	<?end def?>

	<ul>
		<?render frame(exc)?>
	</ul>
