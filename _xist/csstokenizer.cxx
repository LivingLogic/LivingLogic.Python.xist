/*
** Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
** Copyright 1999-2004 by Walter Dörwald
**
** All Rights Reserved
**
** Permission to use, copy, modify, and distribute this software and its documentation
** for any purpose and without fee is hereby granted, provided that the above copyright
** notice appears in all copies and that both that copyright notice and this permission
** notice appear in supporting documentation, and that the name of LivingLogic AG or
** the author not be used in advertising or publicity pertaining to distribution of the
** software without specific, written prior permission.
**
** LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
** INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
** LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
** DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
** IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
** IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
**
** This file is based on Java code from the Batik application, which is
**
******************************************************************************
** Copyright (C) The Apache Software Foundation. All rights reserved.        *
** ------------------------------------------------------------------------- *
** This software is published under the terms of the Apache Software License *
** version 1.1, a copy of which has been included at the end of this file    *
******************************************************************************
*/

#include "Python.h"

enum Token
{
	TOKEN_EOF, /* Represents the EOF lexical unit. */
	TOKEN_LEFT_CURLY_BRACE, /* Represents the '{' lexical unit. */
	TOKEN_RIGHT_CURLY_BRACE, /* Represents the '}' lexical unit. */
	TOKEN_EQUAL, /* Represents the '=' lexical unit. */
	TOKEN_PLUS, /* Represents the '+' lexical unit. */
	TOKEN_MINUS, /* Represents the '-' lexical unit. */
	TOKEN_COMMA, /* Represents the ',' lexical unit. */
	TOKEN_DOT, /* Represents the '.' lexical unit. */
	TOKEN_SEMI_COLON, /* Represents the ';' lexical unit. */
	TOKEN_PRECEDE, /* Represents the '>' lexical unit. */
	TOKEN_DIVIDE, /* Represents the '/' lexical unit. */
	TOKEN_LEFT_BRACKET, /* Represents the '[' lexical unit. */
	TOKEN_RIGHT_BRACKET, /* Represents the ']' lexical unit. */
	TOKEN_ANY, /* Represents the '*' lexical unit. */
	TOKEN_LEFT_BRACE, /* Represents the '(' lexical unit. */
	TOKEN_RIGHT_BRACE, /* Represents the ')' lexical unit. */
	TOKEN_COLON, /* Represents the ':' lexical unit. */
	TOKEN_SPACE, /* Represents the white space lexical unit. */
	TOKEN_COMMENT, /* Represents the comment lexical unit. */
	TOKEN_STRING, /* Represents the string lexical unit. */
	TOKEN_IDENTIFIER, /* Represents the identifier lexical unit. */
	TOKEN_CDO, /* Represents the '<!--' lexical unit. */
	TOKEN_CDC, /* Represents the '-->' lexical unit. */
	TOKEN_IMPORTANT_SYMBOL, /* Represents the '!important' lexical unit. */
	TOKEN_INTEGER, /* Represents an integer. */
	TOKEN_DASHMATCH, /* Represents the '|=' lexical unit. */
	TOKEN_INCLUDES, /* Represents the '~=' lexical unit. */
	TOKEN_HASH, /* Represents the '#name' lexical unit. */
	TOKEN_IMPORT_SYMBOL, /* Represents the '@import' lexical unit. */
	TOKEN_AT_KEYWORD, /* Represents the '@ident' lexical unit. */
	TOKEN_CHARSET_SYMBOL, /* Represents the '@charset' lexical unit. */
	TOKEN_FONT_FACE_SYMBOL, /* Represents the '@font-face' lexical unit. */
	TOKEN_MEDIA_SYMBOL, /* Represents the '@media' lexical unit. */
	TOKEN_PAGE_SYMBOL, /* Represents the '@page' lexical unit. */
	TOKEN_DIMENSION, /* Represents a dimension lexical unit. */
	TOKEN_EX, /* Represents a ex lexical unit. */
	TOKEN_EM, /* Represents a em lexical unit. */
	TOKEN_CM, /* Represents a cm lexical unit. */
	TOKEN_MM, /* Represents a mm lexical unit. */
	TOKEN_IN, /* Represents a in lexical unit. */
	TOKEN_MS, /* Represents a ms lexical unit. */
	TOKEN_HZ, /* Represents a hz lexical unit. */
	TOKEN_PERCENTAGE, /* Represents a % lexical unit. */
	TOKEN_S, /* Represents a s lexical unit. */
	TOKEN_PC, /* Represents a pc lexical unit. */
	TOKEN_PT, /* Represents a pt lexical unit. */
	TOKEN_PX, /* Represents a px lexical unit. */
	TOKEN_DEG, /* Represents a deg lexical unit. */
	TOKEN_RAD, /* Represents a rad lexical unit. */
	TOKEN_GRAD, /* Represents a grad lexical unit. */
	TOKEN_KHZ, /* Represents a khz lexical unit. */
	TOKEN_URI, /* Represents a 'url(URI)' lexical unit. */
	TOKEN_FUNCTION, /* Represents a 'ident(' lexical unit. */
	TOKEN_UNICODE_RANGE, /* Represents a unicode range lexical unit. */
	TOKEN_REAL /* represents a real number. */
};

const char *token_names[] =
{
	"EOF",
	"LEFT_CURLY_BRACE",
	"RIGHT_CURLY_BRACE",
	"EQUAL",
	"PLUS",
	"MINUS",
	"COMMA",
	"DOT",
	"SEMI_COLON",
	"PRECEDE",
	"DIVIDE",
	"LEFT_BRACKET",
	"RIGHT_BRACKET",
	"ANY",
	"LEFT_BRACE",
	"RIGHT_BRACE",
	"COLON",
	"SPACE",
	"COMMENT",
	"STRING",
	"IDENTIFIER",
	"CDO",
	"CDC",
	"IMPORTANT_SYMBOL",
	"INTEGER",
	"DASHMATCH",
	"INCLUDES",
	"HASH",
	"IMPORT_SYMBOL",
	"AT_KEYWORD",
	"CHARSET_SYMBOL",
	"FONT_FACE_SYMBOL",
	"MEDIA_SYMBOL",
	"PAGE_SYMBOL",
	"DIMENSION",
	"EX",
	"EM",
	"CM",
	"MM",
	"IN",
	"MS",
	"HZ",
	"PERCENTAGE",
	"S",
	"PC",
	"PT",
	"PX",
	"DEG",
	"RAD",
	"GRAD",
	"KHZ",
	"URI",
	"FUNCTION",
	"UNICODE_RANGE",
	"REAL"
};

/* tokenizer type definition */
class CSSTokenizer
{
	public:
	PyObject_HEAD

	PyObject *string; /* the string to parse */

	/* callbacks */
	PyObject *startDocument;
	PyObject *endDocument;
	PyObject *token;
};

extern PyTypeObject CSSTokenizer_Type;

static int IDENTIFIER_START[] = { 0, 0, 0x7fffffe, 0x7fffffe }; /* The set of the valid identifier start characters. */
static int NAME[] = { 0, 67051520, 134217726, 134217726 }; /* The set of the valid name characters. */
static int STRING[] = { 512, -133, -1, 2147483647 }; /* The set of the valid string characters. */
static int URI[] = { 0x0, 0xfffffc7a, 0xffffffff, 0x47ffffff }; /* The set of the valid uri characters. */

/* Tests whether the given character is a valid space. */
static bool isCSSSpace(int c)
{
	return ((c==' ') || (c=='\t') || (c=='\n') || (c=='\r') || (c=='\f'));
}

/* Tests whether the given character is a valid identifier start character. */
static bool isCSSIdentifierStartCharacter(int c)
{
	return c >= 128 || ((IDENTIFIER_START[c / 32] & (1 << (c % 32))) != 0);
}

/* Tests whether the given character is a valid name character. */
static bool isCSSNameCharacter(int c)
{
	return c >= 128 || ((NAME[c / 32] & (1 << (c % 32))) != 0);
}

/* Tests whether the given character is a valid hexadecimal character. */
static bool isCSSHexadecimalCharacter(int c)
{
	return isxdigit(c);
}

/* Tests whether the given character is a valid string character. */
static bool isCSSStringCharacter(int c) {
	return c >= 128 || ((STRING[c / 32] & (1 << (c % 32))) != 0);
}

/* Tests whether the given character is a valid URI character. */
static bool isCSSURICharacter(int c) {
	return c >= 128 || ((URI[c / 32] & (1 << (c % 32))) != 0);
}

class Scanner
{
	private:
	public:
		const char *buffer;
		int buflen; /* the size of the buffer */
		int line; /* The current line. */
		int column; /* The current column. */
		int current; /* The current char. */
		int position; /* The current position in the buffer. */
		enum Token type; /* The type of the current lexical unit. */
		int start; /* The start offset of the last lexical unit. */
		int end; /* The end offset of the last lexical unit. */
		int blankCharacters; /* The characters to skip to create the string which represents the current token. */

	public:
		Scanner(const char *s, int ibuflen) :
			buffer(s),
			buflen(ibuflen),
			line(0),
			column(-1),
			current('\0'),
			position(0),
			type((Token)-1),
			start(0),
			end(0),
			blankCharacters(0)
		{
			current = nextChar();
		}

		int getLine()
		{
			return line;
		}

		int getColumn()
		{
			return column;
		}

		int getStart()
		{
			return start;
		}

		int getEnd()
		{
			return end;
		}

		Token getType()
		{
			return type;
		}

		/* Returns the next token. Return -1 on success, 0 on error */
		int next()
		{
			blankCharacters = 0;
			start = position - 1;
			if (!nextToken())
				return 0;
			end = position - endGap();
			return -1;
		}

	protected:
		/* Returns the end gap of the current lexical unit. */
		int endGap()
		{
			int result = (current == -1) ? 0 : 1;
			switch (type)
			{
				case TOKEN_FUNCTION:
				case TOKEN_STRING:
				case TOKEN_S:
				case TOKEN_PERCENTAGE:
					result += 1;
					break;
				case TOKEN_COMMENT:
				case TOKEN_HZ:
				case TOKEN_EM:
				case TOKEN_EX:
				case TOKEN_PC:
				case TOKEN_PT:
				case TOKEN_PX:
				case TOKEN_CM:
				case TOKEN_MM:
				case TOKEN_IN:
				case TOKEN_MS:
					result += 2;
					break;
				case TOKEN_KHZ:
				case TOKEN_DEG:
				case TOKEN_RAD:
					result += 3;
					break;
				case TOKEN_GRAD:
					result += 4;
				default:
					break;
			}
			return result + blankCharacters;
		}

		/* Sets the value of the current char to the next character or -1 if the end of stream has been reached. */
		int nextChar()
		{
			if (position>=buflen)
				return current = -1;

			if (current != 10)
				++column;
			else
			{
				++line;
				column = 0;
			}

			return current = buffer[position++];
		}

		/* Scans an escape sequence, if one. Return -1 on success, 0 on error */
		int escape()
		{
			if (isCSSHexadecimalCharacter(current))
			{
				nextChar();
				if (!isCSSHexadecimalCharacter(current))
				{
					if (isCSSSpace(current))
					{
						nextChar();
					}
					return -1;
				}
				nextChar();
				if (!isCSSHexadecimalCharacter(current))
				{
					if (isCSSSpace(current))
					{
						nextChar();
					}
					return -1;
				}
				nextChar();
				if (!isCSSHexadecimalCharacter(current))
				{
					if (isCSSSpace(current))
					{
						nextChar();
					}
					return -1;
				}
				nextChar();
				if (!isCSSHexadecimalCharacter(current))
				{
					if (isCSSSpace(current))
					{
						nextChar();
					}
					return -1;
				}
				nextChar();
				if (!isCSSHexadecimalCharacter(current))
				{
					if (isCSSSpace(current))
					{
						nextChar();
					}
					return -1;
				}
			}
			if ((current >= ' ' && current <= '~') || current >= 128)
			{
				nextChar();
				return -1;
			}
			PyErr_Format(PyExc_ValueError,"character at line %d col %d", getLine(), getColumn());
			return 0;
		}

		/* Scans a single quoted string. return -1 on success, 0 on error */
		int string1()
		{
			nextChar();
			start = position - 1;
			for (;;)
			{
				switch (nextChar())
				{
					case -1:
						PyErr_Format(PyExc_ValueError,"eof at line %d column %d", getLine(), getColumn());
						return 0;
					case '\'':
						goto breakloop;
					case '"':
						break;
					case '\\':
						switch (nextChar())
						{
							case '\n':
							case '\f':
								break;
							default:
								if (!escape())
									return 0;
						}
						break;
					default:
						if (!isCSSStringCharacter(current))
						{
							PyErr_Format(PyExc_ValueError,"string1 character at line %d column %d", getLine(), getColumn());
							return 0;
						}
				}
			}
			breakloop:
			nextChar();
			type = TOKEN_STRING;
			return -1;
		}

		/* Scans a double quoted string. return -1 on success, 0 on error */
		int string2()
		{
			nextChar();
			start = position - 1;
			for (;;)
			{
				switch (nextChar())
				{
					case -1:
						PyErr_Format(PyExc_ValueError,"eof at line %d column %d", getLine(), getColumn());
						return 0;
					case '\'':
						break;
					case '"':
						goto breakloop;
					case '\\':
						switch (nextChar())
						{
							case '\n':
							case '\f':
								break;
							default:
								if (!escape())
									return 0;
						}
						break;
					default:
						if (!isCSSStringCharacter(current))
						{
							PyErr_Format(PyExc_ValueError,"string1 character at line %d column %d", getLine(), getColumn());
							return 0;
						}
				}
			}
			breakloop:
			nextChar();
			type = TOKEN_STRING;
			return -1;
		}

		/* Scans a number. Return -1 on success, 0 on error */
		int number()
		{
			for (;;)
			{
				switch (nextChar())
				{
					case '.':
						switch (nextChar())
						{
							case '0': case '1': case '2': case '3': case '4':
							case '5': case '6': case '7': case '8': case '9':
							return dotNumber();
						}
						PyErr_Format(PyExc_ValueError,"number at line %d column %d", getLine(), getColumn());
						return 0;
					default:
						goto breakloop;
					case '0': case '1': case '2': case '3': case '4':
					case '5': case '6': case '7': case '8': case '9':
						break;
				}
			}
			breakloop:
			return numberUnit(true);
		}

		/* Scans the decimal part of a number. Return -1 on success, 0 on error */
		int dotNumber()
		{
			for (;;)
			{
				switch (nextChar())
				{
					default:
						goto breakloop;
					case '0': case '1': case '2': case '3': case '4':
					case '5': case '6': case '7': case '8': case '9':
						break;
				}
			}
			breakloop:
			return numberUnit(false);
		}

		/* Scans the unit of a number. Return -1 on success, 0 on error */
		int numberUnit(bool integer)
		{
			switch (current)
			{
				case '%':
					nextChar();
					type = TOKEN_PERCENTAGE;
					return -1;
				case 'c':
				case 'C':
					switch (nextChar())
					{
						case 'm':
						case 'M':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								type = TOKEN_DIMENSION;
								return -1;
							}
							type = TOKEN_CM;
							return -1;
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							type = TOKEN_DIMENSION;
							return -1;
					}
				case 'd':
				case 'D':
					switch(nextChar())
					{
						case 'e':
						case 'E':
							switch (nextChar())
							{
								case 'g':
								case 'G':
									nextChar();
									if (current != -1 && isCSSNameCharacter(current))
									{
										do
										{
											nextChar();
										} while (current != -1 && isCSSNameCharacter(current));
										type = TOKEN_DIMENSION;
										return -1;
									}
									type = TOKEN_DEG;
									return -1;
							}
							default:
								while (current != -1 && isCSSNameCharacter(current))
								{
									nextChar();
								}
								type = TOKEN_DIMENSION;
								return -1;
					}
				case 'e':
				case 'E':
					switch(nextChar())
					{
						case 'm':
						case 'M':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								type = TOKEN_DIMENSION;
								return -1;
							}
							type = TOKEN_EM;
							return -1;
						case 'x':
						case 'X':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								type = TOKEN_DIMENSION;
								return -1;
							}
							type = TOKEN_EX;
							return -1;
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							type = TOKEN_DIMENSION;
							return -1;
					}
				case 'g':
				case 'G':
					switch(nextChar())
					{
						case 'r':
						case 'R':
							switch(nextChar())
							{
								case 'a':
								case 'A':
									switch(nextChar())
									{
										case 'd':
										case 'D':
											nextChar();
											if (current != -1 && isCSSNameCharacter(current))
											{
												do
												{
													nextChar();
												} while (current != -1 && isCSSNameCharacter(current));
												type = TOKEN_DIMENSION;
												return -1;
											}
											type = TOKEN_GRAD;
											return -1;
									}
							}
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							type = TOKEN_DIMENSION;
							return -1;
					}
				case 'h':
				case 'H':
					nextChar();
					switch(current)
					{
						case 'z':
						case 'Z':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								type = TOKEN_DIMENSION;
								return -1;
							}
							type = TOKEN_HZ;
							return -1;
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							type = TOKEN_DIMENSION;
							return -1;
					}
				case 'i':
				case 'I':
					switch(nextChar())
					{
						case 'n':
						case 'N':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								type = TOKEN_DIMENSION;
								return -1;
							}
							type = TOKEN_IN;
							return -1;
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							type = TOKEN_DIMENSION;
							return -1;
					}
				case 'k':
				case 'K':
					switch(nextChar())
					{
						case 'h':
						case 'H':
							switch(nextChar())
							{
								case 'z':
								case 'Z':
									nextChar();
									if (current != -1 && isCSSNameCharacter(current))
									{
										do
										{
											nextChar();
										} while (current != -1 && isCSSNameCharacter(current));
										return TOKEN_DIMENSION;
									}
									return TOKEN_KHZ;
							}
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							return TOKEN_DIMENSION;
					}
				case 'm':
				case 'M':
					switch(nextChar())
					{
						case 'm':
						case 'M':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								return TOKEN_DIMENSION;
							}
							return TOKEN_MM;
						case 's':
						case 'S':
							nextChar();
							if (current != -1 && isCSSNameCharacter(current))
							{
								do
								{
									nextChar();
								} while (current != -1 && isCSSNameCharacter(current));
								return TOKEN_DIMENSION;
							}
							return TOKEN_MS;
						default:
							while (current != -1 && isCSSNameCharacter(current))
							{
								nextChar();
							}
							return TOKEN_DIMENSION;
					}
					case 'p':
					case 'P':
						switch(nextChar())
						{
							case 'c':
							case 'C':
								nextChar();
								if (current != -1 && isCSSNameCharacter(current))
								{
									do
									{
										nextChar();
									} while (current != -1 && isCSSNameCharacter(current));
									return TOKEN_DIMENSION;
								}
								return TOKEN_PC;
							case 't':
							case 'T':
								nextChar();
								if (current != -1 && isCSSNameCharacter(current))
								{
									do
									{
										nextChar();
									} while (current != -1 && isCSSNameCharacter(current));
									return TOKEN_DIMENSION;
								}
								return TOKEN_PT;
							case 'x':
							case 'X':
								nextChar();
								if (current != -1 && isCSSNameCharacter(current))
								{
									do
									{
										nextChar();
									} while (current != -1 && isCSSNameCharacter(current));
									return TOKEN_DIMENSION;
								}
								return TOKEN_PX;
							default:
								while (current != -1 && isCSSNameCharacter(current))
								{
									nextChar();
								}
								return TOKEN_DIMENSION;
						}
					case 'r':
					case 'R':
						switch(nextChar())
						{
							case 'a':
							case 'A':
								switch(nextChar())
								{
									case 'd':
									case 'D':
										nextChar();
										if (current != -1 && isCSSNameCharacter(current))
										{
											do
											{
												nextChar();
											} while (current != -1 && isCSSNameCharacter(current));
											return TOKEN_DIMENSION;
										}
										return TOKEN_RAD;
								}
							default:
								while (current != -1 && isCSSNameCharacter(current))
								{
									nextChar();
								}
								return TOKEN_DIMENSION;
						}
					case 's':
					case 'S':
						nextChar();
						return TOKEN_S;
					default:
						if (current != -1 && isCSSIdentifierStartCharacter(current))
						{
							do
							{
								nextChar();
							} while (current != -1 && isCSSNameCharacter(current));
							return TOKEN_DIMENSION;
						}
						return (integer) ? TOKEN_INTEGER : TOKEN_REAL;
			}
		}

		/* Compares the given int with the given character, ignoring case. */
		static bool isEqualIgnoreCase(int i, char c)
		{
			return (i == -1) ? false : tolower(i) == c;
		}

	public:
		/* gets the next token. Return -1 on success, 0 on error */
		int nextToken()
		{
			switch (current)
			{
				case -1:
					type = TOKEN_EOF;
					return -1;
				case '{':
					nextChar();
					type = TOKEN_LEFT_CURLY_BRACE;
					return -1;
				case '}':
					nextChar();
					type = TOKEN_RIGHT_CURLY_BRACE;
					return -1;
				case '=':
					nextChar();
					type = TOKEN_EQUAL;
					return -1;
				case '+':
					nextChar();
					type = TOKEN_PLUS;
					return -1;
				case ',':
					nextChar();
					type = TOKEN_COMMA;
					return -1;
				case ';':
					nextChar();
					type = TOKEN_SEMI_COLON;
					return -1;
				case '>':
					nextChar();
					type = TOKEN_PRECEDE;
					return -1;
				case '[':
					nextChar();
					type = TOKEN_LEFT_BRACKET;
					return -1;
				case ']':
					nextChar();
					type = TOKEN_RIGHT_BRACKET;
					return -1;
				case '*':
					nextChar();
					type = TOKEN_ANY;
					return -1;
				case '(':
					nextChar();
					type = TOKEN_LEFT_BRACE;
					return -1;
				case ')':
					nextChar();
					type = TOKEN_RIGHT_BRACE;
					return -1;
				case ':':
					nextChar();
					type = TOKEN_COLON;
					return -1;
				case ' ':
				case '\t':
				case '\r':
				case '\n':
				case '\f':
					do
					{
						nextChar();
					} while (isCSSSpace(current));
					type = TOKEN_SPACE;
					return -1;
				case '/':
					nextChar();
					if (current != '*')
					{
						type = TOKEN_DIVIDE;
						return -1;
					}
					// Comment
					nextChar();
					start = position - 1;
					do
					{
						while (current != -1 && current != '*')
						{
							nextChar();
						}
						do
						{
							nextChar();
						} while (current != -1 && current == '*');
					} while (current != -1 && current != '/');
					if (current == -1)
					{
						PyErr_Format(PyExc_ValueError,"eof while looking for end of comment at line %d column %d", getLine(), getColumn());
						return 0;
					}
					nextChar();
					type = TOKEN_COMMENT;
					return -1;
				case '\'': // String1
					return string1();
				case '"': // String2
					return string2();
				case '<':
					nextChar();
					if (current != '!')
					{
						PyErr_Format(PyExc_ValueError,"wrong char while looking for ! at line %d column %d", getLine(), getColumn());
						return 0;
					}
					nextChar();
					if (current == '-')
					{
						nextChar();
						if (current == '-')
						{
							nextChar();
							type = TOKEN_CDO;
							return -1;
						}
					}
					PyErr_Format(PyExc_ValueError,"wrong char while looking for ! at line %d column %d", getLine(), getColumn());
					return 0;
				case '-':
					nextChar();
					if (current != '-')
					{
						type = TOKEN_MINUS;
						return -1;
					}
					nextChar();
					if (current == '>')
					{
						nextChar();
						type = TOKEN_CDC;
						return -1;
					}
					PyErr_Format(PyExc_ValueError,"wrong char while looking for - or > at line %d column %d", getLine(), getColumn());
					return 0;
				case '|':
					nextChar();
					if (current == '=')
					{
						nextChar();
						type = TOKEN_DASHMATCH;
						return -1;
					}
					PyErr_Format(PyExc_ValueError,"wrong char while looking for = in |= at line %d column %d", getLine(), getColumn());
					return 0;
				case '~':
					nextChar();
					if (current == '=')
					{
						nextChar();
						type = TOKEN_INCLUDES;
						return -1;
					}
					PyErr_Format(PyExc_ValueError,"wrong char while looking for = in ~= at line %d column %d", getLine(), getColumn());
					return 0;
				case '#':
					nextChar();
					if (isCSSNameCharacter(current))
					{
						start = position - 1;
						do
						{
							nextChar();
							if (current == '\\')
							{
								nextChar();
								escape();
							}
						} while (current != -1 && isCSSNameCharacter(current));
						type = TOKEN_HASH;
						return -1;
					}
					PyErr_Format(PyExc_ValueError,"wrong char in # at line %d column %d", getLine(), getColumn());
					return 0;
				case '@':
					nextChar();
					switch (current)
					{
						case 'c':
						case 'C':
							start = position - 1;
							if (isEqualIgnoreCase(nextChar(), 'h') &&
							    isEqualIgnoreCase(nextChar(), 'a') &&
							    isEqualIgnoreCase(nextChar(), 'r') &&
							    isEqualIgnoreCase(nextChar(), 's') &&
							    isEqualIgnoreCase(nextChar(), 'e') &&
							    isEqualIgnoreCase(nextChar(), 't'))
							{
								nextChar();
								type = TOKEN_CHARSET_SYMBOL;
								return -1;
							}
							break;
						case 'f':
						case 'F':
							start = position - 1;
							if (isEqualIgnoreCase(nextChar(), 'o') &&
							    isEqualIgnoreCase(nextChar(), 'n') &&
							    isEqualIgnoreCase(nextChar(), 't') &&
							    isEqualIgnoreCase(nextChar(), '-') &&
							    isEqualIgnoreCase(nextChar(), 'f') &&
							    isEqualIgnoreCase(nextChar(), 'a') &&
							    isEqualIgnoreCase(nextChar(), 'c') &&
							    isEqualIgnoreCase(nextChar(), 'e'))
							{
								nextChar();
								type = TOKEN_FONT_FACE_SYMBOL;
								return -1;
							}
							break;
						case 'i':
						case 'I':
							start = position - 1;
							if (isEqualIgnoreCase(nextChar(), 'm') &&
							    isEqualIgnoreCase(nextChar(), 'p') &&
							    isEqualIgnoreCase(nextChar(), 'o') &&
							    isEqualIgnoreCase(nextChar(), 'r') &&
							    isEqualIgnoreCase(nextChar(), 't'))
							{
								nextChar();
								type = TOKEN_IMPORT_SYMBOL;
								return -1;
							}
							break;
						case 'm':
						case 'M':
							start = position - 1;
							if (isEqualIgnoreCase(nextChar(), 'e') &&
							    isEqualIgnoreCase(nextChar(), 'd') &&
							    isEqualIgnoreCase(nextChar(), 'i') &&
							    isEqualIgnoreCase(nextChar(), 'a'))
							{
								nextChar();
								type = TOKEN_MEDIA_SYMBOL;
								return -1;
							}
							break;
						case 'p':
						case 'P':
							start = position - 1;
							if (isEqualIgnoreCase(nextChar(), 'a') &&
							    isEqualIgnoreCase(nextChar(), 'g') &&
							    isEqualIgnoreCase(nextChar(), 'e'))
							{
								nextChar();
								type = TOKEN_PAGE_SYMBOL;
								return -1;
							}
							break;
						default:
							if (!isCSSIdentifierStartCharacter(current))
							{
								PyErr_Format(PyExc_ValueError,"wrong char at line %d column %d", getLine(), getColumn());
								return 0;
							}
							start = position - 1;
					}
					do
					{
						nextChar();
						if (current == '\\')
						{
							nextChar();
							escape();
						}
					} while (current != -1 && isCSSNameCharacter(current));
					type = TOKEN_AT_KEYWORD;
					return -1;
				case '!':
					do
					{
						nextChar();
					} while (current != -1 && isCSSSpace(current));
					if (isEqualIgnoreCase(current, 'i') &&
					    isEqualIgnoreCase(nextChar(), 'm') &&
					    isEqualIgnoreCase(nextChar(), 'p') &&
					    isEqualIgnoreCase(nextChar(), 'o') &&
					    isEqualIgnoreCase(nextChar(), 'r') &&
					    isEqualIgnoreCase(nextChar(), 't') &&
					    isEqualIgnoreCase(nextChar(), 'a') &&
					    isEqualIgnoreCase(nextChar(), 'n') &&
					    isEqualIgnoreCase(nextChar(), 't'))
					{
						nextChar();
						type = TOKEN_IMPORTANT_SYMBOL;
						return -1;
					}
					if (current == -1)
						PyErr_Format(PyExc_ValueError,"eof when parsing !important at line %d column %d", getLine(), getColumn());
					else
						PyErr_Format(PyExc_ValueError,"wrong char when parsing !important at line %d column %d", getLine(), getColumn());
					return 0;
				case '0': case '1': case '2': case '3': case '4':
				case '5': case '6': case '7': case '8': case '9':
					return number();
				case '.':
					switch (nextChar())
					{
						case '0': case '1': case '2': case '3': case '4':
						case '5': case '6': case '7': case '8': case '9':
							return dotNumber();
						default:
							type = TOKEN_DOT;
							return -1;
					}
				case 'u':
				case 'U':
					nextChar();
					switch (current)
					{
						case '+':
						{
							bool range = false;
							for (int i = 0; i < 6; i++)
							{
								nextChar();
								switch (current)
								{
									case '?':
										range = true;
										break;
									default:
										if (range && !isCSSHexadecimalCharacter(current))
										{
											PyErr_Format(PyExc_ValueError,"unicode at line %d column %d", getLine(), getColumn());
											return 0;
										}
								}
							}
							nextChar();
							if (range)
							{
								type = TOKEN_UNICODE_RANGE;
								return -1;
							}
							if (current == '-')
							{
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									PyErr_Format(PyExc_ValueError,"unicode at line %d column %d", getLine(), getColumn());
									return 0;
								}
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									type = TOKEN_UNICODE_RANGE;
									return -1;
								}
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									type = TOKEN_UNICODE_RANGE;
									return -1;
								}
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									type = TOKEN_UNICODE_RANGE;
									return -1;
								}
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									type = TOKEN_UNICODE_RANGE;
									return -1;
								}
								nextChar();
								if (!isCSSHexadecimalCharacter(current))
								{
									type = TOKEN_UNICODE_RANGE;
									return -1;
								}
								nextChar();
								type = TOKEN_UNICODE_RANGE;
								return -1;
							}
						}
						case 'r':
						case 'R':
							nextChar();
							switch (current)
							{
								case 'l':
								case 'L':
									nextChar();
									switch (current)
									{
										case '(':
											do
											{
												nextChar();
											} while (current != -1 && isCSSSpace(current));
											switch (current)
											{
												case '\'':
													string1();
													blankCharacters += 2;
													while (current != -1 && isCSSSpace(current))
													{
														blankCharacters++;
														nextChar();
													}
													if (current == -1)
													{
														PyErr_Format(PyExc_ValueError,"eof while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													if (current != ')')
													{
														PyErr_Format(PyExc_ValueError,"wrong char while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													nextChar();
													type = TOKEN_URI;
													return -1;
												case '"':
													string2();
													blankCharacters += 2;
													while (current != -1 && isCSSSpace(current))
													{
														blankCharacters++;
														nextChar();
													}
													if (current == -1)
													{
														PyErr_Format(PyExc_ValueError,"eof while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													if (current != ')')
													{
														PyErr_Format(PyExc_ValueError,"wrong char while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													nextChar();
													type = TOKEN_URI;
													return -1;
												case ')':
													PyErr_Format(PyExc_ValueError,"wrong char while parsing URL at line %d column %d", getLine(), getColumn());
													return 0;
												default:
													if (!isCSSURICharacter(current))
													{
														PyErr_Format(PyExc_ValueError,"wrong char in URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													start = position - 1;
													do
													{
														nextChar();
													} while (current != -1 && isCSSURICharacter(current));
													blankCharacters++;
													while (current != -1 && isCSSSpace(current))
													{
														blankCharacters++;
														nextChar();
													}
													if (current == -1)
													{
														PyErr_Format(PyExc_ValueError,"eof while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													if (current != ')')
													{
														PyErr_Format(PyExc_ValueError,"wrong char while parsing URL at line %d column %d", getLine(), getColumn());
														return 0;
													}
													nextChar();
													type = TOKEN_URI;
													return -1;
											}
									}
							}
					}
					while (current != -1 && isCSSNameCharacter(current))
					{
						nextChar();
					}
					if (current == '(')
					{
						nextChar();
						type = TOKEN_FUNCTION;
						return -1;
					}
					type = TOKEN_IDENTIFIER;
					return -1;
				default:
					if (isCSSIdentifierStartCharacter(current))
					{
						// Identifier
						do
						{
							nextChar();
							if (current == '\\')
							{
								nextChar();
								escape();
							}
						} while (current != -1 && isCSSNameCharacter(current));
						if (current == '(')
						{
							nextChar();
							type = TOKEN_FUNCTION;
							return -1;
						}
						type = TOKEN_IDENTIFIER;
						return -1;
					}
					nextChar();
					PyErr_Format(PyExc_ValueError,"illegal char at line %d column %d", getLine(), getColumn());
					return 0;
			}
			return -1;
		}
};

static int callWithVoid(CSSTokenizer *self, PyObject *callback)
{
	if (callback)
	{
		PyObject *res = PyObject_CallFunction(callback, NULL);
		if (!res)
			return 0;
		Py_DECREF(res);
	}
	return -1;
}

/*
static int callWithString(CSSTokenizer *self, PyObject *callback, const char *data, int len)
{
	if (callback)
	{
		PyObject *res = PyObject_CallFunction(callback, "s#", data, len);
		if (!res)
			return 0;
		Py_DECREF(res);
	}
	return -1;
}
*/

static int callWith2Strings(CSSTokenizer *self, PyObject *callback, const char *data1, int len1, const char *data2, int len2)
{
	if (callback)
	{
		PyObject *res = PyObject_CallFunction(callback, "s#s#", data1, len1, data2, len2);
		if (!res)
			return 0;
		Py_DECREF(res);
	}
	return -1;
}

#define GETCB(member, name) Py_XDECREF(self->member); self->member = PyObject_GetAttrString(item, name);

static PyObject *parser_register(CSSTokenizer *self, PyObject *args)
{
	/* register a callback object */
	PyObject* item;
	if (!PyArg_ParseTuple(args, "O", &item))
	  return NULL;

	GETCB(startDocument, "startDocument");
	GETCB(endDocument, "endDocument");
	GETCB(token, "token");

	PyErr_Clear();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *parser_parse(CSSTokenizer *self, PyObject *args)
{
	const char *s;
	int len;

	if (!PyArg_ParseTuple(args, "s#:parse", &s, &len))
		return NULL;

	if (!callWithVoid(self, self->startDocument))
		return NULL;

	Scanner scanner(s, len);

	Token t;
	if (!scanner.next())
		return NULL;
	while ((t = scanner.getType()) != TOKEN_EOF)
	{
		if (!callWith2Strings(self, self->token,
					token_names[t], strlen(token_names[t]),
				scanner.buffer+scanner.start, scanner.end-scanner.start))
			return NULL;
		if (!scanner.next())
			return NULL;
	}
	if (!callWithVoid(self, self->endDocument))
		return NULL;

	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef CSSTokenizer_methods[] =
{
	/* register callbacks */
	{"register", (PyCFunction) parser_register, METH_VARARGS},
	/* one-shot parsing */
	{"parse", (PyCFunction) parser_parse, METH_VARARGS},
	{NULL, NULL}
};

static char parser_new__doc__[] = "create a parser";

static PyObject *parser_new(PyObject *noself, PyObject *args)
{
	if (!PyArg_NoArgs(args))
		return NULL;

	CSSTokenizer *self = PyObject_NEW(CSSTokenizer, &CSSTokenizer_Type);
	self->startDocument = NULL;
	self->endDocument = NULL;
	self->token = NULL;
	return (PyObject *)self;
}

static void parser_del(CSSTokenizer *self)
{
	Py_XDECREF(self->startDocument);
	Py_XDECREF(self->endDocument);
	Py_XDECREF(self->token);
	PyMem_DEL(self);
}

static PyObject *parser_getattr(CSSTokenizer *self, char *name)
{
    return Py_FindMethod(CSSTokenizer_methods, (PyObject*) self, name);
}

PyTypeObject CSSTokenizer_Type =
{
	PyObject_HEAD_INIT(NULL)
	0, /* ob_size */
	"CSSTokenizer", /* tp_name */
	sizeof(CSSTokenizer), /* tp_size */
	0, /* tp_itemsize */
	/* methods */
	(destructor)parser_del, /* tp_dealloc */
	0, /* tp_print */
	(getattrfunc)parser_getattr, /* tp_getattr */
	0 /* tp_setattr */
};

static PyMethodDef _functions[] =
{
	{"CSSTokenizer", parser_new, METH_NOARGS, parser_new__doc__},
	{NULL, NULL}
};

static char module__doc__[] =
"a CSS parser.";

extern "C" void
#ifdef WIN32
__declspec(dllexport)
#endif
initcsstokenizer(void)
{
	// PyANSIStream_Type.ob_type = &PyType_Type; /* fix the type pointer */
	Py_InitModule3("csstokenizer", _functions, module__doc__);
}

/*
 ============================================================================
                   The Apache Software License, Version 1.1
 ============================================================================
 
 Copyright (C) 2000 The Apache Software Foundation. All rights reserved.
 
 Redistribution and use in source and binary forms, with or without modifica-
 tion, are permitted provided that the following conditions are met:
 
 1. Redistributions of  source code must  retain the above copyright  notice,
    this list of conditions and the following disclaimer.
 
 2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
 
 3. The end-user documentation included with the redistribution, if any, must
    include  the following  acknowledgment:  "This product includes  software
    developed  by the  Apache Software Foundation  (http://www.apache.org/)."
    Alternately, this  acknowledgment may  appear in the software itself,  if
    and wherever such third-party acknowledgments normally appear.
 
 4. The names "Batik" and  "Apache Software Foundation"  must not be  used to
    endorse  or promote  products derived  from this  software without  prior
    written permission. For written permission, please contact
    apache@apache.org.
 
 5. Products  derived from this software may not  be called "Apache", nor may
    "Apache" appear  in their name,  without prior written permission  of the
    Apache Software Foundation.
 
 THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED WARRANTIES,
 INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 FITNESS  FOR A PARTICULAR  PURPOSE ARE  DISCLAIMED.  IN NO  EVENT SHALL  THE
 APACHE SOFTWARE  FOUNDATION  OR ITS CONTRIBUTORS  BE LIABLE FOR  ANY DIRECT,
 INDIRECT, INCIDENTAL, SPECIAL,  EXEMPLARY, OR CONSEQUENTIAL  DAMAGES (INCLU-
 DING, BUT NOT LIMITED TO, PROCUREMENT  OF SUBSTITUTE GOODS OR SERVICES; LOSS
 OF USE, DATA, OR  PROFITS; OR BUSINESS  INTERRUPTION)  HOWEVER CAUSED AND ON
 ANY  THEORY OF LIABILITY,  WHETHER  IN CONTRACT,  STRICT LIABILITY,  OR TORT
 (INCLUDING  NEGLIGENCE OR  OTHERWISE) ARISING IN  ANY WAY OUT OF THE  USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
 This software  consists of voluntary contributions made  by many individuals
 on  behalf  of the Apache Software  Foundation. For more  information on the
 Apache Software Foundation, please see <http://www.apache.org/>.
*/
