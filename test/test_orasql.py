#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2004-2011 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2004-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


import sys, os, datetime

import py.test

from ll import orasql, url
from ll.orasql.scripts import oracreate, oradrop, oradiff, oramerge, oragrant, orafind


dbname = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


# here all objects are collected, so we don't need to call :meth:`iterobjects` multiple times
objlist = []
objdict = {}

def setup_module(module):
	if dbname:
		db = orasql.connect(dbname)
		# get all definitions
		# (this tests that :meth:`iterobjects`, :meth:`iterreferences` and :meth:`iterreferencedby` run to completion)
		module.objdict = {}
		for obj in db.iterobjects():
			if obj.owner is None:
				module.objlist.append(obj)
				references = [o for o in obj.iterreferences() if o.owner is None]
				referencedby = [o for o in obj.iterreferencedby() if o.owner is None]
				module.objdict[obj] = (references, referencedby)


def teardown_module(module):
	module.objlist = []
	module.objdict = {}


def readlob(value, size=None):
	result = []
	while True:
		data = value.read(size)
		if not data:
			break
		result.append(data)
	return "".join(result)


@py.test.mark.db
def test_connect():
	db = orasql.connect(dbname)
	assert isinstance(db, orasql.Connection)


@py.test.mark.db
def test_connection_connectstring():
	db = orasql.connect(dbname)
	user = dbname.split("/")[0]
	name = dbname.split("@")[1]
	assert "{}@{}".format(user, name) == db.connectstring()


@py.test.mark.db
def test_connection_iterschema():
	db = orasql.connect(dbname)
	list(db.iterschema())


@py.test.mark.db
def test_connection_itertables():
	db = orasql.connect(dbname)
	list(db.itertables())


@py.test.mark.db
def test_connection_iterfks():
	db = orasql.connect(dbname)
	list(db.iterfks())


@py.test.mark.db
def test_connection_iterprivileges():
	db = orasql.connect(dbname)
	list(db.iterprivileges())


@py.test.mark.db
def test_referenceconsistency():
	for (obj, (references, referencedby)) in objdict.iteritems():
		for refobj in references:
			# check that :meth:`iterobjects` returned everything from this schema
			assert refobj.owner is not None or refobj in objdict
			# check that the referenced object points back to this one (via referencedby)
			if refobj.owner is None:
				assert obj in objdict[refobj][1]

		# do the inverted check
		for refobj in referencedby:
			assert refobj.owner is not None or refobj in objdict
			if refobj.owner is None:
				assert obj in objdict[refobj][0]


@py.test.mark.db
def test_ddl():
	# check various ddl methods
	for obj in objdict:
		obj.createddl()
		if isinstance(obj, orasql.Sequence):
			obj.createddlcopy()
		obj.dropddl()
		if isinstance(obj, orasql.ForeignKey):
			obj.enableddl()
			obj.disableddl()


@py.test.mark.db
def test_repr():
	# check that each repr method works
	for obj in objdict:
		repr(obj)


@py.test.mark.db
def test_cudate():
	# check that cdate/udate method works
	for obj in objdict:
		cdate = obj.cdate()
		assert cdate is None or isinstance(cdate, datetime.datetime)
		udate = obj.udate()
		assert udate is None or isinstance(udate, datetime.datetime)


@py.test.mark.db
def test_table_columns():
	for obj in objdict:
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


@py.test.mark.db
def test_table_comments():
	for obj in objdict:
		if isinstance(obj, orasql.Table):
			# comments are output by :meth:`iterobjects`, but not for materialized views
			if obj.ismview():
				for com in obj.itercomments():
					assert obj in com.iterreferences()
			else:
				for com in obj.itercomments():
					assert obj in objdict[com][0]


@py.test.mark.db
def test_table_constraints():
	for obj in objdict:
		if isinstance(obj, orasql.Table):
			for con in obj.iterconstraints():
				assert obj in objdict[con][0]


@py.test.mark.db
def test_table_records():
	for obj in objdict:
		if isinstance(obj, orasql.Table):
			# fetch only a few records
			for (i, rec) in enumerate(obj.iterrecords()):
				if i >= 5:
					break


@py.test.mark.db
def test_table_mview():
	for obj in objdict:
		if isinstance(obj, orasql.Table):
			assert (obj.mview() is not None) == obj.ismview()


@py.test.mark.db
def test_constraints():
	for obj in objdict:
		if isinstance(obj, orasql.Constraint):
			obj.table()
			if isinstance(obj, orasql.ForeignKey):
				obj.pk()
				list(obj.itercolumns())


@py.test.mark.db
def test_procedure_arguments():
	for obj in objdict:
		if isinstance(obj, orasql.Procedure):
			list(obj.iterarguments())


@py.test.mark.db
def test_procedure_nonexistant():
	db = orasql.connect(dbname)
	with py.test.raises(orasql.SQLObjectNotFoundError):
		orasql.Procedure("DOESNOTEXIST")(db.cursor())


@py.test.mark.db
def test_createorder():
	# check that the default output order of :meth:`iterobjects` (i.e. create order) works
	done = set()
	for obj in objlist:
		for refobj in objdict[obj][0]:
			assert refobj in done
		done.add(obj)


@py.test.mark.db
def test_scripts_oracreate():
	# Test oracreate without executing anything
	args = "--color=yes --verbose=yes --seqcopy=yes {}".format(dbname)
	oracreate.main(args.split())


@py.test.mark.db
def test_scripts_oradrop():
	# Test oradrop without executing anything
	args = "--color=yes --verbose=yes {}".format(dbname)
	oradrop.main(args.split())


@py.test.mark.db
def test_scripts_oradiff():
	# Test oradiff (not really: we will not get any differences)
	allargs = [
		"--color=yes --verbose=yes {0} {0}".format(dbname),
		"--color=yes --verbose=yes {0} {0} -mfull".format(dbname),
	]
	for args in allargs:
		oradiff.main(args.split())


@py.test.mark.db
def test_scripts_oramerge():
	# Test oramerge (not really: we will not get any differences)
	args = "--color=yes --verbose=yes {0} {0} {0}".format(dbname)
	oramerge.main(args.split())


@py.test.mark.db
def test_scripts_oragrant():
	# Test oragrant
	args = "--color=yes {0}".format(dbname)
	oragrant.main(args.split())


@py.test.mark.db
def test_scripts_orafind():
	# Test orafind
	args = "--ignore-case yes --color=yes {0} foo".format(dbname)
	orafind.main(args.split())


@py.test.mark.db
def test_callprocedure():
	db = orasql.connect(dbname)
	proc = db.getobject("orasql_testprocedure")
	result = proc(db.cursor(readlobs=True), c_user=u"py.test", p_in=u"abcäöü", p_inout=u"abc"*10000)
	assert result.p_in == u"abcäöü"
	assert result.p_out == u"ABCÄÖÜ"
	assert result.p_inout == u"ABC"*10000 + u"abcäöü"
	
	result = proc(db.cursor(readlobs=False), c_user=u"py.test", p_in=u"abcäöü", p_inout=u"abc"*10000)
	assert result.p_in == u"abcäöü"
	assert result.p_out == u"ABCÄÖÜ"
	assert readlob(result.p_inout, 8192) == u"ABC"*10000 + u"abcäöü"


@py.test.mark.db
def test_callfunction():
	db = orasql.connect(dbname)
	func = db.getobject("orasql_testfunction")
	(result, args) = func(db.cursor(readlobs=True), c_user=u"py.test", p_in=u"abcäöü", p_inout=u"abc"*10000)
	assert result == u"ABCÄÖÜ"
	assert args.p_in == u"abcäöü"
	assert args.p_out == u"ABCÄÖÜ"
	assert args.p_inout == u"ABC"*10000 + u"abcäöü"

	(result, args) = func(db.cursor(readlobs=False), c_user=u"py.test", p_in=u"abcäöü", p_inout=u"abc"*10000)
	assert result == u"ABCÄÖÜ"
	assert args.p_in == u"abcäöü"
	assert args.p_out == u"ABCÄÖÜ"
	assert readlob(args.p_inout, 8192) == u"ABC"*10000 + u"abcäöü"


@py.test.mark.db
def test_clob_fromprocedure():
	db = orasql.connect(dbname)
	proc = db.getobject("orasql_testprocedure")
	def check(sizearg):
		result = proc(db.cursor(readlobs=False), c_user=u"py.test", p_in=u"abcäöü", p_inout=u"abc"*10000)
		assert readlob(result.p_inout, sizearg) == u"ABC"*10000 + u"abcäöü"
		assert result.p_inout.read() == ""
	yield check, 1
	yield check, 2
	yield check, 8192
	yield check, 0
	yield check, None


@py.test.mark.db
def test_fetch():
	for obj in objdict:
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


@py.test.mark.db
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
