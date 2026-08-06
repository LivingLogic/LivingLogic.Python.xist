'''
Tests for the vSQL binary bitwise "exclusive or" operator ``A ^ B``.

To run the tests, :mod:`pytest` is required.
'''


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool ^ False", where="r.identifier == 'bool_false'") == 0


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool ^ True", where="r.identifier == 'bool_false'") == 1


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool ^ 3", where="r.identifier == 'bool_true'") == 2


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int ^ True", where="r.identifier == 'int'") == 1777


def test_int_int1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_int ^ 313", where="r.identifier == 'int'") == 1993


def test_int_int2(vsql_db, vsql_data):
	assert vsql_db.expr("(-r.v_int) ^ 313", where="r.identifier == 'int'") == -2007