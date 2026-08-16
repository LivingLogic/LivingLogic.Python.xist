"""
Tests for the vSQL equality comparision operator ``==``.

To run the tests, :mod:`pytest` is required.
"""

import pytest

import conftest


###
### Tests
###

def test_bool_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool == None", where="r.identifier == 'none'")


def test_bool_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_bool == None", where="r.identifier == 'bool_true'")


def test_int_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int == None", where="r.identifier == 'none'")


def test_int_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_int == None", where="r.identifier == 'int'")


def test_number_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number == None", where="r.identifier == 'none'")


def test_number_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_number == None", where="r.identifier == 'number'")


def test_str_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str == None", where="r.identifier == 'none'")


def test_str_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_str == None", where="r.identifier == 'str'")


def test_date_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date == None", where="r.identifier == 'none'")


def test_date_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_date == None", where="r.identifier == 'date'")


def test_datetime_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime == None", where="r.identifier == 'none'")


def test_datetime_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datetime == None", where="r.identifier == 'datetime'")


def test_color_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color == None", where="r.identifier == 'none'")


def test_color_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_color == None", where="r.identifier == 'color'")


def test_datedelta_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta == None", where="r.identifier == 'none'")


def test_datedelta_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datedelta == None", where="r.identifier == 'datedelta'")


def test_datetimedelta_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta == None", where="r.identifier == 'none'")


def test_datetimedelta_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datetimedelta == None", where="r.identifier == 'datetimedelta'")


def test_monthdelta_none_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta == None", where="r.identifier == 'none'")


def test_monthdelta_none_true(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_monthdelta == None", where="r.identifier == 'monthdelta'")


def test_bool_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool == False", where="r.identifier == 'bool_false'")


def test_bool_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool == True", where="r.identifier == 'bool_true'")


def test_bool_int_false(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool == 0", where="r.identifier == 'bool_false'")


def test_bool_int_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool == 1", where="r.identifier == 'bool_true'")


def test_int_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("0 == r.v_bool", where="r.identifier == 'bool_false'")


def test_int_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("1 == r.v_bool", where="r.identifier == 'bool_true'")


def test_number_bool_false(vsql_db, vsql_data):
	assert vsql_db.expr("0.0 == r.v_bool", where="r.identifier == 'bool_false'")


def test_number_bool_true(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 == r.v_bool", where="r.identifier == 'bool_true'")


def test_number_int_false(vsql_db, vsql_data):
	assert not vsql_db.expr("42.5 == r.v_int", where="r.identifier == 'int'")


def test_number_int_true(vsql_db, vsql_data):
	assert vsql_db.expr("1776.0 == r.v_int", where="r.identifier == 'int'")


def test_number_number_false(vsql_db, vsql_data):
	assert not vsql_db.expr("17.23 == r.v_number", where="r.identifier == 'number'")


def test_number_number_true(vsql_db, vsql_data):
	assert vsql_db.expr("42.5 == r.v_number", where="r.identifier == 'number'")


def test_str_str_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_str == 'gurk'", where="r.identifier == 'none'")


def test_str_str_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str == 'gurk'", where="r.identifier == 'str'")


def test_date_date_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_date == @(2000-02-29)", where="r.identifier == 'none'")


def test_date_date_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date == @(2000-02-29)", where="r.identifier == 'date'")


def test_datetime_datetime_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datetime == @(2000-02-29T12:34:56)", where="r.identifier == 'none'")


def test_datetime_datetime_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime == @(2000-02-29T12:34:56)", where="r.identifier == 'datetime'")


def test_datedelta_datedelta_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datedelta == days(12)", where="r.identifier == 'none'")


def test_datedelta_datedelta_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta == days(12)", where="r.identifier == 'datedelta'")


def test_color_color_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_color == #369c", where="r.identifier == 'none'")


def test_color_color_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color == #123456ff", where="r.identifier == 'color'")


def test_datetimedelta_datetimedelta_false(vsql_db, vsql_data):
	assert not vsql_db.expr("r.v_datetimedelta == timedelta(1, 45296)", where="r.identifier == 'none'")


def test_datetimedelta_datetimedelta_true(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta == timedelta(1, 45296)", where="r.identifier == 'datetimedelta'")


def test_intlist_intlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [2]")


def test_intlist_intlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [1, 2]")


def test_intlist_intlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1, 2] == [1]")


def test_intlist_intlist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[1, None] == [1]")


def test_intlist_intlist5(vsql_db, vsql_data):
	assert vsql_db.expr("[1, None, 2, None, 3] == [1, None, 2, None, 3]")


def test_intlist_numberlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [1.5]")


def test_intlist_numberlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [1.0, 2.0]")


def test_intlist_numberlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1, 2] == [1.0]")


def test_intlist_numberlist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[1, None] == [1.0]")


def test_intlist_numberlist5(vsql_db, vsql_data):
	assert vsql_db.expr("[1, None, 2, None, 3] == [1.0, None, 2.0, None, 3.0]")


def test_numberlist_intlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.5] == [2]")


def test_numberlist_intlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.0] == [1, 2]")


def test_numberlist_intlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.0, 2.0] == [1]")


def test_numberlist_intlist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.0, None] == [1]")


def test_numberlist_intlist5(vsql_db, vsql_data):
	assert vsql_db.expr("[1.0, None, 2.0, None, 3.0] == [1, None, 2, None, 3]")


def test_numberlist_numberlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.5] == [2.5]")


def test_numberlist_numberlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.0] == [1.0, 2.0]")


def test_numberlist_numberlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.0, 2.0] == [1.0]")


def test_numberlist_numberlist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.5, None] == [1.5]")


def test_numberlist_numberlist5(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, None, 2.5, None, 3.5] == [1.5, None, 2.5, None, 3.5]")


def test_strlist_strlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("['foo'] == ['bar']")


def test_strlist_strlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("['foo'] == ['foo', 'bar']")


def test_strlist_strlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("['foo', 'bar'] == ['foo']")


def test_strlist_strlist4(vsql_db, vsql_data):
	assert not vsql_db.expr("['foo', None] == ['foo']")


def test_strlist_strlist5(vsql_db, vsql_data):
	assert vsql_db.expr("['foo', None, 'bar', None, 'baz'] == ['foo', None, 'bar', None, 'baz']")


def test_datelist_datelist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] == [@(2000-03-01)]")


def test_datelist_datelist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] == [@(2000-02-29), @(2000-03-01)]")


def test_datelist_datelist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29), @(2000-03-01)] == [@(2000-02-29)]")


def test_datelist_datelist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29), None] == [@(2000-02-29)]")


def test_datelist_datelist5(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), None, @(2000-03-01), None, @(2000-03-02)] == [@(2000-02-29), None, @(2000-03-01), None, @(2000-03-02)]")


def test_datetimelist_datetimelist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] == [@(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] == [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]")


def test_datetimelist_datetimelist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] == [@(2000-02-29T12:34:56)]")


def test_datetimelist_datetimelist4(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56), None] == [@(2000-02-29T12:34:56)]")


def test_datetimelist_datetimelist5(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56), None, @(2000-03-02T12:34:56)] == [@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56), None, @(2000-03-02T12:34:56)]")


def test_nulllist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] == []")


def test_nulllist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] == [None, None]")


def test_nulllist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == [None, None]")


def test_nulllist_intlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[] == [1]")


def test_nulllist_intlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == [1]")


def test_nulllist_intlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] == [1]")


def test_nulllist_numberlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[] == [1.1]")


def test_nulllist_numberlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == [1.1]")


def test_nulllist_numberlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] == [1.1]")


def test_nulllist_strlist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[] == ['gurk']")


def test_nulllist_strlist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == ['gurk']")


def test_nulllist_strlist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] == ['gurk']")


def test_nulllist_datelist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[] == [@(2000-02-29)]")


def test_nulllist_datelist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == [@(2000-02-29)]")


def test_nulllist_datelist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] == [@(2000-02-29)]")


def test_nulllist_datetimelist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[] == [@(2000-02-29T12:34:56)]")


def test_nulllist_datetimelist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[None] == [@(2000-02-29T12:34:56)]")


def test_nulllist_datetimelist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[None, None] == [@(2000-02-29T12:34:56)]")


def test_intlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == []")


def test_intlist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [None]")


def test_intlist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1] == [None, None]")


def test_numberlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.1] == []")


def test_numberlist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.1] == [None]")


def test_numberlist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[1.1] == [None, None]")


def test_strlist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("['gurk'] == []")


def test_strlist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("['gurk'] == [None]")


def test_strlist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("['gurk'] == [None, None]")


def test_datelist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] == []")


def test_datelist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] == [None]")


def test_datelist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29)] == [None, None]")


def test_datetimelist_nulllist1(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] == []")


def test_datetimelist_nulllist2(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] == [None]")


def test_datetimelist_nulllist3(vsql_db, vsql_data):
	assert not vsql_db.expr("[@(2000-02-29T12:34:56)] == [None, None]")


def test_intset_intset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{1} == {2}")


def test_intset_intset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{1} == {1, 2}")


def test_intset_intset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{1, 2} == {1}")


def test_intset_intset4(vsql_db, vsql_data):
	assert vsql_db.expr("({1, 2} == {2, 1})")


def test_intset_intset5(vsql_db, vsql_data):
	assert not vsql_db.expr("{1, None} == {1}")


def test_intset_intset6(vsql_db, vsql_data):
	assert vsql_db.expr("{1, None, 2, None, 3} == {None, 3, 2, 1, None}")


def test_numberset_numberset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.5} == {2.5}")


def test_numberset_numberset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.5} == {1.5, 2.5}")


def test_numberset_numberset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.5, 2.5} == {1.5}")


def test_numberset_numberset4(vsql_db, vsql_data):
	assert vsql_db.expr("({1.5, 2.5} == {2.5, 1.5})")


def test_numberset_numberset5(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.5, None} == {1.5}")


def test_numberset_numberset6(vsql_db, vsql_data):
	assert vsql_db.expr("{1.5, None, 2.5, None, 3.5} == {None, 3.5, 2.5, 1.5, None}")


def test_strset_strset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.5} == {2.5}")


def test_strset_strset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{'foo'} == {'foo', 'bar'}")


def test_strset_strset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{'foo', 'bar'} == {'foo'}")


def test_strset_strset4(vsql_db, vsql_data):
	assert vsql_db.expr("{'foo', 'bar'} == {'bar', 'foo'}")


def test_strset_strset5(vsql_db, vsql_data):
	assert not vsql_db.expr("{'foo', None} == {'foo'}")


def test_strset_strset6(vsql_db, vsql_data):
	assert vsql_db.expr("{'foo', None, 'bar', None, 'baz'} == {None, 'baz', 'bar', 'foo', None}")


def test_dateset_dateset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29)} == {@(2000-03-01)}")


def test_dateset_dateset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29)} == {@(2000-02-29), @(2000-03-01)}")


def test_dateset_dateset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29), @(2000-03-01)} == {@(2000-02-29)}")


def test_dateset_dateset4(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29), @(2000-03-01)} == {@(2000-03-01), @(2000-02-29)}")


def test_dateset_dateset5(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29), None} == {@(2000-02-29)}")


def test_dateset_dateset6(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29), None, @(2000-03-01), None, @(2000-03-02)} == {None, @(2000-03-02), @(2000-03-01), @(2000-02-29), None}")


def test_datetimeset_datetimeset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56)} == {@(2000-03-01T12:34:56)}")


def test_datetimeset_datetimeset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56)} == {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}")


def test_datetimeset_datetimeset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} == {@(2000-02-29T12:34:56)}")


def test_datetimeset_datetimeset4(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} == {@(2000-03-01T12:34:56), @(2000-02-29T12:34:56)}")


def test_datetimeset_datetimeset5(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56), None} == {@(2000-02-29T12:34:56)}")


def test_datetimeset_datetimeset6(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56), None, @(2000-03-02T12:34:56)} == {None, @(2000-03-02T12:34:56), @(2000-03-01T12:34:56), @(2000-02-29T12:34:56), None}")


def test_nullset_nullset1(vsql_db, vsql_data):
	assert vsql_db.expr("{/} == {/}")


def test_nullset_nullset2(vsql_db, vsql_data):
	assert vsql_db.expr("{None} == {None}")


def test_nullset_nullset3(vsql_db, vsql_data):
	assert vsql_db.expr("{None} == {None, None}")


def test_nullset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {None, None}")


def test_nullset_intset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {1}")


def test_nullset_intset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{None} == {1}")


def test_nullset_intset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {1}")


def test_nullset_intset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {1, 2}")


def test_nullset_numberset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {1.1}")


def test_nullset_numberset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{None} == {1.1}")


def test_nullset_numberset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {1.1}")


def test_nullset_numberset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {1.1, 2.2}")


def test_nullset_strset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {'gurk'}")


def test_nullset_strset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{None} == {'gurk'}")


def test_nullset_strset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {'gurk'}")


def test_nullset_strset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {'gurk', 'hurz'}")


def test_nullset_dateset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {@(2000-02-29)}")


def test_nullset_dateset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{None} == {@(2000-02-29)}")


def test_nullset_dateset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {@(2000-02-29)}")


def test_nullset_dateset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {@(2000-02-29), @(2000-03-01)}")


def test_nullset_datetimeset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{/} == {@(2000-02-29T12:34:56)}")


def test_nullset_datetimeset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{None} == {@(2000-02-29T12:34:56)}")


def test_nullset_datetimeset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {@(2000-02-29T12:34:56)}")


def test_nullset_datetimeset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{None, None} == {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}")


def test_intset_nullset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{1} == {/}")


def test_intset_nullset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{1} == {None}")


def test_intset_nullset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{1} == {None, None}")


def test_intset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{1, 2} == {None, None}")


def test_numberset_nullset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.1} == {/}")


def test_numberset_nullset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.1} == {None}")


def test_numberset_nullset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.1} == {None, None}")


def test_numberset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{1.1, 2.2} == {None, None}")


def test_strset_nullset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{'gurk'} == {/}")


def test_strset_nullset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{'gurk'} == {None}")


def test_strset_nullset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{'gurk'} == {None, None}")


def test_strset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{'gurk', 'hurz'} == {None, None}")


def test_dateset_nullset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29)} == {/}")


def test_dateset_nullset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29)} == {None}")


def test_dateset_nullset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29)} == {None, None}")


def test_dateset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29), @(2000-03-01)} == {None, None}")


def test_datetimeset_nullset1(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56)} == {/}")


def test_datetimeset_nullset2(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56)} == {None}")


def test_datetimeset_nullset3(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56)} == {None, None}")


def test_datetimeset_nullset4(vsql_db, vsql_data):
	assert not vsql_db.expr("{@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)} == {None, None}")


###
### Systematic tests for all type combinations
###

# ``==`` supports comparing all vSQL data types with each other. For
# incompatible type combinations the values are never equal — except when both
# values happen to be ``null``. The following test systematically covers all
# type combinations, using the canonical expressions from
# ``conftest.vsql_cmp_exprs``: those are non-constant (so that UL4 doesn't
# constant-fold the comparison) and their values are pairwise unequal, so two
# different expressions must always compare as unequal, while comparing an
# expression with itself must compare as equal.

@pytest.mark.parametrize("t2", conftest.vsql_cmp_exprs)
@pytest.mark.parametrize("t1", conftest.vsql_cmp_exprs)
def test_all_type_combinations(vsql_db, vsql_data, t1, t2):
	(expr1, identifier1) = conftest.vsql_cmp_exprs[t1]
	(expr2, identifier2) = conftest.vsql_cmp_exprs[t2]
	identifier = identifier1 or identifier2
	where = f"r.identifier == '{identifier}'" if identifier else None
	assert vsql_db.expr(f"{expr1} == {expr2}", where=where) == int(t1 == t2)


@pytest.mark.parametrize("f2", conftest.vsql_cmp_fields)
@pytest.mark.parametrize("f1", conftest.vsql_cmp_fields)
def test_all_type_combinations_null(vsql_db, vsql_data, f1, f2):
	# On the ``none`` record all fields are ``null``, and two ``null`` values
	# compare as equal — even when their types are incompatible
	assert vsql_db.expr(f"r.{f1} == r.{f2}", where="r.identifier == 'none'") == 1
