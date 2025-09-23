"""
Tests for vSQL functions.

To run the tests, :mod:`pytest` is required.
"""

import math, datetime

from conftest import *


###
### Tests
###

def test_today(db, vsql_data):
	assert expr(db, "today()") >= datetime.datetime(2000, 2, 29)


def test_now(db, vsql_data):
	assert expr(db, "now()") >= datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_bool(db, vsql_data):
	assert expr(db, "bool()") == False


def test_bool_none(db, vsql_data):
	assert expr(db, "bool(None)") == False


def test_bool_false(db, vsql_data):
	assert expr(db, "bool(False)") == False


def test_bool_true(db, vsql_data):
	assert expr(db, "bool(True)") == True


def test_bool_int_none(db, vsql_data):
	assert expr(db, "bool(r.v_int)", where="r.identifier == 'none'") == False


def test_bool_int_false(db, vsql_data):
	assert expr(db, "bool(0)") == False


def test_bool_int_true(db, vsql_data):
	assert expr(db, "bool(42)") == True


def test_bool_number_false(db, vsql_data):
	assert expr(db, "bool(0.0)") == False


def test_bool_number_true(db, vsql_data):
	assert expr(db, "bool(42.5)") == True


def test_bool_datedelta_false(db, vsql_data):
	assert expr(db, "bool(days(0))") == False


def test_bool_datedelta_true(db, vsql_data):
	assert expr(db, "bool(days(42))") == True


def test_bool_datetimedelta_false(db, vsql_data):
	assert expr(db, "bool(minutes(0))") == False


def test_bool_datetimedelta_true(db, vsql_data):
	assert expr(db, "bool(minutes(42))") == True


def test_bool_monthdelta_false(db, vsql_data):
	assert expr(db, "bool(monthdelta(0))") == False


def test_bool_monthdelta_true(db, vsql_data):
	assert expr(db, "bool(monthdelta(42))") == True


def test_bool_date(db, vsql_data):
	assert expr(db, "bool(@(2000-02-29))") == True


def test_bool_datetime(db, vsql_data):
	assert expr(db, "bool(@(2000-02-29T12:34:56))") == True


def test_bool_color(db, vsql_data):
	assert expr(db, "bool(#fff)") == True


def test_bool_str_false(db, vsql_data):
	assert expr(db, "bool('')") == False


def test_bool_str_true(db, vsql_data):
	assert expr(db, "bool('gurk')") == True


def test_bool_intlist(db, vsql_data):
	assert expr(db, "bool([42])") == True


def test_bool_numberlist(db, vsql_data):
	assert expr(db, "bool([42.5])") == True


def test_bool_strlist(db, vsql_data):
	assert expr(db, "bool(['gurk'])") == True


def test_bool_datelist(db, vsql_data):
	assert expr(db, "bool([today()])") == True


def test_bool_datetimelist(db, vsql_data):
	assert expr(db, "bool([now()])") == True


def test_bool_intset(db, vsql_data):
	assert expr(db, "bool({42})") == True


def test_bool_numberset(db, vsql_data):
	assert expr(db, "bool({42.5})") == True


def test_bool_strset(db, vsql_data):
	assert expr(db, "bool({'gurk'})") == True


def test_bool_dateset(db, vsql_data):
	assert expr(db, "bool({today()})") == True


def test_bool_datetimeset(db, vsql_data):
	assert expr(db, "bool({now()})") == True


def test_int(db, vsql_data):
	assert expr(db, "int()") == False


def test_int_bool_false(db, vsql_data):
	assert expr(db, "int(False)") == False


def test_int_bool_true(db, vsql_data):
	assert expr(db, "int(True)") == 1


def test_int_int(db, vsql_data):
	assert expr(db, "int(42)") == 42


def test_int_number(db, vsql_data):
	assert expr(db, "int(42.4)") == 42


def test_int_str_ok(db, vsql_data):
	assert expr(db, "int('42')") == 42


def test_int_str_bad(db, vsql_data):
	assert expr(db, "int('42.5')") is None


def test_int_str_very_bad(db, vsql_data):
	assert expr(db, "int('verybad')") is None


def test_float(db, vsql_data):
	assert expr(db, "float()") == 0.0


def test_float_bool_false(db, vsql_data):
	assert expr(db, "float(False)") == 0.0


def test_float_bool_true(db, vsql_data):
	assert expr(db, "float(True)") == 1.0


def test_float_int(db, vsql_data):
	assert expr(db, "float(42)") == 42.0


def test_float_number(db, vsql_data):
	assert expr(db, "float(42.5)") == 42.5


def test_float_str(db, vsql_data):
	assert expr(db, "float('42.5')") == 42.5


def test_float_str_bad(db, vsql_data):
	assert expr(db, "float('bad')") is None


def test_str(db, vsql_data):
	assert expr(db, "str()") is None


def test_str_bool_false(db, vsql_data):
	assert expr(db, "str(False)") == "False"


def test_str_bool_true(db, vsql_data):
	assert expr(db, "str(True)") == "True"


def test_str_int(db, vsql_data):
	assert expr(db, "str(-42)") == "-42"


def test_str_number1(db, vsql_data):
	assert expr(db, "str(42.0)") == "42.0"

def test_str_number2(db, vsql_data):
	assert expr(db, "str(-42.5)") == "-42.5"


def test_str_str(db, vsql_data):
	assert expr(db, "str('foo')") == "foo"


def test_str_date(db, vsql_data):
	assert expr(db, "str(@(2000-02-29))") == "2000-02-29"


def test_str_datetime(db, vsql_data):
	assert expr(db, "str(@(2000-02-29T12:34:56))") == "2000-02-29 12:34:56"


def test_str_datedelta_1(db, vsql_data):
	assert expr(db, "str(days(1))") == "1 day"


def test_str_datedelta_2(db, vsql_data):
	assert expr(db, "str(days(42))") == "42 days"


def test_str_datetimedelta_1(db, vsql_data):
	assert expr(db, "str(seconds(42))") == "0:00:42"


def test_str_datetimedelta_2(db, vsql_data):
	assert expr(db, "str(minutes(42))") == "0:42:00"


def test_str_datetimedelta_3(db, vsql_data):
	assert expr(db, "str(hours(17) + minutes(23))") == "17:23:00"


def test_str_datetimedelta_4(db, vsql_data):
	assert expr(db, "str(hours(42) + seconds(0))") == "1 day, 18:00:00"


def test_str_datetimedelta_5(db, vsql_data):
	assert expr(db, "str(days(42) + seconds(0))") == "42 days, 0:00:00"


def test_str_datetimedelta_6(db, vsql_data):
	assert expr(db, "str(days(42) + hours(17) + minutes(23))") == "42 days, 17:23:00"


def test_str_datetimedelta_7(db, vsql_data):
	assert expr(db, "str(-days(1) - hours(12) - minutes(34) - seconds(56))") == "-2 days, 11:25:04"


def test_str_monthdelta_1(db, vsql_data):
	assert expr(db, "str(monthdelta(0))") == "0 months"


def test_str_monthdelta_2(db, vsql_data):
	assert expr(db, "str(monthdelta(1))") == "1 month"


def test_str_monthdelta_3(db, vsql_data):
	assert expr(db, "str(monthdelta(42))") == "42 months"


def test_str_color_1(db, vsql_data):
	assert expr(db, "str(#000f)") == "#000"


def test_str_color_2(db, vsql_data):
	assert expr(db, "str(#fff0)") == "rgba(255, 255, 255, 0.000)"


def test_str_color_3(db, vsql_data):
	assert expr(db, "str(#123456)") == "#123456"


def test_str_color_4(db, vsql_data):
	assert expr(db, "str(#12345678)") == "rgba(18, 52, 86, 0.471)"


def test_str_geo_without_info(db, vsql_data):
	assert expr(db, "str(geo(49.95, 11.59))") == "<geo lat=49.95 long=11.59 info=None>"


def test_str_geo_with_info(db, vsql_data):
	assert expr(db, "str(geo(49.95, 11.59, 'Here'))") == "<geo lat=49.95 long=11.59 info='Here'>"


def test_str_intlist(db, vsql_data):
	assert expr(db, "str([1, 2, 3, None])") == "[1, 2, 3, None]"


def test_str_numberlist(db, vsql_data):
	assert expr(db, "str([1.2, 3.4, 5.6, None])") == "[1.2, 3.4, 5.6, None]"


def test_str_strlist(db, vsql_data):
	assert expr(db, "str(['foo', 'bar', None])") == "['foo', 'bar', None]"


def test_str_datelist(db, vsql_data):
	assert expr(db, "str([@(2000-02-29), None])") == "[@(2000-02-29), None]"


def test_str_datetimelist(db, vsql_data):
	assert expr(db, "str([@(2000-02-29T12:34:56), None])") == "[@(2000-02-29T12:34:56), None]"


# For the set test only include one non-``None`` value,
# as the order of the other elements is undefined

def test_str_intset(db, vsql_data):
	assert expr(db, "str({1, None})") == "{1, None}"


def test_str_numberset(db, vsql_data):
	assert expr(db, "str({1.2, None})") == "{1.2, None}"


def test_str_strset(db, vsql_data):
	assert expr(db, "str({'foo', None})") == "{'foo', None}"


def test_str_dateset(db, vsql_data):
	assert expr(db, "str({@(2000-02-29), None})") == "{@(2000-02-29), None}"


def test_str_datetimeset(db, vsql_data):
	assert expr(db, "str({@(2000-02-29T12:34:56), None})") == "{@(2000-02-29T12:34:56), None}"


def test_repr_none(db, vsql_data):
	assert expr(db, "repr(None)") == "None"


def test_repr_bool_false(db, vsql_data):
	assert expr(db, "repr(False)") == "False"


def test_repr_bool_True(db, vsql_data):
	assert expr(db, "repr(True)") == "True"


def test_repr_int(db, vsql_data):
	assert expr(db, "repr(-42)") == "-42"


def test_repr_number_1(db, vsql_data):
	assert expr(db, "repr(42.0)") == "42.0"


def test_repr_number_2(db, vsql_data):
	assert expr(db, "repr(-42.5)") == "-42.5"


def test_repr_str(db, vsql_data):
	assert expr(db, "repr('foo\"bar')") == "'foo\"bar'"


def test_repr_date(db, vsql_data):
	assert expr(db, "repr(@(2000-02-29))") == "@(2000-02-29)"


def test_repr_datetime(db, vsql_data):
	assert expr(db, "repr(@(2000-02-29T12:34:56))") == "@(2000-02-29T12:34:56)"


def test_repr_datedelta_1(db, vsql_data):
	assert expr(db, "repr(days(1))") == "timedelta(1)"


def test_repr_datedelta_2(db, vsql_data):
	assert expr(db, "repr(days(42))") == "timedelta(42)"


def test_repr_datetimedelta_1(db, vsql_data):
	# FIXME: Oracle doesn't have enough precision for seconds
	assert expr(db, "repr(seconds(42))") == "timedelta(0, 42)"


def test_repr_datetimedelta_2(db, vsql_data):
	assert expr(db, "repr(minutes(42))") == "timedelta(0, 2520)"


def test_repr_datetimedelta_3(db, vsql_data):
	assert expr(db, "repr(hours(17) + minutes(23))") == "timedelta(0, 62580)"


def test_repr_datetimedelta_4(db, vsql_data):
	assert expr(db, "repr(hours(42) + seconds(0))") == "timedelta(1, 64800)"


def test_repr_datetimedelta_5(db, vsql_data):
	assert expr(db, "repr(days(42) + seconds(0))") == "timedelta(42)"


def test_repr_datetimedelta_6(db, vsql_data):
	assert expr(db, "repr(days(42) + hours(17) + minutes(23))") == "timedelta(42, 62580)"


def test_repr_monthdelta(db, vsql_data):
	assert expr(db, "repr(monthdelta(42))") == "monthdelta(42)"


def test_repr_color_1(db, vsql_data):
	assert expr(db, "repr(#000)") == "#000"


def test_repr_color_2(db, vsql_data):
	assert expr(db, "repr(#369c)") == "#369c"


def test_repr_color_3(db, vsql_data):
	assert expr(db, "repr(#123456)") == "#123456"


def test_repr_color_4(db, vsql_data):
	assert expr(db, "repr(#12345678)") == "#12345678"


def test_repr_geo_without_info(db, vsql_data):
	assert expr(db, "repr(geo(49.95, 11.59))") == "<geo lat=49.95 long=11.59 info=None>"


def test_repr_geo_with_info(db, vsql_data):
	assert expr(db, "repr(geo(49.95, 11.59, 'Here'))") == "<geo lat=49.95 long=11.59 info='Here'>"


def test_repr_intlist(db, vsql_data):
	assert expr(db, "repr([1, 2, 3, None])") == "[1, 2, 3, None]"


def test_repr_numberlist(db, vsql_data):
	assert expr(db, "repr([1.2, 3.4, 5.6, None])") == "[1.2, 3.4, 5.6, None]"


def test_repr_strlist(db, vsql_data):
	assert expr(db, "repr(['foo', 'bar', None])") == "['foo', 'bar', None]"


def test_repr_datelist(db, vsql_data):
	assert expr(db, "repr([@(2000-02-29), None])") == "[@(2000-02-29), None]"


def test_repr_datetimelist(db, vsql_data):
	assert expr(db, "repr([@(2000-02-29T12:34:56), None])") == "[@(2000-02-29T12:34:56), None]"


# For the set test only include one non-``None`` value,
# as the order of the other elements is undefined

def test_repr_intset(db, vsql_data):
	assert expr(db, "repr({1, None})") == "{1, None}"


def test_repr_numberset(db, vsql_data):
	assert expr(db, "repr({1.2, None})") == "{1.2, None}"


def test_repr_strset(db, vsql_data):
	assert expr(db, "repr({'foo', None})") == "{'foo', None}"


def test_repr_dateset(db, vsql_data):
	assert expr(db, "repr({@(2000-02-29), None})") == "{@(2000-02-29), None}"


def test_repr_datetimeset(db, vsql_data):
	assert expr(db, "repr({@(2000-02-29T12:34:56), None})") == "{@(2000-02-29T12:34:56), None}"


def test_date_int(db, vsql_data):
	assert expr(db, "date(2000, 2, 29)") == datetime.datetime(2000, 2, 29)


def test_date_datetime(db, vsql_data):
	assert expr(db, "date(@(2000-02-29T12:34:56))") == datetime.datetime(2000, 2, 29)


def test_datetime_int3(db, vsql_data):
	assert expr(db, "datetime(2000, 2, 29)") == datetime.datetime(2000, 2, 29)


def test_datetime_int4(db, vsql_data):
	assert expr(db, "datetime(2000, 2, 29, 12)") == datetime.datetime(2000, 2, 29, 12)


def test_datetime_int5(db, vsql_data):
	assert expr(db, "datetime(2000, 2, 29, 12, 34)") == datetime.datetime(2000, 2, 29, 12, 34)


def test_datetime_int6(db, vsql_data):
	assert expr(db, "datetime(2000, 2, 29, 12, 34, 56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_datetime_date(db, vsql_data):
	assert expr(db, "datetime(@(2000-02-29))") == datetime.datetime(2000, 2, 29)


def test_datetime_date_int1(db, vsql_data):
	assert expr(db, "datetime(@(2000-02-29), 12)") == datetime.datetime(2000, 2, 29, 12)


def test_datetime_date_int2(db, vsql_data):
	assert expr(db, "datetime(@(2000-02-29), 12, 34)") == datetime.datetime(2000, 2, 29, 12, 34)


def test_datetime_date_int3(db, vsql_data):
	assert expr(db, "datetime(@(2000-02-29), 12, 34, 56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_len_str1(db, vsql_data):
	assert expr(db, "len('')") == 0


def test_len_str2(db, vsql_data):
	assert expr(db, "len('gurk')") == 4


def test_len_str3(db, vsql_data):
	assert expr(db, "len('\\t\\n')") == 2


def test_len_intlist(db, vsql_data):
	assert expr(db, "len([1, 2, 3])") == 3


def test_len_numberlist(db, vsql_data):
	assert expr(db, "len([1.2, 3.4, 5.6])") == 3


def test_len_strlist(db, vsql_data):
	assert expr(db, "len(['foo', 'bar', 'baz'])") == 3


def test_len_datelist(db, vsql_data):
	assert expr(db, "len([@(2000-02-29), @(2000-02-29), @(2000-03-01)])") == 3


def test_len_datetimelist(db, vsql_data):
	assert expr(db, "len([@(2000-02-29T12:34:56), @(2000-02-29T12:34:56), @(2000-03-01T12:34:56)])") == 3


def test_len_intset(db, vsql_data):
	assert expr(db, "len({1, 1, 2, 2, 3, 3, None, None})") == 4


def test_len_numberset(db, vsql_data):
	assert expr(db, "len({1.2, 3.4, 5.6, None, 1.2, 3.4, 5.6, None})") == 4


def test_len_strset(db, vsql_data):
	assert expr(db, "len({'foo', 'bar', 'baz', None, 'foo', 'bar', 'baz'})") == 4


def test_len_dateset(db, vsql_data):
	assert expr(db, "len({@(2000-02-29), @(2000-02-29), @(2000-03-21), None})") == 3


def test_len_datetimeset(db, vsql_data):
	assert expr(db, "len({@(2000-02-29T12:34:56), None, @(2000-02-29T12:34:56), None, @(2000-02-29T11:22:33)})") == 3


def test_timedelta(db, vsql_data):
	assert expr(db, "timedelta()") == False


def test_timedelta_int1(db, vsql_data):
	assert expr(db, "timedelta(42)") == 42


def test_timedelta_int2(db, vsql_data):
	assert expr(db, "timedelta(42, 12)") == 42 + 12/24/60/60


def test_monthdelta(db, vsql_data):
	assert expr(db, "monthdelta()") == 0


def test_monthdelta_int(db, vsql_data):
	assert expr(db, "monthdelta(42)") == 42


def test_years(db, vsql_data):
	assert expr(db, "years(25)") == 25 * 12


def test_months(db, vsql_data):
	assert expr(db, "months(3)") == 3


def test_weeks(db, vsql_data):
	assert expr(db, "weeks(3)") == 3 * 7


def test_days(db, vsql_data):
	assert expr(db, "days(12)") == 12


def test_hours(db, vsql_data):
	assert expr(db, "hours(8)") == 8/24


def test_minutes(db, vsql_data):
	assert expr(db, "minutes(45)") == 45/24/60


def test_seconds(db, vsql_data):
	assert expr(db, "seconds(60)") == pytest.approx(60/24/60/60)


def test_md5(db, vsql_data):
	assert expr(db, "md5('gurk')") == "4b5b6a3fa4af2541daa569277c7ff4c5"


def test_random(db, vsql_data):
	assert 1.0 <= expr(db, "random() + 1") <= 2.0


def test_randrange(db, vsql_data):
	assert 0 <= expr(db, "randrange(1, 10)") < 10


def test_seq(db, vsql_data):
	assert expr(db, "seq()")


def test_rgb1(db, vsql_data):
	assert expr(db, "rgb(0.2, 0.4, 0.6)") == 0x336699ff


def test_rgb2(db, vsql_data):
	assert expr(db, "rgb(0.2, 0.4, 0.6, 0.8)") == 0x336699cc


def test_list_str(db, vsql_data):
	assert expr(db, "list('gurk')") == ["g", "u", "r", "k"]


def test_list_intlist(db, vsql_data):
	assert expr(db, "list([1, 2, 3])") == [1, 2, 3]


def test_list_numberlist(db, vsql_data):
	assert expr(db, "list([1.2, 3.4, 5.6])") == [1.2, 3.4, 5.6]


def test_list_strlist(db, vsql_data):
	assert expr(db, "list(['foo', 'bar', 'baz', None])") == ["foo", "bar", "baz", None]


def test_list_datelist(db, vsql_data):
	assert expr(db, "list([@(2000-02-29), @(2000-03-01), None])") == [datetime.datetime(2000, 2, 29), datetime.datetime(2000, 3, 1), None]


def test_list_datetimelist(db, vsql_data):
	assert expr(db, "list([@(2000-02-29T12:34:56), @(2000-02-29T11:22:33), None])") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 11, 22, 33), None]


def test_list_intset(db, vsql_data):
	assert expr(db, "list({1, None})") == [1, None]


def test_list_numberset(db, vsql_data):
	assert expr(db, "list({1.2, None})") == [1.2, None]


def test_list_strset(db, vsql_data):
	assert expr(db, "list({'foo', None})") == ['foo', None]


def test_list_dateset(db, vsql_data):
	assert expr(db, "list({@(2000-02-29), None})") == [datetime.datetime(2000, 2, 29), None]


def test_list_datetimeset(db, vsql_data):
	assert expr(db, "list({@(2000-02-29T12:34:56), None})") == [datetime.datetime(2000, 2, 29, 12, 34, 56), None]


def test_set_str(db, vsql_data):
	assert set(expr(db, "set('mississippi')")) == {"i", "m", "p", "s"}


def test_set_intlist(db, vsql_data):
	assert set(expr(db, "set([1, 2, 3, 2, 1, None])")) == {1, 2, 3, None}


def test_set_numberlist(db, vsql_data):
	assert set(expr(db, "set([1.2, 3.4, 5.6, 3.4, 1.2, None])")) == {1.2, 3.4, 5.6, None}


def test_set_strlist(db, vsql_data):
	assert set(expr(db, "set(['foo', 'bar', 'baz', None, 'baz', 'bar', 'foo'])")) == {"foo", "bar", "baz", None}


def test_set_datelist(db, vsql_data):
	assert set(expr(db, "set([@(2000-02-29), @(2000-03-01), None, @(2000-03-01), @(2000-02-29)])")) == {datetime.datetime(2000, 2, 29), datetime.datetime(2000, 3, 1), None}


def test_set_datetimelist(db, vsql_data):
	assert set(expr(db, "set([@(2000-02-29T12:34:56), @(2000-02-29T11:22:33), @(2000-02-29T11:22:33), None, @(2000-02-29T12:34:56)])")) == {datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 11, 22, 33), None}


def test_set_intset(db, vsql_data):
	assert set(expr(db, "set({1, None})")) == {1, None}


def test_set_numberset(db, vsql_data):
	assert set(expr(db, "set({1.2, None})")) == {1.2, None}


def test_set_strset(db, vsql_data):
	assert set(expr(db, "set({'foo', None})")) == {'foo', None}


def test_set_dateset(db, vsql_data):
	assert set(expr(db, "set({@(2000-02-29), None})")) == {datetime.datetime(2000, 2, 29), None}


def test_set_datetimeset(db, vsql_data):
	assert set(expr(db, "set({@(2000-02-29T12:34:56), None})")) == {datetime.datetime(2000, 2, 29, 12, 34, 56), None}


def test_dist(db, vsql_data):
	assert abs(expr(db, "dist(geo(49.95, 11.59, 'Here'), geo(12.34, 56.67, 'There'))")) - 5845.77551787602 < 1e-5


def test_abs(db, vsql_data):
	assert expr(db, "abs(-42)") == 42


def test_cos_bool(db, vsql_data):
	assert expr(db, "cos(False)") == 1.0


def test_cos_int(db, vsql_data):
	assert expr(db, "cos(0)") == 1.0


def test_cos_number1(db, vsql_data):
	assert expr(db, "cos(0.0)") == 1.0


def test_cos_number2(db, vsql_data):
	assert abs(expr(db, f"cos({math.pi} / 2)")) < 1e-10


def test_cos_number3(db, vsql_data):
	assert abs(expr(db, f"cos({math.pi})") + 1) < 1e-10


def test_sin_bool(db, vsql_data):
	assert expr(db, "sin(False)") == 0.0


def test_sin_int(db, vsql_data):
	assert expr(db, "sin(0)") == 0.0


def test_sin_number1(db, vsql_data):
	assert expr(db, "sin(0.0)") == 0.0


def test_sin_number2(db, vsql_data):
	assert abs(expr(db, f"sin({math.pi} / 2)") - 1) < 1e-10


def test_sin_number3(db, vsql_data):
	assert abs(expr(db, f"sin({math.pi})")) < 1e-10


def test_tan_bool(db, vsql_data):
	assert expr(db, "tan(False)") == 0.0


def test_tan_int(db, vsql_data):
	assert expr(db, "tan(0)") == 0.0


def test_tan_number1(db, vsql_data):
	assert expr(db, "tan(0.0)") == 0.0


def test_tan_number2(db, vsql_data):
	assert abs(expr(db, f"tan(0.25 * {math.pi})") - 1) < 1e-10


def test_tan_number3(db, vsql_data):
	assert abs(expr(db, f"tan(0.75 * {math.pi})") + 1) < 1e-10


def test_sqrt_bool1(db, vsql_data):
	assert expr(db, "sqrt(False)") == 0.0


def test_sqrt_bool2(db, vsql_data):
	assert expr(db, "sqrt(True)") == 1.0


def test_sqrt_int1(db, vsql_data):
	assert expr(db, "sqrt(16)") == 4.0


def test_sqrt_int2(db, vsql_data):
	assert expr(db, "sqrt(-16)") is None


def test_sqrt_number1(db, vsql_data):
	assert expr(db, "sqrt(16.0)") == 4.0


def test_sqrt_number2(db, vsql_data):
	assert expr(db, "sqrt(-16.0)") is None
