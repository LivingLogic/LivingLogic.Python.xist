#! /usr/bin/env python

"""
A XSC module that contains elements that are simplify generating
SQL statements.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types

class SQLCommand:
	"""
	encapsulates an SQL command and provides a bunch of services for derived classes
	"""

	def formatValue(self, value):
		t = type(value)
		if t is types.NoneType:
			return "NULL"
		elif t in (types.StringType, types.UnicodeType):
			return ("'" + value.replace("'", "''") + "'").encode("latin1")
		elif t in (types.IntType, types.LongType, types.FloatType):
			return str(value)
		else:
			raise ValueError, "unrecognised type for database field"

	def formatField(self, name, value, format=0):
		"""
		format == 0: setting
		format == 1: testing
		format == 2: inserting
		"""
		if value is None:
			if format==0:
				return name + "=NULL"
			elif format==1:
				return name + " IS NULL"
			else:
				return "NULL"
		else:
			if format==0 or format==1:
				return name + "=" + self.formatValue(value)
			else:
				return self.formatValue(value)

	def formatFields(self, fields, format=0):
		v = []
		for field in fields.keys():
			v.append(self.formatField(field, fields[field], format))
		if format==0:
			return ",".join(v)
		elif format==1:
			return " AND ".join(v)
		else:
			return ",".join(v)

	def do(self, connection):
		return connection.query(str(self))

class SQLInsert(SQLCommand):
	"""
	an update
	"""
	def __init__(self, table, set):
		self.table = table
		self.set = set

	def __str__(self):
		v = []
		v.append("INSERT INTO ")
		v.append(self.table)
		v.append(" (")
		vv = []
		for field in self.set.keys():
			vv.append(field)
		v.append(",".join(vv))
		v.append(") VALUES (")
		v.append(self.formatFields(self.set, 2))
		v.append(");")
		return "".join(v)

class SQLUpdate(SQLCommand):
	"""
	an update
	"""
	def __init__(self, table, set, where):
		self.table = table
		self.set = set
		self.where = where

	def __str__(self):
		v = []
		v.append("UPDATE " + self.table + " SET ")
		v.append(self.formatFields(self.set, 0))
		if len(self.where.keys()):
			v.append(" WHERE ")
			v.append(self.formatFields(self.where, 1))
		v.append(";")
		return "".join(v)

class SQLDelete(SQLCommand):
	"""
	an delete command
	"""
	def __init__(self, table, where):
		self.table = table
		self.where = where

	def __str__(self):
		v = []
		v.append("DELETE FROM " + self.table)
		if len(self.where.keys()):
			v.append(" WHERE ")
			v.append(self.formatFields(self.where, 1))
		v.append(";")
		return "".join(v)
