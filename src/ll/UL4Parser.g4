/*
** Copyright 2009-2020 by LivingLogic AG, Bayreuth/Germany
** All Rights Reserved
** See LICENSE for the license
*/

parser grammar UL4Parser;

options { tokenVocab = UL4Lexer; }


template
	:
		head=ul4tag?
		content+=templatebodyitem* # TopLevel
	;

ul4tag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS?
		MAYBETAG_UL4
		MAYBETAG_WS?
		(
			templatename=name
		)?
		(
			templatesignature=signature
		)?
		ENDDELIM # TagUL4
	;

whitespacetag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS?
		MAYBETAG_WHITESPACE
		WHITESPACE_WS?
		whitespace=WHITESPACE_VALUE
		WHITESPACE_WS?
		WHITESPACE_ENDDELIM # TagWhitespace
	;

doctag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS?
		MAYBETAG_DOC
		MAYBETAG_WS?
		ENDDELIM
	;

notetag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS?
		MAYBETAG_NOTE
		MAYBETAG_WS?
		ENDDELIM
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
		star=STAR
		unpackitem=expr # UnpackSeqItem
	;

list_
	:
		open_=BRACKET_OPEN
		close=BRACKET_CLOSE # ListEmpty
	|
		open_=BRACKET_OPEN
		items+=seqitem
		(
			COMMA
			items+=seqitem
		)*
		COMMA?
		close=BRACKET_CLOSE # List
	;

listcomprehension
	:
		open_=BRACKET_OPEN
		item=expr
		FOR
		varname=nestedlvalue
		IN
		container=expr
		(
			IF
			condition=expr
		)?
		close=BRACKET_CLOSE # ListComprehension
	;

/* Set literals */
set_
	:
		open_=BRACE_OPEN
		SLASH
		close=BRACE_CLOSE # SetEmpty
	|
		open_=BRACE_OPEN
		items+=seqitem
		(
			COMMA
			items+=seqitem
		)*
		COMMA?
		close=BRACE_CLOSE # Set
	;

setcomprehension
	:
		open_=BRACE_OPEN
		item=expr
		FOR
		varname=nestedlvalue
		IN
		container=expr
		(
			IF
			condition=expr
		)?
		close=BRACE_CLOSE # SetComprehension
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
		open_=BRACE_OPEN
		close=BRACE_CLOSE # DictEmpty
	|
		open_=BRACE_OPEN
		items+=dictitem
		(
			COMMA
			items+=dictitem
		)*
		COMMA?
		close=BRACE_CLOSE # Dict
	;

dictcomprehension
	:
		open_=BRACE_OPEN
		key=expr
		':'
		value=expr
		FOR
		varname=nestedlvalue
		IN
		container=expr
		(
			IF
			condition=expr
		)?
		close=BRACE_CLOSE # DictComprehension
	;

generatorexpression
	:
		item=expr
		FOR
		varname=nestedlvalue
		IN
		container=expr
		(
			IF
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
	| open_=PARENS_OPEN arg=generatorexpression close=PARENS_CLOSE # AtomGeneratorExpression
	| open_=PARENS_OPEN arg=expr close=PARENS_CLOSE # AtomBracket
	;

/* For variable unpacking in assignments and for loops */
nestedlvalue
	:
		lvalue=expr # LValueSimple
	|
		PARENS_OPEN lvalue=nestedlvalue COMMA PARENS_CLOSE # LValueOne
	|
		PARENS_OPEN
		lvalue+=nestedlvalue
		COMMA
		lvalue+=nestedlvalue
		(
			COMMA
			lvalue+=nestedlvalue
		)*
		COMMA?
		PARENS_CLOSE # LValueMulti
	;


/* Slice expression */
slice_
	:
		(
			index1=expr
		)?
		colon=COLON
		(
			index2=expr
		)? # Slice
	;


/* Argument for a function/emthod call */
argument
	:
		argvalue=exprarg # PosArg
	|
		argname=name ASSIGN argvalue=exprarg # KeywordArg
	|
		star=STAR argvalue=exprarg # UnpackListArg
	|
		star=STAR_STAR argvalue=exprarg # UnpackDictArg
	;

expr
	:
		e=atom # ExprAtom
	|
		/* Attribute access */
		e1=expr DOT n=name # Attr
	|
		/* Function/method call */
		e1=expr PARENS_OPEN ( args+=argument ( COMMA args+=argument )* COMMA? )* close=PARENS_CLOSE # Call
	|
		/* Item access */
		e1=expr BRACKET_OPEN index=expr close=BRACKET_CLOSE # Item
	|
		/* Slice access */
		e1=expr BRACKET_OPEN index=slice_ close=BRACKET_CLOSE # ItemSlice
	|
		/* Negation */
		MINUS arg=expr # Neg
	|
		/* Bitwise not */
		TILDE arg=expr # BitNot
	|
		/* Multiplication */
		left=expr STAR right=expr # Mul
	|
		/* True division */
		left=expr SLASH right=expr # TrueDiv
	|
		/* Floor division */
		left=expr SLASH_SLASH right=expr # FloorDiv
	|
		/* Modulo */
		left=expr PERCENT right=expr # Mod
	|
		/* Addition */
		left=expr PLUS right=expr # Add
	|
		/* Subtraction */
		left=expr MINUS right=expr # Sub
	|
		/* Binary shift left */
		left=expr SHIFTLEFT right=expr # ShiftLeft
	|
		/* Binary shift right */
		left=expr SHIFTRIGHT right=expr # ShiftRight
	|
		/* Bitwise and */
		left=expr AMPERSAND right=expr # BitAnd
	|
		/* Bitwise exclusive or */
		left=expr CARET right=expr # BitXOr
	|
		/* Bitwise or */
		left=expr BAR right=expr # BitOr
	|
		/* Comparison: equal */
		left=expr EQUAL right=expr # EQ
	|
		/* Comparison: not equal */
		left=expr NOT_EQUAL right=expr # NE
	|
		/* Comparison: less than */
		left=expr LESS_THAN right=expr # LT
	|
		/* Comparison: less than or equal */
		left=expr LESS_THAN_OR_EQUAL right=expr # LE
	|
		/* Comparison: greater than */
		left=expr GREATER_THAN right=expr # GT
	|
		/* Comparison: greater than or equal */
		left=expr GREATER_THAN_OR_EQUAL right=expr # GE
	|
		/* Containment test */
		left=expr IN right=expr # Contains
	|
		/* Inverted Containment test */
		left=expr NOT IN right=expr # NotContains
	|
		/* Identify comparison */
		left=expr IS right=expr # Is
	|
		/* Inverted identify comparison */
		left=expr IS NOT right=expr # IsNot
	|
		/* Boolean not operator */
		NOT e=expr # Not
	|
		/* Boolean and operator */
		left=expr AND right=expr # And
	|
		/* Boolean or operator */
		left=expr OR right=expr # Or
	|	
		/* If expression operator */
		argif=expr IF argcond=expr ELSE argelse=expr # If
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
		IN
		container=expr
		EOF # For
	;


/* Additional rules for "code" tag */

stmt
	: nn=nestedlvalue ASSIGN e=expr EOF
	/* Actually the assignment target in the following rules must be "lvalue" (i.e. Attribute, item or slices assigments) */
	| n=expr AUGADD e=expr EOF
	| n=expr AUGSUB e=expr EOF
	| n=expr AUGMUL e=expr EOF
	| n=expr AUGFLOORDIV e=expr EOF
	| n=expr AUGTRUEDIV e=expr EOF
	| n=expr AUGMOD e=expr EOF
	| n=expr AUGSHIFTLEFT e=expr EOF
	| n=expr AUGSHIFTRIGHT e=expr EOF
	| n=expr AUGAND e=expr EOF
	| n=expr AUGXOR e=expr EOF
	| n=expr AUGOR e=expr EOF
	| ex=expression EOF
	;


/* Used for parsing signatures */
signature
	:
		/* No parameters */
		open_=PARENS_OPEN
		close=PARENS_CLOSE # SignatureNoParams
	|
		/* "**" parameter only */
		open_=PARENS_OPEN
		'**' rkwargsname=name
		COMMA?
		close=PARENS_CLOSE # SignatureUnpackDictParams
	|
		/* "*" parameter only (and maybe **) */
		open_=PARENS_OPEN
		'*' rargsname=name
		(
			COMMA
			'**' rkwargsname=name
		)?
		COMMA?
		close=PARENS_CLOSE # SignatureUnpackParams
	|
		/* All parameters have a default */
		open_=PARENS_OPEN
		names+=name
		'='
		defaults+=exprarg
		(
			COMMA
			names+=name
			'='
			defaults+=exprarg
		)*
		(
			COMMA
			'*' rargsname=name
		)?
		(
			COMMA
			'**' rkwargsname=name
		)?
		COMMA?
		close=PARENS_CLOSE # SignatureDefaultParams
	|
		/* At least one parameter without a default */
		open_=PARENS_OPEN
		names_without_defaults+=name
		(
			COMMA
			names_without_defaults+=name
		)*
		(
			COMMA
			names_with_defaults+=name
			'='
			defaults+=exprarg
		)*
		(
			COMMA
			'*' rargsname=name
		)?
		(
			COMMA
			'**' rkwargsname=name
		)?
		COMMA?
		close=PARENS_CLOSE # SignatureAnyParams
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


/* Complete tags */
defblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_DEF
		definition
		ENDDELIM
		content=blockitem*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		DEF?
		ENDDELIM
	;

forblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_FOR
		var=nestedlvalue
		IN
		container=expr
		ENDDELIM
		content=blockitem*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		FOR?
		ENDDELIM
	;

whileblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WHILE
		cond=expr
		ENDDELIM
		content=blockitem*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		WHILE?
		ENDDELIM
	;

ifblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_IF
		cond=expr
		ENDDELIM
		content=blockitem*
		(
			(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
			MAYBETAG_ELIF
			cond=expr
			ENDDELIM
			content=blockitem*
		)*
		(
			(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
			MAYBETAG_ELSE
			ENDDELIM
			content=blockitem*
		)
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		IF?
		ENDDELIM
	;

renderblockblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_RENDERBLOCK
		e1=expr PARENS_OPEN ( args+=argument ( COMMA args+=argument )* COMMA? )* close=PARENS_CLOSE
		ENDDELIM
		content=blockitem*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		RENDERBLOCK?
		ENDDELIM
	;

renderblocksblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_RENDERBLOCKS
		e1=expr PARENS_OPEN ( args+=argument ( COMMA args+=argument )* COMMA? )* close=PARENS_CLOSE
		ENDDELIM
		content=blockitem*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		RENDERBLOCKS?
		ENDDELIM
	;

blockitem
	:
		(
			defblock
		|
			forblock
		|
			whileblock
		|
			ifblock
		)
	;

templatebodyitem
	:
		(
			whitespacetag
		|
			notetag
		|
			defblock
		|
			forblock
		|
			whileblock
		|
			ifblock
		) # TemplateBodyItem
	;
