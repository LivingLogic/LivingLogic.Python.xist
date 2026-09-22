"""
Tests for :class:`ll.vsql.Query`

To run the tests, :mod:`pytest` is required.
"""

import math, datetime

import pytest

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


def test_query_replacement_var(vsql_db, vsql_data):
	# ``f`` is a replacement variable that stands for ``p.field`` in this
	# select expression only.
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.select_vsql("f.parent.name", alias="fld", f="p.field")
	q.where_vsql("p.lastname == 'Einstein'")
	rs = vsql_db.execute(q)

	assert rs[0].fld == "Science"


def test_query_replacement_var_shares_join(vsql_db, vsql_data):
	# The replaced expression references the same fields as the direct
	# expression, so the table is joined only once.
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.select_vsql("p.field.name", alias="fld")
	q.where_vsql("f.name == 'Physics'", f="p.field")
	sql = raw_sql(q)

	assert sql.count("vsql_field") == 1
	assert "p.field.name" in sql and "/* f" not in sql


def test_query_replacement_var_overrides_query_var(vsql_db, vsql_data):
	# A replacement variable replaces the query variable with the same name
	# for this expression only.
	q = vsql_db.query(p=vsql_db.p, r=vsql_db.r)
	q.from_vsql("p")
	q.select_vsql("p.firstname", alias="fn")
	q.where_vsql("r.lastname == 'Einstein'", r="p")
	rs = vsql_db.execute(q)

	assert rs[0].fn == "Albert"
	# The table of the query variable ``r`` isn't joined.
	assert "/* r */" not in raw_sql(q)


def test_query_replacement_var_unavailable_elsewhere(vsql_db, vsql_data):
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.where_vsql("f.name == 'Physics'", f="p.field")

	with pytest.raises(vsql.VSQLUnknownNameError):
		q.where_vsql("f.name == 'Physics'")


def test_query_replacement_var_references_replacement_var(vsql_db, vsql_data):
	# Replacement variables may only reference real variables.
	q = vsql_db.query(p=vsql_db.p)

	with pytest.raises(vsql.VSQLReplacementVariableError):
		q.where_vsql("g.name == 'Physics'", f="p.field", g="f")
	with pytest.raises(vsql.VSQLReplacementVariableError):
		q.where_vsql("f.name == 'Physics'", f="f")


def test_source_parenthesized_call(vsql_db, vsql_data):
	# The reconstructed source of a parenthesized call that is used in
	# another call must be the original source.
	sources = [
		"(p.lastname.upper()).lower()",
		"len((p.lastname.upper())) > 1",
		"( p.lastname.upper( ) ).lower( )",
		"(p.lastname.upper() + 'x').lower()",
	]
	for source in sources:
		assert vsql.AST.fromsource(source, p=vsql_db.p).source() == source


def test_query_replacement_var_interpolation(vsql_db, vsql_data):
	# Interpolations in the expression and in the replacement expression
	# become bind parameters.
	q = vsql_db.query(p=vsql_db.p)
	q.from_vsql("p")
	q.select_vsql("p.firstname", alias="fn")
	q.where_vsql(t"p.lastname == {'Einstein'} and p.field.name == x", x=t"{'Physics'}")
	rs = vsql_db.execute(q)

	assert rs[0].fn == "Albert"
