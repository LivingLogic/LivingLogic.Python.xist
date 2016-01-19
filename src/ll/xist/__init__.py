# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.
##
##
## This software includes sgmlop by Fredrik Lundh:
## http://effbot.org/zone/sgmlop-index.htm
##
## Copyright (c) 1998-2007 by Secret Labs AB
## Copyright (c) 1998-2007 by Fredrik Lundh
##
## fredrik@pythonware.com
## http://www.pythonware.com
##
## By obtaining, using, and/or copying this software and/or its
## associated documentation, you agree that you have read, understood,
## and will comply with the following terms and conditions:
##
## Permission to use, copy, modify, and distribute this software and its
## associated documentation for any purpose and without fee is hereby
## granted, provided that the above copyright notice appears in all
## copies, and that both that copyright notice and this permission notice
## appear in supporting documentation, and that the name of Secret Labs
## AB or the author not be used in advertising or publicity pertaining to
## distribution of the software without specific, written prior
## permission.
##
## SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
## THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR
## ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
## WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
## ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
## OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
##
##
## This software includes the ANTLR runtime:
## [The "BSD licence"]
## Copyright (c) 2005-2008 Terence Parr
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions
## are met:
## 1. Redistributions of source code must retain the above copyright
##    notice, this list of conditions and the following disclaimer.
## 2. Redistributions in binary form must reproduce the above copyright
##    notice, this list of conditions and the following disclaimer in the
##    documentation and/or other materials provided with the distribution.
## 3. The name of the author may not be used to endorse or promote products
##    derived from this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
## IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
## OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
## IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
## INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
## NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
## THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
##
## This software includes jsmin by Douglas Crockford/Baruch Even:
## http://www.crockford.com/javascript/jsmin.py.txt
##
## This code is original from jsmin by Douglas Crockford, it was translated to
## Python by Baruch Even. The original code had the following copyright and
## license.
##
## /* jsmin.c
##    2007-05-22
##
## Copyright (c) 2002 Douglas Crockford  (www.crockford.com)
##
## Permission is hereby granted, free of charge, to any person obtaining a copy of
## this software and associated documentation files (the "Software"), to deal in
## the Software without restriction, including without limitation the rights to
## use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
## of the Software, and to permit persons to whom the Software is furnished to do
## so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## The Software shall be used for Good, not Evil.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

"""
XIST is an extensible HTML and XML generator. XIST is also a XML parser with a
very simple and pythonesque tree API. Every XML element type corresponds to a
Python class and these Python classes provide a conversion method to transform
the XML tree (e.g. into HTML). XIST can be considered 'object oriented XSLT'.

XIST was written as a replacement for the HTML preprocessor HSC__, and borrows
some features and ideas from it.

__ https://github.com/mbethke/hsc

It also borrows the basic ideas (XML/HTML elements as Python objects) from
HTMLgen_ and HyperText_.

.. _HTMLgen: http://www.linuxjournal.com/article/2986
.. _HyperText: http://dustman.net/andy/python/HyperText
"""


__docformat__ = "reStructuredText"


__all__ = ["xsc", "present", "parse", "sims", "xnd", "xfind", "ns"]
