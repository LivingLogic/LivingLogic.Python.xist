/*
** Copyright 1999-2014 by LivingLogic AG, Bayreuth, Germany.
** Copyright 1999-2014 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/


#ifdef STRINGLIB_NAME
static PyObject *STRINGLIB_NAME(PyObject *str, int doquot, int doapos)
{
	Py_ssize_t oldsize;
	void *olddata;
	int maxchar = 127;
	Py_ssize_t i;
	Py_ssize_t newsize = 0;
	void *newdata;

	STRINGLIB_INTRO

	oldsize = STRINGLIB_LEN(str);
	olddata = STRINGLIB_STR(str);
	for (i = 0; i < oldsize; ++i)
	{
		STRINGLIB_CHAR ch = STRINGLIB_GET(olddata, i);
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
		PyObject *result = STRINGLIB_NEW(newsize, maxchar);
		newdata = STRINGLIB_STR(result);
		int index = 0;
		if (result == NULL)
			return NULL;
		for (i = 0; i < oldsize; ++i)
		{
			STRINGLIB_CHAR ch = STRINGLIB_GET(olddata, i);
			if (ch == (STRINGLIB_CHAR)'<')
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, 'l');
				STRINGLIB_SET(newdata, index++, 't');
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if (ch == (STRINGLIB_CHAR)'>')
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, 'g');
				STRINGLIB_SET(newdata, index++, 't');
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if (ch == (STRINGLIB_CHAR)'&')
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, 'a');
				STRINGLIB_SET(newdata, index++, 'm');
				STRINGLIB_SET(newdata, index++, 'p');
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if ((ch == (STRINGLIB_CHAR)'"') && doquot)
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, 'q');
				STRINGLIB_SET(newdata, index++, 'u');
				STRINGLIB_SET(newdata, index++, 'o');
				STRINGLIB_SET(newdata, index++, 't');
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if ((ch == (STRINGLIB_CHAR)'\'') && doapos)
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, '#');
				STRINGLIB_SET(newdata, index++, '3');
				STRINGLIB_SET(newdata, index++, '9');
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if (ch <= 0x8)
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, '#');
				STRINGLIB_SET(newdata, index++, '0'+ch);
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if ((ch >= 0xB) && (ch <= 0x1F) && (ch != 0xD))
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, '#');
				STRINGLIB_SET(newdata, index++, '0'+ch/10);
				STRINGLIB_SET(newdata, index++, '0'+ch%10);
				STRINGLIB_SET(newdata, index++, ';');
			}
			else if ((ch >= 0x7F) && (ch <= 0x9F) && (ch != 0x85))
			{
				STRINGLIB_SET(newdata, index++, '&');
				STRINGLIB_SET(newdata, index++, '#');
				STRINGLIB_SET(newdata, index++, '0'+ch/100);
				STRINGLIB_SET(newdata, index++, '0'+(ch/10)%10);
				STRINGLIB_SET(newdata, index++, '0'+ch%10);
				STRINGLIB_SET(newdata, index++, ';');
			}
			else
				STRINGLIB_SET(newdata, index++, ch);
		}
		return result;
	}
}
#endif
