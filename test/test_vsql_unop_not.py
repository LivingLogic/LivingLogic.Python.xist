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


def test_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_clob", where="r.identifier == 'none'") == True


def test_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("not r.v_clob", where="r.identifier == 'shortclob'") == False


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


def test_null(vsql_db, vsql_data):
	# ``not None`` would be constant-folded by UL4, but ``[None, None][0]``
	# is a non-constant expression of type ``NULL``, so the database really
	# executes the operator
	assert vsql_db.expr("not [None, None][0]") == True


def test_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("not []") == True


def test_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("not [None, None]") == False


def test_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("not [1, 2]") == False


def test_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("not [1.5, 2.5]") == False


def test_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("not ['gurk', 'hurz']") == False


def test_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("not [r.v_clob]", where="r.identifier == 'shortclob'") == False


def test_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("not [@(2000-02-29), @(2000-03-01)]") == False


def test_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("not [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == False


def test_intset(vsql_db, vsql_data):
	assert vsql_db.expr("not {1, 2}") == False


def test_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("not {1.5, 2.5}") == False


def test_strset(vsql_db, vsql_data):
	assert vsql_db.expr("not {'gurk', 'hurz'}") == False


def test_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("not {@(2000-02-29), @(2000-03-01)}") == False


def test_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("not {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}") == False


def test_nullset1(vsql_db, vsql_data):
	assert vsql_db.expr("not {/}") == True


def test_nullset2(vsql_db, vsql_data):
	assert vsql_db.expr("not {None, None}") == False
