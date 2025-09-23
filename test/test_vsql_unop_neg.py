"""
Tests for the vSQL unary negation operator ``-``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

def test_bool1(db, vsql_data):
	assert expr(db, "-r.v_bool", where="r.identifier == 'none'") is None


def test_bool2(db, vsql_data):
	assert expr(db, "-r.v_bool", where="r.identifier == 'bool_false'") == 0


def test_bool3(db, vsql_data):
	assert expr(db, "-r.v_bool", where="r.identifier == 'bool_true'") == -1


def test_int1(db, vsql_data):
	assert expr(db, "-r.v_int", where="r.identifier == 'none'") is None


def test_int2(db, vsql_data):
	assert expr(db, "-r.v_int", where="r.identifier == 'int'") == -1776


def test_number1(db, vsql_data):
	assert expr(db, "-r.v_number", where="r.identifier == 'none'") is None


def test_number2(db, vsql_data):
	assert expr(db, "-r.v_number", where="r.identifier == 'number'") == -42.5


def test_datedelta1(db, vsql_data):
	assert expr(db, "-r.v_datedelta", where="r.identifier == 'none'") is None


def test_datedelta2(db, vsql_data):
	assert expr(db, "-r.v_datedelta", where="r.identifier == 'datedelta'") == -12


def test_datetimedelta1(db, vsql_data):
	assert expr(db, "-r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_datetimedelta2(db, vsql_data):
	assert expr(db, "-r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == -(1 + 12/24 + 34/24/60 + 56/24/60/60)


def test_monthdelta1(db, vsql_data):
	assert expr(db, "-r.v_monthdelta", where="r.identifier == 'none'") is None


def test_monthdelta2(db, vsql_data):
	assert expr(db, "-r.v_monthdelta", where="r.identifier == 'monthdelta'") == -3
