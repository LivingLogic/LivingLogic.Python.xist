"""
Tests for the vSQL floor division ``//``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_int // True", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool // True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool // True", where="r.identifier == 'bool_true'") == 1


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool // 1", where="r.identifier == 'bool_true'") == 1


def test_bool_number(db, vsql_data):
	assert expr(db, "r.v_bool // 0.5", where="r.identifier == 'bool_true'") == 2


def test_int_bool(db, vsql_data):
	assert expr(db, "2 // r.v_bool", where="r.identifier == 'bool_true'") == 2


def test_int_int(db, vsql_data):
	assert expr(db, "r.v_int // 2", where="r.identifier == 'int'") == 888


def test_int_number(db, vsql_data):
	assert expr(db, "85 // r.v_number", where="r.identifier == 'number'") == 2


def test_number_bool(db, vsql_data):
	assert expr(db, "r.v_number // True", where="r.identifier == 'number'") == 42


def test_number_int(db, vsql_data):
	assert expr(db, "r.v_number // 2", where="r.identifier == 'number'") == 21


def test_number_number(db, vsql_data):
	assert expr(db, "r.v_number // 3.5", where="r.identifier == 'number'") == 12


def test_datedelta_bool(db, vsql_data):
	assert expr(db, "r.v_datedelta // True", where="r.identifier == 'datedelta'") == 12


def test_datedelta_int(db, vsql_data):
	assert expr(db, "r.v_datedelta // 5", where="r.identifier == 'datedelta'") == 2


def test_monthdelta_bool(db, vsql_data):
	assert expr(db, "r.v_monthdelta // True", where="r.identifier == 'monthdelta'") == 3


def test_monthdelta_int(db, vsql_data):
	assert expr(db, "r.v_monthdelta // 2", where="r.identifier == 'monthdelta'") == 1


def test_datetimedelta_bool(db, vsql_data):
	assert expr(db, "r.v_datetimedelta // True", where="r.identifier == 'datetimedelta'") == 1


def test_datetimedelta_int(db, vsql_data):
	assert expr(db, "r.v_datetimedelta // 2", where="r.identifier == 'datetimedelta'") == 0


def test_datetimedelta_number(db, vsql_data):
	assert expr(db, "r.v_datetimedelta // 12.5", where="r.identifier == 'datetimedelta'") == 0