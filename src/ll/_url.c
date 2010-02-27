/*
** Copyright 2002-2010 by LivingLogic AG, Bayreuth, Germany.
** Copyright 2002-2010 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/__init__.py for the license
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
	char *r;
	char *startr;
	char *endr;
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

	starts = PyString_AS_STRING(str);
	ends = starts + PyString_GET_SIZE(str);

	for (newsize = 0, s = starts; s < ends; ++s)
	{
		if (safe ? (strchr(safe, *s)!=NULL) : (*s<0x80))
			++newsize;
		else
			newsize += 3;
	}

	res = PyString_FromStringAndSize(NULL, newsize);
	if (res)
	{
		startr = PyString_AS_STRING(res);
		endr = startr + PyString_GET_SIZE(res);

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

static void widechar_to_utf8(unsigned long widechar, char **out)
{
	unsigned long first_bits = 0;
	int trail = 0;

	if (widechar >= 0x80)
	{
		if (widechar < 0x00000800)
		{
			first_bits = 0xc0;
			trail = 1;
		}
		else if (widechar < 0x00010000)
		{
			first_bits = 0xe0;
			trail = 2;
		}
	}

	{
		int i;
		for (i = trail; i; --i)
		{
			(*out)[i] = (char)((widechar & 0x3f) | 0x80);
			widechar >>= 6;
		}
		(*out)[0] = (char) (widechar | first_bits);
	}

	*out += trail + 1;
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
			if (pos+3>len || (in[pos+1] == 'u' && pos+6>len))
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
			else if (in[pos+1] == 'u')
			{
				if ((!isxdigit(in[pos+2])) || (!isxdigit(in[pos+3])) ||
				    (!isxdigit(in[pos+4])) || (!isxdigit(in[pos+5])))
				{
					int k;
					sprintf(buffer, "malformed escape at position %d", pos);
					if (PyErr_Warn(PyExc_UserWarning, buffer) < 0)
					{
						PyMem_Free(res);
						return NULL;
					}

					for (k = 0; k < 6; ++k)
						*out++ = in[pos + k];
				}
				else
				{
					int k;
					for (k = 0; k < 4; ++k)
						buffer[k] = in[pos + k + 2];

					buffer[4] = '\0';

					widechar_to_utf8(strtol(buffer, NULL, 16), &out);
				}
				pos += 6;
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
	PyObject *newsegment = Py_BuildValue("(u#)", pos, 0); /* pos is ignored */
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
	for i in xrange(l):
		segment = path_segments[i]
		if segment==(".",) or segment==("",):
			if i==l-1:
				new_path_segments.append(("",))
		elif segment==("..",) and len(new_path_segments) and new_path_segments[-1]!=("..",):
			new_path_segments.pop()
			if i==l-1:
				new_path_segments.append(("",))
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
		PyObject *dir;
		int segmentsize;

		if (!PyTuple_CheckExact(segment) || (((segmentsize = PyTuple_GET_SIZE(segment)) != 1) && (segmentsize != 2)))
		{
			PyErr_SetString(PyExc_TypeError, "path entries must be tuples with 1 or 2 entries");
			Py_DECREF(newpath);
			return NULL;
		}
		dir = PyTuple_GET_ITEM(segment, 0);
		if (!PyUnicode_CheckExact(dir))
		{
			PyErr_SetString(PyExc_TypeError, "path entry directory must be unicode");
			Py_DECREF(newpath);
			return NULL;
		}
		if (segmentsize == 1) /* we can only optimize it, if it doesn't have params */
		{
			int dirlen = PyUnicode_GET_SIZE(dir);
			if ((dirlen==0) || ((dirlen==1) && (PyUnicode_AS_UNICODE(dir)[0] == '.'))) /* skip '' and '.' */
			{
				if (in==pathsize-1) /* add empty terminating segment */
					if (!appendempty(newpath, &out))
						return NULL;
				continue; /* skip output */
			}
			else if ((dirlen == 2) && (PyUnicode_AS_UNICODE(dir)[0] == '.') && (PyUnicode_AS_UNICODE(dir)[1] == '.') && out) /* drop '..' and a previous real directory name */
			{
				PyObject *lastnewsegment = PyTuple_GET_ITEM(newpath, out-1);
				int lastnewsegmentsize = PyTuple_GET_SIZE(lastnewsegment);
				PyObject *lastnewsegmentdir = PyTuple_GET_ITEM(lastnewsegment, 0);

				if (!((lastnewsegmentsize==1) && /* check that previous name is not '..' */
						(PyUnicode_GET_SIZE(lastnewsegmentdir) == 2) &&
						(PyUnicode_AS_UNICODE(lastnewsegmentdir)[0] == '.') &&
						(PyUnicode_AS_UNICODE(lastnewsegmentdir)[1] == '.')))
				{
					Py_DECREF(lastnewsegment);
					PyTuple_SET_ITEM(newpath, --out, NULL); /* drop previous */
					if (in==pathsize-1) /* add empty terminating segment */
						if (!appendempty(newpath, &out))
							return NULL;
					continue; /* skip output */
				}
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

void
#ifdef WIN32
__declspec(dllexport)
#endif
init_url(void)
{
	Py_InitModule("_url", _functions);
}
