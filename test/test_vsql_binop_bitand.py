'''
Tests for the vSQL binary bitwise "and" operator ``A & B``.

To run the tests, :mod:`pytest` is required.
'''

import datetime
from conftest import *


###
### Tests
###

def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool & True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool & True", where="r.identifier == 'bool_true'") == 1


def test_bool_int1(db, vsql_data):
	assert expr(db, "r.v_bool & 3", where="r.identifier == 'bool_false'") == 0


def test_bool_int2(db, vsql_data):
	assert expr(db, "r.v_bool & 3", where="r.identifier == 'bool_true'") == 1


def test_int_bool1(db, vsql_data):
	assert expr(db, "r.v_int & False", where="r.identifier == 'int'") == 0


def test_int_bool2(db, vsql_data):
	assert expr(db, "r.v_int & True", where="r.identifier == 'int'") == 0


def test_int_int1(db, vsql_data):
	assert expr(db, "r.v_int & 313", where="r.identifier == 'int'") == 48


def test_int_int2(db, vsql_data):
	assert expr(db, "r.v_int & 270", where="r.identifier == 'int'") == 0


def test_int_int3(db, vsql_data):
	assert expr(db, "(-r.v_int) & 313", where="r.identifier == 'int'") == 272


def test_intset_intset1(db, vsql_data):
	assert expr(db, "{1} & {2}") == []


def test_intset_intset2(db, vsql_data):
	assert expr(db, "{1, 2} & {2, 3}") == [2]


def test_numberset_numberset1(db, vsql_data):
	assert expr(db, "{1.1} & {2.2}") == []


def test_numberset_numberset2(db, vsql_data):
	assert expr(db, "{1.1, 2.2} & {2.2, 3.3}") == [2.2]


def test_strset_strset1(db, vsql_data):
	assert expr(db, '{"gurk", "hurz"} & {"hinz", "kunz"}') == []


def test_strset_strset2(db, vsql_data):
	assert expr(db, '{"gurk", "hurz"} & {"hurz", "kunz"}') == ["hurz"]


def test_dateset_dateset1(db, vsql_data):
	assert expr(db, "{@(2000-02-29), @(2000-03-01)} & {@(2000-03-02), @(2000-03-03)}") == []


def test_dateset_dateset2(db, vsql_data):
	assert expr(db, "{@(2000-02-29), @(2000-03-01)} & {@(2000-03-01), @(2000-03-02)}") == [datetime.datetime(2000, 3, 1)]


def test_datetimeset_datetimeset1(db, vsql_data):
	assert expr(db, "{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} & {@(2000-03-02T12:34:56), @(2000-03-03T12:34:56)}") == []


def test_datetimeset_datetimeset2(db, vsql_data):
	assert expr(db, "{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} & {@(2000-03-01T12:34:56), @(2000-03-02T12:34:56)}") == [datetime.datetime(2000, 3, 1, 12, 34, 56)]