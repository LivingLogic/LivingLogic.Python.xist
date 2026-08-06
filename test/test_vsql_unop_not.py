"""
Tests for the vSQL unary logical "not" operator ``not``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_bool", where="r.identifier == 'none'") == True


def test_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_bool", where="r.identifier == 'bool_false'") == True


def test_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_bool", where="r.identifier == 'bool_true'") == False


def test_int1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_int", where="r.identifier == 'none'") == True


def test_int2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_int", where="r.identifier == 'int'") == False


def test_number1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_number", where="r.identifier == 'none'") == True


def test_number2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_number", where="r.identifier == 'number'") == False


def test_str1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_str", where="r.identifier == 'none'") == True


def test_str2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_str", where="r.identifier == 'str'") == False


def test_date1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_date", where="r.identifier == 'none'") == True


def test_date2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_date", where="r.identifier == 'date'") == False


def test_datetime1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datetime", where="r.identifier == 'none'") == True


def test_datetime2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datetime", where="r.identifier == 'datetime'") == False


def test_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datedelta", where="r.identifier == 'none'") == True


def test_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datedelta", where="r.identifier == 'datedelta'") == False


def test_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datetimedelta", where="r.identifier == 'none'") == True


def test_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == False


def test_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_monthdelta", where="r.identifier == 'none'") == True


def test_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_monthdelta", where="r.identifier == 'monthdelta'") == False


def test_color1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_color", where="r.identifier == 'none'") == True


def test_color2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_color", where="r.identifier == 'color'") == False


def test_geo(vsql_db, vsql_data):
	assert vsql_db.expr("not geo(49, 11, 'Here')") == False
