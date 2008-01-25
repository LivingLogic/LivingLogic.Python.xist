/*
** Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
** Copyright 1999-2008 by Walter Dörwald
**
** All Rights Reserved
**
** See xist/__init__.py for the license
*/


#define PY_SSIZE_T_CLEAN
#include "Python.h"


/* Backwards compatibility defines */
#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif

/* define unicode version of escape */
#define STRINGLIB_NAME escape_unicode
#define STRINGLIB_CHAR Py_UNICODE
#define STRINGLIB_LEN  PyUnicode_GET_SIZE
#define STRINGLIB_NEW  PyUnicode_FromUnicode
#define STRINGLIB_STR  PyUnicode_AS_UNICODE

#include "helpers_include.c"

#undef STRINGLIB_NAME
#undef STRINGLIB_CHAR
#undef STRINGLIB_LEN
#undef STRINGLIB_NEW
#undef STRINGLIB_STR


/* define str version of escape */
#define STRINGLIB_NAME escape_str
#define STRINGLIB_CHAR unsigned char
#define STRINGLIB_LEN PyString_GET_SIZE
#define STRINGLIB_NEW PyString_FromStringAndSize
#define STRINGLIB_STR PyString_AS_STRING

#include "helpers_include.c"

#undef STRINGLIB_NAME
#undef STRINGLIB_CHAR
#undef STRINGLIB_LEN
#undef STRINGLIB_NEW
#undef STRINGLIB_STR


static PyObject *escape(PyObject *str, int inattr)
{
	if (PyUnicode_Check(str))
	{
		return escape_unicode(str, inattr);
	}
	else if (PyString_Check(str))
	{
		return escape_str(str, inattr);
	}
	else
	{
		PyErr_SetString(PyExc_TypeError, "expected a str or unicode object");
		return NULL;
	}
}


static char escapetext__doc__[] =
"Return a copy of the argument string, where every occurrence of\n\
``<``, ``>``, ``&`` and restricted characters has been replaced\n\
with its XML character entity or character reference.";


static PyObject *escapetext(PyObject *self, PyObject *arg)
{
	return escape(arg, 0);
}


static char escapeattr__doc__[] =
"Return a copy of the argument string, where every occurrence of\n\
``<``, ``>``, ``&``, ``\"``` and restricted characters has been replaced\n\
with their XML character entity or character reference.";


static PyObject *escapeattr(PyObject *self, PyObject *arg)
{
	return escape(arg, 1);
}


static char cssescapereplace__doc__[] =
"Return a copy of the argument string, where every unencodable character\n\
in the specified encoding has been replaced with a ``\\xx`` hexadecimal\n\
escape sequence.";


static Py_UNICODE hexdigits[] = { (Py_UNICODE)'0', (Py_UNICODE)'1', (Py_UNICODE)'2', (Py_UNICODE)'3', (Py_UNICODE)'4', (Py_UNICODE)'5', (Py_UNICODE)'6', (Py_UNICODE)'7', (Py_UNICODE)'8', (Py_UNICODE)'9', (Py_UNICODE)'A', (Py_UNICODE)'B', (Py_UNICODE)'C', (Py_UNICODE)'D', (Py_UNICODE)'E', (Py_UNICODE)'F' };

static PyObject *cssescapereplace(PyObject *self, PyObject *args)
{
	PyObject *str;
	Py_ssize_t oldsize;
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
			Py_ssize_t i;
			Py_ssize_t oldsize = PyUnicode_GET_SIZE(str);
			Py_ssize_t newsize = 0;
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


/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"cssescapereplace", cssescapereplace, METH_VARARGS, cssescapereplace__doc__ },
	{"escapetext",       escapetext,       METH_O      , escapetext__doc__},
	{"escapeattr",       escapeattr,       METH_O      , escapeattr__doc__},
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
