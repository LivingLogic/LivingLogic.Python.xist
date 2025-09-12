"""
Tests for the vSQL subtraction operator ``-``.

To run the tests, :mod:`pytest` is required.
"""

import datetime
import pytest

from conftest import *


###
### Tests
###

def test_bool_bool1(db, vsql_data):
	assert expr(db, "r.v_bool - True", where="r.identifier == 'none'") is None


def test_bool_bool2(db, vsql_data):
	assert expr(db, "r.v_bool - True", where="r.identifier == 'bool_false'") == -1


def test_bool_bool3(db, vsql_data):
	assert expr(db, "r.v_bool - True", where="r.identifier == 'bool_true'") == 0


def test_bool_int(db, vsql_data):
	assert expr(db, "r.v_bool - 1", where="r.identifier == 'bool_true'") == 0


def test_bool_number(db, vsql_data):
	assert expr(db, "r.v_bool - 1.5", where="r.identifier == 'bool_true'") == -0.5


def test_int_bool(db, vsql_data):
	assert expr(db, "1 - r.v_bool", where="r.identifier == 'bool_true'") == 0


def test_int_int(db, vsql_data):
	assert expr(db, "1 - r.v_int", where="r.identifier == 'int'") == -1775


def test_int_number(db, vsql_data):
	assert expr(db, "1 - r.v_number", where="r.identifier == 'number'") == -41.5


def test_number_bool(db, vsql_data):
	assert expr(db, "r.v_number - True", where="r.identifier == 'number'") == 41.5


def test_number_int(db, vsql_data):
	assert expr(db, "r.v_number - 1", where="r.identifier == 'number'") == 41.5


def test_number_number(db, vsql_data):
	assert expr(db, "r.v_number - 1.5", where="r.identifier == 'number'") == 41.0


def test_date_datedelta(db, vsql_data):
	assert expr(db, "r.v_date - days(1)", where="r.identifier == 'date'") == datetime.datetime(2000, 2, 28)


def test_date_date(db, vsql_data):
	assert expr(db, "@(2000-03-01) - r.v_date", where="r.identifier == 'date'") == 1


def test_datetime_datetime(db, vsql_data):
	assert expr(db, "@(2000-03-01T13:35:57) - r.v_datetime", where="r.identifier == 'datetime'") == pytest.approx(1 + (1*3600+1*60+1)/86400)


def test_date_monthdelta(db, vsql_data):
	assert expr(db, "@(2000-03-31) - months(1)") == datetime.datetime(2000, 2, 29)


def test_datetime_monthdelta(db, vsql_data):
	assert expr(db, "@(2000-03-31T12:34:56) - months(1)") == datetime.datetime(2000, 2, 29, 12, 34, 56)


def test_datedelta_datedelta(db, vsql_data):
	assert expr(db, "r.v_datedelta - days(7)", where="r.identifier == 'datedelta'") == 5


def test_monthdelta_monthdelta(db, vsql_data):
	assert expr(db, "r.v_monthdelta - months(12)", where="r.identifier == 'monthdelta'") == -9


def test_datedelta_datetimedelta(db, vsql_data):
	assert expr(db, "r.v_datedelta - hours(12)", where="r.identifier == 'datedelta'") == 11.5


def test_datetimedelta_datedelta(db, vsql_data):
	assert expr(db, "r.v_datetimedelta - days(1)", where="r.identifier == 'datetimedelta'") == pytest.approx(12/24 + 34/1440 + 56/86400)


def test_datetimedelta_datetimedelta(db, vsql_data):
	assert expr(db, f"r.v_datetimedelta - timedelta(1, {(12 * 60 + 34) * 60 + 56})", where="r.identifier == 'datetimedelta'") == pytest.approx(0)
