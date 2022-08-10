#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2022-2022 by LivingLogic AG, Bayreuth/Germany
## Copyright 2022-2022 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, os, datetime, decimal

import pytest

from ll import postsql, url


dbname = os.environ.get("LL_POSTSQL_TEST_CONNECT") # Need a connectstring as environment var


class Info:
	def __init__(self, obj):
		self.obj = obj
		self.references = list(obj.references())
		self.referencedby = list(obj.referencedby())


# here all objects are collected, so we don't need to call :meth:`objects` multiple times
class Data:
	def __init__(self, dbname):
		self.dbname = dbname
		self._objects = None

	def _make(self):
		self._objects = {}
		db = postsql.connect(self.dbname)
		# get all definitions
		# (this tests that :meth:`objects`, :meth:`references` and :meth:`referencedby` run to completion)
		self._objects = {obj: Info(obj) for obj in db.objects()}

	def objects(self):
		if dbname and self._objects is None:
			self._make()
		return self._objects


@pytest.fixture(scope="module")
def db_data(request):
	"""
	Return a :class:`Data` object. :meth:`Data.objects` returns a dictionary
	object containing information about all database objects and the references
	between those objects.
	"""
	return Data(dbname)


@pytest.mark.db
def test_connect():
	db = postsql.connect(dbname)
	assert isinstance(db, postsql.Connection)


@pytest.mark.db
def test_connection_connectstring():
	db = postsql.connect(dbname)
	assert set(db.dsn.split()) <= set(dbname.split())


@pytest.mark.db
def test_connection_schemas():
	db = postsql.connect(dbname)
	list(db.schemas(internal=None))
	list(db.schemas(internal=True))
	list(db.schemas(internal=False))
	list(db.schemas(schema="information_schema"))


@pytest.mark.db
def test_connection_tables():
	db = postsql.connect(dbname)
	list(db.tables(internal=None))
	list(db.tables(internal=True))
	list(db.tables(internal=False))
	list(db.tables(schema="information_schema"))


@pytest.mark.db
def test_connection_sequences():
	db = postsql.connect(dbname)
	list(db.sequences(internal=None))
	list(db.sequences(internal=True))
	list(db.sequences(internal=False))
	list(db.sequences(schema="information_schema"))


@pytest.mark.db
def test_connection_fks():
	db = postsql.connect(dbname)
	list(db.fks())


@pytest.mark.db
def test_referenceconsistency(db_data):
	objects = db_data.objects()
	for info in objects.values():
		for refobj in info.references:
			# check that :meth:`objects` returned everything
			print(f"{info.obj} -> {refobj}")
			assert refobj in objects
			# check that the referenced object points back to this one (via referencedby)
			assert info.obj in objects[refobj].referencedby

		# do the inverted check
		for refobj in info.referencedby:
			print(f"{info.obj} <- {refobj}")
			assert refobj in objects
			assert info.obj in objects[refobj].references


@pytest.mark.db
def test_sql(db_data):
	# check various sql methods
	for obj in db_data.objects():
		obj.createsql()
		if isinstance(obj, postsql.Sequence):
			obj.createsqlcopy()
		obj.dropsql()
		if isinstance(obj, postsql.ForeignKey):
			obj.enablesql()
			obj.disablesql()


@pytest.mark.db
def test_repr(db_data):
	# check that each repr method works
	for obj in db_data.objects():
		repr(obj)


@pytest.mark.db
def test_table_columns(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Table):
			for col in obj.columns():
				# comments are not output by :meth:`objects`, so we have to call :meth:`references`
				assert obj in col.references()
				# check various methods
				# calling :meth:`modifysql` doesn't make sense
				col.addsql()
				col.dropsql()
				col.datatype()
				col.default()
				col.nullable()
				col.comment()
				assert col.table() == obj


@pytest.mark.db
def test_table_comments(db_data):
	objects = db_data.objects()
	for obj in objects:
		if isinstance(obj, postsql.Table):
			# comments are output by :meth:`objects`, but not for materialized views
			if obj.ismview():
				for com in obj.comments():
					assert obj in com.references()
			else:
				for com in obj.comments():
					assert obj in objects[com].references


@pytest.mark.db
def test_table_constraints(db_data):
	objects = db_data.objects()
	for obj in objects:
		if isinstance(obj, postsql.Table):
			for con in obj.constraints():
				assert obj in objects[con].references


@pytest.mark.db
def test_table_records(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Table):
			# fetch only a few records
			for (i, rec) in enumerate(obj.records()):
				if i >= 5:
					break


@pytest.mark.db
def test_table_mview(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Table):
			assert (obj.mview() is not None) == obj.ismview()


@pytest.mark.db
def test_constraints(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Constraint):
			obj.table()
			if isinstance(obj, postsql.ForeignKey):
				obj.refconstraint()
				list(obj.columns())


@pytest.mark.db
def test_procedure_arguments(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Procedure):
			list(obj.arguments())


@pytest.mark.db
def test_procedure_nonexistent():
	if dbname:
		db = postsql.connect(dbname)
		with pytest.raises(postsql.SQLObjectNotFoundError):
			postsql.Procedure("DOESNOTEXIST")(db.cursor())


@pytest.mark.db
def test_createorder(db_data):
	# check that the default output order of :meth:`objects` (i.e. create order) works
	objects = db_data.objects()
	done = set()
	for info in objects.values():
		for refobj in info.references:
			assert refobj in done
		done.add(info.obj)


@pytest.mark.db
def test_scripts_oracreate():
	if dbname:
		# Test oracreate without executing anything
		args = f"--color=yes --verbose=yes --seqcopy=yes {dbname}"
		oracreate.main(args.split())


@pytest.mark.db
def test_scripts_oradrop():
	if dbname:
		# Test oradrop without executing anything
		args = f"--color=yes --verbose=yes {dbname}"
		oradrop.main(args.split())


@pytest.mark.db
def test_scripts_oradiff():
	if dbname:
		# Test oradiff (not really: we will not get any differences)
		allargs = [
			f"--color=yes --verbose=yes {dbname} {dbname}",
			f"--color=yes --verbose=yes {dbname} {dbname} -mfull",
		]
		for args in allargs:
			oradiff.main(args.split())


@pytest.mark.db
def test_scripts_oramerge():
	if dbname:
		# Test oramerge (not really: we will not get any differences)
		args = f"--color=yes --verbose=yes {dbname} {dbname} {dbname}"
		oramerge.main(args.split())


@pytest.mark.db
def test_scripts_oragrant():
	if dbname:
		# Test oragrant
		args = f"--color=yes {dbname}"
		oragrant.main(args.split())


@pytest.mark.db
def test_scripts_orafind():
	if dbname:
		# Test orafind
		args = f"--ignore-case yes --color=yes {dbname} foo"
		orafind.main(args.split())


@pytest.mark.db
def test_scripts_oradelete():
	if dbname:
		# Test oradelete without executing anything
		args = f"--color=yes --verbose=yes {dbname}"
		oradelete.main(args.split())


@pytest.mark.db
def test_scripts_orareindex():
	if dbname:
		# Test orareindex without executing anything
		args = f"--color=yes --verbose=yes {dbname}"
		orareindex.main(args.split())


@pytest.mark.db
def test_callprocedure():
	if dbname:
		db = postsql.connect(dbname)
		proc = db.object_named("postsql_testprocedure")
		result = proc(db.cursor(readlobs=True), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
		assert result.p_in == "abcäöü"
		assert result.p_out == "ABCÄÖÜ"
		assert result.p_inout == "ABC"*10000 + "abcäöü"

		result = proc(db.cursor(readlobs=False), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
		assert result.p_in == "abcäöü"
		assert result.p_out == "ABCÄÖÜ"
		assert readlob(result.p_inout, 8192) == "ABC"*10000 + "abcäöü"


@pytest.mark.db
def test_callfunction():
	if dbname:
		db = postsql.connect(dbname)
		func = db.object_named("postsql_testfunction")
		(result, args) = func(db.cursor(readlobs=True), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
		assert result == "ABCÄÖÜ"
		assert args.p_in == "abcäöü"
		assert args.p_out == "ABCÄÖÜ"
		assert args.p_inout == "ABC"*10000 + "abcäöü"

		(result, args) = func(db.cursor(readlobs=False), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
		assert result == "ABCÄÖÜ"
		assert args.p_in == "abcäöü"
		assert args.p_out == "ABCÄÖÜ"
		assert readlob(args.p_inout, 8192) == "ABC"*10000 + "abcäöü"


@pytest.mark.db
def test_clob_fromprocedure():
	if dbname:
		db = postsql.connect(dbname)
		proc = db.object_named("postsql_testprocedure")

		def check(sizearg):
			result = proc(db.cursor(readlobs=False), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
			assert readlob(result.p_inout, sizearg) == "ABC"*10000 + "abcäöü"
			assert result.p_inout.read() == ""

		check(8192)
		check(0)
		check(None)


@pytest.mark.db
def test_fetch(db_data):
	for obj in db_data.objects():
		if isinstance(obj, postsql.Table):
			# fetch only a few records
			db = postsql.connect(dbname)
			c = db.cursor()
			c.execute(f"select * from {obj.name}")
			c.fetchone()
			c.execute(f"select * from {obj.name}")
			c.fetchone()
			break


@pytest.mark.db
def test_url():
	dburl = dbname.replace("/", ":")
	u = url.URL(f"oracle://{dburl}/")
	assert u.isdir()
	assert u.mimetype() == "application/octet-stream"
	u.owner()
	u.cdate()
	u.mdate()
	u.listdir()
	u.files()
	u.dirs()

	u = url.URL(f"oracle://{dburl}/procedure/postSQL_TESTPROCEDURE")
	assert u.isfile()
	assert u.mimetype() == "text/x-oracle-procedure"
	u.owner()
	u.cdate()
	u.mdate()
	assert "postsql_testprocedure" in u.open("r").read().lower()


@pytest.mark.db
def test_exists():
	if dbname:
		db = postsql.connect(dbname)

		assert postsql.Procedure("postSQL_TESTPROCEDURE").exists(db)
		assert not postsql.Procedure("postSQL_NOTTESTPROCEDURE").exists(db)


@pytest.mark.db
def test_decimal():
	if dbname:
		db = postsql.connect(dbname, decimal=True)
		c = db.cursor()

		c.execute("select 42 from dual")
		r = c.fetchone()
		assert type(r[0]) is decimal.Decimal

		c.execute("select 42.5 from dual")
		r = c.fetchone()
		assert type(r[0]) is decimal.Decimal

		c.execute("select cast(42 as integer) from dual")
		r = c.fetchone()
		assert type(r[0]) is int
