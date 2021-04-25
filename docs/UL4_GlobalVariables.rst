Global variables
################

UL4 templates support global variables. To be able to pass parameters and
global variables to an UL4 template a second set of methods is available, so
that a list of positional arguments, a dictionary with keyword arguments and a
dictionary with global variables can be passed.

These methods are :meth:`~ll.ul4c.Template.render_with_globals`,
:meth:`~ll.ul4c.Template.renders_with_globals` and
:meth:`~ll.ul4c.Template.call_with_globals`.

An example using :meth:`~ll.ul4c.Template.renders_with_globals` looks like this::

	from ll import ul4c

	t1 = ul4c.Template("<?print x?>")
	t2 = ul4c.Template("<?render t1()?>")

	output = t2.renders_with_globals((), {"t1": t1}, {"x": 42})

With this ``output`` will be the string ``"42"``.

And an example using :meth:`~ll.ul4c.Template.call_with_globals` looks like this::

	from ll import ul4c

	t1 = ul4c.Template("<?return x?>")
	t2 = ul4c.Template("<?return t1()?>")

	result = t2.call_with_globals((), {"t1": t1}, {"x": 42})

With this ``result`` will be ``42``.
