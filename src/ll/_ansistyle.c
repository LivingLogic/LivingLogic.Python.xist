/*
** Copyright 1999-2016 by LivingLogic AG, Bayreuth, Germany.
** Copyright 1999-2016 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/

#include "Python.h"


/* switches from fromcolor to tocolor. If tocolor is different from the fromcolor (and not -1),
the appropriate ANSI escape sequence will be returned. */
static PyObject *_switchcolor(PyObject *self, PyObject *args)
{
	int fromcolor;
	int tocolor;

	if (!PyArg_ParseTuple(args, "ii:switchcolor", &fromcolor, &tocolor))
		return (NULL);

	if ((tocolor != -1) && (fromcolor != tocolor))
	{
		char buffer[15];
		char *p = buffer;
		int first = 1;

		if (fromcolor == -1)
			fromcolor = 0070;

		*p++ = '\033';
		*p++ = '[';
		if ((!(tocolor&0700) && (fromcolor&0700)) /* do we have to get rid of the bold/underline/blink bit? (can only be done by a reset) */
			|| (tocolor==0070)) /* use reset when our target color is the default color (this is shorter than 40;37) */
		{
			*p++ = '0';
			fromcolor = 0070;
			first = 0;
		}
		/* now we know that old and new color have the same boldness, or the new color is bold and the old isn't, i.e. we only might have to switch bold on, not off */
		if ((tocolor&0100) && !(fromcolor&0100))
		{
			if (!first)
				*p++ = ';';
			else
				first = 0;
			*p++ = '1';
		}
		/* Fix underline */
		if ((tocolor&0200) && !(fromcolor&0200))
		{
			if (!first)
				*p++ = ';';
			else
				first = 0;
			*p++ = '4';
		}
		/* Fix blink */
		if ((tocolor&0400) && !(fromcolor&0400))
		{
			if (!first)
				*p++ = ';';
			else
				first = 0;
			*p++ = '5';
		}
		/* Fix foreground color */
		if ((tocolor&0070) != (fromcolor&0070))
		{
			if (!first)
				*p++ = ';';
			else
				first = 0;
			*p++ = '3';
			*p++ = '0' + ((tocolor & 0070) >> 3);
		}
		/* Finally fix the background color */
		if ((tocolor&0007) != (fromcolor&0007))
		{
			if (!first)
				*p++ = ';';
			*p++ = '4';
			*p++ = '0' + (tocolor & 0007);
		}

		*p++ = 'm';

		return PyUnicode_FromStringAndSize(buffer, p-buffer);
	}
	return PyUnicode_FromStringAndSize(NULL, 0);
}


/* ==================================================================== */
/* python module interface */


static PyMethodDef _functions[] =
{
	{"switchcolor", _switchcolor, METH_VARARGS, NULL},
	{NULL, NULL}
};

static char module__doc__[] =
"This module contains the function switchcolor().";

static struct PyModuleDef _ansistylemodule = {
    PyModuleDef_HEAD_INIT,
    "_ansistyle",
    module__doc__, /* module doc */
    -1,
    _functions,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit__ansistyle(void)
{
    return PyModule_Create(&_ansistylemodule);
}
