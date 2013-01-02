/*
** Copyright 2002-2013 by LivingLogic AG, Bayreuth, Germany.
** Copyright 2002-2013 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/

#include "Python.h"

static char escape__doc__[] =
"escape(string, safe) -> string\n\
\n\
Escape any character not in safe with a %xx sequence.\n\
If safe is not specified all 7bit characters are considered safe.";

static char hexdigits[16] = "0123456789ABCDEF";

static PyObject *escape(PyObject *self, PyObject *args)
{
	PyObject *str;
	PyObject *uni;
	char *safe = NULL;
	PyObject *res;
	unsigned char *s;
	unsigned char *starts;
	unsigned char *ends;
	Py_UNICODE *r;
	Py_UNICODE *startr;
	Py_UNICODE *endr;
	int newsize;

	if (!PyArg_ParseTuple(args, "O|s:escape", &str, &safe))
		return NULL;

	uni = PyUnicode_FromObject(str);
	if (!uni)
		return NULL;
	str = PyUnicode_EncodeUTF8(PyUnicode_AS_UNICODE(uni), PyUnicode_GET_SIZE(uni), NULL);
	if (!str)
	{
		Py_DECREF(uni);
		return NULL;
	}

	starts = PyBytes_AS_STRING(str);
	ends = starts + PyBytes_GET_SIZE(str);

	for (newsize = 0, s = starts; s < ends; ++s)
	{
		if (safe ? (strchr(safe, *s)!=NULL) : (*s<0x80))
			++newsize;
		else
			newsize += 3;
	}

	res = PyUnicode_FromStringAndSize(NULL, newsize);
	if (res)
	{
		startr = PyUnicode_AS_UNICODE(res);
		endr = startr + PyUnicode_GET_SIZE(res);

		for (s = starts, r = startr; s < ends;)
		{
			if (safe ? (strchr(safe, *s)!=NULL) : (*s<0x80))
				*r++ = *s++;
			else
			{
				*r++ = '%';
				*r++ = hexdigits[((*s)>>4) & 0xf];
				*r++ = hexdigits[(*s++) & 0xf];
			}
		}
	}
	Py_DECREF(str);
	Py_DECREF(uni);
	return res;
}

static char unescape__doc__[] =
"unescape(string) -> unicode\n\
\n\
Unescape a %-escaped string. The result will be UTF-8 decoded if possible.\n\
If this fails, ISO-8859-1 will be tried.";

static PyObject *unescape(PyObject *self, PyObject *args)
{
	char *in;
	int len;
	char *res;
	int pos = 0;
	char *out;
	PyObject *uni;

	if (!PyArg_ParseTuple(args, "s#:unescape", &in, &len))
		return NULL;

	res = PyMem_Malloc(len);
	if (!res)
		return NULL;

	out = res;
	while (pos<len)
	{
		if (in[pos] != '%')
			*out++ = in[pos++];
		else
		{
			char buffer[100];
			if (pos+3>len)
			{
				sprintf(buffer, "truncated escape at position %d", pos);
				if (PyErr_Warn(PyExc_UserWarning, buffer))
				{
					PyMem_Free(res);
					return NULL;
				}
				/* copy the characters literally */
				while (pos<len)
					*out++ = in[pos++];
			}
			else
			{
				if ((!isxdigit(in[pos+1])) || (!isxdigit(in[pos+2])))
				{
					sprintf(buffer, "malformed escape at position %d", pos);
					if (PyErr_Warn(PyExc_UserWarning, buffer) < 0)
					{
						PyMem_Free(res);
						return NULL;
					}
					*out++ = in[pos];
					*out++ = in[pos+1];
					*out++ = in[pos+2];
				}
				else
				{
					buffer[0] = in[pos+1];
					buffer[1] = in[pos+2];
					buffer[2] = '\0';
					*out++ = (char)strtol(buffer, NULL, 16);
				}
				pos += 3;
			}
		}
	}

	uni = PyUnicode_Decode(res, out-res, "utf-8", NULL);
	if (uni || (!PyErr_ExceptionMatches(PyExc_UnicodeDecodeError)))
	{
		PyMem_Free(res);
		return uni;
	}
	PyErr_Clear();
	if (PyErr_Warn(PyExc_UserWarning, "malformed utf-8") < 0)
	{
		PyMem_Free(res);
		return NULL;
	}
	uni = PyUnicode_Decode(res, out-res, "latin-1", NULL);
	PyMem_Free(res);
	return uni;
}

int appendempty(PyObject *newpath, int *pos)
{
	PyObject *newsegment = PyUnicode_FromString("");
	if (!newsegment)
	{
		Py_DECREF(newpath);
		return 0;
	}
	PyTuple_SET_ITEM(newpath, (*pos)++, newsegment);
	return -1;
}

static char normalizepath__doc__[] =
"normalizepath(list) -> list\n\
\n\
Internal helper function for normalizing a path list";

/* the following function should be equivalent to RFC2396, Section 5.2 (6) (c)-(f)
 * with the exception of removing empty path_segments. The equivalent Python
 * code is:
	new_path_segments = []
	l = len(path_segments)
	for i in range(l):
		segment = path_segments[i]
		if segment=="." or segment=="":
			if i==l-1:
				new_path_segments.append("")
		elif segment==".." and len(new_path_segments) and new_path_segments[-1]!="..":
			new_path_segments.pop()
			if i==l-1:
				new_path_segments.append("")
		else:
			new_path_segments.append(segment)
	return new_path_segments
*/
static PyObject *normalizepath(PyObject *self, PyObject *path)
{
	PyObject *newpath;
	PyObject *newpathlist;
	int in;
	int out;
	int pathsize;

	if (!PyList_Check(path))
	{
		PyErr_SetString(PyExc_TypeError, "normalizepath argument must be list");
		return NULL;
	}

	pathsize = PyList_GET_SIZE(path);
	newpath = PyTuple_New(pathsize);

	if (!path)
		return NULL;

	out = 0;
	for (in = 0; in < pathsize; ++in)
	{
		PyObject *segment = PyList_GET_ITEM(path, in);
		int seglen;

		if (!PyUnicode_CheckExact(segment))
		{
			PyErr_SetString(PyExc_TypeError, "path entry directory must be unicode");
			Py_DECREF(newpath);
			return NULL;
		}
		seglen = PyUnicode_GET_SIZE(segment);
		if ((seglen==0) || ((seglen==1) && (PyUnicode_AS_UNICODE(segment)[0] == '.'))) /* skip '' and '.' */
		{
			if (in==pathsize-1) /* add empty terminating segment */
				if (!appendempty(newpath, &out))
					return NULL;
			continue; /* skip output */
		}
		else if ((seglen == 2) && (PyUnicode_AS_UNICODE(segment)[0] == '.') && (PyUnicode_AS_UNICODE(segment)[1] == '.') && out) /* drop '..' and a previous real directory name */
		{
			PyObject *lastnewsegment = PyTuple_GET_ITEM(newpath, out-1);

			if (!((PyUnicode_GET_SIZE(lastnewsegment) == 2) && /* check that previous name is not '..' */
					(PyUnicode_AS_UNICODE(lastnewsegment)[0] == '.') &&
					(PyUnicode_AS_UNICODE(lastnewsegment)[1] == '.')))
			{
				Py_DECREF(lastnewsegment);
				PyTuple_SET_ITEM(newpath, --out, NULL); /* drop previous */
				if (in==pathsize-1) /* add empty terminating segment */
					if (!appendempty(newpath, &out))
						return NULL;
				continue; /* skip output */
			}
		}
		PyTuple_SET_ITEM(newpath, out++, segment); /* append segment to output */
		Py_INCREF(segment);
	}
	/* Convert the result into a list */
	newpathlist = PyList_New(out);
	if (!newpathlist)
	{
		Py_DECREF(newpath);
		return NULL;
	}
	for (in = 0; in<out; ++in)
	{
		PyObject *segment = PyTuple_GET_ITEM(newpath, in);
		PyTuple_SET_ITEM(newpath, in, NULL); /* remove reference, because we copy the reference over to the result list, and drop the tuple afterwards */
		PyList_SET_ITEM(newpathlist, in, segment);
	}
	Py_DECREF(newpath);
	return newpathlist;
}

/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"escape", escape, METH_VARARGS, escape__doc__},
	{"unescape", unescape, METH_VARARGS, unescape__doc__},
	{"normalizepath", normalizepath, METH_O, normalizepath__doc__},
	{NULL, NULL}
};

static struct PyModuleDef _urlmodule = {
	PyModuleDef_HEAD_INIT,
	"_url",
	0, /* module doc */
	-1,
	_functions,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC
PyInit__url(void)
{
	return PyModule_Create(&_urlmodule);
}
