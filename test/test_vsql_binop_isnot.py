"""
Tests for the vSQL binary inverted containment test operator ``not in``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is not None", where="r.identifier == 'none'") == 0


def test_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is not None", where="r.identifier == 'bool_false'") == 1


def test_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is not None", where="r.identifier == 'bool_true'") == 1


def test_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_bool", where="r.identifier == 'none'") == 0


def test_bool5(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_bool", where="r.identifier == 'bool_false'") == 1


def test_bool6(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_bool", where="r.identifier == 'bool_true'") == 1


def test_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int is not None", where="r.identifier == 'none'") == 0


def test_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int is not None", where="r.identifier == 'int'") == 1


def test_int3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_int", where="r.identifier == 'none'") == 0


def test_int4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_int", where="r.identifier == 'int'") == 1


def test_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number is not None", where="r.identifier == 'none'") == 0


def test_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number is not None", where="r.identifier == 'number'") == 1


def test_number3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_number", where="r.identifier == 'none'") == 0


def test_number4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_number", where="r.identifier == 'number'") == 1


def test_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str is not None", where="r.identifier == 'none'") == 0


def test_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str is not None", where="r.identifier == 'str'") == 1


def test_str3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_str", where="r.identifier == 'none'") == 0


def test_str4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_str", where="r.identifier == 'str'") == 1


def test_color1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color is not None", where="r.identifier == 'none'") == 0


def test_color2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color is not None", where="r.identifier == 'color'") == 1


def test_color3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_color", where="r.identifier == 'none'") == 0


def test_color4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_color", where="r.identifier == 'color'") == 1


def test_date1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date is not None", where="r.identifier == 'none'") == 0


def test_date2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date is not None", where="r.identifier == 'date'") == 1


def test_date3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_date", where="r.identifier == 'none'") == 0


def test_date4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_date", where="r.identifier == 'date'") == 1


def test_datetime1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime is not None", where="r.identifier == 'none'") == 0


def test_datetime2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime is not None", where="r.identifier == 'datetime'") == 1


def test_datetime3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datetime", where="r.identifier == 'none'") == 0


def test_datetime4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datetime", where="r.identifier == 'datetime'") == 1


def test_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta is not None", where="r.identifier == 'none'") == 0


def test_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta is not None", where="r.identifier == 'datedelta'") == 1


def test_datedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datedelta", where="r.identifier == 'none'") == 0


def test_datedelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datedelta", where="r.identifier == 'datedelta'") == 1


def test_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta is not None", where="r.identifier == 'none'") == 0


def test_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta is not None", where="r.identifier == 'datetimedelta'") == 1


def test_datetimedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datetimedelta", where="r.identifier == 'none'") == 0


def test_datetimedelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == 1


def test_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta is not None", where="r.identifier == 'none'") == 0


def test_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta is not None", where="r.identifier == 'monthdelta'") == 1


def test_monthdelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_monthdelta", where="r.identifier == 'none'") == 0


def test_monthdelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is not r.v_monthdelta", where="r.identifier == 'monthdelta'") == 1


def test_geo1(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49, 11, 'Here') is not None") == 1


def test_geo2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not geo(49, 11, 'Here')") == 1


def test_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3] is not None") == 1


def test_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not [1, 2, 3]") == 1


def test_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3] is not None") == 1


def test_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not [1.1, 2.2, 3.3]") == 1


def test_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] is not None") == 1


def test_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not ['gurk', 'hurz']") == 1


def test_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] is not None") == 1


def test_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not [@(2000-02-29), @(2000-03-01)]") == 1


def test_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] is not None") == 1


def test_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is not [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 1