# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2026 by LivingLogic AG, Bayreuth/Germany
## Copyright 2026 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.iterm2` contains functions for working with the terminal emulator
iTerm2__ for macOS.

__ https://iterm2.com/

iTerm2 supports a number of proprietary escape sequences (documented at
https://iterm2.com/documentation-escape-codes.html) in addition to the
standard ANSI and xterm sequences. These can be used e.g. to display inline
images, set the badge or the title of the current tab/window, mark the
prompt/command boundaries for shell integration, add annotations, change
the cursor shape or copy text to the clipboard.

This module provides three things:

*	:func:`running_in_iterm2` detects whether the current program runs inside
	iTerm2 (locally or via ``ssh``), so that these sequences can be used only
	when they are supported;

*	functions that return the iTerm2-specific escape sequences for various
	features as strings, so that they can be printed to the terminal;

*	for each of those a ``set_*`` function that writes the escape sequence
	directly to the controlling terminal (i.e. to ``/dev/tty``), so that it
	takes effect even if ``stdout`` and ``stderr`` are redirected. These
	functions do nothing if the current program isn't running in iTerm2 or if
	there is no controlling terminal (e.g. when running under CI).
"""


import os, base64


def running_in_iterm2():
	"""
	Return whether the current program is running in iTerm2.

	This is the case if the environment variable :envvar:`TERM_PROGRAM` is
	``"iTerm.app"`` (which iTerm2 sets for local shells) or the environment
	variable :envvar:`LC_TERMINAL` is ``"iTerm2"`` (which is forwarded via
	``ssh`` to remote shells, if iTerm2 is configured to do so).
	"""

	return os.environ.get("TERM_PROGRAM") == "iTerm.app" or os.environ.get("LC_TERMINAL") == "iTerm2"


###
### Escape sequences
###
### These functions return the escape sequence for a feature as a string
### (without outputting it).
###

def session_status(status=None, indicator=None, status_color=None, detail=None):
	"""
	Return the escape sequence that sets the `session status`__ of the current
	iTerm2 session.

	The session status is shown by iTerm2 in the tab of the session (as a
	subtitle and a colored dot) and in the "Session Status" tool window, so
	that the state of several long-running sessions can be monitored at a
	glance.

	The arguments are:

	``status`` : string or ``None``
		The status text, e.g. ``"Working"`` or ``"Waiting"``. It is shown as
		the subtitle of the tab.

	``indicator`` : string or ``None``
		The color of the dot shown in the tab. Colors are given in xterm
		notation, i.e. either as ``"#rrggbb"`` or ``"rgb:rr/gg/bb"``.

	``status_color`` : string or ``None``
		The color of the status text (in the same notation as ``indicator``).

	``detail`` : string or ``None``
		Optional additional text that is shown next to the status in the
		"Session Status" tool window, but not in the tab.

	Passing ``None`` for an argument (the default) leaves the corresponding
	part of the session status unchanged, passing an empty string clears it
	(so ``session_status("", "", "", "")`` clears the complete session
	status). If all arguments are ``None`` an empty string is returned, so
	that outputting the result does nothing.

	As ``;`` separates the fields of the escape sequence and ``BEL``
	terminates it, any ``;`` in the arguments is replaced by ``,`` and any
	``BEL`` is removed.

	The returned string has to be written to the terminal to take effect. The
	sequence is only understood by iTerm2, so :func:`running_in_iterm2` should
	be used to check whether it should be output at all.

	__ https://iterm2.com/documentation-session-status.html
	"""

	s = []
	if status is not None:
		s.append(f"status={status}")
	if indicator is not None:
		s.append(f"indicator={indicator}")
	if status_color is not None:
		s.append(f"status-color={status_color}")
	if detail is not None:
		s.append(f"detail={detail}")
	if s:
		s = ";".join(p.replace(';', ',').replace('\007', '') for p in s)
		s = f"\033]21337;{s}\007"
	else:
		s = ""

	return s


def _title(ps, title):
	if title is not None:
		return f"\033]{ps};{title.replace('\007', '')}\007"
	else:
		return ""


def icon_title(title=None):
	"""
	Return the escape sequence that sets the icon title of the terminal to
	``title``.

	The icon title is the name that a terminal traditionally uses for its
	minimized window. iTerm2 shows it as the title of the tab (unless the
	tab title is configured to be something else in the profile settings).
	The window title is not affected (see :func:`window_title` and
	:func:`window_and_icon_title`).

	The sequence used (``OSC 1``) is a standard xterm sequence, so it is
	understood by most other terminals too. As ``BEL`` terminates the
	sequence, any ``BEL`` in ``title`` is removed.

	If ``title`` is ``None`` (the default) an empty string is returned, so
	that outputting the result does nothing.
	"""

	return _title(1, title)


def window_title(title=None):
	"""
	Return the escape sequence that sets the window title of the terminal to
	``title``.

	iTerm2 shows the window title in the title bar of the window (unless the
	window title is configured to be something else in the profile settings).
	The icon title (i.e. the tab title) is not affected (see
	:func:`icon_title` and :func:`window_and_icon_title`).

	The sequence used (``OSC 2``) is a standard xterm sequence, so it is
	understood by most other terminals too. As ``BEL`` terminates the
	sequence, any ``BEL`` in ``title`` is removed.

	If ``title`` is ``None`` (the default) an empty string is returned, so
	that outputting the result does nothing.
	"""

	return _title(2, title)


def window_and_icon_title(title=None):
	"""
	Return the escape sequence that sets both the window title and the icon
	title of the terminal to ``title``.

	This is equivalent to outputting the results of :func:`window_title` and
	:func:`icon_title` in one sequence (``OSC 0``), which is a standard xterm
	sequence too. As ``BEL`` terminates the sequence, any ``BEL`` in ``title``
	is removed.

	If ``title`` is ``None`` (the default) an empty string is returned, so
	that outputting the result does nothing.
	"""

	return _title(0, title)


def badge(format=None):
	r"""
	Return the escape sequence that sets the badge__ of the current iTerm2
	session to ``format``.

	The badge is a large semi-transparent text that iTerm2 shows in the upper
	right corner of the session. ``format`` may contain references to iTerm2
	session variables like ``\(session.hostname)`` or ``\(user.foo)``, which
	iTerm2 interpolates when it displays the badge (this is why the argument
	is called ``format`` and not ``text``). An empty string removes the badge.

	The sequence used (``OSC 1337 ; SetBadgeFormat``) is proprietary to
	iTerm2. As ``format`` is transferred base64 encoded, it can contain
	arbitrary characters.

	If ``format`` is ``None`` (the default) an empty string is returned, so
	that outputting the result does nothing.

	__ https://iterm2.com/documentation-badges.html
	"""

	if format is not None:
		format = base64.b64encode(format.encode('utf-8')).decode('ascii')
		return f"\033]1337;SetBadgeFormat={format}\007"
	else:
		return ""


def notification(message=None):
	"""
	Return the escape sequence that makes iTerm2 post ``message`` as a macOS
	notification.

	iTerm2 shows the notification only if the session isn't currently the
	active session in the frontmost window (so that a program can e.g. notify
	the user about the end of a long running task the user isn't watching).
	Whether notifications are shown at all can be configured in the profile
	settings under "Terminal" -> "Notifications".

	The sequence used (``OSC 9``) is also supported by several other
	terminals. As ``BEL`` terminates the sequence, any ``BEL`` in ``message``
	is removed.

	If ``message`` is ``None`` (the default) an empty string is returned, so
	that outputting the result does nothing.
	"""

	if message is not None:
		return f"\033]9;{message.replace('\007', '')}\007"
	else:
		return ""


###
### Output
###
### These functions write the escape sequences returned by the functions above
### to the controlling terminal.
###

def _output(function, *args, **kwargs):
	"""
	Write the escape sequence returned by ``function(*args, **kwargs)`` to the
	controlling terminal (if there is one and we're running in iTerm2).
	"""

	if not running_in_iterm2():
		return
	s = function(*args, **kwargs)
	if s:
		try:
			with open("/dev/tty", "w") as tty:
				tty.write(s)
				tty.flush()
		except OSError:
			# No controlling terminal (CI, redirected output)
			pass


def set_session_status(status=None, indicator=None, status_color=None, detail=None):
	"""
	Set the session status of the current iTerm2 session.

	The arguments have the same meaning as for :func:`session_status`.
	"""

	_output(session_status, status=status, indicator=indicator, status_color=status_color, detail=detail)


def clear_session_status():
	"""
	Clear the session status of the current iTerm2 session (i.e. the status
	text, the indicator, the status color and the detail text).
	"""

	set_session_status(status="", indicator="", status_color="", detail="")


def set_icon_title(title=None):
	"""
	Set the icon title (i.e. the tab title) of the current iTerm2 session to
	``title``.

	If ``title`` is ``None`` nothing is done.
	"""

	_output(icon_title, title=title)


def set_window_title(title=None):
	"""
	Set the window title of the current iTerm2 session to ``title``.

	If ``title`` is ``None`` nothing is done.
	"""

	_output(window_title, title=title)


def set_window_and_icon_title(title=None):
	"""
	Set both the window title and the icon title (i.e. the tab title) of the
	current iTerm2 session to ``title``.

	If ``title`` is ``None`` nothing is done.
	"""

	_output(window_and_icon_title, title=title)


def set_badge(format=None):
	"""
	Set the badge of the current iTerm2 session to ``format`` (see
	:func:`badge` for the meaning of ``format``).

	If ``format`` is ``None`` nothing is done.
	"""

	_output(badge, format=format)


def set_notification(message=None):
	"""
	Post ``message`` as a macOS notification via iTerm2 (see
	:func:`notification`).

	If ``message`` is ``None`` nothing is done.
	"""

	_output(notification, message=message)
