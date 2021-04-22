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

def pos(self, token):
	return slice(self.tag.codepos.start + token.start, self.tag.codepos.start + token.stop + 1)
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

/* We don't have negative ints (as this would tokenize "1-2" wrong) */
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
	: NONE { $node = ul4c.ConstAST(self.tag.template, self.pos($NONE), None) }
	;

true_ returns [node]
	: TRUE { $node = ul4c.ConstAST(self.tag.template, self.pos($TRUE), True) }
	;

false_ returns [node]
	: FALSE { $node = ul4c.ConstAST(self.tag.template, self.pos($FALSE), False) }
	;

int_ returns [node]
	: INT { $node = ul4c.ConstAST(self.tag.template, self.pos($INT), int($INT.text, 0)) }
	;

float_ returns [node]
	: FLOAT { $node = ul4c.ConstAST(self.tag.template, self.pos($FLOAT), float($FLOAT.text)) }
	;

string returns [node]
	: STRING { $node = ul4c.ConstAST(self.tag.template, self.pos($STRING), ast.literal_eval($STRING.text)) }
	| STRING3 { $node = ul4c.ConstAST(self.tag.template, self.pos($STRING3), ast.literal_eval($STRING3.text.replace("\r", "\\r"))) }
	;

date returns [node]
	: DATE { $node = ul4c.ConstAST(self.tag.template, self.pos($DATE), datetime.date(*map(int, [f for f in ul4c._datesplitter.split($DATE.text[2:-1]) if f]))) }
	;

datetime returns [node]
	: DATETIME { $node = ul4c.ConstAST(self.tag.template, self.pos($DATETIME), datetime.datetime(*map(int, [f for f in ul4c._datesplitter.split($DATETIME.text[2:-1]) if f]))) }
	;

color returns [node]
	: COLOR { $node = ul4c.ConstAST(self.tag.template, self.pos($COLOR), color.Color.fromrepr($COLOR.text)) }
	;

name returns [node]
	: NAME { $node = ul4c.VarAST(self.tag.template, self.pos($NAME), $NAME.text) }
	;

literal returns [node]
	: e_none=none { $node = $e_none.node; }
	| e_false=false_ { $node = $e_false.node; }
	| e_true=true_ { $node = $e_true.node; }
	| e_int=int_ { $node = $e_int.node; }
	| e_float=float_ { $node = $e_float.node; }
	| e_string=string { $node = $e_string.node; }
	| e_date=date { $node = $e_date.node; }
	| e_datetime=datetime { $node = $e_datetime.node; }
	| e_color=color { $node = $e_color.node; }
	| e_name=name { $node = $e_name.node; }
	;

/* List literals */
fragment
seqitem returns [node]
	:
		e=expr_if { $node = ul4c.SeqItemAST(self.tag.template, $e.node._startpos, $e.node) }
	|
		star='*'
		es=expr_if { $node = ul4c.UnpackSeqItemAST(self.tag.template, slice(self.pos($star).start, $es.node._startpos.stop), $es.node) }
	;

list returns [node]
	:
		open='['
		close=']' { $node = ul4c.ListAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop)) }
	|
		open='[' {$node = ul4c.ListAST(self.tag.template, slice(self.pos($open).start, None)) }
		i1=seqitem { $node.items.append($i1.node) }
		(
			','
			i2=seqitem { $node.items.append($i2.node) }
		)*
		','?
		close=']' { $node.startpos = slice($node._startpos.start, self.pos($close).stop) }
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
		close=']' { $node = ul4c.ListComprehensionAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop), $item.node, $n.lvalue, $container.node, _condition) }
	;

/* Set literals */
set returns [node]
	:
		open='{'
		'/'
		close='}' { $node = ul4c.SetAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop)) }
	|
		open='{' {$node = ul4c.SetAST(self.tag.template, slice(self.pos($open).start, None)) }
		i1=seqitem { $node.items.append($i1.node) }
		(
			','
			i2=seqitem { $node.items.append($i2.node) }
		)*
		','?
		close='}' { $node.startpos = slice($node._startpos.start, self.pos($close).stop) }
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
		close='}' { $node = ul4c.SetComprehensionAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop), $item.node, $n.lvalue, $container.node, _condition) }
	;

/* Dict literal */
fragment
dictitem returns [node]
	:
		k=expr_if
		':'
		v=expr_if { $node = ul4c.DictItemAST(self.tag.template, slice($k.node._startpos.start, $v.node._startpos.start), $k.node, $v.node) }
	|
		star='**'
		e=expr_if { $node = ul4c.UnpackDictItemAST(self.tag.template, slice(self.pos($star).start, $e.node._startpos.stop), $e.node) }
	;

dict returns [node]
	:
		open='{'
		close='}' { $node = ul4c.DictAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop)) }
	|
		open='{' { $node = ul4c.DictAST(self.tag.template, slice(self.pos($open).start, None)) }
		i1=dictitem { $node.items.append($i1.node) }
		(
			','
			i2=dictitem { $node.items.append($i2.node) }
		)*
		','?
		close='}' { $node.startpos = slice($node._startpos.start, self.pos($close).stop) }
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
		close='}' { $node = ul4c.DictComprehensionAST(self.tag.template, slice(self.pos($open).start, self.pos($close).stop), $key.node, $value.node, $n.lvalue, $container.node, _condition) }
	;

generatorexpression returns [node]
	@init
	{
		_condition = None
		_stop = None
	}
	:
		item=expr_if { _start = $item.node._startpos.start }
		'for'
		n=nestedlvalue
		'in'
		container=expr_if { _stop = $container.node._startpos.stop }
		(
			'if'
			condition=expr_if { _condition = $condition.node; _stop = $condition.node._startpos.stop }
		)? { $node = ul4c.GeneratorExpressionAST(self.tag.template, slice($item.node._startpos.start, _stop), $item.node, $n.lvalue, $container.node, _condition) }
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
		$node.startpos = slice(self.pos($open).start, self.pos($close).stop)
	}
	| open='(' e_bracket=expr_if close=')' {
		$node = $e_bracket.node
		$node.startpos = slice(self.pos($open).start, self.pos($close).stop)
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
		stoppos = None
	}
	:
		(
			e1=expr_if { index1 = $e1.node; startpos = $e1.node._startpos.start; }
		)?
		colon=':' {
			pos = self.pos($colon)
			if startpos is None:
				startpos = pos.start
			stoppos = pos.stop
		}
		(
			e2=expr_if { index2 = $e2.node; stoppos = $e2.node._startpos.stop; }
		)? { $node = ul4c.SliceAST(self.tag.template, slice(startpos, stoppos), index1, index2) }
	;

/* Function/method call, attribute access, item access, slice access */
fragment
argument returns [node]
	:
		e=exprarg { $node = ul4c.PositionalArgumentAST(self.tag.template, $e.node._startpos, $e.node) }
	|
		en=name '=' ev=exprarg { $node = ul4c.KeywordArgumentAST(self.tag.template, slice($en.node._startpos.start, $ev.node._startpos.stop), $en.text, $ev.node) }
	|
		star='*'
		es=exprarg { $node = ul4c.UnpackListArgumentAST(self.tag.template, slice(self.pos($star).start, $es.node._startpos.stop), $es.node) }
	|
		star='**'
		es=exprarg { $node = ul4c.UnpackDictArgumentAST(self.tag.template, slice(self.pos($star).start, $es.node._startpos.stop), $es.node) }
	;

expr_subscript returns [node]
	:
		e1=atom { $node = $e1.node; }
		(
			/* Attribute access */
			'.'
			n=name { $node = ul4c.AttrAST(self.tag.template, slice($node._startpos.start, self.pos($n.stop).stop), $node, $n.text) }
		|
			/* Function/method call */
			'(' { $node = ul4c.CallAST(self.tag.template, slice($node._startpos.start, None), $node) }
			(
				a1=argument { $a1.node.append($node) }
				(
					','
					a2=argument { $a2.node.append($node) }
				)*
				','?
			)*
			close=')' { $node.startpos = slice($node._startpos.start, self.pos($close).stop) }
		|
			/* Item access */
			'['
				e2=expr_if
			close=']' { $node = ul4c.ItemAST(self.tag.template, slice($e1.node._startpos.start, self.pos($close).stop), $node, $e2.node) }
		|
			/* Slice access */
			'['
				e2=slice
			close=']' { $node = ul4c.ItemAST(self.tag.template, slice($e1.node._startpos.start, self.pos($close).stop), $node, $e2.node) }
		)*
	;

/* Negation/bitwise not */
expr_unary returns [node]
	:
		e1=expr_subscript { $node = $e1.node; }
	|
		minus='-' e2=expr_unary { $node = ul4c.NegAST.make(self.tag.template, slice(self.pos($minus).start, $e2.node._startpos.stop), $e2.node) }
	|
		bitnot='~' e2=expr_unary { $node = ul4c.BitNotAST.make(self.tag.template, slice(self.pos($bitnot).start, $e2.node._startpos.stop), $e2.node) }
	;


/* Multiplication, division, modulo */
expr_mul returns [node]
	:
		e1=expr_unary { $node = $e1.node; }
		(
			(
				'*' { cls = ul4c.MulAST; }
			|
				'/' { cls = ul4c.TrueDivAST; }
			|
				'//' { cls = ul4c.FloorDivAST; }
			|
				'%' { cls = ul4c.ModAST; }
			)
			e2=expr_unary { $node = cls.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Addition, substraction */
expr_add returns [node]
	:
		e1=expr_mul { $node = $e1.node; }
		(
			(
				'+' { cls = ul4c.AddAST; }
			|
				'-' { cls = ul4c.SubAST; }
			)
			e2=expr_mul { $node = cls.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Binary shift */
expr_bitshift returns [node]
	:
		e1=expr_add { $node = $e1.node; }
		(
			(
				'<<' { cls = ul4c.ShiftLeftAST; }
			|
				'>>' { cls = ul4c.ShiftRightAST; }
			)
			e2=expr_add { $node = cls.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Bitwise and */
expr_bitand returns [node]
	:
		e1=expr_bitshift { $node = $e1.node; }
		(
			'&'
			e2=expr_bitshift { $node = ul4c.BitAndAST.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Bitwise exclusive or */
expr_bitxor returns [node]
	:
		e1=expr_bitand { $node = $e1.node; }
		(
			'^'
			e2=expr_bitand { $node = ul4c.BitXOrAST.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Bitwise or */
expr_bitor returns [node]
	:
		e1=expr_bitxor { $node = $e1.node; }
		(
			'|'
			e2=expr_bitxor { $node = ul4c.BitOrAST.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Comparisons */
expr_cmp returns [node]
	:
		e1=expr_bitor { $node = $e1.node; }
		(
			(
				'==' { cls = ul4c.EQAST; }
			|
				'!=' { cls = ul4c.NEAST; }
			|
				'<' { cls = ul4c.LTAST; }
			|
				'<=' { cls = ul4c.LEAST; }
			|
				'>' { cls = ul4c.GTAST; }
			|
				'>=' { cls = ul4c.GEAST; }
			|
				'in' { cls = ul4c.ContainsAST; }
			|
				'not' 'in' { cls = ul4c.NotContainsAST; }
			|
				'is' { cls = ul4c.IsAST; }
			|
				'is' 'not' { cls = ul4c.IsNotAST; }
			)
			e2=expr_bitor { $node = cls.make(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Boolean not */
expr_not returns [node]
	:
		e1=expr_cmp { $node = $e1.node; }
	|
		n='not' e2=expr_not { $node = ul4c.NotAST.make(self.tag.template, slice(self.pos($n).start, $e2.node._startpos.stop), $e2.node) }
	;


/* And operator */
expr_and returns [node]
	:
		e1=expr_not { $node = $e1.node; }
		(
			'and'
			e2=expr_not { $node = ul4c.AndAST(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
		)*
	;

/* Or operator */
expr_or returns [node]
	:
		e1=expr_and { $node = $e1.node; }
		(
			'or'
			e2=expr_and { $node = ul4c.OrAST(self.tag.template, slice($node._startpos.start, $e2.node._startpos.stop), $node, $e2.node) }
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
			e3=expr_or { $node = ul4c.IfAST.make(self.tag.template, slice($e1.node._startpos.start, $e3.node._startpos.stop), $node, $e2.node, $e3.node); }
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
		e=expr_if { $node = ul4c.ForBlockAST(self.tag.template, self.tag._startpos, None, $n.lvalue, $e.node) }
		EOF
	;


/* Additional rules for "code" tag */

statement returns [node]
	: nn=nestedlvalue '=' e=expr_if EOF { $node = ul4c.SetVarAST(self.tag.template, self.tag._startpos, $nn.lvalue, $e.node) }
	| n=expr_subscript '+=' e=expr_if EOF { $node = ul4c.AddVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '-=' e=expr_if EOF { $node = ul4c.SubVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '*=' e=expr_if EOF { $node = ul4c.MulVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '/=' e=expr_if EOF { $node = ul4c.TrueDivVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '//=' e=expr_if EOF { $node = ul4c.FloorDivVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '%=' e=expr_if EOF { $node = ul4c.ModVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '<<=' e=expr_if EOF { $node = ul4c.ShiftLeftVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '>>=' e=expr_if EOF { $node = ul4c.ShiftRightVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '&=' e=expr_if EOF { $node = ul4c.BitAndVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '^=' e=expr_if EOF { $node = ul4c.BitXOrVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
	| n=expr_subscript '|=' e=expr_if EOF { $node = ul4c.BitOrVarAST(self.tag.template, self.tag._startpos, $n.node, $e.node) }
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
	open='(' { $node = ul4c.SignatureAST(self.tag.template, slice(self.pos($open).start, None)) }
	(
		/* No parameters */
	|
		/* "**" parameter only */
		'**' rkwargsname=name { $node.params.append(($rkwargsname.text, "**", None)); }
		','?
	|
		/* "*" parameter only (and maybe **) */
		'*' rargsname=name { $node.params.append(($rargsname.text, "*", None)); }
		(
			','
			'**' rkwargsname=name { $node.params.append(($rkwargsname.text, "**", None)); }
		)?
		','?
	|
		/* All parameters have a default */
		aname1=name
		'='
		adefault1=exprarg { $node.params.append(($aname1.text, "pk=", $adefault1.node)); }
		(
			','
			aname2=name
			'='
			adefault2=exprarg { $node.params.append(($aname2.text, "pk=", $adefault2.node)); }
		)*
		(
			','
			'*' rargsname=name { $node.params.append(($rargsname.text, "*", None)); }
		)?
		(
			','
			'**' rkwargsname=name { $node.params.append(($rkwargsname.text, "**", None)); }
		)?
		','?
	|
		/* At least one parameter without a default */
		aname1=name { $node.params.append(($aname1.text, "pk", None)); }
		(
			','
			aname2=name { $node.params.append(($aname2.text, "pk", None)); }
		)*
		(
			','
			aname3=name
			'='
			adefault3=exprarg { $node.params.append(($aname3.text, "pk=", $adefault3.node)); }
		)*
		(
			','
			'*' rargsname=name { $node.params.append(($rargsname.text, "*", None)); }
		)?
		(
			','
			'**' rkwargsname=name { $node.params.append(($rkwargsname.text, "**", None)); }
		)?
		','?
	)
	close=')' { $node.startpos = slice($node._startpos.start, self.pos($close).stop) }
	EOF
;
