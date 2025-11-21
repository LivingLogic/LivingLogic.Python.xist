"""
Tests for the vSQL binary operator ``and``.

To run the tests, :mod:`pytest` is required.
"""

import datetime

from conftest import *


###
### Tests
###

def test_null_bool(db, vsql_data):
	assert expr(db, "None and r.v_bool", where="r.identifier == 'bool_true'") is None


def test_bool_null(db, vsql_data):
	assert expr(db, "r.v_bool and None", where="r.identifier == 'bool_true'") is None


def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool and False", where="r.identifier == 'bool_true'") == 0


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool and True", where="r.identifier == 'bool_true'") == 1


def test_int_int1(db, vsql_data):
	assert expr(db, "r.v_int and 0", where="r.identifier == 'int'") == 0


def test_int_int2(db, vsql_data):
	assert expr(db, "r.v_int and 42", where="r.identifier == 'int'") == 42


def test_number_number1(db, vsql_data):
	assert expr(db, "r.v_number and 0.0", where="r.identifier == 'number'") == 0.0


def test_number_number2(db, vsql_data):
	assert expr(db, "r.v_number and 42.5", where="r.identifier == 'number'") == 42.5


def test_str_str1(db, vsql_data):
	assert expr(db, "r.v_str and 'gurk'", where="r.identifier == 'none'") is None


def test_str_str2(db, vsql_data):
	assert expr(db, "r.v_str and 'hurz'", where="r.identifier == 'str'") == "hurz"


def test_date_date1(db, vsql_data):
	assert expr(db, "r.v_date and @(2000-02-20)", where="r.identifier == 'none'") is None


def test_date_date2(db, vsql_data):
	assert expr(db, "r.v_date and @(2000-02-20)", where="r.identifier == 'date'") == datetime.datetime(2000, 2, 20)


def test_datetime_datetime1(db, vsql_data):
	assert expr(db, "r.v_datetime and @(2000-02-20T12:34:56)", where="r.identifier == 'none'") is None


def test_datetime_datetime2(db, vsql_data):
	assert expr(db, "r.v_datetime and @(2000-02-20T12:34:56)", where="r.identifier == 'datetime'") == datetime.datetime(2000, 2, 20, 12, 34, 56)


def test_datedelta_datedelta1(db, vsql_data):
	assert expr(db, "r.v_datedelta and days(10)", where="r.identifier == 'none'") is None


def test_datedelta_datedelta2(db, vsql_data):
	assert expr(db, "r.v_datedelta and days(10)", where="r.identifier == 'datedelta'") == 10


def test_datetimedelta_datetimedelta1(db, vsql_data):
	assert expr(db, "r.v_datetimedelta and hours(12)", where="r.identifier == 'none'") is None


def test_datetimedelta_datetimedelta2(db, vsql_data):
	assert expr(db, "r.v_datetimedelta and hours(12)", where="r.identifier == 'datetimedelta'") == 0.5


def test_intlist_intlist1(db, vsql_data):
	assert expr(db, "0*[1] and [4, 5, 6]") == []


def test_intlist_intlist2(db, vsql_data):
	assert expr(db, "[1, 2, 3] and [4, 5, 6]") == [4, 5, 6]


def test_numberlist_numberlist1(db, vsql_data):
	assert expr(db, "0*[1.1] and [4.4, 5.5, 6.6]") == []


def test_numberlist_numberlist2(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] and [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_nulllist_intlist1(db, vsql_data):
	assert expr(db, "[] and [4, 5, 6]") == []


def test_nulllist_intlist2(db, vsql_data):
	assert expr(db, "[None] and [4, 5, 6]") == [4, 5, 6]


def test_nulllist_numberlist1(db, vsql_data):
	assert expr(db, "[] and [4.4, 5.5, 6.6]") == []


def test_nulllist_numberlist2(db, vsql_data):
	assert expr(db, "[None] and [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_nulllist_strlist1(db, vsql_data):
	assert expr(db, "[] and ['gurk', 'hurz']") == []


def test_nulllist_strlist2(db, vsql_data):
	assert expr(db, "[None] and ['gurk', 'hurz']") == ['gurk', 'hurz']


def test_nulllist_datelist1(db, vsql_data):
	assert expr(db, "[] and [@(2000-02-29), @(2000-03-01)]") == []


def test_nulllist_datelist2(db, vsql_data):
	assert expr(db, "[None] and [@(2000-02-29), @(2000-03-01)]") == [datetime.datetime(2000, 2, 29), datetime.datetime(2000, 3, 1)]


def test_nulllist_datetimelist1(db, vsql_data):
	assert expr(db, "[] and [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == []


def test_nulllist_datetimelist2(db, vsql_data):
	assert expr(db, "[None] and [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 3, 1, 12, 34, 56)]


def test_intlist_nulllist1(db, vsql_data):
	assert expr(db, "[1, 2, 3] and []") == []


def test_intlist_nulllist2(db, vsql_data):
	assert expr(db, "[1, 2, 3] and [None]") == [None]


def test_numberlist_nulllist1(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] and []") == []


def test_numberlist_nulllist2(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] and [None]") == [None]


def test_strlist_nulllist1(db, vsql_data):
	assert expr(db, "['gurk', 'hurz'] and []") == []


def test_strlist_nulllist2(db, vsql_data):
	assert expr(db, "['gurk', 'hurz'] and [None]") == [None]


def test_datelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] and []") == []


def test_datelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] and [None]") == [None]


def test_datetimelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] and []") == []


def test_datetimelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] and [None]") == [None]