"""
Tests for the vSQL binary operator ``or``.

To run the tests, :mod:`pytest` is required.
"""

import pytest

from conftest import *
import datetime

###
### Tests
###

d1 = datetime.datetime(2000, 2, 29)
d2 = datetime.datetime(2000, 3, 1)

dt1 = datetime.datetime(2000, 2, 29, 12, 34, 56)
dt2 = datetime.datetime(2000, 3, 1, 12, 34, 56)


def test_null_bool(db, vsql_data):
	assert expr(db, "None or r.v_bool", where="r.identifier == 'bool_true'") == True


def test_bool_null(db, vsql_data):
	assert expr(db, "r.v_bool or None", where="r.identifier == 'bool_true'") == True


def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool or False", where="r.identifier == 'bool_false'") == False


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool or False", where="r.identifier == 'bool_true'") == True


def test_int_int1(db, vsql_data):
	assert expr(db, "0 or r.v_int", where="r.identifier == 'int'") == 1776


def test_int_int2(db, vsql_data):
	assert expr(db, "42 or r.v_int", where="r.identifier == 'int'") == 42


def test_number_number1(db, vsql_data):
	assert expr(db, "0.0 or r.v_number", where="r.identifier == 'number'") == 42.5


def test_number_number2(db, vsql_data):
	assert expr(db, "17.25 or r.v_number", where="r.identifier == 'number'") == 17.25


def test_str_str1(db, vsql_data):
	assert expr(db, "'' or r.v_str", where="r.identifier == 'str'") == "gurk"


def test_str_str2(db, vsql_data):
	assert expr(db, "'hurz' or r.v_str", where="r.identifier == 'str'") == "hurz"


def test_clob_str1(db, vsql_data):
	assert expr(db, "r.v_clob or ''", where="r.identifier == 'clob'") == "gurk" * 100000


def test_str_clob1(db, vsql_data):
	assert expr(db, "'' or r.v_clob", where="r.identifier == 'clob'") == "gurk" * 100000


def test_clob_clob1(db, vsql_data):
	assert expr(db, "r.v_clob or r.v_clob", where="r.identifier == 'clob'") == "gurk" * 100000


def test_date_date1(db, vsql_data):
	assert expr(db, "@(2000-02-29) or r.v_date", where="r.identifier == 'none'") == d1


def test_date_date2(db, vsql_data):
	assert expr(db, "@(2000-02-29) or r.v_date", where="r.identifier == 'date'") == d1


def test_datetime_datetime1(db, vsql_data):
	assert expr(db, "r.v_datetime or @(2000-02-29T12:34:56)", where="r.identifier == 'none'") == dt1


def test_datetime_datetime2(db, vsql_data):
	assert expr(db, "r.v_datetime or @(2000-02-29T12:34:56)", where="r.identifier == 'datetime'") == dt1


def test_datedelta_datedelta1(db, vsql_data):
	assert expr(db, "r.v_datedelta or days(10)", where="r.identifier == 'none'") == 10


def test_datedelta_datedelta2(db, vsql_data):
	assert expr(db, "r.v_datedelta or days(10)", where="r.identifier == 'datedelta'") == 12


def test_datetimedelta_datetimedelta1(db, vsql_data):
	assert expr(db, "r.v_datetimedelta or hours(12)", where="r.identifier == 'none'") == 0.5


def test_datetimedelta_datetimedelta2(db, vsql_data):
	assert expr(db, "r.v_datetimedelta or hours(12)", where="r.identifier == 'datetimedelta'") == pytest.approx(1.5242592592592592)


def test_intlist_intlist1(db, vsql_data):
	assert expr(db, "0*[1] or [4, 5, 6]") == [4, 5, 6]


def test_intlist_intlist2(db, vsql_data):
	assert expr(db, "[1, 2, 3] or [4, 5, 6]") == [1, 2, 3]


def test_numberlist_numberlist1(db, vsql_data):
	assert expr(db, "0*[1.1] or [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_numberlist_numberlist2(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] or [4.4, 5.5, 6.6]") == [1.1, 2.2, 3.3]


def test_nulllist_intlist1(db, vsql_data):
	assert expr(db, "[] or [4, 5, 6]") == [4, 5, 6]


def test_nulllist_intlist2(db, vsql_data):
	assert expr(db, "[None] or [4, 5, 6]") == [None]


def test_nulllist_numberlist1(db, vsql_data):
	assert expr(db, "[] or [4.4, 5.5, 6.6]") == [4.4, 5.5, 6.6]


def test_nulllist_numberlist2(db, vsql_data):
	assert expr(db, "[None] or [4.4, 5.5, 6.6]") == [None]


def test_nulllist_strlist1(db, vsql_data):
	assert expr(db, "[] or ['gurk', 'hurz']") == ["gurk", "hurz"]


def test_nulllist_strlist2(db, vsql_data):
	assert expr(db, "[None] or ['gurk', 'hurz']") == [None]


def test_nulllist_cloblist1(db, vsql_data):
	assert expr(db, "[] or [r.v_clob, 'hurz']", where="r.identifier == 'clob'") == ["gurk" * 100000, "hurz"]


def test_nulllist_cloblist2(db, vsql_data):
	assert expr(db, "[None] or [r.v_clob, 'hurz']", where="r.identifier == 'clob'") == [None]


def test_nulllist_datelist1(db, vsql_data):
	assert expr(db, "[] or [@(2000-02-29), @(2000-03-01)]") == [d1, d2]


def test_nulllist_datelist2(db, vsql_data):
	assert expr(db, "[None] or [@(2000-02-29), @(2000-03-01)]") == [None]


def test_nulllist_datetimelist1(db, vsql_data):
	assert expr(db, "[] or [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == [dt1, dt2]


def test_nulllist_datetimelist2(db, vsql_data):
	assert expr(db, "[None] or [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == [None]


def test_intlist_nulllist1(db, vsql_data):
	assert expr(db, "[1, 2, 3] or []") == [1, 2, 3]


def test_intlist_nulllist2(db, vsql_data):
	assert expr(db, "[1, 2, 3] or [None]") == [1, 2, 3]


def test_numberlist_nulllist1(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] or []") == [1.1, 2.2, 3.3]


def test_numberlist_nulllist2(db, vsql_data):
	assert expr(db, "[1.1, 2.2, 3.3] or [None]") == [1.1, 2.2, 3.3]


def test_strlist_nulllist1(db, vsql_data):
	assert expr(db, "['gurk', 'hurz'] or []") == ['gurk', 'hurz']


def test_strlist_nulllist2(db, vsql_data):
	assert expr(db, "['gurk', 'hurz'] or [None]") == ['gurk', 'hurz']


def test_cloblist_nulllist1(db, vsql_data):
	assert expr(db, "[r.v_clob, 'hurz'] or []", where="r.identifier == 'clob'") == ["gurk" * 100000, "hurz"]


def test_cloblist_nulllist2(db, vsql_data):
	assert expr(db, "[r.v_clob, 'hurz'] or [None]", where="r.identifier == 'clob'") == ["gurk" * 100000, "hurz"]


def test_datelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] or []") == [d1, d2]


def test_datelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] or [None]") == [d1, d2]


def test_datetimelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] or []") == [dt1, dt2]


def test_datetimelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] or [None]") == [dt1, dt2]