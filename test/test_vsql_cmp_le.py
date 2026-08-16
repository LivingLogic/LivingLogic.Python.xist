"""
Tests for the vSQL "less than or equal" comparison operator ``<=``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'none'")


def test_bool_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_false'") is None


def test_bool_none3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_true'") is None


def test_int_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= None", where="r.identifier == 'none'")


def test_int_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= None", where="r.identifier == 'int'") is None


def test_number_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= None", where="r.identifier == 'none'")


def test_number_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= None", where="r.identifier == 'number'") is None


def test_str_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str <= None", where="r.identifier == 'none'")


def test_str_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str <= None", where="r.identifier == 'str'") is None


def test_date_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date <= None", where="r.identifier == 'none'")


def test_date_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date <= None", where="r.identifier == 'date'") is None


def test_datetime_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime <= None", where="r.identifier == 'none'")


def test_datetime_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime <= None", where="r.identifier == 'datetime'") is None


def test_color_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color <= None", where="r.identifier == 'none'")


def test_color_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color <= None", where="r.identifier == 'color'") is None


def test_datedelta_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta <= None", where="r.identifier == 'none'")


def test_datedelta_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta <= None", where="r.identifier == 'datedelta'") is None


def test_datetimedelta_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta <= None", where="r.identifier == 'none'")


def test_datetimedelta_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta <= None", where="r.identifier == 'datetimedelta'") is None


def test_monthdelta_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta <= None", where="r.identifier == 'none'")


def test_monthdelta_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta <= None", where="r.identifier == 'monthdelta'") is None


def test_intlist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] <= None") is None


def test_numberlist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[1.2, 3.4] <= None") is None


def test_strlist_none(vsql_db, vsql_data):
	assert vsql_db.expr("['foo', 'bar'] <= None") is None


def test_datelist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] <= None") is None


def test_datetimelist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] <= None") is None


def test_none_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_bool", where="r.identifier == 'none'")


def test_none_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_bool", where="r.identifier == 'bool_false'") is None


def test_none_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_bool", where="r.identifier == 'bool_true'") is None


def test_none_int1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_int", where="r.identifier == 'none'")


def test_none_int2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_int", where="r.identifier == 'int'") is None


def test_none_number1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_number", where="r.identifier == 'none'")


def test_none_number2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_number", where="r.identifier == 'number'") is None


def test_none_str1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_str", where="r.identifier == 'none'")


def test_none_str2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_str", where="r.identifier == 'str'") is None


def test_none_date1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_date", where="r.identifier == 'none'")


def test_none_date2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_date", where="r.identifier == 'date'") is None


def test_none_datetime1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datetime", where="r.identifier == 'none'")


def test_none_datetime2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datetime", where="r.identifier == 'datetime'") is None


def test_none_color1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_color", where="r.identifier == 'none'")


def test_none_color2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_color", where="r.identifier == 'color'") is None


def test_none_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datedelta", where="r.identifier == 'none'")


def test_none_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datedelta", where="r.identifier == 'datedelta'") is None


def test_none_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datetimedelta", where="r.identifier == 'none'")


def test_none_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_datetimedelta", where="r.identifier == 'datetimedelta'") is None


def test_none_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_monthdelta", where="r.identifier == 'none'")


def test_none_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_monthdelta", where="r.identifier == 'monthdelta'") is None


def test_none_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= [1, 2]") is None


def test_none_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= [1.2, 3.4]") is None


def test_none_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= ['foo', 'bar']") is None


def test_none_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= [@(2000-02-29)]") is None


def test_none_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= [@(2000-02-29T12:34:56)]") is None


def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'none'")


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= False", where="r.identifier == 'none'") is None


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= True", where="r.identifier == 'none'") is None


def test_bool_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_false'") is None


def test_bool_bool5(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= False", where="r.identifier == 'bool_false'")


def test_bool_bool6(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= True", where="r.identifier == 'bool_false'")


def test_bool_bool7(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_true'") is None


def test_bool_bool8(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_bool <= False", where="r.identifier == 'bool_true'")


def test_bool_bool9(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= True", where="r.identifier == 'bool_true'")


def test_bool_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'none'")


def test_bool_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= -1", where="r.identifier == 'none'") is None


def test_bool_int3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_false'") is None


def test_bool_int4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 0", where="r.identifier == 'bool_false'")


def test_bool_int5(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 1", where="r.identifier == 'bool_false'")


def test_bool_int6(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_true'") is None


def test_bool_int7(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_bool <= 0", where="r.identifier == 'bool_true'")


def test_bool_int8(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 1", where="r.identifier == 'bool_true'")


def test_bool_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'none'")


def test_bool_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= -1.0", where="r.identifier == 'none'") is None


def test_bool_number3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_false'") is None


def test_bool_number4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 0.0", where="r.identifier == 'bool_false'")


def test_bool_number5(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 1.0", where="r.identifier == 'bool_false'")


def test_bool_number6(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= None", where="r.identifier == 'bool_true'") is None


def test_bool_number7(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_bool <= 0.0", where="r.identifier == 'bool_true'")


def test_bool_number8(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool <= 1.0", where="r.identifier == 'bool_true'")


def test_int_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= None", where="r.identifier == 'none'")


def test_int_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= False", where="r.identifier == 'none'") is None


def test_int_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= True", where="r.identifier == 'none'") is None


def test_int_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= None", where="r.identifier == 'int'") is None


def test_int_bool5(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_int <= False", where="r.identifier == 'int'")


def test_int_bool6(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_int <= True", where="r.identifier == 'int'")


def test_int_bool7(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int <= None", where="r.identifier == 'int'") is None


def test_int_bool8(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int <= False", where="r.identifier == 'int'")


def test_int_bool9(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int <= True", where="r.identifier == 'int'")


def test_int_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= None", where="r.identifier == 'none'")


def test_int_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= 1", where="r.identifier == 'none'") is None


def test_int_int3(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_int <= 1775", where="r.identifier == 'int'")


def test_int_int4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= 1777", where="r.identifier == 'int'")


def test_int_int5(vsql_db, vsql_data):
	assert vsql_db.expr("1776 <= r.v_int", where="r.identifier == 'none'") is None


def test_number_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= None", where="r.identifier == 'none'")


def test_number_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= False", where="r.identifier == 'none'") is None


def test_number_bool3(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_number <= True", where="r.identifier == 'number'")


def test_number_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_number <= True", where="r.identifier == 'number'")


def test_number_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= None", where="r.identifier == 'none'")


def test_number_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= 1", where="r.identifier == 'none'") is None


def test_number_int3(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_number <= 1", where="r.identifier == 'number'")


def test_number_int4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= 73", where="r.identifier == 'number'")


def test_number_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= None", where="r.identifier == 'none'")


def test_number_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= 1.0", where="r.identifier == 'none'") is None


def test_number_number3(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_number <= 1.0", where="r.identifier == 'number'")


def test_number_number4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number <= 73.0", where="r.identifier == 'number'")


def test_str_str1(vsql_db, vsql_data):
	assert vsql_db.expr("'abc' <= r.v_str", where="r.identifier == 'str'")


def test_str_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str <= r.v_str", where="r.identifier == 'str'")


def test_date_date(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-28) <= r.v_date", where="r.identifier == 'date'")


def test_datetime_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-28T23:59:59) <= r.v_datetime", where="r.identifier == 'datetime'")


def test_datedelta_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("days(1) <= days(2)")


def test_datedelta_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("days(1) <= days(1)")


def test_datetimedelta_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("hours(1) <= hours(2)")


def test_datetimedelta_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("hours(1) <= hours(1)")


def test_intlist_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1] <= [1, 2]")


def test_intlist_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] <= [1, 3]")


def test_intlist_intlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1, 2] <= [1]")


def test_intlist_intlist4(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] <= [1, 2]")


def test_numberlist_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5] <= [1.5, 2.5]")


def test_numberlist_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] <= [1.5, 3.5]")


def test_numberlist_numberlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.5, 2.5] <= [1.5]")


def test_numberlist_numberlist4(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] <= [1.5, 2.5]")


def test_strlist_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("['foo'] <= ['foo', 'bar']")


def test_strlist_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("['foo', 'bar'] <= ['foo', 'baz']")


def test_strlist_strlist3(vsql_db, vsql_data):
	assert vsql_db.expr("['foo'] <= ['foo', 'bar']")


def test_strlist_strlist4(vsql_db, vsql_data):
	assert vsql_db.expr("['foo', 'bar'] <= ['foo', 'bar']")


def test_datelist_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] <= [@(2000-02-29), @(2000-03-01)]")


def test_datelist_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] <= [@(2000-02-29), @(2000-03-02)]")


def test_datelist_datelist3(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] <= [@(2000-02-29), @(2000-03-01)]")


def test_datelist_datelist4(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] <= [@(2000-02-29), @(2000-03-01)]")


def test_datetimelist_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] <= [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] <= [@(2000-02-29T12:34:56), @(2000-03-02T12:34:56)]")


def test_datetimelist_datetimelist3(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] <= [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist4(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] <= [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_nulllist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= []")


def test_nulllist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] <= []")


def test_nulllist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [None, None]")


def test_nulllist_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [1]")


def test_nulllist_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= [1]") is None


def test_nulllist_intlist3(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] <= [1]") is None


def test_nulllist_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [1.1]")


def test_nulllist_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= [1.1]") is None


def test_nulllist_numberlist3(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] <= [1.1]") is None


def test_nulllist_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= ['gurk']")


def test_nulllist_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= ['gurk']") is None


def test_nulllist_strlist3(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] <= ['gurk']") is None


def test_nulllist_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [@(2000-02-29)]")


def test_nulllist_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= [@(2000-02-29)]") is None


def test_nulllist_datelist3(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] <= [@(2000-02-29)]") is None


def test_nulllist_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [@(2000-02-29T12:34:56)]")


def test_nulllist_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= [@(2000-02-29T12:34:56)]") is None


def test_nulllist_datetimelist3(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] <= [@(2000-02-29T12:34:56)]") is None


def test_intlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] <= []")


def test_intlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1] <= [None]") is None


def test_intlist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("[1] <= [None, None]") is None


def test_numberlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.1] <= []")


def test_numberlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1] <= [None]") is None


def test_numberlist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1] <= [None, None]") is None


def test_strlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("['gurk'] <= []")


def test_strlist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("['gurk'] <= [None]")


def test_strlist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk'] <= [None, None]") is None


def test_datelist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] <= []")


def test_datelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] <= [None]") is None


def test_datelist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] <= [None, None]") is None


def test_datetimelist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] <= []")


def test_datetimelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] <= [None]") is None


def test_datetimelist_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] <= [None, None]") is None


def test_null_none(vsql_db, vsql_data):
	# ``None`` on both sides would be constant-folded by UL4, but
	# ``[None, None][0]`` is a non-constant expression of type ``NULL``,
	# so the database really executes the operator
	assert vsql_db.expr("[None, None][0] <= None")


def test_geo_none(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49, 11, 'Here') <= None") is None


def test_none_geo(vsql_db, vsql_data):
	assert vsql_db.expr("None <= geo(49, 11, 'Here')") is None


def test_nulllist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= None") is None


def test_none_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= []") is None


def test_nullset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{None} <= None") is None


def test_none_nullset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {None}") is None


def test_clob_none1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob <= None", where="r.identifier == 'none'")


def test_clob_none2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob <= None", where="r.identifier == 'shortclob'") is None


def test_none_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_clob", where="r.identifier == 'none'")


def test_none_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("None <= r.v_clob", where="r.identifier == 'shortclob'") is None


def test_cloblist_none(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] <= None", where="r.identifier == 'shortclob'") is None


def test_none_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("None <= [r.v_clob]", where="r.identifier == 'shortclob'") is None


def test_intset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{1, 2} <= None") is None


def test_none_intset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {1, 2}") is None


def test_numberset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{1.5, 2.5} <= None") is None


def test_none_numberset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {1.5, 2.5}") is None


def test_strset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{'gurk', 'hurz'} <= None") is None


def test_none_strset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {'gurk', 'hurz'}") is None


def test_dateset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29)} <= None") is None


def test_none_dateset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {@(2000-02-29)}") is None


def test_datetimeset_none(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56)} <= None") is None


def test_none_datetimeset(vsql_db, vsql_data):
	assert vsql_db.expr("None <= {@(2000-02-29T12:34:56)}") is None


def test_int_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int <= 1776.5", where="r.identifier == 'int'")


def test_int_number2(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_int <= 1775.5", where="r.identifier == 'int'")


def test_str_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("'gu' <= r.v_clob", where="r.identifier == 'shortclob'")


def test_str_clob2(vsql_db, vsql_data):
	assert not vsql_db.expr("'hurz' <= r.v_clob", where="r.identifier == 'shortclob'")


def test_clob_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob <= 'hurz'", where="r.identifier == 'shortclob'")


def test_clob_str2(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_clob <= 'gu'", where="r.identifier == 'shortclob'")


def test_clob_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob <= r.v_clob", where="r.identifier == 'shortclob'")


def test_clob_clob2(vsql_db, vsql_data):
	assert not vsql_db.expr("(r.v_clob + 'x') <= r.v_clob", where="r.identifier == 'shortclob'")


def test_intlist_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] <= [1.5]")


def test_numberlist_intlist(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.5] <= [1, 2]")


def test_strlist_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("['aa'] <= [r.v_clob]", where="r.identifier == 'shortclob'")


def test_cloblist_strlist(vsql_db, vsql_data):
	assert not vsql_db.expr("[r.v_clob] <= ['aa']", where="r.identifier == 'shortclob'")


def test_cloblist_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] <= [r.v_clob]", where="r.identifier == 'shortclob'")


def test_cloblist_cloblist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[r.v_clob, r.v_clob] <= [r.v_clob]", where="r.identifier == 'shortclob'")


def test_nulllist_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] <= [r.v_clob]", where="r.identifier == 'shortclob'")


def test_nulllist_cloblist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] <= [r.v_clob]", where="r.identifier == 'shortclob'") is None


def test_cloblist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[r.v_clob] <= []", where="r.identifier == 'shortclob'")


def test_cloblist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] <= [None]", where="r.identifier == 'shortclob'") is None
