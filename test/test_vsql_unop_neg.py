"""
Tests for the vSQL unary negation operator ``-``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_bool", where="r.identifier == 'none'") is None


def test_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_bool", where="r.identifier == 'bool_false'") == 0


def test_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_bool", where="r.identifier == 'bool_true'") == -1


def test_int1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int", where="r.identifier == 'none'") is None


def test_int2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int", where="r.identifier == 'int'") == -1776


def test_number1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_number", where="r.identifier == 'none'") is None


def test_number2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_number", where="r.identifier == 'number'") == -42.5


def test_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_datedelta", where="r.identifier == 'none'") is None


def test_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_datedelta", where="r.identifier == 'datedelta'") == -12


def test_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == -(1 + 12/24 + 34/24/60 + 56/24/60/60)


def test_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_monthdelta", where="r.identifier == 'none'") is None


def test_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_monthdelta", where="r.identifier == 'monthdelta'") == -3
