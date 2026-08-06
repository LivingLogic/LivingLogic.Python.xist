"""
Tests for the vSQL binary inverted containment test operator ``not in``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

d1 = "@(2000-02-29)"

dt1 = "@(2000-02-29T12:34:56)"

def test_null_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [1, 2]") == 1


def test_null_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [1, None, 2]") == 0


def test_null_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [1.1, 2.2]") == 1


def test_null_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [1.1, None, 2.2]") == 0


def test_null_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in ['foo', 'bar']") == 1


def test_null_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in ['foo', None, 'bar']") == 0


def test_null_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [@(2000-02-29), @(2000-03-01)]") == 1


def test_null_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [@(2000-02-29), None, @(2000-03-01)]") == 0


def test_null_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 1


def test_null_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56)]") == 0


def test_str_str1(vsql_db, vsql_data):
	assert vsql_db.expr("'az' not in r.v_str", where="r.identifier == 'str'") == 1


def test_str_str2(vsql_db, vsql_data):
	assert vsql_db.expr("'ur' not in r.v_str", where="r.identifier == 'str'") == 0


def test_str_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("'az' not in r.v_clob", where="r.identifier == 'clob'") == 1


def test_str_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("'rkgurkgu' not in r.v_clob", where="r.identifier == 'clob'") == 0


def test_str_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' not in ['gurk', 'hurz']") == 1


def test_str_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' not in ['gurk', 'hurz']") == 0


def test_str_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist2(vsql_db, vsql_data):
	assert vsql_db.expr("'rkgurkgu' not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist3(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' not in ['hurz', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_cloblist4(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' not in ['hurz', r.v_clob]", where="r.identifier == 'shortclob'") == 0


def test_clob_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in ['hinz', 'kunz']", where="r.identifier == 'clob'") == 1


def test_clob_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in ['gurk', 'hurz']", where="r.identifier == 'clob'") == 1


def test_clob_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 0


def test_str_strset1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' not in {'gurk', 'hurz'}") == 1


def test_str_strset2(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' not in {'gurk', 'hurz'}") == 0


def test_int_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1 not in [2, 3]") == 1


def test_int_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3 not in [1, 2, 3]") == 0


def test_int_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1 not in [2.2, 3.3]") == 1


def test_int_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3 not in [1.1, 2.2, 3.0]") == 0


def test_int_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("1 not in {2, 3}") == 1


def test_int_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("3 not in {1, 2, 3}") == 0


def test_int_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("1 not in {2.2, 3.3}") == 1


def test_int_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("3 not in {1.1, 2.2, 3.0}") == 0


def test_number_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 not in [2, 3]") == 1


def test_number_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 not in [1, 2, 3]") == 0


def test_number_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 not in [2.2, 3.3]") == 1


def test_number_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 not in [1.1, 2.2, 3.0]") == 0


def test_number_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 not in {2, 3}") == 1


def test_number_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 not in {1, 2, 3}") == 0


def test_number_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 not in {2.2, 3.3}") == 1


def test_number_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("3.3 not in {1.1, 2.2, 3.3}") == 0


def test_date_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) not in [@(2000-02-28), @(2000-03-01)]") == 1


def test_date_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) not in [@(2000-02-29), @(2000-03-01)]") == 0


def test_date_dateset1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) not in {@(2000-02-28), @(2000-03-01)}") == 1


def test_date_dateset2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) not in {@(2000-02-29), @(2000-03-01)}") == 0


def test_datetime_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) not in [@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)]") == 1


def test_datetime_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) not in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 0


def test_datetime_datetimeset1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) not in {@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)}") == 1


def test_datetime_datetimeset2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) not in {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}") == 0


def test_null_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("None not in []") == 1


def test_null_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("None not in [None, None]") == 0


def test_int_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int not in []", where="r.identifier == 'none'") == 1


def test_int_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int not in [None]", where="r.identifier == 'none'") == 0


def test_int_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("1 not in [None]") == 1


def test_number_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number not in []", where="r.identifier == 'none'") == 1


def test_number_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number not in [None]", where="r.identifier == 'none'") == 0


def test_number_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("1.1 not in [None]") == 1


def test_str_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str not in []", where="r.identifier == 'none'") == 1


def test_str_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str not in [None]", where="r.identifier == 'none'") == 0


def test_str_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' not in [None]") == 1


def test_clob_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in []", where="r.identifier == 'none'") == 1


def test_clob_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in [None]", where="r.identifier == 'none'") == 0


def test_clob_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob not in [None]", where="r.identifier == 'clob'") == 1


def test_date_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {d1}][0] not in []") == 1


def test_date_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {d1}][0] not in [None]") == 0


def test_date_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{d1} not in [None]") == 1


def test_datetime_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {dt1}][0] not in []") == 1


def test_datetime_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {dt1}][0] not in [None]") == 0


def test_datetime_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{dt1} not in [None]") == 1
