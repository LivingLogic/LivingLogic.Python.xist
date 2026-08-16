"""
Tests for the vSQL slice operator ``A[B:C]``.

To run the tests, :mod:`pytest` is required.
"""

import datetime

import pytest


###
### Tests
###

def d1(vsql_db):
	return vsql_db.type_for_date(2000, 2, 29)


def d2(vsql_db):
	return vsql_db.type_for_date(2000, 3, 1)


def d3(vsql_db):
	return vsql_db.type_for_date(2000, 3, 2)


def d4(vsql_db):
	return vsql_db.type_for_date(2000, 3, 3)


dt1 = datetime.datetime(2000, 2, 29, 12, 34, 56)
dt2 = datetime.datetime(2000, 3, 1, 12, 34, 56)
dt3 = datetime.datetime(2000, 3, 2, 12, 34, 56)
dt4 = datetime.datetime(2000, 3, 3, 12, 34, 56)

int_list = "[1, 2, 3, 4]"

number_list = "[1.1, 2.2, 3.3, 4.4]"

date_list = "[@(2000-02-29), @(2000-03-01), @(2000-03-02), @(2000-03-03)]"

datetime_list = "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56), @(2000-03-02T12:34:56), @(2000-03-03T12:34:56)]"


def test_str_1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[1:3]", where="r.identifier == 'str'") == "ur"


def test_str_2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[-3:-1]", where="r.identifier == 'str'") == "ur"


def test_str_3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[4:10]", where="r.identifier == 'str'") is None


def test_str_4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[-10:-5]", where="r.identifier == 'str'") is None


def test_str_5(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[1:]", where="r.identifier == 'str'") == "urk"


def test_str_6(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[-3:]", where="r.identifier == 'str'") == "urk"


def test_str_7(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[4:]", where="r.identifier == 'str'") is None


def test_str_8(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[-10:]", where="r.identifier == 'str'") == "gurk"


def test_str_9(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[:3]", where="r.identifier == 'str'") == "gur"


def test_str_10(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[:-1]", where="r.identifier == 'str'") == "gur"


def test_str_11(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[:10]", where="r.identifier == 'str'") == "gurk"


def test_str_12(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[:-5]", where="r.identifier == 'str'") is None


def test_str_13(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[:]", where="r.identifier == 'str'") == "gurk"


def test_str_14(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str[None:None]", where="r.identifier == 'str'") == "gurk"


def test_intlist_1(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[1:3]") == [2, 3]


def test_intlist_2(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[-3:-1]") == [2, 3]


def test_intlist_3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[4:10]") == []


def test_intlist_4(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[-10:-5]") == []


def test_intlist_5(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[1:]") == [2, 3, 4]


def test_intlist_6(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[-3:]") == [2, 3, 4]


def test_intlist_7(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[4:]") == []


def test_intlist_8(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[-10:]") == [1, 2, 3, 4]


def test_intlist_9(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[:3]") == [1, 2, 3]


def test_intlist_10(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[:-1]") == [1, 2, 3]


def test_intlist_11(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[:10]") == [1, 2, 3, 4]


def test_intlist_12(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[:-5]") == []


def test_intlist_13(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[:]") == [1, 2, 3, 4]


def test_intlist_14(vsql_db, vsql_data):
	assert vsql_db.expr(f"{int_list}[None:None]") == [1, 2, 3, 4]


def test_numberlist_1(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[1:3]") == [2.2, 3.3]


def test_numberlist_2(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[-3:-1]") == [2.2, 3.3]


def test_numberlist_3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[4:10]") == []


def test_numberlist_4(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[-10:-5]") == []


def test_numberlist_5(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[1:]") == [2.2, 3.3, 4.4]


def test_numberlist_6(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[-3:]") == [2.2, 3.3, 4.4]


def test_numberlist_7(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[4:]") == []


def test_numberlist_8(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[-10:]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_9(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[:3]") == [1.1, 2.2, 3.3]


def test_numberlist_10(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[:-1]") == [1.1, 2.2, 3.3]


def test_numberlist_11(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[:10]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_12(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[:-5]") == []


def test_numberlist_13(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[:]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_14(vsql_db, vsql_data):
	assert vsql_db.expr(f"{number_list}[None:None]") == [1.1, 2.2, 3.3, 4.4]


def test_datelist_1(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[1:3]") == [d2(vsql_db), d3(vsql_db)]


def test_datelist_2(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[-3:-1]") == [d2(vsql_db), d3(vsql_db)]


def test_datelist_3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[4:10]") == []


def test_datelist_4(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[-10:-5]") == []


def test_datelist_5(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[1:]") == [d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datelist_6(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[-3:]") == [d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datelist_7(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[4:]") == []


def test_datelist_8(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[-10:]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datelist_9(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[:3]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db)]


def test_datelist_10(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[:-1]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db)]


def test_datelist_11(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[:10]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datelist_12(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[:-5]") == []


def test_datelist_13(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[:]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datelist_14(vsql_db, vsql_data):
	assert vsql_db.expr(f"{date_list}[None:None]") == [d1(vsql_db), d2(vsql_db), d3(vsql_db), d4(vsql_db)]


def test_datetimelist_1(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[1:3]") == [dt2, dt3]


def test_datetimelist_2(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[-3:-1]") == [dt2, dt3]


def test_datetimelist_3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[4:10]") == []


def test_datetimelist_4(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[-10:-5]") == []


def test_datetimelist_5(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[1:]") == [dt2, dt3, dt4]


def test_datetimelist_6(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[-3:]") == [dt2, dt3, dt4]


def test_datetimelist_7(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[4:]") == []


def test_datetimelist_8(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[-10:]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_9(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[:3]") == [dt1, dt2, dt3]


def test_datetimelist_10(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[:-1]") == [dt1, dt2, dt3]


def test_datetimelist_11(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[:10]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_12(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[:-5]") == []


def test_datetimelist_13(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[:]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_14(vsql_db, vsql_data):
	assert vsql_db.expr(f"{datetime_list}[None:None]") == [dt1, dt2, dt3, dt4]


def test_nulllist_1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][1:3]") == 2


def test_nulllist_2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][-3:-1]") == 2


def test_nulllist_3(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][4:10]") == 0


def test_nulllist_4(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][-10:-5]") == 0


def test_nulllist_5(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][1:]") == 3


def test_nulllist_6(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][-3:]") == 3


def test_nulllist_7(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][4:]") == 0


def test_nulllist_8(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][-10:]") == 4


def test_nulllist_9(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][:3]") == 3


def test_nulllist_10(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][:-1]") == 3


def test_nulllist_11(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][:10]") == 4


def test_nulllist_12(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][:-5]") == 0


def test_nulllist_13(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][:]") == 4


def test_nulllist_14(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, None, None, None][None:None]") == 4


def test_nulllist_15(vsql_db, vsql_data):
	assert vsql_db.expr(f"[][:]") == 0


# The slice operator supports ``BOOL``, ``INT`` and ``NULL`` (i.e. an omitted
# bound) for both bounds on every sliceable type. The following test covers
# all those combinations, comparing against Python's slicing behaviour. The
# indexes are chosen so that the result is never empty (Oracle can't
# distinguish an empty string from ``None``).

_slice_objs = dict(
	str=("'gurkhurz'", None, "gurkhurz", None),
	clob=("(r.v_clob + r.v_clob)", "shortclob", "gurkgurk", None),
	nulllist=("[None, None, None]", None, [None, None, None], "nulllist"),
	intlist=("[1, 2, 3, 4]", None, [1, 2, 3, 4], None),
	numberlist=("[1.5, 2.5, 3.5]", None, [1.5, 2.5, 3.5], None),
	strlist=("['a', 'b', 'c']", None, ["a", "b", "c"], None),
	cloblist=("['a', r.v_clob, 'c']", "shortclob", ["a", "gurk", "c"], None),
	datelist=("[@(2000-02-29), @(2000-03-01), @(2000-03-02)]", None, [(2000, 2, 29), (2000, 3, 1), (2000, 3, 2)], "date"),
	datetimelist=("[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]", None, [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 3, 1, 12, 34, 56)], None),
)

_slice_starts = dict(null=("", None), bool=("False", False), int=("0", 0))
_slice_ends = dict(null=("", None), bool=("True", True), int=("3", 3))

@pytest.mark.parametrize("i2", _slice_ends)
@pytest.mark.parametrize("i1", _slice_starts)
@pytest.mark.parametrize("obj", _slice_objs)
def test_all_type_combinations(vsql_db, vsql_data, obj, i1, i2):
	(objexpr, identifier, value, conv) = _slice_objs[obj]
	(startsrc, start) = _slice_starts[i1]
	(endsrc, end) = _slice_ends[i2]
	where = f"r.identifier == '{identifier}'" if identifier else None
	result = vsql_db.expr(f"{objexpr}[{startsrc}:{endsrc}]", where=where)
	expected = value[start:end]
	if conv == "nulllist":
		# A ``NULLLIST`` result is returned as the number of its elements
		expected = len(expected)
	elif conv == "date":
		expected = [vsql_db.type_for_date(*d) for d in expected]
	assert result == expected
