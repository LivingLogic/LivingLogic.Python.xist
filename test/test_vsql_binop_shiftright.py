"""
Tests for the vSQL right shift operator ``>>``.

The test are done via the Python DB interface.

To run the tests, :mod:`pytest` is required.
"""

from conftest import *


###
### Tests
###

def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool >> False", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool >> True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool >> False", where="r.identifier == 'bool_true'") == 1


def test_bool_bool4(db, vsql_data):
	assert expr(db, "r.v_bool >> True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool >> 1", where="r.identifier == 'bool_true'") == 0


def test_int_bool(db, vsql_data):
	assert expr(db, "128 >> r.v_bool", where="r.identifier == 'bool_true'") == 64


def test_int_int(db, vsql_data):
	assert expr(db, "r.v_int >> 2", where="r.identifier == 'int'") == 444