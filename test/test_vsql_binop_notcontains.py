"""
Tests for the vSQL binary inverted containment test operator ``not in``.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

d1 = "@(2000-02-29)"

dt1 = "@(2000-02-29T12:34:56)"

def test_null_intlist1(db, vsql_data):
	assert expr(db, "None not in [1, 2]") == 1


def test_null_intlist2(db, vsql_data):
	assert expr(db, "None not in [1, None, 2]") == 0


def test_null_numberlist1(db, vsql_data):
	assert expr(db, "None not in [1.1, 2.2]") == 1


def test_null_numberlist2(db, vsql_data):
	assert expr(db, "None not in [1.1, None, 2.2]") == 0


def test_null_strlist1(db, vsql_data):
	assert expr(db, "None not in ['foo', 'bar']") == 1


def test_null_strlist2(db, vsql_data):
	assert expr(db, "None not in ['foo', None, 'bar']") == 0


def test_null_datelist1(db, vsql_data):
	assert expr(db, "None not in [@(2000-02-29), @(2000-03-01)]") == 1


def test_null_datelist2(db, vsql_data):
	assert expr(db, "None not in [@(2000-02-29), None, @(2000-03-01)]") == 0


def test_null_datetimelist1(db, vsql_data):
	assert expr(db, "None not in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 1


def test_null_datetimelist2(db, vsql_data):
	assert expr(db, "None not in [@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56)]") == 0


def test_str_str1(db, vsql_data):
	assert expr(db, "'az' not in r.v_str", where="r.identifier == 'str'") == 1


def test_str_str2(db, vsql_data):
	assert expr(db, "'ur' not in r.v_str", where="r.identifier == 'str'") == 0


def test_str_clob1(db, vsql_data):
	assert expr(db, "'az' not in r.v_clob", where="r.identifier == 'clob'") == 1


def test_str_clob2(db, vsql_data):
	assert expr(db, "'rkgurkgu' not in r.v_clob", where="r.identifier == 'clob'") == 0


def test_str_strlist1(db, vsql_data):
	assert expr(db, "'hinz' not in ['gurk', 'hurz']") == 1


def test_str_strlist2(db, vsql_data):
	assert expr(db, "'hurz' not in ['gurk', 'hurz']") == 0


def test_str_cloblist1(db, vsql_data):
	assert expr(db, "'hinz' not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist2(db, vsql_data):
	assert expr(db, "'rkgurkgu' not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist3(db, vsql_data):
	assert expr(db, "'gurk' not in ['hurz', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist4(db, vsql_data):
	assert expr(db, "'gurk' not in ['hurz', r.v_clob]", where="r.identifier == 'shortclob'") == 0


def test_clob_strlist1(db, vsql_data):
	assert expr(db, "r.v_clob not in ['hinz', 'kunz']", where="r.identifier == 'clob'") == 1


def test_clob_strlist2(db, vsql_data):
	assert expr(db, "r.v_clob not in ['gurk', 'hurz']", where="r.identifier == 'clob'") == 1


def test_clob_cloblist1(db, vsql_data):
	assert expr(db, "r.v_clob not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 0


def test_str_strset1(db, vsql_data):
	assert expr(db, "'hinz' not in {'gurk', 'hurz'}") == 1


def test_str_strset2(db, vsql_data):
	assert expr(db, "'hurz' not in {'gurk', 'hurz'}") == 0


def test_int_intlist1(db, vsql_data):
	assert expr(db, "1 not in [2, 3]") == 1


def test_int_intlist2(db, vsql_data):
	assert expr(db, "3 not in [1, 2, 3]") == 0


def test_int_numberlist1(db, vsql_data):
	assert expr(db, "1 not in [2.2, 3.3]") == 1


def test_int_numberlist2(db, vsql_data):
	assert expr(db, "3 not in [1.1, 2.2, 3.0]") == 0


def test_int_intset1(db, vsql_data):
	assert expr(db, "1 not in {2, 3}") == 1


def test_int_intset2(db, vsql_data):
	assert expr(db, "3 not in {1, 2, 3}") == 0


def test_int_numberset1(db, vsql_data):
	assert expr(db, "1 not in {2.2, 3.3}") == 1


def test_int_numberset2(db, vsql_data):
	assert expr(db, "3 not in {1.1, 2.2, 3.0}") == 0


def test_number_intlist1(db, vsql_data):
	assert expr(db, "1.0 not in [2, 3]") == 1


def test_number_intlist2(db, vsql_data):
	assert expr(db, "3.0 not in [1, 2, 3]") == 0


def test_number_numberlist1(db, vsql_data):
	assert expr(db, "1.0 not in [2.2, 3.3]") == 1


def test_number_numberlist2(db, vsql_data):
	assert expr(db, "3.0 not in [1.1, 2.2, 3.0]") == 0


def test_number_intset1(db, vsql_data):
	assert expr(db, "1.0 not in {2, 3}") == 1


def test_number_intset2(db, vsql_data):
	assert expr(db, "3.0 not in {1, 2, 3}") == 0


def test_number_numberset1(db, vsql_data):
	assert expr(db, "1.0 not in {2.2, 3.3}") == 1


def test_number_numberset2(db, vsql_data):
	assert expr(db, "3.3 not in {1.1, 2.2, 3.3}") == 0


def test_date_datelist1(db, vsql_data):
	assert expr(db, "@(2000-02-29) not in [@(2000-02-28), @(2000-03-01)]") == 1


def test_date_datelist2(db, vsql_data):
	assert expr(db, "@(2000-02-29) not in [@(2000-02-29), @(2000-03-01)]") == 0


def test_date_dateset1(db, vsql_data):
	assert expr(db, "@(2000-02-29) not in {@(2000-02-28), @(2000-03-01)}") == 1


def test_date_dateset2(db, vsql_data):
	assert expr(db, "@(2000-02-29) not in {@(2000-02-29), @(2000-03-01)}") == 0


def test_datetime_datetimelist1(db, vsql_data):
	assert expr(db, "@(2000-02-29T12:34:56) not in [@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)]") == 1


def test_datetime_datetimelist2(db, vsql_data):
	assert expr(db, "@(2000-02-29T12:34:56) not in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 0


def test_datetime_datetimeset1(db, vsql_data):
	assert expr(db, "@(2000-02-29T12:34:56) not in {@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)}") == 1


def test_datetime_datetimeset2(db, vsql_data):
	assert expr(db, "@(2000-02-29T12:34:56) not in {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}") == 0


def test_null_nulllist1(db, vsql_data):
	assert expr(db, "None not in []") == 1


def test_null_nulllist2(db, vsql_data):
	assert expr(db, "None not in [None, None]") == 0


def test_int_nulllist1(db, vsql_data):
	assert expr(db, "r.v_int not in []", where="r.identifier == 'none'") == 1


def test_int_nulllist2(db, vsql_data):
	assert expr(db, "r.v_int not in [None]", where="r.identifier == 'none'") == 0


def test_int_nulllist3(db, vsql_data):
	assert expr(db, "1 not in [None]") == 1


def test_number_nulllist1(db, vsql_data):
	assert expr(db, "r.v_number not in []", where="r.identifier == 'none'") == 1


def test_number_nulllist2(db, vsql_data):
	assert expr(db, "r.v_number not in [None]", where="r.identifier == 'none'") == 0


def test_number_nulllist3(db, vsql_data):
	assert expr(db, "1.1 not in [None]") == 1


def test_str_nulllist1(db, vsql_data):
	assert expr(db, "r.v_str not in []", where="r.identifier == 'none'") == 1


def test_str_nulllist2(db, vsql_data):
	assert expr(db, "r.v_str not in [None]", where="r.identifier == 'none'") == 0


def test_str_nulllist3(db, vsql_data):
	assert expr(db, "'gurk' not in [None]") == 1


def test_clob_nulllist1(db, vsql_data):
	assert expr(db, "r.v_clob not in []", where="r.identifier == 'none'") == 1


def test_clob_nulllist2(db, vsql_data):
	assert expr(db, "r.v_clob not in [None]", where="r.identifier == 'none'") == 0


def test_clob_nulllist3(db, vsql_data):
	assert expr(db, "r.v_clob not in [None]", where="r.identifier == 'clob'") == 1


def test_date_nulllist1(db, vsql_data):
	assert expr(db, f"[None, {d1}][0] not in []") == 1


def test_date_nulllist2(db, vsql_data):
	assert expr(db, f"[None, {d1}][0] not in [None]") == 0


def test_date_nulllist3(db, vsql_data):
	assert expr(db, f"{d1} not in [None]") == 1


def test_datetime_nulllist1(db, vsql_data):
	assert expr(db, f"[None, {dt1}][0] not in []") == 1


def test_datetime_nulllist2(db, vsql_data):
	assert expr(db, f"[None, {dt1}][0] not in [None]") == 0


def test_datetime_nulllist3(db, vsql_data):
	assert expr(db, f"{dt1} not in [None]") == 1
