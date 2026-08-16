"""
Tests for the vSQL binary identity test operator ``is``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is None", where="r.identifier == 'none'") == 1

def test_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is None", where="r.identifier == 'bool_false'") == 0

def test_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool is None", where="r.identifier == 'bool_true'") == 0

def test_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_bool", where="r.identifier == 'none'") == 1

def test_bool5(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_bool", where="r.identifier == 'bool_false'") == 0

def test_bool6(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_bool", where="r.identifier == 'bool_true'") == 0

def test_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int is None", where="r.identifier == 'none'") == 1

def test_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int is None", where="r.identifier == 'int'") == 0

def test_int3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_int", where="r.identifier == 'none'") == 1

def test_int4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_int", where="r.identifier == 'int'") == 0

def test_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number is None", where="r.identifier == 'none'") == 1

def test_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number is None", where="r.identifier == 'number'") == 0

def test_number3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_number", where="r.identifier == 'none'") == 1

def test_number4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_number", where="r.identifier == 'number'") == 0

def test_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str is None", where="r.identifier == 'none'") == 1

def test_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str is None", where="r.identifier == 'str'") == 0

def test_str3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_str", where="r.identifier == 'none'") == 1

def test_str4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_str", where="r.identifier == 'str'") == 0

def test_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob is None", where="r.identifier == 'none'") == 1

def test_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob is None", where="r.identifier == 'shortclob'") == 0

def test_clob3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_clob", where="r.identifier == 'none'") == 1

def test_clob4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_clob", where="r.identifier == 'shortclob'") == 0

def test_color1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color is None", where="r.identifier == 'none'") == 1

def test_color2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color is None", where="r.identifier == 'color'") == 0

def test_color3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_color", where="r.identifier == 'none'") == 1

def test_color4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_color", where="r.identifier == 'color'") == 0

def test_date1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date is None", where="r.identifier == 'none'") == 1

def test_date2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date is None", where="r.identifier == 'date'") == 0

def test_date3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_date", where="r.identifier == 'none'") == 1

def test_date4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_date", where="r.identifier == 'date'") == 0

def test_datetime1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime is None", where="r.identifier == 'none'") == 1

def test_datetime2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime is None", where="r.identifier == 'datetime'") == 0

def test_datetime3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datetime", where="r.identifier == 'none'") == 1

def test_datetime4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datetime", where="r.identifier == 'datetime'") == 0

def test_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta is None", where="r.identifier == 'none'") == 1

def test_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta is None", where="r.identifier == 'datedelta'") == 0

def test_datedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datedelta", where="r.identifier == 'none'") == 1

def test_datedelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datedelta", where="r.identifier == 'datedelta'") == 0

def test_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta is None", where="r.identifier == 'none'") == 1

def test_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta is None", where="r.identifier == 'datetimedelta'") == 0

def test_datetimedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datetimedelta", where="r.identifier == 'none'") == 1

def test_datetimedelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == 0

def test_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta is None", where="r.identifier == 'none'") == 1

def test_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta is None", where="r.identifier == 'monthdelta'") == 0

def test_monthdelta3(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_monthdelta", where="r.identifier == 'none'") == 1

def test_monthdelta4(vsql_db, vsql_data):
	assert vsql_db.expr("None is r.v_monthdelta", where="r.identifier == 'monthdelta'") == 0

def test_geo1(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49, 11, 'Here') is None") == 0

def test_geo2(vsql_db, vsql_data):
	assert vsql_db.expr("None is geo(49, 11, 'Here')") == 0

def test_null1(vsql_db, vsql_data):
	# ``None is None`` would be constant-folded by UL4, but ``[None, None][0]``
	# is a non-constant expression of type ``NULL``, so the database really
	# executes the operator
	assert vsql_db.expr("[None, None][0] is None") == 1

def test_null2(vsql_db, vsql_data):
	# Not constant-folded (see ``test_null1``)
	assert vsql_db.expr("None is [None, None][0]") == 1

def test_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] is None") == 0

def test_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [None, None]") == 0

def test_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3] is None") == 0

def test_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [1, 2, 3]") == 0

def test_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3] is None") == 0

def test_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [1.1, 2.2, 3.3]") == 0

def test_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] is None") == 0

def test_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is ['gurk', 'hurz']") == 0

def test_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] is None", where="r.identifier == 'shortclob'") == 0

def test_cloblist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [r.v_clob]", where="r.identifier == 'shortclob'") == 0

def test_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] is None") == 0

def test_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [@(2000-02-29), @(2000-03-01)]") == 0

def test_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] is None") == 0

def test_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None is [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 0

def test_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("{1, 2, 3} is None") == 0

def test_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {1, 2, 3}") == 0

def test_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("{1.1, 2.2, 3.3} is None") == 0

def test_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {1.1, 2.2, 3.3}") == 0

def test_strset1(vsql_db, vsql_data):
	assert vsql_db.expr("{'gurk', 'hurz'} is None") == 0

def test_strset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {'gurk', 'hurz'}") == 0

def test_dateset1(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29), @(2000-03-01)} is None") == 0

def test_dateset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {@(2000-02-29), @(2000-03-01)}") == 0

def test_datetimeset1(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} is None") == 0

def test_datetimeset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}") == 0

def test_nullset1(vsql_db, vsql_data):
	assert vsql_db.expr("{None} is None") == 0

def test_nullset2(vsql_db, vsql_data):
	assert vsql_db.expr("None is {None}") == 0
