/*
** Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
** Copyright 1999-2002 by Walter Dörwald
**
** All Rights Reserved
**
** Permission to use, copy, modify, and distribute this software and its documentation
** for any purpose and without fee is hereby granted, provided that the above copyright
** notice appears in all copies and that both that copyright notice and this permission
** notice appear in supporting documentation, and that the name of LivingLogic AG or
** the author not be used in advertising or publicity pertaining to distribution of the
** software without specific, written prior permission.
**
** LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
** INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
** LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
** DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
** IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
** IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

#include "Python.h"

static Py_UNICODE lt[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'l'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };
static Py_UNICODE gt[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'g'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };
static Py_UNICODE amp[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'a'), ((Py_UNICODE)'m'), ((Py_UNICODE)'p'), ((Py_UNICODE)';') };
static Py_UNICODE quot[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'q'), ((Py_UNICODE)'u'), ((Py_UNICODE)'o'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };

static Py_UNICODE hexdigits[] = { (Py_UNICODE)'0', (Py_UNICODE)'1', (Py_UNICODE)'2', (Py_UNICODE)'3', (Py_UNICODE)'4', (Py_UNICODE)'5', (Py_UNICODE)'6', (Py_UNICODE)'7', (Py_UNICODE)'8', (Py_UNICODE)'9', (Py_UNICODE)'A', (Py_UNICODE)'B', (Py_UNICODE)'C', (Py_UNICODE)'D', (Py_UNICODE)'E', (Py_UNICODE)'F' };

#define COUNTOF(x) (sizeof(x)/sizeof((x)[0]))

static char escapetext__doc__[] =
"escapetext(unicode) -> unicode\n\
\n\
Return a copy of the string S, where every occurrence of\n\
'<', '>' and '&' has been replaced with its XML character entity.";

static PyObject *escapetext(PyObject *self, PyObject *args)
{
	int i;
	PyObject *str;
	int oldsize;
	int newsize = 0;

	if (!PyArg_ParseTuple(args, "O!:escapetext", &PyUnicode_Type, &str))
		return NULL;

	oldsize = PyUnicode_GET_SIZE(str);
	for (i = 0; i < oldsize; ++i)
	{
		Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
		if (ch == ((Py_UNICODE)'<'))
			newsize += COUNTOF(lt);
		else if (ch == ((Py_UNICODE)'>')) /* Note that we always replace '>' with its entity, not just in case it is part of ']]>' */
			newsize += COUNTOF(gt);
		else if (ch == ((Py_UNICODE)'&'))
			newsize += COUNTOF(amp);
		else
			newsize++;
	}
	if (oldsize==newsize)
	{
		/* nothing to replace => return original */
		Py_INCREF(str);
		return str;
	}
	else
	{
		PyObject *result = PyUnicode_FromUnicode(NULL, newsize);
		Py_UNICODE *p;
		if (result == NULL)
			return NULL;
		p = PyUnicode_AS_UNICODE(result);
		for (i = 0; i < oldsize; ++i)
		{
			Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
			if (ch == ((Py_UNICODE)'<'))
			{
				Py_UNICODE_COPY(p, lt, COUNTOF(lt));
				p += COUNTOF(lt);
			}
			else if (ch == ((Py_UNICODE)'>'))
			{
				Py_UNICODE_COPY(p, gt, COUNTOF(gt));
				p += COUNTOF(gt);
			}
			else if (ch == ((Py_UNICODE)'&'))
			{
				Py_UNICODE_COPY(p, amp, COUNTOF(amp));
				p += COUNTOF(amp);
			}
			else
				*p++ = ch;
		}
		return result;
	}
}

static char escapeattr__doc__[] =
"escapeattr(unicode) -> unicode\n\
\n\
Return a copy of the string S, where every occurrence of\n\
'<', '>', '&', and '\"' has been replaced with their XML\n\
character entity.";

static PyObject *escapeattr(PyObject *self, PyObject *args)
{
	int i;
	PyObject *str;
	int oldsize;
	int newsize = 0;

	if (!PyArg_ParseTuple(args, "O!:escapeattr", &PyUnicode_Type, &str))
		return NULL;

	oldsize = PyUnicode_GET_SIZE(str);
	for (i = 0; i < oldsize; ++i)
	{
		Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
		if (ch == ((Py_UNICODE)'<'))
			newsize += COUNTOF(lt);
		else if (ch == ((Py_UNICODE)'>'))
			newsize += COUNTOF(gt);
		else if (ch == ((Py_UNICODE)'&'))
			newsize += COUNTOF(amp);
		else if (ch == ((Py_UNICODE)'\"'))
			newsize += COUNTOF(quot);
		else
			newsize++;
	}
	if (oldsize==newsize)
	{
		/* nothing to replace => return original */
		Py_INCREF(str);
		return str;
	}
	else
	{
		PyObject *result = PyUnicode_FromUnicode(NULL, newsize);
		Py_UNICODE *p;
		if (result == NULL)
			return NULL;
		p = PyUnicode_AS_UNICODE(result);
		for (i = 0; i < oldsize; ++i)
		{
			Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
			if (ch == ((Py_UNICODE)'<'))
			{
				Py_UNICODE_COPY(p, lt, COUNTOF(lt));
				p += COUNTOF(lt);
			}
			else if (ch == ((Py_UNICODE)'>'))
			{
				Py_UNICODE_COPY(p, gt, COUNTOF(gt));
				p += COUNTOF(gt);
			}
			else if (ch == ((Py_UNICODE)'&'))
			{
				Py_UNICODE_COPY(p, amp, COUNTOF(amp));
				p += COUNTOF(amp);
			}
			else if (ch == ((Py_UNICODE)'"'))
			{
				Py_UNICODE_COPY(p, quot, COUNTOF(quot));
				p += COUNTOF(quot);
			}
			else
				*p++ = ch;
		}
		return result;
	}
}

static char xmlcharrefreplace__doc__[] =
"xmlcharrefreplace(unicode, encoding) -> unicode\n\
\n\
Return a copy of the string S, where every unencodable character\n\
in the specified encoding has been replaced with an XML character\n\
reference.";

static PyObject *xmlcharrefreplace(PyObject *self, PyObject *args)
{
	PyObject *str;
	char *encoding;
	PyObject *test;

	if (!PyArg_ParseTuple(args, "Os:xmlcharrefreplace", &str, &encoding))
		return NULL;

	test = PyUnicode_AsEncodedString((PyObject *)str, encoding, NULL);

	if (test == NULL) /* an exception has occurred */
	{
		if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* OK, we try it character by character */
		{
			int i;
			int oldsize = PyUnicode_GET_SIZE(str);
			int newsize = 0;
			PyObject *result;
			Py_UNICODE *p;

			PyErr_Clear();

			/* determine the space we'll need */
			for (i = 0; i < oldsize; ++i)
			{
				Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
				test = PyUnicode_Encode(&ch, 1, encoding, NULL);

				if (test == NULL) /* exception */
				{
					if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* we must create a character reference for it */
					{
						PyErr_Clear();

						/* We use decimal charref, because they are more efficient in most cases, i.e. upto 1000000 */
						#if Py_UNICODE_SIZE==4
						if (ch>=1000000)
							newsize += 2+7+1;
						else if (ch>=100000)
							newsize += 2+6+1;
						else
						#endif
						if (ch>=10000)
							newsize += 2+5+1;
						else if (ch>=1000)
							newsize += 2+4+1;
						else if (ch>=100)
							newsize += 2+3+1;
						else if (ch>=10)
							newsize += 2+2+1;
						else
							newsize += 2+1+1;
					}
					else
						return NULL;
				}
				else /* we were able to encode this character, so use it */
				{
					++newsize;
					Py_DECREF(test);
				}
			}

			/* allocate what we calculated */
			result = PyUnicode_FromUnicode(NULL, newsize);

			if (result == NULL)
				return NULL;

			/* create the string */
			p = PyUnicode_AS_UNICODE(result);
			for (i = 0; i < oldsize; ++i)
			{
				Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
				test = PyUnicode_Encode(&ch, 1, encoding, NULL);

				if (test == NULL) /* exception */
				{
					if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* we must create a character reference for it */
					{
						PyErr_Clear();

						*p++ = (Py_UNICODE)'&';
						*p++ = (Py_UNICODE)'#';
						#if Py_UNICODE_SIZE==4
						if (ch>=1000000)
						{
							*p++ = ((Py_UNICODE)'0') + ch/1000000;
							ch = ch % 1000000;
							goto digit1;
						}
						if (ch>=100000)
						{
							digit1:
							*p++ = ((Py_UNICODE)'0') + ch/100000;
							ch = ch % 100000;
							goto digit2;
						}
						#endif
						if (ch>=10000)
						{
							#if Py_UNICODE_SIZE==4
							digit2:
							#endif
							*p++ = ((Py_UNICODE)'0') + ch/10000;
							ch = ch % 10000;
							goto digit3;
						}
						if (ch>=1000)
						{
							digit3:
							*p++ = ((Py_UNICODE)'0') + ch/1000;
							ch = ch % 1000;
							goto digit4;
						}
						if (ch>=100)
						{
							digit4:
							*p++ = ((Py_UNICODE)'0') + ch/100;
							ch = ch % 100;
							goto digit5;
						}
						if (ch>=10)
						{
							digit5:
							*p++ = ((Py_UNICODE)'0') + ch/10;
							ch = ch % 10;
						}
						*p++ = ((Py_UNICODE)'0') + ch;
						*p++ = (Py_UNICODE)';';
					}
					else
					{
						Py_DECREF(result);
						return NULL;
					}
				}
				else /* we were able to encode this character, so use it */
				{
					*p++ = ch;
					Py_DECREF(test);
				}
			}
			return result;
		}
		else /* a "real exception" */
			return NULL;
	}
	else /* no exception, i.e. it worked, so we can use the string as it is */
	{
		Py_DECREF(test); /* we no longer need the encoded version */
		Py_INCREF(str);
		return str;
	}
}

static char cssescapereplace__doc__[] =
"cssescapereplace(unicode, encoding) -> unicode\n\
\n\
Return a copy of the string S, where every unencodable character\n\
in the specified encoding has been replaced with a \\xx hexadecimal\n\
escape sequence.";

static PyObject *cssescapereplace(PyObject *self, PyObject *args)
{
	PyObject *str;
	int oldsize;
	const char *encoding;
	PyObject *test;

	if (!PyArg_ParseTuple(args, "O!s:cssescapereplace", &PyUnicode_Type, &str, &encoding))
		return NULL;

	oldsize = PyUnicode_GET_SIZE(str);
	test = PyUnicode_AsEncodedString((PyObject *)str, encoding, NULL);

	if (test == NULL) /* an exception has occurred */
	{
		if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* OK, we try it character by character */
		{
			int i;
			int oldsize = PyUnicode_GET_SIZE(str);
			int newsize = 0;
			PyObject *result;
			Py_UNICODE *p;

			PyErr_Clear();

			/* determine the space we'll need */
			for (i = 0; i < oldsize; ++i)
			{
				Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
				test = PyUnicode_Encode(&ch, 1, encoding, NULL);

				if (test == NULL) /* exception */
				{
					if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* we must create a character reference for it */
					{
						PyErr_Clear();

						#if Py_UNICODE_SIZE==4
						if (ch>=0x100000)
							newsize += 1+6;
						else if (ch>=0x10000)
							newsize += 1+5;
						else
						#endif
						if (ch>=0x1000)
							newsize += 1+4;
						else if (ch>=0x100)
							newsize += 1+3;
						else if (ch>=0x10)
							newsize += 1+2;
						else
							newsize += 1+1;
					}
					else
						return NULL;
				}
				else /* we were able to encode this character, so use it */
				{
					++newsize;
					Py_DECREF(test);
				}
			}

			/* allocate what we calculated */
			result = PyUnicode_FromUnicode(NULL, newsize);

			if (result == NULL)
				return NULL;

			/* create the string */
			p = PyUnicode_AS_UNICODE(result);
			for (i = 0; i < oldsize; ++i)
			{
				Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
				test = PyUnicode_Encode(&ch, 1, encoding, NULL);

				if (test == NULL) /* exception */
				{
					if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* we must create a character reference for it */
					{
						PyErr_Clear();

						*p++ = (Py_UNICODE)'\\';
						#if Py_UNICODE_SIZE==4
						if (ch>=0x100000)
						{
							*p++ = hexdigits[ch/0x100000];
							ch = ch % 0x100000;
							goto digit1;
						}
						if (ch>=0x10000)
						{
							digit1:
							*p++ = hexdigits[ch/0x10000];
							ch = ch % 0x10000;
							goto digit2;
						}
						#endif
						if (ch>=0x1000)
						{
							digit2:
							*p++ = hexdigits[ch/0x1000];
							ch = ch % 0x1000;
							goto digit3;
						}
						if (ch>=0x100)
						{
							digit3:
							*p++ = hexdigits[ch/0x100];
							ch = ch % 0x100;
							goto digit4;
						}
						if (ch>=0x10)
						{
							digit4:
							*p++ = hexdigits[ch/0x10];
							ch = ch % 0x10;
						}
						*p++ = hexdigits[ch];
					}
					else
					{
						Py_DECREF(result);
						return NULL;
					}
				}
				else /* we were able to encode this character, so use it */
				{
					*p++ = ch;
					Py_DECREF(test);
				}
			}
			return result;
		}
		else /* a "real exception" */
			return NULL;
	}
	else /* no exception, i.e. it worked, so we can use the string as it is */
	{
		Py_DECREF(test); /* we no longer need the encoded version */
		Py_INCREF(str);
		return str;
	}
}

static char strict__doc__[] =
"strict(unicode, encoding) -> unicode\n\
\n\
Return a copy of the string S without any replacements.";

static PyObject *strict(PyObject *self, PyObject *args)
{
	PyObject *str;
	int oldsize;
	const char *encoding;
	PyObject *test;

	if (!PyArg_ParseTuple(args, "O!s:cssescapereplace", &PyUnicode_Type, &str, &encoding))
		return NULL;

	Py_INCREF(str);
	return str;
}

/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"xmlcharrefreplace", xmlcharrefreplace, METH_VARARGS, xmlcharrefreplace__doc__},
	{"cssescapereplace",  cssescapereplace,  METH_VARARGS, cssescapereplace__doc__ },
	{"strict",            strict,            METH_VARARGS, strict__doc__ },
	{"escapetext",        escapetext,        METH_VARARGS, escapetext__doc__},
	{"escapeattr",        escapeattr,        METH_VARARGS, escapeattr__doc__},
	{NULL, NULL}
};

void
#ifdef WIN32
__declspec(dllexport)
#endif
inithelpers(void)
{
	Py_InitModule("helpers", _functions);
}
