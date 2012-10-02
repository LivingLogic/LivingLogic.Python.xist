#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2004-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2004-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


import sys, os, datetime

import pytest

from ll import orasql, url
from ll.orasql.scripts import oracreate, oradrop, oradiff, oramerge, oragrant, orafind


dbname = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


# here all objects are collected, so we don't need to call :meth:`iterobjects` multiple times
class Data:
	def __init__(self, dbname):
		self.dbname = dbname
		self._objlist = None
		self._objdict = None

	def _make(self):
		self._objlist = []
		self._objdict = {}
		db = orasql.connect(self.dbname)
		# get all definitions
		# (this tests that :meth:`iterobjects`, :meth:`iterreferences` and :meth:`iterreferencedby` run to completion)
		for obj in db.iterobjects(None):
			if obj.owner is None:
				self._objlist.append(obj)
				references = [o for o in obj.iterreferences() if o.owner is None]
				referencedby = [o for o in obj.iterreferencedby() if o.owner is None]
				self._objdict[obj] = (references, referencedby)

	def objlist(self):
		if dbname and self._objlist is None:
			self._make()
		return self._objlist

	def objdict(self):
		if dbname and self._objdict is None:
			self._make()
		return self._objdict


data = Data(dbname)


def readlob(value, size=None):
	result = []
	while True:
		data = value.read(size)
		if not data:
			break
		result.append(data)
	return "".join(result)


@pytest.mark.db
def test_connect():
	db = orasql.connect(dbname)
	assert isinstance(db, orasql.Connection)


@pytest.mark.db
def test_connection_connectstring():
	db = orasql.connect(dbname)
	user = dbname.split("/")[0]
	name = dbname.split("@")[1]
	assert "{}@{}".format(user, name) == db.connectstring()


@pytest.mark.db
def test_connection_itertables():
	db = orasql.connect(dbname)
	list(db.itertables(None))


@pytest.mark.db
def test_connection_itersequences():
	db = orasql.connect(dbname)
	list(db.itersequences(None))


@pytest.mark.db
def test_connection_iterfks():
	db = orasql.connect(dbname)
	list(db.iterfks(None))


@pytest.mark.db
def test_connection_iterprivileges():
	db = orasql.connect(dbname)
	list(db.iterprivileges(None))


@pytest.mark.db
def test_connection_iterusers():
	db = orasql.connect(dbname)
	list(db.iterusers())


@pytest.mark.db
def test_referenceconsistency():
	for (obj, (references, referencedby)) in data.objdict().items():
		for refobj in references:
			# check that :meth:`iterobjects` returned everything from this schema
			assert refobj.owner is not None or refobj in data.objdict()
			# check that the referenced object points back to this one (via referencedby)
			if refobj.owner is None:
				assert obj in data.objdict()[refobj][1]

		# do the inverted check
		for refobj in referencedby:
			assert refobj.owner is not None or refobj in data.objdict()
			if refobj.owner is None:
				assert obj in data.objdict()[refobj][0]


@pytest.mark.db
def test_ddl():
	# check various ddl methods
	for obj in data.objdict():
		obj.createddl()
		if isinstance(obj, orasql.Sequence):
			obj.createddlcopy()
		obj.dropddl()
		if isinstance(obj, orasql.ForeignKey):
			obj.enableddl()
			obj.disableddl()


@pytest.mark.db
def test_repr():
	# check that each repr method works
	for obj in data.objdict():
		repr(obj)


@pytest.mark.db
def test_cudate():
	# check that cdate/udate method works
	for obj in data.objdict():
		cdate = obj.cdate()
		assert cdate is None or isinstance(cdate, datetime.datetime)
		udate = obj.udate()
		assert udate is None or isinstance(udate, datetime.datetime)


@pytest.mark.db
def test_table_columns():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			for col in obj.itercolumns():
				# comments are not output by :meth:`iterobjects`, so we have to call :meth:`iterreferences`
				assert obj in col.iterreferences()
				# check various methods
				# calling :meth:`modifyddl` doesn't make sense
				col.addddl()
				col.dropddl()
				col.cdate()
				col.udate()
				col.datatype()
				col.default()
				col.nullable()
				col.comment()
				assert col.table() == obj


@pytest.mark.db
def test_table_comments():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			# comments are output by :meth:`iterobjects`, but not for materialized views
			if obj.ismview():
				for com in obj.itercomments():
					assert obj in com.iterreferences()
			else:
				for com in obj.itercomments():
					assert obj in data.objdict()[com][0]


@pytest.mark.db
def test_table_constraints():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			for con in obj.iterconstraints():
				assert obj in data.objdict()[con][0]


@pytest.mark.db
def test_table_records():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			# fetch only a few records
			for (i, rec) in enumerate(obj.iterrecords()):
				if i >= 5:
					break


@pytest.mark.db
def test_table_mview():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			assert (obj.mview() is not None) == obj.ismview()


@pytest.mark.db
def test_constraints():
	for obj in data.objdict():
		if isinstance(obj, orasql.Constraint):
			obj.table()
			if isinstance(obj, orasql.ForeignKey):
				obj.pk()
				list(obj.itercolumns())


@pytest.mark.db
def test_procedure_arguments():
	for obj in data.objdict():
		if isinstance(obj, orasql.Procedure):
			list(obj.iterarguments())


@pytest.mark.db
def test_procedure_nonexistant():
	if dbname:
		db = orasql.connect(dbname)
		with pytest.raises(orasql.SQLObjectNotFoundError):
			orasql.Procedure("DOESNOTEXIST")(db.cursor())


@pytest.mark.db
def test_createorder():
	# check that the default output order of :meth:`iterobjects` (i.e. create order) works
	done = set()
	for obj in data.objlist():
		for refobj in data.objdict()[obj][0]:
			assert refobj in done
		done.add(obj)


@pytest.mark.db
def test_scripts_oracreate():
	if dbname:
		# Test oracreate without executing anything
		args = "--color=yes --verbose=yes --seqcopy=yes {}".format(dbname)
		oracreate.main(args.split())


@pytest.mark.db
def test_scripts_oradrop():
	if dbname:
		# Test oradrop without executing anything
		args = "--color=yes --verbose=yes {}".format(dbname)
		oradrop.main(args.split())


@pytest.mark.db
def test_scripts_oradiff():
	if dbname:
		# Test oradiff (not really: we will not get any differences)
		allargs = [
			"--color=yes --verbose=yes {0} {0}".format(dbname),
			"--color=yes --verbose=yes {0} {0} -mfull".format(dbname),
		]
		for args in allargs:
			oradiff.main(args.split())


@pytest.mark.db
def test_scripts_oramerge():
	if dbname:
		# Test oramerge (not really: we will not get any differences)
		args = "--color=yes --verbose=yes {0} {0} {0}".format(dbname)
		oramerge.main(args.split())


@pytest.mark.db
def test_scripts_oragrant():
	if dbname:
		# Test oragrant
		args = "--color=yes {0}".format(dbname)
		oragrant.main(args.split())


@pytest.mark.db
def test_scripts_orafind():
	if dbname:
		# Test orafind
		args = "--ignore-case yes --color=yes {0} foo".format(dbname)
		orafind.main(args.split())


@pytest.mark.db
def test_callprocedure():
	if dbname:
		db = orasql.connect(dbname)
		proc = db.getobject("orasql_testprocedure")
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
		db = orasql.connect(dbname)
		func = db.getobject("orasql_testfunction")
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
		db = orasql.connect(dbname)
		proc = db.getobject("orasql_testprocedure")
		@pytest.mark.db
		def check(sizearg):
			result = proc(db.cursor(readlobs=False), c_user="pytest", p_in="abcäöü", p_inout="abc"*10000)
			assert readlob(result.p_inout, sizearg) == "ABC"*10000 + "abcäöü"
			assert result.p_inout.read() == ""
		yield check, 1
		yield check, 2
		yield check, 8192
		yield check, 0
		yield check, None


@pytest.mark.db
def test_fetch():
	for obj in data.objdict():
		if isinstance(obj, orasql.Table):
			# fetch only a few records
			db = orasql.connect(dbname)
			c = db.cursor()
			c.execute("select * from {}".format(obj.name))
			c.readlobs = False
			c.fetchone()
			c.execute("select * from {}".format(obj.name))
			c.readlobs = True
			c.fetchone()
			break


@pytest.mark.db
def test_url():
	u = url.URL("oracle://{}/".format(dbname.replace("/", ":")))
	assert u.isdir()
	assert u.mimetype() == "application/octet-stream"
	u.owner()
	u.cdate()
	u.mdate()
	u.listdir()
	u.files()
	u.dirs()

	u = url.URL("oracle://{}/procedure/ORASQL_TESTPROCEDURE".format(dbname.replace("/", ":")))
	assert u.isfile()
	assert u.mimetype() == "text/x-oracle-procedure"
	u.owner()
	u.cdate()
	u.mdate()
	assert "orasql_testprocedure" in u.openread().read().lower()
