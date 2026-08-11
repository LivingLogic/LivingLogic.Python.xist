"""
Tests for the vSQL addition operator ``+``.

To run the tests, :mod:`pytest` is required.
"""

import datetime

import pytest


###
### Tests
###

d1_v = "@(2000-02-29)"
d2_v = "@(2000-03-01)"

dt1_v = "@(2000-02-29T12:34:56)"
dt2_v = "@(2000-03-01T12:34:56)"


def d1(vsql_db):
	return vsql_db.type_for_date(2000, 2, 29)


def d2(vsql_db):
	return vsql_db.type_for_date(2000, 3, 1)


dt1 = datetime.datetime(2000, 2, 29, 12, 34, 56)
dt2 = datetime.datetime(2000, 3, 1, 12, 34, 56)


def test_bool_bool1(vsql_db, vsql_data):
	vsql_db.expr("r.v_bool + True", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool + True", where="r.identifier == 'bool_false'") == 1


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool + True", where="r.identifier == 'bool_true'") == 2


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool + 1", where="r.identifier == 'bool_true'") == 2


def test_bool_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool + 1.5", where="r.identifier == 'bool_true'") == 2.5


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("1 + r.v_bool", where="r.identifier == 'bool_true'") == 2


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("1 + r.v_int", where="r.identifier == 'int'") == 1777


def test_int_number(vsql_db, vsql_data):
	assert vsql_db.expr("1 + r.v_number", where="r.identifier == 'number'") == 43.5


def test_str_str1(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' + r.v_str", where="r.identifier == 'none'") == "gurk"


def test_str_str2(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' + r.v_str", where="r.identifier == 'str'") == "gurkgurk"


def test_str_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' + r.v_clob", where="r.identifier == 'none'") == "hurz"


def test_str_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' + r.v_clob", where="r.identifier == 'clob'") == "hurz" + "gurk" * 100000


def test_clob_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob + 'hurz'", where="r.identifier == 'none'") == "hurz"


def test_clob_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob + 'hurz'", where="r.identifier == 'clob'") == "gurk" * 100000 + "hurz"


def test_intlist_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] + [3, 4]") == [1, 2, 3, 4]


def test_intlist_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] + [3.5, 4.5]") == [1.0, 2.0, 3.5, 4.5]


def test_numberlist_intlist(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] + [3, 4]") == [1.5, 2.5, 3.0, 4.0]


def test_numberlist_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] + [3.5, 4.5]") == [1.5, 2.5, 3.5, 4.5]


def test_strlist_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] + ['hinz', 'kunz']") == ['gurk', 'hurz', 'hinz', 'kunz']


def test_datelist_datelist(vsql_db, vsql_data):
	result = vsql_db.expr("[@(2000-02-29), @(2000-03-01)] + [@(2000-03-02), @(2000-03-03)]")
	expected = [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1), vsql_db.type_for_date(2000, 3, 2), vsql_db.type_for_date(2000, 3, 3)]
	assert result == expected

def test_datetimelist_datetimelist(vsql_db, vsql_data):
	result = vsql_db.expr("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] + [@(2000-03-02T12:34:56), @(2000-03-03T12:34:56)]")
	expected = [vsql_db.type_for_datetime(2000, 2, 29, 12, 34, 56), vsql_db.type_for_datetime(2000, 3, 1, 12, 34, 56), vsql_db.type_for_datetime(2000, 3, 2, 12, 34, 56), vsql_db.type_for_datetime(2000, 3, 3, 12, 34, 56)]
	assert result == expected


def test_date_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date + days(1)", where="r.identifier == 'date'") == vsql_db.type_for_date(2000, 3, 1)


def test_date_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-01-31) + months(1)") == vsql_db.type_for_date(2000, 2, 29)


def test_datetime_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime + days(1)", where="r.identifier == 'datetime'") == vsql_db.type_for_datetime(2000, 3, 1, 12, 34, 56)


def test_datetime_datetimedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime + timedelta(1, 1)", where="r.identifier == 'datetime'") == vsql_db.type_for_datetime(2000, 3, 1, 12, 34, 57)


def test_datetime_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-01-31T12:34:56) + months(1)") == vsql_db.type_for_datetime(2000, 2, 29, 12, 34, 56)


def test_monthdelta_date(vsql_db, vsql_data):
	assert vsql_db.expr("months(1) + @(2000-01-31)") == vsql_db.type_for_date(2000, 2, 29)


def test_monthdelta_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("months(1) + @(2000-01-31T12:34:56)") == vsql_db.type_for_datetime(2000, 2, 29,12, 34, 56)


def test_datedelta_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta + days(12)", where="r.identifier == 'datedelta'") == vsql_db.type_for_datedelta(24)


def test_datedelta_datetimedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta + timedelta(1, 1)", where="r.identifier == 'datedelta'") == vsql_db.type_for_datetimedelta(13, 1)


def test_datetimedelta_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta + days(12)", where="r.identifier == 'datetimedelta'") == pytest.approx(vsql_db.type_for_datetimedelta(13, (12 * 60 + 34) * 60 + 56), rel=0.001)


def test_datetimedelta_datetimedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta + timedelta(2, (12 * 60 + 34) * 60 + 56)", where="r.identifier == 'datetimedelta'") == vsql_db.type_for_datetimedelta(3, 2 * ((12 * 60 + 34) * 60 + 56))


def test_monthdelta_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta + months(9)", where="r.identifier == 'monthdelta'") == vsql_db.type_for_monthdelta(12)


def test_nulllist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] + []") == 0


def test_nulllist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] + [None]") == 3


def test_nulllist_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] + [1, None, 2]") == [1, None, 2]


def test_nulllist_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] + [1, None, 2]") == [None, None, 1, None, 2]


def test_nulllist_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] + [1.1, None, 2.2]") == [1.1, None, 2.2]


def test_nulllist_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] + [1.1, None, 2.2]") == [None, None, 1.1, None, 2.2]


def test_nulllist_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] + ['gurk', None, 'hurz']") == ['gurk', None, 'hurz']


def test_nulllist_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] + ['gurk', None, 'hurz']") == [None, None, 'gurk', None, 'hurz']


def test_nulllist_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[] + [{d1_v}, None, {d2_v}]") == [d1(vsql_db), None, d2(vsql_db)]


def test_nulllist_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None] + [{d1_v}, None, {d2_v}]") == [None, None, d1(vsql_db), None, d2(vsql_db)]


def test_nulllist_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[] + [{dt1_v}, None, {dt2_v}]") == [dt1, None, dt2]


def test_nulllist_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None] + [{dt1_v}, None, {dt2_v}]") == [None, None, dt1, None, dt2]


def test_intlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1, None, 2] + []") == [1, None, 2]


def test_intlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1, None, 2] + [None, None]") == [1, None, 2, None, None]


def test_numberlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, None, 2.2] + []") == [1.1, None, 2.2]


def test_numberlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, None, 2.2] + [None, None]") == [1.1, None, 2.2, None, None]


def test_strlist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', None, 'hurz'] + []") == ['gurk', None, 'hurz']


def test_strlist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', None, 'hurz'] + [None, None]") == ['gurk', None, 'hurz', None, None]


def test_datelist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[{d1_v}, None, {d2_v}] + []") == [d1(vsql_db), None, d2(vsql_db)]


def test_datelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[{d1_v}, None, {d2_v}] + [None, None]") == [d1(vsql_db), None, d2(vsql_db), None, None]


def test_datetimelist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[{dt1_v}, None, {dt2_v}] + []") == [dt1, None, dt2]


def test_datetimelist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[{dt1_v}, None, {dt2_v}] + [None, None]") == [dt1, None, dt2, None, None]
