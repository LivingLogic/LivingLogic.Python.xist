"""
Tests for the vSQL binary operator ``and``.

To run the tests, :mod:`pytest` is required.
"""

import datetime


###
### Tests
###

def test_null_bool(vsql_db, vsql_data):
	assert vsql_db.expr("None and r.v_bool", where="r.identifier == 'bool_true'") is None


def test_bool_null(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool and None", where="r.identifier == 'bool_true'") is None


def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool and False", where="r.identifier == 'bool_true'") == 0


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool and True", where="r.identifier == 'bool_true'") == 1


def test_int_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int and 0", where="r.identifier == 'int'") == 0


def test_int_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int and 42", where="r.identifier == 'int'") == 42


def test_number_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number and 0.0", where="r.identifier == 'number'") == 0.0


def test_number_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number and 42.5", where="r.identifier == 'number'") == 42.5


def test_str_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str and 'gurk'", where="r.identifier == 'none'") is None


def test_str_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str and 'hurz'", where="r.identifier == 'str'") == "hurz"


def test_date_date1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date and @(2000-02-20)", where="r.identifier == 'none'") is None


def test_date_date2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date and @(2000-02-20)", where="r.identifier == 'date'") == vsql_db.type_for_date(2000, 2, 20)


def test_datetime_datetime1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime and @(2000-02-20T12:34:56)", where="r.identifier == 'none'") is None


def test_datetime_datetime2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime and @(2000-02-20T12:34:56)", where="r.identifier == 'datetime'") == datetime.datetime(2000, 2, 20, 12, 34, 56)


def test_datedelta_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta and days(10)", where="r.identifier == 'none'") is None


def test_datedelta_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta and days(10)", where="r.identifier == 'datedelta'") == vsql_db.type_for_datedelta(10)


def test_datetimedelta_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta and hours(12)", where="r.identifier == 'none'") is None


def test_datetimedelta_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta and hours(12)", where="r.identifier == 'datetimedelta'") == vsql_db.type_for_datetimedelta(0, 12 * 60 * 60)


def test_intlist_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("0*[1] and [4, 5, 6]") == []


def test_intlist_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3] and [4, 5, 6]") == [4, 5, 6]


def test_numberlist_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("0*[1.1] and [4.4, 5.5, 6.6]") == []


def test_numberlist_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3] and [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_nulllist_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] and [4, 5, 6]") == []


def test_nulllist_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] and [4, 5, 6]") == [4, 5, 6]


def test_nulllist_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] and [4.4, 5.5, 6.6]") == []


def test_nulllist_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] and [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_nulllist_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] and ['gurk', 'hurz']") == []


def test_nulllist_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] and ['gurk', 'hurz']") == ['gurk', 'hurz']


def test_nulllist_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] and [@(2000-02-29), @(2000-03-01)]") == []


def test_nulllist_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] and [@(2000-02-29), @(2000-03-01)]") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1)]


def test_nulllist_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] and [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == []


def test_nulllist_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] and [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 3, 1, 12, 34, 56)]


def test_intlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3] and []") == []


def test_intlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2, 3] and [None]") == [None]


def test_numberlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3] and []") == []


def test_numberlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2, 3.3] and [None]") == [None]


def test_strlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] and []") == []


def test_strlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] and [None]") == [None]


def test_datelist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] and []") == []


def test_datelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] and [None]") == [None]


def test_datetimelist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] and []") == []


def test_datetimelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] and [None]") == [None]