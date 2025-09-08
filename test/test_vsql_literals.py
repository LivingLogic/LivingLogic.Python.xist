"""
Tests for vSQL literals.

To run the tests, :mod:`pytest` is required.
"""

###
### Tests
###

import datetime

from ll import vsql

from conftest import execute, expr, vsql_r


def test_literal_none(db, vsql_data):
	assert expr(db, "None") is None


def test_literal_bool(db, vsql_data):
	assert expr(db, "False") == 0
	assert expr(db, "True") == 1


def test_literal_int(db, vsql_data):
	assert expr(db, str(42)) == 42
	assert expr(db, bin(42)) == 42
	assert expr(db, oct(42)) == 42
	assert expr(db, hex(42)) == 42
	assert expr(db, str(-42)) == -42
	assert expr(db, bin(-42)) == -42
	assert expr(db, oct(-42)) == -42
	assert expr(db, hex(-42)) == -42


def test_literal_float(db, vsql_data):
	assert expr(db, "42.5") == 42.5
	assert expr(db, "-42.5") == -42.5
	assert expr(db, "1e2") == 100.0
	assert expr(db, "-1e2") == -100.0


def test_literal_string(db, vsql_data):
	assert expr(db, "'foo'") == "foo"
	assert expr(db, "'\x01\xff\u3042'") == "\x01\xff\u3042"
	assert expr(db, "'\\a\\b\\t\\n\\f\\r\\\"\\'\\\\'") == "\a\b\t\n\f\r\"'\\"
	assert expr(db, "'\\x00\\xff\\u3042'") == "\x00\xff\u3042"
	assert expr(db, "'\\U0001f389'") == "🎉"
	# FIXME: This doesn't work yet, because UL4 inherits the 16-bit limitation of ANTLR 3
	# assert expr(db, "'🎉'") == "🎉"


def test_literal_date(db, vsql_data):
	assert expr(db, "@(2000-02-29)") == datetime.datetime(2000, 2, 29)
	assert expr(db, "@(2000-02-29T12:34:56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_literal_color(db, vsql_data):
	assert expr(db, "#369") == 0x336699ff
	assert expr(db, "#123456") == 0x123456ff
	assert expr(db, "#369c") == 0x336699cc
	assert expr(db, "#12345678") == 0x12345678


def test_x(db, vsql_data):
	q = vsql.Query(r=vsql_r)
	q.select_vsql("r.identifier")
	q.where_vsql("r.identifier == 'none'")

	rs = execute(db, q)

	assert len(rs) == 1
	assert rs[0][0] == "none"
