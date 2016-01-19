# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2004-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2004-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


'''
This module is an XIST namespace. It provides the processing instruction classes
needed to create TOXIC functions and procedures via XIST. For more info about
the TOXIC compiler see the module :mod:`ll.toxicc`.
'''


from ll.xist import xsc


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/toxic"


class args(xsc.ProcInst):
	"""
	Specifies the arguments to be used by the generated function. For example::

		<?args
			key in integer,
			lang in varchar2
		?>

	for Oracle, or::

		<?args
			@key int,
			@lang varchar(10)
		?>

	for SQL Server. If :class:`args` is used multiple times, the contents will
	be concatenated with a ``,`` inbetween.
	"""


class vars(xsc.ProcInst):
	"""
	Specifies the local variables to be used by the function. For example::

		<?vars
			buffer varchar2(200) := 'foo';
			counter integer;
		?>

	for Oracle, or::

		<?vars
			declare @buffer varchar(200) := 'foo';
			declare @counter int;
		?>

	If :class:`vars` is used multiple times, the contents will simple be
	concatenated. (Note that for SQL Server this could be done via a normal
	:class:`code` PI too.)
	"""


class code(xsc.ProcInst):
	"""
	A SQL code fragment that will be embedded literally in the generated
	function. For example::

		<?code select user into v_user from dual;?>

	for Oracle, or::

		<?code set @user = user;?>

	for SQL Server
	"""


class expr(xsc.ProcInst):
	"""
	The data of an :class:`expr` processing instruction must contain a SQL
	expression whose value will be embedded in the string returned by the
	generated function. This value will not be escaped in any way, so you can
	generate XML tags with :class:`expr` PIs but you must make sure to generate
	the value in the encoding that the caller of the generated function expects.
	"""


class proc(xsc.ProcInst):
	"""
	When this processing instruction is found in the source :func:`compile` will
	not generate a function as a result, but a procedure. This procedure must
	have ``c_out`` as an "out" variable (of the appropriate type (see
	:class:`type`) where the output will be written to.
	"""


class type(xsc.ProcInst):
	"""
	Can be used to specify the return type of the generated function/procedure.
	The default is ``clob`` for Oracle and ``varchar(max)`` for SQL Server.
	"""
