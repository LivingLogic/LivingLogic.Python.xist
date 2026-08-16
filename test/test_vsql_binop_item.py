"""
Tests for the vSQL binary item access operator ``A[B]``.

To run the tests, :mod:`pytest` is required.
"""

import datetime

###
### Tests
###

def test_str_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[True]", where="r.identifier == 'str'") == 'u'


def test_str_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[2]", where="r.identifier == 'str'") == 'r'


def test_clob_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob[True]", where="r.identifier == 'clob'") == 'u'


def test_clob_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob[99998]", where="r.identifier == 'clob'") == 'r'


def test_strlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz', 'hinz', 'kunz'][True]") == 'hurz'


def test_strlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz', 'hinz', 'kunz'][2]") == 'hinz'


def test_cloblist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob, 'hurz'][True]", where="r.identifier == 'shortclob'") == 'hurz'


def test_cloblist_int(vsql_db, vsql_data):
	assert vsql_db.expr("['hurz', r.v_clob][1]", where="r.identifier == 'shortclob'") == 'gurk'


def test_intlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3][True]") == 2


def test_intlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3][2]") == 3


def test_numberlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3][True]") == 2.2


def test_numberlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3][2]") == 3.3


def test_datelist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01), @(2000-03-02)][True]") == vsql_db.type_for_date(2000, 3, 1)


def test_datelist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01), @(2000-03-02)][2]") == vsql_db.type_for_date(2000, 3, 2)


def test_datetimelist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56), @(2000-03-02T12:34:56)][True]") == datetime.datetime(2000, 3, 1, 12, 34, 56)


def test_datetimelist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56), @(2000-03-02T12:34:56)][2]") == datetime.datetime(2000, 3, 2, 12, 34, 56)


def test_nulllist_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("[][False]") is None


def test_nulllist_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None][True]") is None


def test_nulllist_int1(vsql_db, vsql_data):
	assert vsql_db.expr("[][0]") is None


def test_nulllist_int2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None][1]") is None