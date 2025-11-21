"""
Tests for the vSQL "greater than" comparison operator ``>``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import expr


###
### Tests
###

def test_bool_none1(db, vsql_data):
	assert not expr(db, "r.v_bool > None", where="r.identifier == 'none'")


def test_bool_none2(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_false'") is None


def test_bool_none3(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_true'") is None


def test_int_none1(db, vsql_data):
	assert not expr(db, "r.v_int > None", where="r.identifier == 'none'")


def test_int_none2(db, vsql_data):
	assert expr(db, "r.v_int > None", where="r.identifier == 'int'") is None


def test_number_none1(db, vsql_data):
	assert not expr(db, "r.v_number > None", where="r.identifier == 'none'")


def test_number_none2(db, vsql_data):
	assert expr(db, "r.v_number > None", where="r.identifier == 'number'") is None


def test_str_none1(db, vsql_data):
	assert not expr(db, "r.v_str > None", where="r.identifier == 'none'")


def test_str_none2(db, vsql_data):
	assert expr(db, "r.v_str > None", where="r.identifier == 'str'") is None


def test_date_none1(db, vsql_data):
	assert not expr(db, "r.v_date > None", where="r.identifier == 'none'")


def test_date_none2(db, vsql_data):
	assert expr(db, "r.v_date > None", where="r.identifier == 'date'") is None


def test_datetime_none1(db, vsql_data):
	assert not expr(db, "r.v_datetime > None", where="r.identifier == 'none'")


def test_datetime_none2(db, vsql_data):
	assert expr(db, "r.v_datetime > None", where="r.identifier == 'datetime'") is None


def test_color_none1(db, vsql_data):
	assert not expr(db, "r.v_color > None", where="r.identifier == 'none'")


def test_color_none2(db, vsql_data):
	assert expr(db, "r.v_color > None", where="r.identifier == 'color'") is None


def test_datedelta_none1(db, vsql_data):
	assert not expr(db, "r.v_datedelta > None", where="r.identifier == 'none'")


def test_datedelta_none2(db, vsql_data):
	assert expr(db, "r.v_datedelta > None", where="r.identifier == 'datedelta'") is None


def test_datetimedelta_none1(db, vsql_data):
	assert not expr(db, "r.v_datetimedelta > None", where="r.identifier == 'none'")


def test_datetimedelta_none2(db, vsql_data):
	assert expr(db, "r.v_datetimedelta > None", where="r.identifier == 'datetimedelta'") is None


def test_monthdelta_none1(db, vsql_data):
	assert not expr(db, "r.v_monthdelta > None", where="r.identifier == 'none'")


def test_monthdelta_none2(db, vsql_data):
	assert expr(db, "r.v_monthdelta > None", where="r.identifier == 'monthdelta'") is None


def test_intlist_none(db, vsql_data):
	assert expr(db, "[1, 2] > None") is None


def test_numberlist_none(db, vsql_data):
	assert expr(db, "[1.2, 3.4] > None") is None


def test_strlist_none(db, vsql_data):
	assert expr(db, "['foo', 'bar'] > None") is None


def test_datelist_none(db, vsql_data):
	assert expr(db, "[@(2000-02-29)] > None") is None


def test_datetimelist_none(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56)] > None") is None


def test_none_bool1(db, vsql_data):
	assert not expr(db, "None > r.v_bool", where="r.identifier == 'none'")


def test_none_bool2(db, vsql_data):
	assert expr(db, "None > r.v_bool", where="r.identifier == 'bool_false'") is None


def test_none_bool3(db, vsql_data):
	assert expr(db, "None > r.v_bool", where="r.identifier == 'bool_true'") is None


def test_none_int1(db, vsql_data):
	assert not expr(db, "None > r.v_int", where="r.identifier == 'none'")


def test_none_int2(db, vsql_data):
	assert expr(db, "None > r.v_int", where="r.identifier == 'int'") is None


def test_none_number1(db, vsql_data):
	assert not expr(db, "None > r.v_number", where="r.identifier == 'none'")


def test_none_number2(db, vsql_data):
	assert expr(db, "None > r.v_number", where="r.identifier == 'number'") is None


def test_none_str1(db, vsql_data):
	assert not expr(db, "None > r.v_str", where="r.identifier == 'none'")


def test_none_str2(db, vsql_data):
	assert expr(db, "None > r.v_str", where="r.identifier == 'str'") is None


def test_none_date1(db, vsql_data):
	assert not expr(db, "None > r.v_date", where="r.identifier == 'none'")


def test_none_date2(db, vsql_data):
	assert expr(db, "None > r.v_date", where="r.identifier == 'date'") is None


def test_none_datetime1(db, vsql_data):
	assert not expr(db, "None > r.v_datetime", where="r.identifier == 'none'")


def test_none_datetime2(db, vsql_data):
	assert expr(db, "None > r.v_datetime", where="r.identifier == 'datetime'") is None


def test_none_color1(db, vsql_data):
	assert not expr(db, "None > r.v_color", where="r.identifier == 'none'")


def test_none_color2(db, vsql_data):
	assert expr(db, "None > r.v_color", where="r.identifier == 'color'") is None


def test_none_datedelta1(db, vsql_data):
	assert not expr(db, "None > r.v_datedelta", where="r.identifier == 'none'")


def test_none_datedelta2(db, vsql_data):
	assert expr(db, "None > r.v_datedelta", where="r.identifier == 'datedelta'") is None


def test_none_datetimedelta1(db, vsql_data):
	assert not expr(db, "None > r.v_datetimedelta", where="r.identifier == 'none'")


def test_none_datetimedelta2(db, vsql_data):
	assert expr(db, "None > r.v_datetimedelta", where="r.identifier == 'datetimedelta'") is None


def test_none_monthdelta1(db, vsql_data):
	assert not expr(db, "None > r.v_monthdelta", where="r.identifier == 'none'")


def test_none_monthdelta2(db, vsql_data):
	assert expr(db, "None > r.v_monthdelta", where="r.identifier == 'monthdelta'") is None


def test_none_intlist(db, vsql_data):
	assert expr(db, "None > [1, 2]") is None


def test_none_numberlist(db, vsql_data):
	assert expr(db, "None > [1.2, 3.4]") is None


def test_none_strlist(db, vsql_data):
	assert expr(db, "None > ['foo', 'bar']") is None


def test_none_datelist(db, vsql_data):
	assert expr(db, "None > [@(2000-02-29)]") is None


def test_none_datetimelist(db, vsql_data):
	assert expr(db, "None > [@(2000-02-29T12:34:56)]") is None


def test_bool_bool1(db, vsql_data):
	assert not expr(db, "r.v_bool > None", where="r.identifier == 'none'")


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool > False", where="r.identifier == 'none'") is None


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool > True", where="r.identifier == 'none'") is None


def test_bool_bool4(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_false'") is None


def test_bool_bool5(db, vsql_data):
	assert not expr(db, "r.v_bool > False", where="r.identifier == 'bool_false'")


def test_bool_bool6(db, vsql_data):
	assert not expr(db, "r.v_bool > True", where="r.identifier == 'bool_false'")


def test_bool_bool7(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_true'") is None


def test_bool_bool8(db, vsql_data):
	assert expr(db, "r.v_bool > False", where="r.identifier == 'bool_true'")


def test_bool_bool9(db, vsql_data):
	assert not expr(db, "r.v_bool > True", where="r.identifier == 'bool_true'")


def test_bool_int1(db, vsql_data):
	assert not expr(db, "r.v_bool > None", where="r.identifier == 'none'")


def test_bool_int2(db, vsql_data):
	assert expr(db, "r.v_bool > -1", where="r.identifier == 'none'") is None


def test_bool_int3(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_false'") is None


def test_bool_int4(db, vsql_data):
	assert not expr(db, "r.v_bool > 0", where="r.identifier == 'bool_false'")


def test_bool_int5(db, vsql_data):
	assert not expr(db, "r.v_bool > 1", where="r.identifier == 'bool_false'")


def test_bool_int6(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_true'") is None


def test_bool_int7(db, vsql_data):
	assert expr(db, "r.v_bool > 0", where="r.identifier == 'bool_true'")


def test_bool_int8(db, vsql_data):
	assert not expr(db, "r.v_bool > 1", where="r.identifier == 'bool_true'")


def test_bool_number1(db, vsql_data):
	assert not expr(db, "r.v_bool > None", where="r.identifier == 'none'")


def test_bool_number2(db, vsql_data):
	assert expr(db, "r.v_bool > -1.0", where="r.identifier == 'none'") is None


def test_bool_number3(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_false'") is None


def test_bool_number4(db, vsql_data):
	assert not expr(db, "r.v_bool > 0.0", where="r.identifier == 'bool_false'")


def test_bool_number5(db, vsql_data):
	assert not expr(db, "r.v_bool > 1.0", where="r.identifier == 'bool_false'")


def test_bool_number6(db, vsql_data):
	assert expr(db, "r.v_bool > None", where="r.identifier == 'bool_true'") is None


def test_bool_number7(db, vsql_data):
	assert expr(db, "r.v_bool > 0.0", where="r.identifier == 'bool_true'")


def test_bool_number8(db, vsql_data):
	assert not expr(db, "r.v_bool > 1.0", where="r.identifier == 'bool_true'")


def test_int_bool1(db, vsql_data):
	assert not expr(db, "r.v_int > None", where="r.identifier == 'none'")


def test_int_bool2(db, vsql_data):
	assert expr(db, "r.v_int > False", where="r.identifier == 'none'") is None


def test_int_bool3(db, vsql_data):
	assert expr(db, "r.v_int > True", where="r.identifier == 'none'") is None


def test_int_bool4(db, vsql_data):
	assert expr(db, "r.v_int > None", where="r.identifier == 'int'") is None


def test_int_bool5(db, vsql_data):
	assert expr(db, "r.v_int > False", where="r.identifier == 'int'")


def test_int_bool6(db, vsql_data):
	assert expr(db, "r.v_int > True", where="r.identifier == 'int'")


def test_int_bool7(db, vsql_data):
	assert expr(db, "-r.v_int > None", where="r.identifier == 'int'") is None


def test_int_bool8(db, vsql_data):
	assert not expr(db, "-r.v_int > False", where="r.identifier == 'int'")


def test_int_bool9(db, vsql_data):
	assert not expr(db, "-r.v_int > True", where="r.identifier == 'int'")


def test_int_int1(db, vsql_data):
	assert not expr(db, "r.v_int > None", where="r.identifier == 'none'")


def test_int_int2(db, vsql_data):
	assert expr(db, "r.v_int > 1", where="r.identifier == 'none'") is None


def test_int_int3(db, vsql_data):
	assert expr(db, "r.v_int > 1775", where="r.identifier == 'int'")


def test_int_int4(db, vsql_data):
	assert not expr(db, "r.v_int > 1777", where="r.identifier == 'int'")


def test_int_int5(db, vsql_data):
	assert expr(db, "1777 > r.v_int", where="r.identifier == 'int'")


def test_number_bool1(db, vsql_data):
	assert not expr(db, "r.v_number > None", where="r.identifier == 'none'")


def test_number_bool2(db, vsql_data):
	assert expr(db, "r.v_number > False", where="r.identifier == 'none'") is None


def test_number_bool3(db, vsql_data):
	assert expr(db, "r.v_number > True", where="r.identifier == 'number'")


def test_number_bool4(db, vsql_data):
	assert not expr(db, "-r.v_number > True", where="r.identifier == 'number'")


def test_number_int1(db, vsql_data):
	assert not expr(db, "r.v_number > None", where="r.identifier == 'none'")


def test_number_int2(db, vsql_data):
	assert expr(db, "r.v_number > 1", where="r.identifier == 'none'") is None


def test_number_int3(db, vsql_data):
	assert expr(db, "r.v_number > 1", where="r.identifier == 'number'")


def test_number_int4(db, vsql_data):
	assert not expr(db, "r.v_number > 73", where="r.identifier == 'number'")


def test_number_number1(db, vsql_data):
	assert not expr(db, "r.v_number > None", where="r.identifier == 'none'")


def test_number_number2(db, vsql_data):
	assert expr(db, "r.v_number > 1.0", where="r.identifier == 'none'") is None


def test_number_number3(db, vsql_data):
	assert expr(db, "r.v_number > 1.0", where="r.identifier == 'number'")


def test_number_number4(db, vsql_data):
	assert not expr(db, "r.v_number > 73.0", where="r.identifier == 'number'")


def test_str_str(db, vsql_data):
	assert expr(db, "r.v_str > 'abc'", where="r.identifier == 'str'")


def test_date_date(db, vsql_data):
	assert expr(db, "r.v_date > @(2000-02-28)", where="r.identifier == 'date'")


def test_datetime_datetime(db, vsql_data):
	assert expr(db, "r.v_datetime > @(2000-02-28T23:59:59)", where="r.identifier == 'datetime'")


def test_datedelta_datedelta(db, vsql_data):
	assert expr(db, "days(2) > days(1)")


def test_datetimedelta_datetimedelta(db, vsql_data):
	assert expr(db, "hours(2) > hours(1)")


def test_intlist_intlist1(db, vsql_data):
	assert expr(db, "[1, 2] > [1]")


def test_intlist_intlist2(db, vsql_data):
	assert expr(db, "[1, 3] > [1, 2]")


def test_intlist_intlist3(db, vsql_data):
	assert not expr(db, "[1] > [1, 2]")


def test_intlist_intlist4(db, vsql_data):
	assert not expr(db, "[1, 2] > [1, 2]")


def test_numberlist_numberlist1(db, vsql_data):
	assert expr(db, "[1.5, 2.5] > [1.5]")


def test_numberlist_numberlist2(db, vsql_data):
	assert expr(db, "[1.5, 3.5] > [1.5, 2.5]")


def test_numberlist_numberlist3(db, vsql_data):
	assert not expr(db, "[1.5] > [1.5, 2.5]")


def test_numberlist_numberlist4(db, vsql_data):
	assert not expr(db, "[1.5, 2.5] > [1.5, 2.5]")


def test_strlist_strlist1(db, vsql_data):
	assert expr(db, "['foo', 'bar'] > ['foo']")


def test_strlist_strlist2(db, vsql_data):
	assert expr(db, "['foo', 'baz'] > ['foo', 'bar']")


def test_strlist_strlist3(db, vsql_data):
	assert not expr(db, "['foo'] > ['foo', 'bar']")


def test_strlist_strlist4(db, vsql_data):
	assert not expr(db, "['foo', 'bar'] > ['foo', 'bar']")


def test_datelist_datelist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] > [@(2000-02-29)]")


def test_datelist_datelist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-02)] > [@(2000-02-29), @(2000-03-01)]")


def test_datelist_datelist3(db, vsql_data):
	assert not expr(db, "[@(2000-02-29)] > [@(2000-02-29), @(2000-03-01)]")


def test_datelist_datelist4(db, vsql_data):
	assert not expr(db, "[@(2000-02-29), @(2000-03-01)] > [@(2000-02-29), @(2000-03-01)]")


def test_datetimelist_datetimelist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] > [@(2000-02-29T12:34:56)]")


def test_datetimelist_datetimelist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-02T12:34:56)] > [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist3(db, vsql_data):
	assert not expr(db, "[@(2000-02-29T12:34:56)] > [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist4(db, vsql_data):
	assert not expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] > [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_nulllist_nulllist1(db, vsql_data):
	assert not expr(db, "[] > []")


def test_nulllist_nulllist2(db, vsql_data):
	assert expr(db, "[None, None] > []")


def test_nulllist_nulllist3(db, vsql_data):
	assert not expr(db, "[] > [None, None]")


def test_nulllist_intlist1(db, vsql_data):
	assert not expr(db, "[] > [1]")


def test_nulllist_intlist2(db, vsql_data):
	assert expr(db, "[None] > [1]") is None


def test_nulllist_intlist3(db, vsql_data):
	assert expr(db, "[None, None] > [1]") is None


def test_nulllist_numberlist1(db, vsql_data):
	assert not expr(db, "[] > [1.1]")


def test_nulllist_numberlist2(db, vsql_data):
	assert expr(db, "[None] > [1.1]") is None


def test_nulllist_numberlist3(db, vsql_data):
	assert expr(db, "[None, None] > [1.1]") is None


def test_nulllist_strlist1(db, vsql_data):
	assert not expr(db, "[] > ['gurk']")


def test_nulllist_strlist2(db, vsql_data):
	assert expr(db, "[None] > ['gurk']") is None


def test_nulllist_strlist3(db, vsql_data):
	assert expr(db, "[None, None] > ['gurk']") is None


def test_nulllist_datelist1(db, vsql_data):
	assert not expr(db, "[] > [@(2000-02-29)]")


def test_nulllist_datelist2(db, vsql_data):
	assert expr(db, "[None] > [@(2000-02-29)]") is None


def test_nulllist_datelist3(db, vsql_data):
	assert expr(db, "[None, None] > [@(2000-02-29)]") is None


def test_nulllist_datetimelist1(db, vsql_data):
	assert not expr(db, "[] > [@(2000-02-29T12:34:56)]")


def test_nulllist_datetimelist2(db, vsql_data):
	assert expr(db, "[None] > [@(2000-02-29T12:34:56)]") is None


def test_nulllist_datetimelist3(db, vsql_data):
	assert expr(db, "[None, None] > [@(2000-02-29T12:34:56)]") is None


def test_intlist_nulllist1(db, vsql_data):
	assert expr(db, "[1] > []")


def test_intlist_nulllist2(db, vsql_data):
	assert expr(db, "[1] > [None]") is None


def test_intlist_nulllist3(db, vsql_data):
	assert expr(db, "[1] > [None, None]") is None


def test_numberlist_nulllist1(db, vsql_data):
	assert expr(db, "[1.1] > []")


def test_numberlist_nulllist2(db, vsql_data):
	assert expr(db, "[1.1] > [None]") is None


def test_numberlist_nulllist3(db, vsql_data):
	assert expr(db, "[1.1] > [None, None]") is None


def test_strlist_nulllist1(db, vsql_data):
	assert expr(db, "['gurk'] > []")


def test_strlist_nulllist2(db, vsql_data):
	assert expr(db, "['gurk'] > [None]") is None


def test_strlist_nulllist3(db, vsql_data):
	assert expr(db, "['gurk'] > [None, None]") is None


def test_datelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29)] > []")


def test_datelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29)] > [None]") is None


def test_datelist_nulllist3(db, vsql_data):
	assert expr(db, "[@(2000-02-29)] > [None, None]") is None


def test_datetimelist_nulllist1(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56)] > []")


def test_datetimelist_nulllist2(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56)] > [None]") is None


def test_datetimelist_nulllist3(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56)] > [None, None]") is None
