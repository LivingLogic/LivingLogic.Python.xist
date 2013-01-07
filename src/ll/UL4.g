grammar UL4;

options
{
	language=Python;
	backtrack=true;
}

@lexer::header
{
    from ll import ul4c
}

@header
{
    import datetime, ast
    from ll import ul4c, color
}

@lexer::members {
def reportError(self, e):
   raise e
}

@members {
def mismatch(self, input, ttype, follow):
    raise MismatchedTokenException(ttype, input)

def recoverFromMismatchedSet(self, input, e, follow):
    raise e
}

@rulecatch {
except RecognitionException as e:
    raise
}

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

/* We don't have negative ints (as this would lex "1-2" wrong) */
INT
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
	: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ('T' TIME?)? ')';

COLOR
	: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	| '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
	;

WS
	: (' '|'\t'|'\r'|'\n') { $channel=HIDDEN; }
	;

STRING
	: '"' ( ESC_SEQ | ~('\\'|'"'|'\r'|'\n') )* '"'
	| '\'' ( ESC_SEQ | ~('\\'|'\''|'\r'|'\n') )* '\''
	;

fragment
ESC_SEQ
	: '\\' ('a'|'b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
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

none returns [node]
	: NONE { $node = ul4c.Const(None); }
	;

true_ returns [node]
	: TRUE { $node = ul4c.Const(True); }
	;

false_ returns [node]
	: FALSE { $node = ul4c.Const(False); }
	;

int_ returns [node]
	: INT { $node = ul4c.Const(int($INT.text, 0)); }
	;

float_ returns [node]
	: FLOAT { $node = ul4c.Const(float($FLOAT.text)); }
	;

string returns [node]
	: STRING { $node = ul4c.Const(ast.literal_eval($STRING.text)); }
	;

date returns [node]
	: DATE { $node = ul4c.Const(datetime.datetime(*map(int, [f for f in ul4c.datesplitter.split($DATE.text[2:-1]) if f]))); }
	;

color returns [node]
	: COLOR { $node = ul4c.Const(color.Color.fromrepr($COLOR.text)); }
	;

name returns [node]
	: NAME { $node = ul4c.Var($NAME.text); }
	;

literal returns [node]
	: e_none=none { $node = $e_none.node; }
	| e_false=false_ { $node = $e_false.node; }
	| e_true=true_ { $node = $e_true.node; }
	| e_int=int_ { $node = $e_int.node; }
	| e_float=float_ { $node = $e_float.node; }
	| e_string=string { $node = $e_string.node; }
	| e_date=date { $node = $e_date.node; }
	| e_color=color { $node = $e_color.node; }
	| e_name=name { $node = $e_name.node; }
	;

/* List literals */
list returns [node]
	:
		'['
		']' { $node = ul4c.List(); }
	|
		'[' {$node = ul4c.List(); }
		e1=expr1 { $node.items.append($e1.node); }
		(
			','
			e2=expr1 { $node.items.append($e2.node); }
		)*
		','?
		']'
	;

listcomprehension returns [node]
	@init
	{
		_condition = None;
	}
	:
		'['
		item=expr1
		'for'
		n=nestedname
		'in'
		container=expr1
		(
			'if'
			condition=expr1 { _condition = $condition.node; }
		)?
		']' { $node = ul4c.ListComp($item.node, $n.varname, $container.node, _condition); }
	;

/* Dict literal */
fragment
dictitem returns [node]
	:
		k=expr1
		':'
		v=expr1 { $node = ($k.node, $v.node); }
	|
		'**'
		d=expr1 { $node = ($d.node,); }
	;

dict returns [node]
	:
		'{'
		'}' { $node = ul4c.Dict(); }
	|
		'{' { $node = ul4c.Dict(); }
		i1=dictitem { $node.items.append($i1.node); }
		(
			','
			i2=dictitem { $node.items.append($i2.node); }
		)*
		','?
		'}'
	;

dictcomprehension returns [node]
	@init
	{
		_condition = None;
	}
	:
		'{'
		key=expr1
		':'
		value=expr1
		'for'
		n=nestedname
		'in'
		container=expr1
		(
			'if'
			condition=expr1 { _condition = $condition.node; }
		)?
		'}' { $node = ul4c.DictComp($key.node, $value.node, $n.varname, $container.node, _condition); }
	;

generatorexpression returns [node]
	@init
	{
		_condition = None;
	}
	:
		item=expr1
		'for'
		n=nestedname
		'in'
		container=expr1
		(
			'if'
			condition=expr1 { _condition = $condition.node; }
		)? { $node = ul4c.GenExpr($item.node, $n.varname, $container.node, _condition); }
	;

atom returns [node]
	: e_literal=literal { $node = $e_literal.node; }
	| e_list=list { $node = $e_list.node; }
	| e_listcomp=listcomprehension { $node = $e_listcomp.node; }
	| e_dict=dict { $node = $e_dict.node; }
	| e_dictcomp=dictcomprehension { $node = $e_dictcomp.node; }
	| '(' e_genexpr=generatorexpression ')' { $node = $e_genexpr.node; }
	| '(' e_bracket=expr1 ')' { $node = $e_bracket.node; }
	;

/* For variable unpacking in assignments and for loops */
nestedname returns [varname]
	:
		n=name { $varname = $n.text; }
	|
		'(' n0=nestedname ',' ')' { $varname = ($n0.varname,); }
	|
		'('
		n1=nestedname
		','
		n2=nestedname { $varname = ($n1.varname, $n2.varname); }
		(
			','
			n3=nestedname { $varname += ($n3.varname,); }
		)*
		','?
		')' 
	;

/* Function call */
expr10 returns [node]
	: a=atom { $node = $a.node; }
	|
		n=name
		'(' { $node = ul4c.CallFunc($n.text); }
		(
			/* No arguments */
		|
			/* "**" argument only */
			'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
			','?
		|
			/* "*" argument only (and maybe **) */
			'*' rargs=exprarg { $node.remargs = $rargs.node; }
			(
				','
				'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
			)?
			','?
		|
			/* At least one positional argument */
			a1=exprarg { $node.args.append($a1.node); }
			(
				','
				a2=exprarg { $node.args.append($a2.node); }
			)*
			(
				','
				an3=name '=' av3=exprarg { $node.kwargs.append(($an3.text, $av3.node)); }
			)*
			(
				','
				'*' rargs=exprarg { $node.remargs = $rargs.node; }
			)?
			(
				','
				'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
			)?
			','?
		|
			/* Keyword arguments only */
			an1=name '=' av1=exprarg { $node.kwargs.append(($an1.text, $av1.node)); }
			(
				','
				an2=name '=' av2=exprarg { $node.kwargs.append(($an2.text, $av2.node)); }
			)*
			(
				','
				'*' rargs=exprarg { $node.remargs = $rargs.node; }
			)?
			(
				','
				'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
			)?
			','?
		)
		')' 
	;

/* Attribute access, method call, item access, slice access */
expr9 returns [node]
	@init
	{
		callmeth = False
		index1 = None
		index2 = None
		slice = False
	}
	:
		e1=expr10 { $node = $e1.node; }
		(
			/* Attribute access/method call */
			'.'
			n=name
			(
				/* Method call */
				'(' { callmeth = True; $node = ul4c.CallMeth($n.text, $node); }
				(
					/* No arguments */
				|
					/* "**" argument only */
					'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
					','?
				|
					/* "*" argument only (and maybe **) */
					'*' rargs=exprarg { $node.remargs = $rargs.node; }
					(
						','
						'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
					)?
					','?
				|
					/* At least one positional argument */
					a1=exprarg { $node.args.append($a1.node); }
					(
						','
						a2=exprarg { $node.args.append($a2.node); }
					)*
					(
						','
						an3=name '=' av3=exprarg { $node.kwargs.append(($an3.text, $av3.node)); }
					)*
					(
						','
						'*' rargs=exprarg { $node.remargs = $rargs.node; }
					)?
					(
						','
						'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
					)?
					','?
				|
					/* Keyword arguments only */
					an1=name '=' av1=exprarg { $node.kwargs.append(($an1.text, $av1.node)); }
					(
						','
						an2=name '=' av2=exprarg { $node.kwargs.append(($an2.text, $av2.node)); }
					)*
					(
						','
						'*' rargs=exprarg { $node.remargs = $rargs.node; }
					)?
					(
						','
						'**' rkwargs=exprarg { $node.remkwargs = $rkwargs.node; }
					)?
					','?
				)
				')'
			)? {
				if not callmeth:
					$node = ul4c.GetAttr($node, $n.text);
			}
		|
			/* Item/slice access */
			'['
			(
				':'
				(
					e2=expr1 { index2 = $e2.node; }
				)? { $node = ul4c.GetSlice($node, None, index2); }
			|
				e2=expr1 { index1 = $e2.node; }
				(
					':' { slice = True; }
					(
						e3=expr1 { index2 = $e3.node; }
					)?
				)? { $node = ul4c.GetSlice($node, index1, index2) if slice else ul4c.GetItem($node, index1); }
			)
			']'
		)*
	;

/* Negation */
expr8 returns [node]
	@init
	{
		count = 0;
	}
	:
		(
			'-' { count += 1; }
		)*
		e=expr9 {
			$node = $e.node;
			for i in range(count):
				$node = ul4c.Neg.make($node);
		}
	;

/* Multiplication, division, modulo */
expr7 returns [node]
	:
		e1=expr8 { $node = $e1.node; }
		(
			(
				'*' { cls = ul4c.Mul; }
			|
				'/' { cls = ul4c.TrueDiv; }
			|
				'//' { cls = ul4c.FloorDiv; }
			|
				'%' { cls = ul4c.Mod; }
			)
			e2=expr8 { $node = cls.make($node, $e2.node); }
		)*
	;

/* Addition, substraction */
expr6 returns [node]
	:
		e1=expr7 { $node = $e1.node; }
		(
			(
				'+' { cls = ul4c.Add; }
			|
				'-' { cls = ul4c.Sub; }
			)
			e2=expr7 { $node = cls.make($node, $e2.node) }
		)*
	;

/* Comparisons */
expr5 returns [node]
	:
		e1=expr6 { $node = $e1.node; }
		(
			(
				'==' { cls = ul4c.EQ; }
			|
				'!=' { cls = ul4c.NE; }
			|
				'<' { cls = ul4c.LT; }
			|
				'<=' { cls = ul4c.LE; }
			|
				'>' { cls = ul4c.GT; }
			|
				'>=' { cls = ul4c.GE; }
			)
			e2=expr6 { $node = cls.make($node, $e2.node); }
		)*
	;

/* "in"/"not in" operator */
expr4 returns [node]
	:
		e1=expr5 { $node = $e1.node; }
		(
			{ cls = ul4c.Contains; }
			(
				'not' { cls = ul4c.NotContains; }
			)?
			'in'
			e2=expr5 { $node = cls.make($node, $e2.node); }
		)?
	;

/* Not operator */
expr3 returns [node]
	:
		'not'
		e=expr4 { $node = ul4c.Not.make($e.node); }
	|
		e=expr4 { $node = $e.node; }
	;


/* And operator */
expr2 returns [node]
	:
		e1=expr3 { $node = $e1.node; }
		(
			'and'
			e2=expr3 { $node = ul4c.And.make($node, $e2.node); }
		)*
	;

/* Or operator */
expr1 returns [node]
	:
		e1=expr2 { $node = $e1.node; }
		(
			'or'
			e2=expr2 { $node = ul4c.Or.make($node, $e2.node); }
		)*
	;

exprarg returns [node]
	: ege=generatorexpression { $node = $ege.node; }
	| e1=expr1 { $node = $e1.node; }
	;

expression returns [node]
	: ege=generatorexpression EOF { $node = $ege.node; }
	| e=expr1 EOF { $node = $e.node; }
	;


/* Additional rules for "for" tag */

for_ returns [node]
	:
		n=nestedname
		'in'
		e=expr1 { $node = ul4c.For(self.location, $n.varname, $e.node); }
		EOF
	;


/* Additional rules for "code" tag */

statement returns [node]
	: nn=nestedname '=' e=expr1 EOF { $node = ul4c.StoreVar(self.location, $nn.varname, $e.node); }
	| n=name '+=' e=expr1 EOF { $node = ul4c.AddVar(self.location, $n.text, $e.node); }
	| n=name '-=' e=expr1 EOF { $node = ul4c.SubVar(self.location, $n.text, $e.node); }
	| n=name '*=' e=expr1 EOF { $node = ul4c.MulVar(self.location, $n.text, $e.node); }
	| n=name '/=' e=expr1 EOF { $node = ul4c.TrueDivVar(self.location, $n.text, $e.node); }
	| n=name '//=' e=expr1 EOF { $node = ul4c.FloorDivVar(self.location, $n.text, $e.node); }
	| n=name '%=' e=expr1 EOF { $node = ul4c.ModVar(self.location, $n.text, $e.node); }
	;
