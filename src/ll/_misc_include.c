/*
** Copyright 1999-2010 by LivingLogic AG, Bayreuth, Germany.
** Copyright 1999-2010 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/__init__.py for the license
*/


#ifdef STRINGLIB_NAME
static PyObject *STRINGLIB_NAME(PyObject *str, int doquot, int doapos)
{
	Py_ssize_t i;
	Py_ssize_t oldsize;
	Py_ssize_t newsize = 0;

	oldsize = STRINGLIB_LEN(str);
	for (i = 0; i < oldsize; ++i)
	{
		STRINGLIB_CHAR ch = STRINGLIB_STR(str)[i];
		if (ch == ((STRINGLIB_CHAR)'<'))
			newsize += 4; /* &lt; */
		else if (ch == (STRINGLIB_CHAR)'>') /* Note that we always replace '>' with its entity, not just in case it is part of ']]>' */
			newsize += 4; /* &gt; */
		else if (ch == (STRINGLIB_CHAR)'&')
			newsize += 5; /* &amp; */
		else if ((ch == (STRINGLIB_CHAR)'"') && doquot)
			newsize += 6; /* &quot; */
		else if ((ch == (STRINGLIB_CHAR)'\'') && doapos)
			newsize += 5; /* &#39; */
		else if (ch <= 0x8)
			newsize += 4;
		else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			newsize += 5;
		else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			newsize += 6;
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
		PyObject *result = STRINGLIB_NEW(NULL, newsize);
		STRINGLIB_CHAR *p;
		if (result == NULL)
			return NULL;
		p = STRINGLIB_STR(result);
		for (i = 0; i < oldsize; ++i)
		{
			STRINGLIB_CHAR ch = STRINGLIB_STR(str)[i];
			if (ch == (STRINGLIB_CHAR)'<')
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'l';
				*p++ = (STRINGLIB_CHAR)'t';
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if (ch == (STRINGLIB_CHAR)'>')
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'g';
				*p++ = (STRINGLIB_CHAR)'t';
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if (ch == (STRINGLIB_CHAR)'&')
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'a';
				*p++ = (STRINGLIB_CHAR)'m';
				*p++ = (STRINGLIB_CHAR)'p';
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if ((ch == (STRINGLIB_CHAR)'"') && doquot)
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'q';
				*p++ = (STRINGLIB_CHAR)'u';
				*p++ = (STRINGLIB_CHAR)'o';
				*p++ = (STRINGLIB_CHAR)'t';
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if ((ch == (STRINGLIB_CHAR)'\'') && doapos)
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'#';
				*p++ = (STRINGLIB_CHAR)'3';
				*p++ = (STRINGLIB_CHAR)'9';
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if (ch <= 0x8)
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'#';
				*p++ = ((STRINGLIB_CHAR)'0')+ch;
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'#';
				*p++ = ((STRINGLIB_CHAR)'0')+ch/10;
				*p++ = ((STRINGLIB_CHAR)'0')+ch%10;
				*p++ = (STRINGLIB_CHAR)';';
			}
			else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			{
				*p++ = (STRINGLIB_CHAR)'&';
				*p++ = (STRINGLIB_CHAR)'#';
				*p++ = ((STRINGLIB_CHAR)'0')+ch/100;
				*p++ = ((STRINGLIB_CHAR)'0')+(ch/10)%10;
				*p++ = ((STRINGLIB_CHAR)'0')+ch%10;
				*p++ = (STRINGLIB_CHAR)';';
			}
			else
				*p++ = ch;
		}
		return result;
	}
}
#endif
