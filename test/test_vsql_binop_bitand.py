'''
Tests for the vSQL binary bitwise "and" operator ``A & B``.

To run the tests, :mod:`pytest` is required.
'''

import datetime


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool & True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool & True", where="r.identifier == 'bool_true'") == 1


def test_bool_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool & 3", where="r.identifier == 'bool_false'") == 0


def test_bool_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool & 3", where="r.identifier == 'bool_true'") == 1


def test_int_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int & False", where="r.identifier == 'int'") == 0


def test_int_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int & True", where="r.identifier == 'int'") == 0


def test_int_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int & 313", where="r.identifier == 'int'") == 48


def test_int_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int & 270", where="r.identifier == 'int'") == 0


def test_int_int3(vsql_db, vsql_data):
	assert vsql_db.expr("(-r.v_int) & 313", where="r.identifier == 'int'") == 272


def test_intset_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("{1} & {2}") == []


def test_intset_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("{1, 2} & {2, 3}") == [2]


def test_numberset_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("{1.1} & {2.2}") == []


def test_numberset_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("{1.1, 2.2} & {2.2, 3.3}") == [2.2]


def test_strset_strset1(vsql_db, vsql_data):
	assert vsql_db.expr('{"gurk", "hurz"} & {"hinz", "kunz"}') == []


def test_strset_strset2(vsql_db, vsql_data):
	assert vsql_db.expr('{"gurk", "hurz"} & {"hurz", "kunz"}') == ["hurz"]


def test_dateset_dateset1(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29), @(2000-03-01)} & {@(2000-03-02), @(2000-03-03)}") == []


def test_dateset_dateset2(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29), @(2000-03-01)} & {@(2000-03-01), @(2000-03-02)}") == [datetime.datetime(2000, 3, 1)]


def test_datetimeset_datetimeset1(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} & {@(2000-03-02T12:34:56), @(2000-03-03T12:34:56)}") == []


def test_datetimeset_datetimeset2(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} & {@(2000-03-01T12:34:56), @(2000-03-02T12:34:56)}") == [datetime.datetime(2000, 3, 1, 12, 34, 56)]