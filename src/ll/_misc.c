/*
** Copyright 2007-2019 by LivingLogic AG, Bayreuth, Germany.
** Copyright 2007-2019 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/


#include "Python.h"


/* define unicode version of xmlescape */
static PyObject *xmlescape_str(PyObject *str, int doquot, int doapos)
{
	Py_ssize_t oldsize;
	void *olddata;
	int maxchar = 127;
	Py_ssize_t i;
	Py_ssize_t newsize = 0;
	void *newdata;

	int kind = PyUnicode_KIND(str);

	oldsize = PyUnicode_GET_LENGTH(str);
	olddata = PyUnicode_DATA(str);
	for (i = 0; i < oldsize; ++i)
	{
		Py_UCS4 ch = PyUnicode_READ(kind, olddata, i);
		if (ch == ((Py_UCS4)'<'))
			newsize += 4; /* &lt; */
		else if (ch == (Py_UCS4)'>') /* Note that we always replace '>' with its entity, not just in case it is part of ']]>' */
			newsize += 4; /* &gt; */
		else if (ch == (Py_UCS4)'&')
			newsize += 5; /* &amp; */
		else if ((ch == (Py_UCS4)'"') && doquot)
			newsize += 6; /* &quot; */
		else if ((ch == (Py_UCS4)'\'') && doapos)
			newsize += 5; /* &#39; */
		else if (ch <= 0x8)
			newsize += 4;
		else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			newsize += 5;
		else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			newsize += 6;
		else
		{
			newsize++;
			if (ch > maxchar)
				maxchar = ch;
		}
	}
	if (oldsize==newsize)
	{
		/* nothing to replace => return original */
		Py_INCREF(str);
		return str;
	}
	else
	{
		int index = 0;
		PyObject *result = PyUnicode_New(newsize, maxchar);
		newdata = PyUnicode_DATA(result);
		if (result == NULL)
			return NULL;
		for (i = 0; i < oldsize; ++i)
		{
			Py_UCS4 ch = PyUnicode_READ(kind, olddata, i);
			if (ch == (Py_UCS4)'<')
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, 'l');
				PyUnicode_WRITE(kind, newdata, index++, 't');
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if (ch == (Py_UCS4)'>')
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, 'g');
				PyUnicode_WRITE(kind, newdata, index++, 't');
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if (ch == (Py_UCS4)'&')
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, 'a');
				PyUnicode_WRITE(kind, newdata, index++, 'm');
				PyUnicode_WRITE(kind, newdata, index++, 'p');
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if ((ch == (Py_UCS4)'"') && doquot)
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, 'q');
				PyUnicode_WRITE(kind, newdata, index++, 'u');
				PyUnicode_WRITE(kind, newdata, index++, 'o');
				PyUnicode_WRITE(kind, newdata, index++, 't');
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if ((ch == (Py_UCS4)'\'') && doapos)
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, '#');
				PyUnicode_WRITE(kind, newdata, index++, '3');
				PyUnicode_WRITE(kind, newdata, index++, '9');
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if (ch <= 0x8)
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, '#');
				PyUnicode_WRITE(kind, newdata, index++, '0'+ch);
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, '#');
				PyUnicode_WRITE(kind, newdata, index++, '0'+ch/10);
				PyUnicode_WRITE(kind, newdata, index++, '0'+ch%10);
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			{
				PyUnicode_WRITE(kind, newdata, index++, '&');
				PyUnicode_WRITE(kind, newdata, index++, '#');
				PyUnicode_WRITE(kind, newdata, index++, '0'+ch/100);
				PyUnicode_WRITE(kind, newdata, index++, '0'+(ch/10)%10);
				PyUnicode_WRITE(kind, newdata, index++, '0'+ch%10);
				PyUnicode_WRITE(kind, newdata, index++, ';');
			}
			else
				PyUnicode_WRITE(kind, newdata, index++, ch);
		}
		return result;
	}
}


/* define bytes version of xmlescape */
static PyObject *xmlescape_bytes(PyObject *str, int doquot, int doapos)
{
	Py_ssize_t oldsize;
	unsigned char *olddata;
	int maxchar = 127;
	Py_ssize_t i;
	Py_ssize_t newsize = 0;
	unsigned char *newdata;

	oldsize = PyBytes_GET_SIZE(str);
	olddata = (unsigned char *)PyBytes_AS_STRING(str);
	for (i = 0; i < oldsize; ++i)
	{
		unsigned char ch = olddata[i];
		if (ch == '<')
			newsize += 4; /* &lt; */
		else if (ch == '>') /* Note that we always replace '>' with its entity, not just in case it is part of ']]>' */
			newsize += 4; /* &gt; */
		else if (ch == '&')
			newsize += 5; /* &amp; */
		else if ((ch == '"') && doquot)
			newsize += 6; /* &quot; */
		else if ((ch == '\'') && doapos)
			newsize += 5; /* &#39; */
		else if (ch <= 0x8)
			newsize += 4;
		else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			newsize += 5;
		else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			newsize += 6;
		else
		{
			newsize++;
			if (ch > maxchar)
				maxchar = ch;
		}
	}
	if (oldsize==newsize)
	{
		/* nothing to replace => return original */
		Py_INCREF(str);
		return str;
	}
	else
	{
		int index = 0;
		PyObject *result = PyBytes_FromStringAndSize(NULL, newsize);
		newdata = (unsigned char *)PyBytes_AS_STRING(result);
		if (result == NULL)
			return NULL;
		for (i = 0; i < oldsize; ++i)
		{
			unsigned char ch = olddata[i];
			if (ch == '<')
			{
				newdata[index++] = '&';
				newdata[index++] = 'l';
				newdata[index++] = 't';
				newdata[index++] = ';';
			}
			else if (ch == '>')
			{
				newdata[index++] = '&';
				newdata[index++] = 'g';
				newdata[index++] = 't';
				newdata[index++] = ';';
			}
			else if (ch == '&')
			{
				newdata[index++] = '&';
				newdata[index++] = 'a';
				newdata[index++] = 'm';
				newdata[index++] = 'p';
				newdata[index++] = ';';
			}
			else if ((ch == '"') && doquot)
			{
				newdata[index++] = '&';
				newdata[index++] = 'q';
				newdata[index++] = 'u';
				newdata[index++] = 'o';
				newdata[index++] = 't';
				newdata[index++] = ';';
			}
			else if ((ch == '\'') && doapos)
			{
				newdata[index++] = '&';
				newdata[index++] = '#';
				newdata[index++] = '3';
				newdata[index++] = '9';
				newdata[index++] = ';';
			}
			else if (ch <= 0x8)
			{
				newdata[index++] = '&';
				newdata[index++] = '#';
				newdata[index++] = '0'+ch;
				newdata[index++] = ';';
			}
			else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			{
				newdata[index++] = '&';
				newdata[index++] = '#';
				newdata[index++] = '0'+ch/10;
				newdata[index++] = '0'+ch%10;
				newdata[index++] = ';';
			}
			else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			{
				newdata[index++] = '&';
				newdata[index++] = '#';
				newdata[index++] = '0'+ch/100;
				newdata[index++] = '0'+(ch/10)%10;
				newdata[index++] = '0'+ch%10;
				newdata[index++] = ';';
			}
			else
				newdata[index++] = ch;
		}
		return result;
	}
}


static PyObject *_xmlescape(PyObject *arg, int doquot, int doapos)
{
	if (PyUnicode_Check(arg))
	{
		return xmlescape_str(arg, doquot, doapos);
	}
	else if (PyBytes_Check(arg))
	{
		return xmlescape_bytes(arg, doquot, doapos);
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
	{"xmlescape",      (PyCFunction)xmlescape, METH_O,      xmlescape_doc},
	{"xmlescape_text", (PyCFunction)xmlescape_text, METH_O, xmlescape_text_doc},
	{"xmlescape_attr", (PyCFunction)xmlescape_attr, METH_O, xmlescape_attr_doc},
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
