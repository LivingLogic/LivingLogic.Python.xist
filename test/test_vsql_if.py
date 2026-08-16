"""
Tests for the vSQL ternary operator ``A if cond else B``.

To run the tests, :mod:`pytest` is required.
"""

import pytest

import conftest


###
### Tests
###

# ``A if cond else B`` supports every type of the ``ANY`` group as the
# condition and for the two branches: both branches of the same type, one
# branch of type ``NULL``, and the ``BOOL``/``INT``/``NUMBER`` cross
# combinations. The following tests systematically cover all of those
# combinations, using the canonical expressions from
# ``conftest.vsql_cmp_exprs``.
#
# Whether the condition is true depends on the test record selected by the
# ``where`` condition: if both a branch expression and the condition
# reference a field, but require different records, the condition is ``null``
# (and therefore false).


def _cond_is_true(c, cond_identifier, where_identifier):
	if c == "null":
		return False
	elif c == "cloblist":
		# The ``cloblist`` expression wraps its field in a list literal, so
		# it is a non-empty list (and therefore true) even on a record where
		# the field itself is null
		return True
	else:
		return cond_identifier in (None, where_identifier)


@pytest.mark.parametrize("c", conftest.vsql_cmp_exprs)
@pytest.mark.parametrize("t", conftest.vsql_cmp_exprs)
def test_all_type_combinations(vsql_db, vsql_data, t, c):
	(vexpr, videntifier) = conftest.vsql_cmp_exprs[t]
	(cexpr, cidentifier) = conftest.vsql_cmp_exprs[c]
	identifier = videntifier or cidentifier
	where = f"r.identifier == '{identifier}'" if identifier else None
	condtrue = _cond_is_true(c, cidentifier, identifier)

	# Both branches have the same type (and the same value)
	if t == "null":
		assert vsql_db.expr(f"({vexpr}) if ({cexpr}) else ({vexpr})", where=where) is None
	else:
		assert vsql_db.expr(f"(({vexpr}) if ({cexpr}) else ({vexpr})) == ({vexpr})", where=where) == 1

	# The ``else`` branch is ``None``
	if condtrue and t != "null":
		assert vsql_db.expr(f"(({vexpr}) if ({cexpr}) else None) == ({vexpr})", where=where) == 1
	else:
		assert vsql_db.expr(f"({vexpr}) if ({cexpr}) else None", where=where) is None

	# The ``if`` branch is ``None``
	if condtrue or t == "null":
		assert vsql_db.expr(f"None if ({cexpr}) else ({vexpr})", where=where) is None
	else:
		assert vsql_db.expr(f"(None if ({cexpr}) else ({vexpr})) == ({vexpr})", where=where) == 1


@pytest.mark.parametrize("c", conftest.vsql_cmp_exprs)
def test_numeric_type_combinations(vsql_db, vsql_data, c):
	(cexpr, cidentifier) = conftest.vsql_cmp_exprs[c]
	where = f"r.identifier == '{cidentifier}'" if cidentifier else None
	condtrue = c != "null"
	for (a, b, va, vb) in (
		("True", "42", 1, 42),
		("42", "True", 42, 1),
		("True", "42.5", 1, 42.5),
		("42.5", "True", 42.5, 1),
		("42", "42.5", 42, 42.5),
		("42.5", "42", 42.5, 42),
	):
		assert vsql_db.expr(f"({a}) if ({cexpr}) else ({b})", where=where) == (va if condtrue else vb)
