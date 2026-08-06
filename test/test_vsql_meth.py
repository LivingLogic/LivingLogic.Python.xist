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
