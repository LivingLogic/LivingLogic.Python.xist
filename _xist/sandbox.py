#! /usr/bin/env python

"""
This module provides a sandbox for the code that is evaluated in
XSC processing instructions (i.e. <?code:exec?> and <?code:eval?>).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc
