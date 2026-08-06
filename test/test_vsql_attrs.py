"""
Tests for vSQL attributes.

To run the tests, :mod:`pytest` is required.
"""

import datetime


###
### Tests
###


def test_date_year(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date.year", where="r.identifier == 'date'") == 2000


def test_datetime_year(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.year", where="r.identifier == 'datetime'") == 2000


def test_date_month(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date.month", where="r.identifier == 'date'") == 2


def test_datetime_month(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.month", where="r.identifier == 'datetime'") == 2


def test_date_day(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date.day", where="r.identifier == 'date'") == 29


def test_datetime_day(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.day", where="r.identifier == 'datetime'") == 29


def test_datetime_hour(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.hour", where="r.identifier == 'datetime'") == 12


def test_datetime_minute(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.minute", where="r.identifier == 'datetime'") == 34


def test_datetime_second(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.second", where="r.identifier == 'datetime'") == 56


def test_date_weekday(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date.weekday", where="r.identifier == 'date'") == 1


def test_datetime_weekday(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.weekday", where="r.identifier == 'datetime'") == 1


def test_date_yearday(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_date.yearday", where="r.identifier == 'date'") == 60


def test_datetime_yearday(vsql_db, vsql_data):
	assert vsql_db.expr("r.v_datetime.yearday", where="r.identifier == 'datetime'") == 60


def test_datedelta_days(vsql_db, vsql_data):
	assert vsql_db.expr("days(12).days") == 12


def test_datetimedelta_days(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).days") == 12


def test_datetimedelta_seconds(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).seconds") == 34


def test_datetimedelta_total_days(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).total_days * 60 * 60 * 24") == 12 * 60 * 60 * 24 + 34


def test_datetimedelta_total_hours(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).total_hours * 60 * 60") == 12 * 60 * 60 * 24 + 34


def test_datetimedelta_total_minutes(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).total_minutes * 60") == 12 * 60 * 60 * 24 + 34


def test_datetimedelta_total_seconds(vsql_db, vsql_data):
	assert vsql_db.expr("timedelta(12, 34).total_seconds") == 12 * 60 * 60 * 24 + 34


def test_color_r(vsql_db, vsql_data):
	assert vsql_db.expr("#369c.r") == 0x33


def test_color_g(vsql_db, vsql_data):
	assert vsql_db.expr("#369c.g") == 0x66


def test_color_b(vsql_db, vsql_data):
	assert vsql_db.expr("#369c.b") == 0x99


def test_color_a(vsql_db, vsql_data):
	assert vsql_db.expr("#369c.a") == 0xcc


def test_geo_lat(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49.95, 11.59, 'Here').lat") == 49.95


def test_geo_long(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49.95, 11.59, 'Here').long") == 11.59


def test_geo_info_with_info(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49.95, 11.59, 'Here').info") == "Here"


def test_geo_info_without_info(vsql_db, vsql_data):
	assert vsql_db.expr("geo(49.95, 11.59).info") is None
