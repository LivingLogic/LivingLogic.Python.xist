#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<doc:par>This module provides a sandbox for the code that is evaluated in
XSC processing instructions (i.e. <code>&lt;?code:exec?&gt;</code> and
<code>&lt;?code:eval?&gt;</code>).</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc
