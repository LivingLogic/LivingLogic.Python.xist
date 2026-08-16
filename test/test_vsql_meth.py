"""
Tests for vSQL methods.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###


def test_str_lower(vsql_db, vsql_data):
	assert vsql_db.expr("'MISSISSIPPI'.lower()") == "mississippi"


def test_str_upper(vsql_db, vsql_data):
	assert vsql_db.expr("'mississippi'.upper()") == "MISSISSIPPI"


def test_str_startswith(vsql_db, vsql_data):
	assert vsql_db.expr("'mississippi'.startswith('missi')") == True


def test_str_endswith(vsql_db, vsql_data):
	assert vsql_db.expr("'mississippi'.endswith('sippi')") == True


def test_str_strip1(vsql_db, vsql_data):
	assert vsql_db.expr("'\\r\\t\\n foo \\r\\t\\n '.strip()") == "foo"


def test_str_strip2(vsql_db, vsql_data):
	assert vsql_db.expr("'xyzzygurkxyzzy'.strip('xyz')") == "gurk"


def test_str_lstrip1(vsql_db, vsql_data):
	assert vsql_db.expr("'\\r\\t\\n foo \\r\\t\\n '.lstrip()") == "foo \r\t\n "


def test_str_lstrip2(vsql_db, vsql_data):
	assert vsql_db.expr("'xyzzygurkxyzzy'.lstrip('xyz')") == "gurkxyzzy"


def test_str_rstrip1(vsql_db, vsql_data):
	assert vsql_db.expr("'\\r\\t\\n foo \\r\\t\\n '.rstrip()") == "\r\t\n foo"


def test_str_rstrip2(vsql_db, vsql_data):
	assert vsql_db.expr("'xyzzygurkxyzzy'.rstrip('xyz')") == "xyzzygurk"


def test_str_find1(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('ks')") == -1


def test_str_find2(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk')") == 2


def test_str_find3(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 2)") == 2


def test_str_find4(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', -3)") == 6


def test_str_find5(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 2, 4)") == 2


def test_str_find6(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 4, 8)") == 6


def test_str_find7(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('ur', -4, -1)") == 5


def test_str_find8(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 2, 3)") == -1


def test_str_find9(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 7)") == -1


def test_str_replace(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk'.replace('u', 'oo')") == "goork"


def test_str_split1(vsql_db, vsql_data):
	assert vsql_db.expr("' \\t\\r\\nf \\t\\r\\no \\t\\r\\no \\t\\r\\n'.split()") == ['f', 'o', 'o']


def test_str_split2(vsql_db, vsql_data):
	assert vsql_db.expr("' \\t\\r\\nf \\t\\r\\no \\t\\r\\no \\t\\r\\n'.split(None, 1)") == ['f', 'o \t\r\no']


def test_str_split3(vsql_db, vsql_data):
	assert vsql_db.expr("'xxfxxoxxoxx'.split('xx')") == [None, 'f', 'o', 'o', None]


def test_str_split4(vsql_db, vsql_data):
	assert vsql_db.expr("'xxfxxoxxoxx'.split('xx', 2)") == [None, 'f', 'oxxoxx']


def test_str_join_str(vsql_db, vsql_data):
	assert vsql_db.expr("','.join('1234')") == "1,2,3,4"


def test_str_join_list(vsql_db, vsql_data):
	assert vsql_db.expr("','.join(['1', '2', '3', '4'])") == "1,2,3,4"


def test_color_lum1(vsql_db, vsql_data):
	assert vsql_db.expr("#000.lum()") == 0.0


def test_color_lum2(vsql_db, vsql_data):
	assert vsql_db.expr("#fff.lum()") == 1.0


def test_date_week(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29).week()") == 9


def test_datetime_week(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29T12:34:56).week()") == 9


def test_clob_lower(vsql_db, vsql_data):
	assert vsql_db.expr("('X' + r.v_clob).lower()", where="r.identifier == 'shortclob'") == 'xgurk'


def test_clob_upper(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.upper()", where="r.identifier == 'shortclob'") == 'GURK'


def test_clob_replace(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.replace('u', 'X')", where="r.identifier == 'shortclob'") == 'gXrk'


def test_str_startswith_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("'mississippi'.startswith(['xx', 'mis'])") == True


def test_clob_startswith_str(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.startswith('gu')", where="r.identifier == 'shortclob'") == True


def test_clob_startswith_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.startswith(['xx', 'gu'])", where="r.identifier == 'shortclob'") == True


def test_str_endswith_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("'mississippi'.endswith(['xx', 'ppi'])") == True


def test_clob_endswith_str(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.endswith('rk')", where="r.identifier == 'shortclob'") == True


def test_clob_endswith_strlist(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_clob.endswith(['xx', 'rk'])", where="r.identifier == 'shortclob'") == True


def test_clob_strip1(vsql_db, vsql_data):
	assert vsql_db.expr("(' ' + r.v_clob + ' ').strip()", where="r.identifier == 'shortclob'") == 'gurk'


def test_clob_strip2(vsql_db, vsql_data):
	assert vsql_db.expr("('xy' + r.v_clob + 'yx').strip('xy')", where="r.identifier == 'shortclob'") == 'gurk'


def test_clob_lstrip1(vsql_db, vsql_data):
	assert vsql_db.expr("(' ' + r.v_clob + ' ').lstrip()", where="r.identifier == 'shortclob'") == 'gurk '


def test_clob_lstrip2(vsql_db, vsql_data):
	assert vsql_db.expr("('xy' + r.v_clob + 'yx').lstrip('xy')", where="r.identifier == 'shortclob'") == 'gurkyx'


def test_clob_rstrip1(vsql_db, vsql_data):
	assert vsql_db.expr("(' ' + r.v_clob + ' ').rstrip()", where="r.identifier == 'shortclob'") == ' gurk'


def test_clob_rstrip2(vsql_db, vsql_data):
	assert vsql_db.expr("('xy' + r.v_clob + 'yx').rstrip('xy')", where="r.identifier == 'shortclob'") == 'xygurk'


def test_str_find_clob(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:])", where="r.identifier == 'shortclob'") == 2


def test_clob_find_str(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk')", where="r.identifier == 'shortclob'") == 2


def test_clob_find_clob(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:])", where="r.identifier == 'shortclob'") == 2


def test_str_find_str_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', None)") == 2


def test_str_find_clob_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], None)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_str_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', None)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_clob_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], None)", where="r.identifier == 'shortclob'") == 2


def test_str_find_str_null_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', None, None)") == 2


def test_str_find_clob_null_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], None, None)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_str_null_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', None, None)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_clob_null_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], None, None)", where="r.identifier == 'shortclob'") == 2


def test_str_find_clob_int(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], 3)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_str_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', 3)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_clob_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], 3)", where="r.identifier == 'shortclob'") == 6


def test_str_find_str_null_int(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', None, 4)") == 2


def test_str_find_str_int_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find('rk', 3, None)") == 6


def test_str_find_clob_null_int(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], None, 4)", where="r.identifier == 'shortclob'") == 2


def test_str_find_clob_int_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], 3, None)", where="r.identifier == 'shortclob'") == 6


def test_str_find_clob_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("'gurkgurk'.find(r.v_clob[2:], 3, 8)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_str_null_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', None, 4)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_str_int_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', 3, None)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_str_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find('rk', 3, 8)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_clob_null_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], None, 4)", where="r.identifier == 'shortclob'") == 2


def test_clob_find_clob_int_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], 3, None)", where="r.identifier == 'shortclob'") == 6


def test_clob_find_clob_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + r.v_clob).find(r.v_clob[2:], 3, 8)", where="r.identifier == 'shortclob'") == 6


def test_clob_split(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ' ' + r.v_clob).split()", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_str_split_null(vsql_db, vsql_data):
	assert vsql_db.expr("'gurk hurz'.split(None)") == ['gurk', 'hurz']


def test_clob_split_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ' ' + r.v_clob).split(None)", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_clob_split_str(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ',' + r.v_clob).split(',')", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_str_split_str_null(vsql_db, vsql_data):
	assert vsql_db.expr("'g,h,i'.split(',', None)") == ['g', 'h', 'i']


def test_clob_split_str_null(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ',' + r.v_clob).split(',', None)", where="r.identifier == 'shortclob'") == ['gurk', 'gurk']


def test_str_split_null_bool(vsql_db, vsql_data):
	assert vsql_db.expr("'g h i'.split(None, True)") == ['g', 'h i']


def test_clob_split_null_bool(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ' g h').split(None, True)", where="r.identifier == 'shortclob'") == ['gurk', 'g h']


def test_clob_split_null_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ' g h').split(None, 1)", where="r.identifier == 'shortclob'") == ['gurk', 'g h']


def test_str_split_str_bool(vsql_db, vsql_data):
	assert vsql_db.expr("'g,h,i'.split(',', True)") == ['g', 'h,i']


def test_clob_split_str_bool(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ',g,h').split(',', True)", where="r.identifier == 'shortclob'") == ['gurk', 'g,h']


def test_clob_split_str_int(vsql_db, vsql_data):
	assert vsql_db.expr("(r.v_clob + ',g,h').split(',', 1)", where="r.identifier == 'shortclob'") == ['gurk', 'g,h']


def test_str_join_clob(vsql_db, vsql_data):
	assert vsql_db.expr("','.join(r.v_clob)", where="r.identifier == 'shortclob'") == 'g,u,r,k'


def test_str_join_cloblist(vsql_db, vsql_data):
	assert vsql_db.expr("','.join([r.v_clob, r.v_clob])", where="r.identifier == 'shortclob'") == 'gurk,gurk'
