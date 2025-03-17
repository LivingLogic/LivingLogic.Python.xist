/*
** Copyright 2007-2025 by LivingLogic AG, Bayreuth/Germany
** Copyright 2007-2025 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/

#ifdef STRINGLIB_FIXENCODING

#define COPYCHARS(kind) \
	/* Copy characters before the encoding name */ \
	for (; inpos < oldencodingstart-str; ++inpos, ++outpos) \
		PyUnicode_WRITE(kind, newdata, outpos, PyUnicode_READ(STRINGLIB_KIND_XML, str, inpos)); \
	/* Copy new encoding name */ \
	for (Py_ssize_t newencpos = 0; newencpos < newencodinglen; ++newencpos, ++outpos) \
		PyUnicode_WRITE(kind, newdata, outpos, PyUnicode_READ(STRINGLIB_KIND_ENC, newencodingstart, newencpos)); \
	inpos += oldencodingend-oldencodingstart; \
	/* Copy characters after the encoding name */ \
	for (; inpos < len; ++inpos, ++outpos) \
		PyUnicode_WRITE(kind, newdata, outpos, PyUnicode_READ(STRINGLIB_KIND_XML, str, inpos));

static PyObject *STRINGLIB_FIXENCODING(PyObject *strobj, PyObject *newencodingobj, int final)
{
	const STRINGLIB_CHAR_XML *str = PyUnicode_DATA(strobj);
	Py_ssize_t len = PyUnicode_GET_LENGTH(strobj);
	const STRINGLIB_CHAR_ENC *newencodingstart = PyUnicode_DATA(newencodingobj);
	Py_ssize_t newencodinglen = PyUnicode_GET_LENGTH(newencodingobj);

	const STRINGLIB_CHAR_XML *oldencodingstart = NULL;
	const STRINGLIB_CHAR_XML *oldencodingend = NULL;
	switch (STRINGLIB_PARSEDECLARATION(str, str + len, &oldencodingstart, &oldencodingend))
	{
		case -1:
			return NULL;
		case 0: /* don't know yet */
			if (final) /* we won't get better data, so use what we have */
				goto original;
			Py_RETURN_NONE;
		case 1: /* not found => return original string */
			goto original;
		case 2: /* found it */
		{
			/* Find maximum character in the XML string (ignoring the old encoding name) */
			Py_UCS4 strmax = 0;
			Py_ssize_t inpos = 0;
			for (; inpos < oldencodingstart-str; ++inpos)
			{
				Py_UCS4 c = PyUnicode_READ(STRINGLIB_KIND_XML, str, inpos);
				if (c > strmax)
					strmax = c;
			}
			for (inpos += oldencodingend-oldencodingstart; inpos < len; ++inpos)
			{
				Py_UCS4 c = PyUnicode_READ(STRINGLIB_KIND_XML, str, inpos);
				if (c > strmax)
					strmax = c;
			}

			Py_UCS4 encmax = PyUnicode_MAX_CHAR_VALUE(newencodingobj);

			/* put the encoding name into this spot and return the new string */
			Py_ssize_t newsize = len + newencodinglen - (oldencodingend - oldencodingstart);
			PyObject *newobj = PyUnicode_New(newsize, Py_MAX(strmax, encmax));
			int kind = PyUnicode_KIND(newobj);
			if (!newobj)
				return NULL;
			void *newdata = PyUnicode_DATA(newobj);
			inpos = 0;
			Py_ssize_t outpos = 0;
			switch (kind)
			{
				case PyUnicode_4BYTE_KIND:
					COPYCHARS(PyUnicode_4BYTE_KIND);
					break;
				case PyUnicode_2BYTE_KIND:
					COPYCHARS(PyUnicode_2BYTE_KIND);
					break;
				case PyUnicode_1BYTE_KIND:
					COPYCHARS(PyUnicode_1BYTE_KIND);
					break;
			}
			return newobj;
		}
	}
	Py_RETURN_NONE;
	original:
	Py_INCREF(strobj);
	return strobj;
}

#endif