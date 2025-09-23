"""
Tests for vSQL methods.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###


def test_str_lower(db, vsql_data):
	assert expr(db, "'MISSISSIPPI'.lower()") == "mississippi"


def test_str_upper(db, vsql_data):
	assert expr(db, "'mississippi'.upper()") == "MISSISSIPPI"


def test_str_startswith(db, vsql_data):
	assert expr(db, "'mississippi'.startswith('missi')") == True


def test_str_endswith(db, vsql_data):
	assert expr(db, "'mississippi'.endswith('sippi')") == True


def test_str_strip1(db, vsql_data):
	assert expr(db, "'\\r\\t\\n foo \\r\\t\\n '.strip()") == "foo"


def test_str_strip2(db, vsql_data):
	assert expr(db, "'xyzzygurkxyzzy'.strip('xyz')") == "gurk"


def test_str_lstrip1(db, vsql_data):
	assert expr(db, "'\\r\\t\\n foo \\r\\t\\n '.lstrip()") == "foo \r\t\n "


def test_str_lstrip2(db, vsql_data):
	assert expr(db, "'xyzzygurkxyzzy'.lstrip('xyz')") == "gurkxyzzy"


def test_str_rstrip1(db, vsql_data):
	assert expr(db, "'\\r\\t\\n foo \\r\\t\\n '.rstrip()") == "\r\t\n foo"


def test_str_rstrip2(db, vsql_data):
	assert expr(db, "'xyzzygurkxyzzy'.rstrip('xyz')") == "xyzzygurk"


def test_str_find1(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('ks')") == -1


def test_str_find2(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk')") == 2


def test_str_find3(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', 2)") == 2


def test_str_find4(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', -3)") == 6


def test_str_find5(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', 2, 4)") == 2


def test_str_find6(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', 4, 8)") == 6


def test_str_find7(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('ur', -4, -1)") == 5


def test_str_find8(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', 2, 3)") == -1


def test_str_find9(db, vsql_data):
	assert expr(db, "'gurkgurk'.find('rk', 7)") == -1


def test_str_replace(db, vsql_data):
	assert expr(db, "'gurk'.replace('u', 'oo')") == "goork"


def test_str_split1(db, vsql_data):
	assert expr(db, "' \\t\\r\\nf \\t\\r\\no \\t\\r\\no \\t\\r\\n'.split()") == ['f', 'o', 'o']


def test_str_split2(db, vsql_data):
	assert expr(db, "' \\t\\r\\nf \\t\\r\\no \\t\\r\\no \\t\\r\\n'.split(None, 1)") == ['f', 'o \t\r\no']


def test_str_split3(db, vsql_data):
	assert expr(db, "'xxfxxoxxoxx'.split('xx')") == [None, 'f', 'o', 'o', None]


def test_str_split4(db, vsql_data):
	assert expr(db, "'xxfxxoxxoxx'.split('xx', 2)") == [None, 'f', 'oxxoxx']


def test_str_join_str(db, vsql_data):
	assert expr(db, "','.join('1234')") == "1,2,3,4"


def test_str_join_list(db, vsql_data):
	assert expr(db, "','.join(['1', '2', '3', '4'])") == "1,2,3,4"


def test_color_lum1(db, vsql_data):
	assert expr(db, "#000.lum()") == 0.0


def test_color_lum2(db, vsql_data):
	assert expr(db, "#fff.lum()") == 1.0


def test_date_week(db, vsql_data):
	assert expr(db, "@(2000-02-29).week()") == 9


def test_datetime_week(db, vsql_data):
	assert expr(db, "@(2000-02-29T12:34:56).week()") == 9
