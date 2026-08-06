"""
Tests for the vSQL right shift operator ``>>``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool >> False", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool >> True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool >> False", where="r.identifier == 'bool_true'") == 1


def test_bool_bool4(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool >> True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool >> 1", where="r.identifier == 'bool_true'") == 0


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("128 >> r.v_bool", where="r.identifier == 'bool_true'") == 64


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int >> 2", where="r.identifier == 'int'") == 444