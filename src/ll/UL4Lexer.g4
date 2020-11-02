/*
** Copyright 2009-2020 by LivingLogic AG, Bayreuth/Germany
** All Rights Reserved
** See LICENSE for the license
*/

lexer grammar UL4Lexer;

/*
	We have multiple modes:

		* DEFAULT_MODE: The initial mode that extracts the indentation of a line
		* TEXT_MODE: any other text outside of a tag
		* MAYBETAG_MODE: We've seen a `<?'
		* TAG_MODE: Inside of a tag
*/

DEFAULT_INDENT: [ \t]+ -> mode(TEXT_MODE);
DEFAULT_LINEEND: '\r'? '\n' -> mode(DEFAULT_MODE);
DEFAULT_MAYBETAG: '<?' -> mode(MAYBETAG_MODE);
DEFAULT_OTHER: . -> mode(TEXT_MODE);


mode TEXT_MODE;

TEXT_MAYBETAG: '<?' -> pushMode(MAYBETAG_MODE);
TEXT_LINEEND: '\r'? '\n' -> mode(DEFAULT_MODE);
TEXT_OTHER: ~('<?' | '\r\n'| '\n')+;


mode MAYBETAG_MODE;

MAYBETAG_WS: [ \t\r\n];
MAYBETAG_WHITESPACE: 'whitespace' -> mode(WHITESPACE_MODE);
MAYBETAG_DOC: 'doc' -> mode(TEXTTAG_MODE);
MAYBETAG_NOTE: 'note' -> mode(TEXTTAG_MODE);
MAYBETAG_UL4: 'ul4' -> mode(TAG_MODE);
MAYBETAG_DEF: 'def' -> mode(TAG_MODE);
MAYBETAG_FOR: 'for' -> mode(TAG_MODE);
MAYBETAG_WHILE: 'while' -> mode(TAG_MODE);
MAYBETAG_IF: 'if' -> mode(TAG_MODE);
MAYBETAG_ELIF: 'elif' -> mode(TAG_MODE);
MAYBETAG_ELSE: 'else' -> mode(TAG_MODE);
MAYBETAG_RENDERBLOCK: 'renderblock' -> mode(TAG_MODE);
MAYBETAG_RENDERBLOCKS: 'renderblocks' -> mode(TAG_MODE);
MAYBETAG_PRINT: 'print' -> mode(TAG_MODE);
MAYBETAG_PRINTX: 'printx' -> mode(TAG_MODE);
MAYBETAG_CODE: 'code' -> mode(TAG_MODE);
MAYBETAG_END: 'end' -> mode(TAG_MODE);

MAYBETAG_OTHER: .+?;

mode WHITESPACE_MODE;

WHITESPACE_VALUE: ('keep'|'smart'|'strip');
WHITESPACE_WS: [ \t\r\n];
WHITESPACE_ENDDELIM: '?>' -> mode(TEXT_MODE);

mode TEXTTAG_MODE;

TEXTTAG_TEXT: .;
TEXTTAG_WS: [ \t\r\n];
TEXTTAG_ENDDELIM: '?>' -> mode(TEXT_MODE);

mode TAG_MODE;

ENDDELIM: '?>' -> mode(TEXT_MODE);

/* Keywords */
FOR: 'for';
IN: 'in';
IF: 'if';
ELSE: 'else';
NOT: 'not';
IS: 'is';
AND: 'and';
OR: 'or';

/* Keywords for constants */
NONE: 'None';
TRUE: 'True';
FALSE: 'False';

/* Additional keywords for block ends */
DEF: 'def';
WHILE: 'while';
RENDERBLOCK: 'renderblock';
RENDERBLOCKS: 'renderblocks';

/* Symbols */
PARENS_OPEN: '(';
PARENS_CLOSE: ')';
BRACKET_OPEN: '[';
BRACKET_CLOSE: ']';
BRACE_OPEN: '{';
BRACE_CLOSE: '}';
STAR_STAR: '**';
STAR: '*';
PLUS: '+';
MINUS: '-';
SLASH_SLASH: '//';
SLASH: '/';
PERCENT: '%';
EQUAL: '==';
NOT_EQUAL: '!=';
LESS_THAN_OR_EQUAL: '<=';
LESS_THAN: '<';
GREATER_THAN_OR_EQUAL: '>=';
GREATER_THAN: '>';
ASSIGN: '=';
COMMA: ',';
COLON: ':';
TILDE: '~';
AMPERSAND: '&';
CARET: '^';
DOT: '.';
SHIFTLEFT: '<<';
SHIFTRIGHT: '>>';
BAR: '|';

/* Symbol for augmentet assignment */
AUGADD: '+=';
AUGSUB: '-=';
AUGMUL: '*=';
AUGFLOORDIV: '//=';
AUGTRUEDIV: '/=';
AUGMOD: '%=';
AUGSHIFTLEFT: '<<=';
AUGSHIFTRIGHT: '>>=';
AUGAND: '&=';
AUGXOR: '^=';
AUGOR: '|=';


NAME
	: ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
	;

fragment
DIGIT
	: '0'..'9'
	;

fragment
BIN_DIGIT
	: ('0'|'1')
	;

fragment
OCT_DIGIT
	: '0'..'7'
	;

fragment
HEX_DIGIT
	: ('0'..'9'|'a'..'f'|'A'..'F')
	;

INT
	/* We don't have negative ints (as this would tokenize "1-2" wrong) */
	: DIGIT+
	| '0' ('b'|'B') BIN_DIGIT+
	| '0' ('o'|'O') OCT_DIGIT+
	| '0' ('x'|'X') HEX_DIGIT+
	;

fragment
EXPONENT
	: ('e'|'E') ('+'|'-')? DIGIT+
	;

FLOAT
	: DIGIT+ '.' DIGIT* EXPONENT?
	| '.' DIGIT+ EXPONENT?
	| DIGIT+ EXPONENT
	;

fragment
TIME
	: DIGIT DIGIT ':' DIGIT DIGIT ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT)?)?;

DATE
	: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ')';

DATETIME
	: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT 'T' TIME? ')';

COLOR
	: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	;

WS
	: (' '|'\t'|'\r'|'\n') -> skip
	;

STRING
	: '"' ( ESC_SEQ | ~('\\'|'"'|'\r'|'\n') )* '"'
	| '\'' ( ESC_SEQ | ~('\\'|'\''|'\r'|'\n') )* '\''
	;

STRING3
	: '"""' TRIQUOTE*? '"""'
	|  '\'\'\'' TRIAPOS*? '\'\'\''
	;

fragment
TRIQUOTE
	: ('"'|'""')? (ESC_SEQ|~('\\'|'"'))+
	;

fragment
TRIAPOS
	: ('\''|'\'\'')? (ESC_SEQ|~('\\'|'\''))+
	;

fragment
ESC_SEQ
	: '\\' ('a'|'b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\')
	| UNICODE1_ESC
	| UNICODE2_ESC
	| UNICODE4_ESC
	;

fragment
UNICODE1_ESC
	: '\\' 'x' HEX_DIGIT HEX_DIGIT
	;

fragment
UNICODE2_ESC
	: '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	;

fragment
UNICODE4_ESC
	: '\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	;
