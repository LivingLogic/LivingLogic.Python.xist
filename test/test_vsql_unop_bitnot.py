"""
Tests for the vSQL unary bitwise not operator ``~``.

To run the tests, :mod:`pytest` is required.
"""


###
### Tests
###

def test_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("~r.v_bool", where="r.identifier == 'none'") is None


def test_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("~r.v_bool", where="r.identifier == 'bool_false'") == -1


def test_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("~r.v_bool", where="r.identifier == 'bool_true'") == -2


def test_int1(vsql_db, vsql_data):
	assert vsql_db.expr("~r.v_int", where="r.identifier == 'none'") is None


def test_int2(vsql_db, vsql_data):
	assert vsql_db.expr("~r.v_int", where="r.identifier == 'int'") == -1777