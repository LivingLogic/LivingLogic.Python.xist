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
		content+=template_content*
		EOF # TopLevel
	;

ul4tag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_UL4
		MAYBETAG_WS*
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
		MAYBETAG_WS*
		MAYBETAG_WHITESPACE
		WHITESPACE_WS*
		whitespace=WHITESPACE_VALUE
		WHITESPACE_WS*
		WHITESPACE_ENDDELIM # TagWhitespace
	;

doctag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_DOC
		MAYBETAG_WS*
		texttag_content?
		TEXTTAG_WS*
		TEXTTAG_ENDDELIM
	;

notetag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_NOTE
		MAYBETAG_WS*
		texttag_content?
		TEXTTAG_WS?
		TEXTTAG_ENDDELIM
	;

texttag_content
	:
		~TEXTTAG_WS
	|
		~TEXTTAG_WS
		TEXTTAG_TEXT*
		~TEXTTAG_WS
	;

indent
	:
		DEFAULT_INDENT+
	;

text
	:
		DEFAULT_OTHER+
	|
		TEXT_OTHER+
	;

lineend
	:
		DEFAULT_LINEEND
	|
		TEXT_LINEEND
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
	: nn=nestedlvalue ASSIGN e=expr
	| n=lexpr AUGADD e=expr
	| n=lexpr AUGSUB e=expr
	| n=lexpr AUGMUL e=expr
	| n=lexpr AUGFLOORDIV e=expr
	| n=lexpr AUGTRUEDIV e=expr
	| n=lexpr AUGMOD e=expr
	| n=lexpr AUGSHIFTLEFT e=expr
	| n=lexpr AUGSHIFTRIGHT e=expr
	| n=lexpr AUGAND e=expr
	| n=lexpr AUGXOR e=expr
	| n=lexpr AUGOR e=expr
	| ex=expression
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
	;


/* Complete tags */
defblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_DEF
		definition
		ENDDELIM
		content=block_content*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		DEF?
		ENDDELIM
	;

forblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_FOR
		MAYBETAG_WS*
		var=nestedlvalue
		IN
		container=expr
		ENDDELIM
		content=block_content*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_END
		MAYBETAG_WS*
		FOR?
		MAYBETAG_WS*
		ENDDELIM
	;

whileblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WHILE
		cond=expr
		ENDDELIM
		content=block_content*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_END
		MAYBETAG_WS*
		WHILE?
		MAYBETAG_WS*
		ENDDELIM
	;

ifblock
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_IF
		cond=expr
		ENDDELIM
		content=block_content*
		(
			(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
			MAYBETAG_ELIF
			cond=expr
			ENDDELIM
			content=block_content*
		)*
		(
			(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
			MAYBETAG_ELSE
			ENDDELIM
			content=block_content*
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
		content=block_content*
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
		content=block_content*
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_END
		RENDERBLOCKS?
		ENDDELIM
	;

printtag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_PRINT
		TEXTTAG_WS*
		expr
		TEXTTAG_WS*
		ENDDELIM
	;

printxtag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_PRINTX
		TEXTTAG_WS*
		expr
		TEXTTAG_WS*
		ENDDELIM
	;

codetag
	:
		(DEFAULT_MAYBETAG|TEXT_MAYBETAG)
		MAYBETAG_WS*
		MAYBETAG_CODE
		TEXTTAG_WS*
		stmt
		TEXTTAG_WS*
		ENDDELIM
	;


block_content
	:
		(
			defblock
		|
			forblock
		|
			whileblock
		|
			ifblock
		|
			printtag
		|
			printxtag
		|
			codetag
		|
			indent
		|
			text
		|
			lineend
		)
	;

template_content
	:
		(
			whitespacetag
		|
			doctag
		|
			notetag
		|
			block_content
		) # Template_content2
	;

/* Rules common to all tags */

name
	: NAME
	;

none_literal
	:
		value=NONE
	;

bool_literal
	:
		value=FALSE # BoolLiteralFalse
	|
		value=TRUE # BoolLiteralTrue
	;

integer_literal
	:
		value=INT # IntegerLiteral
	;

float_literal
	:
		value=FLOAT # FloatLiteral
	;

string_literal
	:
		value=STRING
	|
		value=STRING3
	;

date_literal
	:
		value=DATE
	;

datetime_literal
	:
		value=DATE
	;

color_literal
	:
		value=COLOR
	;

literal
	: none_literal # LiteralNone
	| bool_literal # LiteralBool
	| integer_literal # LiteralInteger
	| float_literal # LiteralFloat
	| string_literal # LiteralString
	| date_literal # LiteralDate
	| datetime_literal # LiteralDatetime
	| color_literal # LiteralColor
	;

/* List literals */
seqitem
	:
		item=expr # SeqItem2
	|
		star=STAR
		unpackitem=expr # UnpackSeqItem
	;

list_display
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
		close=BRACKET_CLOSE # Listcomprehension2
	;

/* Set literals */
set_display
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
		close=BRACE_CLOSE # Setcomprehension2
	;

/* Dict literal */
dictitem
	:
		key=expr
		':'
		value=expr # Dictitem2
	|
		star='**'
		unpackitem=expr # UnpackDictItem
	;

dict_display
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
		close=BRACE_CLOSE # Dictcomprehension2
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
	: arg=name # AtomName
	| arg=literal # AtomLiteral
	| arg=list_display # AtomList
	| arg=listcomprehension # AtomListComprehension
	| arg=set_display # AtomSet
	| arg=setcomprehension # AtomSetComprehension
	| arg=dict_display # AtomDict
	| arg=dictcomprehension  # AtomDictComprehension
	| PARENS_OPEN arg=generatorexpression PARENS_CLOSE # AtomGeneratorExpression
	| PARENS_OPEN arg=expr PARENS_CLOSE # AtomBracket
	;

/* For variable unpacking in assignments and for loops */
nestedlvalue
	:
		lvalue=lexpr # LValueSimple
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

lexpr
	:
		e=name # LValueVar
	|
		/* Attribute access */
		e1=expr DOT n=name # LValueAttr
	|
		/* Item access */
		e1=expr BRACKET_OPEN index=expr close=BRACKET_CLOSE # LValueItem
	|
		/* Slice access */
		e1=expr BRACKET_OPEN index=slice_ close=BRACKET_CLOSE # LValueItemSlice
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
