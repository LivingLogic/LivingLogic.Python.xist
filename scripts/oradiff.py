#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3

import sys


if __name__ == "__main__":
	from ll.orasql.scripts import oradiff
	sys.exit(oradiff.main())
