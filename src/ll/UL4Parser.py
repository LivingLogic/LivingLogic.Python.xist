# $ANTLR 3.4 src/ll/UL4.g 2012-10-29 17:47:35

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


import datetime, ast
from ll import ul4c, color



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
T__25=25
T__26=26
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
TIME=18
TRUE=19
UNDEFINED=20
UNICODE1_ESC=21
UNICODE2_ESC=22
UNICODE4_ESC=23
WS=24

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "BIN_DIGIT", "COLOR", "DATE", "DIGIT", "ESC_SEQ", "EXPONENT", "FALSE", 
    "FLOAT", "HEX_DIGIT", "INT", "NAME", "NONE", "OCT_DIGIT", "STRING", 
    "TIME", "TRUE", "UNDEFINED", "UNICODE1_ESC", "UNICODE2_ESC", "UNICODE4_ESC", 
    "WS", "'!='", "'%'", "'%='", "'('", "')'", "'*'", "'**'", "'*='", "'+'", 
    "'+='", "','", "'-'", "'-='", "'.'", "'/'", "'//'", "'//='", "'/='", 
    "':'", "'<'", "'<='", "'='", "'=='", "'>'", "'>='", "'['", "']'", "'and'", 
    "'for'", "'if'", "'in'", "'not'", "'or'", "'{'", "'}'"
]




class UL4Parser(Parser):
    grammarFileName = "src/ll/UL4.g"
    api_version = 1
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(UL4Parser, self).__init__(input, state, *args, **kwargs)




        self.delegates = []




             
    def mismatch(self, input, ttype, follow):
        raise MismatchedTokenException(ttype, input)

    def recoverFromMismatchedSet(self, input, e, follow):
        raise e



    # $ANTLR start "undefined"
    # src/ll/UL4.g:146:1: undefined returns [node] : UNDEFINED ;
    def undefined(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:147:2: ( UNDEFINED )
                # src/ll/UL4.g:147:4: UNDEFINED
                pass 
                self.match(self.input, UNDEFINED, self.FOLLOW_UNDEFINED_in_undefined706)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, ul4c.Undefined) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "undefined"



    # $ANTLR start "none"
    # src/ll/UL4.g:150:1: none returns [node] : NONE ;
    def none(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:151:2: ( NONE )
                # src/ll/UL4.g:151:4: NONE
                pass 
                self.match(self.input, NONE, self.FOLLOW_NONE_in_none723)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, None) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "none"



    # $ANTLR start "true_"
    # src/ll/UL4.g:154:1: true_ returns [node] : TRUE ;
    def true_(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:155:2: ( TRUE )
                # src/ll/UL4.g:155:4: TRUE
                pass 
                self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_740)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, True) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "true_"



    # $ANTLR start "false_"
    # src/ll/UL4.g:158:1: false_ returns [node] : FALSE ;
    def false_(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:159:2: ( FALSE )
                # src/ll/UL4.g:159:4: FALSE
                pass 
                self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_757)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, False) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "false_"



    # $ANTLR start "int_"
    # src/ll/UL4.g:162:1: int_ returns [node] : INT ;
    def int_(self, ):
        node = None


        INT1 = None

        try:
            try:
                # src/ll/UL4.g:163:2: ( INT )
                # src/ll/UL4.g:163:4: INT
                pass 
                INT1 = self.match(self.input, INT, self.FOLLOW_INT_in_int_774)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, int(INT1.text, 0)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "int_"



    # $ANTLR start "float_"
    # src/ll/UL4.g:166:1: float_ returns [node] : FLOAT ;
    def float_(self, ):
        node = None


        FLOAT2 = None

        try:
            try:
                # src/ll/UL4.g:167:2: ( FLOAT )
                # src/ll/UL4.g:167:4: FLOAT
                pass 
                FLOAT2 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_791)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, float(FLOAT2.text)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "float_"



    # $ANTLR start "string"
    # src/ll/UL4.g:170:1: string returns [node] : STRING ;
    def string(self, ):
        node = None


        STRING3 = None

        try:
            try:
                # src/ll/UL4.g:171:2: ( STRING )
                # src/ll/UL4.g:171:4: STRING
                pass 
                STRING3 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string808)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, ast.literal_eval(STRING3.text)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "string"



    # $ANTLR start "date"
    # src/ll/UL4.g:174:1: date returns [node] : DATE ;
    def date(self, ):
        node = None


        DATE4 = None

        try:
            try:
                # src/ll/UL4.g:175:2: ( DATE )
                # src/ll/UL4.g:175:4: DATE
                pass 
                DATE4 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date825)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, datetime.datetime(*map(int, [f for f in ul4c.datesplitter.split(DATE4.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "date"



    # $ANTLR start "color"
    # src/ll/UL4.g:178:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR5 = None

        try:
            try:
                # src/ll/UL4.g:179:2: ( COLOR )
                # src/ll/UL4.g:179:4: COLOR
                pass 
                COLOR5 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color842)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.Const(self.location, color.Color.fromrepr(COLOR5.text)) 






                       
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
    # src/ll/UL4.g:182:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME6 = None

        try:
            try:
                # src/ll/UL4.g:183:2: ( NAME )
                # src/ll/UL4.g:183:4: NAME
                pass 
                NAME6 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name859)

                if self._state.backtracking == 0:
                    pass
                    retval.node =  ul4c.Var(self.location, NAME6.text) 





                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "name"



    # $ANTLR start "literal"
    # src/ll/UL4.g:186:1: literal returns [node] : (e_undefined= undefined |e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name );
    def literal(self, ):
        node = None


        e_undefined = None

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
                # src/ll/UL4.g:187:2: (e_undefined= undefined |e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name )
                alt1 = 10
                LA1 = self.input.LA(1)
                if LA1 == UNDEFINED:
                    alt1 = 1
                elif LA1 == NONE:
                    alt1 = 2
                elif LA1 == FALSE:
                    alt1 = 3
                elif LA1 == TRUE:
                    alt1 = 4
                elif LA1 == INT:
                    alt1 = 5
                elif LA1 == FLOAT:
                    alt1 = 6
                elif LA1 == STRING:
                    alt1 = 7
                elif LA1 == DATE:
                    alt1 = 8
                elif LA1 == COLOR:
                    alt1 = 9
                elif LA1 == NAME:
                    alt1 = 10
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae


                if alt1 == 1:
                    # src/ll/UL4.g:187:4: e_undefined= undefined
                    pass 
                    self._state.following.append(self.FOLLOW_undefined_in_literal878)
                    e_undefined = self.undefined()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_undefined 




                elif alt1 == 2:
                    # src/ll/UL4.g:188:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal887)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt1 == 3:
                    # src/ll/UL4.g:189:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal896)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt1 == 4:
                    # src/ll/UL4.g:190:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal905)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt1 == 5:
                    # src/ll/UL4.g:191:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal914)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt1 == 6:
                    # src/ll/UL4.g:192:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal923)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt1 == 7:
                    # src/ll/UL4.g:193:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal932)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt1 == 8:
                    # src/ll/UL4.g:194:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal941)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt1 == 9:
                    # src/ll/UL4.g:195:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal950)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt1 == 10:
                    # src/ll/UL4.g:196:4: e_name= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_literal959)
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



    # $ANTLR start "list"
    # src/ll/UL4.g:200:1: list returns [node] : ( '[' ']' | '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']' );
    def list(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:201:2: ( '[' ']' | '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']' )
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == 50) :
                    LA4_1 = self.input.LA(2)

                    if (LA4_1 == 51) :
                        alt4 = 1
                    elif ((COLOR <= LA4_1 <= DATE) or (FALSE <= LA4_1 <= FLOAT) or (INT <= LA4_1 <= NONE) or LA4_1 == STRING or (TRUE <= LA4_1 <= UNDEFINED) or LA4_1 == 28 or LA4_1 == 36 or LA4_1 == 50 or LA4_1 == 56 or LA4_1 == 58) :
                        alt4 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 4, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 4, 0, self.input)

                    raise nvae


                if alt4 == 1:
                    # src/ll/UL4.g:202:3: '[' ']'
                    pass 
                    self.match(self.input, 50, self.FOLLOW_50_in_list980)

                    self.match(self.input, 51, self.FOLLOW_51_in_list984)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.List(self.location) 




                elif alt4 == 2:
                    # src/ll/UL4.g:205:3: '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']'
                    pass 
                    self.match(self.input, 50, self.FOLLOW_50_in_list993)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.List(self.location) 



                    self._state.following.append(self.FOLLOW_expr1_in_list1001)
                    e1 = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1); 



                    # src/ll/UL4.g:207:3: ( ',' e2= expr1 )*
                    while True: #loop2
                        alt2 = 2
                        LA2_0 = self.input.LA(1)

                        if (LA2_0 == 35) :
                            LA2_1 = self.input.LA(2)

                            if ((COLOR <= LA2_1 <= DATE) or (FALSE <= LA2_1 <= FLOAT) or (INT <= LA2_1 <= NONE) or LA2_1 == STRING or (TRUE <= LA2_1 <= UNDEFINED) or LA2_1 == 28 or LA2_1 == 36 or LA2_1 == 50 or LA2_1 == 56 or LA2_1 == 58) :
                                alt2 = 1




                        if alt2 == 1:
                            # src/ll/UL4.g:208:4: ',' e2= expr1
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_list1012)

                            self._state.following.append(self.FOLLOW_expr1_in_list1019)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2); 




                        else:
                            break #loop2


                    # src/ll/UL4.g:211:3: ( ',' )?
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == 35) :
                        alt3 = 1
                    if alt3 == 1:
                        # src/ll/UL4.g:211:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_list1030)




                    self.match(self.input, 51, self.FOLLOW_51_in_list1035)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "list"



    # $ANTLR start "listcomprehension"
    # src/ll/UL4.g:215:1: listcomprehension returns [node] : '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']' ;
    def listcomprehension(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:220:2: ( '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']' )
                # src/ll/UL4.g:221:3: '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']'
                pass 
                self.match(self.input, 50, self.FOLLOW_50_in_listcomprehension1059)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1065)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 53, self.FOLLOW_53_in_listcomprehension1069)

                self._state.following.append(self.FOLLOW_nestedname_in_listcomprehension1075)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_listcomprehension1079)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1085)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:227:3: ( 'if' condition= expr1 )?
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 54) :
                    alt5 = 1
                if alt5 == 1:
                    # src/ll/UL4.g:228:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_listcomprehension1094)

                    self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1101)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                self.match(self.input, 51, self.FOLLOW_51_in_listcomprehension1112)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.ListComp(self.location, item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:236:1: fragment dictitem returns [node] : (k= expr1 ':' v= expr1 | '**' d= expr1 );
    def dictitem(self, ):
        node = None


        k = None

        v = None

        d = None


        try:
            try:
                # src/ll/UL4.g:237:2: (k= expr1 ':' v= expr1 | '**' d= expr1 )
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if ((COLOR <= LA6_0 <= DATE) or (FALSE <= LA6_0 <= FLOAT) or (INT <= LA6_0 <= NONE) or LA6_0 == STRING or (TRUE <= LA6_0 <= UNDEFINED) or LA6_0 == 28 or LA6_0 == 36 or LA6_0 == 50 or LA6_0 == 56 or LA6_0 == 58) :
                    alt6 = 1
                elif (LA6_0 == 31) :
                    alt6 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 6, 0, self.input)

                    raise nvae


                if alt6 == 1:
                    # src/ll/UL4.g:238:3: k= expr1 ':' v= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_dictitem1137)
                    k = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, 43, self.FOLLOW_43_in_dictitem1141)

                    self._state.following.append(self.FOLLOW_expr1_in_dictitem1147)
                    v = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (k, v) 




                elif alt6 == 2:
                    # src/ll/UL4.g:242:3: '**' d= expr1
                    pass 
                    self.match(self.input, 31, self.FOLLOW_31_in_dictitem1156)

                    self._state.following.append(self.FOLLOW_expr1_in_dictitem1162)
                    d = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (d,) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictitem"



    # $ANTLR start "dict"
    # src/ll/UL4.g:246:1: dict returns [node] : ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' );
    def dict(self, ):
        node = None


        i1 = None

        i2 = None


        try:
            try:
                # src/ll/UL4.g:247:2: ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 58) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 59) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or LA9_1 == STRING or (TRUE <= LA9_1 <= UNDEFINED) or LA9_1 == 28 or LA9_1 == 31 or LA9_1 == 36 or LA9_1 == 50 or LA9_1 == 56 or LA9_1 == 58) :
                        alt9 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 9, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 9, 0, self.input)

                    raise nvae


                if alt9 == 1:
                    # src/ll/UL4.g:248:3: '{' '}'
                    pass 
                    self.match(self.input, 58, self.FOLLOW_58_in_dict1181)

                    self.match(self.input, 59, self.FOLLOW_59_in_dict1185)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Dict(self.location) 




                elif alt9 == 2:
                    # src/ll/UL4.g:251:3: '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}'
                    pass 
                    self.match(self.input, 58, self.FOLLOW_58_in_dict1194)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Dict(self.location) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1202)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1); 



                    # src/ll/UL4.g:253:3: ( ',' i2= dictitem )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 35) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or LA7_1 == STRING or (TRUE <= LA7_1 <= UNDEFINED) or LA7_1 == 28 or LA7_1 == 31 or LA7_1 == 36 or LA7_1 == 50 or LA7_1 == 56 or LA7_1 == 58) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:254:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_dict1213)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1220)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2); 




                        else:
                            break #loop7


                    # src/ll/UL4.g:257:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 35) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:257:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_dict1231)




                    self.match(self.input, 59, self.FOLLOW_59_in_dict1236)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:261:1: dictcomprehension returns [node] : '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' ;
    def dictcomprehension(self, ):
        node = None


        key = None

        value = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:266:2: ( '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' )
                # src/ll/UL4.g:267:3: '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}'
                pass 
                self.match(self.input, 58, self.FOLLOW_58_in_dictcomprehension1260)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1266)
                key = self.expr1()

                self._state.following.pop()

                self.match(self.input, 43, self.FOLLOW_43_in_dictcomprehension1270)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1276)
                value = self.expr1()

                self._state.following.pop()

                self.match(self.input, 53, self.FOLLOW_53_in_dictcomprehension1280)

                self._state.following.append(self.FOLLOW_nestedname_in_dictcomprehension1286)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_dictcomprehension1290)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1296)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:275:3: ( 'if' condition= expr1 )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 54) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:276:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_dictcomprehension1305)

                    self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1312)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                self.match(self.input, 59, self.FOLLOW_59_in_dictcomprehension1323)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.DictComp(self.location, key, value, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:282:1: generatorexpression returns [node] : item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ;
    def generatorexpression(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:287:2: (item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? )
                # src/ll/UL4.g:288:3: item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )?
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1351)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 53, self.FOLLOW_53_in_generatorexpression1355)

                self._state.following.append(self.FOLLOW_nestedname_in_generatorexpression1361)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_generatorexpression1365)

                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1371)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:293:3: ( 'if' condition= expr1 )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 54) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:294:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_generatorexpression1380)

                    self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1387)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.GenExpr(self.location, item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:299:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' );
    def atom(self, ):
        node = None


        e_literal = None

        e_list = None

        e_listcomp = None

        e_dict = None

        e_dictcomp = None

        e_genexpr = None

        e_bracket = None


        try:
            try:
                # src/ll/UL4.g:300:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == COLOR or LA12 == DATE or LA12 == FALSE or LA12 == FLOAT or LA12 == INT or LA12 == NAME or LA12 == NONE or LA12 == STRING or LA12 == TRUE or LA12 == UNDEFINED:
                    alt12 = 1
                elif LA12 == 50:
                    LA12_11 = self.input.LA(2)

                    if (self.synpred21_UL4()) :
                        alt12 = 2
                    elif (self.synpred22_UL4()) :
                        alt12 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 11, self.input)

                        raise nvae


                elif LA12 == 58:
                    LA12_12 = self.input.LA(2)

                    if (self.synpred23_UL4()) :
                        alt12 = 4
                    elif (self.synpred24_UL4()) :
                        alt12 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 12, self.input)

                        raise nvae


                elif LA12 == 28:
                    LA12_13 = self.input.LA(2)

                    if (self.synpred25_UL4()) :
                        alt12 = 6
                    elif (True) :
                        alt12 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae


                if alt12 == 1:
                    # src/ll/UL4.g:300:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1413)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt12 == 2:
                    # src/ll/UL4.g:301:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1422)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt12 == 3:
                    # src/ll/UL4.g:302:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1431)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt12 == 4:
                    # src/ll/UL4.g:303:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1440)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt12 == 5:
                    # src/ll/UL4.g:304:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1449)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt12 == 6:
                    # src/ll/UL4.g:305:4: '(' e_genexpr= generatorexpression ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_atom1456)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1460)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_atom1462)

                    if self._state.backtracking == 0:
                        pass
                        node =  e_genexpr 




                elif alt12 == 7:
                    # src/ll/UL4.g:306:4: '(' e_bracket= expr1 ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_atom1469)

                    self._state.following.append(self.FOLLOW_expr1_in_atom1473)
                    e_bracket = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_atom1475)

                    if self._state.backtracking == 0:
                        pass
                        node =  e_bracket 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "atom"



    # $ANTLR start "nestedname"
    # src/ll/UL4.g:310:1: nestedname returns [varname] : (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' );
    def nestedname(self, ):
        varname = None


        n = None

        n0 = None

        n1 = None

        n2 = None

        n3 = None


        try:
            try:
                # src/ll/UL4.g:311:2: (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if (LA15_0 == NAME) :
                    alt15 = 1
                elif (LA15_0 == 28) :
                    LA15_2 = self.input.LA(2)

                    if (self.synpred27_UL4()) :
                        alt15 = 2
                    elif (True) :
                        alt15 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 15, 2, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 15, 0, self.input)

                    raise nvae


                if alt15 == 1:
                    # src/ll/UL4.g:312:3: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_nestedname1498)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname =  ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0] 




                elif alt15 == 2:
                    # src/ll/UL4.g:314:3: '(' n0= nestedname ',' ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1507)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1511)
                    n0 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 35, self.FOLLOW_35_in_nestedname1513)

                    self.match(self.input, 29, self.FOLLOW_29_in_nestedname1515)

                    if self._state.backtracking == 0:
                        pass
                        varname =  (n0,) 




                elif alt15 == 3:
                    # src/ll/UL4.g:316:3: '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1524)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1530)
                    n1 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 35, self.FOLLOW_35_in_nestedname1534)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1540)
                    n2 = self.nestedname()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname =  (n1, n2) 



                    # src/ll/UL4.g:320:3: ( ',' n3= nestedname )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 35) :
                            LA13_1 = self.input.LA(2)

                            if (LA13_1 == NAME or LA13_1 == 28) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:321:4: ',' n3= nestedname
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_nestedname1551)

                            self._state.following.append(self.FOLLOW_nestedname_in_nestedname1558)
                            n3 = self.nestedname()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                varname += (n3,); 




                        else:
                            break #loop13


                    # src/ll/UL4.g:324:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 35) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:324:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_nestedname1569)




                    self.match(self.input, 29, self.FOLLOW_29_in_nestedname1574)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return varname

    # $ANTLR end "nestedname"



    # $ANTLR start "expr10"
    # src/ll/UL4.g:329:1: expr10 returns [node] : (a= atom |n= name '(' ')' |n= name '(' a1= exprarg ( ',' a2= exprarg )* ( ',' )? ')' );
    def expr10(self, ):
        node = None


        a = None

        n = None

        a1 = None

        a2 = None


        try:
            try:
                # src/ll/UL4.g:330:2: (a= atom |n= name '(' ')' |n= name '(' a1= exprarg ( ',' a2= exprarg )* ( ',' )? ')' )
                alt18 = 3
                LA18_0 = self.input.LA(1)

                if ((COLOR <= LA18_0 <= DATE) or (FALSE <= LA18_0 <= FLOAT) or LA18_0 == INT or LA18_0 == NONE or LA18_0 == STRING or (TRUE <= LA18_0 <= UNDEFINED) or LA18_0 == 28 or LA18_0 == 50 or LA18_0 == 58) :
                    alt18 = 1
                elif (LA18_0 == NAME) :
                    LA18_2 = self.input.LA(2)

                    if (LA18_2 == EOF or (25 <= LA18_2 <= 26) or (29 <= LA18_2 <= 30) or LA18_2 == 33 or (35 <= LA18_2 <= 36) or (38 <= LA18_2 <= 40) or (43 <= LA18_2 <= 45) or (47 <= LA18_2 <= 57) or LA18_2 == 59) :
                        alt18 = 1
                    elif (LA18_2 == 28) :
                        LA18_3 = self.input.LA(3)

                        if (LA18_3 == 29) :
                            alt18 = 2
                        elif ((COLOR <= LA18_3 <= DATE) or (FALSE <= LA18_3 <= FLOAT) or (INT <= LA18_3 <= NONE) or LA18_3 == STRING or (TRUE <= LA18_3 <= UNDEFINED) or LA18_3 == 28 or LA18_3 == 36 or LA18_3 == 50 or LA18_3 == 56 or LA18_3 == 58) :
                            alt18 = 3
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 18, 3, self.input)

                            raise nvae


                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 18, 2, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 18, 0, self.input)

                    raise nvae


                if alt18 == 1:
                    # src/ll/UL4.g:330:4: a= atom
                    pass 
                    self._state.following.append(self.FOLLOW_atom_in_expr101594)
                    a = self.atom()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  a 




                elif alt18 == 2:
                    # src/ll/UL4.g:331:4: n= name '(' ')'
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_expr101603)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 28, self.FOLLOW_28_in_expr101605)

                    self.match(self.input, 29, self.FOLLOW_29_in_expr101607)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.CallFunc(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                elif alt18 == 3:
                    # src/ll/UL4.g:333:3: n= name '(' a1= exprarg ( ',' a2= exprarg )* ( ',' )? ')'
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_expr101618)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.CallFunc(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 



                    self.match(self.input, 28, self.FOLLOW_28_in_expr101624)

                    self._state.following.append(self.FOLLOW_exprarg_in_expr101630)
                    a1 = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.args.append(a1); 



                    # src/ll/UL4.g:336:3: ( ',' a2= exprarg )*
                    while True: #loop16
                        alt16 = 2
                        LA16_0 = self.input.LA(1)

                        if (LA16_0 == 35) :
                            LA16_1 = self.input.LA(2)

                            if ((COLOR <= LA16_1 <= DATE) or (FALSE <= LA16_1 <= FLOAT) or (INT <= LA16_1 <= NONE) or LA16_1 == STRING or (TRUE <= LA16_1 <= UNDEFINED) or LA16_1 == 28 or LA16_1 == 36 or LA16_1 == 50 or LA16_1 == 56 or LA16_1 == 58) :
                                alt16 = 1




                        if alt16 == 1:
                            # src/ll/UL4.g:337:4: ',' a2= exprarg
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr101641)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr101648)
                            a2 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.args.append(a2); 




                        else:
                            break #loop16


                    # src/ll/UL4.g:340:3: ( ',' )?
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == 35) :
                        alt17 = 1
                    if alt17 == 1:
                        # src/ll/UL4.g:340:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_expr101659)




                    self.match(self.input, 29, self.FOLLOW_29_in_expr101664)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr10"



    # $ANTLR start "callarg"
    # src/ll/UL4.g:346:1: fragment callarg returns [node] : (n= name '=' e= exprarg | '**' e= exprarg );
    def callarg(self, ):
        node = None


        n = None

        e = None


        try:
            try:
                # src/ll/UL4.g:347:2: (n= name '=' e= exprarg | '**' e= exprarg )
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == NAME) :
                    alt19 = 1
                elif (LA19_0 == 31) :
                    alt19 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 19, 0, self.input)

                    raise nvae


                if alt19 == 1:
                    # src/ll/UL4.g:348:3: n= name '=' e= exprarg
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_callarg1687)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_callarg1691)

                    self._state.following.append(self.FOLLOW_exprarg_in_callarg1697)
                    e = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt19 == 2:
                    # src/ll/UL4.g:352:3: '**' e= exprarg
                    pass 
                    self.match(self.input, 31, self.FOLLOW_31_in_callarg1706)

                    self._state.following.append(self.FOLLOW_exprarg_in_callarg1712)
                    e = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (e,) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "callarg"



    # $ANTLR start "expr9"
    # src/ll/UL4.g:356:1: expr9 returns [node] : e1= expr10 ( '.' n= name ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )? | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* ;
    def expr9(self, ):
        node = None


        e1 = None

        n = None

        pa1 = None

        pa2 = None

        kwa1 = None

        kwa2 = None

        e2 = None

        e3 = None


         
        callmeth = False
        index1 = None
        index2 = None
        slice = False
        	
        try:
            try:
                # src/ll/UL4.g:364:2: (e1= expr10 ( '.' n= name ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )? | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* )
                # src/ll/UL4.g:365:3: e1= expr10 ( '.' n= name ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )? | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                pass 
                self._state.following.append(self.FOLLOW_expr10_in_expr91740)
                e1 = self.expr10()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:366:3: ( '.' n= name ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )? | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                while True: #loop30
                    alt30 = 3
                    LA30_0 = self.input.LA(1)

                    if (LA30_0 == 38) :
                        alt30 = 1
                    elif (LA30_0 == 50) :
                        alt30 = 2


                    if alt30 == 1:
                        # src/ll/UL4.g:368:4: '.' n= name ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )?
                        pass 
                        self.match(self.input, 38, self.FOLLOW_38_in_expr91756)

                        self._state.following.append(self.FOLLOW_name_in_expr91763)
                        n = self.name()

                        self._state.following.pop()

                        # src/ll/UL4.g:370:4: ( ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' ) )?
                        alt25 = 2
                        LA25_0 = self.input.LA(1)

                        if (LA25_0 == 28) :
                            alt25 = 1
                        if alt25 == 1:
                            # src/ll/UL4.g:372:5: ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' )
                            pass 
                            # src/ll/UL4.g:372:5: ( '(' ')' | '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')' | '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')' )
                            alt24 = 3
                            LA24_0 = self.input.LA(1)

                            if (LA24_0 == 28) :
                                LA24 = self.input.LA(2)
                                if LA24 == 29:
                                    alt24 = 1
                                elif LA24 == COLOR or LA24 == DATE or LA24 == FALSE or LA24 == FLOAT or LA24 == INT or LA24 == NONE or LA24 == STRING or LA24 == TRUE or LA24 == UNDEFINED or LA24 == 28 or LA24 == 36 or LA24 == 50 or LA24 == 56 or LA24 == 58:
                                    alt24 = 2
                                elif LA24 == NAME:
                                    LA24_4 = self.input.LA(3)

                                    if ((25 <= LA24_4 <= 26) or (28 <= LA24_4 <= 30) or LA24_4 == 33 or (35 <= LA24_4 <= 36) or (38 <= LA24_4 <= 40) or (44 <= LA24_4 <= 45) or (47 <= LA24_4 <= 50) or (52 <= LA24_4 <= 53) or (55 <= LA24_4 <= 57)) :
                                        alt24 = 2
                                    elif (LA24_4 == 46) :
                                        alt24 = 3
                                    else:
                                        if self._state.backtracking > 0:
                                            raise BacktrackingFailed


                                        nvae = NoViableAltException("", 24, 4, self.input)

                                        raise nvae


                                elif LA24 == 31:
                                    alt24 = 3
                                else:
                                    if self._state.backtracking > 0:
                                        raise BacktrackingFailed


                                    nvae = NoViableAltException("", 24, 1, self.input)

                                    raise nvae


                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 24, 0, self.input)

                                raise nvae


                            if alt24 == 1:
                                # src/ll/UL4.g:374:6: '(' ')'
                                pass 
                                self.match(self.input, 28, self.FOLLOW_28_in_expr91794)

                                self.match(self.input, 29, self.FOLLOW_29_in_expr91801)

                                if self._state.backtracking == 0:
                                    pass
                                    callmeth = True; node =  ul4c.CallMeth(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], node) 




                            elif alt24 == 2:
                                # src/ll/UL4.g:378:6: '(' pa1= exprarg ( ',' pa2= exprarg )* ( ',' )? ')'
                                pass 
                                self.match(self.input, 28, self.FOLLOW_28_in_expr91823)

                                if self._state.backtracking == 0:
                                    pass
                                    callmeth = True; node =  ul4c.CallMeth(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], node) 



                                self._state.following.append(self.FOLLOW_exprarg_in_expr91834)
                                pa1 = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.args.append(pa1); 



                                # src/ll/UL4.g:380:6: ( ',' pa2= exprarg )*
                                while True: #loop20
                                    alt20 = 2
                                    LA20_0 = self.input.LA(1)

                                    if (LA20_0 == 35) :
                                        LA20_1 = self.input.LA(2)

                                        if ((COLOR <= LA20_1 <= DATE) or (FALSE <= LA20_1 <= FLOAT) or (INT <= LA20_1 <= NONE) or LA20_1 == STRING or (TRUE <= LA20_1 <= UNDEFINED) or LA20_1 == 28 or LA20_1 == 36 or LA20_1 == 50 or LA20_1 == 56 or LA20_1 == 58) :
                                            alt20 = 1




                                    if alt20 == 1:
                                        # src/ll/UL4.g:381:7: ',' pa2= exprarg
                                        pass 
                                        self.match(self.input, 35, self.FOLLOW_35_in_expr91851)

                                        self._state.following.append(self.FOLLOW_exprarg_in_expr91861)
                                        pa2 = self.exprarg()

                                        self._state.following.pop()

                                        if self._state.backtracking == 0:
                                            pass
                                            node.args.append(pa2); 




                                    else:
                                        break #loop20


                                # src/ll/UL4.g:384:6: ( ',' )?
                                alt21 = 2
                                LA21_0 = self.input.LA(1)

                                if (LA21_0 == 35) :
                                    alt21 = 1
                                if alt21 == 1:
                                    # src/ll/UL4.g:384:6: ','
                                    pass 
                                    self.match(self.input, 35, self.FOLLOW_35_in_expr91878)




                                self.match(self.input, 29, self.FOLLOW_29_in_expr91886)


                            elif alt24 == 3:
                                # src/ll/UL4.g:388:6: '(' kwa1= callarg ( ',' kwa2= callarg )* ( ',' )? ')'
                                pass 
                                self.match(self.input, 28, self.FOLLOW_28_in_expr91906)

                                if self._state.backtracking == 0:
                                    pass
                                    callmeth = True; node =  ul4c.CallMethKeywords(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], node) 



                                self._state.following.append(self.FOLLOW_callarg_in_expr91917)
                                kwa1 = self.callarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.args.append(kwa1); 



                                # src/ll/UL4.g:390:6: ( ',' kwa2= callarg )*
                                while True: #loop22
                                    alt22 = 2
                                    LA22_0 = self.input.LA(1)

                                    if (LA22_0 == 35) :
                                        LA22_1 = self.input.LA(2)

                                        if (LA22_1 == NAME or LA22_1 == 31) :
                                            alt22 = 1




                                    if alt22 == 1:
                                        # src/ll/UL4.g:391:7: ',' kwa2= callarg
                                        pass 
                                        self.match(self.input, 35, self.FOLLOW_35_in_expr91934)

                                        self._state.following.append(self.FOLLOW_callarg_in_expr91944)
                                        kwa2 = self.callarg()

                                        self._state.following.pop()

                                        if self._state.backtracking == 0:
                                            pass
                                            node.args.append(kwa2); 




                                    else:
                                        break #loop22


                                # src/ll/UL4.g:394:6: ( ',' )?
                                alt23 = 2
                                LA23_0 = self.input.LA(1)

                                if (LA23_0 == 35) :
                                    alt23 = 1
                                if alt23 == 1:
                                    # src/ll/UL4.g:394:6: ','
                                    pass 
                                    self.match(self.input, 35, self.FOLLOW_35_in_expr91961)




                                self.match(self.input, 29, self.FOLLOW_29_in_expr91969)







                        if self._state.backtracking == 0:
                            pass
                                  
                            if not callmeth:
                            	node =  ul4c.GetAttr(self.location, node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0])
                            				




                    elif alt30 == 2:
                        # src/ll/UL4.g:403:4: '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']'
                        pass 
                        self.match(self.input, 50, self.FOLLOW_50_in_expr91997)

                        # src/ll/UL4.g:404:4: ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? )
                        alt29 = 2
                        LA29_0 = self.input.LA(1)

                        if (LA29_0 == 43) :
                            alt29 = 1
                        elif ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or LA29_0 == STRING or (TRUE <= LA29_0 <= UNDEFINED) or LA29_0 == 28 or LA29_0 == 36 or LA29_0 == 50 or LA29_0 == 56 or LA29_0 == 58) :
                            alt29 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 29, 0, self.input)

                            raise nvae


                        if alt29 == 1:
                            # src/ll/UL4.g:405:5: ':' (e2= expr1 )?
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr92008)

                            # src/ll/UL4.g:406:5: (e2= expr1 )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if ((COLOR <= LA26_0 <= DATE) or (FALSE <= LA26_0 <= FLOAT) or (INT <= LA26_0 <= NONE) or LA26_0 == STRING or (TRUE <= LA26_0 <= UNDEFINED) or LA26_0 == 28 or LA26_0 == 36 or LA26_0 == 50 or LA26_0 == 56 or LA26_0 == 58) :
                                alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:407:6: e2= expr1
                                pass 
                                self._state.following.append(self.FOLLOW_expr1_in_expr92023)
                                e2 = self.expr1()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                node =  ul4c.GetSlice(self.location, node, None, index2) 




                        elif alt29 == 2:
                            # src/ll/UL4.g:410:5: e2= expr1 ( ':' (e3= expr1 )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr1_in_expr92047)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:411:5: ( ':' (e3= expr1 )? )?
                            alt28 = 2
                            LA28_0 = self.input.LA(1)

                            if (LA28_0 == 43) :
                                alt28 = 1
                            if alt28 == 1:
                                # src/ll/UL4.g:412:6: ':' (e3= expr1 )?
                                pass 
                                self.match(self.input, 43, self.FOLLOW_43_in_expr92062)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:413:6: (e3= expr1 )?
                                alt27 = 2
                                LA27_0 = self.input.LA(1)

                                if ((COLOR <= LA27_0 <= DATE) or (FALSE <= LA27_0 <= FLOAT) or (INT <= LA27_0 <= NONE) or LA27_0 == STRING or (TRUE <= LA27_0 <= UNDEFINED) or LA27_0 == 28 or LA27_0 == 36 or LA27_0 == 50 or LA27_0 == 56 or LA27_0 == 58) :
                                    alt27 = 1
                                if alt27 == 1:
                                    # src/ll/UL4.g:414:7: e3= expr1
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr1_in_expr92081)
                                    e3 = self.expr1()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                node =  ul4c.GetSlice(self.location, node, index1, index2) if slice else ul4c.GetItem(self.location, node, index1) 






                        self.match(self.input, 51, self.FOLLOW_51_in_expr92110)


                    else:
                        break #loop30





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr9"



    # $ANTLR start "expr8"
    # src/ll/UL4.g:423:1: expr8 returns [node] : ( '-' )* e= expr9 ;
    def expr8(self, ):
        node = None


        e = None


         
        count = 0;
        	
        try:
            try:
                # src/ll/UL4.g:428:2: ( ( '-' )* e= expr9 )
                # src/ll/UL4.g:429:3: ( '-' )* e= expr9
                pass 
                # src/ll/UL4.g:429:3: ( '-' )*
                while True: #loop31
                    alt31 = 2
                    LA31_0 = self.input.LA(1)

                    if (LA31_0 == 36) :
                        alt31 = 1


                    if alt31 == 1:
                        # src/ll/UL4.g:430:4: '-'
                        pass 
                        self.match(self.input, 36, self.FOLLOW_36_in_expr82146)

                        if self._state.backtracking == 0:
                            pass
                            count += 1; 




                    else:
                        break #loop31


                self._state.following.append(self.FOLLOW_expr9_in_expr82159)
                e = self.expr9()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                              
                    node =  e
                    for i in range(count):
                    	node =  ul4c.Neg(self.location, node)
                    		






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr8"



    # $ANTLR start "expr7"
    # src/ll/UL4.g:440:1: expr7 returns [node] : e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* ;
    def expr7(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:441:2: (e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* )
                # src/ll/UL4.g:442:3: e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                pass 
                self._state.following.append(self.FOLLOW_expr8_in_expr72182)
                e1 = self.expr8()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:443:3: ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 26 or LA33_0 == 30 or (39 <= LA33_0 <= 40)) :
                        alt33 = 1


                    if alt33 == 1:
                        # src/ll/UL4.g:444:4: ( '*' | '/' | '//' | '%' ) e2= expr8
                        pass 
                        # src/ll/UL4.g:444:4: ( '*' | '/' | '//' | '%' )
                        alt32 = 4
                        LA32 = self.input.LA(1)
                        if LA32 == 30:
                            alt32 = 1
                        elif LA32 == 39:
                            alt32 = 2
                        elif LA32 == 40:
                            alt32 = 3
                        elif LA32 == 26:
                            alt32 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:445:5: '*'
                            pass 
                            self.match(self.input, 30, self.FOLLOW_30_in_expr72199)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt32 == 2:
                            # src/ll/UL4.g:447:5: '/'
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_expr72212)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt32 == 3:
                            # src/ll/UL4.g:449:5: '//'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr72225)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt32 == 4:
                            # src/ll/UL4.g:451:5: '%'
                            pass 
                            self.match(self.input, 26, self.FOLLOW_26_in_expr72238)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr8_in_expr72252)
                        e2 = self.expr8()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  cls(self.location, node, e2) 




                    else:
                        break #loop33





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr7"



    # $ANTLR start "expr6"
    # src/ll/UL4.g:458:1: expr6 returns [node] : e1= expr7 ( ( '+' | '-' ) e2= expr7 )* ;
    def expr6(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:459:2: (e1= expr7 ( ( '+' | '-' ) e2= expr7 )* )
                # src/ll/UL4.g:460:3: e1= expr7 ( ( '+' | '-' ) e2= expr7 )*
                pass 
                self._state.following.append(self.FOLLOW_expr7_in_expr62280)
                e1 = self.expr7()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:461:3: ( ( '+' | '-' ) e2= expr7 )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 33 or LA35_0 == 36) :
                        alt35 = 1


                    if alt35 == 1:
                        # src/ll/UL4.g:462:4: ( '+' | '-' ) e2= expr7
                        pass 
                        # src/ll/UL4.g:462:4: ( '+' | '-' )
                        alt34 = 2
                        LA34_0 = self.input.LA(1)

                        if (LA34_0 == 33) :
                            alt34 = 1
                        elif (LA34_0 == 36) :
                            alt34 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 34, 0, self.input)

                            raise nvae


                        if alt34 == 1:
                            # src/ll/UL4.g:463:5: '+'
                            pass 
                            self.match(self.input, 33, self.FOLLOW_33_in_expr62297)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt34 == 2:
                            # src/ll/UL4.g:465:5: '-'
                            pass 
                            self.match(self.input, 36, self.FOLLOW_36_in_expr62310)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr7_in_expr62324)
                        e2 = self.expr7()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls(self.location, node, e2) 




                    else:
                        break #loop35





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr6"



    # $ANTLR start "expr5"
    # src/ll/UL4.g:472:1: expr5 returns [node] : e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* ;
    def expr5(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:473:2: (e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* )
                # src/ll/UL4.g:474:3: e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                pass 
                self._state.following.append(self.FOLLOW_expr6_in_expr52352)
                e1 = self.expr6()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:475:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                while True: #loop37
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if (LA37_0 == 25 or (44 <= LA37_0 <= 45) or (47 <= LA37_0 <= 49)) :
                        alt37 = 1


                    if alt37 == 1:
                        # src/ll/UL4.g:476:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6
                        pass 
                        # src/ll/UL4.g:476:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt36 = 6
                        LA36 = self.input.LA(1)
                        if LA36 == 47:
                            alt36 = 1
                        elif LA36 == 25:
                            alt36 = 2
                        elif LA36 == 44:
                            alt36 = 3
                        elif LA36 == 45:
                            alt36 = 4
                        elif LA36 == 48:
                            alt36 = 5
                        elif LA36 == 49:
                            alt36 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 36, 0, self.input)

                            raise nvae


                        if alt36 == 1:
                            # src/ll/UL4.g:477:5: '=='
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr52369)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt36 == 2:
                            # src/ll/UL4.g:479:5: '!='
                            pass 
                            self.match(self.input, 25, self.FOLLOW_25_in_expr52382)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt36 == 3:
                            # src/ll/UL4.g:481:5: '<'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr52395)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt36 == 4:
                            # src/ll/UL4.g:483:5: '<='
                            pass 
                            self.match(self.input, 45, self.FOLLOW_45_in_expr52408)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt36 == 5:
                            # src/ll/UL4.g:485:5: '>'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr52421)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt36 == 6:
                            # src/ll/UL4.g:487:5: '>='
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr52434)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr6_in_expr52448)
                        e2 = self.expr6()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  cls(self.location, node, e2) 




                    else:
                        break #loop37





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr5"



    # $ANTLR start "expr4"
    # src/ll/UL4.g:494:1: expr4 returns [node] : e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? ;
    def expr4(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:495:2: (e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? )
                # src/ll/UL4.g:496:3: e1= expr5 ( ( 'not' )? 'in' e2= expr5 )?
                pass 
                self._state.following.append(self.FOLLOW_expr5_in_expr42476)
                e1 = self.expr5()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:497:3: ( ( 'not' )? 'in' e2= expr5 )?
                alt39 = 2
                LA39_0 = self.input.LA(1)

                if ((55 <= LA39_0 <= 56)) :
                    alt39 = 1
                if alt39 == 1:
                    # src/ll/UL4.g:498:4: ( 'not' )? 'in' e2= expr5
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains; 



                    # src/ll/UL4.g:499:4: ( 'not' )?
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 56) :
                        alt38 = 1
                    if alt38 == 1:
                        # src/ll/UL4.g:500:5: 'not'
                        pass 
                        self.match(self.input, 56, self.FOLLOW_56_in_expr42498)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains; 






                    self.match(self.input, 55, self.FOLLOW_55_in_expr42511)

                    self._state.following.append(self.FOLLOW_expr5_in_expr42518)
                    e2 = self.expr5()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  cls(self.location, node, e2) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr4"



    # $ANTLR start "expr3"
    # src/ll/UL4.g:508:1: expr3 returns [node] : ( 'not' e= expr4 |e= expr4 );
    def expr3(self, ):
        node = None


        e = None


        try:
            try:
                # src/ll/UL4.g:509:2: ( 'not' e= expr4 |e= expr4 )
                alt40 = 2
                LA40_0 = self.input.LA(1)

                if (LA40_0 == 56) :
                    alt40 = 1
                elif ((COLOR <= LA40_0 <= DATE) or (FALSE <= LA40_0 <= FLOAT) or (INT <= LA40_0 <= NONE) or LA40_0 == STRING or (TRUE <= LA40_0 <= UNDEFINED) or LA40_0 == 28 or LA40_0 == 36 or LA40_0 == 50 or LA40_0 == 58) :
                    alt40 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 40, 0, self.input)

                    raise nvae


                if alt40 == 1:
                    # src/ll/UL4.g:510:3: 'not' e= expr4
                    pass 
                    self.match(self.input, 56, self.FOLLOW_56_in_expr32544)

                    self._state.following.append(self.FOLLOW_expr4_in_expr32550)
                    e = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Not(self.location, e) 




                elif alt40 == 2:
                    # src/ll/UL4.g:513:3: e= expr4
                    pass 
                    self._state.following.append(self.FOLLOW_expr4_in_expr32561)
                    e = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr3"



    # $ANTLR start "expr2"
    # src/ll/UL4.g:518:1: expr2 returns [node] : e1= expr3 ( 'and' e2= expr3 )* ;
    def expr2(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:519:2: (e1= expr3 ( 'and' e2= expr3 )* )
                # src/ll/UL4.g:520:3: e1= expr3 ( 'and' e2= expr3 )*
                pass 
                self._state.following.append(self.FOLLOW_expr3_in_expr22585)
                e1 = self.expr3()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:521:3: ( 'and' e2= expr3 )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 52) :
                        alt41 = 1


                    if alt41 == 1:
                        # src/ll/UL4.g:522:4: 'and' e2= expr3
                        pass 
                        self.match(self.input, 52, self.FOLLOW_52_in_expr22596)

                        self._state.following.append(self.FOLLOW_expr3_in_expr22603)
                        e2 = self.expr3()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.And(self.location, node, e2) 




                    else:
                        break #loop41





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr2"



    # $ANTLR start "expr1"
    # src/ll/UL4.g:528:1: expr1 returns [node] : e1= expr2 ( 'or' e2= expr2 )* ;
    def expr1(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:529:2: (e1= expr2 ( 'or' e2= expr2 )* )
                # src/ll/UL4.g:530:3: e1= expr2 ( 'or' e2= expr2 )*
                pass 
                self._state.following.append(self.FOLLOW_expr2_in_expr12631)
                e1 = self.expr2()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:531:3: ( 'or' e2= expr2 )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 57) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:532:4: 'or' e2= expr2
                        pass 
                        self.match(self.input, 57, self.FOLLOW_57_in_expr12642)

                        self._state.following.append(self.FOLLOW_expr2_in_expr12649)
                        e2 = self.expr2()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.Or(self.location, node, e2) 




                    else:
                        break #loop42





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr1"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:537:1: exprarg returns [node] : (ege= generatorexpression |e1= expr1 );
    def exprarg(self, ):
        node = None


        ege = None

        e1 = None


        try:
            try:
                # src/ll/UL4.g:538:2: (ege= generatorexpression |e1= expr1 )
                alt43 = 2
                LA43 = self.input.LA(1)
                if LA43 == 56:
                    LA43_1 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 1, self.input)

                        raise nvae


                elif LA43 == 36:
                    LA43_2 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 2, self.input)

                        raise nvae


                elif LA43 == UNDEFINED:
                    LA43_3 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 3, self.input)

                        raise nvae


                elif LA43 == NONE:
                    LA43_4 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 4, self.input)

                        raise nvae


                elif LA43 == FALSE:
                    LA43_5 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 5, self.input)

                        raise nvae


                elif LA43 == TRUE:
                    LA43_6 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 6, self.input)

                        raise nvae


                elif LA43 == INT:
                    LA43_7 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 7, self.input)

                        raise nvae


                elif LA43 == FLOAT:
                    LA43_8 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 8, self.input)

                        raise nvae


                elif LA43 == STRING:
                    LA43_9 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 9, self.input)

                        raise nvae


                elif LA43 == DATE:
                    LA43_10 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 10, self.input)

                        raise nvae


                elif LA43 == COLOR:
                    LA43_11 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 11, self.input)

                        raise nvae


                elif LA43 == NAME:
                    LA43_12 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 12, self.input)

                        raise nvae


                elif LA43 == 50:
                    LA43_13 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 13, self.input)

                        raise nvae


                elif LA43 == 58:
                    LA43_14 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 14, self.input)

                        raise nvae


                elif LA43 == 28:
                    LA43_15 = self.input.LA(2)

                    if (self.synpred66_UL4()) :
                        alt43 = 1
                    elif (True) :
                        alt43 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 43, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 43, 0, self.input)

                    raise nvae


                if alt43 == 1:
                    # src/ll/UL4.g:538:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2673)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt43 == 2:
                    # src/ll/UL4.g:539:4: e1= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_exprarg2682)
                    e1 = self.expr1()

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
    # src/ll/UL4.g:542:1: expression returns [node] : (ege= generatorexpression EOF |e= expr1 EOF );
    def expression(self, ):
        node = None


        ege = None

        e = None


        try:
            try:
                # src/ll/UL4.g:543:2: (ege= generatorexpression EOF |e= expr1 EOF )
                alt44 = 2
                LA44 = self.input.LA(1)
                if LA44 == 56:
                    LA44_1 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 1, self.input)

                        raise nvae


                elif LA44 == 36:
                    LA44_2 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 2, self.input)

                        raise nvae


                elif LA44 == UNDEFINED:
                    LA44_3 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 3, self.input)

                        raise nvae


                elif LA44 == NONE:
                    LA44_4 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 4, self.input)

                        raise nvae


                elif LA44 == FALSE:
                    LA44_5 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 5, self.input)

                        raise nvae


                elif LA44 == TRUE:
                    LA44_6 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 6, self.input)

                        raise nvae


                elif LA44 == INT:
                    LA44_7 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 7, self.input)

                        raise nvae


                elif LA44 == FLOAT:
                    LA44_8 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 8, self.input)

                        raise nvae


                elif LA44 == STRING:
                    LA44_9 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 9, self.input)

                        raise nvae


                elif LA44 == DATE:
                    LA44_10 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 10, self.input)

                        raise nvae


                elif LA44 == COLOR:
                    LA44_11 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 11, self.input)

                        raise nvae


                elif LA44 == NAME:
                    LA44_12 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 12, self.input)

                        raise nvae


                elif LA44 == 50:
                    LA44_13 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 13, self.input)

                        raise nvae


                elif LA44 == 58:
                    LA44_14 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 14, self.input)

                        raise nvae


                elif LA44 == 28:
                    LA44_15 = self.input.LA(2)

                    if (self.synpred67_UL4()) :
                        alt44 = 1
                    elif (True) :
                        alt44 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 44, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 44, 0, self.input)

                    raise nvae


                if alt44 == 1:
                    # src/ll/UL4.g:543:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression2701)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2703)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt44 == 2:
                    # src/ll/UL4.g:544:4: e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_expression2712)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2714)

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
    # src/ll/UL4.g:550:1: for_ returns [node] : n= nestedname 'in' e= expr1 EOF ;
    def for_(self, ):
        node = None


        n = None

        e = None


        try:
            try:
                # src/ll/UL4.g:551:2: (n= nestedname 'in' e= expr1 EOF )
                # src/ll/UL4.g:552:3: n= nestedname 'in' e= expr1 EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedname_in_for_2739)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_for_2743)

                self._state.following.append(self.FOLLOW_expr1_in_for_2749)
                e = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.For(self.location, n, e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_2755)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:561:1: statement returns [node] : (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF );
    def statement(self, ):
        node = None


        nn = None

        e = None

        n = None


        try:
            try:
                # src/ll/UL4.g:562:2: (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF )
                alt45 = 7
                LA45_0 = self.input.LA(1)

                if (LA45_0 == NAME) :
                    LA45 = self.input.LA(2)
                    if LA45 == 46:
                        alt45 = 1
                    elif LA45 == 34:
                        alt45 = 2
                    elif LA45 == 37:
                        alt45 = 3
                    elif LA45 == 32:
                        alt45 = 4
                    elif LA45 == 42:
                        alt45 = 5
                    elif LA45 == 41:
                        alt45 = 6
                    elif LA45 == 27:
                        alt45 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 1, self.input)

                        raise nvae


                elif (LA45_0 == 28) :
                    alt45 = 1
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 45, 0, self.input)

                    raise nvae


                if alt45 == 1:
                    # src/ll/UL4.g:562:4: nn= nestedname '=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedname_in_statement2776)
                    nn = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement2778)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2782)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2784)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.StoreVar(self.location, nn, e) 




                elif alt45 == 2:
                    # src/ll/UL4.g:563:4: n= name '+=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2793)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_statement2795)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2799)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2801)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.AddVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt45 == 3:
                    # src/ll/UL4.g:564:4: n= name '-=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2810)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_statement2812)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2816)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2818)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.SubVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt45 == 4:
                    # src/ll/UL4.g:565:4: n= name '*=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2827)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 32, self.FOLLOW_32_in_statement2829)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2833)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2835)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.MulVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt45 == 5:
                    # src/ll/UL4.g:566:4: n= name '/=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2844)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 42, self.FOLLOW_42_in_statement2846)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2850)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2852)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.TrueDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt45 == 6:
                    # src/ll/UL4.g:567:4: n= name '//=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2861)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement2863)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2867)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2869)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.FloorDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt45 == 7:
                    # src/ll/UL4.g:568:4: n= name '%=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2878)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 27, self.FOLLOW_27_in_statement2880)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2884)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2886)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.ModVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "statement"

    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_list = None


        # src/ll/UL4.g:301:4: (e_list= list )
        # src/ll/UL4.g:301:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred21_UL41422)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_listcomp = None


        # src/ll/UL4.g:302:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:302:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred22_UL41431)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_dict = None


        # src/ll/UL4.g:303:4: (e_dict= dict )
        # src/ll/UL4.g:303:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred23_UL41440)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred23_UL4"



    # $ANTLR start "synpred24_UL4"
    def synpred24_UL4_fragment(self, ):
        e_dictcomp = None


        # src/ll/UL4.g:304:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:304:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred24_UL41449)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred25_UL4"
    def synpred25_UL4_fragment(self, ):
        e_genexpr = None


        # src/ll/UL4.g:305:4: ( '(' e_genexpr= generatorexpression ')' )
        # src/ll/UL4.g:305:4: '(' e_genexpr= generatorexpression ')'
        pass 
        self.match(self.input, 28, self.FOLLOW_28_in_synpred25_UL41456)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred25_UL41460)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred25_UL41462)



    # $ANTLR end "synpred25_UL4"



    # $ANTLR start "synpred27_UL4"
    def synpred27_UL4_fragment(self, ):
        n0 = None


        # src/ll/UL4.g:314:3: ( '(' n0= nestedname ',' ')' )
        # src/ll/UL4.g:314:3: '(' n0= nestedname ',' ')'
        pass 
        self.match(self.input, 28, self.FOLLOW_28_in_synpred27_UL41507)

        self._state.following.append(self.FOLLOW_nestedname_in_synpred27_UL41511)
        n0 = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 35, self.FOLLOW_35_in_synpred27_UL41513)

        self.match(self.input, 29, self.FOLLOW_29_in_synpred27_UL41515)



    # $ANTLR end "synpred27_UL4"



    # $ANTLR start "synpred66_UL4"
    def synpred66_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:538:4: (ege= generatorexpression )
        # src/ll/UL4.g:538:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred66_UL42673)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred66_UL4"



    # $ANTLR start "synpred67_UL4"
    def synpred67_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:543:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:543:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred67_UL42701)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred67_UL42703)



    # $ANTLR end "synpred67_UL4"




    def synpred22_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred22_UL4_fragment()
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

    def synpred21_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred21_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred24_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred24_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred67_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred67_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred25_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred25_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred23_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred23_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred66_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred66_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success



 

    FOLLOW_UNDEFINED_in_undefined706 = frozenset([1])
    FOLLOW_NONE_in_none723 = frozenset([1])
    FOLLOW_TRUE_in_true_740 = frozenset([1])
    FOLLOW_FALSE_in_false_757 = frozenset([1])
    FOLLOW_INT_in_int_774 = frozenset([1])
    FOLLOW_FLOAT_in_float_791 = frozenset([1])
    FOLLOW_STRING_in_string808 = frozenset([1])
    FOLLOW_DATE_in_date825 = frozenset([1])
    FOLLOW_COLOR_in_color842 = frozenset([1])
    FOLLOW_NAME_in_name859 = frozenset([1])
    FOLLOW_undefined_in_literal878 = frozenset([1])
    FOLLOW_none_in_literal887 = frozenset([1])
    FOLLOW_false__in_literal896 = frozenset([1])
    FOLLOW_true__in_literal905 = frozenset([1])
    FOLLOW_int__in_literal914 = frozenset([1])
    FOLLOW_float__in_literal923 = frozenset([1])
    FOLLOW_string_in_literal932 = frozenset([1])
    FOLLOW_date_in_literal941 = frozenset([1])
    FOLLOW_color_in_literal950 = frozenset([1])
    FOLLOW_name_in_literal959 = frozenset([1])
    FOLLOW_50_in_list980 = frozenset([51])
    FOLLOW_51_in_list984 = frozenset([1])
    FOLLOW_50_in_list993 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_list1001 = frozenset([35, 51])
    FOLLOW_35_in_list1012 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_list1019 = frozenset([35, 51])
    FOLLOW_35_in_list1030 = frozenset([51])
    FOLLOW_51_in_list1035 = frozenset([1])
    FOLLOW_50_in_listcomprehension1059 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1065 = frozenset([53])
    FOLLOW_53_in_listcomprehension1069 = frozenset([14, 28])
    FOLLOW_nestedname_in_listcomprehension1075 = frozenset([55])
    FOLLOW_55_in_listcomprehension1079 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1085 = frozenset([51, 54])
    FOLLOW_54_in_listcomprehension1094 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1101 = frozenset([51])
    FOLLOW_51_in_listcomprehension1112 = frozenset([1])
    FOLLOW_expr1_in_dictitem1137 = frozenset([43])
    FOLLOW_43_in_dictitem1141 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictitem1147 = frozenset([1])
    FOLLOW_31_in_dictitem1156 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictitem1162 = frozenset([1])
    FOLLOW_58_in_dict1181 = frozenset([59])
    FOLLOW_59_in_dict1185 = frozenset([1])
    FOLLOW_58_in_dict1194 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 31, 36, 50, 56, 58])
    FOLLOW_dictitem_in_dict1202 = frozenset([35, 59])
    FOLLOW_35_in_dict1213 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 31, 36, 50, 56, 58])
    FOLLOW_dictitem_in_dict1220 = frozenset([35, 59])
    FOLLOW_35_in_dict1231 = frozenset([59])
    FOLLOW_59_in_dict1236 = frozenset([1])
    FOLLOW_58_in_dictcomprehension1260 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1266 = frozenset([43])
    FOLLOW_43_in_dictcomprehension1270 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1276 = frozenset([53])
    FOLLOW_53_in_dictcomprehension1280 = frozenset([14, 28])
    FOLLOW_nestedname_in_dictcomprehension1286 = frozenset([55])
    FOLLOW_55_in_dictcomprehension1290 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1296 = frozenset([54, 59])
    FOLLOW_54_in_dictcomprehension1305 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1312 = frozenset([59])
    FOLLOW_59_in_dictcomprehension1323 = frozenset([1])
    FOLLOW_expr1_in_generatorexpression1351 = frozenset([53])
    FOLLOW_53_in_generatorexpression1355 = frozenset([14, 28])
    FOLLOW_nestedname_in_generatorexpression1361 = frozenset([55])
    FOLLOW_55_in_generatorexpression1365 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_generatorexpression1371 = frozenset([1, 54])
    FOLLOW_54_in_generatorexpression1380 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_generatorexpression1387 = frozenset([1])
    FOLLOW_literal_in_atom1413 = frozenset([1])
    FOLLOW_list_in_atom1422 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1431 = frozenset([1])
    FOLLOW_dict_in_atom1440 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1449 = frozenset([1])
    FOLLOW_28_in_atom1456 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_generatorexpression_in_atom1460 = frozenset([29])
    FOLLOW_29_in_atom1462 = frozenset([1])
    FOLLOW_28_in_atom1469 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_atom1473 = frozenset([29])
    FOLLOW_29_in_atom1475 = frozenset([1])
    FOLLOW_name_in_nestedname1498 = frozenset([1])
    FOLLOW_28_in_nestedname1507 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1511 = frozenset([35])
    FOLLOW_35_in_nestedname1513 = frozenset([29])
    FOLLOW_29_in_nestedname1515 = frozenset([1])
    FOLLOW_28_in_nestedname1524 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1530 = frozenset([35])
    FOLLOW_35_in_nestedname1534 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1540 = frozenset([29, 35])
    FOLLOW_35_in_nestedname1551 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1558 = frozenset([29, 35])
    FOLLOW_35_in_nestedname1569 = frozenset([29])
    FOLLOW_29_in_nestedname1574 = frozenset([1])
    FOLLOW_atom_in_expr101594 = frozenset([1])
    FOLLOW_name_in_expr101603 = frozenset([28])
    FOLLOW_28_in_expr101605 = frozenset([29])
    FOLLOW_29_in_expr101607 = frozenset([1])
    FOLLOW_name_in_expr101618 = frozenset([28])
    FOLLOW_28_in_expr101624 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr101630 = frozenset([29, 35])
    FOLLOW_35_in_expr101641 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr101648 = frozenset([29, 35])
    FOLLOW_35_in_expr101659 = frozenset([29])
    FOLLOW_29_in_expr101664 = frozenset([1])
    FOLLOW_name_in_callarg1687 = frozenset([46])
    FOLLOW_46_in_callarg1691 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_callarg1697 = frozenset([1])
    FOLLOW_31_in_callarg1706 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_callarg1712 = frozenset([1])
    FOLLOW_expr10_in_expr91740 = frozenset([1, 38, 50])
    FOLLOW_38_in_expr91756 = frozenset([14])
    FOLLOW_name_in_expr91763 = frozenset([1, 28, 38, 50])
    FOLLOW_28_in_expr91794 = frozenset([29])
    FOLLOW_29_in_expr91801 = frozenset([1, 38, 50])
    FOLLOW_28_in_expr91823 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91834 = frozenset([29, 35])
    FOLLOW_35_in_expr91851 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91861 = frozenset([29, 35])
    FOLLOW_35_in_expr91878 = frozenset([29])
    FOLLOW_29_in_expr91886 = frozenset([1, 38, 50])
    FOLLOW_28_in_expr91906 = frozenset([14, 31])
    FOLLOW_callarg_in_expr91917 = frozenset([29, 35])
    FOLLOW_35_in_expr91934 = frozenset([14, 31])
    FOLLOW_callarg_in_expr91944 = frozenset([29, 35])
    FOLLOW_35_in_expr91961 = frozenset([29])
    FOLLOW_29_in_expr91969 = frozenset([1, 38, 50])
    FOLLOW_50_in_expr91997 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 43, 50, 56, 58])
    FOLLOW_43_in_expr92008 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 51, 56, 58])
    FOLLOW_expr1_in_expr92023 = frozenset([51])
    FOLLOW_expr1_in_expr92047 = frozenset([43, 51])
    FOLLOW_43_in_expr92062 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 51, 56, 58])
    FOLLOW_expr1_in_expr92081 = frozenset([51])
    FOLLOW_51_in_expr92110 = frozenset([1, 38, 50])
    FOLLOW_36_in_expr82146 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr9_in_expr82159 = frozenset([1])
    FOLLOW_expr8_in_expr72182 = frozenset([1, 26, 30, 39, 40])
    FOLLOW_30_in_expr72199 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_39_in_expr72212 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_40_in_expr72225 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_26_in_expr72238 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr8_in_expr72252 = frozenset([1, 26, 30, 39, 40])
    FOLLOW_expr7_in_expr62280 = frozenset([1, 33, 36])
    FOLLOW_33_in_expr62297 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_36_in_expr62310 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr7_in_expr62324 = frozenset([1, 33, 36])
    FOLLOW_expr6_in_expr52352 = frozenset([1, 25, 44, 45, 47, 48, 49])
    FOLLOW_47_in_expr52369 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_25_in_expr52382 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_44_in_expr52395 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_45_in_expr52408 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_48_in_expr52421 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_49_in_expr52434 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr6_in_expr52448 = frozenset([1, 25, 44, 45, 47, 48, 49])
    FOLLOW_expr5_in_expr42476 = frozenset([1, 55, 56])
    FOLLOW_56_in_expr42498 = frozenset([55])
    FOLLOW_55_in_expr42511 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr5_in_expr42518 = frozenset([1])
    FOLLOW_56_in_expr32544 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 58])
    FOLLOW_expr4_in_expr32550 = frozenset([1])
    FOLLOW_expr4_in_expr32561 = frozenset([1])
    FOLLOW_expr3_in_expr22585 = frozenset([1, 52])
    FOLLOW_52_in_expr22596 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr3_in_expr22603 = frozenset([1, 52])
    FOLLOW_expr2_in_expr12631 = frozenset([1, 57])
    FOLLOW_57_in_expr12642 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr2_in_expr12649 = frozenset([1, 57])
    FOLLOW_generatorexpression_in_exprarg2673 = frozenset([1])
    FOLLOW_expr1_in_exprarg2682 = frozenset([1])
    FOLLOW_generatorexpression_in_expression2701 = frozenset([])
    FOLLOW_EOF_in_expression2703 = frozenset([1])
    FOLLOW_expr1_in_expression2712 = frozenset([])
    FOLLOW_EOF_in_expression2714 = frozenset([1])
    FOLLOW_nestedname_in_for_2739 = frozenset([55])
    FOLLOW_55_in_for_2743 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_for_2749 = frozenset([])
    FOLLOW_EOF_in_for_2755 = frozenset([1])
    FOLLOW_nestedname_in_statement2776 = frozenset([46])
    FOLLOW_46_in_statement2778 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2782 = frozenset([])
    FOLLOW_EOF_in_statement2784 = frozenset([1])
    FOLLOW_name_in_statement2793 = frozenset([34])
    FOLLOW_34_in_statement2795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2799 = frozenset([])
    FOLLOW_EOF_in_statement2801 = frozenset([1])
    FOLLOW_name_in_statement2810 = frozenset([37])
    FOLLOW_37_in_statement2812 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2816 = frozenset([])
    FOLLOW_EOF_in_statement2818 = frozenset([1])
    FOLLOW_name_in_statement2827 = frozenset([32])
    FOLLOW_32_in_statement2829 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2833 = frozenset([])
    FOLLOW_EOF_in_statement2835 = frozenset([1])
    FOLLOW_name_in_statement2844 = frozenset([42])
    FOLLOW_42_in_statement2846 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2850 = frozenset([])
    FOLLOW_EOF_in_statement2852 = frozenset([1])
    FOLLOW_name_in_statement2861 = frozenset([41])
    FOLLOW_41_in_statement2863 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2867 = frozenset([])
    FOLLOW_EOF_in_statement2869 = frozenset([1])
    FOLLOW_name_in_statement2878 = frozenset([27])
    FOLLOW_27_in_statement2880 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2884 = frozenset([])
    FOLLOW_EOF_in_statement2886 = frozenset([1])
    FOLLOW_list_in_synpred21_UL41422 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred22_UL41431 = frozenset([1])
    FOLLOW_dict_in_synpred23_UL41440 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred24_UL41449 = frozenset([1])
    FOLLOW_28_in_synpred25_UL41456 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 20, 28, 36, 50, 56, 58])
    FOLLOW_generatorexpression_in_synpred25_UL41460 = frozenset([29])
    FOLLOW_29_in_synpred25_UL41462 = frozenset([1])
    FOLLOW_28_in_synpred27_UL41507 = frozenset([14, 28])
    FOLLOW_nestedname_in_synpred27_UL41511 = frozenset([35])
    FOLLOW_35_in_synpred27_UL41513 = frozenset([29])
    FOLLOW_29_in_synpred27_UL41515 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred66_UL42673 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred67_UL42701 = frozenset([])
    FOLLOW_EOF_in_synpred67_UL42703 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
