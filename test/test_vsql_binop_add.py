"""
Tests for the vSQL addition operator ``+``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

d1_v = "@(2000-02-29)"
d2_v = "@(2000-03-01)"

dt1_v = "@(2000-02-29T12:34:56)"
dt2_v = "@(2000-03-01T12:34:56)"

d1 = datetime.datetime(2000, 2, 29)
d2 = datetime.datetime(2000, 3, 1)

dt1 = datetime.datetime(2000, 2, 29, 12, 34, 56)
dt2 = datetime.datetime(2000, 3, 1, 12, 34, 56)


def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool + True", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool + True", where="r.identifier == 'bool_false'") == 1


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool + True", where="r.identifier == 'bool_true'") == 2


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool + 1", where="r.identifier == 'bool_true'") == 2


def test_bool_number(db, vsql_data):
	assert expr(db, "r.v_bool + 1.5", where="r.identifier == 'bool_true'") == 2.5


def test_int_bool(db, vsql_data):
	assert expr(db, "1 + r.v_bool", where="r.identifier == 'bool_true'") == 2


def test_int_int(db, vsql_data):
	assert expr(db, "1 + r.v_int", where="r.identifier == 'int'") == 1777


def test_int_number(db, vsql_data):
	assert expr(db, "1 + r.v_number", where="r.identifier == 'number'") == 43.5


def test_str_str1(db, vsql_data):
	assert expr(db, "'gurk' + r.v_str", where="r.identifier == 'none'") == "gurk"


def test_str_str2(db, vsql_data):
	assert expr(db, "'gurk' + r.v_str", where="r.identifier == 'str'") == "gurkgurk"


def test_intlist_intlist(db, vsql_data):
	assert expr(db, "[1, 2] + [3, 4]") == [1, 2, 3, 4]


def test_intlist_numberlist(db, vsql_data):
	assert expr(db, "[1, 2] + [3.5, 4.5]") == [1.0, 2.0, 3.5, 4.5]


def test_numberlist_intlist(db, vsql_data):
	assert expr(db, "[1.5, 2.5] + [3, 4]") == [1.5, 2.5, 3.0, 4.0]


def test_numberlist_numberlist(db, vsql_data):
	assert expr(db, "[1.5, 2.5] + [3.5, 4.5]") == [1.5, 2.5, 3.5, 4.5]


def test_strlist_strlist(db, vsql_data):
	assert expr(db, "['gurk', 'hurz'] + ['hinz', 'kunz']") == ['gurk', 'hurz', 'hinz', 'kunz']


def test_datelist_datelist(db, vsql_data):
	assert expr(db, "[@(2000-02-29), @(2000-03-01)] + [@(2000-03-02), @(2000-03-03)]") == [datetime.datetime(2000, 2, 29), datetime.datetime(2000, 3, 1), datetime.datetime(2000, 3, 2), datetime.datetime(2000, 3, 3)]


def test_datetimelist_datetimelist(db, vsql_data):
	assert expr(db, "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)] + [@(2000-03-02T12:34:56), @(2000-03-03T12:34:56)]") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 3, 1, 12, 34, 56), datetime.datetime(2000, 3, 2, 12, 34, 56), datetime.datetime(2000, 3, 3, 12, 34, 56)]


def test_date_datedelta(db, vsql_data):
	assert expr(db, "r.v_date + days(1)", where="r.identifier == 'date'") == datetime.datetime(2000, 3, 1)


def test_date_monthdelta(db, vsql_data):
	assert expr(db, "@(2000-01-31) + months(1)") == datetime.datetime(2000, 2, 29)


def test_datetime_datedelta(db, vsql_data):
	assert expr(db, "r.v_datetime + days(1)", where="r.identifier == 'datetime'") == datetime.datetime(2000, 3, 1, 12, 34, 56)


def test_datetime_datetimedelta(db, vsql_data):
	assert expr(db, "r.v_datetime + timedelta(1, 1)", where="r.identifier == 'datetime'") == datetime.datetime(2000, 3, 1, 12, 34, 57)


def test_datetime_monthdelta(db, vsql_data):
	assert expr(db, "@(2000-01-31T12:34:56) + months(1)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_monthdelta_date(db, vsql_data):
	assert expr(db, "months(1) + @(2000-01-31)") == datetime.datetime(2000, 2, 29)


def test_monthdelta_datetime(db, vsql_data):
	assert expr(db, "months(1) + @(2000-01-31T12:34:56)") == datetime.datetime(2000, 2, 29,12, 34, 56)


def test_datedelta_datedelta(db, vsql_data):
	assert expr(db, "r.v_datedelta + days(12)", where="r.identifier == 'datedelta'") == 24


def test_datedelta_datetimedelta(db, vsql_data):
	assert expr(db, "r.v_datedelta + timedelta(1, 1)", where="r.identifier == 'datedelta'") == 13.0 + 1/24/60/60


def test_datetimedelta_datedelta(db, vsql_data):
	assert expr(db, "r.v_datetimedelta + days(12)", where="r.identifier == 'datetimedelta'") == 13 + 12/24 + 34/24/60 + 56/24/60/60


def test_datetimedelta_datetimedelta(db, vsql_data):
	assert expr(db, "r.v_datetimedelta + timedelta(2, (12 * 60 + 34) * 60 + 56)", where="r.identifier == 'datetimedelta'") == 3 + 2 * (12/24 + 34/24/60 + 56/24/60/60)


def test_monthdelta_monthdelta(db, vsql_data):
	assert expr(db, "r.v_monthdelta + months(9)", where="r.identifier == 'monthdelta'") == 12


def test_nulllist_nulllist1(db, vsql_data):
	assert expr(db, "[] + []") == 0


def test_nulllist_nulllist2(db, vsql_data):
	assert expr(db, "[None, None] + [None]") == 3


def test_nulllist_intlist1(db, vsql_data):
	assert expr(db, "[] + [1, None, 2]") == [1, None, 2]


def test_nulllist_intlist2(db, vsql_data):
	assert expr(db, "[None, None] + [1, None, 2]") == [None, None, 1, None, 2]


def test_nulllist_numberlist1(db, vsql_data):
	assert expr(db, "[] + [1.1, None, 2.2]") == [1.1, None, 2.2]


def test_nulllist_numberlist2(db, vsql_data):
	assert expr(db, "[None, None] + [1.1, None, 2.2]") == [None, None, 1.1, None, 2.2]


def test_nulllist_strlist1(db, vsql_data):
	assert expr(db, "[] + ['gurk', None, 'hurz']") == ['gurk', None, 'hurz']


def test_nulllist_strlist2(db, vsql_data):
	assert expr(db, "[None, None] + ['gurk', None, 'hurz']") == [None, None, 'gurk', None, 'hurz']


def test_nulllist_datelist1(db, vsql_data):
	assert expr(db, f"[] + [{d1_v}, None, {d2_v}]") == [d1, None, d2]


def test_nulllist_datelist2(db, vsql_data):
	assert expr(db, f"[None, None] + [{d1_v}, None, {d2_v}]") == [None, None, d1, None, d2]


def test_nulllist_datetimelist1(db, vsql_data):
	assert expr(db, f"[] + [{dt1_v}, None, {dt2_v}]") == [dt1, None, dt2]


def test_nulllist_datetimelist2(db, vsql_data):
	assert expr(db, f"[None, None] + [{dt1_v}, None, {dt2_v}]") == [None, None, dt1, None, dt2]


def test_intlist_nulllist1(db, vsql_data):
	assert expr(db, "[1, None, 2] + []") == [1, None, 2]


def test_intlist_nulllist2(db, vsql_data):
	assert expr(db, "[1, None, 2] + [None, None]") == [1, None, 2, None, None]


def test_numberlist_nulllist1(db, vsql_data):
	assert expr(db, "[1.1, None, 2.2] + []") == [1.1, None, 2.2]


def test_numberlist_nulllist2(db, vsql_data):
	assert expr(db, "[1.1, None, 2.2] + [None, None]") == [1.1, None, 2.2, None, None]


def test_strlist_nulllist1(db, vsql_data):
	assert expr(db, "['gurk', None, 'hurz'] + []") == ['gurk', None, 'hurz']


def test_strlist_nulllist2(db, vsql_data):
	assert expr(db, "['gurk', None, 'hurz'] + [None, None]") == ['gurk', None, 'hurz', None, None]


def test_datelist_nulllist1(db, vsql_data):
	assert expr(db, f"[{d1_v}, None, {d2_v}] + []") == [d1, None, d2]


def test_datelist_nulllist2(db, vsql_data):
	assert expr(db, f"[{d1_v}, None, {d2_v}] + [None, None]") == [d1, None, d2, None, None]


def test_datetimelist_nulllist1(db, vsql_data):
	assert expr(db, f"[{dt1_v}, None, {dt2_v}] + []") == [dt1, None, dt2]


def test_datetimelist_nulllist2(db, vsql_data):
	assert expr(db, f"[{dt1_v}, None, {dt2_v}] + [None, None]") == [dt1, None, dt2, None, None]
