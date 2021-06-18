Interfacing with Python
#######################


Exposing attributes
===================

It is possible to expose attributes of a Python object to UL4 templates.
This is done by setting the class attribute ``ul4_attrs``::

	from ll import ul4c

	class Person:
		ul4_attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``Doe, John``.

Attributes not in ``ul4_attrs`` will not be visible::

	template = ul4c.Template("<?print p.age?>")
	print(template.renders(p=p))

This will output nothing, as the ``age`` attribute is not visible and thus
``p.age`` returns an ``undefined`` object.


Exposing methods
================

It is also possible to expose methods of a Python object to UL4 templates.
This is done by including the method name in the ``ul4_attrs`` class attribute::

	from ll import ul4c

	class Person:
		ul4_attrs = {"fullname"}

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
		ul4_attrs = {"fullname", "varcount"}

		@ul4c.withcontext
		def varcount(self, context):
			return len(context.vars)


Custom attributes
=================

To customize getting and setting object attributes from UL4 templates the
methods :meth:`ul4_getattr` and :meth:`ul4_setattr` can be implemented::

	from ll import ul4c

	class Person:
		ul4_attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

		def ul4_getattr(self, name):
			return getattr(self, name).upper()

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``DOE, JOHN``.

If the object has an attribute ``ul4_attrs`` :meth:`ul4_getattr` will only be
called for the attributes in ``ul4_attrs``, otherwise :meth:`ul4_getattr` will
be called for all attributes (and should raise an :exc:`AttributeError` for
nonexistent attributes)

Attributes can be made writable by implementing the method :meth:`ul4_setattr`::

	from ll import ul4c

	class Person:
		ul4_attrs = {"firstname", "lastname"}

		def __init__(self, firstname, lastname, age):
			self.firstname = firstname
			self.lastname = lastname
			self.age = age

		def ul4_setattr(self, name, value):
			return setattr(self, name, value.upper())

	p = Person("John", "Doe", 42)

	template = ul4c.Template("<?code p.lastname = 'Doe'?><?print p.lastname?>, <?print p.firstname?>")
	print(template.renders(p=p))

This will output ``DOE, John``.

If the object has an attribute ``ul4_attrs`` :meth:`ul4_setattr` will only be
called for the attributes in ``ul4_attrs``, otherwise :meth:`ul4_setattr` will
be called for all attributes (and should raise an :exc:`AttributeError` for
nonexistent or readonly attributes)

Without a :meth:`ul4_setattr` method, attributes will never be made writable.
