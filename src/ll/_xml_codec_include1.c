/*
** Copyright 2007-2025 by LivingLogic AG, Bayreuth/Germany
** Copyright 2007-2025 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/

#ifdef STRINGLIB_CHAR

#ifdef STRINGLIB_CMP2CHAR_DEFINED
static int STRINGLIB_CMP2CHAR(const STRINGLIB_CHAR *u, const char *s, Py_ssize_t len)
{
	while (len)
	{
		if (*u != *((const unsigned char *)s))
			return *u - *((const unsigned char *)s);
		++u;
		++s;
		--len;
	}
	return 0;
}
#endif

/* Parses a pseudoattr. Returns 2 if a name has been found, 1 if we're at the
   end of the declaration, 0 if we didn't have enough data and -1 on error.
   The pseudoattr name is put into `namestart` and `nameend`,
   The pseudoattr value is put into `valuestart` and `valueend`. */
static int STRINGLIB_PARSEPSEUDOATTR(const STRINGLIB_CHAR *s, const STRINGLIB_CHAR *end, const STRINGLIB_CHAR **namestart, const STRINGLIB_CHAR **nameend, const STRINGLIB_CHAR **valuestart, const STRINGLIB_CHAR **valueend)
{
	STRINGLIB_CHAR quote;

	/* goto beginning of next word */
	while (s<end && (*s == ' ' || *s == '\t' || *s == '\r' || *s == '\n'))
		++s;

	if (s == end) /* don't know yet */
		return 0;

	if (s+1<end)
	{
		/* we're at the end of the declaration => there's no pseudoattr there */
		if (s[0] == '?' && s[1] == '>')
			return 1;
	}

	*namestart = s;
	while (s<end && STRINGLIB_ISALPHA(*s))
		++s;
	if (s == end) /* don't know yet */
		return 0;
	*nameend = s;

	if (*namestart == *nameend)
	{
		PyErr_SetString(PyExc_ValueError, "malformed XML declaration: empty or malformed pseudoattr name");
		return -1;
	}

	while (s<end && (*s == ' ' || *s == '\t' || *s == '\r' || *s == '\n'))
		++s;

	if (s==end) /* don't know yet */
		return 0;

	if (*s++ != '=')
	{
		PyErr_SetString(PyExc_ValueError, "malformed XML declaration: expected '='");
		return -1;
	}

	while (s<end && (*s == ' ' || *s == '\t' || *s == '\r' || *s == '\n'))
		++s;
	if (s == end) /* don't know yet */
		return 0;

	quote = *s;

	if (quote != '"' && quote != '\'')
	{
		PyErr_SetString(PyExc_ValueError, "malformed XML declaration: expected quote");
		return -1;
	}

	*valuestart = ++s;
	while (s < end && *s != quote)
		++s;
	if (s == end) /* don't know yet */
		return 0;
	*valueend = s;

	if (*valuestart == *valueend)
	{
		PyErr_SetString(PyExc_ValueError, "malformed XML declaration: empty pseudoattr value");
		return -1;
	}

	return 2; /* found one */
}


/* finds the pseudo attribute `encoding` and returns the position in
   `encodingstart`/`encodingend`.
   Return values are the same as for `parsepseudoattr()`
*/
static int STRINGLIB_PARSEENCODING(const STRINGLIB_CHAR *str, const STRINGLIB_CHAR *strend, const STRINGLIB_CHAR **encodingstart, const STRINGLIB_CHAR **encodingend)
{
	while (1)
	{
		const STRINGLIB_CHAR *namestart;
		const STRINGLIB_CHAR *nameend;

		int result = STRINGLIB_PARSEPSEUDOATTR(str, strend, &namestart, &nameend, encodingstart, encodingend);

		switch (result)
		{
			default:
				return result;
			case 2: /* found one, now check if it's "encoding"  */
				if ((nameend-namestart == 8) && !STRINGLIB_CMP2CHAR(namestart, "encoding", 8))
					return 2;
				/* not "encoding" => continue */
				str = *encodingend+1;
		}
	}
}

/* Parses a unicode XML declaration and returns the position of the encoding in
   `encodingstart`/`encodingend`. Return values are the same as for `parseencoding()`. */
int STRINGLIB_PARSEDECLARATION(const STRINGLIB_CHAR *str, const STRINGLIB_CHAR *strend, const STRINGLIB_CHAR **encodingstart, const STRINGLIB_CHAR **encodingend)
{
	Py_ssize_t strlength = strend - str;

	if (strlength>0)
	{
		if (*str++ != '<')
			return 1;
		if (strlength>1)
		{
			if (*str++ != '?')
				return 1;
			if (strlength>2)
			{
				if (*str++ != 'x')
					return 1;
				if (strlength>3)
				{
					if (*str++ != 'm')
						return 1;
					if (strlength>4)
					{
						if (*str++ != 'l')
							return 1;
						if (strlength>5)
						{
							if (*str != ' ' && *str != '\t' && *str != '\r' && *str != '\n')
								return 1;
							return STRINGLIB_PARSEENCODING(++str, strend, encodingstart, encodingend);
						}
					}
				}
			}
		}
	}
	return 0;
}

static PyObject *STRINGLIB_DETECTENCODING(const STRINGLIB_CHAR *str, Py_ssize_t len, int final)
{
	const STRINGLIB_CHAR *encodingstart;
	const STRINGLIB_CHAR *encodingend;

	switch (STRINGLIB_PARSEDECLARATION(str, str+len, &encodingstart, &encodingend))
	{
		case -1:
			return NULL;
		case 0: /* don't know yet */
			if (final) /* we won't get better data, so default to utf-8 */
				goto utf8;
			Py_RETURN_NONE;
		case 1: /* not found => default to UTF-8 */
			goto utf8;
		case 2: /* found it => Return the encoding name we found */
			return PyUnicode_FromKindAndData(STRINGLIB_KIND, encodingstart, encodingend-encodingstart);
	}
	utf8:
	return PyUnicode_DecodeASCII("utf-8", 5, NULL);
}

#endif