/*
** Copyright 2007-2025 by LivingLogic AG, Bayreuth/Germany
** Copyright 2007-2025 by Walter Dörwald
**
** All Rights Reserved
**
** See ll/xist/__init__.py for the license
*/


#define PY_SSIZE_T_CLEAN
#include "Python.h"


/* define 4 byte version of parsepseudoattr/parseencoding */
#define STRINGLIB_PARSEPSEUDOATTR   parsepseudoattr_ucs4
#define STRINGLIB_PARSEENCODING     parseencoding_ucs4
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs4
#define STRINGLIB_DETECTENCODING    detectencoding_ucs4
#define STRINGLIB_CHAR              Py_UCS4
#define STRINGLIB_KIND              PyUnicode_4BYTE_KIND
#define STRINGLIB_ISALPHA(c)        Py_UNICODE_ISALPHA(c)
#define STRINGLIB_CMP2CHAR_DEFINED  1
#define STRINGLIB_CMP2CHAR(u, s, l) compare_ucs4_2_char(u, s, l)

#include "_xml_codec_include1.c"

#undef STRINGLIB_PARSEPSEUDOATTR
#undef STRINGLIB_PARSEENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_DETECTENCODING
#undef STRINGLIB_CHAR
#undef STRINGLIB_KIND
#undef STRINGLIB_ISALPHA
#undef STRINGLIB_CMP2CHAR_DEFINED
#undef STRINGLIB_CMP2CHAR

/* define 2 byte version of parsepseudoattr/parseencoding */
#define STRINGLIB_PARSEPSEUDOATTR   parsepseudoattr_ucs2
#define STRINGLIB_PARSEENCODING     parseencoding_ucs2
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs2
#define STRINGLIB_DETECTENCODING    detectencoding_ucs2
#define STRINGLIB_CHAR              Py_UCS2
#define STRINGLIB_KIND              PyUnicode_2BYTE_KIND
#define STRINGLIB_ISALPHA(c)        Py_UNICODE_ISALPHA(c)
#define STRINGLIB_CMP2CHAR_DEFINED  1
#define STRINGLIB_CMP2CHAR(u, s, l) compare_ucs2_2_char(u, s, l)

#include "_xml_codec_include1.c"

#undef STRINGLIB_PARSEPSEUDOATTR
#undef STRINGLIB_PARSEENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_DETECTENCODING
#undef STRINGLIB_CHAR
#undef STRINGLIB_KIND
#undef STRINGLIB_ISALPHA
#undef STRINGLIB_CMP2CHAR_DEFINED
#undef STRINGLIB_CMP2CHAR


/* define 2 byte version of parsepseudoattr/parseencoding */
#define STRINGLIB_PARSEPSEUDOATTR   parsepseudoattr_ucs1
#define STRINGLIB_PARSEENCODING     parseencoding_ucs1
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs1
#define STRINGLIB_DETECTENCODING    detectencoding_ucs1
#define STRINGLIB_CHAR              char
#define STRINGLIB_KIND              PyUnicode_1BYTE_KIND
#define STRINGLIB_ISALPHA(c)        (((c)>='a' && (c)<='z') || ((c)>='A' && (c)<='Z'))
#define STRINGLIB_CMP2CHAR(u, s, l) strncmp(u, s, l)

#include "_xml_codec_include1.c"

#undef STRINGLIB_PARSEPSEUDOATTR
#undef STRINGLIB_PARSEENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_DETECTENCODING
#undef STRINGLIB_CHAR
#undef STRINGLIB_KIND
#undef STRINGLIB_ISALPHA
#undef STRINGLIB_CMP2CHAR

/* define various versions of fixencoding (with 1/2/4 bytes for the XML string and 1/2/4 bytes for the new encoding name) */
#define STRINGLIB_FIXENCODING       fixencoding_ucs4_ucs4
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs4
#define STRINGLIB_CHAR_XML          Py_UCS4
#define STRINGLIB_KIND_XML          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS4
#define STRINGLIB_KIND_ENC          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS4
#define STRINGLIB_KIND_RES          PyUnicode_4BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs4_ucs2
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs4
#define STRINGLIB_CHAR_XML          Py_UCS4
#define STRINGLIB_KIND_XML          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS2
#define STRINGLIB_KIND_ENC          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS4
#define STRINGLIB_KIND_RES          PyUnicode_4BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs4_ucs1
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs4
#define STRINGLIB_CHAR_XML          Py_UCS4
#define STRINGLIB_KIND_XML          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS1
#define STRINGLIB_KIND_ENC          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS4
#define STRINGLIB_KIND_RES          PyUnicode_4BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs2_ucs4
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs2
#define STRINGLIB_CHAR_XML          Py_UCS2
#define STRINGLIB_KIND_XML          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS4
#define STRINGLIB_KIND_ENC          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS4
#define STRINGLIB_KIND_RES          PyUnicode_4BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs2_ucs2
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs2
#define STRINGLIB_CHAR_XML          Py_UCS2
#define STRINGLIB_KIND_XML          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS2
#define STRINGLIB_KIND_ENC          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS2
#define STRINGLIB_KIND_RES          PyUnicode_2BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs2_ucs1
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs2
#define STRINGLIB_CHAR_XML          Py_UCS2
#define STRINGLIB_KIND_XML          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_ENC          char
#define STRINGLIB_KIND_ENC          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS2
#define STRINGLIB_KIND_RES          PyUnicode_2BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs1_ucs4
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs1
#define STRINGLIB_CHAR_XML          char
#define STRINGLIB_KIND_XML          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS4
#define STRINGLIB_KIND_ENC          PyUnicode_4BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS4
#define STRINGLIB_KIND_RES          PyUnicode_4BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs1_ucs2
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs1
#define STRINGLIB_CHAR_XML          char
#define STRINGLIB_KIND_XML          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_ENC          Py_UCS2
#define STRINGLIB_KIND_ENC          PyUnicode_2BYTE_KIND
#define STRINGLIB_CHAR_RES          Py_UCS2
#define STRINGLIB_KIND_RES          PyUnicode_2BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

#define STRINGLIB_FIXENCODING       fixencoding_ucs1_ucs1
#define STRINGLIB_PARSEDECLARATION  parsedeclaration_ucs1
#define STRINGLIB_CHAR_XML          char
#define STRINGLIB_KIND_XML          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_ENC          char
#define STRINGLIB_KIND_ENC          PyUnicode_1BYTE_KIND
#define STRINGLIB_CHAR_RES          char
#define STRINGLIB_KIND_RES          PyUnicode_1BYTE_KIND

#include "_xml_codec_include2.c"

#undef STRINGLIB_FIXENCODING
#undef STRINGLIB_PARSEDECLARATION
#undef STRINGLIB_CHAR_XML
#undef STRINGLIB_KIND_XML
#undef STRINGLIB_CHAR_ENC
#undef STRINGLIB_KIND_ENC
#undef STRINGLIB_CHAR_RES
#undef STRINGLIB_KIND_RES

/* We're using bits to store all possible candidate encodings (or variants, i.e.
 * we have two bits for the variants of UTF-16 and two for the
 * variants of UTF-32).
 *
 * Prefixes for various XML encodings
 * (see http://www.w3.org/TR/2004/REC-xml-20040204/#sec-guessing)
 * UTF-8-SIG   xEF  xBB  xBF
 * UTF-16 (LE) xFF  xFE ~x00|~x00
 * UTF-16 (BE) xFE  xFF
 * UTF-16-LE    <   x00   ?   x00
 * UTF-16-BE   x00   <
 * UTF-32 (LE) xFF  xFE  x00  x00
 * UTF-32 (BE) x00  x00  xFE  xFF
 * UTF-32-LE    <   x00  x00  x00
 * UTF-32-BE   x00  x00  x00   <
 * XML-DECL     <    ?    x    m    l
*/

#define CANDIDATE_UTF_8_SIG    (1<<0)
#define CANDIDATE_UTF_16_AS_LE (1<<1)
#define CANDIDATE_UTF_16_AS_BE (1<<2)
#define CANDIDATE_UTF_16_LE    (1<<3)
#define CANDIDATE_UTF_16_BE    (1<<4)
#define CANDIDATE_UTF_32_AS_LE (1<<5)
#define CANDIDATE_UTF_32_AS_BE (1<<6)
#define CANDIDATE_UTF_32_LE    (1<<7)
#define CANDIDATE_UTF_32_BE    (1<<8)
#define CANDIDATE_EBCDIC       (1<<9)
#define CANDIDATE_DECL         (1<<10)
#define CANDIDATES             ((CANDIDATE_DECL<<1)-1) /* All bits */


#if 0
/* for debugging output */
void DUMPCANDIDATES(int candidates)
{
	if (candidates&CANDIDATE_UTF_8_SIG)
		printf("u8s ");
	else
		printf("--- ");
	if (candidates&CANDIDATE_UTF_16_AS_LE)
		printf("u16(le) ");
	else
		printf("------- ");
	if (candidates&CANDIDATE_UTF_16_AS_BE)
		printf("u16(be) ");
	else
		printf("------- ");
	if (candidates&CANDIDATE_UTF_16_LE)
		printf("u16le ");
	else
		printf("----- ");
	if (candidates&CANDIDATE_UTF_16_BE)
		printf("u16be ");
	else
		printf("----- ");
	if (candidates&CANDIDATE_UTF_32_AS_LE)
		printf("u32(le) ");
	else
		printf("------- ");
	if (candidates&CANDIDATE_UTF_32_AS_BE)
		printf("u32(be) ");
	else
		printf("------- ");
	if (candidates&CANDIDATE_UTF_32_LE)
		printf("u32le ");
	else
		printf("----- ");
	if (candidates&CANDIDATE_UTF_32_BE)
		printf("u32be ");
	else
		printf("----- ");
	if (candidates&CANDIDATE_EBCDIC)
		printf("ebcdic ");
	else
		printf("------ ");
	if (candidates&CANDIDATE_DECL)
		printf("decl\n");
	else
		printf("----\n");
}

/* for debugging output */
void DUMPBYTE(char c)
{
	printf("-> %02x\n", (int)(unsigned char)c);
}
#else
#define DUMPCANDIDATES(x)
#define DUMPBYTE(x)
#endif


static PyObject *detectencoding_bytes(const char *str, Py_ssize_t len, int final)
{
	const char *origstr;
	Py_ssize_t origlen;
	int candidates = CANDIDATES; /* all 10 encodings are still possible */
	const char *strend;
	char firstbytes[4];

	origlen = len;
	origstr = str;
	strend = str + len;

	/* For each byte in the input delete the appropriate bit if the
	 * encoding has the wrong value in this spot. If no bits remain
	 * we default to UTF-8. If only one bit remains (and we had enough input)
	 * this is the resulting encoding.
	 */
	DUMPCANDIDATES(candidates);
	if (len)
	{
		/* Check first byte */
		firstbytes[0] = *str;
		DUMPBYTE(*str);
		if (firstbytes[0] != '\xef')
			candidates &= ~CANDIDATE_UTF_8_SIG;
		if (firstbytes[0] != '\xff')
			candidates &= ~CANDIDATE_UTF_32_AS_LE&
			              ~CANDIDATE_UTF_16_AS_LE;
		if (firstbytes[0] != '\xfe')
			candidates &= ~CANDIDATE_UTF_16_AS_BE;
		if (firstbytes[0] != '<')
			candidates &= ~CANDIDATE_UTF_32_LE&
			              ~CANDIDATE_UTF_16_LE&
			              ~CANDIDATE_DECL;
		if (firstbytes[0] != '\x00')
			candidates &= ~CANDIDATE_UTF_32_AS_BE&
			              ~CANDIDATE_UTF_32_BE&
			              ~CANDIDATE_UTF_16_BE;
		if (firstbytes[0] != '\x4c')
			candidates &= ~CANDIDATE_EBCDIC;
		DUMPCANDIDATES(candidates);
		if (++str, --len)
		{
			/* Check second byte */
			firstbytes[1] = *str;
			DUMPBYTE(*str);
			if (firstbytes[1] != '\xbb')
				candidates &= ~CANDIDATE_UTF_8_SIG;
			if (firstbytes[1] != '\xfe')
				candidates &= ~CANDIDATE_UTF_16_AS_LE&
				              ~CANDIDATE_UTF_32_AS_LE;
			if (firstbytes[1] != '\xff')
				candidates &= ~CANDIDATE_UTF_16_AS_BE;
			if (firstbytes[1] != '\x00')
				candidates &= ~CANDIDATE_UTF_16_LE&
				              ~CANDIDATE_UTF_32_AS_BE&
				              ~CANDIDATE_UTF_32_LE&
				              ~CANDIDATE_UTF_32_BE;
			if (firstbytes[1] != '<')
				candidates &= ~CANDIDATE_UTF_16_BE;
			if (firstbytes[1] != '\x6F')
				candidates &= ~CANDIDATE_EBCDIC;
			if (firstbytes[1] != '?')
				candidates &= ~CANDIDATE_DECL;
			DUMPCANDIDATES(candidates);
			if (++str, --len)
			{
				/* Check third byte */
				firstbytes[2] = *str;
				DUMPBYTE(*str);
				if (firstbytes[2] != '\xbf')
					candidates &= ~CANDIDATE_UTF_8_SIG;
				if (firstbytes[2] != '?')
					candidates &= ~CANDIDATE_UTF_16_LE;
				if (firstbytes[2] != '\x00')
					candidates &= ~CANDIDATE_UTF_32_AS_LE&
					              ~CANDIDATE_UTF_32_LE&
					              ~CANDIDATE_UTF_32_BE;
				if (firstbytes[2] != '\xfe')
					candidates &= ~CANDIDATE_UTF_32_AS_BE;
				if (firstbytes[2] != '\xA7')
					candidates &= ~CANDIDATE_EBCDIC;
				if (firstbytes[2] != 'x')
					candidates &= ~CANDIDATE_DECL;
				DUMPCANDIDATES(candidates);
				if (++str, --len)
				{
					/* Check fourth byte */
					firstbytes[3] = *str;
					DUMPBYTE(*str);
					if (firstbytes[3] == '\x00' && firstbytes[2] == '\x00')
						candidates &= ~CANDIDATE_UTF_16_AS_LE;
					if (firstbytes[3] != '\x00')
						candidates &= ~CANDIDATE_UTF_16_LE&
						              ~CANDIDATE_UTF_32_AS_LE&
						              ~CANDIDATE_UTF_32_LE;
					if (firstbytes[3] != '\xff')
						candidates &= ~CANDIDATE_UTF_32_AS_BE;
					if (firstbytes[3] != '<')
						candidates &= ~CANDIDATE_UTF_32_BE;
					if (firstbytes[3] != '\x94')
						candidates &= ~CANDIDATE_EBCDIC;
					if (firstbytes[3] != 'm')
						candidates &= ~CANDIDATE_DECL;
					DUMPCANDIDATES(candidates);
					if (++str, --len)
					{
						/* Check fifth byte */
						DUMPBYTE(*str);
						if (*str != 'l')
							candidates &= ~CANDIDATE_DECL;
						DUMPCANDIDATES(candidates);
						if (++str, --len)
						{
							/* Check sixth byte */
							DUMPBYTE(*str);
							if (*str != ' ' && *str != '\t' && *str != '\r' && *str != '\n')
								candidates &= ~CANDIDATE_DECL;
							DUMPCANDIDATES(candidates);
						}
					}
				}
			}
		}
	}
	if (candidates == 0)
		return PyUnicode_FromString("utf-8");
	else if (!(candidates & (candidates-1))) /* only one encoding remaining */
	{
		if ((candidates == CANDIDATE_UTF_8_SIG) && (origlen >= 3))
			return PyUnicode_FromString("utf-8-sig");
		else if ((candidates == CANDIDATE_UTF_16_AS_LE) && (origlen >= 2))
			return PyUnicode_FromString("utf-16");
		else if ((candidates == CANDIDATE_UTF_16_AS_BE) && (origlen >= 2))
			return PyUnicode_FromString("utf-16");
		else if ((candidates == CANDIDATE_UTF_16_LE) && (origlen >= 4))
			return PyUnicode_FromString("utf-16-le");
		else if ((candidates == CANDIDATE_UTF_16_BE) && (origlen >= 2))
			return PyUnicode_FromString("utf-16-be");
		else if ((candidates == CANDIDATE_UTF_32_AS_LE) && (origlen >= 4))
			return PyUnicode_FromString("utf-32");
		else if ((candidates == CANDIDATE_UTF_32_AS_BE) && (origlen >= 4))
			return PyUnicode_FromString("utf-32");
		else if ((candidates == CANDIDATE_UTF_32_LE) && (origlen >= 4))
			return PyUnicode_FromString("utf-32-le");
		else if ((candidates == CANDIDATE_UTF_32_BE) && (origlen >= 4))
			return PyUnicode_FromString("utf-32-be");
		else if ((candidates == CANDIDATE_EBCDIC) && (origlen >= 4))
			return PyUnicode_FromString("cp037");
		else if ((candidates == CANDIDATE_DECL) && (origlen >= 6))
		{
			const char *encodingstart;
			const char *encodingend;

			switch (parseencoding_ucs1(str, strend, &encodingstart, &encodingend))
			{
				case -1:
					return NULL;
				case 0: /* don't know yet */
					Py_RETURN_NONE;
				case 1: /* not found => default to utf-8 */
					return PyUnicode_FromString("utf-8");
				case 2: /* found it  */
					return PyUnicode_FromStringAndSize(encodingstart, encodingend-encodingstart);
			}
		}
	}
	if (final) /* if this is the last call, and we haven't determined an encoding yet, we default to UTF-8 */
		return PyUnicode_FromString("utf-8");
	/* We don't know yet */
	Py_RETURN_NONE;
}


static PyObject *detectencoding(PyObject *self, PyObject *args)
{
	PyObject *obj;
	Py_buffer buf;
	int final = 0;

	if (!PyArg_ParseTuple(args, "O|i:detectencoding", &obj, &final))
		return NULL;

	if (PyUnicode_Check(obj))
	{
		int kind = PyUnicode_KIND(obj);
		switch (kind)
		{
			case PyUnicode_1BYTE_KIND:
				return detectencoding_ucs1(PyUnicode_DATA(obj), PyUnicode_GET_LENGTH(obj), final);
			case PyUnicode_2BYTE_KIND:
				return detectencoding_ucs2(PyUnicode_DATA(obj), PyUnicode_GET_LENGTH(obj), final);
			case PyUnicode_4BYTE_KIND:
				return detectencoding_ucs4(PyUnicode_DATA(obj), PyUnicode_GET_LENGTH(obj), final);
			default:
				PyErr_SetString(PyExc_ValueError, "Unknown unicode format");
				return NULL;
		}
	}
	else if (!PyObject_GetBuffer(obj, &buf, PyBUF_CONTIG_RO))
		return detectencoding_bytes(buf.buf, buf.len, final);
	return NULL;
}


static char detectencoding__doc__[] = PyDoc_STR(
	"detectencoding(str[, final=False]) -> str or None\n\
	\n\
	Tries to detect the XML encoding from the first few bytes of the string\n\
	or the encoding declaration in the XML header. Return the name of the\n\
	encoding or None, if the encoding is ambiguous."
);


PyObject *fixencoding(PyObject *self, PyObject *args)
{
	PyObject *strobj;
	PyObject *newencodingobj;
	int final = 0;

	if (!PyArg_ParseTuple(args, "O!O!|i:fixencoding", &PyUnicode_Type, &strobj, &PyUnicode_Type, &newencodingobj, &final))
		return NULL;

	int kind_xml = PyUnicode_KIND(strobj);
	int kind_enc = PyUnicode_KIND(newencodingobj);

	switch (kind_xml)
	{
		case PyUnicode_4BYTE_KIND:
			switch (kind_enc)
			{
				case PyUnicode_4BYTE_KIND:
					return fixencoding_ucs4_ucs4(strobj, newencodingobj, final);
				case PyUnicode_2BYTE_KIND:
					return fixencoding_ucs4_ucs2(strobj, newencodingobj, final);
				case PyUnicode_1BYTE_KIND:
					return fixencoding_ucs4_ucs1(strobj, newencodingobj, final);
				default:
					goto error;
			}
		case PyUnicode_2BYTE_KIND:
			switch (kind_enc)
			{
				case PyUnicode_4BYTE_KIND:
					return fixencoding_ucs2_ucs4(strobj, newencodingobj, final);
				case PyUnicode_2BYTE_KIND:
					return fixencoding_ucs2_ucs2(strobj, newencodingobj, final);
				case PyUnicode_1BYTE_KIND:
					return fixencoding_ucs2_ucs1(strobj, newencodingobj, final);
				default:
					goto error;
			}
		case PyUnicode_1BYTE_KIND:
			switch (kind_enc)
			{
				case PyUnicode_4BYTE_KIND:
					return fixencoding_ucs1_ucs4(strobj, newencodingobj, final);
				case PyUnicode_2BYTE_KIND:
					return fixencoding_ucs1_ucs2(strobj, newencodingobj, final);
				case PyUnicode_1BYTE_KIND:
					return fixencoding_ucs1_ucs1(strobj, newencodingobj, final);
				default:
					goto error;
			}
		default:
			goto error;
	}
	error:
	PyErr_SetString(PyExc_ValueError, "Unknown unicode format");
	return NULL;
}


static char fixencoding__doc__[] = PyDoc_STR(
	"fixencoding(str, encoding) -> str or None\n\
	\n\
	Replaces the encoding specification in the XML declaration at the start of the\n\
	first argument with the encoding specified. If there's no XML declaration the\n\
	original string is returned. If the string isn't long enough to find an encoding\n\
	None is returned."
);


/* ==================================================================== */
/* python module interface */

static PyMethodDef _functions[] =
{
	{"detectencoding", detectencoding, METH_VARARGS, detectencoding__doc__ },
	{"fixencoding", fixencoding, METH_VARARGS, fixencoding__doc__ },
	{NULL, NULL}
};


static PyModuleDef_Slot _xml_codec_slots[] = {
	{0, NULL}
};

static struct PyModuleDef _xml_codec_module = {
	PyModuleDef_HEAD_INIT,
	.m_name = "_xml_codec",
	.m_size = 0,
	.m_methods = _functions,
	.m_slots = _xml_codec_slots
};

PyMODINIT_FUNC
PyInit__xml_codec(void)
{
	return PyModuleDef_Init(&_xml_codec_module);
}
