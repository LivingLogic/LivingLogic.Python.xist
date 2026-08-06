"""
Tests for vSQL literals.

To run the tests, :mod:`pytest` is required.
"""

###
### Tests
###

import datetime

from ll import vsql


def test_literal_none(vsql_db, vsql_data):
	assert vsql_db.expr("None") is None


def test_literal_bool(vsql_db, vsql_data):
	assert vsql_db.expr("False") == 0
	assert vsql_db.expr("True") == 1


def test_literal_int(vsql_db, vsql_data):
	assert vsql_db.expr(str(42)) == 42
	assert vsql_db.expr(bin(42)) == 42
	assert vsql_db.expr(oct(42)) == 42
	assert vsql_db.expr(hex(42)) == 42
	assert vsql_db.expr(str(-42)) == -42
	assert vsql_db.expr(bin(-42)) == -42
	assert vsql_db.expr(oct(-42)) == -42
	assert vsql_db.expr(hex(-42)) == -42


def test_literal_float(vsql_db, vsql_data):
	assert vsql_db.expr("42.5") == 42.5
	assert vsql_db.expr("-42.5") == -42.5
	assert vsql_db.expr("1e2") == 100.0
	assert vsql_db.expr("-1e2") == -100.0


def test_literal_string(vsql_db, vsql_data):
	assert vsql_db.expr("'foo'") == "foo"
	assert vsql_db.expr("'\x01\xff\u3042'") == "\x01\xff\u3042"
	assert vsql_db.expr("'\\a\\b\\t\\n\\f\\r\\\"\\'\\\\'") == "\a\b\t\n\f\r\"'\\"
	if vsql_db.supports_nul:
		assert vsql_db.expr("'\\x00\\xff\\u3042'") == "\x00\xff\u3042"
	else:
		assert vsql_db.expr("'\\xff\\u3042'") == "\xff\u3042"
	assert vsql_db.expr("'\\U0001f389'") == "🎉"
	# FIXME: This doesn't work yet, because UL4 inherits the 16-bit limitation of ANTLR 3
	# assert vsql_db.expr("'🎉'") == "🎉"


def test_literal_date(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-02-29)") == vsql_db.type_for_date(2000, 2, 29)
	assert vsql_db.expr("@(2000-02-29T12:34:56)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_literal_color(vsql_db, vsql_data):
	assert vsql_db.expr("#369") == 0x336699ff
	assert vsql_db.expr("#123456") == 0x123456ff
	assert vsql_db.expr("#369c") == 0x336699cc
	assert vsql_db.expr("#12345678") == 0x12345678


def test_x(vsql_db, vsql_data):
	q = vsql_db.query(r=vsql_db.r)
	q.select_vsql("r.identifier")
	q.where_vsql("r.identifier == 'none'")

	rs = vsql_db.execute(q)

	assert len(rs) == 1
	assert rs[0][0] == "none"
