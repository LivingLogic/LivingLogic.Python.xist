"""
Tests for the vSQL subtraction operator ``-``.

To run the tests, :mod:`pytest` is required.
"""

import datetime
import pytest


###
### Tests
###

def test_bool_bool1(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool - True", where="r.identifier == 'none'") is None


def test_bool_bool2(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool - True", where="r.identifier == 'bool_false'") == -1


def test_bool_bool3(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool - True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool - 1", where="r.identifier == 'bool_true'") == 0


def test_bool_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_bool - 1.5", where="r.identifier == 'bool_true'") == -0.5


def test_int_bool(vsql_db, vsql_data):
	assert vsql_db.expr("1 - r.v_bool", where="r.identifier == 'bool_true'") == 0


def test_int_int(vsql_db, vsql_data):
	assert vsql_db.expr("1 - r.v_int", where="r.identifier == 'int'") == -1775


def test_int_number(vsql_db, vsql_data):
	assert vsql_db.expr("1 - r.v_number", where="r.identifier == 'number'") == -41.5


def test_number_bool(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number - True", where="r.identifier == 'number'") == 41.5


def test_number_int(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number - 1", where="r.identifier == 'number'") == 41.5


def test_number_number(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_number - 1.5", where="r.identifier == 'number'") == 41.0


def test_date_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date - days(1)", where="r.identifier == 'date'") == datetime.datetime(2000, 2, 28)


def test_date_date(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-03-01) - r.v_date", where="r.identifier == 'date'") == 1


def test_datetime_datetime(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-03-01T13:35:57) - r.v_datetime", where="r.identifier == 'datetime'") == pytest.approx(1 + (1*3600+1*60+1)/86400)


def test_date_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-03-31) - months(1)") == datetime.datetime(2000, 2, 29)


def test_datetime_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("@(2000-03-31T12:34:56) - months(1)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_datedelta_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta - days(7)", where="r.identifier == 'datedelta'") == 5


def test_monthdelta_monthdelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_monthdelta - months(12)", where="r.identifier == 'monthdelta'") == -9


def test_datedelta_datetimedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datedelta - hours(12)", where="r.identifier == 'datedelta'") == 11.5


def test_datetimedelta_datedelta(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetimedelta - days(1)", where="r.identifier == 'datetimedelta'") == pytest.approx(12/24 + 34/1440 + 56/86400)


def test_datetimedelta_datetimedelta(vsql_db, vsql_data):
	assert vsql_db.expr(f"r.v_datetimedelta - timedelta(1, {(12 * 60 + 34) * 60 + 56})", where="r.identifier == 'datetimedelta'") == pytest.approx(0)
