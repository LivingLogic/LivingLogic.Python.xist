/*
** Copyright 2009-2020 by LivingLogic AG, Bayreuth/Germany
** All Rights Reserved
** See LICENSE for the license
*/

grammar UL4;

NONE
	: 'None'
	;

TRUE
	: 'True'
	;

FALSE
	: 'False'
	;

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
	: (' '|'\t'|'\r'|'\n') -> channel(HIDDEN)
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


/* Rules common to all tags */

name
	: NAME
	;

literal
	: e_none=NONE # LiteralNone
	| e_false=FALSE # LiteralFalse
	| e_true=TRUE # LiteralTrue
	| e_integer=INT # LiteralInteger
	| e_float=FLOAT # LiteralFloat
	| e_string=STRING # LiteralString
	| e_string=STRING3 # LiteralString
	| e_date=DATE # LiteralDate
	| e_datetime=DATETIME # LiteralDatetime
	| e_color=COLOR # LiteralColor
	| e_name=name # LiteralName
	;

/* List literals */
seqitem
	:
		item=expr # SeqItem
	|
		star='*'
		unpackitem=expr # UnpackSeqItem
	;

list_
	:
		open_='['
		close=']' # ListEmpty
	|
		open_='['
		items+=seqitem
		(
			','
			items+=seqitem
		)*
		','?
		close=']' # List
	;

listcomprehension
	:
		open_='['
		item=expr
		'for'
		varname=nestedlvalue
		'in'
		container=expr
		(
			'if'
			condition=expr
		)?
		close=']' # ListComprehension
	;

/* Set literals */
set_
	:
		open_='{'
		'/'
		close='}' # SetEmpty
	|
		open_='{'
		items+=seqitem
		(
			','
			items+=seqitem
		)*
		','?
		close='}' # Set
	;

setcomprehension
	:
		open_='{'
		item=expr
		'for'
		varname=nestedlvalue
		'in'
		container=expr
		(
			'if'
			condition=expr
		)?
		close='}' # SetComprehension
	;

/* Dict literal */
dictitem
	:
		key=expr
		':'
		value=expr # DictItem
	|
		star='**'
		unpackitem=expr # UnpackDictItem
	;

dict_
	:
		open_='{'
		close='}' # DictEmpty
	|
		open_='{'
		items+=dictitem
		(
			','
			items+=dictitem
		)*
		','?
		close='}' # Dict
	;

dictcomprehension
	:
		open_='{'
		key=expr
		':'
		value=expr
		'for'
		varname=nestedlvalue
		'in'
		container=expr
		(
			'if'
			condition=expr
		)?
		close='}' # DictComprehension
	;

generatorexpression
	:
		item=expr
		'for'
		varname=nestedlvalue
		'in'
		container=expr
		(
			'if'
			condition=expr
		)? # GeneratorExpresssion
	;

atom
	: arg=literal # AtomLiteral
	| arg=list_ # AtomList
	| arg=listcomprehension # AtomListComprehension
	| arg=set_ # AtomSet
	| arg=setcomprehension # AtomSetComprehension
	| arg=dict_ # AtomDict
	| arg=dictcomprehension  # AtomDictComprehension
	| open_='(' arg=generatorexpression close=')' # AtomGeneratorExpression
	| open_='(' arg=expr close=')' # AtomBracket
	;

/* For variable unpacking in assignments and for loops */
nestedlvalue
	:
		lvalue=expr # LValueSimple
	|
		'(' lvalue=nestedlvalue ',' ')' # LValueOne
	|
		'('
		lvalue+=nestedlvalue
		','
		lvalue+=nestedlvalue
		(
			','
			lvalue+=nestedlvalue
		)*
		','?
		')' # LValueMulti
	;


/* Slice expression */
slice_
	:
		(
			index1=expr
		)?
		colon=':'
		(
			index2=expr
		)? # Slice
	;


/* Argument for a function/emthod call */
argument
	:
		argvalue=exprarg # PosArg
	|
		argname=name '=' argvalue=exprarg # KeywordArg
	|
		star='*' argvalue=exprarg # UnpackListArg
	|
		star='**' argvalue=exprarg # UnpackDictArg
	;

expr
	:
		e=atom # ExprAtom
	|
		/* Attribute access */
		e1=expr '.' n=name # Attr
	|
		/* Function/method call */
		e1=expr '(' ( args+=argument ( ',' args+=argument )* ','? )* close=')' # Call
	|
		/* Item access */
		e1=expr '[' index=expr close=']' # Item
	|
		/* Slice access */
		e1=expr '[' index=slice_ close=']' # ItemSlice
	|
		/* Negation */
		'-' arg=expr # Neg
	|
		/* Bitwise not */
		'~' arg=expr # BitNot
	|
		/* Multiplication */
		left=expr '*' right=expr # Mul
	|
		/* True division */
		left=expr '/' right=expr # TrueDiv
	|
		/* Floor division */
		left=expr '//' right=expr # FloorDiv
	|
		/* Modulo */
		left=expr '%' right=expr # Mod
	|
		/* Addition */
		left=expr '+' right=expr # Add
	|
		/* Subtraction */
		left=expr '-' right=expr # Sub
	|
		/* Binary shift left */
		left=expr '<<' right=expr # ShiftLeft
	|
		/* Binary shift right */
		left=expr '>>' right=expr # ShiftRight
	|
		/* Bitwise and */
		left=expr '&' right=expr # BitAnd
	|
		/* Bitwise exclusive or */
		left=expr '^' right=expr # BitXOr
	|
		/* Bitwise or */
		left=expr '|' right=expr # BitOr
	|
		/* Comparison: equal */
		left=expr '==' right=expr # EQ
	|
		/* Comparison: not equal */
		left=expr '!=' right=expr # NE
	|
		/* Comparison: less than */
		left=expr '<' right=expr # LT
	|
		/* Comparison: less than or equal */
		left=expr '<=' right=expr # LE
	|
		/* Comparison: greater than */
		left=expr '>' right=expr # GT
	|
		/* Comparison: greater than or equal */
		left=expr '>=' right=expr # GE
	|
		/* Containment test */
		left=expr 'in' right=expr # Contains
	|
		/* Inverted Containment test */
		left=expr 'not' 'in' right=expr # NotContains
	|
		/* Identify comparison */
		left=expr 'is' right=expr # Is
	|
		/* Inverted identify comparison */
		left=expr 'is' 'not' right=expr # IsNot
	|
		/* Boolean not operator */
		'not'e=expr # Not
	|
		/* Boolean and operator */
		left=expr 'and' right=expr # And
	|
		/* Boolean or operator */
		left=expr 'or' right=expr # Or
	|	
		/* If expression operator */
		argif=expr 'if' argcond=expr 'else' argelse=expr # If
	;

exprarg
	: ege=generatorexpression
	| e1=expr
	;

expression
	: ege=generatorexpression EOF # ExpressionGeneratorExpression
	| e=expr EOF # ExpressionExpression
	;


/* Additional rules for "for" tag */

for_
	:
		var=nestedlvalue
		'in'
		container=expr
		EOF # For
	;


/* Additional rules for "code" tag */

stmt
	: nn=nestedlvalue '=' e=expr EOF
	/* Actually the assignment target in the following rules must be "lvalue" (i.e. Attribute, item or slices assigments) */
	| n=expr '+=' e=expr EOF
	| n=expr '-=' e=expr EOF
	| n=expr '*=' e=expr EOF
	| n=expr '//=' e=expr EOF
	| n=expr '/=' e=expr EOF
	| n=expr '%=' e=expr EOF
	| n=expr '<<=' e=expr EOF
	| n=expr '>>=' e=expr EOF
	| n=expr '&=' e=expr EOF
	| n=expr '^=' e=expr EOF
	| n=expr '|=' e=expr EOF
	| ex=expression EOF
	;


/* Used for parsing signatures */
signature
	:
		/* No parameters */
		open_='('
		close=')' # SignatureNoParams
	|
		/* "**" parameter only */
		open_='('
		'**' rkwargsname=name
		','?
		close=')' # SignatureUnpackDictParams
	|
		/* "*" parameter only (and maybe **) */
		open_='('
		'*' rargsname=name
		(
			','
			'**' rkwargsname=name
		)?
		','?
		close=')' # SignatureUnpackParams
	|
		/* All parameters have a default */
		open_='('
		names+=name
		'='
		defaults+=exprarg
		(
			','
			names+=name
			'='
			defaults+=exprarg
		)*
		(
			','
			'*' rargsname=name
		)?
		(
			','
			'**' rkwargsname=name
		)?
		','?
		close=')' # SignatureDefaultParams
	|
		/* At least one parameter without a default */
		open_='('
		names_without_defaults+=name
		(
			','
			names_without_defaults+=name
		)*
		(
			','
			names_with_defaults+=name
			'='
			defaults+=exprarg
		)*
		(
			','
			'*' rargsname=name
		)?
		(
			','
			'**' rkwargsname=name
		)?
		','?
		close=')' # SignatureAnyParams
;


/* Additional rules for "def" tag */

definition
	:
		(
			n=name
		)?
		(
			sig=signature
		)?
		EOF
	;
