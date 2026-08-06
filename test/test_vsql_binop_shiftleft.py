"""
Tests for the vSQL left shift operator ``<<``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int << False", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool << True", where="r.identifier == 'bool_false'") == 0


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool << True", where="r.identifier == 'bool_true'") == 2


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool << 1", where="r.identifier == 'bool_true'") == 2


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("2 << r.v_bool", where="r.identifier == 'bool_true'") == 4


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("-r.v_int << 2", where="r.identifier == 'int'") == -7104