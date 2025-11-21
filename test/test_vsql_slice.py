"""
Tests for the vSQL slice operator ``A[B:C]``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

d1 = datetime.datetime(2000, 2, 29)
d2 = datetime.datetime(2000, 3, 1)
d3 = datetime.datetime(2000, 3, 2)
d4 = datetime.datetime(2000, 3, 3)

dt1 = datetime.datetime(2000, 2, 29, 12, 34, 56)
dt2 = datetime.datetime(2000, 3, 1, 12, 34, 56)
dt3 = datetime.datetime(2000, 3, 2, 12, 34, 56)
dt4 = datetime.datetime(2000, 3, 3, 12, 34, 56)

int_list = "[1, 2, 3, 4]"

number_list = "[1.1, 2.2, 3.3, 4.4]"

date_list = "[@(2000-02-29), @(2000-03-01), @(2000-03-02), @(2000-03-03)]"

datetime_list = "[@(2000-02-29T12:34:56), @(2000-03-01T12:34:56), @(2000-03-02T12:34:56), @(2000-03-03T12:34:56)]"


def test_str_1(db, vsql_data):
	assert expr(db, "r.v_str[1:3]", where="r.identifier == 'str'") == "ur"


def test_str_2(db, vsql_data):
	assert expr(db, "r.v_str[-3:-1]", where="r.identifier == 'str'") == "ur"


def test_str_3(db, vsql_data):
	assert expr(db, "r.v_str[4:10]", where="r.identifier == 'str'") is None


def test_str_4(db, vsql_data):
	assert expr(db, "r.v_str[-10:-5]", where="r.identifier == 'str'") is None


def test_str_5(db, vsql_data):
	assert expr(db, "r.v_str[1:]", where="r.identifier == 'str'") == "urk"


def test_str_6(db, vsql_data):
	assert expr(db, "r.v_str[-3:]", where="r.identifier == 'str'") == "urk"


def test_str_7(db, vsql_data):
	assert expr(db, "r.v_str[4:]", where="r.identifier == 'str'") is None


def test_str_8(db, vsql_data):
	assert expr(db, "r.v_str[-10:]", where="r.identifier == 'str'") == "gurk"


def test_str_9(db, vsql_data):
	assert expr(db, "r.v_str[:3]", where="r.identifier == 'str'") == "gur"


def test_str_10(db, vsql_data):
	assert expr(db, "r.v_str[:-1]", where="r.identifier == 'str'") == "gur"


def test_str_11(db, vsql_data):
	assert expr(db, "r.v_str[:10]", where="r.identifier == 'str'") == "gurk"


def test_str_12(db, vsql_data):
	assert expr(db, "r.v_str[:-5]", where="r.identifier == 'str'") is None


def test_str_13(db, vsql_data):
	assert expr(db, "r.v_str[:]", where="r.identifier == 'str'") == "gurk"


def test_str_14(db, vsql_data):
	assert expr(db, "r.v_str[None:None]", where="r.identifier == 'str'") == "gurk"


def test_intlist_1(db, vsql_data):
	assert expr(db, f"{int_list}[1:3]") == [2, 3]


def test_intlist_2(db, vsql_data):
	assert expr(db, f"{int_list}[-3:-1]") == [2, 3]


def test_intlist_3(db, vsql_data):
	assert expr(db, f"{int_list}[4:10]") == []


def test_intlist_4(db, vsql_data):
	assert expr(db, f"{int_list}[-10:-5]") == []


def test_intlist_5(db, vsql_data):
	assert expr(db, f"{int_list}[1:]") == [2, 3, 4]


def test_intlist_6(db, vsql_data):
	assert expr(db, f"{int_list}[-3:]") == [2, 3, 4]


def test_intlist_7(db, vsql_data):
	assert expr(db, f"{int_list}[4:]") == []


def test_intlist_8(db, vsql_data):
	assert expr(db, f"{int_list}[-10:]") == [1, 2, 3, 4]


def test_intlist_9(db, vsql_data):
	assert expr(db, f"{int_list}[:3]") == [1, 2, 3]


def test_intlist_10(db, vsql_data):
	assert expr(db, f"{int_list}[:-1]") == [1, 2, 3]


def test_intlist_11(db, vsql_data):
	assert expr(db, f"{int_list}[:10]") == [1, 2, 3, 4]


def test_intlist_12(db, vsql_data):
	assert expr(db, f"{int_list}[:-5]") == []


def test_intlist_13(db, vsql_data):
	assert expr(db, f"{int_list}[:]") == [1, 2, 3, 4]


def test_intlist_14(db, vsql_data):
	assert expr(db, f"{int_list}[None:None]") == [1, 2, 3, 4]


def test_numberlist_1(db, vsql_data):
	assert expr(db, f"{number_list}[1:3]") == [2.2, 3.3]


def test_numberlist_2(db, vsql_data):
	assert expr(db, f"{number_list}[-3:-1]") == [2.2, 3.3]


def test_numberlist_3(db, vsql_data):
	assert expr(db, f"{number_list}[4:10]") == []


def test_numberlist_4(db, vsql_data):
	assert expr(db, f"{number_list}[-10:-5]") == []


def test_numberlist_5(db, vsql_data):
	assert expr(db, f"{number_list}[1:]") == [2.2, 3.3, 4.4]


def test_numberlist_6(db, vsql_data):
	assert expr(db, f"{number_list}[-3:]") == [2.2, 3.3, 4.4]


def test_numberlist_7(db, vsql_data):
	assert expr(db, f"{number_list}[4:]") == []


def test_numberlist_8(db, vsql_data):
	assert expr(db, f"{number_list}[-10:]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_9(db, vsql_data):
	assert expr(db, f"{number_list}[:3]") == [1.1, 2.2, 3.3]


def test_numberlist_10(db, vsql_data):
	assert expr(db, f"{number_list}[:-1]") == [1.1, 2.2, 3.3]


def test_numberlist_11(db, vsql_data):
	assert expr(db, f"{number_list}[:10]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_12(db, vsql_data):
	assert expr(db, f"{number_list}[:-5]") == []


def test_numberlist_13(db, vsql_data):
	assert expr(db, f"{number_list}[:]") == [1.1, 2.2, 3.3, 4.4]


def test_numberlist_14(db, vsql_data):
	assert expr(db, f"{number_list}[None:None]") == [1.1, 2.2, 3.3, 4.4]


def test_datelist_1(db, vsql_data):
	assert expr(db, f"{date_list}[1:3]") == [d2, d3]


def test_datelist_2(db, vsql_data):
	assert expr(db, f"{date_list}[-3:-1]") == [d2, d3]


def test_datelist_3(db, vsql_data):
	assert expr(db, f"{date_list}[4:10]") == []


def test_datelist_4(db, vsql_data):
	assert expr(db, f"{date_list}[-10:-5]") == []


def test_datelist_5(db, vsql_data):
	assert expr(db, f"{date_list}[1:]") == [d2, d3, d4]


def test_datelist_6(db, vsql_data):
	assert expr(db, f"{date_list}[-3:]") == [d2, d3, d4]


def test_datelist_7(db, vsql_data):
	assert expr(db, f"{date_list}[4:]") == []


def test_datelist_8(db, vsql_data):
	assert expr(db, f"{date_list}[-10:]") == [d1, d2, d3, d4]


def test_datelist_9(db, vsql_data):
	assert expr(db, f"{date_list}[:3]") == [d1, d2, d3]


def test_datelist_10(db, vsql_data):
	assert expr(db, f"{date_list}[:-1]") == [d1, d2, d3]


def test_datelist_11(db, vsql_data):
	assert expr(db, f"{date_list}[:10]") == [d1, d2, d3, d4]


def test_datelist_12(db, vsql_data):
	assert expr(db, f"{date_list}[:-5]") == []


def test_datelist_13(db, vsql_data):
	assert expr(db, f"{date_list}[:]") == [d1, d2, d3, d4]


def test_datelist_14(db, vsql_data):
	assert expr(db, f"{date_list}[None:None]") == [d1, d2, d3, d4]


def test_datetimelist_1(db, vsql_data):
	assert expr(db, f"{datetime_list}[1:3]") == [dt2, dt3]


def test_datetimelist_2(db, vsql_data):
	assert expr(db, f"{datetime_list}[-3:-1]") == [dt2, dt3]


def test_datetimelist_3(db, vsql_data):
	assert expr(db, f"{datetime_list}[4:10]") == []


def test_datetimelist_4(db, vsql_data):
	assert expr(db, f"{datetime_list}[-10:-5]") == []


def test_datetimelist_5(db, vsql_data):
	assert expr(db, f"{datetime_list}[1:]") == [dt2, dt3, dt4]


def test_datetimelist_6(db, vsql_data):
	assert expr(db, f"{datetime_list}[-3:]") == [dt2, dt3, dt4]


def test_datetimelist_7(db, vsql_data):
	assert expr(db, f"{datetime_list}[4:]") == []


def test_datetimelist_8(db, vsql_data):
	assert expr(db, f"{datetime_list}[-10:]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_9(db, vsql_data):
	assert expr(db, f"{datetime_list}[:3]") == [dt1, dt2, dt3]


def test_datetimelist_10(db, vsql_data):
	assert expr(db, f"{datetime_list}[:-1]") == [dt1, dt2, dt3]


def test_datetimelist_11(db, vsql_data):
	assert expr(db, f"{datetime_list}[:10]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_12(db, vsql_data):
	assert expr(db, f"{datetime_list}[:-5]") == []


def test_datetimelist_13(db, vsql_data):
	assert expr(db, f"{datetime_list}[:]") == [dt1, dt2, dt3, dt4]


def test_datetimelist_14(db, vsql_data):
	assert expr(db, f"{datetime_list}[None:None]") == [dt1, dt2, dt3, dt4]


def test_nulllist_1(db, vsql_data):
	assert expr(db, f"[None, None, None, None][1:3]") == 2


def test_nulllist_2(db, vsql_data):
	assert expr(db, f"[None, None, None, None][-3:-1]") == 2


def test_nulllist_3(db, vsql_data):
	assert expr(db, f"[None, None, None, None][4:10]") == 0


def test_nulllist_4(db, vsql_data):
	assert expr(db, f"[None, None, None, None][-10:-5]") == 0


def test_nulllist_5(db, vsql_data):
	assert expr(db, f"[None, None, None, None][1:]") == 3


def test_nulllist_6(db, vsql_data):
	assert expr(db, f"[None, None, None, None][-3:]") == 3


def test_nulllist_7(db, vsql_data):
	assert expr(db, f"[None, None, None, None][4:]") == 0


def test_nulllist_8(db, vsql_data):
	assert expr(db, f"[None, None, None, None][-10:]") == 4


def test_nulllist_9(db, vsql_data):
	assert expr(db, f"[None, None, None, None][:3]") == 3


def test_nulllist_10(db, vsql_data):
	assert expr(db, f"[None, None, None, None][:-1]") == 3


def test_nulllist_11(db, vsql_data):
	assert expr(db, f"[None, None, None, None][:10]") == 4


def test_nulllist_12(db, vsql_data):
	assert expr(db, f"[None, None, None, None][:-5]") == 0


def test_nulllist_13(db, vsql_data):
	assert expr(db, f"[None, None, None, None][:]") == 4


def test_nulllist_14(db, vsql_data):
	assert expr(db, f"[None, None, None, None][None:None]") == 4


def test_nulllist_15(db, vsql_data):
	assert expr(db, f"[][:]") == 0
