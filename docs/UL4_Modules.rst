Modules
#######

A module is an object that collects a number of constants, functions and
types under a common name. Also a module always has the attributes ``__name__``
and ``__doc__``.


``operator``
============

The ``operator`` module contains the type ``attrgetter``. The object
``attrgetter(n)`` is callable and when called with an object ``a`` returns
``a``\s attribute named ``n``.  This can be used for sorting objects by their
attributes without having to create local templates.

For example ::

	<?print operator.attrgetter('year')(now())()?>

prints ``2021``.


``math``
========

This module contains constants and functions related to mathematical operations:

*	``math.e`` is the base of the natural logarithm (2.718281828...).
*	``math.pi`` is the ratio of a circle's circumference to its diameter
	(3.14159265...).
*	``math.tau`` is ``2 * math.pi``.
*	The trigonometric function ``math.cos()`` return the cosine of it argument
	(which must be in radians).
*	The trigonometric function ``math.sin()`` return the sine of it argument
	(which must be in radians).
*	The trigonometric function ``math.tan()`` return the tangent of it argument
	(which must be in radians).
*	``math.sqrt()`` which returns the square root of its argument.
*	``math.isclose(a, b)`` returns ``True`` if the values ``a`` and ``b``
	are close to each other and ``False`` otherwise. Whether or not two values
	are considered close is determined according to given absolute and relative
	tolerances (via the keyword arguments ``rel_tol`` and ``abs_tol``).


``ul4on``
=========

This module contains functions and types for working with :mod:`ll.ul4on`:

*	``ul4on.dumps(foo)`` returns the UL4ON representation of the object ``foo``.

*	``ul4on.loads(foo)`` decodes the UL4ON string ``foo`` and returns the
	resulting object.

*	``ul4on.Encoder(indent)`` creates an encoder object that can be used to
	create multiple UL4ON dump using the same context. An ``ul4on.Encoder``
	object has a method ``dumps`` that creates an UL4ON dump for the passed in
	object.

*	``ul4on.Decoder()`` creates a decoder object that can be used to recreate
	objects from multiple UL4ON dumps using the same context. An
	``ul4on.Decoder`` object has a method ``loads`` that recreates an object
	from the passed in UL4ON dump.


``ul4``
=======

This module contains all the types of the nodes in the abstract syntax tree that
comprises an UL4 template. The available types are: ``TextAST``, ``IndentAST``,
``LineEndAST``, ``CodeAST``, ``ConstAST``, ``SeqItemAST``, ``UnpackSeqItemAST``,
``DictItemAST``, ``UnpackDictItemAST``, ``PositionalArgumentAST``,
``KeywordArgumentAST``, ``UnpackListArgumentAST``, ``UnpackDictArgumentAST``,
``ListAST``, ``ListComprehensionAST``, ``SetAST``, ``SetComprehensionAST``,
``DictAST``, ``DictComprehensionAST``, ``GeneratorExpressionAST``, ``VarAST``,
``BlockAST``, ``ConditionalBlocksAST``, ``IfBlockAST``, ``ElIfBlockAST``,
``ElseBlockAST``, ``ForBlockAST``, ``WhileBlockAST``, ``BreakAST``,
``ContinueAST``, ``AttrAST``, ``SliceAST``, ``UnaryAST``, ``NotAST``,
``NegAST``, ``BitNotAST``, ``PrintAST``, ``PrintXAST``, ``ReturnAST``,
``BinaryAST``, ``ItemAST``, ``IsAST``, ``IsNotAST``, ``EQAST``, ``NEAST``,
``LTAST``, ``LEAST``, ``GTAST``, ``GEAST``, ``ContainsAST``, ``NotContainsAST``,
``AddAST``, ``SubAST``, ``MulAST``, ``FloorDivAST``, ``TrueDivAST``, ``ModAST``,
``ShiftLeftAST``, ``ShiftRightAST``, ``BitAndAST``, ``BitXOrAST``, ``BitOrAST``,
``AndAST``, ``OrAST``, ``IfAST``, ``ChangeVarAST``, ``SetVarAST``, ``AddVarAST``,
``SubVarAST``, ``MulVarAST``, ``FloorDivVarAST``, ``TrueDivVarAST``,
``ModVarAST``, ``ShiftLeftVarAST``, ``ShiftRightVarAST``, ``BitAndVarAST``,
``BitXOrVarAST``, ``BitOrVarAST``, ``CallAST``, ``RenderAST``, ``RenderXAST``,
``RenderBlockAST``, ``RenderBlocksAST``, ``SignatureAST``, ``Template`` and
``TemplateClosure``.

The only callable type in this list is ``Template`` which can be used to
create an UL4 template from source. Its signature is ::

	(
		source=None,
		name=None,
		*,
		whitespace="keep",
		signature=None
	)

.. note::
	``ul4.Template`` is not callable in the Javascript version of UL4.
