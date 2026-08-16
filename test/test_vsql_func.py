"""
Tests for vSQL functions.

To run the tests, :mod:`pytest` is required.
"""

import itertools, math, datetime

import pytest


###
### Tests
###

def test_today(vsql_db, vsql_data):
	assert vsql_db.expr("today()") >= vsql_db.type_for_date(2000, 2, 29)


def test_now(vsql_db, vsql_data):
	assert vsql_db.expr("now()") >= datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_bool(vsql_db, vsql_data):
	assert vsql_db.expr("bool()") == False


def test_bool_none(vsql_db, vsql_data):
	assert vsql_db.expr("bool(None)") == False


def test_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(False)") == False


def test_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(True)") == True


def test_bool_int_none(vsql_db, vsql_data):
	assert vsql_db.expr("bool(r.v_int)", where="r.identifier == 'none'") == False


def test_bool_int_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(0)") == False


def test_bool_int_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(42)") == True


def test_bool_number_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(0.0)") == False


def test_bool_number_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(42.5)") == True


def test_bool_datedelta_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(days(0))") == False


def test_bool_datedelta_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(days(42))") == True


def test_bool_datetimedelta_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(minutes(0))") == False


def test_bool_datetimedelta_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(minutes(42))") == True


def test_bool_monthdelta_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool(monthdelta(0))") == False


def test_bool_monthdelta_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool(monthdelta(42))") == True


def test_bool_date(vsql_db, vsql_data):
	assert vsql_db.expr("bool(@(2000-02-29))") == True


def test_bool_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("bool(@(2000-02-29T12:34:56))") == True


def test_bool_color(vsql_db, vsql_data):
	assert vsql_db.expr("bool(#fff)") == True


def test_bool_str_false(vsql_db, vsql_data):
	assert vsql_db.expr("bool('')") == False


def test_bool_str_true(vsql_db, vsql_data):
	assert vsql_db.expr("bool('gurk')") == True


def test_bool_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("bool([42])") == True


def test_bool_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("bool([42.5])") == True


def test_bool_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("bool(['gurk'])") == True


def test_bool_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("bool([today()])") == True


def test_bool_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("bool([now()])") == True


def test_bool_intset(vsql_db, vsql_data):
	assert vsql_db.expr("bool({42})") == True


def test_bool_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("bool({42.5})") == True


def test_bool_strset(vsql_db, vsql_data):
	assert vsql_db.expr("bool({'gurk'})") == True


def test_bool_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("bool({today()})") == True


def test_bool_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("bool({now()})") == True


def test_int(vsql_db, vsql_data):
	assert vsql_db.expr("int()") == False


def test_int_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("int(False)") == False


def test_int_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("int(True)") == 1


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("int(42)") == 42


def test_int_number(vsql_db, vsql_data):
	assert vsql_db.expr("int(42.4)") == 42


def test_int_str_ok(vsql_db, vsql_data):
	assert vsql_db.expr("int('42')") == 42


def test_int_str_bad(vsql_db, vsql_data):
	assert vsql_db.expr("int('42.5')") is None


def test_int_str_very_bad(vsql_db, vsql_data):
	assert vsql_db.expr("int('verybad')") is None


def test_float(vsql_db, vsql_data):
	assert vsql_db.expr("float()") == 0.0


def test_float_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("float(False)") == 0.0


def test_float_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("float(True)") == 1.0


def test_float_int(vsql_db, vsql_data):
	assert vsql_db.expr("float(42)") == 42.0


def test_float_number(vsql_db, vsql_data):
	assert vsql_db.expr("float(42.5)") == 42.5


def test_float_str(vsql_db, vsql_data):
	assert vsql_db.expr("float('42.5')") == 42.5


def test_float_str_bad(vsql_db, vsql_data):
	assert vsql_db.expr("float('bad')") is None


def test_str(vsql_db, vsql_data):
	assert vsql_db.expr("str()") is None


def test_str_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("str(False)") == "False"


def test_str_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("str(True)") == "True"


def test_str_int(vsql_db, vsql_data):
	assert vsql_db.expr("str(-42)") == "-42"


def test_str_number1(vsql_db, vsql_data):
	assert vsql_db.expr("str(42.0)") == "42.0"

def test_str_number2(vsql_db, vsql_data):
	assert vsql_db.expr("str(-42.5)") == "-42.5"


def test_str_str(vsql_db, vsql_data):
	assert vsql_db.expr("str('foo')") == "foo"


def test_str_date(vsql_db, vsql_data):
	assert vsql_db.expr("str(@(2000-02-29))") == "2000-02-29"


def test_str_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("str(@(2000-02-29T12:34:56))") == "2000-02-29 12:34:56"


def test_str_datedelta_1(vsql_db, vsql_data):
	assert vsql_db.expr("str(days(1))") == "1 day"


def test_str_datedelta_2(vsql_db, vsql_data):
	assert vsql_db.expr("str(days(42))") == "42 days"


def test_str_datetimedelta_1(vsql_db, vsql_data):
	assert vsql_db.expr("str(seconds(42))") == "0:00:42"


def test_str_datetimedelta_2(vsql_db, vsql_data):
	assert vsql_db.expr("str(minutes(42))") == "0:42:00"


def test_str_datetimedelta_3(vsql_db, vsql_data):
	assert vsql_db.expr("str(hours(17) + minutes(23))") == "17:23:00"


def test_str_datetimedelta_4(vsql_db, vsql_data):
	assert vsql_db.expr("str(hours(42) + seconds(0))") == "1 day, 18:00:00"


def test_str_datetimedelta_5(vsql_db, vsql_data):
	assert vsql_db.expr("str(days(42) + seconds(0))") == "42 days, 0:00:00"


def test_str_datetimedelta_6(vsql_db, vsql_data):
	assert vsql_db.expr("str(days(42) + hours(17) + minutes(23))") == "42 days, 17:23:00"


def test_str_datetimedelta_7(vsql_db, vsql_data):
	assert vsql_db.expr("str(-days(1) - hours(12) - minutes(34) - seconds(56))") == "-2 days, 11:25:04"


def test_str_monthdelta_1(vsql_db, vsql_data):
	assert vsql_db.expr("str(monthdelta(0))") == "0 months"


def test_str_monthdelta_2(vsql_db, vsql_data):
	assert vsql_db.expr("str(monthdelta(1))") == "1 month"


def test_str_monthdelta_3(vsql_db, vsql_data):
	assert vsql_db.expr("str(monthdelta(42))") == "42 months"


def test_str_color_1(vsql_db, vsql_data):
	assert vsql_db.expr("str(#000f)") == "#000"


def test_str_color_2(vsql_db, vsql_data):
	assert vsql_db.expr("str(#fff0)") == "rgba(255, 255, 255, 0.000)"


def test_str_color_3(vsql_db, vsql_data):
	assert vsql_db.expr("str(#123456)") == "#123456"


def test_str_color_4(vsql_db, vsql_data):
	assert vsql_db.expr("str(#12345678)") == "rgba(18, 52, 86, 0.471)"


def test_str_geo_without_info(vsql_db, vsql_data):
	assert vsql_db.expr("str(geo(49.95, 11.59))") == "<geo lat=49.95 long=11.59 info=None>"


def test_str_geo_with_info(vsql_db, vsql_data):
	assert vsql_db.expr("str(geo(49.95, 11.59, 'Here'))") == "<geo lat=49.95 long=11.59 info='Here'>"


def test_str_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("str([1, 2, 3, None])") == "[1, 2, 3, None]"


def test_str_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("str([1.2, 3.4, 5.6, None])") == "[1.2, 3.4, 5.6, None]"


def test_str_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("str(['foo', 'bar', None])") == "['foo', 'bar', None]"


def test_str_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("str([@(2000-02-29), None])") == "[@(2000-02-29), None]"


def test_str_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("str([@(2000-02-29T12:34:56), None])") == "[@(2000-02-29T12:34:56), None]"


# For the set test only include one non-``None`` value,
# as the order of the other elements is undefined

def test_str_intset(vsql_db, vsql_data):
	assert vsql_db.expr("str({1, None})") == "{1, None}"


def test_str_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("str({1.2, None})") == "{1.2, None}"


def test_str_strset(vsql_db, vsql_data):
	assert vsql_db.expr("str({'foo', None})") == "{'foo', None}"


def test_str_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("str({@(2000-02-29), None})") == "{@(2000-02-29), None}"


def test_str_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("str({@(2000-02-29T12:34:56), None})") == "{@(2000-02-29T12:34:56), None}"


def test_repr_none(vsql_db, vsql_data):
	assert vsql_db.expr("repr(None)") == "None"


def test_repr_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("repr(False)") == "False"


def test_repr_bool_True(vsql_db, vsql_data):
	assert vsql_db.expr("repr(True)") == "True"


def test_repr_int(vsql_db, vsql_data):
	assert vsql_db.expr("repr(-42)") == "-42"


def test_repr_number_1(vsql_db, vsql_data):
	assert vsql_db.expr("repr(42.0)") == "42.0"


def test_repr_number_2(vsql_db, vsql_data):
	assert vsql_db.expr("repr(-42.5)") == "-42.5"


def test_repr_str(vsql_db, vsql_data):
	assert vsql_db.expr("repr('foo\"bar')") == "'foo\"bar'"


def test_repr_date(vsql_db, vsql_data):
	assert vsql_db.expr("repr(@(2000-02-29))") == "@(2000-02-29)"


def test_repr_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("repr(@(2000-02-29T12:34:56))") == "@(2000-02-29T12:34:56)"


def test_repr_datedelta_1(vsql_db, vsql_data):
	assert vsql_db.expr("repr(days(1))") == "timedelta(1)"


def test_repr_datedelta_2(vsql_db, vsql_data):
	assert vsql_db.expr("repr(days(42))") == "timedelta(42)"


def test_repr_datetimedelta_1(vsql_db, vsql_data):
	# FIXME: Oracle doesn't have enough precision for seconds
	assert vsql_db.expr("repr(seconds(42))") == "timedelta(0, 42)"


def test_repr_datetimedelta_2(vsql_db, vsql_data):
	assert vsql_db.expr("repr(minutes(42))") == "timedelta(0, 2520)"


def test_repr_datetimedelta_3(vsql_db, vsql_data):
	assert vsql_db.expr("repr(hours(17) + minutes(23))") == "timedelta(0, 62580)"


def test_repr_datetimedelta_4(vsql_db, vsql_data):
	assert vsql_db.expr("repr(hours(42) + seconds(0))") == "timedelta(1, 64800)"


def test_repr_datetimedelta_5(vsql_db, vsql_data):
	assert vsql_db.expr("repr(days(42) + seconds(0))") == "timedelta(42)"


def test_repr_datetimedelta_6(vsql_db, vsql_data):
	assert vsql_db.expr("repr(days(42) + hours(17) + minutes(23))") == "timedelta(42, 62580)"


def test_repr_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("repr(monthdelta(42))") == "monthdelta(42)"


def test_repr_color_1(vsql_db, vsql_data):
	assert vsql_db.expr("repr(#000)") == "#000"


def test_repr_color_2(vsql_db, vsql_data):
	assert vsql_db.expr("repr(#369c)") == "#369c"


def test_repr_color_3(vsql_db, vsql_data):
	assert vsql_db.expr("repr(#123456)") == "#123456"


def test_repr_color_4(vsql_db, vsql_data):
	assert vsql_db.expr("repr(#12345678)") == "#12345678"


def test_repr_geo_without_info(vsql_db, vsql_data):
	assert vsql_db.expr("repr(geo(49.95, 11.59))") == "<geo lat=49.95 long=11.59 info=None>"


def test_repr_geo_with_info(vsql_db, vsql_data):
	assert vsql_db.expr("repr(geo(49.95, 11.59, 'Here'))") == "<geo lat=49.95 long=11.59 info='Here'>"


def test_repr_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([1, 2, 3, None])") == "[1, 2, 3, None]"


def test_repr_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([1.2, 3.4, 5.6, None])") == "[1.2, 3.4, 5.6, None]"


def test_repr_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("repr(['foo', 'bar', None])") == "['foo', 'bar', None]"


def test_repr_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([@(2000-02-29), None])") == "[@(2000-02-29), None]"


def test_repr_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([@(2000-02-29T12:34:56), None])") == "[@(2000-02-29T12:34:56), None]"


# For the set test only include one non-``None`` value,
# as the order of the other elements is undefined

def test_repr_intset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({1, None})") == "{1, None}"


def test_repr_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({1.2, None})") == "{1.2, None}"


def test_repr_strset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({'foo', None})") == "{'foo', None}"


def test_repr_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({@(2000-02-29), None})") == "{@(2000-02-29), None}"


def test_repr_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({@(2000-02-29T12:34:56), None})") == "{@(2000-02-29T12:34:56), None}"


def test_date_int(vsql_db, vsql_data):
	assert vsql_db.expr("date(2000, 2, 29)") == vsql_db.type_for_date(2000, 2, 29)


def test_date_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("date(@(2000-02-29T12:34:56))") == vsql_db.type_for_date(2000, 2, 29)


def test_datetime_int3(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(2000, 2, 29)") == datetime.datetime(2000, 2, 29)


def test_datetime_int4(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(2000, 2, 29, 12)") == datetime.datetime(2000, 2, 29, 12)


def test_datetime_int5(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(2000, 2, 29, 12, 34)") == datetime.datetime(2000, 2, 29, 12, 34)


def test_datetime_int6(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(2000, 2, 29, 12, 34, 56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_datetime_date(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(@(2000-02-29))") == datetime.datetime(2000, 2, 29)


def test_datetime_date_int1(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(@(2000-02-29), 12)") == datetime.datetime(2000, 2, 29, 12)


def test_datetime_date_int2(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(@(2000-02-29), 12, 34)") == datetime.datetime(2000, 2, 29, 12, 34)


def test_datetime_date_int3(vsql_db, vsql_data):
	assert vsql_db.expr("datetime(@(2000-02-29), 12, 34, 56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_len_str1(vsql_db, vsql_data):
	assert vsql_db.expr("len('')") == 0


def test_len_str2(vsql_db, vsql_data):
	assert vsql_db.expr("len('gurk')") == 4


def test_len_str3(vsql_db, vsql_data):
	assert vsql_db.expr("len('\\t\\n')") == 2


def test_len_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("len([1, 2, 3])") == 3


def test_len_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("len([1.2, 3.4, 5.6])") == 3


def test_len_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("len(['foo', 'bar', 'baz'])") == 3


def test_len_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("len([@(2000-02-29), @(2000-02-29), @(2000-03-01)])") == 3


def test_len_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("len([@(2000-02-29T12:34:56), @(2000-02-29T12:34:56), @(2000-03-01T12:34:56)])") == 3


def test_len_intset(vsql_db, vsql_data):
	assert vsql_db.expr("len({1, 1, 2, 2, 3, 3, None, None})") == 4


def test_len_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("len({1.2, 3.4, 5.6, None, 1.2, 3.4, 5.6, None})") == 4


def test_len_strset(vsql_db, vsql_data):
	assert vsql_db.expr("len({'foo', 'bar', 'baz', None, 'foo', 'bar', 'baz'})") == 4


def test_len_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("len({@(2000-02-29), @(2000-02-29), @(2000-03-21), None})") == 3


def test_len_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("len({@(2000-02-29T12:34:56), None, @(2000-02-29T12:34:56), None, @(2000-02-29T11:22:33)})") == 3


def test_timedelta(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta()") == vsql_db.type_for_datedelta(0)


def test_timedelta_int1(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(42)") == vsql_db.type_for_datedelta(42)


def test_timedelta_int2(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(42, 12)") == vsql_db.type_for_datetimedelta(42, 12)


def test_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("monthdelta()") == vsql_db.type_for_monthdelta(0)


def test_monthdelta_int(vsql_db, vsql_data):
	assert vsql_db.expr("monthdelta(42)") == vsql_db.type_for_monthdelta(42)


def test_years(vsql_db, vsql_data):
	assert vsql_db.expr("years(25)") == vsql_db.type_for_monthdelta(25 * 12)


def test_months(vsql_db, vsql_data):
	assert vsql_db.expr("months(3)") == vsql_db.type_for_monthdelta(3)


def test_weeks(vsql_db, vsql_data):
	assert vsql_db.expr("weeks(3)") == vsql_db.type_for_datedelta(3 * 7)


def test_days(vsql_db, vsql_data):
	assert vsql_db.expr("days(12)") == vsql_db.type_for_datedelta(12)


def test_hours(vsql_db, vsql_data):
	assert vsql_db.expr("hours(8)") == vsql_db.type_for_datetimedelta(0, 8 * 60 * 60)


def test_minutes(vsql_db, vsql_data):
	assert vsql_db.expr("minutes(45)") == vsql_db.type_for_datetimedelta(0, 45 * 60)


def test_seconds(vsql_db, vsql_data):
	assert vsql_db.expr("seconds(60)") == vsql_db.type_for_datetimedelta(0, 60)


def test_md5(vsql_db, vsql_data):
	assert vsql_db.expr("md5('gurk')") == "4b5b6a3fa4af2541daa569277c7ff4c5"


def test_random(vsql_db, vsql_data):
	assert 1.0 <= vsql_db.expr("random() + 1") <= 2.0


def test_randrange(vsql_db, vsql_data):
	assert 0 <= vsql_db.expr("randrange(1, 10)") < 10


def test_seq(vsql_db, vsql_data):
	assert vsql_db.expr("seq()")


def test_rgb1(vsql_db, vsql_data):
	assert vsql_db.expr("rgb(0.2, 0.4, 0.6)") == 0x336699ff


def test_rgb2(vsql_db, vsql_data):
	assert vsql_db.expr("rgb(0.2, 0.4, 0.6, 0.8)") == 0x336699cc


def test_list_str(vsql_db, vsql_data):
	assert vsql_db.expr("list('gurk')") == ["g", "u", "r", "k"]


def test_list_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("list([1, 2, 3])") == [1, 2, 3]


def test_list_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("list([1.2, 3.4, 5.6])") == [1.2, 3.4, 5.6]


def test_list_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("list(['foo', 'bar', 'baz', None])") == ["foo", "bar", "baz", None]


def test_list_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("list([@(2000-02-29), @(2000-03-01), None])") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1), None]


def test_list_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("list([@(2000-02-29T12:34:56), @(2000-02-29T11:22:33), None])") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 11, 22, 33), None]


def test_list_intset(vsql_db, vsql_data):
	assert vsql_db.expr("list({1, None})") == [1, None]


def test_list_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("list({1.2, None})") == [1.2, None]


def test_list_strset(vsql_db, vsql_data):
	assert vsql_db.expr("list({'foo', None})") == ['foo', None]


def test_list_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("list({@(2000-02-29), None})") == [vsql_db.type_for_date(2000, 2, 29), None]


def test_list_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("list({@(2000-02-29T12:34:56), None})") == [datetime.datetime(2000, 2, 29, 12, 34, 56), None]


def test_set_str(vsql_db, vsql_data):
	assert set(vsql_db.expr("set('mississippi')")) == {"i", "m", "p", "s"}


def test_set_intlist(vsql_db, vsql_data):
	assert set(vsql_db.expr("set([1, 2, 3, 2, 1, None])")) == {1, 2, 3, None}


def test_set_numberlist(vsql_db, vsql_data):
	assert set(vsql_db.expr("set([1.2, 3.4, 5.6, 3.4, 1.2, None])")) == {1.2, 3.4, 5.6, None}


def test_set_strlist(vsql_db, vsql_data):
	assert set(vsql_db.expr("set(['foo', 'bar', 'baz', None, 'baz', 'bar', 'foo'])")) == {"foo", "bar", "baz", None}


def test_set_datelist(vsql_db, vsql_data):
	assert set(vsql_db.expr("set([@(2000-02-29), @(2000-03-01), None, @(2000-03-01), @(2000-02-29)])")) == {vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1), None}


def test_set_datetimelist(vsql_db, vsql_data):
	assert set(vsql_db.expr("set([@(2000-02-29T12:34:56), @(2000-02-29T11:22:33), @(2000-02-29T11:22:33), None, @(2000-02-29T12:34:56)])")) == {datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 11, 22, 33), None}


def test_set_intset(vsql_db, vsql_data):
	assert set(vsql_db.expr("set({1, None})")) == {1, None}


def test_set_numberset(vsql_db, vsql_data):
	assert set(vsql_db.expr("set({1.2, None})")) == {1.2, None}


def test_set_strset(vsql_db, vsql_data):
	assert set(vsql_db.expr("set({'foo', None})")) == {'foo', None}


def test_set_dateset(vsql_db, vsql_data):
	assert set(vsql_db.expr("set({@(2000-02-29), None})")) == {vsql_db.type_for_date(2000, 2, 29), None}


def test_set_datetimeset(vsql_db, vsql_data):
	assert set(vsql_db.expr("set({@(2000-02-29T12:34:56), None})")) == {datetime.datetime(2000, 2, 29, 12, 34, 56), None}


def test_dist(vsql_db, vsql_data):
	assert abs(vsql_db.expr("dist(geo(49.95, 11.59, 'Here'), geo(12.34, 56.67, 'There'))")) - 5845.77551787602 < 1e-5


def test_abs_bool(vsql_db, vsql_data):
	assert vsql_db.expr("abs(False)") == 0


def test_abs_int(vsql_db, vsql_data):
	assert vsql_db.expr("abs(-42)") == 42


def test_abs_number(vsql_db, vsql_data):
	assert vsql_db.expr("abs(-42.5)") == 42.5


def test_cos_bool(vsql_db, vsql_data):
	assert vsql_db.expr("cos(False)") == 1.0


def test_cos_int(vsql_db, vsql_data):
	assert vsql_db.expr("cos(0)") == 1.0


def test_cos_number1(vsql_db, vsql_data):
	assert vsql_db.expr("cos(0.0)") == 1.0


def test_cos_number2(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"cos({math.pi} / 2)")) < 1e-10


def test_cos_number3(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"cos({math.pi})") + 1) < 1e-10


def test_sin_bool(vsql_db, vsql_data):
	assert vsql_db.expr("sin(False)") == 0.0


def test_sin_int(vsql_db, vsql_data):
	assert vsql_db.expr("sin(0)") == 0.0


def test_sin_number1(vsql_db, vsql_data):
	assert vsql_db.expr("sin(0.0)") == 0.0


def test_sin_number2(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"sin({math.pi} / 2)") - 1) < 1e-10


def test_sin_number3(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"sin({math.pi})")) < 1e-10


def test_tan_bool(vsql_db, vsql_data):
	assert vsql_db.expr("tan(False)") == 0.0


def test_tan_int(vsql_db, vsql_data):
	assert vsql_db.expr("tan(0)") == 0.0


def test_tan_number1(vsql_db, vsql_data):
	assert vsql_db.expr("tan(0.0)") == 0.0


def test_tan_number2(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"tan(0.25 * {math.pi})") - 1) < 1e-10


def test_tan_number3(vsql_db, vsql_data):
	assert abs(vsql_db.expr(f"tan(0.75 * {math.pi})") + 1) < 1e-10


def test_sqrt_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(False)") == 0.0


def test_sqrt_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(True)") == 1.0


def test_sqrt_int1(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(16)") == 4.0


def test_sqrt_int2(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(-16)") is None


def test_sqrt_number1(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(16.0)") == 4.0


def test_sqrt_number2(vsql_db, vsql_data):
	assert vsql_db.expr("sqrt(-16.0)") is None


def test_bool_geo(vsql_db, vsql_data):
	assert vsql_db.expr("bool(geo(49, 11, 'Here'))") == True


def test_bool_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("bool(r.v_clob)", where="r.identifier == 'none'") == False


def test_bool_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("bool(r.v_clob)", where="r.identifier == 'shortclob'") == True


def test_bool_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("bool([])") == False


def test_bool_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("bool([None, None])") == True


def test_bool_nullset1(vsql_db, vsql_data):
	assert vsql_db.expr("bool({/})") == False


def test_bool_nullset2(vsql_db, vsql_data):
	assert vsql_db.expr("bool({None})") == True


def test_bool_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("bool([r.v_clob])", where="r.identifier == 'shortclob'") == True


def test_int_clob(vsql_db, vsql_data):
	assert vsql_db.expr("int(('42' + r.v_clob)[0:2])", where="r.identifier == 'shortclob'") == 42


def test_float_clob(vsql_db, vsql_data):
	assert vsql_db.expr("float(('4.5' + r.v_clob)[0:3])", where="r.identifier == 'shortclob'") == 4.5


def test_str_null(vsql_db, vsql_data):
	assert vsql_db.expr("str(None)") is None


def test_str_clob(vsql_db, vsql_data):
	assert vsql_db.expr("str(r.v_clob)", where="r.identifier == 'shortclob'") == "gurk"


def test_str_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("str([None, None])") == "[None, None]"


def test_str_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("str([r.v_clob])", where="r.identifier == 'shortclob'") == "['gurk']"


def test_str_nullset(vsql_db, vsql_data):
	assert vsql_db.expr("str({None})") == "{None}"


def test_repr_clob(vsql_db, vsql_data):
	assert vsql_db.expr("repr(r.v_clob)", where="r.identifier == 'shortclob'") == "'gurk'"


def test_repr_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([r.v_clob])", where="r.identifier == 'shortclob'") == "['gurk']"


def test_repr_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("repr([None, None])") == "[None, None]"


def test_repr_nullset(vsql_db, vsql_data):
	assert vsql_db.expr("repr({None})") == "{None}"


def test_len_clob(vsql_db, vsql_data):
	assert vsql_db.expr("len(r.v_clob)", where="r.identifier == 'shortclob'") == 4


def test_len_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("len([None, None])") == 2


def test_len_nullset(vsql_db, vsql_data):
	assert vsql_db.expr("len({None})") == 1


def test_len_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("len([r.v_clob])", where="r.identifier == 'shortclob'") == 1


def test_list_clob(vsql_db, vsql_data):
	assert vsql_db.expr("list(r.v_clob)", where="r.identifier == 'shortclob'") == ["g", "u", "r", "k"]


def test_list_nulllist(vsql_db, vsql_data):
	# A ``NULLLIST`` result is returned as the number of its elements
	assert vsql_db.expr("list([None, None])") == 2


def test_list_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("list([r.v_clob])", where="r.identifier == 'shortclob'") == ["gurk"]


def test_list_nullset(vsql_db, vsql_data):
	# A ``NULLLIST`` result is returned as the number of its elements
	assert vsql_db.expr("list({None})") == 1


def test_set_clob(vsql_db, vsql_data):
	assert set(vsql_db.expr("set(r.v_clob)", where="r.identifier == 'shortclob'")) == {"g", "u", "r", "k"}


def test_set_nulllist(vsql_db, vsql_data):
	# A ``NULLSET`` result is returned as the number of its elements
	assert vsql_db.expr("set([None, None])") == 1


# ``rgb()`` and ``geo()`` accept every combination of ``BOOL``/``INT``/
# ``NUMBER`` for their numeric arguments. Since testing each of those type
# combinations individually would be excessive, the following tests are
# parametrized with all combinations instead.

_rgb_args = dict(bool=("True", 255), int=("1", 255), number=("0.5", 128))

@pytest.mark.parametrize("types", [t for n in (3, 4) for t in itertools.product(sorted(_rgb_args), repeat=n)], ids="_".join)
def test_rgb_all_type_combinations(vsql_db, vsql_data, types):
	expr = f"rgb({', '.join(_rgb_args[t][0] for t in types)})"
	expected = 0
	for t in types:
		expected = expected * 256 + _rgb_args[t][1]
	if len(types) == 3:
		expected = expected * 256 + 255
	assert vsql_db.expr(expr) == expected


_geo_args = dict(bool=("True", 1), int=("49", 49), number=("49.5", 49.5))
_geo_combos = list(itertools.product(sorted(_geo_args), repeat=2))

@pytest.mark.parametrize("types", _geo_combos + [t + ("str",) for t in _geo_combos], ids="_".join)
def test_geo_all_type_combinations(vsql_db, vsql_data, types):
	args = [_geo_args[t][0] for t in types[:2]]
	if len(types) == 3:
		args.append("'Here'")
	expr = f"geo({', '.join(args)})"
	assert vsql_db.expr(f"{expr}.lat") == _geo_args[types[0]][1]
	assert vsql_db.expr(f"{expr}.long") == _geo_args[types[1]][1]
