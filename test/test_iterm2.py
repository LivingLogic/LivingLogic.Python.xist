#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2026 by LivingLogic AG, Bayreuth/Germany
## Copyright 2026 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import builtins, base64

import pytest

from ll import iterm2


@pytest.fixture
def not_in_iterm2(monkeypatch):
	monkeypatch.delenv("TERM_PROGRAM", raising=False)
	monkeypatch.delenv("LC_TERMINAL", raising=False)


@pytest.fixture
def no_tty(monkeypatch):
	def open(*args, **kwargs):
		pytest.fail(f"unexpected call to open({args!r}, {kwargs!r})")
	monkeypatch.setattr(builtins, "open", open)


def test_running_in_iterm2(monkeypatch, not_in_iterm2):
	assert not iterm2.running_in_iterm2()

	monkeypatch.setenv("TERM_PROGRAM", "iTerm.app")
	assert iterm2.running_in_iterm2()

	monkeypatch.setenv("TERM_PROGRAM", "Apple_Terminal")
	assert not iterm2.running_in_iterm2()

	monkeypatch.setenv("LC_TERMINAL", "iTerm2")
	assert iterm2.running_in_iterm2()

	monkeypatch.delenv("TERM_PROGRAM")
	assert iterm2.running_in_iterm2()


def test_session_status():
	assert iterm2.session_status() == ""
	assert iterm2.session_status("Working") == "\x1b]21337;status=Working\x07"
	assert iterm2.session_status(indicator="#00ff00") == "\x1b]21337;indicator=#00ff00\x07"
	assert iterm2.session_status(status_color="#00ff00") == "\x1b]21337;status-color=#00ff00\x07"
	assert iterm2.session_status(detail="Step 1") == "\x1b]21337;detail=Step 1\x07"
	assert iterm2.session_status("Working", "#00ff00", "#0000ff", "Step 1") == "\x1b]21337;status=Working;indicator=#00ff00;status-color=#0000ff;detail=Step 1\x07"
	# Empty strings clear the fields, so they must be output
	assert iterm2.session_status("", "", "", "") == "\x1b]21337;status=;indicator=;status-color=;detail=\x07"
	# ``;`` separates fields and ``BEL`` terminates the sequence
	assert iterm2.session_status("a;b\x07c", detail="d;e") == "\x1b]21337;status=a,bc;detail=d,e\x07"


def test_titles():
	assert iterm2.icon_title() == ""
	assert iterm2.window_title() == ""
	assert iterm2.window_and_icon_title() == ""
	assert iterm2.icon_title("foo") == "\x1b]1;foo\x07"
	assert iterm2.window_title("foo") == "\x1b]2;foo\x07"
	assert iterm2.window_and_icon_title("foo") == "\x1b]0;foo\x07"
	# ``;`` is allowed in the title, but ``BEL`` terminates the sequence
	assert iterm2.icon_title("a;b\x07c") == "\x1b]1;a;bc\x07"


def test_badge():
	assert iterm2.badge() == ""
	assert iterm2.badge("") == "\x1b]1337;SetBadgeFormat=\x07"
	format = "XIST \\(session.hostname) ;\x07 äöü"
	s = iterm2.badge(format)
	assert s.startswith("\x1b]1337;SetBadgeFormat=")
	assert s.endswith("\x07")
	encoded = s[len("\x1b]1337;SetBadgeFormat="):-1]
	assert base64.b64decode(encoded).decode("utf-8") == format


def test_notification():
	assert iterm2.notification() == ""
	assert iterm2.notification("Done") == "\x1b]9;Done\x07"
	assert iterm2.notification("a;b\x07c") == "\x1b]9;a;bc\x07"


def test_set_not_in_iterm2(not_in_iterm2, no_tty):
	# When not running in iTerm2 the terminal must not be touched at all
	iterm2.set_session_status("Working", "#00ff00", "#0000ff", "Step 1")
	iterm2.clear_session_status()
	iterm2.set_icon_title("foo")
	iterm2.set_window_title("foo")
	iterm2.set_window_and_icon_title("foo")
	iterm2.set_badge("foo")
	iterm2.set_notification("foo")


def test_set_none_in_iterm2(monkeypatch, no_tty):
	# ``None`` means "do nothing", so the terminal must not be touched either
	monkeypatch.setenv("TERM_PROGRAM", "iTerm.app")
	iterm2.set_session_status()
	iterm2.set_icon_title()
	iterm2.set_window_title()
	iterm2.set_window_and_icon_title()
	iterm2.set_badge()
	iterm2.set_notification()
