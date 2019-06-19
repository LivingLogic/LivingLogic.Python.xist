# $ANTLR 3.5.2 src/ll/UL4.g 2019-06-19 15:10:04

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


import datetime, ast
from ll import ul4c, color



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
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
T__75=75
BIN_DIGIT=4
COLOR=5
DATE=6
DATETIME=7
DIGIT=8
ESC_SEQ=9
EXPONENT=10
FALSE=11
FLOAT=12
HEX_DIGIT=13
INT=14
NAME=15
NONE=16
OCT_DIGIT=17
STRING=18
STRING3=19
TIME=20
TRIAPOS=21
TRIQUOTE=22
TRUE=23
UNICODE1_ESC=24
UNICODE2_ESC=25
UNICODE4_ESC=26
WS=27

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "BIN_DIGIT", "COLOR", "DATE", "DATETIME", "DIGIT", "ESC_SEQ", "EXPONENT", 
    "FALSE", "FLOAT", "HEX_DIGIT", "INT", "NAME", "NONE", "OCT_DIGIT", "STRING", 
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

    def pos(self, token):
    	return slice(self.tag.codepos.start + token.start, self.tag.codepos.start + token.stop + 1)



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
                NONE1 = self.match(self.input, NONE, self.FOLLOW_NONE_in_none829)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(NONE1), None) 






                       
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
                TRUE2 = self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_846)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(TRUE2), True) 






                       
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
                FALSE3 = self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_863)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(FALSE3), False) 






                       
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
                INT4 = self.match(self.input, INT, self.FOLLOW_INT_in_int_880)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(INT4), int(INT4.text, 0)) 






                       
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
                FLOAT5 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_897)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(FLOAT5), float(FLOAT5.text)) 






                       
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
                    STRING6 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string914)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.tag.template, self.pos(STRING6), ast.literal_eval(STRING6.text)) 




                elif alt1 == 2:
                    # src/ll/UL4.g:187:4: STRING3
                    pass 
                    STRING37 = self.match(self.input, STRING3, self.FOLLOW_STRING3_in_string921)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.tag.template, self.pos(STRING37), ast.literal_eval(STRING37.text.replace("\r", "\\r"))) 





                       
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
                DATE8 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date938)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(DATE8), datetime.date(*map(int, [f for f in ul4c._datesplitter.split(DATE8.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "date"



    # $ANTLR start "datetime"
    # src/ll/UL4.g:194:1: datetime returns [node] : DATETIME ;
    def datetime(self, ):
        node = None


        DATETIME9 = None

        try:
            try:
                # src/ll/UL4.g:195:2: ( DATETIME )
                # src/ll/UL4.g:195:4: DATETIME
                pass 
                DATETIME9 = self.match(self.input, DATETIME, self.FOLLOW_DATETIME_in_datetime955)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(DATETIME9), datetime.datetime(*map(int, [f for f in ul4c._datesplitter.split(DATETIME9.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "datetime"



    # $ANTLR start "color"
    # src/ll/UL4.g:198:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR10 = None

        try:
            try:
                # src/ll/UL4.g:199:2: ( COLOR )
                # src/ll/UL4.g:199:4: COLOR
                pass 
                COLOR10 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color972)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.tag.template, self.pos(COLOR10), color.Color.fromrepr(COLOR10.text)) 






                       
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
    # src/ll/UL4.g:202:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME11 = None

        try:
            try:
                # src/ll/UL4.g:203:2: ( NAME )
                # src/ll/UL4.g:203:4: NAME
                pass 
                NAME11 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name989)

                if self._state.backtracking == 0:
                    pass
                    retval.node = ul4c.Var(self.tag.template, self.pos(NAME11), NAME11.text) 





                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return retval

    # $ANTLR end "name"



    # $ANTLR start "literal"
    # src/ll/UL4.g:206:1: literal returns [node] : (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_datetime= datetime |e_color= color |e_name= name );
    def literal(self, ):
        node = None


        e_none = None
        e_false = None
        e_true = None
        e_int = None
        e_float = None
        e_string = None
        e_date = None
        e_datetime = None
        e_color = None
        e_name = None

        try:
            try:
                # src/ll/UL4.g:207:2: (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_datetime= datetime |e_color= color |e_name= name )
                alt2 = 10
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
                elif LA2 == DATETIME:
                    alt2 = 8
                elif LA2 == COLOR:
                    alt2 = 9
                elif LA2 == NAME:
                    alt2 = 10
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 2, 0, self.input)

                    raise nvae


                if alt2 == 1:
                    # src/ll/UL4.g:207:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal1008)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt2 == 2:
                    # src/ll/UL4.g:208:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal1017)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt2 == 3:
                    # src/ll/UL4.g:209:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal1026)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt2 == 4:
                    # src/ll/UL4.g:210:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal1035)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt2 == 5:
                    # src/ll/UL4.g:211:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal1044)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt2 == 6:
                    # src/ll/UL4.g:212:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal1053)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt2 == 7:
                    # src/ll/UL4.g:213:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal1062)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt2 == 8:
                    # src/ll/UL4.g:214:4: e_datetime= datetime
                    pass 
                    self._state.following.append(self.FOLLOW_datetime_in_literal1071)
                    e_datetime = self.datetime()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_datetime 




                elif alt2 == 9:
                    # src/ll/UL4.g:215:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal1080)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt2 == 10:
                    # src/ll/UL4.g:216:4: e_name= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_literal1089)
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
    # src/ll/UL4.g:221:1: fragment seqitem returns [node] : (e= expr_if |star= '*' es= expr_if );
    def seqitem(self, ):
        node = None


        star = None
        e = None
        es = None

        try:
            try:
                # src/ll/UL4.g:222:2: (e= expr_if |star= '*' es= expr_if )
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((COLOR <= LA3_0 <= DATETIME) or (FALSE <= LA3_0 <= FLOAT) or (INT <= LA3_0 <= NONE) or (STRING <= LA3_0 <= STRING3) or LA3_0 == TRUE or LA3_0 == 33 or LA3_0 == 41 or LA3_0 == 59 or LA3_0 == 69 or LA3_0 == 71 or LA3_0 == 75) :
                    alt3 = 1
                elif (LA3_0 == 35) :
                    alt3 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 3, 0, self.input)

                    raise nvae


                if alt3 == 1:
                    # src/ll/UL4.g:223:3: e= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_seqitem1114)
                    e = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SeqItem(self.tag.template, e._startpos, e) 




                elif alt3 == 2:
                    # src/ll/UL4.g:225:3: star= '*' es= expr_if
                    pass 
                    star = self.match(self.input, 35, self.FOLLOW_35_in_seqitem1125)

                    self._state.following.append(self.FOLLOW_expr_if_in_seqitem1131)
                    es = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackSeqItem(self.tag.template, slice(self.pos(star).start, es._startpos.stop), es) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "seqitem"



    # $ANTLR start "list"
    # src/ll/UL4.g:229:1: list returns [node] : (open= '[' close= ']' |open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']' );
    def list(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:230:2: (open= '[' close= ']' |open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']' )
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 59) :
                    LA6_1 = self.input.LA(2)

                    if (LA6_1 == 60) :
                        alt6 = 1
                    elif ((COLOR <= LA6_1 <= DATETIME) or (FALSE <= LA6_1 <= FLOAT) or (INT <= LA6_1 <= NONE) or (STRING <= LA6_1 <= STRING3) or LA6_1 == TRUE or LA6_1 == 33 or LA6_1 == 35 or LA6_1 == 41 or LA6_1 == 59 or LA6_1 == 69 or LA6_1 == 71 or LA6_1 == 75) :
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
                    # src/ll/UL4.g:231:3: open= '[' close= ']'
                    pass 
                    open = self.match(self.input, 59, self.FOLLOW_59_in_list1152)

                    close = self.match(self.input, 60, self.FOLLOW_60_in_list1158)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.tag.template, slice(self.pos(open).start, self.pos(close).stop)) 




                elif alt6 == 2:
                    # src/ll/UL4.g:234:3: open= '[' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 59, self.FOLLOW_59_in_list1169)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.tag.template, slice(self.pos(open).start, None)) 



                    self._state.following.append(self.FOLLOW_seqitem_in_list1177)
                    i1 = self.seqitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:236:3: ( ',' i2= seqitem )*
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == 40) :
                            LA4_1 = self.input.LA(2)

                            if ((COLOR <= LA4_1 <= DATETIME) or (FALSE <= LA4_1 <= FLOAT) or (INT <= LA4_1 <= NONE) or (STRING <= LA4_1 <= STRING3) or LA4_1 == TRUE or LA4_1 == 33 or LA4_1 == 35 or LA4_1 == 41 or LA4_1 == 59 or LA4_1 == 69 or LA4_1 == 71 or LA4_1 == 75) :
                                alt4 = 1




                        if alt4 == 1:
                            # src/ll/UL4.g:237:4: ',' i2= seqitem
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_list1188)

                            self._state.following.append(self.FOLLOW_seqitem_in_list1195)
                            i2 = self.seqitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop4


                    # src/ll/UL4.g:240:3: ( ',' )?
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == 40) :
                        alt5 = 1
                    if alt5 == 1:
                        # src/ll/UL4.g:240:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_list1206)




                    close = self.match(self.input, 60, self.FOLLOW_60_in_list1213)

                    if self._state.backtracking == 0:
                        pass
                        node.startpos = slice(node._startpos.start, self.pos(close).stop) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "list"



    # $ANTLR start "listcomprehension"
    # src/ll/UL4.g:244:1: listcomprehension returns [node] : open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' ;
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
                # src/ll/UL4.g:249:2: (open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' )
                # src/ll/UL4.g:250:3: open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']'
                pass 
                open = self.match(self.input, 59, self.FOLLOW_59_in_listcomprehension1241)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1247)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 65, self.FOLLOW_65_in_listcomprehension1251)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_listcomprehension1257)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 67, self.FOLLOW_67_in_listcomprehension1261)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1267)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:256:3: ( 'if' condition= expr_if )?
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == 66) :
                    alt7 = 1
                if alt7 == 1:
                    # src/ll/UL4.g:257:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 66, self.FOLLOW_66_in_listcomprehension1276)

                    self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1283)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 60, self.FOLLOW_60_in_listcomprehension1296)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ListComp(self.tag.template, slice(self.pos(open).start, self.pos(close).stop), item, n, container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "set"
    # src/ll/UL4.g:264:1: set returns [node] : (open= '{' '/' close= '}' |open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}' );
    def set(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:265:2: (open= '{' '/' close= '}' |open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}' )
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 71) :
                    LA10_1 = self.input.LA(2)

                    if (LA10_1 == 44) :
                        alt10 = 1
                    elif ((COLOR <= LA10_1 <= DATETIME) or (FALSE <= LA10_1 <= FLOAT) or (INT <= LA10_1 <= NONE) or (STRING <= LA10_1 <= STRING3) or LA10_1 == TRUE or LA10_1 == 33 or LA10_1 == 35 or LA10_1 == 41 or LA10_1 == 59 or LA10_1 == 69 or LA10_1 == 71 or LA10_1 == 75) :
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
                    # src/ll/UL4.g:266:3: open= '{' '/' close= '}'
                    pass 
                    open = self.match(self.input, 71, self.FOLLOW_71_in_set1319)

                    self.match(self.input, 44, self.FOLLOW_44_in_set1323)

                    close = self.match(self.input, 74, self.FOLLOW_74_in_set1329)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.tag.template, slice(self.pos(open).start, self.pos(close).stop)) 




                elif alt10 == 2:
                    # src/ll/UL4.g:270:3: open= '{' i1= seqitem ( ',' i2= seqitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 71, self.FOLLOW_71_in_set1340)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.tag.template, slice(self.pos(open).start, None)) 



                    self._state.following.append(self.FOLLOW_seqitem_in_set1348)
                    i1 = self.seqitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:272:3: ( ',' i2= seqitem )*
                    while True: #loop8
                        alt8 = 2
                        LA8_0 = self.input.LA(1)

                        if (LA8_0 == 40) :
                            LA8_1 = self.input.LA(2)

                            if ((COLOR <= LA8_1 <= DATETIME) or (FALSE <= LA8_1 <= FLOAT) or (INT <= LA8_1 <= NONE) or (STRING <= LA8_1 <= STRING3) or LA8_1 == TRUE or LA8_1 == 33 or LA8_1 == 35 or LA8_1 == 41 or LA8_1 == 59 or LA8_1 == 69 or LA8_1 == 71 or LA8_1 == 75) :
                                alt8 = 1




                        if alt8 == 1:
                            # src/ll/UL4.g:273:4: ',' i2= seqitem
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_set1359)

                            self._state.following.append(self.FOLLOW_seqitem_in_set1366)
                            i2 = self.seqitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop8


                    # src/ll/UL4.g:276:3: ( ',' )?
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == 40) :
                        alt9 = 1
                    if alt9 == 1:
                        # src/ll/UL4.g:276:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_set1377)




                    close = self.match(self.input, 74, self.FOLLOW_74_in_set1384)

                    if self._state.backtracking == 0:
                        pass
                        node.startpos = slice(node._startpos.start, self.pos(close).stop) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "set"



    # $ANTLR start "setcomprehension"
    # src/ll/UL4.g:280:1: setcomprehension returns [node] : open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
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
                # src/ll/UL4.g:285:2: (open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:286:3: open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 71, self.FOLLOW_71_in_setcomprehension1412)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1418)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 65, self.FOLLOW_65_in_setcomprehension1422)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_setcomprehension1428)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 67, self.FOLLOW_67_in_setcomprehension1432)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1438)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:292:3: ( 'if' condition= expr_if )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 66) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:293:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 66, self.FOLLOW_66_in_setcomprehension1447)

                    self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1454)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 74, self.FOLLOW_74_in_setcomprehension1467)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.SetComp(self.tag.template, slice(self.pos(open).start, self.pos(close).stop), item, n, container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "setcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:301:1: fragment dictitem returns [node] : (k= expr_if ':' v= expr_if |star= '**' e= expr_if );
    def dictitem(self, ):
        node = None


        star = None
        k = None
        v = None
        e = None

        try:
            try:
                # src/ll/UL4.g:302:2: (k= expr_if ':' v= expr_if |star= '**' e= expr_if )
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if ((COLOR <= LA12_0 <= DATETIME) or (FALSE <= LA12_0 <= FLOAT) or (INT <= LA12_0 <= NONE) or (STRING <= LA12_0 <= STRING3) or LA12_0 == TRUE or LA12_0 == 33 or LA12_0 == 41 or LA12_0 == 59 or LA12_0 == 69 or LA12_0 == 71 or LA12_0 == 75) :
                    alt12 = 1
                elif (LA12_0 == 36) :
                    alt12 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae


                if alt12 == 1:
                    # src/ll/UL4.g:303:3: k= expr_if ':' v= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1492)
                    k = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, 48, self.FOLLOW_48_in_dictitem1496)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1502)
                    v = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.DictItem(self.tag.template, slice(k._startpos.start, v._startpos.start), k, v) 




                elif alt12 == 2:
                    # src/ll/UL4.g:307:3: star= '**' e= expr_if
                    pass 
                    star = self.match(self.input, 36, self.FOLLOW_36_in_dictitem1513)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictitem1519)
                    e = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackDictItem(self.tag.template, slice(self.pos(star).start, e._startpos.stop), e) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dictitem"



    # $ANTLR start "dict"
    # src/ll/UL4.g:311:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:312:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == 71) :
                    LA15_1 = self.input.LA(2)

                    if (LA15_1 == 74) :
                        alt15 = 1
                    elif ((COLOR <= LA15_1 <= DATETIME) or (FALSE <= LA15_1 <= FLOAT) or (INT <= LA15_1 <= NONE) or (STRING <= LA15_1 <= STRING3) or LA15_1 == TRUE or LA15_1 == 33 or LA15_1 == 36 or LA15_1 == 41 or LA15_1 == 59 or LA15_1 == 69 or LA15_1 == 71 or LA15_1 == 75) :
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
                    # src/ll/UL4.g:313:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 71, self.FOLLOW_71_in_dict1540)

                    close = self.match(self.input, 74, self.FOLLOW_74_in_dict1546)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.tag.template, slice(self.pos(open).start, self.pos(close).stop)) 




                elif alt15 == 2:
                    # src/ll/UL4.g:316:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 71, self.FOLLOW_71_in_dict1557)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.tag.template, slice(self.pos(open).start, None)) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1565)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:318:3: ( ',' i2= dictitem )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 40) :
                            LA13_1 = self.input.LA(2)

                            if ((COLOR <= LA13_1 <= DATETIME) or (FALSE <= LA13_1 <= FLOAT) or (INT <= LA13_1 <= NONE) or (STRING <= LA13_1 <= STRING3) or LA13_1 == TRUE or LA13_1 == 33 or LA13_1 == 36 or LA13_1 == 41 or LA13_1 == 59 or LA13_1 == 69 or LA13_1 == 71 or LA13_1 == 75) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:319:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_dict1576)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1583)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop13


                    # src/ll/UL4.g:322:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 40) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:322:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_dict1594)




                    close = self.match(self.input, 74, self.FOLLOW_74_in_dict1601)

                    if self._state.backtracking == 0:
                        pass
                        node.startpos = slice(node._startpos.start, self.pos(close).stop) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:326:1: dictcomprehension returns [node] : open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
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
                # src/ll/UL4.g:331:2: (open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:332:3: open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 71, self.FOLLOW_71_in_dictcomprehension1629)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1635)
                key = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 48, self.FOLLOW_48_in_dictcomprehension1639)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1645)
                value = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 65, self.FOLLOW_65_in_dictcomprehension1649)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_dictcomprehension1655)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 67, self.FOLLOW_67_in_dictcomprehension1659)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1665)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:340:3: ( 'if' condition= expr_if )?
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if (LA16_0 == 66) :
                    alt16 = 1
                if alt16 == 1:
                    # src/ll/UL4.g:341:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 66, self.FOLLOW_66_in_dictcomprehension1674)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1681)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 74, self.FOLLOW_74_in_dictcomprehension1694)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.DictComp(self.tag.template, slice(self.pos(open).start, self.pos(close).stop), key, value, n, container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:347:1: generatorexpression returns [node] : item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? ;
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
                # src/ll/UL4.g:353:2: (item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? )
                # src/ll/UL4.g:354:3: item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )?
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1722)
                item = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item._startpos.start 



                self.match(self.input, 65, self.FOLLOW_65_in_generatorexpression1728)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_generatorexpression1734)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 67, self.FOLLOW_67_in_generatorexpression1738)

                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1744)
                container = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _stop = container._startpos.stop 



                # src/ll/UL4.g:359:3: ( 'if' condition= expr_if )?
                alt17 = 2
                LA17_0 = self.input.LA(1)

                if (LA17_0 == 66) :
                    alt17 = 1
                if alt17 == 1:
                    # src/ll/UL4.g:360:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 66, self.FOLLOW_66_in_generatorexpression1755)

                    self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1762)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; _stop = condition._startpos.stop 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.GenExpr(self.tag.template, slice(item._startpos.start, _stop), item, n, container, _condition) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:365:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' );
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
                # src/ll/UL4.g:366:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' )
                alt18 = 9
                LA18 = self.input.LA(1)
                if LA18 == COLOR or LA18 == DATE or LA18 == DATETIME or LA18 == FALSE or LA18 == FLOAT or LA18 == INT or LA18 == NAME or LA18 == NONE or LA18 == STRING or LA18 == STRING3 or LA18 == TRUE:
                    alt18 = 1
                elif LA18 == 59:
                    LA18_12 = self.input.LA(2)

                    if (self.synpred27_UL4()) :
                        alt18 = 2
                    elif (self.synpred28_UL4()) :
                        alt18 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 12, self.input)

                        raise nvae


                elif LA18 == 71:
                    LA18_13 = self.input.LA(2)

                    if (self.synpred29_UL4()) :
                        alt18 = 4
                    elif (self.synpred30_UL4()) :
                        alt18 = 5
                    elif (self.synpred31_UL4()) :
                        alt18 = 6
                    elif (self.synpred32_UL4()) :
                        alt18 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 13, self.input)

                        raise nvae


                elif LA18 == 33:
                    LA18_14 = self.input.LA(2)

                    if (self.synpred33_UL4()) :
                        alt18 = 8
                    elif (True) :
                        alt18 = 9
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 14, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 18, 0, self.input)

                    raise nvae


                if alt18 == 1:
                    # src/ll/UL4.g:366:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1788)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt18 == 2:
                    # src/ll/UL4.g:367:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1797)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt18 == 3:
                    # src/ll/UL4.g:368:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1806)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt18 == 4:
                    # src/ll/UL4.g:369:4: e_set= set
                    pass 
                    self._state.following.append(self.FOLLOW_set_in_atom1815)
                    e_set = self.set()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_set 




                elif alt18 == 5:
                    # src/ll/UL4.g:370:4: e_setcomp= setcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_setcomprehension_in_atom1824)
                    e_setcomp = self.setcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_setcomp 




                elif alt18 == 6:
                    # src/ll/UL4.g:371:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1833)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt18 == 7:
                    # src/ll/UL4.g:372:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1842)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt18 == 8:
                    # src/ll/UL4.g:373:4: open= '(' e_genexpr= generatorexpression close= ')'
                    pass 
                    open = self.match(self.input, 33, self.FOLLOW_33_in_atom1851)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1855)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 34, self.FOLLOW_34_in_atom1859)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.startpos = slice(self.pos(open).start, self.pos(close).stop)
                        	




                elif alt18 == 9:
                    # src/ll/UL4.g:377:4: open= '(' e_bracket= expr_if close= ')'
                    pass 
                    open = self.match(self.input, 33, self.FOLLOW_33_in_atom1868)

                    self._state.following.append(self.FOLLOW_expr_if_in_atom1872)
                    e_bracket = self.expr_if()

                    self._state.following.pop()

                    close = self.match(self.input, 34, self.FOLLOW_34_in_atom1876)

                    if self._state.backtracking == 0:
                        pass
                                                                
                        node = e_bracket
                        node.startpos = slice(self.pos(open).start, self.pos(close).stop)
                        	





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "atom"



    # $ANTLR start "nestedlvalue"
    # src/ll/UL4.g:384:1: nestedlvalue returns [lvalue] : (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' );
    def nestedlvalue(self, ):
        lvalue = None


        n = None
        n0 = None
        n1 = None
        n2 = None
        n3 = None

        try:
            try:
                # src/ll/UL4.g:385:2: (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' )
                alt21 = 3
                LA21_0 = self.input.LA(1)

                if ((COLOR <= LA21_0 <= DATETIME) or (FALSE <= LA21_0 <= FLOAT) or (INT <= LA21_0 <= NONE) or (STRING <= LA21_0 <= STRING3) or LA21_0 == TRUE or LA21_0 == 59 or LA21_0 == 71) :
                    alt21 = 1
                elif (LA21_0 == 33) :
                    LA21_14 = self.input.LA(2)

                    if (self.synpred34_UL4()) :
                        alt21 = 1
                    elif (self.synpred35_UL4()) :
                        alt21 = 2
                    elif (True) :
                        alt21 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 21, 14, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 21, 0, self.input)

                    raise nvae


                if alt21 == 1:
                    # src/ll/UL4.g:386:3: n= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_nestedlvalue1899)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        lvalue =  n 




                elif alt21 == 2:
                    # src/ll/UL4.g:388:3: '(' n0= nestedlvalue ',' ')'
                    pass 
                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1908)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1912)
                    n0 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 40, self.FOLLOW_40_in_nestedlvalue1914)

                    self.match(self.input, 34, self.FOLLOW_34_in_nestedlvalue1916)

                    if self._state.backtracking == 0:
                        pass
                        lvalue = (n0,) 




                elif alt21 == 3:
                    # src/ll/UL4.g:390:3: '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1925)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1931)
                    n1 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 40, self.FOLLOW_40_in_nestedlvalue1935)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1941)
                    n2 = self.nestedlvalue()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        lvalue = (n1, n2) 



                    # src/ll/UL4.g:394:3: ( ',' n3= nestedlvalue )*
                    while True: #loop19
                        alt19 = 2
                        LA19_0 = self.input.LA(1)

                        if (LA19_0 == 40) :
                            LA19_1 = self.input.LA(2)

                            if ((COLOR <= LA19_1 <= DATETIME) or (FALSE <= LA19_1 <= FLOAT) or (INT <= LA19_1 <= NONE) or (STRING <= LA19_1 <= STRING3) or LA19_1 == TRUE or LA19_1 == 33 or LA19_1 == 59 or LA19_1 == 71) :
                                alt19 = 1




                        if alt19 == 1:
                            # src/ll/UL4.g:395:4: ',' n3= nestedlvalue
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_nestedlvalue1952)

                            self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1959)
                            n3 = self.nestedlvalue()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                lvalue += (n3,) 




                        else:
                            break #loop19


                    # src/ll/UL4.g:398:3: ( ',' )?
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if (LA20_0 == 40) :
                        alt20 = 1
                    if alt20 == 1:
                        # src/ll/UL4.g:398:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_nestedlvalue1970)




                    self.match(self.input, 34, self.FOLLOW_34_in_nestedlvalue1975)



                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return lvalue

    # $ANTLR end "nestedlvalue"



    # $ANTLR start "slice"
    # src/ll/UL4.g:403:1: slice returns [node] : (e1= expr_if )? colon= ':' (e2= expr_if )? ;
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
                # src/ll/UL4.g:411:2: ( (e1= expr_if )? colon= ':' (e2= expr_if )? )
                # src/ll/UL4.g:412:3: (e1= expr_if )? colon= ':' (e2= expr_if )?
                pass 
                # src/ll/UL4.g:412:3: (e1= expr_if )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if ((COLOR <= LA22_0 <= DATETIME) or (FALSE <= LA22_0 <= FLOAT) or (INT <= LA22_0 <= NONE) or (STRING <= LA22_0 <= STRING3) or LA22_0 == TRUE or LA22_0 == 33 or LA22_0 == 41 or LA22_0 == 59 or LA22_0 == 69 or LA22_0 == 71 or LA22_0 == 75) :
                    alt22 = 1
                if alt22 == 1:
                    # src/ll/UL4.g:413:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice2008)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index1 = e1; startpos = e1._startpos.start; 






                colon = self.match(self.input, 48, self.FOLLOW_48_in_slice2021)

                if self._state.backtracking == 0:
                    pass
                                
                    pos = self.pos(colon)
                    if startpos is None:
                    	startpos = pos.start
                    stoppos = pos.stop
                    		



                # src/ll/UL4.g:421:3: (e2= expr_if )?
                alt23 = 2
                LA23_0 = self.input.LA(1)

                if ((COLOR <= LA23_0 <= DATETIME) or (FALSE <= LA23_0 <= FLOAT) or (INT <= LA23_0 <= NONE) or (STRING <= LA23_0 <= STRING3) or LA23_0 == TRUE or LA23_0 == 33 or LA23_0 == 41 or LA23_0 == 59 or LA23_0 == 69 or LA23_0 == 71 or LA23_0 == 75) :
                    alt23 = 1
                if alt23 == 1:
                    # src/ll/UL4.g:422:4: e2= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice2034)
                    e2 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index2 = e2; stoppos = e2._startpos.stop; 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Slice(self.tag.template, slice(startpos, stoppos), index1, index2) 






                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "slice"



    # $ANTLR start "argument"
    # src/ll/UL4.g:428:1: fragment argument returns [node] : (e= exprarg |en= name '=' ev= exprarg |star= '*' es= exprarg |star= '**' es= exprarg );
    def argument(self, ):
        node = None


        star = None
        e = None
        en = None
        ev = None
        es = None

        try:
            try:
                # src/ll/UL4.g:429:2: (e= exprarg |en= name '=' ev= exprarg |star= '*' es= exprarg |star= '**' es= exprarg )
                alt24 = 4
                LA24 = self.input.LA(1)
                if LA24 == COLOR or LA24 == DATE or LA24 == DATETIME or LA24 == FALSE or LA24 == FLOAT or LA24 == INT or LA24 == NONE or LA24 == STRING or LA24 == STRING3 or LA24 == TRUE or LA24 == 33 or LA24 == 41 or LA24 == 59 or LA24 == 69 or LA24 == 71 or LA24 == 75:
                    alt24 = 1
                elif LA24 == NAME:
                    LA24_2 = self.input.LA(2)

                    if (LA24_2 == EOF or (COLOR <= LA24_2 <= DATETIME) or (FALSE <= LA24_2 <= FLOAT) or (INT <= LA24_2 <= NONE) or (STRING <= LA24_2 <= STRING3) or LA24_2 == TRUE or (28 <= LA24_2 <= 29) or LA24_2 == 31 or (33 <= LA24_2 <= 36) or LA24_2 == 38 or (40 <= LA24_2 <= 41) or (43 <= LA24_2 <= 45) or (49 <= LA24_2 <= 50) or LA24_2 == 52 or (54 <= LA24_2 <= 57) or LA24_2 == 59 or LA24_2 == 61 or LA24_2 == 63 or (65 <= LA24_2 <= 72) or LA24_2 == 75) :
                        alt24 = 1
                    elif (LA24_2 == 53) :
                        alt24 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 24, 2, self.input)

                        raise nvae


                elif LA24 == 35:
                    alt24 = 3
                elif LA24 == 36:
                    alt24 = 4
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 24, 0, self.input)

                    raise nvae


                if alt24 == 1:
                    # src/ll/UL4.g:430:3: e= exprarg
                    pass 
                    self._state.following.append(self.FOLLOW_exprarg_in_argument2066)
                    e = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.PosArg(self.tag.template, e._startpos, e) 




                elif alt24 == 2:
                    # src/ll/UL4.g:432:3: en= name '=' ev= exprarg
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_argument2077)
                    en = self.name()

                    self._state.following.pop()

                    self.match(self.input, 53, self.FOLLOW_53_in_argument2079)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2083)
                    ev = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.KeywordArg(self.tag.template, slice(((en is not None) and [en.node] or [None])[0]._startpos.start, ev._startpos.stop), ((en is not None) and [self.input.toString(en.start,en.stop)] or [None])[0], ev) 




                elif alt24 == 3:
                    # src/ll/UL4.g:434:3: star= '*' es= exprarg
                    pass 
                    star = self.match(self.input, 35, self.FOLLOW_35_in_argument2094)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2100)
                    es = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackListArg(self.tag.template, slice(self.pos(star).start, es._startpos.stop), es) 




                elif alt24 == 4:
                    # src/ll/UL4.g:437:3: star= '**' es= exprarg
                    pass 
                    star = self.match(self.input, 36, self.FOLLOW_36_in_argument2111)

                    self._state.following.append(self.FOLLOW_exprarg_in_argument2117)
                    es = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.UnpackDictArg(self.tag.template, slice(self.pos(star).start, es._startpos.stop), es) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "argument"



    # $ANTLR start "expr_subscript"
    # src/ll/UL4.g:441:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* ;
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
                # src/ll/UL4.g:442:2: (e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* )
                # src/ll/UL4.g:443:3: e1= atom ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript2138)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:444:3: ( '.' n= name | '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                while True: #loop28
                    alt28 = 5
                    alt28 = self.dfa28.predict(self.input)
                    if alt28 == 1:
                        # src/ll/UL4.g:446:4: '.' n= name
                        pass 
                        self.match(self.input, 43, self.FOLLOW_43_in_expr_subscript2154)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript2161)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Attr(self.tag.template, slice(node._startpos.start, self.pos(n.stop).stop), node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt28 == 2:
                        # src/ll/UL4.g:450:4: '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')'
                        pass 
                        self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2177)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Call(self.tag.template, slice(node._startpos.start, None), node) 



                        # src/ll/UL4.g:451:4: (a1= argument ( ',' a2= argument )* ( ',' )? )*
                        while True: #loop27
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if ((COLOR <= LA27_0 <= DATETIME) or (FALSE <= LA27_0 <= FLOAT) or (INT <= LA27_0 <= NONE) or (STRING <= LA27_0 <= STRING3) or LA27_0 == TRUE or LA27_0 == 33 or (35 <= LA27_0 <= 36) or LA27_0 == 41 or LA27_0 == 59 or LA27_0 == 69 or LA27_0 == 71 or LA27_0 == 75) :
                                alt27 = 1


                            if alt27 == 1:
                                # src/ll/UL4.g:452:5: a1= argument ( ',' a2= argument )* ( ',' )?
                                pass 
                                self._state.following.append(self.FOLLOW_argument_in_expr_subscript2192)
                                a1 = self.argument()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    a1.append(node) 



                                # src/ll/UL4.g:453:5: ( ',' a2= argument )*
                                while True: #loop25
                                    alt25 = 2
                                    LA25_0 = self.input.LA(1)

                                    if (LA25_0 == 40) :
                                        LA25_1 = self.input.LA(2)

                                        if (self.synpred44_UL4()) :
                                            alt25 = 1




                                    if alt25 == 1:
                                        # src/ll/UL4.g:454:6: ',' a2= argument
                                        pass 
                                        self.match(self.input, 40, self.FOLLOW_40_in_expr_subscript2207)

                                        self._state.following.append(self.FOLLOW_argument_in_expr_subscript2216)
                                        a2 = self.argument()

                                        self._state.following.pop()

                                        if self._state.backtracking == 0:
                                            pass
                                            a2.append(node) 




                                    else:
                                        break #loop25


                                # src/ll/UL4.g:457:5: ( ',' )?
                                alt26 = 2
                                LA26_0 = self.input.LA(1)

                                if (LA26_0 == 40) :
                                    alt26 = 1
                                if alt26 == 1:
                                    # src/ll/UL4.g:457:5: ','
                                    pass 
                                    self.match(self.input, 40, self.FOLLOW_40_in_expr_subscript2231)





                            else:
                                break #loop27


                        close = self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2245)

                        if self._state.backtracking == 0:
                            pass
                            node.startpos = slice(node._startpos.start, self.pos(close).stop) 




                    elif alt28 == 3:
                        # src/ll/UL4.g:462:4: '[' e2= expr_if close= ']'
                        pass 
                        self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2261)

                        self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2269)
                        e2 = self.expr_if()

                        self._state.following.pop()

                        close = self.match(self.input, 60, self.FOLLOW_60_in_expr_subscript2276)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Item(self.tag.template, slice(e1._startpos.start, self.pos(close).stop), node, e2) 




                    elif alt28 == 4:
                        # src/ll/UL4.g:467:4: '[' e2= slice close= ']'
                        pass 
                        self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2292)

                        self._state.following.append(self.FOLLOW_slice_in_expr_subscript2300)
                        e2 = self.slice()

                        self._state.following.pop()

                        close = self.match(self.input, 60, self.FOLLOW_60_in_expr_subscript2307)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Item(self.tag.template, slice(e1._startpos.start, self.pos(close).stop), node, e2) 




                    else:
                        break #loop28





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_subscript"



    # $ANTLR start "expr_unary"
    # src/ll/UL4.g:474:1: expr_unary returns [node] : (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary );
    def expr_unary(self, ):
        node = None


        minus = None
        bitnot = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:475:2: (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary )
                alt29 = 3
                LA29 = self.input.LA(1)
                if LA29 == COLOR or LA29 == DATE or LA29 == DATETIME or LA29 == FALSE or LA29 == FLOAT or LA29 == INT or LA29 == NAME or LA29 == NONE or LA29 == STRING or LA29 == STRING3 or LA29 == TRUE or LA29 == 33 or LA29 == 59 or LA29 == 71:
                    alt29 = 1
                elif LA29 == 41:
                    alt29 = 2
                elif LA29 == 75:
                    alt29 = 3
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 29, 0, self.input)

                    raise nvae


                if alt29 == 1:
                    # src/ll/UL4.g:476:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_unary2335)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt29 == 2:
                    # src/ll/UL4.g:478:3: minus= '-' e2= expr_unary
                    pass 
                    minus = self.match(self.input, 41, self.FOLLOW_41_in_expr_unary2346)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2350)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.tag.template, slice(self.pos(minus).start, e2._startpos.stop), e2) 




                elif alt29 == 3:
                    # src/ll/UL4.g:480:3: bitnot= '~' e2= expr_unary
                    pass 
                    bitnot = self.match(self.input, 75, self.FOLLOW_75_in_expr_unary2361)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2365)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitNot.make(self.tag.template, slice(self.pos(bitnot).start, e2._startpos.stop), e2) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_unary"



    # $ANTLR start "expr_mul"
    # src/ll/UL4.g:485:1: expr_mul returns [node] : e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:486:2: (e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* )
                # src/ll/UL4.g:487:3: e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                pass 
                self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2389)
                e1 = self.expr_unary()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:488:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                while True: #loop31
                    alt31 = 2
                    LA31_0 = self.input.LA(1)

                    if (LA31_0 == 35) :
                        LA31_42 = self.input.LA(2)

                        if (self.synpred55_UL4()) :
                            alt31 = 1


                    elif (LA31_0 == 29 or (44 <= LA31_0 <= 45)) :
                        alt31 = 1


                    if alt31 == 1:
                        # src/ll/UL4.g:489:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
                        pass 
                        # src/ll/UL4.g:489:4: ( '*' | '/' | '//' | '%' )
                        alt30 = 4
                        LA30 = self.input.LA(1)
                        if LA30 == 35:
                            alt30 = 1
                        elif LA30 == 44:
                            alt30 = 2
                        elif LA30 == 45:
                            alt30 = 3
                        elif LA30 == 29:
                            alt30 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 30, 0, self.input)

                            raise nvae


                        if alt30 == 1:
                            # src/ll/UL4.g:490:5: '*'
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr_mul2406)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt30 == 2:
                            # src/ll/UL4.g:492:5: '/'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr_mul2419)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt30 == 3:
                            # src/ll/UL4.g:494:5: '//'
                            pass 
                            self.match(self.input, 45, self.FOLLOW_45_in_expr_mul2432)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt30 == 4:
                            # src/ll/UL4.g:496:5: '%'
                            pass 
                            self.match(self.input, 29, self.FOLLOW_29_in_expr_mul2445)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2459)
                        e2 = self.expr_unary()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop31





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_mul"



    # $ANTLR start "expr_add"
    # src/ll/UL4.g:503:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:504:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:505:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2487)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:506:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 41) :
                        LA33_39 = self.input.LA(2)

                        if (self.synpred57_UL4()) :
                            alt33 = 1


                    elif (LA33_0 == 38) :
                        alt33 = 1


                    if alt33 == 1:
                        # src/ll/UL4.g:507:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:507:4: ( '+' | '-' )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 38) :
                            alt32 = 1
                        elif (LA32_0 == 41) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:508:5: '+'
                            pass 
                            self.match(self.input, 38, self.FOLLOW_38_in_expr_add2504)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt32 == 2:
                            # src/ll/UL4.g:510:5: '-'
                            pass 
                            self.match(self.input, 41, self.FOLLOW_41_in_expr_add2517)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2531)
                        e2 = self.expr_mul()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop33





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_add"



    # $ANTLR start "expr_bitshift"
    # src/ll/UL4.g:517:1: expr_bitshift returns [node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:518:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:519:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2559)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:520:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 50 or LA35_0 == 57) :
                        alt35 = 1


                    if alt35 == 1:
                        # src/ll/UL4.g:521:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:521:4: ( '<<' | '>>' )
                        alt34 = 2
                        LA34_0 = self.input.LA(1)

                        if (LA34_0 == 50) :
                            alt34 = 1
                        elif (LA34_0 == 57) :
                            alt34 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 34, 0, self.input)

                            raise nvae


                        if alt34 == 1:
                            # src/ll/UL4.g:522:5: '<<'
                            pass 
                            self.match(self.input, 50, self.FOLLOW_50_in_expr_bitshift2576)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt34 == 2:
                            # src/ll/UL4.g:524:5: '>>'
                            pass 
                            self.match(self.input, 57, self.FOLLOW_57_in_expr_bitshift2589)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2603)
                        e2 = self.expr_add()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop35





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitshift"



    # $ANTLR start "expr_bitand"
    # src/ll/UL4.g:531:1: expr_bitand returns [node] : e1= expr_bitshift ( '&' e2= expr_bitshift )* ;
    def expr_bitand(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:532:2: (e1= expr_bitshift ( '&' e2= expr_bitshift )* )
                # src/ll/UL4.g:533:3: e1= expr_bitshift ( '&' e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2631)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:534:3: ( '&' e2= expr_bitshift )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 31) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:535:4: '&' e2= expr_bitshift
                        pass 
                        self.match(self.input, 31, self.FOLLOW_31_in_expr_bitand2642)

                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2649)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitAnd.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop36





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitand"



    # $ANTLR start "expr_bitxor"
    # src/ll/UL4.g:541:1: expr_bitxor returns [node] : e1= expr_bitand ( '^' e2= expr_bitand )* ;
    def expr_bitxor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:542:2: (e1= expr_bitand ( '^' e2= expr_bitand )* )
                # src/ll/UL4.g:543:3: e1= expr_bitand ( '^' e2= expr_bitand )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2677)
                e1 = self.expr_bitand()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:544:3: ( '^' e2= expr_bitand )*
                while True: #loop37
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if (LA37_0 == 61) :
                        alt37 = 1


                    if alt37 == 1:
                        # src/ll/UL4.g:545:4: '^' e2= expr_bitand
                        pass 
                        self.match(self.input, 61, self.FOLLOW_61_in_expr_bitxor2688)

                        self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2695)
                        e2 = self.expr_bitand()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitXOr.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop37





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitxor"



    # $ANTLR start "expr_bitor"
    # src/ll/UL4.g:551:1: expr_bitor returns [node] : e1= expr_bitxor ( '|' e2= expr_bitxor )* ;
    def expr_bitor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:552:2: (e1= expr_bitxor ( '|' e2= expr_bitxor )* )
                # src/ll/UL4.g:553:3: e1= expr_bitxor ( '|' e2= expr_bitxor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2723)
                e1 = self.expr_bitxor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:554:3: ( '|' e2= expr_bitxor )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 72) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:555:4: '|' e2= expr_bitxor
                        pass 
                        self.match(self.input, 72, self.FOLLOW_72_in_expr_bitor2734)

                        self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2741)
                        e2 = self.expr_bitxor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitOr.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop38





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitor"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:561:1: expr_cmp returns [node] : e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:562:2: (e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )* )
                # src/ll/UL4.g:563:3: e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2769)
                e1 = self.expr_bitor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:564:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 69) :
                        LA40_2 = self.input.LA(2)

                        if (LA40_2 == 67) :
                            alt40 = 1


                    elif (LA40_0 == 28 or LA40_0 == 49 or LA40_0 == 52 or (54 <= LA40_0 <= 56) or (67 <= LA40_0 <= 68)) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:565:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' ) e2= expr_bitor
                        pass 
                        # src/ll/UL4.g:565:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' | 'is' | 'is' 'not' )
                        alt39 = 10
                        LA39 = self.input.LA(1)
                        if LA39 == 54:
                            alt39 = 1
                        elif LA39 == 28:
                            alt39 = 2
                        elif LA39 == 49:
                            alt39 = 3
                        elif LA39 == 52:
                            alt39 = 4
                        elif LA39 == 55:
                            alt39 = 5
                        elif LA39 == 56:
                            alt39 = 6
                        elif LA39 == 67:
                            alt39 = 7
                        elif LA39 == 69:
                            alt39 = 8
                        elif LA39 == 68:
                            LA39_9 = self.input.LA(2)

                            if (LA39_9 == 69) :
                                alt39 = 10
                            elif ((COLOR <= LA39_9 <= DATETIME) or (FALSE <= LA39_9 <= FLOAT) or (INT <= LA39_9 <= NONE) or (STRING <= LA39_9 <= STRING3) or LA39_9 == TRUE or LA39_9 == 33 or LA39_9 == 41 or LA39_9 == 59 or LA39_9 == 71 or LA39_9 == 75) :
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
                            # src/ll/UL4.g:566:5: '=='
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_cmp2786)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:568:5: '!='
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_cmp2799)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt39 == 3:
                            # src/ll/UL4.g:570:5: '<'
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_cmp2812)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt39 == 4:
                            # src/ll/UL4.g:572:5: '<='
                            pass 
                            self.match(self.input, 52, self.FOLLOW_52_in_expr_cmp2825)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt39 == 5:
                            # src/ll/UL4.g:574:5: '>'
                            pass 
                            self.match(self.input, 55, self.FOLLOW_55_in_expr_cmp2838)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt39 == 6:
                            # src/ll/UL4.g:576:5: '>='
                            pass 
                            self.match(self.input, 56, self.FOLLOW_56_in_expr_cmp2851)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 




                        elif alt39 == 7:
                            # src/ll/UL4.g:578:5: 'in'
                            pass 
                            self.match(self.input, 67, self.FOLLOW_67_in_expr_cmp2864)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Contains; 




                        elif alt39 == 8:
                            # src/ll/UL4.g:580:5: 'not' 'in'
                            pass 
                            self.match(self.input, 69, self.FOLLOW_69_in_expr_cmp2877)

                            self.match(self.input, 67, self.FOLLOW_67_in_expr_cmp2879)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NotContains; 




                        elif alt39 == 9:
                            # src/ll/UL4.g:582:5: 'is'
                            pass 
                            self.match(self.input, 68, self.FOLLOW_68_in_expr_cmp2892)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Is; 




                        elif alt39 == 10:
                            # src/ll/UL4.g:584:5: 'is' 'not'
                            pass 
                            self.match(self.input, 68, self.FOLLOW_68_in_expr_cmp2905)

                            self.match(self.input, 69, self.FOLLOW_69_in_expr_cmp2907)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.IsNot; 






                        self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2921)
                        e2 = self.expr_bitor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop40





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_not"
    # src/ll/UL4.g:591:1: expr_not returns [node] : (e1= expr_cmp |n= 'not' e2= expr_not );
    def expr_not(self, ):
        node = None


        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:592:2: (e1= expr_cmp |n= 'not' e2= expr_not )
                alt41 = 2
                LA41_0 = self.input.LA(1)

                if ((COLOR <= LA41_0 <= DATETIME) or (FALSE <= LA41_0 <= FLOAT) or (INT <= LA41_0 <= NONE) or (STRING <= LA41_0 <= STRING3) or LA41_0 == TRUE or LA41_0 == 33 or LA41_0 == 41 or LA41_0 == 59 or LA41_0 == 71 or LA41_0 == 75) :
                    alt41 = 1
                elif (LA41_0 == 69) :
                    alt41 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 41, 0, self.input)

                    raise nvae


                if alt41 == 1:
                    # src/ll/UL4.g:593:3: e1= expr_cmp
                    pass 
                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_not2949)
                    e1 = self.expr_cmp()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt41 == 2:
                    # src/ll/UL4.g:595:3: n= 'not' e2= expr_not
                    pass 
                    n = self.match(self.input, 69, self.FOLLOW_69_in_expr_not2960)

                    self._state.following.append(self.FOLLOW_expr_not_in_expr_not2964)
                    e2 = self.expr_not()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(self.tag.template, slice(self.pos(n).start, e2._startpos.stop), e2) 





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_not"



    # $ANTLR start "expr_and"
    # src/ll/UL4.g:600:1: expr_and returns [node] : e1= expr_not ( 'and' e2= expr_not )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:601:2: (e1= expr_not ( 'and' e2= expr_not )* )
                # src/ll/UL4.g:602:3: e1= expr_not ( 'and' e2= expr_not )*
                pass 
                self._state.following.append(self.FOLLOW_expr_not_in_expr_and2988)
                e1 = self.expr_not()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:603:3: ( 'and' e2= expr_not )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 63) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:604:4: 'and' e2= expr_not
                        pass 
                        self.match(self.input, 63, self.FOLLOW_63_in_expr_and2999)

                        self._state.following.append(self.FOLLOW_expr_not_in_expr_and3006)
                        e2 = self.expr_not()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop42





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_and"



    # $ANTLR start "expr_or"
    # src/ll/UL4.g:610:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:611:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:612:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or3034)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:613:3: ( 'or' e2= expr_and )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 70) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:614:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 70, self.FOLLOW_70_in_expr_or3045)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or3052)
                        e2 = self.expr_and()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.tag.template, slice(node._startpos.start, e2._startpos.stop), node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_or"



    # $ANTLR start "expr_if"
    # src/ll/UL4.g:620:1: expr_if returns [node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:621:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:622:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if3080)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:623:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if (LA44_0 == 66) :
                    LA44_1 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt44 = 1
                if alt44 == 1:
                    # src/ll/UL4.g:624:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 66, self.FOLLOW_66_in_expr_if3091)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3098)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 64, self.FOLLOW_64_in_expr_if3103)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3110)
                    e3 = self.expr_or()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.If.make(self.tag.template, slice(e1._startpos.start, e3._startpos.stop), node, e2, e3) 









                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "expr_if"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:631:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:632:2: (ege= generatorexpression |e1= expr_if )
                alt45 = 2
                LA45 = self.input.LA(1)
                if LA45 == NONE:
                    LA45_1 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 8, self.input)

                        raise nvae


                elif LA45 == DATETIME:
                    LA45_9 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 9, self.input)

                        raise nvae


                elif LA45 == COLOR:
                    LA45_10 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 10, self.input)

                        raise nvae


                elif LA45 == NAME:
                    LA45_11 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 11, self.input)

                        raise nvae


                elif LA45 == 59:
                    LA45_12 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 12, self.input)

                        raise nvae


                elif LA45 == 71:
                    LA45_13 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 13, self.input)

                        raise nvae


                elif LA45 == 33:
                    LA45_14 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 14, self.input)

                        raise nvae


                elif LA45 == 41:
                    LA45_15 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 15, self.input)

                        raise nvae


                elif LA45 == 75:
                    LA45_16 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 16, self.input)

                        raise nvae


                elif LA45 == 69:
                    LA45_17 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 17, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 45, 0, self.input)

                    raise nvae


                if alt45 == 1:
                    # src/ll/UL4.g:632:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg3134)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt45 == 2:
                    # src/ll/UL4.g:633:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg3143)
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
    # src/ll/UL4.g:636:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:637:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt46 = 2
                LA46 = self.input.LA(1)
                if LA46 == NONE:
                    LA46_1 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
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

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 8, self.input)

                        raise nvae


                elif LA46 == DATETIME:
                    LA46_9 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 9, self.input)

                        raise nvae


                elif LA46 == COLOR:
                    LA46_10 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 10, self.input)

                        raise nvae


                elif LA46 == NAME:
                    LA46_11 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 11, self.input)

                        raise nvae


                elif LA46 == 59:
                    LA46_12 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 12, self.input)

                        raise nvae


                elif LA46 == 71:
                    LA46_13 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 13, self.input)

                        raise nvae


                elif LA46 == 33:
                    LA46_14 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 14, self.input)

                        raise nvae


                elif LA46 == 41:
                    LA46_15 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 15, self.input)

                        raise nvae


                elif LA46 == 75:
                    LA46_16 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 16, self.input)

                        raise nvae


                elif LA46 == 69:
                    LA46_17 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 17, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 46, 0, self.input)

                    raise nvae


                if alt46 == 1:
                    # src/ll/UL4.g:637:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3162)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3164)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:638:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3173)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3175)

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
    # src/ll/UL4.g:644:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:645:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:646:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3200)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 67, self.FOLLOW_67_in_for_3204)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3210)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ForBlock(self.tag.template, self.tag._startpos, None, n, e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3216)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:655:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:656:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF )
                alt47 = 13
                LA47 = self.input.LA(1)
                if LA47 == NONE:
                    LA47_1 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
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

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 8, self.input)

                        raise nvae


                elif LA47 == DATETIME:
                    LA47_9 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 9, self.input)

                        raise nvae


                elif LA47 == COLOR:
                    LA47_10 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 10, self.input)

                        raise nvae


                elif LA47 == NAME:
                    LA47_11 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 11, self.input)

                        raise nvae


                elif LA47 == 59:
                    LA47_12 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 12, self.input)

                        raise nvae


                elif LA47 == 71:
                    LA47_13 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 13, self.input)

                        raise nvae


                elif LA47 == 33:
                    LA47_14 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt47 = 1
                    elif (self.synpred80_UL4()) :
                        alt47 = 2
                    elif (self.synpred81_UL4()) :
                        alt47 = 3
                    elif (self.synpred82_UL4()) :
                        alt47 = 4
                    elif (self.synpred83_UL4()) :
                        alt47 = 5
                    elif (self.synpred84_UL4()) :
                        alt47 = 6
                    elif (self.synpred85_UL4()) :
                        alt47 = 7
                    elif (self.synpred86_UL4()) :
                        alt47 = 8
                    elif (self.synpred87_UL4()) :
                        alt47 = 9
                    elif (self.synpred88_UL4()) :
                        alt47 = 10
                    elif (self.synpred89_UL4()) :
                        alt47 = 11
                    elif (self.synpred90_UL4()) :
                        alt47 = 12
                    elif (True) :
                        alt47 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 14, self.input)

                        raise nvae


                elif LA47 == 41 or LA47 == 69 or LA47 == 75:
                    alt47 = 13
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 47, 0, self.input)

                    raise nvae


                if alt47 == 1:
                    # src/ll/UL4.g:656:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3237)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 53, self.FOLLOW_53_in_statement3239)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3243)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3245)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.tag.template, self.tag._startpos, nn, e) 




                elif alt47 == 2:
                    # src/ll/UL4.g:657:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3254)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_statement3256)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3260)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3262)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 3:
                    # src/ll/UL4.g:658:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3271)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 42, self.FOLLOW_42_in_statement3273)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3277)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3279)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 4:
                    # src/ll/UL4.g:659:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3288)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_statement3290)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3294)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3296)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 5:
                    # src/ll/UL4.g:660:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3305)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 47, self.FOLLOW_47_in_statement3307)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3311)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3313)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 6:
                    # src/ll/UL4.g:661:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3322)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement3324)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3328)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3330)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 7:
                    # src/ll/UL4.g:662:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3339)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 30, self.FOLLOW_30_in_statement3341)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3345)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3347)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 8:
                    # src/ll/UL4.g:663:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3356)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 51, self.FOLLOW_51_in_statement3358)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3362)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3364)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 9:
                    # src/ll/UL4.g:664:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3373)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 58, self.FOLLOW_58_in_statement3375)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3379)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3381)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 10:
                    # src/ll/UL4.g:665:4: n= expr_subscript '&=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3390)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 32, self.FOLLOW_32_in_statement3392)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3396)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3398)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitAndVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 11:
                    # src/ll/UL4.g:666:4: n= expr_subscript '^=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3407)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 62, self.FOLLOW_62_in_statement3409)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3413)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3415)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitXOrVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 12:
                    # src/ll/UL4.g:667:4: n= expr_subscript '|=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3424)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 73, self.FOLLOW_73_in_statement3426)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3430)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3432)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitOrVar(self.tag.template, self.tag._startpos, n, e) 




                elif alt47 == 13:
                    # src/ll/UL4.g:668:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3441)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3443)

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
    # src/ll/UL4.g:674:1: definition returns [node] : (n= name )? (sig= signature )? EOF ;
    def definition(self, ):
        node = None


        n = None
        sig = None

        try:
            try:
                # src/ll/UL4.g:675:2: ( (n= name )? (sig= signature )? EOF )
                # src/ll/UL4.g:676:3: (n= name )? (sig= signature )? EOF
                pass 
                if self._state.backtracking == 0:
                    pass
                    node =  (None, None) 



                # src/ll/UL4.g:677:3: (n= name )?
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if (LA48_0 == NAME) :
                    alt48 = 1
                if alt48 == 1:
                    # src/ll/UL4.g:678:4: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_definition3477)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], None) 






                # src/ll/UL4.g:680:3: (sig= signature )?
                alt49 = 2
                LA49_0 = self.input.LA(1)

                if (LA49_0 == 33) :
                    alt49 = 1
                if alt49 == 1:
                    # src/ll/UL4.g:681:4: sig= signature
                    pass 
                    self._state.following.append(self.FOLLOW_signature_in_definition3495)
                    sig = self.signature()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (node[0], sig) 






                self.match(self.input, EOF, self.FOLLOW_EOF_in_definition3506)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "definition"



    # $ANTLR start "signature"
    # src/ll/UL4.g:688:1: signature returns [node] : open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF ;
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
                # src/ll/UL4.g:689:2: (open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF )
                # src/ll/UL4.g:690:2: open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' EOF
                pass 
                open = self.match(self.input, 33, self.FOLLOW_33_in_signature3527)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Signature(self.tag.template, slice(self.pos(open).start, None)) 



                # src/ll/UL4.g:691:2: (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? )
                alt62 = 5
                LA62 = self.input.LA(1)
                if LA62 == 34:
                    alt62 = 1
                elif LA62 == 36:
                    alt62 = 2
                elif LA62 == 35:
                    alt62 = 3
                elif LA62 == NAME:
                    LA62_4 = self.input.LA(2)

                    if (LA62_4 == 53) :
                        alt62 = 4
                    elif (LA62_4 == 34 or LA62_4 == 40) :
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
                    # src/ll/UL4.g:693:2: 
                    pass 

                elif alt62 == 2:
                    # src/ll/UL4.g:695:3: '**' rkwargsname= name ( ',' )?
                    pass 
                    self.match(self.input, 36, self.FOLLOW_36_in_signature3547)

                    self._state.following.append(self.FOLLOW_name_in_signature3551)
                    rkwargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:696:3: ( ',' )?
                    alt50 = 2
                    LA50_0 = self.input.LA(1)

                    if (LA50_0 == 40) :
                        alt50 = 1
                    if alt50 == 1:
                        # src/ll/UL4.g:696:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3557)





                elif alt62 == 3:
                    # src/ll/UL4.g:699:3: '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self.match(self.input, 35, self.FOLLOW_35_in_signature3569)

                    self._state.following.append(self.FOLLOW_name_in_signature3573)
                    rargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:700:3: ( ',' '**' rkwargsname= name )?
                    alt51 = 2
                    LA51_0 = self.input.LA(1)

                    if (LA51_0 == 40) :
                        LA51_1 = self.input.LA(2)

                        if (LA51_1 == 36) :
                            alt51 = 1
                    if alt51 == 1:
                        # src/ll/UL4.g:701:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3584)

                        self.match(self.input, 36, self.FOLLOW_36_in_signature3589)

                        self._state.following.append(self.FOLLOW_name_in_signature3593)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:704:3: ( ',' )?
                    alt52 = 2
                    LA52_0 = self.input.LA(1)

                    if (LA52_0 == 40) :
                        alt52 = 1
                    if alt52 == 1:
                        # src/ll/UL4.g:704:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3604)





                elif alt62 == 4:
                    # src/ll/UL4.g:707:3: aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3618)
                    aname1 = self.name()

                    self._state.following.pop()

                    self.match(self.input, 53, self.FOLLOW_53_in_signature3622)

                    self._state.following.append(self.FOLLOW_exprarg_in_signature3628)
                    adefault1 = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], adefault1)); 



                    # src/ll/UL4.g:710:3: ( ',' aname2= name '=' adefault2= exprarg )*
                    while True: #loop53
                        alt53 = 2
                        LA53_0 = self.input.LA(1)

                        if (LA53_0 == 40) :
                            LA53_1 = self.input.LA(2)

                            if (LA53_1 == NAME) :
                                alt53 = 1




                        if alt53 == 1:
                            # src/ll/UL4.g:711:4: ',' aname2= name '=' adefault2= exprarg
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_signature3639)

                            self._state.following.append(self.FOLLOW_name_in_signature3646)
                            aname2 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 53, self.FOLLOW_53_in_signature3651)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3658)
                            adefault2 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], adefault2)); 




                        else:
                            break #loop53


                    # src/ll/UL4.g:716:3: ( ',' '*' rargsname= name )?
                    alt54 = 2
                    LA54_0 = self.input.LA(1)

                    if (LA54_0 == 40) :
                        LA54_1 = self.input.LA(2)

                        if (LA54_1 == 35) :
                            alt54 = 1
                    if alt54 == 1:
                        # src/ll/UL4.g:717:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3674)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3679)

                        self._state.following.append(self.FOLLOW_name_in_signature3683)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:720:3: ( ',' '**' rkwargsname= name )?
                    alt55 = 2
                    LA55_0 = self.input.LA(1)

                    if (LA55_0 == 40) :
                        LA55_1 = self.input.LA(2)

                        if (LA55_1 == 36) :
                            alt55 = 1
                    if alt55 == 1:
                        # src/ll/UL4.g:721:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3699)

                        self.match(self.input, 36, self.FOLLOW_36_in_signature3704)

                        self._state.following.append(self.FOLLOW_name_in_signature3708)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:724:3: ( ',' )?
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 40) :
                        alt56 = 1
                    if alt56 == 1:
                        # src/ll/UL4.g:724:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3719)





                elif alt62 == 5:
                    # src/ll/UL4.g:727:3: aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3733)
                    aname1 = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:728:3: ( ',' aname2= name )*
                    while True: #loop57
                        alt57 = 2
                        LA57_0 = self.input.LA(1)

                        if (LA57_0 == 40) :
                            LA57_1 = self.input.LA(2)

                            if (LA57_1 == NAME) :
                                LA57_3 = self.input.LA(3)

                                if (LA57_3 == 34 or LA57_3 == 40) :
                                    alt57 = 1






                        if alt57 == 1:
                            # src/ll/UL4.g:729:4: ',' aname2= name
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_signature3744)

                            self._state.following.append(self.FOLLOW_name_in_signature3751)
                            aname2 = self.name()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], None)); 




                        else:
                            break #loop57


                    # src/ll/UL4.g:732:3: ( ',' aname3= name '=' adefault3= exprarg )*
                    while True: #loop58
                        alt58 = 2
                        LA58_0 = self.input.LA(1)

                        if (LA58_0 == 40) :
                            LA58_1 = self.input.LA(2)

                            if (LA58_1 == NAME) :
                                alt58 = 1




                        if alt58 == 1:
                            # src/ll/UL4.g:733:4: ',' aname3= name '=' adefault3= exprarg
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_signature3767)

                            self._state.following.append(self.FOLLOW_name_in_signature3774)
                            aname3 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 53, self.FOLLOW_53_in_signature3779)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3786)
                            adefault3 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname3 is not None) and [self.input.toString(aname3.start,aname3.stop)] or [None])[0], adefault3)); 




                        else:
                            break #loop58


                    # src/ll/UL4.g:738:3: ( ',' '*' rargsname= name )?
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if (LA59_0 == 40) :
                        LA59_1 = self.input.LA(2)

                        if (LA59_1 == 35) :
                            alt59 = 1
                    if alt59 == 1:
                        # src/ll/UL4.g:739:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3802)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3807)

                        self._state.following.append(self.FOLLOW_name_in_signature3811)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:742:3: ( ',' '**' rkwargsname= name )?
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == 40) :
                        LA60_1 = self.input.LA(2)

                        if (LA60_1 == 36) :
                            alt60 = 1
                    if alt60 == 1:
                        # src/ll/UL4.g:743:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3827)

                        self.match(self.input, 36, self.FOLLOW_36_in_signature3832)

                        self._state.following.append(self.FOLLOW_name_in_signature3836)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:746:3: ( ',' )?
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if (LA61_0 == 40) :
                        alt61 = 1
                    if alt61 == 1:
                        # src/ll/UL4.g:746:3: ','
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_signature3847)







                close = self.match(self.input, 34, self.FOLLOW_34_in_signature3856)

                if self._state.backtracking == 0:
                    pass
                    node.startpos = slice(node._startpos.start, self.pos(close).stop) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_signature3861)




                       
            except RecognitionException as e:
            	raise

        finally:
            pass
        return node

    # $ANTLR end "signature"

    # $ANTLR start "synpred27_UL4"
    def synpred27_UL4_fragment(self, ):
        e_list = None

        # src/ll/UL4.g:367:4: (e_list= list )
        # src/ll/UL4.g:367:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred27_UL41797)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred27_UL4"



    # $ANTLR start "synpred28_UL4"
    def synpred28_UL4_fragment(self, ):
        e_listcomp = None

        # src/ll/UL4.g:368:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:368:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred28_UL41806)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred28_UL4"



    # $ANTLR start "synpred29_UL4"
    def synpred29_UL4_fragment(self, ):
        e_set = None

        # src/ll/UL4.g:369:4: (e_set= set )
        # src/ll/UL4.g:369:4: e_set= set
        pass 
        self._state.following.append(self.FOLLOW_set_in_synpred29_UL41815)
        e_set = self.set()

        self._state.following.pop()



    # $ANTLR end "synpred29_UL4"



    # $ANTLR start "synpred30_UL4"
    def synpred30_UL4_fragment(self, ):
        e_setcomp = None

        # src/ll/UL4.g:370:4: (e_setcomp= setcomprehension )
        # src/ll/UL4.g:370:4: e_setcomp= setcomprehension
        pass 
        self._state.following.append(self.FOLLOW_setcomprehension_in_synpred30_UL41824)
        e_setcomp = self.setcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred30_UL4"



    # $ANTLR start "synpred31_UL4"
    def synpred31_UL4_fragment(self, ):
        e_dict = None

        # src/ll/UL4.g:371:4: (e_dict= dict )
        # src/ll/UL4.g:371:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred31_UL41833)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred31_UL4"



    # $ANTLR start "synpred32_UL4"
    def synpred32_UL4_fragment(self, ):
        e_dictcomp = None

        # src/ll/UL4.g:372:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:372:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred32_UL41842)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred32_UL4"



    # $ANTLR start "synpred33_UL4"
    def synpred33_UL4_fragment(self, ):
        open = None
        close = None
        e_genexpr = None

        # src/ll/UL4.g:373:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:373:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 33, self.FOLLOW_33_in_synpred33_UL41851)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred33_UL41855)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 34, self.FOLLOW_34_in_synpred33_UL41859)



    # $ANTLR end "synpred33_UL4"



    # $ANTLR start "synpred34_UL4"
    def synpred34_UL4_fragment(self, ):
        n = None

        # src/ll/UL4.g:386:3: (n= expr_subscript )
        # src/ll/UL4.g:386:3: n= expr_subscript
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred34_UL41899)
        n = self.expr_subscript()

        self._state.following.pop()



    # $ANTLR end "synpred34_UL4"



    # $ANTLR start "synpred35_UL4"
    def synpred35_UL4_fragment(self, ):
        n0 = None

        # src/ll/UL4.g:388:3: ( '(' n0= nestedlvalue ',' ')' )
        # src/ll/UL4.g:388:3: '(' n0= nestedlvalue ',' ')'
        pass 
        self.match(self.input, 33, self.FOLLOW_33_in_synpred35_UL41908)

        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred35_UL41912)
        n0 = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 40, self.FOLLOW_40_in_synpred35_UL41914)

        self.match(self.input, 34, self.FOLLOW_34_in_synpred35_UL41916)



    # $ANTLR end "synpred35_UL4"



    # $ANTLR start "synpred44_UL4"
    def synpred44_UL4_fragment(self, ):
        a2 = None

        # src/ll/UL4.g:454:6: ( ',' a2= argument )
        # src/ll/UL4.g:454:6: ',' a2= argument
        pass 
        self.match(self.input, 40, self.FOLLOW_40_in_synpred44_UL42207)

        self._state.following.append(self.FOLLOW_argument_in_synpred44_UL42216)
        a2 = self.argument()

        self._state.following.pop()



    # $ANTLR end "synpred44_UL4"



    # $ANTLR start "synpred47_UL4"
    def synpred47_UL4_fragment(self, ):
        close = None
        a1 = None
        a2 = None

        # src/ll/UL4.g:450:4: ( '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')' )
        # src/ll/UL4.g:450:4: '(' (a1= argument ( ',' a2= argument )* ( ',' )? )* close= ')'
        pass 
        self.match(self.input, 33, self.FOLLOW_33_in_synpred47_UL42177)

        # src/ll/UL4.g:451:4: (a1= argument ( ',' a2= argument )* ( ',' )? )*
        while True: #loop67
            alt67 = 2
            LA67_0 = self.input.LA(1)

            if ((COLOR <= LA67_0 <= DATETIME) or (FALSE <= LA67_0 <= FLOAT) or (INT <= LA67_0 <= NONE) or (STRING <= LA67_0 <= STRING3) or LA67_0 == TRUE or LA67_0 == 33 or (35 <= LA67_0 <= 36) or LA67_0 == 41 or LA67_0 == 59 or LA67_0 == 69 or LA67_0 == 71 or LA67_0 == 75) :
                alt67 = 1


            if alt67 == 1:
                # src/ll/UL4.g:452:5: a1= argument ( ',' a2= argument )* ( ',' )?
                pass 
                self._state.following.append(self.FOLLOW_argument_in_synpred47_UL42192)
                a1 = self.argument()

                self._state.following.pop()

                # src/ll/UL4.g:453:5: ( ',' a2= argument )*
                while True: #loop65
                    alt65 = 2
                    LA65_0 = self.input.LA(1)

                    if (LA65_0 == 40) :
                        LA65_1 = self.input.LA(2)

                        if (self.synpred44_UL4()) :
                            alt65 = 1




                    if alt65 == 1:
                        # src/ll/UL4.g:454:6: ',' a2= argument
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_synpred47_UL42207)

                        self._state.following.append(self.FOLLOW_argument_in_synpred47_UL42216)
                        a2 = self.argument()

                        self._state.following.pop()


                    else:
                        break #loop65


                # src/ll/UL4.g:457:5: ( ',' )?
                alt66 = 2
                LA66_0 = self.input.LA(1)

                if (LA66_0 == 40) :
                    alt66 = 1
                if alt66 == 1:
                    # src/ll/UL4.g:457:5: ','
                    pass 
                    self.match(self.input, 40, self.FOLLOW_40_in_synpred47_UL42231)





            else:
                break #loop67


        close = self.match(self.input, 34, self.FOLLOW_34_in_synpred47_UL42245)



    # $ANTLR end "synpred47_UL4"



    # $ANTLR start "synpred48_UL4"
    def synpred48_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:462:4: ( '[' e2= expr_if close= ']' )
        # src/ll/UL4.g:462:4: '[' e2= expr_if close= ']'
        pass 
        self.match(self.input, 59, self.FOLLOW_59_in_synpred48_UL42261)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred48_UL42269)
        e2 = self.expr_if()

        self._state.following.pop()

        close = self.match(self.input, 60, self.FOLLOW_60_in_synpred48_UL42276)



    # $ANTLR end "synpred48_UL4"



    # $ANTLR start "synpred49_UL4"
    def synpred49_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:467:4: ( '[' e2= slice close= ']' )
        # src/ll/UL4.g:467:4: '[' e2= slice close= ']'
        pass 
        self.match(self.input, 59, self.FOLLOW_59_in_synpred49_UL42292)

        self._state.following.append(self.FOLLOW_slice_in_synpred49_UL42300)
        e2 = self.slice()

        self._state.following.pop()

        close = self.match(self.input, 60, self.FOLLOW_60_in_synpred49_UL42307)



    # $ANTLR end "synpred49_UL4"



    # $ANTLR start "synpred55_UL4"
    def synpred55_UL4_fragment(self, ):
        e2 = None

        # src/ll/UL4.g:489:4: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )
        # src/ll/UL4.g:489:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
        pass 
        if self.input.LA(1) == 29 or self.input.LA(1) == 35 or (44 <= self.input.LA(1) <= 45):
            self.input.consume()
            self._state.errorRecovery = False


        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed


            mse = MismatchedSetException(None, self.input)
            raise mse



        self._state.following.append(self.FOLLOW_expr_unary_in_synpred55_UL42459)
        e2 = self.expr_unary()

        self._state.following.pop()



    # $ANTLR end "synpred55_UL4"



    # $ANTLR start "synpred57_UL4"
    def synpred57_UL4_fragment(self, ):
        e2 = None

        # src/ll/UL4.g:507:4: ( ( '+' | '-' ) e2= expr_mul )
        # src/ll/UL4.g:507:4: ( '+' | '-' ) e2= expr_mul
        pass 
        if self.input.LA(1) == 38 or self.input.LA(1) == 41:
            self.input.consume()
            self._state.errorRecovery = False


        else:
            if self._state.backtracking > 0:
                raise BacktrackingFailed


            mse = MismatchedSetException(None, self.input)
            raise mse



        self._state.following.append(self.FOLLOW_expr_mul_in_synpred57_UL42531)
        e2 = self.expr_mul()

        self._state.following.pop()



    # $ANTLR end "synpred57_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:624:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:624:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 66, self.FOLLOW_66_in_synpred76_UL43091)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred76_UL43098)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 64, self.FOLLOW_64_in_synpred76_UL43103)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred76_UL43110)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:632:4: (ege= generatorexpression )
        # src/ll/UL4.g:632:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred77_UL43134)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:637:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:637:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred78_UL43162)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43164)



    # $ANTLR end "synpred78_UL4"



    # $ANTLR start "synpred79_UL4"
    def synpred79_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:656:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:656:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred79_UL43237)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 53, self.FOLLOW_53_in_synpred79_UL43239)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred79_UL43243)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred79_UL43245)



    # $ANTLR end "synpred79_UL4"



    # $ANTLR start "synpred80_UL4"
    def synpred80_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:657:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:657:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred80_UL43254)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred80_UL43256)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred80_UL43260)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred80_UL43262)



    # $ANTLR end "synpred80_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:658:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:658:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred81_UL43271)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 42, self.FOLLOW_42_in_synpred81_UL43273)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred81_UL43277)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred81_UL43279)



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:659:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:659:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred82_UL43288)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 37, self.FOLLOW_37_in_synpred82_UL43290)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred82_UL43294)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred82_UL43296)



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:660:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:660:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred83_UL43305)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 47, self.FOLLOW_47_in_synpred83_UL43307)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred83_UL43311)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43313)



    # $ANTLR end "synpred83_UL4"



    # $ANTLR start "synpred84_UL4"
    def synpred84_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:661:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:661:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred84_UL43322)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred84_UL43324)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred84_UL43328)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred84_UL43330)



    # $ANTLR end "synpred84_UL4"



    # $ANTLR start "synpred85_UL4"
    def synpred85_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:662:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:662:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred85_UL43339)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 30, self.FOLLOW_30_in_synpred85_UL43341)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred85_UL43345)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred85_UL43347)



    # $ANTLR end "synpred85_UL4"



    # $ANTLR start "synpred86_UL4"
    def synpred86_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:663:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:663:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred86_UL43356)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 51, self.FOLLOW_51_in_synpred86_UL43358)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred86_UL43362)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred86_UL43364)



    # $ANTLR end "synpred86_UL4"



    # $ANTLR start "synpred87_UL4"
    def synpred87_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:664:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:664:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred87_UL43373)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 58, self.FOLLOW_58_in_synpred87_UL43375)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred87_UL43379)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred87_UL43381)



    # $ANTLR end "synpred87_UL4"



    # $ANTLR start "synpred88_UL4"
    def synpred88_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:665:4: (n= expr_subscript '&=' e= expr_if EOF )
        # src/ll/UL4.g:665:4: n= expr_subscript '&=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred88_UL43390)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 32, self.FOLLOW_32_in_synpred88_UL43392)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred88_UL43396)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred88_UL43398)



    # $ANTLR end "synpred88_UL4"



    # $ANTLR start "synpred89_UL4"
    def synpred89_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:666:4: (n= expr_subscript '^=' e= expr_if EOF )
        # src/ll/UL4.g:666:4: n= expr_subscript '^=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred89_UL43407)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 62, self.FOLLOW_62_in_synpred89_UL43409)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred89_UL43413)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred89_UL43415)



    # $ANTLR end "synpred89_UL4"



    # $ANTLR start "synpred90_UL4"
    def synpred90_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:667:4: (n= expr_subscript '|=' e= expr_if EOF )
        # src/ll/UL4.g:667:4: n= expr_subscript '|=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred90_UL43424)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 73, self.FOLLOW_73_in_synpred90_UL43426)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred90_UL43430)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred90_UL43432)



    # $ANTLR end "synpred90_UL4"




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

    def synpred55_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred55_UL4_fragment()
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

    def synpred57_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred57_UL4_fragment()
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

    def synpred44_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred44_UL4_fragment()
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

    def synpred35_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred35_UL4_fragment()
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

    def synpred49_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred49_UL4_fragment()
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

    def synpred90_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred90_UL4_fragment()
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



    # lookup tables for DFA #28

    DFA28_eot = DFA.unpack(
        u"\100\uffff"
        )

    DFA28_eof = DFA.unpack(
        u"\1\1\77\uffff"
        )

    DFA28_min = DFA.unpack(
        u"\1\5\52\uffff\1\0\1\uffff\1\0\22\uffff"
        )

    DFA28_max = DFA.unpack(
        u"\1\113\52\uffff\1\0\1\uffff\1\0\22\uffff"
        )

    DFA28_accept = DFA.unpack(
        u"\1\uffff\1\5\72\uffff\1\1\1\3\1\4\1\2"
        )

    DFA28_special = DFA.unpack(
        u"\53\uffff\1\0\1\uffff\1\1\22\uffff"
        )


    DFA28_transition = [
        DFA.unpack(u"\3\1\3\uffff\2\1\1\uffff\3\1\1\uffff\2\1\3\uffff\1\1"
        u"\4\uffff\5\1\1\55\11\1\1\74\17\1\1\53\20\1"),
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
                LA28_43 = input.LA(1)

                 
                index28_43 = input.index()
                input.rewind()

                s = -1
                if (self.synpred48_UL4()):
                    s = 61

                elif (self.synpred49_UL4()):
                    s = 62

                elif (True):
                    s = 1

                 
                input.seek(index28_43)

                if s >= 0:
                    return s
            elif s == 1: 
                LA28_45 = input.LA(1)

                 
                index28_45 = input.index()
                input.rewind()

                s = -1
                if (self.synpred47_UL4()):
                    s = 63

                elif (True):
                    s = 1

                 
                input.seek(index28_45)

                if s >= 0:
                    return s

            if self._state.backtracking > 0:
                raise BacktrackingFailed

            nvae = NoViableAltException(self_.getDescription(), 28, _s, input)
            self_.error(nvae)
            raise nvae

 

    FOLLOW_NONE_in_none829 = frozenset([1])
    FOLLOW_TRUE_in_true_846 = frozenset([1])
    FOLLOW_FALSE_in_false_863 = frozenset([1])
    FOLLOW_INT_in_int_880 = frozenset([1])
    FOLLOW_FLOAT_in_float_897 = frozenset([1])
    FOLLOW_STRING_in_string914 = frozenset([1])
    FOLLOW_STRING3_in_string921 = frozenset([1])
    FOLLOW_DATE_in_date938 = frozenset([1])
    FOLLOW_DATETIME_in_datetime955 = frozenset([1])
    FOLLOW_COLOR_in_color972 = frozenset([1])
    FOLLOW_NAME_in_name989 = frozenset([1])
    FOLLOW_none_in_literal1008 = frozenset([1])
    FOLLOW_false__in_literal1017 = frozenset([1])
    FOLLOW_true__in_literal1026 = frozenset([1])
    FOLLOW_int__in_literal1035 = frozenset([1])
    FOLLOW_float__in_literal1044 = frozenset([1])
    FOLLOW_string_in_literal1053 = frozenset([1])
    FOLLOW_date_in_literal1062 = frozenset([1])
    FOLLOW_datetime_in_literal1071 = frozenset([1])
    FOLLOW_color_in_literal1080 = frozenset([1])
    FOLLOW_name_in_literal1089 = frozenset([1])
    FOLLOW_expr_if_in_seqitem1114 = frozenset([1])
    FOLLOW_35_in_seqitem1125 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_seqitem1131 = frozenset([1])
    FOLLOW_59_in_list1152 = frozenset([60])
    FOLLOW_60_in_list1158 = frozenset([1])
    FOLLOW_59_in_list1169 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 41, 59, 69, 71, 75])
    FOLLOW_seqitem_in_list1177 = frozenset([40, 60])
    FOLLOW_40_in_list1188 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 41, 59, 69, 71, 75])
    FOLLOW_seqitem_in_list1195 = frozenset([40, 60])
    FOLLOW_40_in_list1206 = frozenset([60])
    FOLLOW_60_in_list1213 = frozenset([1])
    FOLLOW_59_in_listcomprehension1241 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_listcomprehension1247 = frozenset([65])
    FOLLOW_65_in_listcomprehension1251 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_listcomprehension1257 = frozenset([67])
    FOLLOW_67_in_listcomprehension1261 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_listcomprehension1267 = frozenset([60, 66])
    FOLLOW_66_in_listcomprehension1276 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_listcomprehension1283 = frozenset([60])
    FOLLOW_60_in_listcomprehension1296 = frozenset([1])
    FOLLOW_71_in_set1319 = frozenset([44])
    FOLLOW_44_in_set1323 = frozenset([74])
    FOLLOW_74_in_set1329 = frozenset([1])
    FOLLOW_71_in_set1340 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 41, 59, 69, 71, 75])
    FOLLOW_seqitem_in_set1348 = frozenset([40, 74])
    FOLLOW_40_in_set1359 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 41, 59, 69, 71, 75])
    FOLLOW_seqitem_in_set1366 = frozenset([40, 74])
    FOLLOW_40_in_set1377 = frozenset([74])
    FOLLOW_74_in_set1384 = frozenset([1])
    FOLLOW_71_in_setcomprehension1412 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_setcomprehension1418 = frozenset([65])
    FOLLOW_65_in_setcomprehension1422 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_setcomprehension1428 = frozenset([67])
    FOLLOW_67_in_setcomprehension1432 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_setcomprehension1438 = frozenset([66, 74])
    FOLLOW_66_in_setcomprehension1447 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_setcomprehension1454 = frozenset([74])
    FOLLOW_74_in_setcomprehension1467 = frozenset([1])
    FOLLOW_expr_if_in_dictitem1492 = frozenset([48])
    FOLLOW_48_in_dictitem1496 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictitem1502 = frozenset([1])
    FOLLOW_36_in_dictitem1513 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictitem1519 = frozenset([1])
    FOLLOW_71_in_dict1540 = frozenset([74])
    FOLLOW_74_in_dict1546 = frozenset([1])
    FOLLOW_71_in_dict1557 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 36, 41, 59, 69, 71, 75])
    FOLLOW_dictitem_in_dict1565 = frozenset([40, 74])
    FOLLOW_40_in_dict1576 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 36, 41, 59, 69, 71, 75])
    FOLLOW_dictitem_in_dict1583 = frozenset([40, 74])
    FOLLOW_40_in_dict1594 = frozenset([74])
    FOLLOW_74_in_dict1601 = frozenset([1])
    FOLLOW_71_in_dictcomprehension1629 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictcomprehension1635 = frozenset([48])
    FOLLOW_48_in_dictcomprehension1639 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictcomprehension1645 = frozenset([65])
    FOLLOW_65_in_dictcomprehension1649 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_dictcomprehension1655 = frozenset([67])
    FOLLOW_67_in_dictcomprehension1659 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictcomprehension1665 = frozenset([66, 74])
    FOLLOW_66_in_dictcomprehension1674 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_dictcomprehension1681 = frozenset([74])
    FOLLOW_74_in_dictcomprehension1694 = frozenset([1])
    FOLLOW_expr_if_in_generatorexpression1722 = frozenset([65])
    FOLLOW_65_in_generatorexpression1728 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_generatorexpression1734 = frozenset([67])
    FOLLOW_67_in_generatorexpression1738 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_generatorexpression1744 = frozenset([1, 66])
    FOLLOW_66_in_generatorexpression1755 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_generatorexpression1762 = frozenset([1])
    FOLLOW_literal_in_atom1788 = frozenset([1])
    FOLLOW_list_in_atom1797 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1806 = frozenset([1])
    FOLLOW_set_in_atom1815 = frozenset([1])
    FOLLOW_setcomprehension_in_atom1824 = frozenset([1])
    FOLLOW_dict_in_atom1833 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1842 = frozenset([1])
    FOLLOW_33_in_atom1851 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_generatorexpression_in_atom1855 = frozenset([34])
    FOLLOW_34_in_atom1859 = frozenset([1])
    FOLLOW_33_in_atom1868 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_atom1872 = frozenset([34])
    FOLLOW_34_in_atom1876 = frozenset([1])
    FOLLOW_expr_subscript_in_nestedlvalue1899 = frozenset([1])
    FOLLOW_33_in_nestedlvalue1908 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_nestedlvalue1912 = frozenset([40])
    FOLLOW_40_in_nestedlvalue1914 = frozenset([34])
    FOLLOW_34_in_nestedlvalue1916 = frozenset([1])
    FOLLOW_33_in_nestedlvalue1925 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_nestedlvalue1931 = frozenset([40])
    FOLLOW_40_in_nestedlvalue1935 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_nestedlvalue1941 = frozenset([34, 40])
    FOLLOW_40_in_nestedlvalue1952 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_nestedlvalue1959 = frozenset([34, 40])
    FOLLOW_40_in_nestedlvalue1970 = frozenset([34])
    FOLLOW_34_in_nestedlvalue1975 = frozenset([1])
    FOLLOW_expr_if_in_slice2008 = frozenset([48])
    FOLLOW_48_in_slice2021 = frozenset([1, 5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_slice2034 = frozenset([1])
    FOLLOW_exprarg_in_argument2066 = frozenset([1])
    FOLLOW_name_in_argument2077 = frozenset([53])
    FOLLOW_53_in_argument2079 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_argument2083 = frozenset([1])
    FOLLOW_35_in_argument2094 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_argument2100 = frozenset([1])
    FOLLOW_36_in_argument2111 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_argument2117 = frozenset([1])
    FOLLOW_atom_in_expr_subscript2138 = frozenset([1, 33, 43, 59])
    FOLLOW_43_in_expr_subscript2154 = frozenset([15])
    FOLLOW_name_in_expr_subscript2161 = frozenset([1, 33, 43, 59])
    FOLLOW_33_in_expr_subscript2177 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_argument_in_expr_subscript2192 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 40, 41, 59, 69, 71, 75])
    FOLLOW_40_in_expr_subscript2207 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_argument_in_expr_subscript2216 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 40, 41, 59, 69, 71, 75])
    FOLLOW_40_in_expr_subscript2231 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_34_in_expr_subscript2245 = frozenset([1, 33, 43, 59])
    FOLLOW_59_in_expr_subscript2261 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_expr_subscript2269 = frozenset([60])
    FOLLOW_60_in_expr_subscript2276 = frozenset([1, 33, 43, 59])
    FOLLOW_59_in_expr_subscript2292 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 48, 59, 69, 71, 75])
    FOLLOW_slice_in_expr_subscript2300 = frozenset([60])
    FOLLOW_60_in_expr_subscript2307 = frozenset([1, 33, 43, 59])
    FOLLOW_expr_subscript_in_expr_unary2335 = frozenset([1])
    FOLLOW_41_in_expr_unary2346 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_unary_in_expr_unary2350 = frozenset([1])
    FOLLOW_75_in_expr_unary2361 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_unary_in_expr_unary2365 = frozenset([1])
    FOLLOW_expr_unary_in_expr_mul2389 = frozenset([1, 29, 35, 44, 45])
    FOLLOW_35_in_expr_mul2406 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_44_in_expr_mul2419 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_45_in_expr_mul2432 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_29_in_expr_mul2445 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_unary_in_expr_mul2459 = frozenset([1, 29, 35, 44, 45])
    FOLLOW_expr_mul_in_expr_add2487 = frozenset([1, 38, 41])
    FOLLOW_38_in_expr_add2504 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_41_in_expr_add2517 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_mul_in_expr_add2531 = frozenset([1, 38, 41])
    FOLLOW_expr_add_in_expr_bitshift2559 = frozenset([1, 50, 57])
    FOLLOW_50_in_expr_bitshift2576 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_57_in_expr_bitshift2589 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_add_in_expr_bitshift2603 = frozenset([1, 50, 57])
    FOLLOW_expr_bitshift_in_expr_bitand2631 = frozenset([1, 31])
    FOLLOW_31_in_expr_bitand2642 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_bitshift_in_expr_bitand2649 = frozenset([1, 31])
    FOLLOW_expr_bitand_in_expr_bitxor2677 = frozenset([1, 61])
    FOLLOW_61_in_expr_bitxor2688 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_bitand_in_expr_bitxor2695 = frozenset([1, 61])
    FOLLOW_expr_bitxor_in_expr_bitor2723 = frozenset([1, 72])
    FOLLOW_72_in_expr_bitor2734 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_bitxor_in_expr_bitor2741 = frozenset([1, 72])
    FOLLOW_expr_bitor_in_expr_cmp2769 = frozenset([1, 28, 49, 52, 54, 55, 56, 67, 68, 69])
    FOLLOW_54_in_expr_cmp2786 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_28_in_expr_cmp2799 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_49_in_expr_cmp2812 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_52_in_expr_cmp2825 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_55_in_expr_cmp2838 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_56_in_expr_cmp2851 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_67_in_expr_cmp2864 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_69_in_expr_cmp2877 = frozenset([67])
    FOLLOW_67_in_expr_cmp2879 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_68_in_expr_cmp2892 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_68_in_expr_cmp2905 = frozenset([69])
    FOLLOW_69_in_expr_cmp2907 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_bitor_in_expr_cmp2921 = frozenset([1, 28, 49, 52, 54, 55, 56, 67, 68, 69])
    FOLLOW_expr_cmp_in_expr_not2949 = frozenset([1])
    FOLLOW_69_in_expr_not2960 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_not_in_expr_not2964 = frozenset([1])
    FOLLOW_expr_not_in_expr_and2988 = frozenset([1, 63])
    FOLLOW_63_in_expr_and2999 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_not_in_expr_and3006 = frozenset([1, 63])
    FOLLOW_expr_and_in_expr_or3034 = frozenset([1, 70])
    FOLLOW_70_in_expr_or3045 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_and_in_expr_or3052 = frozenset([1, 70])
    FOLLOW_expr_or_in_expr_if3080 = frozenset([1, 66])
    FOLLOW_66_in_expr_if3091 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_or_in_expr_if3098 = frozenset([64])
    FOLLOW_64_in_expr_if3103 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_or_in_expr_if3110 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg3134 = frozenset([1])
    FOLLOW_expr_if_in_exprarg3143 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3162 = frozenset([])
    FOLLOW_EOF_in_expression3164 = frozenset([1])
    FOLLOW_expr_if_in_expression3173 = frozenset([])
    FOLLOW_EOF_in_expression3175 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3200 = frozenset([67])
    FOLLOW_67_in_for_3204 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_for_3210 = frozenset([])
    FOLLOW_EOF_in_for_3216 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3237 = frozenset([53])
    FOLLOW_53_in_statement3239 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3243 = frozenset([])
    FOLLOW_EOF_in_statement3245 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3254 = frozenset([39])
    FOLLOW_39_in_statement3256 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3260 = frozenset([])
    FOLLOW_EOF_in_statement3262 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3271 = frozenset([42])
    FOLLOW_42_in_statement3273 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3277 = frozenset([])
    FOLLOW_EOF_in_statement3279 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3288 = frozenset([37])
    FOLLOW_37_in_statement3290 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3294 = frozenset([])
    FOLLOW_EOF_in_statement3296 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3305 = frozenset([47])
    FOLLOW_47_in_statement3307 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3311 = frozenset([])
    FOLLOW_EOF_in_statement3313 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3322 = frozenset([46])
    FOLLOW_46_in_statement3324 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3328 = frozenset([])
    FOLLOW_EOF_in_statement3330 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3339 = frozenset([30])
    FOLLOW_30_in_statement3341 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3345 = frozenset([])
    FOLLOW_EOF_in_statement3347 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3356 = frozenset([51])
    FOLLOW_51_in_statement3358 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3362 = frozenset([])
    FOLLOW_EOF_in_statement3364 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3373 = frozenset([58])
    FOLLOW_58_in_statement3375 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3379 = frozenset([])
    FOLLOW_EOF_in_statement3381 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3390 = frozenset([32])
    FOLLOW_32_in_statement3392 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3396 = frozenset([])
    FOLLOW_EOF_in_statement3398 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3407 = frozenset([62])
    FOLLOW_62_in_statement3409 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3413 = frozenset([])
    FOLLOW_EOF_in_statement3415 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3424 = frozenset([73])
    FOLLOW_73_in_statement3426 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_statement3430 = frozenset([])
    FOLLOW_EOF_in_statement3432 = frozenset([1])
    FOLLOW_expression_in_statement3441 = frozenset([])
    FOLLOW_EOF_in_statement3443 = frozenset([1])
    FOLLOW_name_in_definition3477 = frozenset([33])
    FOLLOW_signature_in_definition3495 = frozenset([])
    FOLLOW_EOF_in_definition3506 = frozenset([1])
    FOLLOW_33_in_signature3527 = frozenset([15, 34, 35, 36])
    FOLLOW_36_in_signature3547 = frozenset([15])
    FOLLOW_name_in_signature3551 = frozenset([34, 40])
    FOLLOW_40_in_signature3557 = frozenset([34])
    FOLLOW_35_in_signature3569 = frozenset([15])
    FOLLOW_name_in_signature3573 = frozenset([34, 40])
    FOLLOW_40_in_signature3584 = frozenset([36])
    FOLLOW_36_in_signature3589 = frozenset([15])
    FOLLOW_name_in_signature3593 = frozenset([34, 40])
    FOLLOW_40_in_signature3604 = frozenset([34])
    FOLLOW_name_in_signature3618 = frozenset([53])
    FOLLOW_53_in_signature3622 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_signature3628 = frozenset([34, 40])
    FOLLOW_40_in_signature3639 = frozenset([15])
    FOLLOW_name_in_signature3646 = frozenset([53])
    FOLLOW_53_in_signature3651 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_signature3658 = frozenset([34, 40])
    FOLLOW_40_in_signature3674 = frozenset([35])
    FOLLOW_35_in_signature3679 = frozenset([15])
    FOLLOW_name_in_signature3683 = frozenset([34, 40])
    FOLLOW_40_in_signature3699 = frozenset([36])
    FOLLOW_36_in_signature3704 = frozenset([15])
    FOLLOW_name_in_signature3708 = frozenset([34, 40])
    FOLLOW_40_in_signature3719 = frozenset([34])
    FOLLOW_name_in_signature3733 = frozenset([34, 40])
    FOLLOW_40_in_signature3744 = frozenset([15])
    FOLLOW_name_in_signature3751 = frozenset([34, 40])
    FOLLOW_40_in_signature3767 = frozenset([15])
    FOLLOW_name_in_signature3774 = frozenset([53])
    FOLLOW_53_in_signature3779 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_exprarg_in_signature3786 = frozenset([34, 40])
    FOLLOW_40_in_signature3802 = frozenset([35])
    FOLLOW_35_in_signature3807 = frozenset([15])
    FOLLOW_name_in_signature3811 = frozenset([34, 40])
    FOLLOW_40_in_signature3827 = frozenset([36])
    FOLLOW_36_in_signature3832 = frozenset([15])
    FOLLOW_name_in_signature3836 = frozenset([34, 40])
    FOLLOW_40_in_signature3847 = frozenset([34])
    FOLLOW_34_in_signature3856 = frozenset([])
    FOLLOW_EOF_in_signature3861 = frozenset([1])
    FOLLOW_list_in_synpred27_UL41797 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred28_UL41806 = frozenset([1])
    FOLLOW_set_in_synpred29_UL41815 = frozenset([1])
    FOLLOW_setcomprehension_in_synpred30_UL41824 = frozenset([1])
    FOLLOW_dict_in_synpred31_UL41833 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred32_UL41842 = frozenset([1])
    FOLLOW_33_in_synpred33_UL41851 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_generatorexpression_in_synpred33_UL41855 = frozenset([34])
    FOLLOW_34_in_synpred33_UL41859 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred34_UL41899 = frozenset([1])
    FOLLOW_33_in_synpred35_UL41908 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 59, 71])
    FOLLOW_nestedlvalue_in_synpred35_UL41912 = frozenset([40])
    FOLLOW_40_in_synpred35_UL41914 = frozenset([34])
    FOLLOW_34_in_synpred35_UL41916 = frozenset([1])
    FOLLOW_40_in_synpred44_UL42207 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_argument_in_synpred44_UL42216 = frozenset([1])
    FOLLOW_33_in_synpred47_UL42177 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_argument_in_synpred47_UL42192 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 40, 41, 59, 69, 71, 75])
    FOLLOW_40_in_synpred47_UL42207 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_argument_in_synpred47_UL42216 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 40, 41, 59, 69, 71, 75])
    FOLLOW_40_in_synpred47_UL42231 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 34, 35, 36, 41, 59, 69, 71, 75])
    FOLLOW_34_in_synpred47_UL42245 = frozenset([1])
    FOLLOW_59_in_synpred48_UL42261 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred48_UL42269 = frozenset([60])
    FOLLOW_60_in_synpred48_UL42276 = frozenset([1])
    FOLLOW_59_in_synpred49_UL42292 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 48, 59, 69, 71, 75])
    FOLLOW_slice_in_synpred49_UL42300 = frozenset([60])
    FOLLOW_60_in_synpred49_UL42307 = frozenset([1])
    FOLLOW_set_in_synpred55_UL42400 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_unary_in_synpred55_UL42459 = frozenset([1])
    FOLLOW_set_in_synpred57_UL42498 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 71, 75])
    FOLLOW_expr_mul_in_synpred57_UL42531 = frozenset([1])
    FOLLOW_66_in_synpred76_UL43091 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_or_in_synpred76_UL43098 = frozenset([64])
    FOLLOW_64_in_synpred76_UL43103 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_or_in_synpred76_UL43110 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred77_UL43134 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred78_UL43162 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43164 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred79_UL43237 = frozenset([53])
    FOLLOW_53_in_synpred79_UL43239 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred79_UL43243 = frozenset([])
    FOLLOW_EOF_in_synpred79_UL43245 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred80_UL43254 = frozenset([39])
    FOLLOW_39_in_synpred80_UL43256 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred80_UL43260 = frozenset([])
    FOLLOW_EOF_in_synpred80_UL43262 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred81_UL43271 = frozenset([42])
    FOLLOW_42_in_synpred81_UL43273 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred81_UL43277 = frozenset([])
    FOLLOW_EOF_in_synpred81_UL43279 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred82_UL43288 = frozenset([37])
    FOLLOW_37_in_synpred82_UL43290 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred82_UL43294 = frozenset([])
    FOLLOW_EOF_in_synpred82_UL43296 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred83_UL43305 = frozenset([47])
    FOLLOW_47_in_synpred83_UL43307 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred83_UL43311 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43313 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred84_UL43322 = frozenset([46])
    FOLLOW_46_in_synpred84_UL43324 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred84_UL43328 = frozenset([])
    FOLLOW_EOF_in_synpred84_UL43330 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred85_UL43339 = frozenset([30])
    FOLLOW_30_in_synpred85_UL43341 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred85_UL43345 = frozenset([])
    FOLLOW_EOF_in_synpred85_UL43347 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred86_UL43356 = frozenset([51])
    FOLLOW_51_in_synpred86_UL43358 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred86_UL43362 = frozenset([])
    FOLLOW_EOF_in_synpred86_UL43364 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred87_UL43373 = frozenset([58])
    FOLLOW_58_in_synpred87_UL43375 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred87_UL43379 = frozenset([])
    FOLLOW_EOF_in_synpred87_UL43381 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred88_UL43390 = frozenset([32])
    FOLLOW_32_in_synpred88_UL43392 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred88_UL43396 = frozenset([])
    FOLLOW_EOF_in_synpred88_UL43398 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred89_UL43407 = frozenset([62])
    FOLLOW_62_in_synpred89_UL43409 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred89_UL43413 = frozenset([])
    FOLLOW_EOF_in_synpred89_UL43415 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred90_UL43424 = frozenset([73])
    FOLLOW_73_in_synpred90_UL43426 = frozenset([5, 6, 7, 11, 12, 14, 15, 16, 18, 19, 23, 33, 41, 59, 69, 71, 75])
    FOLLOW_expr_if_in_synpred90_UL43430 = frozenset([])
    FOLLOW_EOF_in_synpred90_UL43432 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
