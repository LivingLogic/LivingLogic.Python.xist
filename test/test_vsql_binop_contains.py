"""
Tests for the vSQL binary containment test operator ``in``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

d1 = "@(2000-02-29)"

dt1 = "@(2000-02-29T12:34:56)"


def test_null_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in [1, 2]") == 0


def test_null_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in [1, None, 2]") == 1


def test_null_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in [1.1, 2.2]") == 0


def test_null_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in [1.1, None, 2.2]") == 1


def test_null_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in ['foo', 'bar']") == 0


def test_null_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in ['foo', None, 'bar']") == 1


def test_null_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in ['gurk', r.v_clob]", where="r.identifier == 'shortclob'") == 0


def test_null_cloblist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in ['gurk', None, r.v_clob]", where="r.identifier == 'shortclob'") == 1


def test_null_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in [@(2000-02-29), @(2000-03-01)]") == 0


def test_null_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in [@(2000-02-29), None, @(2000-03-01)]") == 1


def test_null_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 0


def test_null_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in [@(2000-02-29T12:34:56), None, @(2000-03-01T12:34:56)]") == 1


def test_str_str1(vsql_db, vsql_data):
	assert vsql_db.expr("'az' in r.v_str", where="r.identifier == 'str'") == 0


def test_str_str2(vsql_db, vsql_data):
	assert vsql_db.expr("'ur' in r.v_str", where="r.identifier == 'str'") == 1


def test_str_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("'az' in r.v_clob", where="r.identifier == 'clob'") == 0


def test_str_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("'rkgurkgu' in r.v_clob", where="r.identifier == 'clob'") == 1


def test_clob_str1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in 'gu'", where="r.identifier == 'shortclob'") == 0


def test_clob_str2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in 'gurken'", where="r.identifier == 'shortclob'") == 1


def test_clob_clob1(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + 'x') in r.v_clob", where="r.identifier == 'shortclob'") == 0


def test_clob_clob2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in r.v_clob", where="r.identifier == 'shortclob'") == 1


def test_str_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' in ['gurk', 'hurz']") == 0


def test_str_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' in ['gurk', 'hurz']") == 1


def test_str_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 0


def test_str_cloblist2(vsql_db, vsql_data):
	assert vsql_db.expr("'rkgurkgu' in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 0


def test_str_cloblist3(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' in ['hurz', r.v_clob]", where="r.identifier == 'clob'") == 0


def test_str_cloblist4(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' in ['hurz', r.v_clob]", where="r.identifier == 'shortclob'") == 1


def test_clob_strlist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in ['hinz', 'kunz']", where="r.identifier == 'clob'") == 0


def test_clob_strlist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in ['gurk', 'hurz']", where="r.identifier == 'clob'") == 0


def test_clob_cloblist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in ['gurk', r.v_clob]", where="r.identifier == 'clob'") == 1


def test_str_strset1(vsql_db, vsql_data):
	assert vsql_db.expr("'hinz' in {'gurk', 'hurz'}") == 0


def test_str_strset2(vsql_db, vsql_data):
	assert vsql_db.expr("'hurz' in {'gurk', 'hurz'}") == 1


def test_clob_strset1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in {'hinz', 'kunz'}", where="r.identifier == 'shortclob'") == 0


def test_clob_strset2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in {'gurk', 'hurz'}", where="r.identifier == 'shortclob'") == 1


def test_int_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1 in [2, 3]") == 0


def test_int_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3 in [1, 2, 3]") == 1


def test_int_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1 in [2.2, 3.3]") == 0


def test_int_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3 in [1.1, 2.2, 3.0]") == 1


def test_int_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("1 in {2, 3}") == 0


def test_int_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("3 in {1, 2, 3}") == 1


def test_int_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("1 in {2.2, 3.3}") == 0


def test_int_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("3 in {1.1, 2.2, 3.0}") == 1


def test_number_intlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 in [2, 3]") == 0


def test_number_intlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 in [1, 2, 3]") == 1


def test_number_numberlist1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 in [2.2, 3.3]") == 0


def test_number_numberlist2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 in [1.1, 2.2, 3.0]") == 1


def test_number_intset1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 in {2, 3}") == 0


def test_number_intset2(vsql_db, vsql_data):
	assert vsql_db.expr("3.0 in {1, 2, 3}") == 1


def test_number_numberset1(vsql_db, vsql_data):
	assert vsql_db.expr("1.0 in {2.2, 3.3}") == 0


def test_number_numberset2(vsql_db, vsql_data):
	assert vsql_db.expr("3.3 in {1.1, 2.2, 3.3}") == 1


def test_date_datelist1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) in [@(2000-02-28), @(2000-03-01)]") == 0


def test_date_datelist2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) in [@(2000-02-29), @(2000-03-01)]") == 1


def test_date_dateset1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) in {@(2000-02-28), @(2000-03-01)}") == 0


def test_date_dateset2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29) in {@(2000-02-29), @(2000-03-01)}") == 1


def test_datetime_datetimelist1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) in [@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)]") == 0


def test_datetime_datetimelist2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) in [@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)]") == 1


def test_datetime_datetimeset1(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) in {@(2000-02-28T12:34:56), @(2000-03-01T12:34:56)}") == 0


def test_datetime_datetimeset2(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56) in {@(2000-02-29T12:34:56), @(2000-03-01T12:34:56)}") == 1


def test_null_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("None in []") == 0


def test_null_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("None in [None, None]") == 1


def test_int_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int in []", where="r.identifier == 'none'") == 0


def test_int_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int in [None]", where="r.identifier == 'none'") == 1


def test_int_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("1 in [None]") == 0


def test_number_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number in []", where="r.identifier == 'none'") == 0


def test_number_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number in [None]", where="r.identifier == 'none'") == 1


def test_number_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("1.1 in [None]") == 0


def test_str_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str in []", where="r.identifier == 'none'") == 0


def test_str_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_str in [None]", where="r.identifier == 'none'") == 1


def test_str_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk' in [None]") == 0


def test_clob_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in []", where="r.identifier == 'none'") == 0


def test_clob_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in [None]", where="r.identifier == 'none'") == 1


def test_clob_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob in [None]", where="r.identifier == 'clob'") == 0


def test_date_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {d1}][0] in []") == 0


def test_date_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {d1}][0] in [None]") == 1


def test_date_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{d1} in [None]") == 0


def test_datetime_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {dt1}][0] in []") == 0


def test_datetime_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr(f"[None, {dt1}][0] in [None]") == 1


def test_datetime_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr(f"{dt1} in [None]") == 0

def test_bool_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool in []", where="r.identifier == 'none'") == 0


def test_bool_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool in [None]", where="r.identifier == 'none'") == 1


def test_bool_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("True in [None]") == 0


def test_color_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color in []", where="r.identifier == 'none'") == 0


def test_color_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_color in [None]", where="r.identifier == 'none'") == 1


def test_color_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("#369 in [None]") == 0


def test_geo_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49, 11, 'Here') in []") == 0


def test_geo_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49, 11, 'Here') in [None]") == 0


def test_datedelta_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta in []", where="r.identifier == 'none'") == 0


def test_datedelta_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta in [None]", where="r.identifier == 'none'") == 1


def test_datedelta_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("days(1) in [None]") == 0


def test_datetimedelta_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta in []", where="r.identifier == 'none'") == 0


def test_datetimedelta_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta in [None]", where="r.identifier == 'none'") == 1


def test_datetimedelta_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(1, 1) in [None]") == 0


def test_monthdelta_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta in []", where="r.identifier == 'none'") == 0


def test_monthdelta_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta in [None]", where="r.identifier == 'none'") == 1


def test_monthdelta_nulllist3(vsql_db, vsql_data):
	assert vsql_db.expr("months(3) in [None]") == 0


def test_nulllist_nulllist1(vsql_db, vsql_data):
	assert vsql_db.expr("[] in []") == 0


def test_nulllist_nulllist2(vsql_db, vsql_data):
	assert vsql_db.expr("[None] in [None]") == 0


def test_intlist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("[1, 2] in [None]") == 0


def test_numberlist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("[1.1, 2.2] in [None]") == 0


def test_strlist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("['gurk', 'hurz'] in [None]") == 0


def test_cloblist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("[r.v_clob] in [None]", where="r.identifier == 'shortclob'") == 0


def test_datelist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29)] in [None]") == 0


def test_datetimelist_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("[@(2000-02-29T12:34:56)] in [None]") == 0


def test_intset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{1, 2} in [None]") == 0


def test_numberset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{1.1, 2.2} in [None]") == 0


def test_strset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{'gurk', 'hurz'} in [None]") == 0


def test_dateset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29)} in [None]") == 0


def test_datetimeset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{@(2000-02-29T12:34:56)} in [None]") == 0


def test_nullset_nulllist(vsql_db, vsql_data):
	assert vsql_db.expr("{None} in [None]") == 0
