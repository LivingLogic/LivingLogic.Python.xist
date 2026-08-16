"""
Tests for the vSQL modulo operator ``%``.

To run the tests, :mod:`pytest` is required.
"""

import pytest


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool % True", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool % True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool % True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool % 1", where="r.identifier == 'bool_true'") == 0


def test_bool_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool % 0.3", where="r.identifier == 'bool_true'") == pytest.approx(0.1)


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("2 % r.v_bool", where="r.identifier == 'bool_true'") == 0


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int % 2", where="r.identifier == 'int'") == 0


def test_int_number(vsql_db, vsql_data):
	assert vsql_db.expr("86 % r.v_number", where="r.identifier == 'number'") == 1


def test_number_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number % True", where="r.identifier == 'number'") == 0.5


def test_number_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number % 4", where="r.identifier == 'number'") == 2.5


def test_number_number1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number % 3.5", where="r.identifier == 'number'") == 0.5


def test_number_number2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number % -3.5", where="r.identifier == 'number'") == -3.0


def test_number_number3(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_number % 3.5", where="r.identifier == 'number'") == 3.0


def test_number_number4(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_number % -3.5", where="r.identifier == 'number'") == -0.5


def test_color_color1(vsql_db, vsql_data):
	# With two constant colors UL4 folds the expression at compile time,
	# so this tests the constant folding path, not the database rule
	assert vsql_db.expr("#369 % #fff") == 0x336699ff


def test_color_color2(vsql_db, vsql_data):
	# Constant-folded by UL4 (see ``test_color_color1``)
	assert vsql_db.expr("#369c % #fff6") == 0x4674a2e0


def test_color_color3(vsql_db, vsql_data):
	# Use a field as one operand to prevent UL4 from constant folding the
	# expression, so that the database really executes the operator
	assert vsql_db.expr("#369c % r.v_color", where="r.identifier == 'none'") is None


def test_color_color4(vsql_db, vsql_data):
	# Use a field as one operand to prevent UL4 from constant folding the
	# expression, so that the database really executes the operator
	assert vsql_db.expr("#369c % r.v_color", where="r.identifier == 'color'") == 0x2c5c8cff
