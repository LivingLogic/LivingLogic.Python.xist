"""
Tests for the vSQL multiplication operator ``*``.

The test are done via the Python DB interface.

To run the tests, :mod:`pytest` is required.
"""

import datetime
from conftest import *


###
### Tests
###


def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_int * True", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool * True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool * True", where="r.identifier == 'bool_true'") == 1


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool * 1", where="r.identifier == 'bool_true'") == 1


def test_bool_number(db, vsql_data):
	assert expr(db, "r.v_bool * 1.5", where="r.identifier == 'bool_true'") == 1.5


def test_int_bool(db, vsql_data):
	assert expr(db, "2 * r.v_bool", where="r.identifier == 'bool_true'") == 2


def test_int_int(db, vsql_data):
	assert expr(db, "2 * r.v_int", where="r.identifier == 'int'") == 3552


def test_int_number(db, vsql_data):
	assert expr(db, "2 * r.v_number", where="r.identifier == 'number'") == 85.0


def test_number_bool(db, vsql_data):
	assert expr(db, "r.v_number * True", where="r.identifier == 'number'") == 42.5


def test_number_int(db, vsql_data):
	assert expr(db, "r.v_number * 2", where="r.identifier == 'number'") == 85.0


def test_number_number(db, vsql_data):
	assert expr(db, "r.v_number * 1.5", where="r.identifier == 'number'") == 63.75


def test_bool_str1(db, vsql_data):
	assert expr(db, "r.v_bool * r.v_str", where="r.identifier == 'none'") is None


def test_bool_str2(db, vsql_data):
	assert expr(db, "r.v_bool * r.v_str", where="r.identifier == 'bool_false'") is None


def test_bool_str3(db, vsql_data):
	assert expr(db, "r.v_bool * r.v_str", where="r.identifier == 'bool_false'") is None


def test_bool_str4(db, vsql_data):
	assert expr(db, "r.v_bool * r.v_str", where="r.identifier == 'str'") is None


def test_bool_str5(db, vsql_data):
	assert expr(db, "False * r.v_str", where="r.identifier == 'str'") is None


def test_bool_str6(db, vsql_data):
	assert expr(db, "True * r.v_str", where="r.identifier == 'str'") == "gurk"


def test_int_str1(db, vsql_data):
	assert expr(db, "r.v_int * r.v_str", where="r.identifier == 'none'") is None


def test_int_str2(db, vsql_data):
	assert expr(db, "2 * r.v_str", where="r.identifier == 'none'") is None


def test_int_str3(db, vsql_data):
	assert expr(db, "r.v_int * r.v_str", where="r.identifier == 'str'") is None


def test_int_str4(db, vsql_data):
	assert expr(db, "2 * r.v_str", where="r.identifier == 'str'") == "gurkgurk"


def test_bool_datedelta1(db, vsql_data):
	assert expr(db, "r.v_bool * days(3)", where="r.identifier == 'none'") is None


def test_bool_datedelta2(db, vsql_data):
	assert expr(db, "True * r.v_datedelta", where="r.identifier == 'none'") is None


def test_bool_datedelta3(db, vsql_data):
	assert expr(db, "True * r.v_datedelta", where="r.identifier == 'datedelta'") == 12


def test_int_datedelta1(db, vsql_data):
	assert expr(db, "r.v_int * days(3)", where="r.identifier == 'none'") is None


def test_int_datedelta2(db, vsql_data):
	assert expr(db, "2 * r.v_datedelta", where="r.identifier == 'none'") is None


def test_int_datedelta3(db, vsql_data):
	assert expr(db, "2 * r.v_datedelta", where="r.identifier == 'datedelta'") == 24


def test_bool_datetimedelta1(db, vsql_data):
	assert expr(db, "r.v_bool * minutes(3)", where="r.identifier == 'none'") is None


def test_bool_datetimedelta2(db, vsql_data):
	assert expr(db, "True * r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_bool_datetimedelta3(db, vsql_data):
	assert expr(db, "True * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == 1 + 12/24 + 34/24/60 + 56/24/60/60


def test_int_datetimedelta1(db, vsql_data):
	assert expr(db, "r.v_int * minutes(3)", where="r.identifier == 'none'") is None


def test_int_datetimedelta2(db, vsql_data):
	assert expr(db, "2 * r.v_datetimedelta", where="r.identifier == 'none'") is None


def test_int_datetimedelta3(db, vsql_data):
	assert expr(db, "2 * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == 2 * (1 + 12/24 + 34/24/60 + 56/24/60/60)


def test_bool_monthdelta1(db, vsql_data):
	assert expr(db, "r.v_bool * months(3)", where="r.identifier == 'none'") is None


def test_bool_monthdelta2(db, vsql_data):
	assert expr(db, "True * r.v_monthdelta", where="r.identifier == 'none'") is None


def test_bool_monthdelta3(db, vsql_data):
	assert expr(db, "True * r.v_monthdelta", where="r.identifier == 'monthdelta'") == 3


def test_int_monthdelta1(db, vsql_data):
	assert expr(db, "r.v_int * months(3)", where="r.identifier == 'none'") is None


def test_int_monthdelta2(db, vsql_data):
	assert expr(db, "2 * r.v_monthdelta", where="r.identifier == 'none'") is None


def test_int_monthdelta3(db, vsql_data):
	assert expr(db, "2 * r.v_monthdelta", where="r.identifier == 'monthdelta'") == 6


def test_number_datetimedelta3(db, vsql_data):
	assert expr(db, "2.5 * r.v_datetimedelta", where="r.identifier == 'datetimedelta'") == 2.5 * (1 + 12/24 + 34/24/60 + 56/24/60/60)


def test_str_bool1(db, vsql_data):
	assert expr(db, "r.v_str * r.v_bool", where="r.identifier == 'none'") is None


def test_str_bool2(db, vsql_data):
	assert expr(db, "r.v_str * False", where="r.identifier == 'none'") is None


def test_str_bool3(db, vsql_data):
	assert expr(db, "r.v_str * True", where="r.identifier == 'none'") is None


def test_str_bool4(db, vsql_data):
	assert expr(db, "r.v_str * r.v_bool", where="r.identifier == 'str'") is None


def test_str_bool5(db, vsql_data):
	assert expr(db, "r.v_str * False", where="r.identifier == 'str'") is None


def test_str_bool6(db, vsql_data):
	assert expr(db, "r.v_str * True", where="r.identifier == 'str'") == "gurk"


def test_str_int1(db, vsql_data):
	assert expr(db, "r.v_str * r.v_int", where="r.identifier == 'none'") is None


def test_str_int2(db, vsql_data):
	assert expr(db, "r.v_str * 2", where="r.identifier == 'none'") is None


def test_str_int3(db, vsql_data):
	assert expr(db, "r.v_str * r.v_int", where="r.identifier == 'str'") is None


def test_bool_intlist1(db, vsql_data):
	assert expr(db, "r.v_bool * [1, 2, 3]", where="r.identifier == 'none'") is None


def test_bool_intlist2(db, vsql_data):
	assert expr(db, "r.v_bool * [1, 2, 3]", where="r.identifier == 'bool_false'") == []


def test_bool_intlist3(db, vsql_data):
	assert expr(db, "r.v_bool * [1, 2, 3]", where="r.identifier == 'bool_true'") == [1, 2, 3]


def test_int_intlist1(db, vsql_data):
	assert expr(db, "r.v_int * [1, 2, 3]", where="r.identifier == 'none'") is None


def test_int_intlist2(db, vsql_data):
	assert expr(db, "2 * [1, 2, 3]") == [1, 2, 3, 1, 2, 3]


def test_bool_nulllist1(db, vsql_data):
	assert expr(db, "False * []") == 0


def test_bool_nulllist2(db, vsql_data):
	assert expr(db, "True * []") == 0


def test_bool_nulllist3(db, vsql_data):
	assert expr(db, "False * [None, None]") == 0


def test_bool_nulllist4(db, vsql_data):
	assert expr(db, "True * [None, None]") == 2


def test_int_nulllist1(db, vsql_data):
	assert expr(db, "0 * []") == 0


def test_int_nulllist2(db, vsql_data):
	assert expr(db, "2 * []") == 0


def test_int_nulllist3(db, vsql_data):
	assert expr(db, "0 * [None, None]") == 0


def test_int_nulllist4(db, vsql_data):
	assert expr(db, "2 * [None, None]") == 4


def test_nulllist1_bool(db, vsql_data):
	assert expr(db, "[] * False") == 0


def test_nulllist2_bool(db, vsql_data):
	assert expr(db, "[] * True") == 0


def test_nulllist3_bool(db, vsql_data):
	assert expr(db, "[None, None] * False") == 0


def test_nulllist4_bool(db, vsql_data):
	assert expr(db, "[None, None] * True") == 2


def test_nulllist1_int(db, vsql_data):
	assert expr(db, "[] * 0") == 0


def test_nulllist2_int(db, vsql_data):
	assert expr(db, "[] * 2") == 0


def test_nulllist3_int(db, vsql_data):
	assert expr(db, "[None, None] * 0") == 0


def test_nulllist4_int(db, vsql_data):
	assert expr(db, "[None, None] * 2") == 4