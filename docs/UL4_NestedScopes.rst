Nested scopes
#############

UL4 templates support lexical scopes. This means that a template that is defined
(via ``<?def?>``) inside another template has access to the local variables
of the outer template. The inner template sees the state of the variables at
the point in time when the inner templates gets called. The following example
will output ``2``:

.. sourcecode:: ul4

	<?code i = 1?>
	<?def x?>
		<?print i?>
	<?end def?>
	<?code i = 2?>
	<?render x()?>
