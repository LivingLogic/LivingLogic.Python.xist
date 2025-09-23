"""
Tests for the vSQL unary logical "not" operator ``not``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

def test_bool1(db, vsql_data):
	assert expr(db, "not r.v_bool", where="r.identifier == 'none'") == True


def test_bool2(db, vsql_data):
	assert expr(db, "not r.v_bool", where="r.identifier == 'bool_false'") == True


def test_bool3(db, vsql_data):
	assert expr(db, "not r.v_bool", where="r.identifier == 'bool_true'") == False


def test_int1(db, vsql_data):
	assert expr(db, "not r.v_int", where="r.identifier == 'none'") == True


def test_int2(db, vsql_data):
	assert expr(db, "not r.v_int", where="r.identifier == 'int'") == False


def test_number1(db, vsql_data):
	assert expr(db, "not r.v_number", where="r.identifier == 'none'") == True


def test_number2(db, vsql_data):
	assert expr(db, "not r.v_number", where="r.identifier == 'number'") == False


def test_str1(db, vsql_data):
	assert expr(db, "not r.v_str", where="r.identifier == 'none'") == True


def test_str2(db, vsql_data):
	assert expr(db, "not r.v_str", where="r.identifier == 'str'") == False


def test_date1(db, vsql_data):
	assert expr(db, "not r.v_date", where="r.identifier == 'none'") == True


def test_date2(db, vsql_data):
	assert expr(db, "not r.v_date", where="r.identifier == 'date'") == False


def test_datetime1(db, vsql_data):
	assert expr(db, "not r.v_datetime", where="r.identifier == 'none'") == True


def test_datetime2(db, vsql_data):
	assert expr(db, "not r.v_datetime", where="r.identifier == 'datetime'") == False


def test_datedelta1(db, vsql_data):
	assert expr(db, "not r.v_datedelta", where="r.identifier == 'none'") == True


def test_datedelta2(db, vsql_data):
	assert expr(db, "not r.v_datedelta", where="r.identifier == 'datedelta'") == False


def test_datetimedelta1(db, vsql_data):
	assert expr(db, "not r.v_datetimedelta", where="r.identifier == 'none'") == True


def test_datetimedelta2(db, vsql_data):
	assert expr(db, "not r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == False


def test_monthdelta1(db, vsql_data):
	assert expr(db, "not r.v_monthdelta", where="r.identifier == 'none'") == True


def test_monthdelta2(db, vsql_data):
	assert expr(db, "not r.v_monthdelta", where="r.identifier == 'monthdelta'") == False


def test_color1(db, vsql_data):
	assert expr(db, "not r.v_color", where="r.identifier == 'none'") == True


def test_color2(db, vsql_data):
	assert expr(db, "not r.v_color", where="r.identifier == 'color'") == False


def test_geo(db, vsql_data):
	assert expr(db, "not geo(49, 11, 'Here')") == False
