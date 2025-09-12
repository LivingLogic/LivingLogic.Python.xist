"""
Tests for the vSQL modulo operator ``%``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool % True", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool % True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool % True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool % 1", where="r.identifier == 'bool_true'") == 0


def test_bool_number(db, vsql_data):
	assert expr(db, "r.v_bool % 0.3", where="r.identifier == 'bool_true'") == pytest.approx(0.1)


def test_int_bool(db, vsql_data):
	assert expr(db, "2 % r.v_bool", where="r.identifier == 'bool_true'") == 0


def test_int_int(db, vsql_data):
	assert expr(db, "r.v_int % 2", where="r.identifier == 'int'") == 0


def test_int_number(db, vsql_data):
	assert expr(db, "86 % r.v_number", where="r.identifier == 'number'") == 1


def test_number_bool(db, vsql_data):
	assert expr(db, "r.v_number % True", where="r.identifier == 'number'") == 0.5


def test_number_int(db, vsql_data):
	assert expr(db, "r.v_number % 4", where="r.identifier == 'number'") == 2.5


def test_number_number1(db, vsql_data):
	assert expr(db, "r.v_number % 3.5", where="r.identifier == 'number'") == 0.5


def test_number_number2(db, vsql_data):
	assert expr(db, "r.v_number % -3.5", where="r.identifier == 'number'") == -3.0


def test_number_number3(db, vsql_data):
	assert expr(db, "-r.v_number % 3.5", where="r.identifier == 'number'") == 3.0


def test_number_number4(db, vsql_data):
	assert expr(db, "-r.v_number % -3.5", where="r.identifier == 'number'") == -0.5