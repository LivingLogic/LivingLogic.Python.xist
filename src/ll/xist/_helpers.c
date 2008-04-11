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

#include "_helpers_include.c"

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

#include "_helpers_include.c"

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
``<``, ``>``, ``&`` and every restricted character has been replaced\n\
with its XML character entity or character reference.";


static PyObject *escapetext(PyObject *self, PyObject *arg)
{
	return escape(arg, 0);
}


static char escapeattr__doc__[] =
"Return a copy of the argument string, where every occurrence of\n\
``<``, ``>``, ``&``, ``\"``` and every restricted character has been replaced\n\
with their XML character entity or character reference.";


static PyObject *escapeattr(PyObject *self, PyObject *arg)
{
	return escape(arg, 1);
}


/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"escapetext", escapetext, METH_O, escapetext__doc__},
	{"escapeattr", escapeattr, METH_O, escapeattr__doc__},
	{NULL, NULL}
};


void
#ifdef WIN32
__declspec(dllexport)
#endif
init_helpers(void)
{
	Py_InitModule("_helpers", _functions);
}
