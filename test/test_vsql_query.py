"""
Tests for :class:`ll.vsql.Query`

To run the tests, :mod:`pytest` is required.
"""

import math, datetime

from ll import vsql


def raw_sql(query):
	return "".join(p for p in query.sqlsource() if isinstance(p, str))


###
### Tests
###

def test_query_comment(vsql_db, vsql_data):
	q = vsql_db.query("foo")
	assert "/* foo */" in raw_sql(q)


def test_query_badcomment(vsql_db, vsql_data):
	q = vsql_db.query("/* foo */")
	assert raw_sql(q).count("*/") == 1


def test_query_simple(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.select_vsql("p.firstname", alias="fn")
	q.where_vsql("p.lastname == 'Einstein'")
	rs = vsql_db.execute(q)

	assert rs[0].fn == "Albert"


def test_query_foreignkey(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.select_vsql("p.field.parent.name", alias="fld")
	q.where_vsql("p.lastname == 'Einstein'")
	rs = vsql_db.execute(q)

	assert rs[0].fld == "Science"


def test_query_count_all(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.aggregate_vsql("count()", "Number of persons", "c")
	rs = vsql_db.execute(q)

	assert rs[0].c == 10


def test_query_count_by_gender(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.gender)")
	q.aggregate_vsql("count()")
	rs = vsql_db.execute(q)

	assert {r[0]: r[1] for r in rs} == {"f": 3, "m": 7}


def test_query_oldest_by_gender(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.gender)")
	q.aggregate_vsql("max( int( ( (p.date_of_death or @(2000-02-29)) - p.date_of_birth ).days / 365.2425 ) )")
	rs = vsql_db.execute(q)

	assert {r[0]: int(r[1]) for r in rs} == {
		"f": 66, # Marie Curie
		"m": 93, # Ronald Reagan
	}


def test_query_count_by_field(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.field.id)")
	q.aggregate_vsql("count()")
	rs = vsql_db.execute(q)

	assert {r[0]: int(r[1]) for r in rs} == {
		"computerscience": 1, # Donald Kunth
		"film": 1, # Marilyn Monroe
		"mathematics": 2, # Bern Reieman, Carl Friedrich Gauß
		"music": 1, # Elvis Presley
		"physics": 2, # Albert Einstain, Marie Curie
		"politics": 2, # Ronald Reagan, Angela Merkel
		"sport": 1, # Muhammad Ali
	}


def test_query_first_last_by_century(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.date_of_birth.year//100)")
	q.aggregate_vsql("min(str(p.date_of_birth))")
	q.aggregate_vsql("max(str(p.date_of_birth))")
	q.aggregate_vsql("count()")
	rs = vsql_db.execute(q)

	assert {r[0]: (r[1], r[2], r[3]) for r in rs} == {
		17: (
			'1777-04-30',
			'1777-04-30',
			1,
		),
		18: (
			'1826-06-17',
			'1879-03-14',
			3,
		),
		19: (
			'1911-02-06',
			'1954-06-17',
			6,
		),
	}


def test_query_sql(vsql_db, vsql_data):
	q = vsql_db.query()
	q.select_sql("upper(per_firstname)")
	q.select_sql(t"replace(per_lastname, {'e'}, {'x'})")
	q.from_sql(vsql_db.person_table.tablesql)
	q.where_sql("per_firstname like 'A%'")
	q.orderby_sql("per_firstname asc nulls last")
	rs = [list(r) for r in vsql_db.execute(q)]

	assert rs == [["ALBERT", "Einstxin"], ["ANGELA", "Mxrkxl"]]
