#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2026 by LivingLogic AG, Bayreuth/Germany
## Copyright 2026 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import datetime, pathlib, threading

import pytest

from ll import taskswarm


class SchemaSwarm(taskswarm.Swarm):
	def format_schema(self, name):
		return name.upper()


@pytest.fixture
def swarm():
	swarm = taskswarm.Swarm("test", 1, True)
	swarm.plain_output = True
	return swarm


@pytest.fixture
def color_swarm():
	swarm = taskswarm.Swarm("test", 1, True)
	swarm.plain_output = False
	return swarm


def test_format_str(swarm):
	assert swarm.format("foo") == "foo"
	assert swarm.format(t"foo") == "foo"
	assert swarm.format(42) == "42"


def test_format_types_plain(swarm):
	n = 5000
	assert swarm.format(t"{n}") == "5,000"
	assert swarm.format(t"{n:d}") == "5000"
	f = 1234.5678
	assert swarm.format(t"{f}") == "1,234.6"
	assert swarm.format(t"{f:.2f}") == "1234.57"
	td = datetime.timedelta(seconds=75)
	assert swarm.format(t"{td}") == "0:01:15"
	dt = datetime.datetime(2026, 9, 14, 12, 0, 0)
	assert swarm.format(t"{dt}") == "2026-09-14 12:00:00"
	assert swarm.format(t"{dt:%Y}") == "2026"
	s = "foo"
	assert swarm.format(t"{s}") == "foo"
	assert swarm.format(t"{s:>5}") == "  foo"


def test_format_path(swarm):
	swarm.currentdir = pathlib.Path("/foo/bar")
	assert swarm.format(t"{pathlib.Path('/foo/bar/baz.txt')}") == "baz.txt"
	assert swarm.format(t"{pathlib.Path('/other/baz.txt')}") == "/other/baz.txt"


def test_format_color(color_swarm):
	n = 5000
	assert color_swarm.format(t"{n}") == "\033[1;35m5,000\033[0m"
	assert color_swarm.format(t"{'::':sep}") == "\033[30;1m::\033[0m"
	td = datetime.timedelta(seconds=75)
	assert color_swarm.format(t"{td}") == "\033[35m00:0\033[1;35m1:15\033[0m"


def test_format_conversion(swarm):
	s = "x"
	assert swarm.format(t"{s!r}") == "'x'"
	assert swarm.format(t"{s!s}") == "x"
	assert swarm.format(t"{'ä'!a}") == "'\\xe4'"


def test_format_spec_dispatch(swarm):
	assert swarm.format(t"{'::':sep}") == swarm.format_sep("::")
	with pytest.raises(ValueError):
		swarm.format(t"{'ll':schema}")

	schema_swarm = SchemaSwarm("test", 1, True)
	schema_swarm.plain_output = True
	assert schema_swarm.format(t"Exporting {'ll':schema}") == "Exporting LL"


def test_task_names(swarm):
	schema_swarm = SchemaSwarm("test", 1, True)
	schema_swarm.plain_output = True
	parent = taskswarm.Task(0, schema_swarm.queue, "parent")
	child = taskswarm.Task(1, schema_swarm.queue, t"{'ll':schema} export")
	child.parent = parent
	assert child.plain_name == "ll export"
	assert str(child) == "parent :: ll export"
	assert schema_swarm.format(t"{child:task}") == "parent :: LL export"
	assert schema_swarm.format_task(child) == "parent :: LL export"


def test_task_put_unpicklable(swarm):
	task = taskswarm.Task(0, swarm.queue, "task")
	with pytest.raises(TypeError):
		task.log(t"{threading.Lock()}")
