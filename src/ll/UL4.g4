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

float_
	: FLOAT
	;

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
		item=expr_if # SeqItem
	|
		star='*'
		unpackitem=expr_if # UnpackSeqItem
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
		item=expr_if
		'for'
		varname=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if
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
		item=expr_if
		'for'
		varname=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if
		)?
		close='}' # SetComprehension
	;

/* Dict literal */
dictitem
	:
		key=expr_if
		':'
		value=expr_if # DictItem
	|
		star='**'
		unpackitem=expr_if # UnpackDictItem
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
		key=expr_if
		':'
		value=expr_if
		'for'
		varname=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if
		)?
		close='}' # DictComprehension
	;

generatorexpression
	:
		item=expr_if
		'for'
		varname=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if
		)? # GeneratorExpresssion
	;

atom
	: e_literal=literal # AtomLiteral
	| e_list=list_ # AtomList
	| e_listcomp=listcomprehension # AtomListComprehension
	| e_set=set_ # AtomSet
	| e_setcomp=setcomprehension # AtomSetComprehension
	| e_dict=dict_ # AtomDict
	| e_dictcomp=dictcomprehension  # AtomDictComprehension
	| open_='(' e_genexpr=generatorexpression close=')' # AtomGeneratorComprehension
	| open_='(' e_bracket=expr_if close=')' # AtomIf
	;

/* For variable unpacking in assignments and for loops */
nestedlvalue
	:
		n=expr_subscript
	|
		'(' n0=nestedlvalue ',' ')'
	|
		'('
		n1=nestedlvalue
		','
		n2=nestedlvalue
		(
			','
			n3=nestedlvalue
		)*
		','?
		')'
	;


/* Slice expression */
slice_
	:
		(
			e1=expr_if
		)?
		colon=':'
		(
			e2=expr_if
		)?
	;


/* Function/method call, attribute access, item access, slice access */
argument
	:
		e=exprarg
	|
		en=name '=' ev=exprarg
	|
		star='*'
		es=exprarg
	|
		star='**'
		ess=exprarg
	;

expr_subscript returns [CodeAST node]
	:
		e1=atom
		(
			/* Attribute access */
			'.'
			n=name
		|
			/* Function/method call */
			'('
			(
				a1=argument
				(
					','
					a2=argument
				)*
				','?
			)*
			close=')'
		|
			/* Item access */
			'['
			e2_if=expr_if
			close=']'
		|
			/* Slice access */
			'['
			e2_slice=slice_
			close=']'
		)*
	;

/* Negation/bitwise not */
expr_unary
	:
		e1=expr_subscript
	|
		minus='-' e2=expr_unary
	|
		bitnot='~' e2=expr_unary
	;

/* Multiplication, division, modulo */
expr_mul
	:
		e1=expr_unary
		(
			op=('*'|'/'|'//'|'%')
			e2=expr_unary
		)*
	;

/* Addition, substraction */
expr_add
	:
		e1=expr_mul
		(
			op=('+'|'-')
			e2=expr_mul
		)*
	;

/* Binary shift */
expr_bitshift
	:
		e1=expr_add
		(
			op=('<<'|'>>')
			e2=expr_add
		)*
	;

/* Bitwise and */
expr_bitand
	:
		e1=expr_bitshift
		(
			'&'
			e2=expr_bitshift
		)*
	;

/* Bitwise exclusive or */
expr_bitxor
	:
		e1=expr_bitand
		(
			'^'
			e2=expr_bitand
		)*
	;

/* Bitwise or */
expr_bitor
	:
		e1=expr_bitxor
		(
			'|'
			e2=expr_bitxor
		)*
	;

/* Comparisons */
expr_cmp
	:
		e1=expr_bitor
		(
			(
				ops+='=='
			|
				ops+='!='
			|
				ops+='<'
			|
				ops+='<='
			|
				ops+='>'
			|
				ops+='>='
			|
				ops+='in'
			|
				ops+='not' ops+='in'
			|
				ops+='is'
			|
				ops+='is' ops+='not'
			)
			e2=expr_bitor
		)*
	;

/* Boolean not operator */
expr_not
	:
		e1=expr_cmp
	|
		n='not' e2=expr_not
	;

/* And operator */
expr_and
	:
		e1=expr_not
		(
			'and'
			e2=expr_not
		)*
	;

/* Or operator */
expr_or
	:
		e1=expr_and
		(
			'or'
			e2=expr_and
		)*
	;

/* If expression operator */
expr_if
	:
		e1=expr_or
		(
			'if'
			e2=expr_or
			'else'
			e3=expr_or
		)?
	;

exprarg
	: ege=generatorexpression
	| e1=expr_if
	;

expression
	: ege=generatorexpression EOF
	| e=expr_if EOF
	;


/* Additional rules for "for" tag */

for_
	:
		n=nestedlvalue
		'in'
		e=expr_if
		EOF
	;


/* Additional rules for "code" tag */

stmt
	: nn=nestedlvalue '=' e=expr_if EOF
	| n=expr_subscript '+=' e=expr_if EOF
	| n=expr_subscript '-=' e=expr_if EOF
	| n=expr_subscript '*=' e=expr_if EOF
	| n=expr_subscript '//=' e=expr_if EOF
	| n=expr_subscript '/=' e=expr_if EOF
	| n=expr_subscript '%=' e=expr_if EOF
	| n=expr_subscript '<<=' e=expr_if EOF
	| n=expr_subscript '>>=' e=expr_if EOF
	| n=expr_subscript '&=' e=expr_if EOF
	| n=expr_subscript '^=' e=expr_if EOF
	| n=expr_subscript '|=' e=expr_if EOF
	| ex=expression EOF
	;


/* Used for parsing signatures */
signature
	:
	open_='('
	(
		/* No paramteers */
	|
		/* "**" parameter only */
		'**' rkwargsname=name
		','?
	|
		/* "*" parameter only (and maybe **) */
		'*' rargsname=name
		(
			','
			'**' rkwargsname=name
		)?
		','?
	|
		/* All parameters have a default */
		aname1=name
		'='
		adefault1=exprarg
		(
			','
			aname2=name
			'='
			adefault2=exprarg
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
	|
		/* At least one parameter without a default */
		aname1=name
		(
			','
			aname2=name
		)*
		(
			','
			aname3=name
			'='
			adefault3=exprarg
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
	)
	close=')'
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
