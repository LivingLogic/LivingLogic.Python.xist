/*
** Copyright 2007-2013 by LivingLogic AG, Bayreuth, Germany.
** Copyright 2007-2013 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/


#include "Python.h"


/* define unicode version of xmlescape */
#define STRINGLIB_NAME               xmlescape_unicode
#define STRINGLIB_INTRO              int kind = PyUnicode_KIND(str);
#define STRINGLIB_CHAR               Py_UCS4
#define STRINGLIB_LEN(str)           PyUnicode_GET_LENGTH(str)
#define STRINGLIB_STR(str)           PyUnicode_DATA(str)
#define STRINGLIB_NEW(size, maxchar) PyUnicode_New(size, maxchar)
#define STRINGLIB_GET(str, i)        PyUnicode_READ(kind, str, i)
#define STRINGLIB_SET(str, i, c)     PyUnicode_WRITE(kind, str, i, c)

#include "_misc_include.c"

#undef STRINGLIB_NAME
#undef STRINGLIB_INTRO
#undef STRINGLIB_CHAR
#undef STRINGLIB_STR
#undef STRINGLIB_LEN
#undef STRINGLIB_NEW
#undef STRINGLIB_GET
#undef STRINGLIB_SET


/* define str version of xmlescape */
#define STRINGLIB_NAME               xmlescape_str
#define STRINGLIB_INTRO
#define STRINGLIB_CHAR               unsigned char
#define STRINGLIB_LEN(str)           PyBytes_GET_SIZE(str)
#define STRINGLIB_STR(str)           PyBytes_AS_STRING(str)
#define STRINGLIB_NEW(size, maxchar) PyBytes_FromStringAndSize(NULL, size)
#define STRINGLIB_GET(str, i)        (((unsigned char *)(str))[i])
#define STRINGLIB_SET(str, i, c)     ((((unsigned char *)(str))[i]) = (c))

#include "_misc_include.c"

#undef STRINGLIB_NAME
#undef STRINGLIB_INTRO
#undef STRINGLIB_CHAR
#undef STRINGLIB_STR
#undef STRINGLIB_LEN
#undef STRINGLIB_NEW
#undef STRINGLIB_GET
#undef STRINGLIB_SET


static PyObject *_xmlescape(PyObject *arg, int doquot, int doapos)
{
	if (PyUnicode_Check(arg))
	{
		return xmlescape_unicode(arg, doquot, doapos);
	}
	else if (PyBytes_Check(arg))
	{
		return xmlescape_str(arg, doquot, doapos);
	}
	else
	{
		PyErr_SetString(PyExc_TypeError, "expected a str or bytes object");
		return NULL;
	}
}

static PyObject *xmlescape(PyObject *self, PyObject *arg)
{
	return _xmlescape(arg, 1, 1);
}


static char xmlescape_doc[] =
"Return a copy of the argument string, where every occurrence of ``<``, ``>``,\n\
``&``, ``\"``, ``'`` and every restricted character has been replaced with\n\
their XML character entity or character reference.";


static PyObject *xmlescape_text(PyObject *self, PyObject *arg)
{
	return _xmlescape(arg, 0, 0);
}


static char xmlescape_text_doc[] =
"Return a copy of the argument string, where every occurrence of ``<``, ``>``,\n\
``&`` and every restricted character has been replaced with their XML character\n\
entity or character reference.";


static PyObject *xmlescape_attr(PyObject *self, PyObject *arg)
{
	return _xmlescape(arg, 1, 0);
}


static char xmlescape_attr_doc[] =
"Return a copy of the argument string, where every occurrence of ``<``, ``>``,\n\
``&``, , ``\"`` and every restricted character has been replaced with their\n\
XML character entity or character reference.";


static PyMethodDef _functions[] = {
	{"xmlescape",      (PyCFunction)xmlescape, METH_O,            xmlescape_doc},
	{"xmlescape_text", (PyCFunction)xmlescape_text, METH_O,       xmlescape_text_doc},
	{"xmlescape_attr", (PyCFunction)xmlescape_attr, METH_O,       xmlescape_attr_doc},
	{NULL,     NULL} /* sentinel */
};

static char module__doc__[] =
"This module contains the functions :func:`xmlescape`, :func:`xmlescape_text`\n\
and :func:`xmlescape_attr`";

static struct PyModuleDef _miscmodule = {
    PyModuleDef_HEAD_INIT,
    "_misc",
    module__doc__, /* module doc */
    -1,
    _functions,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit__misc(void)
{
    return PyModule_Create(&_miscmodule);
}
