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

static char escapeText__doc__[] =
"escapeText(unicode) -> unicode\n\
\n\
Return a copy of the string S, where every occurrence of\n\
'<', '>', '&', '\"' and \"'\" has been replaced with its XML\n\
character entity.";

static PyObject *escapeText(PyObject *self, PyObject *args)
{
	int i;
	int oldsize;
	int newsize = 0;
	PyUnicodeObject *str;

	if (!PyArg_ParseTuple(args, "O:escapexml", &str))
		return NULL;
	str = (PyUnicodeObject *)PyUnicode_FromObject((PyObject *)str);
	if (str == NULL)
		return NULL;

	oldsize = PyUnicode_GET_SIZE(str);
	for (i = 0; i < oldsize; ++i)
	{
		Py_UNICODE ch = PyUnicode_AS_UNICODE(str)[i];
		if ((ch == ((Py_UNICODE)'<')) || (ch == ((Py_UNICODE)'>')))
			newsize += 4;
		else if ((ch == ((Py_UNICODE)'\'')) || (ch == ((Py_UNICODE)'"')))
			newsize += 6;
		else if (ch == ((Py_UNICODE)'&'))
			newsize += 5;
		else
		newsize++;
	}
	if (oldsize==newsize)
	{
		/* nothing to replace, return original string */
		Py_INCREF(str);
		return (PyObject *)str;
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
				Py_UNICODE_COPY(p, lt, 4);
				p += 4;
			}
			else if (ch == ((Py_UNICODE)'>'))
			{
				Py_UNICODE_COPY(p, gt, 4);
				p += 4;
			}
			else if (ch == ((Py_UNICODE)'&'))
			{
				Py_UNICODE_COPY(p, amp, 5);
				p += 5;
			}
			else if (ch == ((Py_UNICODE)'\''))
			{
				Py_UNICODE_COPY(p, apos, 6);
				p += 6;
			}
			else if (ch == ((Py_UNICODE)'"'))
			{
				Py_UNICODE_COPY(p, quot, 6);
				p += 6;
			}
			else
				*p++ = ch;
		}
		return (PyObject *)result;
	}
}
/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"escapeText", escapeText, 1, escapeText__doc__},
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
