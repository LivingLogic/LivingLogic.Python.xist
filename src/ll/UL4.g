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
def reportError(self, e):
	raise e

def mismatch(self, input, ttype, follow):
	raise MismatchedTokenException(ttype, input)

def recoverFromMismatchedSet(self, input, e, follow):
	raise e

def startpos(self, token):
	return self.tag.startposcode + token.start

def endpos(self, token):
	return self.tag.startposcode + token.stop + 1
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

STRING3
	: '"""' (options {greedy=false;}:TRIQUOTE)* '"""'
	|  '\'\'\'' (options {greedy=false;}:TRIAPOS)* '\'\'\''
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
	: NONE { $node = ul4c.Const(self.tag, self.startpos($NONE), self.endpos($NONE), None) }
	;

true_ returns [node]
	: TRUE { $node = ul4c.Const(self.tag, self.startpos($TRUE), self.endpos($TRUE), True) }
	;

false_ returns [node]
	: FALSE { $node = ul4c.Const(self.tag, self.startpos($FALSE), self.endpos($FALSE), False) }
	;

int_ returns [node]
	: INT { $node = ul4c.Const(self.tag, self.startpos($INT), self.endpos($INT), int($INT.text, 0)) }
	;

float_ returns [node]
	: FLOAT { $node = ul4c.Const(self.tag, self.startpos($FLOAT), self.endpos($FLOAT), float($FLOAT.text)) }
	;

string returns [node]
	: STRING { $node = ul4c.Const(self.tag, self.startpos($STRING), self.endpos($STRING), ast.literal_eval($STRING.text)) }
	| STRING3 { $node = ul4c.Const(self.tag, self.startpos($STRING3), self.endpos($STRING3), ast.literal_eval($STRING3.text.replace("\r", "\\r"))) }
	;

date returns [node]
	: DATE { $node = ul4c.Const(self.tag, self.startpos($DATE), self.endpos($DATE), datetime.datetime(*map(int, [f for f in ul4c._datesplitter.split($DATE.text[2:-1]) if f]))) }
	;

color returns [node]
	: COLOR { $node = ul4c.Const(self.tag, self.startpos($COLOR), self.endpos($COLOR), color.Color.fromrepr($COLOR.text)) }
	;

name returns [node]
	: NAME { $node = ul4c.Var(self.tag, self.startpos($NAME), self.endpos($NAME), $NAME.text) }
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
fragment
seqitem returns [node]
	:
		e=expr_if { $node = ul4c.SeqItem(self.tag, $e.node.startpos, $e.node.endpos, $e.node) }
	|
		star='*'
		es=expr_if { $node = ul4c.UnpackSeqItem(self.tag, self.startpos($star), $es.node.endpos, $es.node) }
	;

list returns [node]
	:
		open='['
		close=']' { $node = ul4c.List(self.tag, self.startpos($open), self.endpos($close)) }
	|
		open='[' {$node = ul4c.List(self.tag, self.startpos($open), None) }
		i1=seqitem { $node.items.append($i1.node) }
		(
			','
			i2=seqitem { $node.items.append($i2.node) }
		)*
		','?
		close=']' { $node.endpos = self.endpos($close) }
	;

listcomprehension returns [node]
	@init
	{
		_condition = None;
	}
	:
		open='['
		item=expr_if
		'for'
		n=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if { _condition = $condition.node; }
		)?
		close=']' { $node = ul4c.ListComp(self.tag, self.startpos($open), self.endpos($close), $item.node, $n.lvalue, $container.node, _condition) }
	;

/* Set literals */
set returns [node]
	:
		open='{'
		'/'
		close='}' { $node = ul4c.Set(self.tag, self.startpos($open), self.endpos($close)) }
	|
		open='{' {$node = ul4c.Set(self.tag, self.startpos($open), None) }
		i1=seqitem { $node.items.append($i1.node) }
		(
			','
			i2=seqitem { $node.items.append($i2.node) }
		)*
		','?
		close='}' { $node.endpos = self.endpos($close) }
	;

setcomprehension returns [node]
	@init
	{
		_condition = None;
	}
	:
		open='{'
		item=expr_if
		'for'
		n=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if { _condition = $condition.node; }
		)?
		close='}' { $node = ul4c.SetComp(self.tag, self.startpos($open), self.endpos($close), $item.node, $n.lvalue, $container.node, _condition) }
	;

/* Dict literal */
fragment
dictitem returns [node]
	:
		k=expr_if
		':'
		v=expr_if { $node = ul4c.DictItem(self.tag, $k.node.startpos, $v.node.startpos, $k.node, $v.node) }
	|
		star='**'
		e=expr_if { $node = ul4c.UnpackDictItem(self.tag, self.startpos($star), $e.node.endpos, $e.node) }
	;

dict returns [node]
	:
		open='{'
		close='}' { $node = ul4c.Dict(self.tag, self.startpos($open), self.endpos($close)) }
	|
		open='{' { $node = ul4c.Dict(self.tag, self.startpos($open), None) }
		i1=dictitem { $node.items.append($i1.node) }
		(
			','
			i2=dictitem { $node.items.append($i2.node) }
		)*
		','?
		close='}' { $node.endpos = self.endpos($close) }
	;

dictcomprehension returns [node]
	@init
	{
		_condition = None;
	}
	:
		open='{'
		key=expr_if
		':'
		value=expr_if
		'for'
		n=nestedlvalue
		'in'
		container=expr_if
		(
			'if'
			condition=expr_if { _condition = $condition.node; }
		)?
		close='}' { $node = ul4c.DictComp(self.tag, self.startpos($open), self.endpos($close), $key.node, $value.node, $n.lvalue, $container.node, _condition) }
	;

generatorexpression returns [node]
	@init
	{
		_condition = None
		_end = None
	}
	:
		item=expr_if { _start = $item.node.startpos }
		'for'
		n=nestedlvalue
		'in'
		container=expr_if { _end = $container.node.endpos }
		(
			'if'
			condition=expr_if { _condition = $condition.node; _end = $condition.node.endpos }
		)? { $node = ul4c.GenExpr(self.tag, $item.node.startpos, _end, $item.node, $n.lvalue, $container.node, _condition) }
	;

atom returns [node]
	: e_literal=literal { $node = $e_literal.node; }
	| e_list=list { $node = $e_list.node; }
	| e_listcomp=listcomprehension { $node = $e_listcomp.node; }
	| e_set=set { $node = $e_set.node; }
	| e_setcomp=setcomprehension { $node = $e_setcomp.node; }
	| e_dict=dict { $node = $e_dict.node; }
	| e_dictcomp=dictcomprehension { $node = $e_dictcomp.node; }
	| open='(' e_genexpr=generatorexpression close=')' {
		$node = $e_genexpr.node
		$node.startpos = self.startpos($open)
		$node.endpos = self.endpos($close)
	}
	| open='(' e_bracket=expr_if close=')' {
		$node = $e_bracket.node
		$node.startpos = self.startpos($open)
		$node.endpos = self.endpos($close)
	}
	;

/* For variable unpacking in assignments and for loops */
nestedlvalue returns [lvalue]
	:
		n=expr_subscript { $lvalue = $n.node; }
	|
		'(' n0=nestedlvalue ',' ')' { $lvalue = ($n0.lvalue,) }
	|
		'('
		n1=nestedlvalue
		','
		n2=nestedlvalue { $lvalue = ($n1.lvalue, $n2.lvalue) }
		(
			','
			n3=nestedlvalue { $lvalue += ($n3.lvalue,) }
		)*
		','?
		')'
	;

/* Slice expression */
slice returns [node]
	@init
	{
		index1 = None
		index2 = None
		startpos = None
		endpos = None
	}
	:
		(
			e1=expr_if { index1 = $e1.node; startpos = $e1.node.startpos; }
		)?
		colon=':' {
			if startpos is None:
				startpos = self.startpos($colon)
			endpos = self.endpos($colon)
		}
		(
			e2=expr_if { index2 = $e2.node; endpos = $e2.node.endpos; }
		)? { $node = ul4c.Slice(self.tag, startpos, endpos, index1, index2) }
	;

/* Function/method call, attribute access, item access, slice access */
fragment
argument returns [node]
	:
		e=exprarg { $node = ul4c.PosArg(self.tag, $e.node.startpos, $e.node.endpos, $e.node) }
	|
		en=name '=' ev=exprarg { $node = ul4c.KeywordArg(self.tag, $en.node.startpos, $ev.node.endpos, $en.text, $ev.node) }
	|
		star='*'
		es=exprarg { $node = ul4c.UnpackListArg(self.tag, self.startpos($star), $es.node.endpos, $es.node) }
	|
		star='**'
		es=exprarg { $node = ul4c.UnpackDictArg(self.tag, self.startpos($star), $es.node.endpos, $es.node) }
	;

expr_subscript returns [node]
	:
		e1=atom { $node = $e1.node; }
		(
			/* Attribute access */
			'.'
			n=name { $node = ul4c.Attr(self.tag, $node.startpos, self.endpos($n.stop), $node, $n.text) }
		|
			/* Function/method call */
			'(' { $node = ul4c.Call(self.tag, $node.startpos, None, $node) }
			(
				a1=argument { $a1.node.append($node) }
				(
					','
					a2=argument { $a2.node.append($node) }
				)*
				','?
			)*
			close=')' { $node.endpos = self.endpos($close) }
		|
			/* Item access */
			'['
				e2=expr_if
			close=']' { $node = ul4c.Item(self.tag, $e1.node.startpos, self.endpos($close), $node, $e2.node) }
		|
			/* Slice access */
			'['
				e2=slice
			close=']' { $node = ul4c.Item(self.tag, $e1.node.startpos, self.endpos($close), $node, $e2.node) }
		)*
	;

/* Negation/bitwise not */
expr_unary returns [node]
	:
		e1=expr_subscript { $node = $e1.node; }
	|
		minus='-' e2=expr_unary { $node = ul4c.Neg.make(self.tag, self.startpos($minus), $e2.node.endpos, $e2.node) }
	|
		bitnot='~' e2=expr_unary { $node = ul4c.BitNot.make(self.tag, self.startpos($bitnot), $e2.node.endpos, $e2.node) }
	;


/* Multiplication, division, modulo */
expr_mul returns [node]
	:
		e1=expr_unary { $node = $e1.node; }
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
			e2=expr_unary { $node = cls.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Addition, substraction */
expr_add returns [node]
	:
		e1=expr_mul { $node = $e1.node; }
		(
			(
				'+' { cls = ul4c.Add; }
			|
				'-' { cls = ul4c.Sub; }
			)
			e2=expr_mul { $node = cls.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Binary shift */
expr_bitshift returns [node]
	:
		e1=expr_add { $node = $e1.node; }
		(
			(
				'<<' { cls = ul4c.ShiftLeft; }
			|
				'>>' { cls = ul4c.ShiftRight; }
			)
			e2=expr_add { $node = cls.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Bitwise and */
expr_bitand returns [node]
	:
		e1=expr_bitshift { $node = $e1.node; }
		(
			'&'
			e2=expr_bitshift { $node = ul4c.BitAnd.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Bitwise exclusive or */
expr_bitxor returns [node]
	:
		e1=expr_bitand { $node = $e1.node; }
		(
			'^'
			e2=expr_bitand { $node = ul4c.BitXOr.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Bitwise or */
expr_bitor returns [node]
	:
		e1=expr_bitxor { $node = $e1.node; }
		(
			'|'
			e2=expr_bitxor { $node = ul4c.BitOr.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Comparisons */
expr_cmp returns [node]
	:
		e1=expr_bitor { $node = $e1.node; }
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
			|
				'in' { cls = ul4c.Contains; }
			|
				'not' 'in' { cls = ul4c.NotContains; }
			|
				'is' { cls = ul4c.Is; }
			|
				'is' 'not' { cls = ul4c.IsNot; }
			)
			e2=expr_bitor { $node = cls.make(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Boolean not */
expr_not returns [node]
	:
		e1=expr_cmp { $node = $e1.node; }
	|
		n='not' e2=expr_not { $node = ul4c.Not.make(self.tag, self.startpos($n), $e2.node.endpos, $e2.node) }
	;


/* And operator */
expr_and returns [node]
	:
		e1=expr_not { $node = $e1.node; }
		(
			'and'
			e2=expr_not { $node = ul4c.And(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* Or operator */
expr_or returns [node]
	:
		e1=expr_and { $node = $e1.node; }
		(
			'or'
			e2=expr_and { $node = ul4c.Or(self.tag, $node.startpos, $e2.node.endpos, $node, $e2.node) }
		)*
	;

/* If expression operator */
expr_if returns [node]
	:
		e1=expr_or { $node = $e1.node; }
		(
			'if'
			e2=expr_or
			'else'
			e3=expr_or { $node = ul4c.If.make(self.tag, $e1.node.startpos, $e3.node.endpos, $node, $e2.node, $e3.node); }
		)?
	;

exprarg returns [node]
	: ege=generatorexpression { $node = $ege.node; }
	| e1=expr_if { $node = $e1.node; }
	;

expression returns [node]
	: ege=generatorexpression EOF { $node = $ege.node; }
	| e=expr_if EOF { $node = $e.node; }
	;


/* Additional rules for "for" tag */

for_ returns [node]
	:
		n=nestedlvalue
		'in'
		e=expr_if { $node = ul4c.ForBlock(self.tag, self.startpos($n.start), $e.node.endpos, $n.lvalue, $e.node) }
		EOF
	;


/* Additional rules for "code" tag */

statement returns [node]
	: nn=nestedlvalue '=' e=expr_if EOF { $node = ul4c.SetVar(self.tag, self.startpos($nn.start), $e.node.endpos, $nn.lvalue, $e.node) }
	| n=expr_subscript '+=' e=expr_if EOF { $node = ul4c.AddVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '-=' e=expr_if EOF { $node = ul4c.SubVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '*=' e=expr_if EOF { $node = ul4c.MulVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '/=' e=expr_if EOF { $node = ul4c.TrueDivVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '//=' e=expr_if EOF { $node = ul4c.FloorDivVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '%=' e=expr_if EOF { $node = ul4c.ModVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '<<=' e=expr_if EOF { $node = ul4c.ShiftLeftVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '>>=' e=expr_if EOF { $node = ul4c.ShiftRightVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '&=' e=expr_if EOF { $node = ul4c.BitAndVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '^=' e=expr_if EOF { $node = ul4c.BitXOrVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| n=expr_subscript '|=' e=expr_if EOF { $node = ul4c.BitOrVar(self.tag, self.startpos($n.start), $e.node.endpos, $n.node, $e.node) }
	| e=expression EOF { $node = $e.node }
	;


/* Additional rules for "def" and "ul4" tag */

definition returns [node]
	:
		{ $node = (None, None); }
		(
			n=name { $node = ($n.text, None); }
		)?
		(
			sig=signature { $node = ($node[0], $signature.node); }
		)?
		EOF
	;


/* Used for parsing signatures */
signature returns [node]
	:
	open='(' { $node = ul4c.Signature(self.tag, self.startpos($open), None) }
	(
		/* No parameters */
	|
		/* "**" parameter only */
		'**' rkwargsname=name { $node.params.append(("**" + $rkwargsname.text, None)); }
		','?
	|
		/* "*" parameter only (and maybe **) */
		'*' rargsname=name { $node.params.append(("*" + $rargsname.text, None)); }
		(
			','
			'**' rkwargsname=name { $node.params.append(("**" + $rkwargsname.text, None)); }
		)?
		','?
	|
		/* All parameters have a default */
		aname1=name
		'='
		adefault1=exprarg { $node.params.append(($aname1.text, $adefault1.node)); }
		(
			','
			aname2=name
			'='
			adefault2=exprarg { $node.params.append(($aname2.text, $adefault2.node)); }
		)*
		(
			','
			'*' rargsname=name { $node.params.append(("*" + $rargsname.text, None)); }
		)?
		(
			','
			'**' rkwargsname=name { $node.params.append(("**" + $rkwargsname.text, None)); }
		)?
		','?
	|
		/* At least one parameter without a default */
		aname1=name { $node.params.append(($aname1.text, None)); }
		(
			','
			aname2=name { $node.params.append(($aname2.text, None)); }
		)*
		(
			','
			aname3=name
			'='
			adefault3=exprarg { $node.params.append(($aname3.text, $adefault3.node)); }
		)*
		(
			','
			'*' rargsname=name { $node.params.append(("*" + $rargsname.text, None)); }
		)?
		(
			','
			'**' rkwargsname=name { $node.params.append(("**" + $rkwargsname.text, None)); }
		)?
		','?
	)
	close=')' { $node.endpos = self.endpos($close) }
	EOF
;
