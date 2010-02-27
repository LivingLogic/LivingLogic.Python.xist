#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import misc


def err(n):
	for i in xrange(n):
		yield i
	raise SyntaxError


def test_item():
	e = iter(range(10))
	assert misc.item(e, 0) == 0
	assert misc.item(e, 0) == 1
	assert misc.item(e, -1) == 9
	py.test.raises(IndexError, misc.item, e, -1)
	assert misc.item(e, -1, 42) == 42

	e = iter(range(10))
	assert misc.item(e, 4) == 4

	e = iter(range(10))
	py.test.raises(IndexError, misc.item, e, 10)

	e = iter(range(10))
	assert misc.item(e, 10, 42) == 42

	e = iter(range(10))
	assert misc.item(e, -1) == 9

	e = iter(range(10))
	assert misc.item(e, -10) == 0

	e = iter(range(10))
	py.test.raises(IndexError, misc.item, e, -11)

	e = iter(range(10))
	assert misc.item(e, -11, 42) == 42

	iterable = [17, 23, 37]
	
	# Wrong arguments
	py.test.raises(TypeError, misc.item)
	py.test.raises(TypeError, misc.item, [])
	py.test.raises(TypeError, misc.item, 42, 42)

	# Non-negative index
	assert misc.item(iterable, 0), 17
	assert misc.item(iterable, 2), 37
	py.test.raises(IndexError, misc.item, iterable, 3)
	assert misc.item(iterable, 3, 42), 42
	assert misc.item(err(10), 9), 9
	py.test.raises(SyntaxError, misc.item, err(10), 10)

	# Negative index
	assert misc.item(iterable, -1), 37
	assert misc.item(iterable, -3), 17
	py.test.raises(IndexError, misc.item, iterable, -4)
	assert misc.item(iterable, -4, 42), 42
	# iterator is always exhausted
	py.test.raises(SyntaxError, misc.item, err(10), -1)


def test_first():
	e = iter(range(10))
	assert misc.first(e) == 0
	assert misc.first(e) == 1

	e = iter([])
	py.test.raises(IndexError, misc.first, e)

	e = iter([])
	assert misc.first(e, 42) == 42


def test_last():
	e = iter(range(10))
	assert misc.last(e) == 9
	py.test.raises(IndexError, misc.last, e)

	e = iter([])
	py.test.raises(IndexError, misc.last, e)

	e = iter([])
	assert misc.last(e, 42) == 42


def test_count():
	e = iter(range(10))
	assert misc.count(e) == 10
	assert misc.count(e) == 0

	e = iter([])
	assert misc.count(e) == 0


def test_iterator_bool():
	e = misc.Iterator(iter(range(10)))
	assert e

	e = misc.Iterator(iter([]))
	assert not e


def test_iterator_next():
	e = misc.Iterator(iter(range(2)))
	assert e.next() == 0
	assert e.next() == 1
	py.test.raises(StopIteration, e.next)


def test_iterator_getitem():
	e = misc.Iterator(iter(range(10)))
	assert e[0] == 0
	assert e[0] == 1
	assert e[-1] == 9
	py.test.raises(IndexError, e.__getitem__, -1)
