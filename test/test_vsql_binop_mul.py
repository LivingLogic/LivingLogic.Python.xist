"""
Tests for the vSQL multiplication operator ``*``.

To run the tests, :mod:`pytest` is required.
"""

import datetime


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * True", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * True", where="r.identifier == 'bool_true'") == 1


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * 1", where="r.identifier == 'bool_true'") == 1


def test_bool_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * 1.5", where="r.identifier == 'bool_true'") == 1.5


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_bool", where="r.identifier == 'bool_true'") == 2


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_int", where="r.identifier == 'int'") == 3552


def test_int_number(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_number", where="r.identifier == 'number'") == 85.0


def test_number_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number * True", where="r.identifier == 'number'") == 42.5


def test_number_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number * 2", where="r.identifier == 'number'") == 85.0


def test_number_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number * 1.5", where="r.identifier == 'number'") == 63.75


def test_bool_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_str", where="r.identifier == 'none'") is None


def test_bool_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_str", where="r.identifier == 'bool_false'") is None


def test_bool_str3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_str", where="r.identifier == 'bool_false'") is None


def test_bool_str4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_str", where="r.identifier == 'str'") is None


def test_bool_str5(vsql_db, vsql_data):
	assert vsql_db.expr("False * r.v_str", where="r.identifier == 'str'") is None


def test_bool_str6(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_str", where="r.identifier == 'str'") == "gurk"


def test_int_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * r.v_str", where="r.identifier == 'none'") is None


def test_int_str2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_str", where="r.identifier == 'none'") is None


def test_int_str3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * r.v_str", where="r.identifier == 'str'") is None


def test_int_str4(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_str", where="r.identifier == 'str'") == "gurkgurk"


def test_bool_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_clob", where="r.identifier == 'none'") is None


def test_bool_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_clob", where="r.identifier == 'bool_false'") is None


def test_bool_clob3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_clob", where="r.identifier == 'bool_false'") is None


def test_bool_clob4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * r.v_clob", where="r.identifier == 'clob'") is None


def test_bool_clob5(vsql_db, vsql_data):
	result = vsql_db.expr("False * r.v_clob", where="r.identifier == 'clob'")
	assert result is None or result == ""


def test_bool_clob6(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_clob", where="r.identifier == 'clob'") == "gurk" * 100000


def test_int_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * r.v_clob", where="r.identifier == 'none'") is None


def test_int_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_clob", where="r.identifier == 'none'") is None


def test_int_clob3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * r.v_clob", where="r.identifier == 'clob'") is None


def test_int_clob4(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_clob", where="r.identifier == 'clob'") == "gurk" * 200000


def test_bool_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * days(3)", where="r.identifier == 'none'") is None


def test_bool_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_datedelta", where="r.identifier == 'none'") is None


def test_bool_datedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_datedelta", where="r.identifier == 'datedelta'") == vsql_db.type_for_datedelta(12)


def test_int_datedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * days(3)", where="r.identifier == 'none'") is None


def test_int_datedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_datedelta", where="r.identifier == 'none'") is None


def test_int_datedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_datedelta", where="r.identifier == 'datedelta'") == vsql_db.type_for_datedelta(24)


def test_bool_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * minutes(3)", where="r.identifier == 'none'") is None


def test_bool_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_bool_datetimedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == vsql_db.type_for_datetimedelta(1, (12 * 60 + 34) * 60 + 56)


def test_int_datetimedelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * minutes(3)", where="r.identifier == 'none'") is None


def test_int_datetimedelta2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_int_datetimedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == vsql_db.type_for_datetimedelta(2, 2 * ((12 * 60 + 34) * 60 + 56))


def test_bool_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * months(3)", where="r.identifier == 'none'") is None


def test_bool_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_monthdelta", where="r.identifier == 'none'") is None


def test_bool_monthdelta3(vsql_db, vsql_data):
	assert vsql_db.expr("True * r.v_monthdelta", where="r.identifier == 'monthdelta'") == vsql_db.type_for_monthdelta(3)


def test_int_monthdelta1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * months(3)", where="r.identifier == 'none'") is None


def test_int_monthdelta2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_monthdelta", where="r.identifier == 'none'") is None


def test_int_monthdelta3(vsql_db, vsql_data):
	assert vsql_db.expr("2 * r.v_monthdelta", where="r.identifier == 'monthdelta'") == vsql_db.type_for_monthdelta(6)


def test_number_datetimedelta3(vsql_db, vsql_data):
	assert vsql_db.expr("2.5 * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == vsql_db.type_for_datetimedelta(0, round(2.5 * (86400 + (12 * 60 + 34) * 60 + 56)))


def test_str_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * r.v_bool", where="r.identifier == 'none'") is None


def test_str_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * False", where="r.identifier == 'none'") is None


def test_str_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * True", where="r.identifier == 'none'") is None


def test_str_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * r.v_bool", where="r.identifier == 'str'") is None


def test_str_bool5(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * False", where="r.identifier == 'str'") is None


def test_str_bool6(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * True", where="r.identifier == 'str'") == "gurk"


def test_str_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * r.v_int", where="r.identifier == 'none'") is None


def test_str_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * 2", where="r.identifier == 'none'") is None


def test_str_int3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str * r.v_int", where="r.identifier == 'str'") is None


def test_clob_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob * True", where="r.identifier == 'none'") is None


def test_clob_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob * True", where="r.identifier == 'shortclob'") == "gurk"


def test_clob_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob * 2", where="r.identifier == 'none'") is None


def test_clob_int2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob * 2", where="r.identifier == 'shortclob'") == "gurkgurk"


def test_bool_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * [1, 2, 3]", where="r.identifier == 'none'") is None


def test_bool_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * [1, 2, 3]", where="r.identifier == 'bool_false'") == []


def test_bool_intlist3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool * [1, 2, 3]", where="r.identifier == 'bool_true'") == [1, 2, 3]


def test_int_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int * [1, 2, 3]", where="r.identifier == 'none'") is None


def test_int_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * [1, 2, 3]") == [1, 2, 3, 1, 2, 3]


def test_bool_numberlist(vsql_db, vsql_data):
	assert vsql_db.expr("True * [1.5, 2.5]") == [1.5, 2.5]


def test_bool_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("True * ['gurk', 'hurz']") == ['gurk', 'hurz']


def test_bool_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("True * [r.v_clob]", where="r.identifier == 'shortclob'") == ['gurk']


def test_bool_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("True * [@(2000-02-29), @(2000-03-01)]") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1)]


def test_bool_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("True * [@(2000-02-29T12:34:56)]") == [datetime.datetime(2000, 2, 29, 12, 34, 56)]


def test_int_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("2 * ['gurk', 'hurz']") == ['gurk', 'hurz', 'gurk', 'hurz']


def test_int_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("2 * [r.v_clob]", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_int_datelist(vsql_db, vsql_data):
	assert vsql_db.expr("2 * [@(2000-02-29)]") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 2, 29)]


def test_int_datetimelist(vsql_db, vsql_data):
	assert vsql_db.expr("2 * [@(2000-02-29T12:34:56)]") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 12, 34, 56)]


def test_bool_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("False * []") == 0


def test_bool_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("True * []") == 0


def test_bool_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("False * [None, None]") == 0


def test_bool_nulllist4(vsql_db, vsql_data):
	assert vsql_db.expr("True * [None, None]") == 2


def test_int_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("0 * []") == 0


def test_int_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("2 * []") == 0


def test_int_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("0 * [None, None]") == 0


def test_int_nulllist4(vsql_db, vsql_data):
	assert vsql_db.expr("2 * [None, None]") == 4


def test_nulllist1_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[] * False") == 0


def test_nulllist2_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[] * True") == 0


def test_nulllist3_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] * False") == 0


def test_nulllist4_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] * True") == 2


def test_nulllist1_int(vsql_db, vsql_data):
	assert vsql_db.expr("[] * 0") == 0


def test_nulllist2_int(vsql_db, vsql_data):
	assert vsql_db.expr("[] * 2") == 0


def test_nulllist3_int(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] * 0") == 0


def test_nulllist4_int(vsql_db, vsql_data):
	assert vsql_db.expr("[None, None] * 2") == 4


def test_intlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] * True") == [1, 2]


def test_intlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] * 2") == [1, 2, 1, 2]


def test_numberlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] * True") == [1.5, 2.5]


def test_numberlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[1.5, 2.5] * 2") == [1.5, 2.5, 1.5, 2.5]


def test_strlist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] * True") == ['gurk', 'hurz']


def test_strlist_int(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] * 2") == ['gurk', 'hurz', 'gurk', 'hurz']


def test_cloblist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] * True", where="r.identifier == 'shortclob'") == ['gurk']


def test_cloblist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] * 2", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_datelist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29), @(2000-03-01)] * True") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 3, 1)]


def test_datelist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] * 2") == [vsql_db.type_for_date(2000, 2, 29), vsql_db.type_for_date(2000, 2, 29)]


def test_datetimelist_bool(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] * True") == [datetime.datetime(2000, 2, 29, 12, 34, 56)]


def test_datetimelist_int(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] * 2") == [datetime.datetime(2000, 2, 29, 12, 34, 56), datetime.datetime(2000, 2, 29, 12, 34, 56)]