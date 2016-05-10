# $ANTLR 3.5 src/ll/UL4.g 2016-05-10 15:48:43

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


import datetime, ast
from ll import ul4c, color



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
T__27=27
T__28=28
T__29=29
T__30=30
T__31=31
T__32=32
T__33=33
T__34=34
T__35=35
T__36=36
T__37=37
T__38=38
T__39=39
T__40=40
T__41=41
T__42=42
T__43=43
T__44=44
T__45=45
T__46=46
T__47=47
T__48=48
T__49=49
T__50=50
T__51=51
T__52=52
T__53=53
T__54=54
T__55=55
T__56=56
T__57=57
T__58=58
T__59=59
T__60=60
T__61=61
T__62=62
T__63=63
T__64=64
T__65=65
T__66=66
T__67=67
T__68=68
T__69=69
T__70=70
T__71=71
T__72=72
T__73=73
T__74=74
BIN_DIGIT=4
COLOR=5
DATE=6
DIGIT=7
ESC_SEQ=8
EXPONENT=9
FALSE=10
FLOAT=11
HEX_DIGIT=12
INT=13
NAME=14
NONE=15
OCT_DIGIT=16
STRING=17
STRING3=18
TIME=19
TRIAPOS=20
TRIQUOTE=21
TRUE=22
UNICODE1_ESC=23
UNICODE2_ESC=24
UNICODE4_ESC=25
WS=26

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "BIN_DIGIT", "COLOR", "DATE", "DIGIT", "ESC_SEQ", "EXPONENT", "FALSE", 
    "FLOAT", "HEX_DIGIT", "INT", "NAME", "NONE", "OCT_DIGIT", "STRING", 
    "STRING3", "TIME", "TRIAPOS", "TRIQUOTE", "TRUE", "UNICODE1_ESC", "UNICODE2_ESC", 
    "UNICODE4_ESC", "WS", "'!='", "'%'", "'%='", "'&'", "'&='", "'('", "')'", 
    "'*'", "'**'", "'*='", "'+'", "'+='", "','", "'-'", "'-='", "'.'", "'/'", 
    "'//'", "'//='", "'/='", "':'", "'<'", "'<<'", "'<<='", "'<='", "'='", 
    "'=='", "'>'", "'>='", "'>>'", "'>>='", "'['", "']'", "'^'", "'^='", 
    "'and'", "'else'", "'for'", "'if'", "'in'", "'is'", "'not'", "'or'", 
    "'{'", "'|'", "'|='", "'}'", "'~'"
]




class UL4Parser(Parser):
    grammarFileName = "src/ll/UL4.g"
    api_version = 1
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(UL4Parser, self).__init__(input, state, *args, **kwargs)

        self.dfa28 = self.DFA28(
            self, 28,
            eot = self.DFA28_eot,
            eof = self.DFA28_eof,
            min = self.DFA28_min,
            max = self.DFA28_max,
            accept = self.DFA28_accept,
            special = self.DFA28_special,
            transition = self.DFA28_transition
            )




        self.delegates = []




             
    def reportError(self, e):
    	raise e

    def mismatch(self, input, ttype, follow):
    	raise MismatchedTokenException(ttype, input)

    def recoverFromMismatchedSet(self, input, e, follow):
    	raise e

    def startpos(self, token):
    	return self.tag.codepos.start + token.start

    def stoppos(self, token):
    	return self.tag.codepos.start + token.stop + 1



    # $ANTLR start "none"
    # src/ll/UL4.g:165:1: none returns [node] : NONE ;
    def none(self, ):
        node = None


        NONE1 = None

        try:
            try:
                # src/ll/UL4.g:166:2: ( NONE )
                # src/ll/UL4.g:166:4: NONE
                pass 
                NONE1 = self.match(self.input, NONE, self.FOLLOW_NONE_in_none799)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(NONE1), self.stoppos(NONE1)), None) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "none"



    # $ANTLR start "true_"
    # src/ll/UL4.g:169:1: true_ returns [node] : TRUE ;
    def true_(self, ):
        node = None


        TRUE2 = None

        try:
            try:
                # src/ll/UL4.g:170:2: ( TRUE )
                # src/ll/UL4.g:170:4: TRUE
                pass 
                TRUE2 = self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_816)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(TRUE2), self.stoppos(TRUE2)), True) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "true_"



    # $ANTLR start "false_"
    # src/ll/UL4.g:173:1: false_ returns [node] : FALSE ;
    def false_(self, ):
        node = None


        FALSE3 = None

        try:
            try:
                # src/ll/UL4.g:174:2: ( FALSE )
                # src/ll/UL4.g:174:4: FALSE
                pass 
                FALSE3 = self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_833)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(FALSE3), self.stoppos(FALSE3)), False) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "false_"



    # $ANTLR start "int_"
    # src/ll/UL4.g:177:1: int_ returns [node] : INT ;
    def int_(self, ):
        node = None


        INT4 = None

        try:
            try:
                # src/ll/UL4.g:178:2: ( INT )
                # src/ll/UL4.g:178:4: INT
                pass 
                INT4 = self.match(self.input, INT, self.FOLLOW_INT_in_int_850)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(INT4), self.stoppos(INT4)), int(INT4.text, 0)) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "int_"



    # $ANTLR start "float_"
    # src/ll/UL4.g:181:1: float_ returns [node] : FLOAT ;
    def float_(self, ):
        node = None


        FLOAT5 = None

        try:
            try:
                # src/ll/UL4.g:182:2: ( FLOAT )
                # src/ll/UL4.g:182:4: FLOAT
                pass 
                FLOAT5 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_867)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(FLOAT5), self.stoppos(FLOAT5)), float(FLOAT5.text)) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "float_"



    # $ANTLR start "string"
    # src/ll/UL4.g:185:1: string returns [node] : ( STRING | STRING3 );
    def string(self, ):
        node = None


        STRING6 = None
        STRING37 = None

        try:
            try:
                # src/ll/UL4.g:186:2: ( STRING | STRING3 )
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == STRING) :
                    alt1 = 1
                elif (LA1_0 == STRING3) :
                    alt1 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae


                if alt1 == 1:
                    # src/ll/UL4.g:186:4: STRING
                    pass 
                    STRING6 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string884)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.tag, slice(self.startpos(STRING6), self.stoppos(STRING6)), ast.literal_eval(STRING6.text)) 




                elif alt1 == 2:
                    # src/ll/UL4.g:187:4: STRING3
                    pass 
                    STRING37 = self.match(self.input, STRING3, self.FOLLOW_STRING3_in_string891)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.tag, slice(self.startpos(STRING37), self.stoppos(STRING37)), ast.literal_eval(STRING37.text.replace("\r", "\\r"))) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "string"



    # $ANTLR start "date"
    # src/ll/UL4.g:190:1: date returns [node] : DATE ;
    def date(self, ):
        node = None


        DATE8 = None

        try:
            try:
                # src/ll/UL4.g:191:2: ( DATE )
                # src/ll/UL4.g:191:4: DATE
                pass 
                DATE8 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date908)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(DATE8), self.stoppos(DATE8)), datetime.datetime(*map(int, [f for f in ul4c._datesplitter.split(DATE8.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "date"



    # $ANTLR start "color"
    # src/ll/UL4.g:194:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR9 = None

        try:
            try:
                # src/ll/UL4.g:195:2: ( COLOR )
                # src/ll/UL4.g:195:4: COLOR
                pass 
                COLOR9 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color925)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag, slice(self.startpos(COLOR9), self.stoppos(COLOR9)), color.Color.fromrepr(COLOR9.text)) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "color"


    class name_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.name_return, self).__init__()

            self.node = None





    # $ANTLR start "name"
    # src/ll/UL4.g:198:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME10 = None

        try:
            try:
                # src/ll/UL4.g:199:2: ( NAME )
                # src/ll/UL4.g:199:4: NAME
                pass 
                NAME10 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name942)

                if self._state.backtracking == 0:
                    pass
                    retval.node = ul4c.Var(self.tag, slice(self.startpos(NAME10), self.stoppos(NAME10)), NAME10.text) 





                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return retval

    # $ANTLR end "name"



    # $ANTLR start "literal"
    # src/ll/UL4.g:202:1: literal returns [node] : (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name );
    def literal(self, ):
        node = None


        e_none = None
        e_false = None
        e_true = None
        e_int = None
        e_float = None
        e_string = None
        e_date = None
        e_color = None
        e_name = None

        try:
            try:
                # src/ll/UL4.g:203:2: (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name )
                alt2 = 9
                LA2 = self.input.LA(1)
                if LA2 == NONE:
                    alt2 = 1
                elif LA2 == FALSE:
                    alt2 = 2
                elif LA2 == TRUE:
                    alt2 = 3
                elif LA2 == INT:
                    alt2 = 4
                elif LA2 == FLOAT:
                    alt2 = 5
                elif LA2 == STRING or LA2 == STRING3:
                    alt2 = 6
                elif LA2 == DATE:
                    alt2 = 7
                elif LA2 == COLOR:
                    alt2 = 8
                elif LA2 == NAME:
                    alt2 = 9
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 2, 0, self.input)

                    raise nvae


                if alt2 == 1:
                    # src/ll/UL4.g:203:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal961)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt2 == 2:
                    # src/ll/UL4.g:204:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal970)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt2 == 3:
                    # src/ll/UL4.g:205:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal979)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt2 == 4:
                    # src/ll/UL4.g:206:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal988)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt2 == 5:
                    # src/ll/UL4.g:207:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal997)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt2 == 6:
                    # src/ll/UL4.g:208:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal1006)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt2 == 7:
                    # src/ll/UL4.g:209:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal1015)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt2 == 8:
                    # src/ll/UL4.g:210:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal1024)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt2 == 9:
                    # src/ll/UL4.g:211:4: e_name= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_literal1033)
                    e_name = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ((e_name is not None) and [e_name.node] or [None])[0] 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "literal"



    # $ANTLR start "seqitem"
    # src/ll/UL4.g:216:1: fragment seqitem returns [node] : (e= expr_if |star= '*' es= expr_if );
    def seqitem(self, ):
        node = None


        star = None
        e = None
        es = None

        try:
            try:
                # src/ll/UL4.g:217:2: (e= expr_if |star= '*' es= expr_if )
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((COLOR <= LA3_0 <= DATE) or (FALSE <= LA3_0 <= FLOAT) or (INT <= LA3_0 <= NONE) or (STRING <= LA3_0 <= STRING3) or LA3_0 == TRUE or LA3_0 == 32 or LA3_0 == 40 or LA3_0 == 58 or LA3_0 == 68 or LA3_0 == 70 or LA3_0 == 74) :
                    alt3 = 1
                elif (LA3_0 == 34) :
                    alt3 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 3, 0, self.input)

                    raise nvae


                if alt3 == 1:
                    # src/ll/UL4.g:218:3: e= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_seqitem1058)
                    e = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SeqItem(self.tag, slice(e.pos.start, e.pos.stop), e) 




                elif alt3 == 2:
                    # src/ll/UL4.g:220:3: star= '*' es= expr_if
                    pass 
                    star = self.match(self.input, 34, self.FOLLOW_34_in_seqitem1069)

                    self._state.following.append(self.FOLLOW_expr_if_in_seqitem1075)
                    es = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackSeqItem(self.tag, slice(self.startpos(star), es.pos.stop), es) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "seqitem"



    # $ANTLR start "list"
    # src/ll/UL4.g:224:1: list returns [node] : (open= '[' close= ']' |open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']' );
    def list(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:225:2: (open= '[' close= ']' |open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']' )
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 58) :
                    LA6_1 = self.input.LA(2)

                    if (LA6_1 == 59) :
                        alt6 = 1
                    elif ((COLOR <= LA6_1 <= DATE) or (FALSE <= LA6_1 <= FLOAT) or (INT <= LA6_1 <= NONE) or (STRING <= LA6_1 <= STRING3) or LA6_1 == TRUE or LA6_1 == 32 or LA6_1 == 34 or LA6_1 == 40 or LA6_1 == 58 or LA6_1 == 68 or LA6_1 == 70 or LA6_1 == 74) :
                        alt6 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 6, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 6, 0, self.input)

                    raise nvae


                if alt6 == 1:
                    # src/ll/UL4.g:226:3: open= '[' close= ']'
                    pass 
                    open = self.match(self.input, 58, self.FOLLOW_58_in_list1096)

                    close = self.match(self.input, 59, self.FOLLOW_59_in_list1102)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.tag, slice(self.startpos(open), self.stoppos(close))) 




                elif alt6 == 2:
                    # src/ll/UL4.g:229:3: open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 58, self.FOLLOW_58_in_list1113)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.tag, slice(self.startpos(open), None)) 



                    self._state.following.append(self.FOLLOW_seqitem_in_list1121)
                    i1 = self.seqitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:231:3: ( ',' i2= seqitem )*
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == 39) :
                            LA4_1 = self.input.LA(2)

                            if ((COLOR <= LA4_1 <= DATE) or (FALSE <= LA4_1 <= FLOAT) or (INT <= LA4_1 <= NONE) or (STRING <= LA4_1 <= STRING3) or LA4_1 == TRUE or LA4_1 == 32 or LA4_1 == 34 or LA4_1 == 40 or LA4_1 == 58 or LA4_1 == 68 or LA4_1 == 70 or LA4_1 == 74) :
                                alt4 = 1




                        if alt4 == 1:
                            # src/ll/UL4.g:232:4: ',' i2= seqitem
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_list1132)

                            self._state.following.append(self.FOLLOW_seqitem_in_list1139)
                            i2 = self.seqitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop4


                    # src/ll/UL4.g:235:3: ( ',' )?
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == 39) :
                        alt5 = 1
                    if alt5 == 1:
                        # src/ll/UL4.g:235:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_list1150)




                    close = self.match(self.input, 59, self.FOLLOW_59_in_list1157)

                    if self._state.backtracking == 0:
                        pass
                        node.pos = slice(node.pos.start, self.stoppos(close)) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "list"



    # $ANTLR start "listcomprehension"
    # src/ll/UL4.g:239:1: listcomprehension returns [node] : open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' ;
    def listcomprehension(self, ):
        node = None


        open = None
        close = None
        item = None
        n = None
        container = None
        condition = None

         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:244:2: (open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' )
                # src/ll/UL4.g:245:3: open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']'
                pass 
                open = self.match(self.input, 58, self.FOLLOW_58_in_listcomprehension1185)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1191)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_listcomprehension1195)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_listcomprehension1201)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_listcomprehension1205)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1211)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:251:3: ( 'if' condition= expr_if )?
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == 65) :
                    alt7 = 1
                if alt7 == 1:
                    # src/ll/UL4.g:252:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_listcomprehension1220)

                    self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1227)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 59, self.FOLLOW_59_in_listcomprehension1240)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ListComp(self.tag, slice(self.startpos(open), self.stoppos(close)), item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "set"
    # src/ll/UL4.g:259:1: set returns [node] : (open= '{' '/' close= '}' |open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}' );
    def set(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:260:2: (open= '{' '/' close= '}' |open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}' )
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 70) :
                    LA10_1 = self.input.LA(2)

                    if (LA10_1 == 43) :
                        alt10 = 1
                    elif ((COLOR <= LA10_1 <= DATE) or (FALSE <= LA10_1 <= FLOAT) or (INT <= LA10_1 <= NONE) or (STRING <= LA10_1 <= STRING3) or LA10_1 == TRUE or LA10_1 == 32 or LA10_1 == 34 or LA10_1 == 40 or LA10_1 == 58 or LA10_1 == 68 or LA10_1 == 70 or LA10_1 == 74) :
                        alt10 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 10, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 10, 0, self.input)

                    raise nvae


                if alt10 == 1:
                    # src/ll/UL4.g:261:3: open= '{' '/' close= '}'
                    pass 
                    open = self.match(self.input, 70, self.FOLLOW_70_in_set1263)

                    self.match(self.input, 43, self.FOLLOW_43_in_set1267)

                    close = self.match(self.input, 73, self.FOLLOW_73_in_set1273)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.tag, slice(self.startpos(open), self.stoppos(close))) 




                elif alt10 == 2:
                    # src/ll/UL4.g:265:3: open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 70, self.FOLLOW_70_in_set1284)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.tag, slice(self.startpos(open), None)) 



                    self._state.following.append(self.FOLLOW_seqitem_in_set1292)
                    i1 = self.seqitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:267:3: ( ',' i2= seqitem )*
                    while True: #loop8
                        alt8 = 2
                        LA8_0 = self.input.LA(1)

                        if (LA8_0 == 39) :
                            LA8_1 = self.input.LA(2)

                            if ((COLOR <= LA8_1 <= DATE) or (FALSE <= LA8_1 <= FLOAT) or (INT <= LA8_1 <= NONE) or (STRING <= LA8_1 <= STRING3) or LA8_1 == TRUE or LA8_1 == 32 or LA8_1 == 34 or LA8_1 == 40 or LA8_1 == 58 or LA8_1 == 68 or LA8_1 == 70 or LA8_1 == 74) :
                                alt8 = 1




                        if alt8 == 1:
                            # src/ll/UL4.g:268:4: ',' i2= seqitem
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_set1303)

                            self._state.following.append(self.FOLLOW_seqitem_in_set1310)
                            i2 = self.seqitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop8


                    # src/ll/UL4.g:271:3: ( ',' )?
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == 39) :
                        alt9 = 1
                    if alt9 == 1:
                        # src/ll/UL4.g:271:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_set1321)




                    close = self.match(self.input, 73, self.FOLLOW_73_in_set1328)

                    if self._state.backtracking == 0:
                        pass
                        node.pos = slice(node.pos.start, self.stoppos(close)) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "set"



    # $ANTLR start "setcomprehension"
    # src/ll/UL4.g:275:1: setcomprehension returns [node] : open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
    def setcomprehension(self, ):
        node = None


        open = None
        close = None
        item = None
        n = None
        container = None
        condition = None

         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:280:2: (open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:281:3: open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 70, self.FOLLOW_70_in_setcomprehension1356)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1362)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_setcomprehension1366)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_setcomprehension1372)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_setcomprehension1376)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1382)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:287:3: ( 'if' condition= expr_if )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 65) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:288:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_setcomprehension1391)

                    self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1398)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 73, self.FOLLOW_73_in_setcomprehension1411)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.SetComp(self.tag, slice(self.startpos(open), self.stoppos(close)), item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "setcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:296:1: fragment dictitem returns [node] : (k= expr_if ':' v= expr_if |star= '**' e= expr_if );
    def dictitem(self, ):
        node = None


        star = None
        k = None
        v = None
        e = None

        try:
            try:
                # src/ll/UL4.g:297:2: (k= expr_if ':' v= expr_if |star= '**' e= expr_if )
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if ((COLOR <= LA12_0 <= DATE) or (FALSE <= LA12_0 <= FLOAT) or (INT <= LA12_0 <= NONE) or (STRING <= LA12_0 <= STRING3) or LA12_0 == TRUE or LA12_0 == 32 or LA12_0 == 40 or LA12_0 == 58 or LA12_0 == 68 or LA12_0 == 70 or LA12_0 == 74) :
                    alt12 = 1
                elif (LA12_0 == 35) :
                    alt12 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae


                if alt12 == 1:
                    # src/ll/UL4.g:298:3: k= expr_if ':' v= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1436)
                    k = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, 47, self.FOLLOW_47_in_dictitem1440)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1446)
                    v = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.DictItem(self.tag, slice(k.pos.start, v.pos.start), k, v) 




                elif alt12 == 2:
                    # src/ll/UL4.g:302:3: star= '**' e= expr_if
                    pass 
                    star = self.match(self.input, 35, self.FOLLOW_35_in_dictitem1457)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1463)
                    e = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackDictItem(self.tag, slice(self.startpos(star), e.pos.stop), e) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dictitem"



    # $ANTLR start "dict"
    # src/ll/UL4.g:306:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:307:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == 70) :
                    LA15_1 = self.input.LA(2)

                    if (LA15_1 == 73) :
                        alt15 = 1
                    elif ((COLOR <= LA15_1 <= DATE) or (FALSE <= LA15_1 <= FLOAT) or (INT <= LA15_1 <= NONE) or (STRING <= LA15_1 <= STRING3) or LA15_1 == TRUE or LA15_1 == 32 or LA15_1 == 35 or LA15_1 == 40 or LA15_1 == 58 or LA15_1 == 68 or LA15_1 == 70 or LA15_1 == 74) :
                        alt15 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 15, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 15, 0, self.input)

                    raise nvae


                if alt15 == 1:
                    # src/ll/UL4.g:308:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 70, self.FOLLOW_70_in_dict1484)

                    close = self.match(self.input, 73, self.FOLLOW_73_in_dict1490)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.tag, slice(self.startpos(open), self.stoppos(close))) 




                elif alt15 == 2:
                    # src/ll/UL4.g:311:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 70, self.FOLLOW_70_in_dict1501)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.tag, slice(self.startpos(open), None)) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1509)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:313:3: ( ',' i2= dictitem )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 39) :
                            LA13_1 = self.input.LA(2)

                            if ((COLOR <= LA13_1 <= DATE) or (FALSE <= LA13_1 <= FLOAT) or (INT <= LA13_1 <= NONE) or (STRING <= LA13_1 <= STRING3) or LA13_1 == TRUE or LA13_1 == 32 or LA13_1 == 35 or LA13_1 == 40 or LA13_1 == 58 or LA13_1 == 68 or LA13_1 == 70 or LA13_1 == 74) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:314:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_dict1520)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1527)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop13


                    # src/ll/UL4.g:317:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 39) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:317:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_dict1538)




                    close = self.match(self.input, 73, self.FOLLOW_73_in_dict1545)

                    if self._state.backtracking == 0:
                        pass
                        node.pos = slice(node.pos.start, self.stoppos(close)) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:321:1: dictcomprehension returns [node] : open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
    def dictcomprehension(self, ):
        node = None


        open = None
        close = None
        key = None
        value = None
        n = None
        container = None
        condition = None

         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:326:2: (open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:327:3: open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 70, self.FOLLOW_70_in_dictcomprehension1573)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1579)
                key = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 47, self.FOLLOW_47_in_dictcomprehension1583)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1589)
                value = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_dictcomprehension1593)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_dictcomprehension1599)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_dictcomprehension1603)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1609)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:335:3: ( 'if' condition= expr_if )?
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if (LA16_0 == 65) :
                    alt16 = 1
                if alt16 == 1:
                    # src/ll/UL4.g:336:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_dictcomprehension1618)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1625)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 73, self.FOLLOW_73_in_dictcomprehension1638)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.DictComp(self.tag, slice(self.startpos(open), self.stoppos(close)), key, value, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:342:1: generatorexpression returns [node] : item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? ;
    def generatorexpression(self, ):
        node = None


        item = None
        n = None
        container = None
        condition = None

         
        _condition = None
        _stop = None
        	
        try:
            try:
                # src/ll/UL4.g:348:2: (item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? )
                # src/ll/UL4.g:349:3: item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )?
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1666)
                item = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item.pos.start 



                self.match(self.input, 64, self.FOLLOW_64_in_generatorexpression1672)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_generatorexpression1678)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_generatorexpression1682)

                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1688)
                container = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _stop = container.pos.stop 



                # src/ll/UL4.g:354:3: ( 'if' condition= expr_if )?
                alt17 = 2
                LA17_0 = self.input.LA(1)

                if (LA17_0 == 65) :
                    alt17 = 1
                if alt17 == 1:
                    # src/ll/UL4.g:355:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_generatorexpression1699)

                    self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1706)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; _stop = condition.pos.stop 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.GenExpr(self.tag, slice(item.pos.start, _stop), item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:360:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' );
    def atom(self, ):
        node = None


        open = None
        close = None
        e_literal = None
        e_list = None
        e_listcomp = None
        e_set = None
        e_setcomp = None
        e_dict = None
        e_dictcomp = None
        e_genexpr = None
        e_bracket = None

        try:
            try:
                # src/ll/UL4.g:361:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' )
                alt18 = 9
                LA18 = self.input.LA(1)
                if LA18 == COLOR or LA18 == DATE or LA18 == FALSE or LA18 == FLOAT or LA18 == INT or LA18 == NAME or LA18 == NONE or LA18 == STRING or LA18 == STRING3 or LA18 == TRUE:
                    alt18 = 1
                elif LA18 == 58:
                    LA18_11 = self.input.LA(2)

                    if (self.synpred26_UL4()) :
                        alt18 = 2
                    elif (self.synpred27_UL4()) :
                        alt18 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 11, self.input)

                        raise nvae


                elif LA18 == 70:
                    LA18_12 = self.input.LA(2)

                    if (self.synpred28_UL4()) :
                        alt18 = 4
                    elif (self.synpred29_UL4()) :
                        alt18 = 5
                    elif (self.synpred30_UL4()) :
                        alt18 = 6
                    elif (self.synpred31_UL4()) :
                        alt18 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 12, self.input)

                        raise nvae


                elif LA18 == 32:
                    LA18_13 = self.input.LA(2)

                    if (self.synpred32_UL4()) :
                        alt18 = 8
                    elif (True) :
                        alt18 = 9
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 18, 0, self.input)

                    raise nvae


                if alt18 == 1:
                    # src/ll/UL4.g:361:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1732)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt18 == 2:
                    # src/ll/UL4.g:362:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1741)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt18 == 3:
                    # src/ll/UL4.g:363:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1750)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt18 == 4:
                    # src/ll/UL4.g:364:4: e_set= set
                    pass 
                    self._state.following.append(self.FOLLOW_set_in_atom1759)
                    e_set = self.set()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_set 




                elif alt18 == 5:
                    # src/ll/UL4.g:365:4: e_setcomp= setcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_setcomprehension_in_atom1768)
                    e_setcomp = self.setcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_setcomp 




                elif alt18 == 6:
                    # src/ll/UL4.g:366:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1777)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt18 == 7:
                    # src/ll/UL4.g:367:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1786)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt18 == 8:
                    # src/ll/UL4.g:368:4: open= '(' e_genexpr= generatorexpression close= ')'
                    pass 
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1795)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1799)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1803)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.pos = slice(self.startpos(open), self.stoppos(close))
                        	




                elif alt18 == 9:
                    # src/ll/UL4.g:372:4: open= '(' e_bracket= expr_if close= ')'
                    pass 
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1812)

                    self._state.following.append(self.FOLLOW_expr_if_in_atom1816)
                    e_bracket = self.expr_if()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1820)

                    if self._state.backtracking == 0:
                        pass
                                                                
                        node = e_bracket
                        node.pos = slice(self.startpos(open), self.stoppos(close))
                        	





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "atom"


    class nestedlvalue_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.nestedlvalue_return, self).__init__()

            self.lvalue = None





    # $ANTLR start "nestedlvalue"
    # src/ll/UL4.g:379:1: nestedlvalue returns [lvalue] : (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' );
    def nestedlvalue(self, ):
        retval = self.nestedlvalue_return()
        retval.start = self.input.LT(1)


        n = None
        n0 = None
        n1 = None
        n2 = None
        n3 = None

        try:
            try:
                # src/ll/UL4.g:380:2: (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' )
                alt21 = 3
                LA21_0 = self.input.LA(1)

                if ((COLOR <= LA21_0 <= DATE) or (FALSE <= LA21_0 <= FLOAT) or (INT <= LA21_0 <= NONE) or (STRING <= LA21_0 <= STRING3) or LA21_0 == TRUE or LA21_0 == 58 or LA21_0 == 70) :
                    alt21 = 1
                elif (LA21_0 == 32) :
                    LA21_13 = self.input.LA(2)

                    if (self.synpred33_UL4()) :
                        alt21 = 1
                    elif (self.synpred34_UL4()) :
                        alt21 = 2
                    elif (True) :
                        alt21 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 21, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 21, 0, self.input)

                    raise nvae


                if alt21 == 1:
                    # src/ll/UL4.g:381:3: n= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_nestedlvalue1843)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue =  n 




                elif alt21 == 2:
                    # src/ll/UL4.g:383:3: '(' n0= nestedlvalue ',' ')'
                    pass 
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1852)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1856)
                    n0 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1858)

                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1860)

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n0 is not None) and [n0.lvalue] or [None])[0],) 




                elif alt21 == 3:
                    # src/ll/UL4.g:385:3: '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1869)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1875)
                    n1 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1879)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1885)
                    n2 = self.nestedlvalue()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n1 is not None) and [n1.lvalue] or [None])[0], ((n2 is not None) and [n2.lvalue] or [None])[0]) 



                    # src/ll/UL4.g:389:3: ( ',' n3= nestedlvalue )*
                    while True: #loop19
                        alt19 = 2
                        LA19_0 = self.input.LA(1)

                        if (LA19_0 == 39) :
                            LA19_1 = self.input.LA(2)

                            if ((COLOR <= LA19_1 <= DATE) or (FALSE <= LA19_1 <= FLOAT) or (INT <= LA19_1 <= NONE) or (STRING <= LA19_1 <= STRING3) or LA19_1 == TRUE or LA19_1 == 32 or LA19_1 == 58 or LA19_1 == 70) :
                                alt19 = 1




                        if alt19 == 1:
                            # src/ll/UL4.g:390:4: ',' n3= nestedlvalue
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1896)

                            self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1903)
                            n3 = self.nestedlvalue()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.lvalue += (((n3 is not None) and [n3.lvalue] or [None])[0],) 




                        else:
                            break #loop19


                    # src/ll/UL4.g:393:3: ( ',' )?
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if (LA20_0 == 39) :
                        alt20 = 1
                    if alt20 == 1:
                        # src/ll/UL4.g:393:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1914)




                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1919)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedlvalue"



    # $ANTLR start "slice"
    # src/ll/UL4.g:398:1: slice returns [node] : (e1= expr_if )? colon= ':' (e2= expr_if )? ;
    def slice(self, ):
        node = None


        colon = None
        e1 = None
        e2 = None

         
        index1 = None
        index2 = None
        startpos = None
        stoppos = None
        	
        try:
            try:
                # src/ll/UL4.g:406:2: ( (e1= expr_if )? colon= ':' (e2= expr_if )? )
                # src/ll/UL4.g:407:3: (e1= expr_if )? colon= ':' (e2= expr_if )?
                pass 
                # src/ll/UL4.g:407:3: (e1= expr_if )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if ((COLOR <= LA22_0 <= DATE) or (FALSE <= LA22_0 <= FLOAT) or (INT <= LA22_0 <= NONE) or (STRING <= LA22_0 <= STRING3) or LA22_0 == TRUE or LA22_0 == 32 or LA22_0 == 40 or LA22_0 == 58 or LA22_0 == 68 or LA22_0 == 70 or LA22_0 == 74) :
                    alt22 = 1
                if alt22 == 1:
                    # src/ll/UL4.g:408:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1952)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index1 = e1; startpos = e1.pos.start; 






                colon = self.match(self.input, 47, self.FOLLOW_47_in_slice1965)

                if self._state.backtracking == 0:
                    pass
                                
                    if startpos is None:
                    	startpos = self.startpos(colon)
                    stoppos = self.stoppos(colon)
                    		



                # src/ll/UL4.g:415:3: (e2= expr_if )?
                alt23 = 2
                LA23_0 = self.input.LA(1)

                if ((COLOR <= LA23_0 <= DATE) or (FALSE <= LA23_0 <= FLOAT) or (INT <= LA23_0 <= NONE) or (STRING <= LA23_0 <= STRING3) or LA23_0 == TRUE or LA23_0 == 32 or LA23_0 == 40 or LA23_0 == 58 or LA23_0 == 68 or LA23_0 == 70 or LA23_0 == 74) :
                    alt23 = 1
                if alt23 == 1:
                    # src/ll/UL4.g:416:4: e2= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1978)
                    e2 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index2 = e2; stoppos = e2.pos.stop; 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Slice(self.tag, slice(startpos, stoppos), index1, index2) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "slice"



    # $ANTLR start "argument"
    # src/ll/UL4.g:422:1: fragment argument returns [node] : (e= exprarg |en= name '=' ev= exprarg |star= '*' es= exprarg |star= '**' es= exprarg );
    def argument(self, ):
        node = None


        star = None
        e = None
        en = None
        ev = None
        es = None

        try:
            try:
                # src/ll/UL4.g:423:2: (e= exprarg |en= name '=' ev= exprarg |star= '*' es= exprarg |star= '**' es= exprarg )
                alt24 = 4
                LA24 = self.input.LA(1)
                if LA24 == COLOR or LA24 == DATE or LA24 == FALSE or LA24 == FLOAT or LA24 == INT or LA24 == NONE or LA24 == STRING or LA24 == STRING3 or LA24 == TRUE or LA24 == 32 or LA24 == 40 or LA24 == 58 or LA24 == 68 or LA24 == 70 or LA24 == 74:
                    alt24 = 1
                elif LA24 == NAME:
                    LA24_2 = self.input.LA(2)

                    if (LA24_2 == EOF or (COLOR <= LA24_2 <= DATE) or (FALSE <= LA24_2 <= FLOAT) or (INT <= LA24_2 <= NONE) or (STRING <= LA24_2 <= STRING3) or LA24_2 == TRUE or (27 <= LA24_2 <= 28) or LA24_2 == 30 or (32 <= LA24_2 <= 35) or LA24_2 == 37 or (39 <= LA24_2 <= 40) or (42 <= LA24_2 <= 44) or (48 <= LA24_2 <= 49) or LA24_2 == 51 or (53 <= LA24_2 <= 56) or LA24_2 == 58 or LA24_2 == 60 or LA24_2 == 62 or (64 <= LA24_2 <= 71) or LA24_2 == 74) :
                        alt24 = 1
                    elif (LA24_2 == 52) :
                        alt24 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 24, 2, self.input)

                        raise nvae


                elif LA24 == 34:
                    alt24 = 3
                elif LA24 == 35:
                    alt24 = 4
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 24, 0, self.input)

                    raise nvae


                if alt24 == 1:
                    # src/ll/UL4.g:424:3: e= exprarg
                    pass 
                    self._state.following.append(self.FOLLOW_exprarg_in_argument2010)
                    e = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.PosArg(self.tag, e.pos, e) 




                elif alt24 == 2:
                    # src/ll/UL4.g:426:3: en= name '=' ev= exprarg
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_argument2021)
                    en = self.name()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_argument2023)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2027)
                    ev = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.KeywordArg(self.tag, slice(((en is not None) and [en.node] or [None])[0].pos.start, ev.pos.stop), ((en is not None) and [self.input.toString(en.start,en.stop)] or [None])[0], ev) 




                elif alt24 == 3:
                    # src/ll/UL4.g:428:3: star= '*' es= exprarg
                    pass 
                    star = self.match(self.input, 34, self.FOLLOW_34_in_argument2038)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2044)
                    es = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackListArg(self.tag, slice(self.startpos(star), es.pos.stop), es) 




                elif alt24 == 4:
                    # src/ll/UL4.g:431:3: star= '**' es= exprarg
                    pass 
                    star = self.match(self.input, 35, self.FOLLOW_35_in_argument2055)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2061)
                    es = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackDictArg(self.tag, slice(self.startpos(star), es.pos.stop), es) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "argument"



    # $ANTLR start "expr_subscript"
    # src/ll/UL4.g:435:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* ;
    def expr_subscript(self, ):
        node = None


        close = None
        e1 = None
        n = None
        a1 = None
        a2 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:436:2: (e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* )
                # src/ll/UL4.g:437:3: e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript2082)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:438:3: ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                while True: #loop28
                    alt28 = 5
                    alt28 = self.dfa28.predict(self.input)
                    if alt28 == 1:
                        # src/ll/UL4.g:440:4: '.' n= name
                        pass 
                        self.match(self.input, 42, self.FOLLOW_42_in_expr_subscript2098)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript2105)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Attr(self.tag, slice(node.pos.start, self.stoppos(n.stop)), node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt28 == 2:
                        # src/ll/UL4.g:444:4: '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')'
                        pass 
                        self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript2121)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Call(self.tag, slice(node.pos.start, None), node) 



                        # src/ll/UL4.g:445:4: (a1= argument ( ',' a2= argument )* ( ',' )? )*
                        while True: #loop27
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if ((COLOR <= LA27_0 <= DATE) or (FALSE <= LA27_0 <= FLOAT) or (INT <= LA27_0 <= NONE) or (STRING <= LA27_0 <= STRING3) or LA27_0 == TRUE or LA27_0 == 32 or (34 <= LA27_0 <= 35) or LA27_0 == 40 or LA27_0 == 58 or LA27_0 == 68 or LA27_0 == 70 or LA27_0 == 74) :
                                alt27 = 1


                            if alt27 == 1:
                                # src/ll/UL4.g:446:5: a1= argument ( ',' a2= argument )* ( ',' )?
                                pass 
                                self._state.following.append(self.FOLLOW_argument_in_expr_subscript2136)
                                a1 = self.argument()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    a1.append(node) 



                                # src/ll/UL4.g:447:5: ( ',' a2= argument )*
                                while True: #loop25
                                    alt25 = 2
                                    LA25_0 = self.input.LA(1)

                                    if (LA25_0 == 39) :
                                        LA25_1 = self.input.LA(2)

                                        if (self.synpred43_UL4()) :
                                            alt25 = 1




                                    if alt25 == 1:
                                        # src/ll/UL4.g:448:6: ',' a2= argument
                                        pass 
                                        self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2151)

                                        self._state.following.append(self.FOLLOW_argument_in_expr_subscript2160)
                                        a2 = self.argument()

                                        self._state.following.pop()

                                        if self._state.backtracking == 0:
                                            pass
                                            a2.append(node) 




                                    else:
                                        break #loop25


                                # src/ll/UL4.g:451:5: ( ',' )?
                                alt26 = 2
                                LA26_0 = self.input.LA(1)

                                if (LA26_0 == 39) :
                                    alt26 = 1
                                if alt26 == 1:
                                    # src/ll/UL4.g:451:5: ','
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2175)





                            else:
                                break #loop27


                        close = self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2189)

                        if self._state.backtracking == 0:
                            pass
                            node.pos = slice(node.pos.start, self.stoppos(close)) 




                    elif alt28 == 3:
                        # src/ll/UL4.g:456:4: '[' e2= expr_if close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2205)

                        self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2213)
                        e2 = self.expr_if()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2220)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Item(self.tag, slice(e1.pos.start, self.stoppos(close)), node, e2) 




                    elif alt28 == 4:
                        # src/ll/UL4.g:461:4: '[' e2= slice close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2236)

                        self._state.following.append(self.FOLLOW_slice_in_expr_subscript2244)
                        e2 = self.slice()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2251)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Item(self.tag, slice(e1.pos.start, self.stoppos(close)), node, e2) 




                    else:
                        break #loop28





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_subscript"



    # $ANTLR start "expr_unary"
    # src/ll/UL4.g:468:1: expr_unary returns [node] : (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary );
    def expr_unary(self, ):
        node = None


        minus = None
        bitnot = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:469:2: (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary )
                alt29 = 3
                LA29 = self.input.LA(1)
                if LA29 == COLOR or LA29 == DATE or LA29 == FALSE or LA29 == FLOAT or LA29 == INT or LA29 == NAME or LA29 == NONE or LA29 == STRING or LA29 == STRING3 or LA29 == TRUE or LA29 == 32 or LA29 == 58 or LA29 == 70:
                    alt29 = 1
                elif LA29 == 40:
                    alt29 = 2
                elif LA29 == 74:
                    alt29 = 3
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 29, 0, self.input)

                    raise nvae


                if alt29 == 1:
                    # src/ll/UL4.g:470:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_unary2279)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt29 == 2:
                    # src/ll/UL4.g:472:3: minus= '-' e2= expr_unary
                    pass 
                    minus = self.match(self.input, 40, self.FOLLOW_40_in_expr_unary2290)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2294)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.tag, slice(self.startpos(minus), e2.pos.stop), e2) 




                elif alt29 == 3:
                    # src/ll/UL4.g:474:3: bitnot= '~' e2= expr_unary
                    pass 
                    bitnot = self.match(self.input, 74, self.FOLLOW_74_in_expr_unary2305)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2309)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitNot.make(self.tag, slice(self.startpos(bitnot), e2.pos.stop), e2) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_unary"



    # $ANTLR start "expr_mul"
    # src/ll/UL4.g:479:1: expr_mul returns [node] : e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:480:2: (e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* )
                # src/ll/UL4.g:481:3: e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                pass 
                self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2333)
                e1 = self.expr_unary()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:482:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                while True: #loop31
                    alt31 = 2
                    LA31_0 = self.input.LA(1)

                    if (LA31_0 == 34) :
                        LA31_41 = self.input.LA(2)

                        if (self.synpred54_UL4()) :
                            alt31 = 1


                    elif (LA31_0 == 28 or (43 <= LA31_0 <= 44)) :
                        alt31 = 1


                    if alt31 == 1:
                        # src/ll/UL4.g:483:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
                        pass 
                        # src/ll/UL4.g:483:4: ( '*' | '/' | '//' | '%' )
                        alt30 = 4
                        LA30 = self.input.LA(1)
                        if LA30 == 34:
                            alt30 = 1
                        elif LA30 == 43:
                            alt30 = 2
                        elif LA30 == 44:
                            alt30 = 3
                        elif LA30 == 28:
                            alt30 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 30, 0, self.input)

                            raise nvae


                        if alt30 == 1:
                            # src/ll/UL4.g:484:5: '*'
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_mul2350)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt30 == 2:
                            # src/ll/UL4.g:486:5: '/'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr_mul2363)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt30 == 3:
                            # src/ll/UL4.g:488:5: '//'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr_mul2376)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt30 == 4:
                            # src/ll/UL4.g:490:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_mul2389)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2403)
                        e2 = self.expr_unary()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop31





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_mul"



    # $ANTLR start "expr_add"
    # src/ll/UL4.g:497:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:498:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:499:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2431)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:500:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 40) :
                        LA33_38 = self.input.LA(2)

                        if (self.synpred56_UL4()) :
                            alt33 = 1


                    elif (LA33_0 == 37) :
                        alt33 = 1


                    if alt33 == 1:
                        # src/ll/UL4.g:501:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:501:4: ( '+' | '-' )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 37) :
                            alt32 = 1
                        elif (LA32_0 == 40) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:502:5: '+'
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_expr_add2448)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt32 == 2:
                            # src/ll/UL4.g:504:5: '-'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr_add2461)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2475)
                        e2 = self.expr_mul()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop33





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_add"



    # $ANTLR start "expr_bitshift"
    # src/ll/UL4.g:511:1: expr_bitshift returns [node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:512:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:513:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2503)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:514:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 49 or LA35_0 == 56) :
                        alt35 = 1


                    if alt35 == 1:
                        # src/ll/UL4.g:515:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:515:4: ( '<<' | '>>' )
                        alt34 = 2
                        LA34_0 = self.input.LA(1)

                        if (LA34_0 == 49) :
                            alt34 = 1
                        elif (LA34_0 == 56) :
                            alt34 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 34, 0, self.input)

                            raise nvae


                        if alt34 == 1:
                            # src/ll/UL4.g:516:5: '<<'
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_bitshift2520)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt34 == 2:
                            # src/ll/UL4.g:518:5: '>>'
                            pass 
                            self.match(self.input, 56, self.FOLLOW_56_in_expr_bitshift2533)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2547)
                        e2 = self.expr_add()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop35





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitshift"



    # $ANTLR start "expr_bitand"
    # src/ll/UL4.g:525:1: expr_bitand returns [node] : e1= expr_bitshift ( '&' e2= expr_bitshift )* ;
    def expr_bitand(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:526:2: (e1= expr_bitshift ( '&' e2= expr_bitshift )* )
                # src/ll/UL4.g:527:3: e1= expr_bitshift ( '&' e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2575)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:528:3: ( '&' e2= expr_bitshift )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 30) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:529:4: '&' e2= expr_bitshift
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr_bitand2586)

                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2593)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitAnd.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop36





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitand"



    # $ANTLR start "expr_bitxor"
    # src/ll/UL4.g:535:1: expr_bitxor returns [node] : e1= expr_bitand ( '^' e2= expr_bitand )* ;
    def expr_bitxor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:536:2: (e1= expr_bitand ( '^' e2= expr_bitand )* )
                # src/ll/UL4.g:537:3: e1= expr_bitand ( '^' e2= expr_bitand )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2621)
                e1 = self.expr_bitand()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:538:3: ( '^' e2= expr_bitand )*
                while True: #loop37
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if (LA37_0 == 60) :
                        alt37 = 1


                    if alt37 == 1:
                        # src/ll/UL4.g:539:4: '^' e2= expr_bitand
                        pass 
                        self.match(self.input, 60, self.FOLLOW_60_in_expr_bitxor2632)

                        self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2639)
                        e2 = self.expr_bitand()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitXOr.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop37





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitxor"



    # $ANTLR start "expr_bitor"
    # src/ll/UL4.g:545:1: expr_bitor returns [node] : e1= expr_bitxor ( '|' e2= expr_bitxor )* ;
    def expr_bitor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:546:2: (e1= expr_bitxor ( '|' e2= expr_bitxor )* )
                # src/ll/UL4.g:547:3: e1= expr_bitxor ( '|' e2= expr_bitxor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2667)
                e1 = self.expr_bitxor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:548:3: ( '|' e2= expr_bitxor )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 71) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:549:4: '|' e2= expr_bitxor
                        pass 
                        self.match(self.input, 71, self.FOLLOW_71_in_expr_bitor2678)

                        self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2685)
                        e2 = self.expr_bitxor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitOr.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop38





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitor"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:555:1: expr_cmp returns [node] : e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:556:2: (e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )* )
                # src/ll/UL4.g:557:3: e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2713)
                e1 = self.expr_bitor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:558:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 68) :
                        LA40_2 = self.input.LA(2)

                        if (LA40_2 == 66) :
                            alt40 = 1


                    elif (LA40_0 == 27 or LA40_0 == 48 or LA40_0 == 51 or (53 <= LA40_0 <= 55) or (66 <= LA40_0 <= 67)) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:559:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor
                        pass 
                        # src/ll/UL4.g:559:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' )
                        alt39 = 10
                        LA39 = self.input.LA(1)
                        if LA39 == 53:
                            alt39 = 1
                        elif LA39 == 27:
                            alt39 = 2
                        elif LA39 == 48:
                            alt39 = 3
                        elif LA39 == 51:
                            alt39 = 4
                        elif LA39 == 54:
                            alt39 = 5
                        elif LA39 == 55:
                            alt39 = 6
                        elif LA39 == 66:
                            alt39 = 7
                        elif LA39 == 68:
                            alt39 = 8
                        elif LA39 == 67:
                            LA39_9 = self.input.LA(2)

                            if (LA39_9 == 68) :
                                alt39 = 10
                            elif ((COLOR <= LA39_9 <= DATE) or (FALSE <= LA39_9 <= FLOAT) or (INT <= LA39_9 <= NONE) or (STRING <= LA39_9 <= STRING3) or LA39_9 == TRUE or LA39_9 == 32 or LA39_9 == 40 or LA39_9 == 58 or LA39_9 == 70 or LA39_9 == 74) :
                                alt39 = 9
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 39, 9, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:560:5: '=='
                            pass 
                            self.match(self.input, 53, self.FOLLOW_53_in_expr_cmp2730)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:562:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr_cmp2743)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt39 == 3:
                            # src/ll/UL4.g:564:5: '<'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr_cmp2756)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt39 == 4:
                            # src/ll/UL4.g:566:5: '<='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr_cmp2769)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt39 == 5:
                            # src/ll/UL4.g:568:5: '>'
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_cmp2782)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt39 == 6:
                            # src/ll/UL4.g:570:5: '>='
                            pass 
                            self.match(self.input, 55, self.FOLLOW_55_in_expr_cmp2795)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 




                        elif alt39 == 7:
                            # src/ll/UL4.g:572:5: 'in'
                            pass 
                            self.match(self.input, 66, self.FOLLOW_66_in_expr_cmp2808)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Contains; 




                        elif alt39 == 8:
                            # src/ll/UL4.g:574:5: 'not' 'in'
                            pass 
                            self.match(self.input, 68, self.FOLLOW_68_in_expr_cmp2821)

                            self.match(self.input, 66, self.FOLLOW_66_in_expr_cmp2823)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NotContains; 




                        elif alt39 == 9:
                            # src/ll/UL4.g:576:5: 'is'
                            pass 
                            self.match(self.input, 67, self.FOLLOW_67_in_expr_cmp2836)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Is; 




                        elif alt39 == 10:
                            # src/ll/UL4.g:578:5: 'is' 'not'
                            pass 
                            self.match(self.input, 67, self.FOLLOW_67_in_expr_cmp2849)

                            self.match(self.input, 68, self.FOLLOW_68_in_expr_cmp2851)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.IsNot; 






                        self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2865)
                        e2 = self.expr_bitor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop40





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_not"
    # src/ll/UL4.g:585:1: expr_not returns [node] : (e1= expr_cmp |n= 'not' e2= expr_not );
    def expr_not(self, ):
        node = None


        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:586:2: (e1= expr_cmp |n= 'not' e2= expr_not )
                alt41 = 2
                LA41_0 = self.input.LA(1)

                if ((COLOR <= LA41_0 <= DATE) or (FALSE <= LA41_0 <= FLOAT) or (INT <= LA41_0 <= NONE) or (STRING <= LA41_0 <= STRING3) or LA41_0 == TRUE or LA41_0 == 32 or LA41_0 == 40 or LA41_0 == 58 or LA41_0 == 70 or LA41_0 == 74) :
                    alt41 = 1
                elif (LA41_0 == 68) :
                    alt41 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 41, 0, self.input)

                    raise nvae


                if alt41 == 1:
                    # src/ll/UL4.g:587:3: e1= expr_cmp
                    pass 
                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_not2893)
                    e1 = self.expr_cmp()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt41 == 2:
                    # src/ll/UL4.g:589:3: n= 'not' e2= expr_not
                    pass 
                    n = self.match(self.input, 68, self.FOLLOW_68_in_expr_not2904)

                    self._state.following.append(self.FOLLOW_expr_not_in_expr_not2908)
                    e2 = self.expr_not()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(self.tag, slice(self.startpos(n), e2.pos.stop), e2) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_not"



    # $ANTLR start "expr_and"
    # src/ll/UL4.g:594:1: expr_and returns [node] : e1= expr_not ( 'and' e2= expr_not )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:595:2: (e1= expr_not ( 'and' e2= expr_not )* )
                # src/ll/UL4.g:596:3: e1= expr_not ( 'and' e2= expr_not )*
                pass 
                self._state.following.append(self.FOLLOW_expr_not_in_expr_and2932)
                e1 = self.expr_not()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:597:3: ( 'and' e2= expr_not )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 62) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:598:4: 'and' e2= expr_not
                        pass 
                        self.match(self.input, 62, self.FOLLOW_62_in_expr_and2943)

                        self._state.following.append(self.FOLLOW_expr_not_in_expr_and2950)
                        e2 = self.expr_not()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop42





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_and"



    # $ANTLR start "expr_or"
    # src/ll/UL4.g:604:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:605:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:606:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or2978)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:607:3: ( 'or' e2= expr_and )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 69) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:608:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 69, self.FOLLOW_69_in_expr_or2989)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or2996)
                        e2 = self.expr_and()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.tag, slice(node.pos.start, e2.pos.stop), node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_or"



    # $ANTLR start "expr_if"
    # src/ll/UL4.g:614:1: expr_if returns [node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:615:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:616:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if3024)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:617:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if (LA44_0 == 65) :
                    LA44_1 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt44 = 1
                if alt44 == 1:
                    # src/ll/UL4.g:618:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_expr_if3035)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3042)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 63, self.FOLLOW_63_in_expr_if3047)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3054)
                    e3 = self.expr_or()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.If.make(self.tag, slice(e1.pos.start, e3.pos.stop), node, e2, e3) 









                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_if"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:625:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:626:2: (ege= generatorexpression |e1= expr_if )
                alt45 = 2
                LA45 = self.input.LA(1)
                if LA45 == NONE:
                    LA45_1 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 1, self.input)

                        raise nvae


                elif LA45 == FALSE:
                    LA45_2 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 2, self.input)

                        raise nvae


                elif LA45 == TRUE:
                    LA45_3 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 3, self.input)

                        raise nvae


                elif LA45 == INT:
                    LA45_4 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 4, self.input)

                        raise nvae


                elif LA45 == FLOAT:
                    LA45_5 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 5, self.input)

                        raise nvae


                elif LA45 == STRING:
                    LA45_6 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 6, self.input)

                        raise nvae


                elif LA45 == STRING3:
                    LA45_7 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 7, self.input)

                        raise nvae


                elif LA45 == DATE:
                    LA45_8 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 8, self.input)

                        raise nvae


                elif LA45 == COLOR:
                    LA45_9 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 9, self.input)

                        raise nvae


                elif LA45 == NAME:
                    LA45_10 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 10, self.input)

                        raise nvae


                elif LA45 == 58:
                    LA45_11 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 11, self.input)

                        raise nvae


                elif LA45 == 70:
                    LA45_12 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 12, self.input)

                        raise nvae


                elif LA45 == 32:
                    LA45_13 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 13, self.input)

                        raise nvae


                elif LA45 == 40:
                    LA45_14 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 14, self.input)

                        raise nvae


                elif LA45 == 74:
                    LA45_15 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 15, self.input)

                        raise nvae


                elif LA45 == 68:
                    LA45_16 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 45, 0, self.input)

                    raise nvae


                if alt45 == 1:
                    # src/ll/UL4.g:626:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg3078)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt45 == 2:
                    # src/ll/UL4.g:627:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg3087)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "exprarg"



    # $ANTLR start "expression"
    # src/ll/UL4.g:630:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:631:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt46 = 2
                LA46 = self.input.LA(1)
                if LA46 == NONE:
                    LA46_1 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 1, self.input)

                        raise nvae


                elif LA46 == FALSE:
                    LA46_2 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 2, self.input)

                        raise nvae


                elif LA46 == TRUE:
                    LA46_3 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 3, self.input)

                        raise nvae


                elif LA46 == INT:
                    LA46_4 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 4, self.input)

                        raise nvae


                elif LA46 == FLOAT:
                    LA46_5 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 5, self.input)

                        raise nvae


                elif LA46 == STRING:
                    LA46_6 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 6, self.input)

                        raise nvae


                elif LA46 == STRING3:
                    LA46_7 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 7, self.input)

                        raise nvae


                elif LA46 == DATE:
                    LA46_8 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 8, self.input)

                        raise nvae


                elif LA46 == COLOR:
                    LA46_9 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 9, self.input)

                        raise nvae


                elif LA46 == NAME:
                    LA46_10 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 10, self.input)

                        raise nvae


                elif LA46 == 58:
                    LA46_11 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 11, self.input)

                        raise nvae


                elif LA46 == 70:
                    LA46_12 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 12, self.input)

                        raise nvae


                elif LA46 == 32:
                    LA46_13 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 13, self.input)

                        raise nvae


                elif LA46 == 40:
                    LA46_14 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 14, self.input)

                        raise nvae


                elif LA46 == 74:
                    LA46_15 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 15, self.input)

                        raise nvae


                elif LA46 == 68:
                    LA46_16 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 46, 0, self.input)

                    raise nvae


                if alt46 == 1:
                    # src/ll/UL4.g:631:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3106)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3108)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:632:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3117)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3119)

                    if self._state.backtracking == 0:
                        pass
                        node =  e 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expression"



    # $ANTLR start "for_"
    # src/ll/UL4.g:638:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:639:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:640:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3144)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_for_3148)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3154)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ForBlock(self.tag, slice(self.startpos(n.start), e.pos.stop), ((n is not None) and [n.lvalue] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3160)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:649:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:650:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF )
                alt47 = 13
                LA47 = self.input.LA(1)
                if LA47 == NONE:
                    LA47_1 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 1, self.input)

                        raise nvae


                elif LA47 == FALSE:
                    LA47_2 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 2, self.input)

                        raise nvae


                elif LA47 == TRUE:
                    LA47_3 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 3, self.input)

                        raise nvae


                elif LA47 == INT:
                    LA47_4 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 4, self.input)

                        raise nvae


                elif LA47 == FLOAT:
                    LA47_5 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 5, self.input)

                        raise nvae


                elif LA47 == STRING:
                    LA47_6 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 6, self.input)

                        raise nvae


                elif LA47 == STRING3:
                    LA47_7 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 7, self.input)

                        raise nvae


                elif LA47 == DATE:
                    LA47_8 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 8, self.input)

                        raise nvae


                elif LA47 == COLOR:
                    LA47_9 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 9, self.input)

                        raise nvae


                elif LA47 == NAME:
                    LA47_10 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 10, self.input)

                        raise nvae


                elif LA47 == 58:
                    LA47_11 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 11, self.input)

                        raise nvae


                elif LA47 == 70:
                    LA47_12 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 12, self.input)

                        raise nvae


                elif LA47 == 32:
                    LA47_13 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt47 = 1
                    elif (self.synpred79_UL4()) :
                        alt47 = 2
                    elif (self.synpred80_UL4()) :
                        alt47 = 3
                    elif (self.synpred81_UL4()) :
                        alt47 = 4
                    elif (self.synpred82_UL4()) :
                        alt47 = 5
                    elif (self.synpred83_UL4()) :
                        alt47 = 6
                    elif (self.synpred84_UL4()) :
                        alt47 = 7
                    elif (self.synpred85_UL4()) :
                        alt47 = 8
                    elif (self.synpred86_UL4()) :
                        alt47 = 9
                    elif (self.synpred87_UL4()) :
                        alt47 = 10
                    elif (self.synpred88_UL4()) :
                        alt47 = 11
                    elif (self.synpred89_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 13, self.input)

                        raise nvae


                elif LA47 == 40 or LA47 == 68 or LA47 == 74:
                    alt47 = 13
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 47, 0, self.input)

                    raise nvae


                if alt47 == 1:
                    # src/ll/UL4.g:650:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3181)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_statement3183)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3187)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3189)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.tag, self.tag.codepos, ((nn is not None) and [nn.lvalue] or [None])[0], e) 




                elif alt47 == 2:
                    # src/ll/UL4.g:651:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3198)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 38, self.FOLLOW_38_in_statement3200)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3204)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3206)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 3:
                    # src/ll/UL4.g:652:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3215)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement3217)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3221)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3223)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 4:
                    # src/ll/UL4.g:653:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3232)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement3234)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3238)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3240)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 5:
                    # src/ll/UL4.g:654:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3249)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement3251)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3255)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3257)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 6:
                    # src/ll/UL4.g:655:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3266)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement3268)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3272)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3274)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 7:
                    # src/ll/UL4.g:656:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3283)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3285)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3289)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3291)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 8:
                    # src/ll/UL4.g:657:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3300)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 50, self.FOLLOW_50_in_statement3302)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3306)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3308)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 9:
                    # src/ll/UL4.g:658:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3317)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 57, self.FOLLOW_57_in_statement3319)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3323)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3325)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 10:
                    # src/ll/UL4.g:659:4: n= expr_subscript '&=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3334)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement3336)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3340)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3342)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitAndVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 11:
                    # src/ll/UL4.g:660:4: n= expr_subscript '^=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3351)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 61, self.FOLLOW_61_in_statement3353)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3357)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3359)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitXOrVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 12:
                    # src/ll/UL4.g:661:4: n= expr_subscript '|=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3368)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 72, self.FOLLOW_72_in_statement3370)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3374)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3376)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitOrVar(self.tag, self.tag.codepos, n, e) 




                elif alt47 == 13:
                    # src/ll/UL4.g:662:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3385)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3387)

                    if self._state.backtracking == 0:
                        pass
                        node = e 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "statement"



    # $ANTLR start "definition"
    # src/ll/UL4.g:668:1: definition returns [node] : (n= name )? (sig= signature )? EOF ;
    def definition(self, ):
        node = None


        n = None
        sig = None

        try:
            try:
                # src/ll/UL4.g:669:2: ( (n= name )? (sig= signature )? EOF )
                # src/ll/UL4.g:670:3: (n= name )? (sig= signature )? EOF
                pass 
                if self._state.backtracking == 0:
                    pass
                    node =  (None, None) 



                # src/ll/UL4.g:671:3: (n= name )?
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if (LA48_0 == NAME) :
                    alt48 = 1
                if alt48 == 1:
                    # src/ll/UL4.g:672:4: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_definition3421)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], None) 






                # src/ll/UL4.g:674:3: (sig= signature )?
                alt49 = 2
                LA49_0 = self.input.LA(1)

                if (LA49_0 == 32) :
                    alt49 = 1
                if alt49 == 1:
                    # src/ll/UL4.g:675:4: sig= signature
                    pass 
                    self._state.following.append(self.FOLLOW_signature_in_definition3439)
                    sig = self.signature()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (node[0], sig) 






                self.match(self.input, EOF, self.FOLLOW_EOF_in_definition3450)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "definition"



    # $ANTLR start "signature"
    # src/ll/UL4.g:682:1: signature returns [node] : open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF ;
    def signature(self, ):
        node = None


        open = None
        close = None
        rkwargsname = None
        rargsname = None
        aname1 = None
        adefault1 = None
        aname2 = None
        adefault2 = None
        aname3 = None
        adefault3 = None

        try:
            try:
                # src/ll/UL4.g:683:2: (open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF )
                # src/ll/UL4.g:684:2: open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF
                pass 
                open = self.match(self.input, 32, self.FOLLOW_32_in_signature3471)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Signature(self.tag, slice(self.startpos(open), None)) 



                # src/ll/UL4.g:685:2: (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? )
                alt62 = 5
                LA62 = self.input.LA(1)
                if LA62 == 33:
                    alt62 = 1
                elif LA62 == 35:
                    alt62 = 2
                elif LA62 == 34:
                    alt62 = 3
                elif LA62 == NAME:
                    LA62_4 = self.input.LA(2)

                    if (LA62_4 == 52) :
                        alt62 = 4
                    elif (LA62_4 == 33 or LA62_4 == 39) :
                        alt62 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 62, 4, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 62, 0, self.input)

                    raise nvae


                if alt62 == 1:
                    # src/ll/UL4.g:687:2: 
                    pass 

                elif alt62 == 2:
                    # src/ll/UL4.g:689:3: '**' rkwargsname= name ( ',' )?
                    pass 
                    self.match(self.input, 35, self.FOLLOW_35_in_signature3491)

                    self._state.following.append(self.FOLLOW_name_in_signature3495)
                    rkwargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:690:3: ( ',' )?
                    alt50 = 2
                    LA50_0 = self.input.LA(1)

                    if (LA50_0 == 39) :
                        alt50 = 1
                    if alt50 == 1:
                        # src/ll/UL4.g:690:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3501)





                elif alt62 == 3:
                    # src/ll/UL4.g:693:3: '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self.match(self.input, 34, self.FOLLOW_34_in_signature3513)

                    self._state.following.append(self.FOLLOW_name_in_signature3517)
                    rargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:694:3: ( ',' '**' rkwargsname= name )?
                    alt51 = 2
                    LA51_0 = self.input.LA(1)

                    if (LA51_0 == 39) :
                        LA51_1 = self.input.LA(2)

                        if (LA51_1 == 35) :
                            alt51 = 1
                    if alt51 == 1:
                        # src/ll/UL4.g:695:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3528)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3533)

                        self._state.following.append(self.FOLLOW_name_in_signature3537)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:698:3: ( ',' )?
                    alt52 = 2
                    LA52_0 = self.input.LA(1)

                    if (LA52_0 == 39) :
                        alt52 = 1
                    if alt52 == 1:
                        # src/ll/UL4.g:698:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3548)





                elif alt62 == 4:
                    # src/ll/UL4.g:701:3: aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3562)
                    aname1 = self.name()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_signature3566)

                    self._state.following.append(self.FOLLOW_exprarg_in_signature3572)
                    adefault1 = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], adefault1)); 



                    # src/ll/UL4.g:704:3: ( ',' aname2= name '=' adefault2= exprarg )*
                    while True: #loop53
                        alt53 = 2
                        LA53_0 = self.input.LA(1)

                        if (LA53_0 == 39) :
                            LA53_1 = self.input.LA(2)

                            if (LA53_1 == NAME) :
                                alt53 = 1




                        if alt53 == 1:
                            # src/ll/UL4.g:705:4: ',' aname2= name '=' adefault2= exprarg
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3583)

                            self._state.following.append(self.FOLLOW_name_in_signature3590)
                            aname2 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_signature3595)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3602)
                            adefault2 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], adefault2)); 




                        else:
                            break #loop53


                    # src/ll/UL4.g:710:3: ( ',' '*' rargsname= name )?
                    alt54 = 2
                    LA54_0 = self.input.LA(1)

                    if (LA54_0 == 39) :
                        LA54_1 = self.input.LA(2)

                        if (LA54_1 == 34) :
                            alt54 = 1
                    if alt54 == 1:
                        # src/ll/UL4.g:711:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3618)

                        self.match(self.input, 34, self.FOLLOW_34_in_signature3623)

                        self._state.following.append(self.FOLLOW_name_in_signature3627)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:714:3: ( ',' '**' rkwargsname= name )?
                    alt55 = 2
                    LA55_0 = self.input.LA(1)

                    if (LA55_0 == 39) :
                        LA55_1 = self.input.LA(2)

                        if (LA55_1 == 35) :
                            alt55 = 1
                    if alt55 == 1:
                        # src/ll/UL4.g:715:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3643)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3648)

                        self._state.following.append(self.FOLLOW_name_in_signature3652)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:718:3: ( ',' )?
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 39) :
                        alt56 = 1
                    if alt56 == 1:
                        # src/ll/UL4.g:718:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3663)





                elif alt62 == 5:
                    # src/ll/UL4.g:721:3: aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3677)
                    aname1 = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:722:3: ( ',' aname2= name )*
                    while True: #loop57
                        alt57 = 2
                        LA57_0 = self.input.LA(1)

                        if (LA57_0 == 39) :
                            LA57_1 = self.input.LA(2)

                            if (LA57_1 == NAME) :
                                LA57_3 = self.input.LA(3)

                                if (LA57_3 == 33 or LA57_3 == 39) :
                                    alt57 = 1






                        if alt57 == 1:
                            # src/ll/UL4.g:723:4: ',' aname2= name
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3688)

                            self._state.following.append(self.FOLLOW_name_in_signature3695)
                            aname2 = self.name()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], None)); 




                        else:
                            break #loop57


                    # src/ll/UL4.g:726:3: ( ',' aname3= name '=' adefault3= exprarg )*
                    while True: #loop58
                        alt58 = 2
                        LA58_0 = self.input.LA(1)

                        if (LA58_0 == 39) :
                            LA58_1 = self.input.LA(2)

                            if (LA58_1 == NAME) :
                                alt58 = 1




                        if alt58 == 1:
                            # src/ll/UL4.g:727:4: ',' aname3= name '=' adefault3= exprarg
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3711)

                            self._state.following.append(self.FOLLOW_name_in_signature3718)
                            aname3 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_signature3723)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3730)
                            adefault3 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname3 is not None) and [self.input.toString(aname3.start,aname3.stop)] or [None])[0], adefault3)); 




                        else:
                            break #loop58


                    # src/ll/UL4.g:732:3: ( ',' '*' rargsname= name )?
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if (LA59_0 == 39) :
                        LA59_1 = self.input.LA(2)

                        if (LA59_1 == 34) :
                            alt59 = 1
                    if alt59 == 1:
                        # src/ll/UL4.g:733:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3746)

                        self.match(self.input, 34, self.FOLLOW_34_in_signature3751)

                        self._state.following.append(self.FOLLOW_name_in_signature3755)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:736:3: ( ',' '**' rkwargsname= name )?
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == 39) :
                        LA60_1 = self.input.LA(2)

                        if (LA60_1 == 35) :
                            alt60 = 1
                    if alt60 == 1:
                        # src/ll/UL4.g:737:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3771)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3776)

                        self._state.following.append(self.FOLLOW_name_in_signature3780)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:740:3: ( ',' )?
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if (LA61_0 == 39) :
                        alt61 = 1
                    if alt61 == 1:
                        # src/ll/UL4.g:740:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3791)







                close = self.match(self.input, 33, self.FOLLOW_33_in_signature3800)

                if self._state.backtracking == 0:
                    pass
                    node.pos = slice(node.pos.start, self.stoppos(close)) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_signature3805)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "signature"

    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        e_list = None

        # src/ll/UL4.g:362:4: (e_list= list )
        # src/ll/UL4.g:362:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred26_UL41741)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred27_UL4"
    def synpred27_UL4_fragment(self, ):
        e_listcomp = None

        # src/ll/UL4.g:363:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:363:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred27_UL41750)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred27_UL4"



    # $ANTLR start "synpred28_UL4"
    def synpred28_UL4_fragment(self, ):
        e_set = None

        # src/ll/UL4.g:364:4: (e_set= set )
        # src/ll/UL4.g:364:4: e_set= set
        pass 
        self._state.following.append(self.FOLLOW_set_in_synpred28_UL41759)
        e_set = self.set()

        self._state.following.pop()



    # $ANTLR end "synpred28_UL4"



    # $ANTLR start "synpred29_UL4"
    def synpred29_UL4_fragment(self, ):
        e_setcomp = None

        # src/ll/UL4.g:365:4: (e_setcomp= setcomprehension )
        # src/ll/UL4.g:365:4: e_setcomp= setcomprehension
        pass 
        self._state.following.append(self.FOLLOW_setcomprehension_in_synpred29_UL41768)
        e_setcomp = self.setcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred29_UL4"



    # $ANTLR start "synpred30_UL4"
    def synpred30_UL4_fragment(self, ):
        e_dict = None

        # src/ll/UL4.g:366:4: (e_dict= dict )
        # src/ll/UL4.g:366:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred30_UL41777)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred30_UL4"



    # $ANTLR start "synpred31_UL4"
    def synpred31_UL4_fragment(self, ):
        e_dictcomp = None

        # src/ll/UL4.g:367:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:367:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred31_UL41786)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred31_UL4"



    # $ANTLR start "synpred32_UL4"
    def synpred32_UL4_fragment(self, ):
        open = None
        close = None
        e_genexpr = None

        # src/ll/UL4.g:368:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:368:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 32, self.FOLLOW_32_in_synpred32_UL41795)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred32_UL41799)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 33, self.FOLLOW_33_in_synpred32_UL41803)



    # $ANTLR end "synpred32_UL4"



    # $ANTLR start "synpred33_UL4"
    def synpred33_UL4_fragment(self, ):
        n = None

        # src/ll/UL4.g:381:3: (n= expr_subscript )
        # src/ll/UL4.g:381:3: n= expr_subscript
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred33_UL41843)
        n = self.expr_subscript()

        self._state.following.pop()



    # $ANTLR end "synpred33_UL4"



    # $ANTLR start "synpred34_UL4"
    def synpred34_UL4_fragment(self, ):
        n0 = None

        # src/ll/UL4.g:383:3: ( '(' n0= nestedlvalue ',' ')' )
        # src/ll/UL4.g:383:3: '(' n0= nestedlvalue ',' ')'
        pass 
        self.match(self.input, 32, self.FOLLOW_32_in_synpred34_UL41852)

        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred34_UL41856)
        n0 = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred34_UL41858)

        self.match(self.input, 33, self.FOLLOW_33_in_synpred34_UL41860)



    # $ANTLR end "synpred34_UL4"



    # $ANTLR start "synpred43_UL4"
    def synpred43_UL4_fragment(self, ):
        a2 = None

        # src/ll/UL4.g:448:6: ( ',' a2= argument )
        # src/ll/UL4.g:448:6: ',' a2= argument
        pass 
        self.match(self.input, 39, self.FOLLOW_39_in_synpred43_UL42151)

        self._state.following.append(self.FOLLOW_argument_in_synpred43_UL42160)
        a2 = self.argument()

        self._state.following.pop()



    # $ANTLR end "synpred43_UL4"



    # $ANTLR start "synpred46_UL4"
    def synpred46_UL4_fragment(self, ):
        close = None
        a1 = None
        a2 = None

        # src/ll/UL4.g:444:4: ( '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' )
        # src/ll/UL4.g:444:4: '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')'
        pass 
        self.match(self.input, 32, self.FOLLOW_32_in_synpred46_UL42121)

        # src/ll/UL4.g:445:4: (a1= argument ( ',' a2= argument )* ( ',' )? )*
        while True: #loop67
            alt67 = 2
            LA67_0 = self.input.LA(1)

            if ((COLOR <= LA67_0 <= DATE) or (FALSE <= LA67_0 <= FLOAT) or (INT <= LA67_0 <= NONE) or (STRING <= LA67_0 <= STRING3) or LA67_0 == TRUE or LA67_0 == 32 or (34 <= LA67_0 <= 35) or LA67_0 == 40 or LA67_0 == 58 or LA67_0 == 68 or LA67_0 == 70 or LA67_0 == 74) :
                alt67 = 1


            if alt67 == 1:
                # src/ll/UL4.g:446:5: a1= argument ( ',' a2= argument )* ( ',' )?
                pass 
                self._state.following.append(self.FOLLOW_argument_in_synpred46_UL42136)
                a1 = self.argument()

                self._state.following.pop()

                # src/ll/UL4.g:447:5: ( ',' a2= argument )*
                while True: #loop65
                    alt65 = 2
                    LA65_0 = self.input.LA(1)

                    if (LA65_0 == 39) :
                        LA65_1 = self.input.LA(2)

                        if (self.synpred43_UL4()) :
                            alt65 = 1




                    if alt65 == 1:
                        # src/ll/UL4.g:448:6: ',' a2= argument
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_synpred46_UL42151)

                        self._state.following.append(self.FOLLOW_argument_in_synpred46_UL42160)
                        a2 = self.argument()

                        self._state.following.pop()


                    else:
                        break #loop65


                # src/ll/UL4.g:451:5: ( ',' )?
                alt66 = 2
                LA66_0 = self.input.LA(1)

                if (LA66_0 == 39) :
                    alt66 = 1
                if alt66 == 1:
                    # src/ll/UL4.g:451:5: ','
                    pass 
                    self.match(self.input, 39, self.FOLLOW_39_in_synpred46_UL42175)





            else:
                break #loop67


        close = self.match(self.input, 33, self.FOLLOW_33_in_synpred46_UL42189)



    # $ANTLR end "synpred46_UL4"



    # $ANTLR start "synpred47_UL4"
    def synpred47_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:456:4: ( '[' e2= expr_if close= ']' )
        # src/ll/UL4.g:456:4: '[' e2= expr_if close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred47_UL42205)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred47_UL42213)
        e2 = self.expr_if()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred47_UL42220)



    # $ANTLR end "synpred47_UL4"



    # $ANTLR start "synpred48_UL4"
    def synpred48_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:461:4: ( '[' e2= slice close= ']' )
        # src/ll/UL4.g:461:4: '[' e2= slice close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred48_UL42236)

        self._state.following.append(self.FOLLOW_slice_in_synpred48_UL42244)
        e2 = self.slice()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred48_UL42251)



    # $ANTLR end "synpred48_UL4"



    # $ANTLR start "synpred54_UL4"
    def synpred54_UL4_fragment(self, ):
        e2 = None

        # src/ll/UL4.g:483:4: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )
        # src/ll/UL4.g:483:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
        pass 
        if self.input.LA(1) == 28 or self.input.LA(1) == 34 or (43 <= self.input.LA(1) <= 44):
            self.input.consume()
            self._state.errorRecovery = False


        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed


            mse = MismatchedSetException(None, self.input)
            raise mse



        self._state.following.append(self.FOLLOW_expr_unary_in_synpred54_UL42403)
        e2 = self.expr_unary()

        self._state.following.pop()



    # $ANTLR end "synpred54_UL4"



    # $ANTLR start "synpred56_UL4"
    def synpred56_UL4_fragment(self, ):
        e2 = None

        # src/ll/UL4.g:501:4: ( ( '+' | '-' ) e2= expr_mul )
        # src/ll/UL4.g:501:4: ( '+' | '-' ) e2= expr_mul
        pass 
        if self.input.LA(1) == 37 or self.input.LA(1) == 40:
            self.input.consume()
            self._state.errorRecovery = False


        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed


            mse = MismatchedSetException(None, self.input)
            raise mse



        self._state.following.append(self.FOLLOW_expr_mul_in_synpred56_UL42475)
        e2 = self.expr_mul()

        self._state.following.pop()



    # $ANTLR end "synpred56_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:618:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:618:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 65, self.FOLLOW_65_in_synpred75_UL43035)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred75_UL43042)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 63, self.FOLLOW_63_in_synpred75_UL43047)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred75_UL43054)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:626:4: (ege= generatorexpression )
        # src/ll/UL4.g:626:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred76_UL43078)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:631:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:631:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred77_UL43106)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL43108)



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:650:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:650:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred78_UL43181)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 52, self.FOLLOW_52_in_synpred78_UL43183)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred78_UL43187)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43189)



    # $ANTLR end "synpred78_UL4"



    # $ANTLR start "synpred79_UL4"
    def synpred79_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:651:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:651:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred79_UL43198)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 38, self.FOLLOW_38_in_synpred79_UL43200)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred79_UL43204)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred79_UL43206)



    # $ANTLR end "synpred79_UL4"



    # $ANTLR start "synpred80_UL4"
    def synpred80_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:652:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:652:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred80_UL43215)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred80_UL43217)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred80_UL43221)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred80_UL43223)



    # $ANTLR end "synpred80_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:653:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:653:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred81_UL43232)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred81_UL43234)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred81_UL43238)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred81_UL43240)



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:654:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:654:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred82_UL43249)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred82_UL43251)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred82_UL43255)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred82_UL43257)



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:655:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:655:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred83_UL43266)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 45, self.FOLLOW_45_in_synpred83_UL43268)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred83_UL43272)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43274)



    # $ANTLR end "synpred83_UL4"



    # $ANTLR start "synpred84_UL4"
    def synpred84_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:656:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:656:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred84_UL43283)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred84_UL43285)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred84_UL43289)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred84_UL43291)



    # $ANTLR end "synpred84_UL4"



    # $ANTLR start "synpred85_UL4"
    def synpred85_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:657:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:657:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred85_UL43300)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 50, self.FOLLOW_50_in_synpred85_UL43302)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred85_UL43306)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred85_UL43308)



    # $ANTLR end "synpred85_UL4"



    # $ANTLR start "synpred86_UL4"
    def synpred86_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:658:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:658:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred86_UL43317)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 57, self.FOLLOW_57_in_synpred86_UL43319)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred86_UL43323)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred86_UL43325)



    # $ANTLR end "synpred86_UL4"



    # $ANTLR start "synpred87_UL4"
    def synpred87_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:659:4: (n= expr_subscript '&=' e= expr_if EOF )
        # src/ll/UL4.g:659:4: n= expr_subscript '&=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred87_UL43334)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 31, self.FOLLOW_31_in_synpred87_UL43336)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred87_UL43340)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred87_UL43342)



    # $ANTLR end "synpred87_UL4"



    # $ANTLR start "synpred88_UL4"
    def synpred88_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:660:4: (n= expr_subscript '^=' e= expr_if EOF )
        # src/ll/UL4.g:660:4: n= expr_subscript '^=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred88_UL43351)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 61, self.FOLLOW_61_in_synpred88_UL43353)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred88_UL43357)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred88_UL43359)



    # $ANTLR end "synpred88_UL4"



    # $ANTLR start "synpred89_UL4"
    def synpred89_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:661:4: (n= expr_subscript '|=' e= expr_if EOF )
        # src/ll/UL4.g:661:4: n= expr_subscript '|=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred89_UL43368)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 72, self.FOLLOW_72_in_synpred89_UL43370)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred89_UL43374)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred89_UL43376)



    # $ANTLR end "synpred89_UL4"




    def synpred76_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred76_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred31_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred31_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred79_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred79_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred87_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred87_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred43_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred43_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred78_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred78_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred48_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred48_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred84_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred84_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred81_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred81_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred30_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred30_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred33_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred33_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred83_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred83_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred34_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred34_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred27_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred27_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred46_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred46_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred89_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred89_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred32_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred32_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred86_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred86_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred77_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred77_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred47_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred47_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred75_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred75_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred29_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred29_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred80_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred80_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred26_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred26_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred88_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred88_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred56_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred56_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred28_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred28_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred54_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred54_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred85_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred85_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred82_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred82_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success



    # lookup tables for DFA #28

    DFA28_eot = DFA.unpack(
        u"\77\uffff"
        )

    DFA28_eof = DFA.unpack(
        u"\1\1\76\uffff"
        )

    DFA28_min = DFA.unpack(
        u"\1\5\51\uffff\1\0\1\uffff\1\0\22\uffff"
        )

    DFA28_max = DFA.unpack(
        u"\1\112\51\uffff\1\0\1\uffff\1\0\22\uffff"
        )

    DFA28_accept = DFA.unpack(
        u"\1\uffff\1\5\71\uffff\1\1\1\3\1\4\1\2"
        )

    DFA28_special = DFA.unpack(
        u"\52\uffff\1\0\1\uffff\1\1\22\uffff"
        )


    DFA28_transition = [
        DFA.unpack(u"\2\1\3\uffff\2\1\1\uffff\3\1\1\uffff\2\1\3\uffff\1\1"
        u"\4\uffff\5\1\1\54\11\1\1\73\17\1\1\52\20\1"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\uffff"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\uffff"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #28

    class DFA28(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA28_42 = input.LA(1)

                 
                index28_42 = input.index()
                input.rewind()

                s = -1
                if (self.synpred47_UL4()):
                    s = 60

                elif (self.synpred48_UL4()):
                    s = 61

                elif (True):
                    s = 1

                 
                input.seek(index28_42)

                if s >= 0:
                    return s
            elif s == 1: 
                LA28_44 = input.LA(1)

                 
                index28_44 = input.index()
                input.rewind()

                s = -1
                if (self.synpred46_UL4()):
                    s = 62

                elif (True):
                    s = 1

                 
                input.seek(index28_44)

                if s >= 0:
                    return s

            if self._state.backtracking > 0:
                raise BacktrackingFailed

            nvae = NoViableAltException(self_.getDescription(), 28, _s, input)
            self_.error(nvae)
            raise nvae

 

    FOLLOW_NONE_in_none799 = frozenset([1])
    FOLLOW_TRUE_in_true_816 = frozenset([1])
    FOLLOW_FALSE_in_false_833 = frozenset([1])
    FOLLOW_INT_in_int_850 = frozenset([1])
    FOLLOW_FLOAT_in_float_867 = frozenset([1])
    FOLLOW_STRING_in_string884 = frozenset([1])
    FOLLOW_STRING3_in_string891 = frozenset([1])
    FOLLOW_DATE_in_date908 = frozenset([1])
    FOLLOW_COLOR_in_color925 = frozenset([1])
    FOLLOW_NAME_in_name942 = frozenset([1])
    FOLLOW_none_in_literal961 = frozenset([1])
    FOLLOW_false__in_literal970 = frozenset([1])
    FOLLOW_true__in_literal979 = frozenset([1])
    FOLLOW_int__in_literal988 = frozenset([1])
    FOLLOW_float__in_literal997 = frozenset([1])
    FOLLOW_string_in_literal1006 = frozenset([1])
    FOLLOW_date_in_literal1015 = frozenset([1])
    FOLLOW_color_in_literal1024 = frozenset([1])
    FOLLOW_name_in_literal1033 = frozenset([1])
    FOLLOW_expr_if_in_seqitem1058 = frozenset([1])
    FOLLOW_34_in_seqitem1069 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_seqitem1075 = frozenset([1])
    FOLLOW_58_in_list1096 = frozenset([59])
    FOLLOW_59_in_list1102 = frozenset([1])
    FOLLOW_58_in_list1113 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 40, 58, 68, 70, 74])
    FOLLOW_seqitem_in_list1121 = frozenset([39, 59])
    FOLLOW_39_in_list1132 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 40, 58, 68, 70, 74])
    FOLLOW_seqitem_in_list1139 = frozenset([39, 59])
    FOLLOW_39_in_list1150 = frozenset([59])
    FOLLOW_59_in_list1157 = frozenset([1])
    FOLLOW_58_in_listcomprehension1185 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_listcomprehension1191 = frozenset([64])
    FOLLOW_64_in_listcomprehension1195 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_listcomprehension1201 = frozenset([66])
    FOLLOW_66_in_listcomprehension1205 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_listcomprehension1211 = frozenset([59, 65])
    FOLLOW_65_in_listcomprehension1220 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_listcomprehension1227 = frozenset([59])
    FOLLOW_59_in_listcomprehension1240 = frozenset([1])
    FOLLOW_70_in_set1263 = frozenset([43])
    FOLLOW_43_in_set1267 = frozenset([73])
    FOLLOW_73_in_set1273 = frozenset([1])
    FOLLOW_70_in_set1284 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 40, 58, 68, 70, 74])
    FOLLOW_seqitem_in_set1292 = frozenset([39, 73])
    FOLLOW_39_in_set1303 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 40, 58, 68, 70, 74])
    FOLLOW_seqitem_in_set1310 = frozenset([39, 73])
    FOLLOW_39_in_set1321 = frozenset([73])
    FOLLOW_73_in_set1328 = frozenset([1])
    FOLLOW_70_in_setcomprehension1356 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_setcomprehension1362 = frozenset([64])
    FOLLOW_64_in_setcomprehension1366 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_setcomprehension1372 = frozenset([66])
    FOLLOW_66_in_setcomprehension1376 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_setcomprehension1382 = frozenset([65, 73])
    FOLLOW_65_in_setcomprehension1391 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_setcomprehension1398 = frozenset([73])
    FOLLOW_73_in_setcomprehension1411 = frozenset([1])
    FOLLOW_expr_if_in_dictitem1436 = frozenset([47])
    FOLLOW_47_in_dictitem1440 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictitem1446 = frozenset([1])
    FOLLOW_35_in_dictitem1457 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictitem1463 = frozenset([1])
    FOLLOW_70_in_dict1484 = frozenset([73])
    FOLLOW_73_in_dict1490 = frozenset([1])
    FOLLOW_70_in_dict1501 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 35, 40, 58, 68, 70, 74])
    FOLLOW_dictitem_in_dict1509 = frozenset([39, 73])
    FOLLOW_39_in_dict1520 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 35, 40, 58, 68, 70, 74])
    FOLLOW_dictitem_in_dict1527 = frozenset([39, 73])
    FOLLOW_39_in_dict1538 = frozenset([73])
    FOLLOW_73_in_dict1545 = frozenset([1])
    FOLLOW_70_in_dictcomprehension1573 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictcomprehension1579 = frozenset([47])
    FOLLOW_47_in_dictcomprehension1583 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictcomprehension1589 = frozenset([64])
    FOLLOW_64_in_dictcomprehension1593 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_dictcomprehension1599 = frozenset([66])
    FOLLOW_66_in_dictcomprehension1603 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictcomprehension1609 = frozenset([65, 73])
    FOLLOW_65_in_dictcomprehension1618 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_dictcomprehension1625 = frozenset([73])
    FOLLOW_73_in_dictcomprehension1638 = frozenset([1])
    FOLLOW_expr_if_in_generatorexpression1666 = frozenset([64])
    FOLLOW_64_in_generatorexpression1672 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_generatorexpression1678 = frozenset([66])
    FOLLOW_66_in_generatorexpression1682 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_generatorexpression1688 = frozenset([1, 65])
    FOLLOW_65_in_generatorexpression1699 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_generatorexpression1706 = frozenset([1])
    FOLLOW_literal_in_atom1732 = frozenset([1])
    FOLLOW_list_in_atom1741 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1750 = frozenset([1])
    FOLLOW_set_in_atom1759 = frozenset([1])
    FOLLOW_setcomprehension_in_atom1768 = frozenset([1])
    FOLLOW_dict_in_atom1777 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1786 = frozenset([1])
    FOLLOW_32_in_atom1795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_generatorexpression_in_atom1799 = frozenset([33])
    FOLLOW_33_in_atom1803 = frozenset([1])
    FOLLOW_32_in_atom1812 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_atom1816 = frozenset([33])
    FOLLOW_33_in_atom1820 = frozenset([1])
    FOLLOW_expr_subscript_in_nestedlvalue1843 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1852 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_nestedlvalue1856 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1858 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1860 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1869 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_nestedlvalue1875 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1879 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_nestedlvalue1885 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1896 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_nestedlvalue1903 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1914 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1919 = frozenset([1])
    FOLLOW_expr_if_in_slice1952 = frozenset([47])
    FOLLOW_47_in_slice1965 = frozenset([1, 5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_slice1978 = frozenset([1])
    FOLLOW_exprarg_in_argument2010 = frozenset([1])
    FOLLOW_name_in_argument2021 = frozenset([52])
    FOLLOW_52_in_argument2023 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_argument2027 = frozenset([1])
    FOLLOW_34_in_argument2038 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_argument2044 = frozenset([1])
    FOLLOW_35_in_argument2055 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_argument2061 = frozenset([1])
    FOLLOW_atom_in_expr_subscript2082 = frozenset([1, 32, 42, 58])
    FOLLOW_42_in_expr_subscript2098 = frozenset([14])
    FOLLOW_name_in_expr_subscript2105 = frozenset([1, 32, 42, 58])
    FOLLOW_32_in_expr_subscript2121 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_argument_in_expr_subscript2136 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 39, 40, 58, 68, 70, 74])
    FOLLOW_39_in_expr_subscript2151 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_argument_in_expr_subscript2160 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 39, 40, 58, 68, 70, 74])
    FOLLOW_39_in_expr_subscript2175 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_33_in_expr_subscript2189 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2205 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_expr_subscript2213 = frozenset([59])
    FOLLOW_59_in_expr_subscript2220 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2236 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 68, 70, 74])
    FOLLOW_slice_in_expr_subscript2244 = frozenset([59])
    FOLLOW_59_in_expr_subscript2251 = frozenset([1, 32, 42, 58])
    FOLLOW_expr_subscript_in_expr_unary2279 = frozenset([1])
    FOLLOW_40_in_expr_unary2290 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_unary_in_expr_unary2294 = frozenset([1])
    FOLLOW_74_in_expr_unary2305 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_unary_in_expr_unary2309 = frozenset([1])
    FOLLOW_expr_unary_in_expr_mul2333 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_34_in_expr_mul2350 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_43_in_expr_mul2363 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_44_in_expr_mul2376 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_28_in_expr_mul2389 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_unary_in_expr_mul2403 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_expr_mul_in_expr_add2431 = frozenset([1, 37, 40])
    FOLLOW_37_in_expr_add2448 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_40_in_expr_add2461 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_mul_in_expr_add2475 = frozenset([1, 37, 40])
    FOLLOW_expr_add_in_expr_bitshift2503 = frozenset([1, 49, 56])
    FOLLOW_49_in_expr_bitshift2520 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_56_in_expr_bitshift2533 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_add_in_expr_bitshift2547 = frozenset([1, 49, 56])
    FOLLOW_expr_bitshift_in_expr_bitand2575 = frozenset([1, 30])
    FOLLOW_30_in_expr_bitand2586 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_bitshift_in_expr_bitand2593 = frozenset([1, 30])
    FOLLOW_expr_bitand_in_expr_bitxor2621 = frozenset([1, 60])
    FOLLOW_60_in_expr_bitxor2632 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_bitand_in_expr_bitxor2639 = frozenset([1, 60])
    FOLLOW_expr_bitxor_in_expr_bitor2667 = frozenset([1, 71])
    FOLLOW_71_in_expr_bitor2678 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_bitxor_in_expr_bitor2685 = frozenset([1, 71])
    FOLLOW_expr_bitor_in_expr_cmp2713 = frozenset([1, 27, 48, 51, 53, 54, 55, 66, 67, 68])
    FOLLOW_53_in_expr_cmp2730 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_27_in_expr_cmp2743 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_48_in_expr_cmp2756 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_51_in_expr_cmp2769 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_54_in_expr_cmp2782 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_55_in_expr_cmp2795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_66_in_expr_cmp2808 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_68_in_expr_cmp2821 = frozenset([66])
    FOLLOW_66_in_expr_cmp2823 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_67_in_expr_cmp2836 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_67_in_expr_cmp2849 = frozenset([68])
    FOLLOW_68_in_expr_cmp2851 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_bitor_in_expr_cmp2865 = frozenset([1, 27, 48, 51, 53, 54, 55, 66, 67, 68])
    FOLLOW_expr_cmp_in_expr_not2893 = frozenset([1])
    FOLLOW_68_in_expr_not2904 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_not_in_expr_not2908 = frozenset([1])
    FOLLOW_expr_not_in_expr_and2932 = frozenset([1, 62])
    FOLLOW_62_in_expr_and2943 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_not_in_expr_and2950 = frozenset([1, 62])
    FOLLOW_expr_and_in_expr_or2978 = frozenset([1, 69])
    FOLLOW_69_in_expr_or2989 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_and_in_expr_or2996 = frozenset([1, 69])
    FOLLOW_expr_or_in_expr_if3024 = frozenset([1, 65])
    FOLLOW_65_in_expr_if3035 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_or_in_expr_if3042 = frozenset([63])
    FOLLOW_63_in_expr_if3047 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_or_in_expr_if3054 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg3078 = frozenset([1])
    FOLLOW_expr_if_in_exprarg3087 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3106 = frozenset([])
    FOLLOW_EOF_in_expression3108 = frozenset([1])
    FOLLOW_expr_if_in_expression3117 = frozenset([])
    FOLLOW_EOF_in_expression3119 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3144 = frozenset([66])
    FOLLOW_66_in_for_3148 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_for_3154 = frozenset([])
    FOLLOW_EOF_in_for_3160 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3181 = frozenset([52])
    FOLLOW_52_in_statement3183 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3187 = frozenset([])
    FOLLOW_EOF_in_statement3189 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3198 = frozenset([38])
    FOLLOW_38_in_statement3200 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3204 = frozenset([])
    FOLLOW_EOF_in_statement3206 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3215 = frozenset([41])
    FOLLOW_41_in_statement3217 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3221 = frozenset([])
    FOLLOW_EOF_in_statement3223 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3232 = frozenset([36])
    FOLLOW_36_in_statement3234 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3238 = frozenset([])
    FOLLOW_EOF_in_statement3240 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3249 = frozenset([46])
    FOLLOW_46_in_statement3251 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3255 = frozenset([])
    FOLLOW_EOF_in_statement3257 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3266 = frozenset([45])
    FOLLOW_45_in_statement3268 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3272 = frozenset([])
    FOLLOW_EOF_in_statement3274 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3283 = frozenset([29])
    FOLLOW_29_in_statement3285 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3289 = frozenset([])
    FOLLOW_EOF_in_statement3291 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3300 = frozenset([50])
    FOLLOW_50_in_statement3302 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3306 = frozenset([])
    FOLLOW_EOF_in_statement3308 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3317 = frozenset([57])
    FOLLOW_57_in_statement3319 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3323 = frozenset([])
    FOLLOW_EOF_in_statement3325 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3334 = frozenset([31])
    FOLLOW_31_in_statement3336 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3340 = frozenset([])
    FOLLOW_EOF_in_statement3342 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3351 = frozenset([61])
    FOLLOW_61_in_statement3353 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3357 = frozenset([])
    FOLLOW_EOF_in_statement3359 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3368 = frozenset([72])
    FOLLOW_72_in_statement3370 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_statement3374 = frozenset([])
    FOLLOW_EOF_in_statement3376 = frozenset([1])
    FOLLOW_expression_in_statement3385 = frozenset([])
    FOLLOW_EOF_in_statement3387 = frozenset([1])
    FOLLOW_name_in_definition3421 = frozenset([32])
    FOLLOW_signature_in_definition3439 = frozenset([])
    FOLLOW_EOF_in_definition3450 = frozenset([1])
    FOLLOW_32_in_signature3471 = frozenset([14, 33, 34, 35])
    FOLLOW_35_in_signature3491 = frozenset([14])
    FOLLOW_name_in_signature3495 = frozenset([33, 39])
    FOLLOW_39_in_signature3501 = frozenset([33])
    FOLLOW_34_in_signature3513 = frozenset([14])
    FOLLOW_name_in_signature3517 = frozenset([33, 39])
    FOLLOW_39_in_signature3528 = frozenset([35])
    FOLLOW_35_in_signature3533 = frozenset([14])
    FOLLOW_name_in_signature3537 = frozenset([33, 39])
    FOLLOW_39_in_signature3548 = frozenset([33])
    FOLLOW_name_in_signature3562 = frozenset([52])
    FOLLOW_52_in_signature3566 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_signature3572 = frozenset([33, 39])
    FOLLOW_39_in_signature3583 = frozenset([14])
    FOLLOW_name_in_signature3590 = frozenset([52])
    FOLLOW_52_in_signature3595 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_signature3602 = frozenset([33, 39])
    FOLLOW_39_in_signature3618 = frozenset([34])
    FOLLOW_34_in_signature3623 = frozenset([14])
    FOLLOW_name_in_signature3627 = frozenset([33, 39])
    FOLLOW_39_in_signature3643 = frozenset([35])
    FOLLOW_35_in_signature3648 = frozenset([14])
    FOLLOW_name_in_signature3652 = frozenset([33, 39])
    FOLLOW_39_in_signature3663 = frozenset([33])
    FOLLOW_name_in_signature3677 = frozenset([33, 39])
    FOLLOW_39_in_signature3688 = frozenset([14])
    FOLLOW_name_in_signature3695 = frozenset([33, 39])
    FOLLOW_39_in_signature3711 = frozenset([14])
    FOLLOW_name_in_signature3718 = frozenset([52])
    FOLLOW_52_in_signature3723 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_exprarg_in_signature3730 = frozenset([33, 39])
    FOLLOW_39_in_signature3746 = frozenset([34])
    FOLLOW_34_in_signature3751 = frozenset([14])
    FOLLOW_name_in_signature3755 = frozenset([33, 39])
    FOLLOW_39_in_signature3771 = frozenset([35])
    FOLLOW_35_in_signature3776 = frozenset([14])
    FOLLOW_name_in_signature3780 = frozenset([33, 39])
    FOLLOW_39_in_signature3791 = frozenset([33])
    FOLLOW_33_in_signature3800 = frozenset([])
    FOLLOW_EOF_in_signature3805 = frozenset([1])
    FOLLOW_list_in_synpred26_UL41741 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred27_UL41750 = frozenset([1])
    FOLLOW_set_in_synpred28_UL41759 = frozenset([1])
    FOLLOW_setcomprehension_in_synpred29_UL41768 = frozenset([1])
    FOLLOW_dict_in_synpred30_UL41777 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred31_UL41786 = frozenset([1])
    FOLLOW_32_in_synpred32_UL41795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_generatorexpression_in_synpred32_UL41799 = frozenset([33])
    FOLLOW_33_in_synpred32_UL41803 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred33_UL41843 = frozenset([1])
    FOLLOW_32_in_synpred34_UL41852 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 70])
    FOLLOW_nestedlvalue_in_synpred34_UL41856 = frozenset([39])
    FOLLOW_39_in_synpred34_UL41858 = frozenset([33])
    FOLLOW_33_in_synpred34_UL41860 = frozenset([1])
    FOLLOW_39_in_synpred43_UL42151 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_argument_in_synpred43_UL42160 = frozenset([1])
    FOLLOW_32_in_synpred46_UL42121 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_argument_in_synpred46_UL42136 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 39, 40, 58, 68, 70, 74])
    FOLLOW_39_in_synpred46_UL42151 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_argument_in_synpred46_UL42160 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 39, 40, 58, 68, 70, 74])
    FOLLOW_39_in_synpred46_UL42175 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 68, 70, 74])
    FOLLOW_33_in_synpred46_UL42189 = frozenset([1])
    FOLLOW_58_in_synpred47_UL42205 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred47_UL42213 = frozenset([59])
    FOLLOW_59_in_synpred47_UL42220 = frozenset([1])
    FOLLOW_58_in_synpred48_UL42236 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 68, 70, 74])
    FOLLOW_slice_in_synpred48_UL42244 = frozenset([59])
    FOLLOW_59_in_synpred48_UL42251 = frozenset([1])
    FOLLOW_set_in_synpred54_UL42344 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_unary_in_synpred54_UL42403 = frozenset([1])
    FOLLOW_set_in_synpred56_UL42442 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 70, 74])
    FOLLOW_expr_mul_in_synpred56_UL42475 = frozenset([1])
    FOLLOW_65_in_synpred75_UL43035 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_or_in_synpred75_UL43042 = frozenset([63])
    FOLLOW_63_in_synpred75_UL43047 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_or_in_synpred75_UL43054 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred76_UL43078 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred77_UL43106 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL43108 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred78_UL43181 = frozenset([52])
    FOLLOW_52_in_synpred78_UL43183 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred78_UL43187 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43189 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred79_UL43198 = frozenset([38])
    FOLLOW_38_in_synpred79_UL43200 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred79_UL43204 = frozenset([])
    FOLLOW_EOF_in_synpred79_UL43206 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred80_UL43215 = frozenset([41])
    FOLLOW_41_in_synpred80_UL43217 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred80_UL43221 = frozenset([])
    FOLLOW_EOF_in_synpred80_UL43223 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred81_UL43232 = frozenset([36])
    FOLLOW_36_in_synpred81_UL43234 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred81_UL43238 = frozenset([])
    FOLLOW_EOF_in_synpred81_UL43240 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred82_UL43249 = frozenset([46])
    FOLLOW_46_in_synpred82_UL43251 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred82_UL43255 = frozenset([])
    FOLLOW_EOF_in_synpred82_UL43257 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred83_UL43266 = frozenset([45])
    FOLLOW_45_in_synpred83_UL43268 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred83_UL43272 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43274 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred84_UL43283 = frozenset([29])
    FOLLOW_29_in_synpred84_UL43285 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred84_UL43289 = frozenset([])
    FOLLOW_EOF_in_synpred84_UL43291 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred85_UL43300 = frozenset([50])
    FOLLOW_50_in_synpred85_UL43302 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred85_UL43306 = frozenset([])
    FOLLOW_EOF_in_synpred85_UL43308 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred86_UL43317 = frozenset([57])
    FOLLOW_57_in_synpred86_UL43319 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred86_UL43323 = frozenset([])
    FOLLOW_EOF_in_synpred86_UL43325 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred87_UL43334 = frozenset([31])
    FOLLOW_31_in_synpred87_UL43336 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred87_UL43340 = frozenset([])
    FOLLOW_EOF_in_synpred87_UL43342 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred88_UL43351 = frozenset([61])
    FOLLOW_61_in_synpred88_UL43353 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred88_UL43357 = frozenset([])
    FOLLOW_EOF_in_synpred88_UL43359 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred89_UL43368 = frozenset([72])
    FOLLOW_72_in_synpred89_UL43370 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 68, 70, 74])
    FOLLOW_expr_if_in_synpred89_UL43374 = frozenset([])
    FOLLOW_EOF_in_synpred89_UL43376 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
