/* Copyright 2000 by LivingLogic AG, Bayreuth, Germany.
** Copyright 2000 by Walter Dörwald
**
** See the file LICENSE for licensing details
*/

#include "Python.h"

static Py_UNICODE lt[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'l'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };
static Py_UNICODE gt[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'g'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };
static Py_UNICODE amp[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'a'), ((Py_UNICODE)'m'), ((Py_UNICODE)'p'), ((Py_UNICODE)';') };
static Py_UNICODE quot[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'q'), ((Py_UNICODE)'u'), ((Py_UNICODE)'o'), ((Py_UNICODE)'t'), ((Py_UNICODE)';') };
static Py_UNICODE apos[] = { ((Py_UNICODE)'&'), ((Py_UNICODE)'a'), ((Py_UNICODE)'p'), ((Py_UNICODE)'o'), ((Py_UNICODE)'s'), ((Py_UNICODE)';') };

#define COUNTOF(x) (sizeof(x)/sizeof((x)[0]))

static PyUnicodeObject *escapeUnencodable(PyUnicodeObject *str, const char *encoding)
{
	PyObject *test = PyUnicode_AsEncodedString((PyObject *)str, encoding, NULL);
	PyObject *result;

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

			/* determine the space, that we will need */
			for (i = 0; i < oldsize; ++i)
			{
				Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
				test = PyUnicode_Encode(&ch, 1, encoding, NULL);

				if (test == NULL) /* exception */
				{
					if (PyErr_ExceptionMatches(PyExc_UnicodeError)) /* we must create a character reference for it */
					{
						PyErr_Clear();

						if (ch < 10)
							newsize += 2+1+1;
						else if (ch < 100)
							newsize += 2+2+1;
						else if (ch < 1000)
							newsize += 2+3+1;
						else if (ch < 10000)
							newsize += 2+4+1;
						else
							newsize += 2+5+1;
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
						if (ch>10000)
						{
							*p++ = ((Py_UNICODE)'0') + ch/10000;
							ch = ch % 10000;
						}
						if (ch>1000)
						{
							*p++ = ((Py_UNICODE)'0') + ch/1000;
							ch = ch % 1000;
						}
						if (ch>100)
						{
							*p++ = ((Py_UNICODE)'0') + ch/100;
							ch = ch % 100;
						}
						if (ch>10)
						{
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
			return (PyUnicodeObject *)result;
		}
		else /* a "real exception" */
			return NULL;
	}
	else /* no exception, i.e. it worked, so we can use the string as it is */
	{
		Py_DECREF(test); /* we no longer need the encoded version */
		/* we don't incref here, the caller knows this */
		return str;
	}
}

static char escapeText__doc__[] =
"escapeText(unicode, encoding) -> unicode\n\
\n\
Return a copy of the string S, where every occurrence of\n\
'<', '>' and '&' and all unencodable characters in the\n\
specified encoding have been replaced with their XML character entity.";

static PyObject *escapeText(PyObject *self, PyObject *args)
{
	int i;
	int oldsize;
	int newsize = 0;
	PyUnicodeObject *str;
	const char *encoding = NULL;

	if (!PyArg_ParseTuple(args, "Os:escapeText", &str, &encoding))
		return NULL;
	str = (PyUnicodeObject *)PyUnicode_FromObject((PyObject *)str);
	if (str == NULL)
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
		/* nothing to replace, continue with charrefs */
		Py_INCREF(str);
		return (PyObject *)escapeUnencodable(str, encoding);
	}
	else
	{
		PyUnicodeObject *result = (PyUnicodeObject *)PyUnicode_FromUnicode(NULL, newsize);
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
		return (PyObject *)escapeUnencodable(result, encoding);
	}
}

static char escapeAttr__doc__[] =
"escapeAttr(unicode, encoding) -> unicode\n\
\n\
Return a copy of the string S, where every occurrence of\n\
'<', '>', '&', and '\"' and all unencodable characters in the\n\
specified encoding have been replaced with their XML character entity.";

static PyObject *escapeAttr(PyObject *self, PyObject *args)
{
	int i;
	int oldsize;
	int newsize = 0;
	PyUnicodeObject *str;
	const char *encoding;

	if (!PyArg_ParseTuple(args, "Os:escapeAttr", &str, &encoding))
		return NULL;
	str = (PyUnicodeObject *)PyUnicode_FromObject((PyObject *)str);
	if (str == NULL)
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
		/* nothing to replace, continue with charrefs */
		Py_INCREF(str);
		return (PyObject *)escapeUnencodable(str, encoding);
	}
	else
	{
		PyUnicodeObject *result = (PyUnicodeObject *)PyUnicode_FromUnicode(NULL, newsize);
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
		return (PyObject *)escapeUnencodable(result, encoding);
	}
}
/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"escapeText", escapeText, 1, escapeText__doc__},
	{"escapeAttr", escapeAttr, 1, escapeAttr__doc__},
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
