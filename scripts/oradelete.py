#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True


import sys


if __name__ == "__main__":
	from ll.orasql.scripts import oradelete
	sys.exit(oradelete.main())
