# $ANTLR 3.4 src/ll/UL4.g 2013-02-09 21:15:36

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


import datetime, ast
from ll import ul4c, color



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
EOF=-1
T__24=24
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
UNICODE1_ESC=20
UNICODE2_ESC=21
UNICODE4_ESC=22
WS=23

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "BIN_DIGIT", "COLOR", "DATE", "DIGIT", "ESC_SEQ", "EXPONENT", "FALSE", 
    "FLOAT", "HEX_DIGIT", "INT", "NAME", "NONE", "OCT_DIGIT", "STRING", 
    "TIME", "TRUE", "UNICODE1_ESC", "UNICODE2_ESC", "UNICODE4_ESC", "WS", 
    "'!='", "'%'", "'%='", "'('", "')'", "'*'", "'**'", "'*='", "'+'", "'+='", 
    "','", "'-'", "'-='", "'.'", "'/'", "'//'", "'//='", "'/='", "':'", 
    "'<'", "'<='", "'='", "'=='", "'>'", "'>='", "'['", "']'", "'and'", 
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



    # $ANTLR start "none"
    # src/ll/UL4.g:142:1: none returns [node] : NONE ;
    def none(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:143:2: ( NONE )
                # src/ll/UL4.g:143:4: NONE
                pass 
                self.match(self.input, NONE, self.FOLLOW_NONE_in_none695)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(None) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "none"



    # $ANTLR start "true_"
    # src/ll/UL4.g:146:1: true_ returns [node] : TRUE ;
    def true_(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:147:2: ( TRUE )
                # src/ll/UL4.g:147:4: TRUE
                pass 
                self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_712)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(True) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "true_"



    # $ANTLR start "false_"
    # src/ll/UL4.g:150:1: false_ returns [node] : FALSE ;
    def false_(self, ):
        node = None


        try:
            try:
                # src/ll/UL4.g:151:2: ( FALSE )
                # src/ll/UL4.g:151:4: FALSE
                pass 
                self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_729)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(False) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "false_"



    # $ANTLR start "int_"
    # src/ll/UL4.g:154:1: int_ returns [node] : INT ;
    def int_(self, ):
        node = None


        INT1 = None

        try:
            try:
                # src/ll/UL4.g:155:2: ( INT )
                # src/ll/UL4.g:155:4: INT
                pass 
                INT1 = self.match(self.input, INT, self.FOLLOW_INT_in_int_746)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(int(INT1.text, 0)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "int_"



    # $ANTLR start "float_"
    # src/ll/UL4.g:158:1: float_ returns [node] : FLOAT ;
    def float_(self, ):
        node = None


        FLOAT2 = None

        try:
            try:
                # src/ll/UL4.g:159:2: ( FLOAT )
                # src/ll/UL4.g:159:4: FLOAT
                pass 
                FLOAT2 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_763)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(float(FLOAT2.text)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "float_"



    # $ANTLR start "string"
    # src/ll/UL4.g:162:1: string returns [node] : STRING ;
    def string(self, ):
        node = None


        STRING3 = None

        try:
            try:
                # src/ll/UL4.g:163:2: ( STRING )
                # src/ll/UL4.g:163:4: STRING
                pass 
                STRING3 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string780)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(ast.literal_eval(STRING3.text)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "string"



    # $ANTLR start "date"
    # src/ll/UL4.g:166:1: date returns [node] : DATE ;
    def date(self, ):
        node = None


        DATE4 = None

        try:
            try:
                # src/ll/UL4.g:167:2: ( DATE )
                # src/ll/UL4.g:167:4: DATE
                pass 
                DATE4 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date797)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(datetime.datetime(*map(int, [f for f in ul4c.datesplitter.split(DATE4.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "date"



    # $ANTLR start "color"
    # src/ll/UL4.g:170:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR5 = None

        try:
            try:
                # src/ll/UL4.g:171:2: ( COLOR )
                # src/ll/UL4.g:171:4: COLOR
                pass 
                COLOR5 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color814)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(color.Color.fromrepr(COLOR5.text)) 






                       
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
    # src/ll/UL4.g:174:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME6 = None

        try:
            try:
                # src/ll/UL4.g:175:2: ( NAME )
                # src/ll/UL4.g:175:4: NAME
                pass 
                NAME6 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name831)

                if self._state.backtracking == 0:
                    pass
                    retval.node = ul4c.Var(NAME6.text) 





                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "name"



    # $ANTLR start "literal"
    # src/ll/UL4.g:178:1: literal returns [node] : (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name );
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
                # src/ll/UL4.g:179:2: (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name )
                alt1 = 9
                LA1 = self.input.LA(1)
                if LA1 == NONE:
                    alt1 = 1
                elif LA1 == FALSE:
                    alt1 = 2
                elif LA1 == TRUE:
                    alt1 = 3
                elif LA1 == INT:
                    alt1 = 4
                elif LA1 == FLOAT:
                    alt1 = 5
                elif LA1 == STRING:
                    alt1 = 6
                elif LA1 == DATE:
                    alt1 = 7
                elif LA1 == COLOR:
                    alt1 = 8
                elif LA1 == NAME:
                    alt1 = 9
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae


                if alt1 == 1:
                    # src/ll/UL4.g:179:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal850)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt1 == 2:
                    # src/ll/UL4.g:180:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal859)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt1 == 3:
                    # src/ll/UL4.g:181:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal868)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt1 == 4:
                    # src/ll/UL4.g:182:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal877)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt1 == 5:
                    # src/ll/UL4.g:183:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal886)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt1 == 6:
                    # src/ll/UL4.g:184:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal895)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt1 == 7:
                    # src/ll/UL4.g:185:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal904)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt1 == 8:
                    # src/ll/UL4.g:186:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal913)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt1 == 9:
                    # src/ll/UL4.g:187:4: e_name= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_literal922)
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
    # src/ll/UL4.g:191:1: list returns [node] : ( '[' ']' | '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']' );
    def list(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:192:2: ( '[' ']' | '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']' )
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == 49) :
                    LA4_1 = self.input.LA(2)

                    if (LA4_1 == 50) :
                        alt4 = 1
                    elif ((COLOR <= LA4_1 <= DATE) or (FALSE <= LA4_1 <= FLOAT) or (INT <= LA4_1 <= NONE) or LA4_1 == STRING or LA4_1 == TRUE or LA4_1 == 27 or LA4_1 == 35 or LA4_1 == 49 or LA4_1 == 55 or LA4_1 == 57) :
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
                    # src/ll/UL4.g:193:3: '[' ']'
                    pass 
                    self.match(self.input, 49, self.FOLLOW_49_in_list943)

                    self.match(self.input, 50, self.FOLLOW_50_in_list947)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List() 




                elif alt4 == 2:
                    # src/ll/UL4.g:196:3: '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']'
                    pass 
                    self.match(self.input, 49, self.FOLLOW_49_in_list956)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List() 



                    self._state.following.append(self.FOLLOW_expr1_in_list964)
                    e1 = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1) 



                    # src/ll/UL4.g:198:3: ( ',' e2= expr1 )*
                    while True: #loop2
                        alt2 = 2
                        LA2_0 = self.input.LA(1)

                        if (LA2_0 == 34) :
                            LA2_1 = self.input.LA(2)

                            if ((COLOR <= LA2_1 <= DATE) or (FALSE <= LA2_1 <= FLOAT) or (INT <= LA2_1 <= NONE) or LA2_1 == STRING or LA2_1 == TRUE or LA2_1 == 27 or LA2_1 == 35 or LA2_1 == 49 or LA2_1 == 55 or LA2_1 == 57) :
                                alt2 = 1




                        if alt2 == 1:
                            # src/ll/UL4.g:199:4: ',' e2= expr1
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_list975)

                            self._state.following.append(self.FOLLOW_expr1_in_list982)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2) 




                        else:
                            break #loop2


                    # src/ll/UL4.g:202:3: ( ',' )?
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == 34) :
                        alt3 = 1
                    if alt3 == 1:
                        # src/ll/UL4.g:202:3: ','
                        pass 
                        self.match(self.input, 34, self.FOLLOW_34_in_list993)




                    self.match(self.input, 50, self.FOLLOW_50_in_list998)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "list"



    # $ANTLR start "listcomprehension"
    # src/ll/UL4.g:206:1: listcomprehension returns [node] : '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']' ;
    def listcomprehension(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:211:2: ( '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']' )
                # src/ll/UL4.g:212:3: '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ']'
                pass 
                self.match(self.input, 49, self.FOLLOW_49_in_listcomprehension1022)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1028)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 52, self.FOLLOW_52_in_listcomprehension1032)

                self._state.following.append(self.FOLLOW_nestedname_in_listcomprehension1038)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_listcomprehension1042)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1048)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:218:3: ( 'if' condition= expr1 )?
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 53) :
                    alt5 = 1
                if alt5 == 1:
                    # src/ll/UL4.g:219:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 53, self.FOLLOW_53_in_listcomprehension1057)

                    self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1064)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                self.match(self.input, 50, self.FOLLOW_50_in_listcomprehension1075)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ListComp(item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:227:1: fragment dictitem returns [node] : k= expr1 ':' v= expr1 ;
    def dictitem(self, ):
        node = None


        k = None

        v = None


        try:
            try:
                # src/ll/UL4.g:228:2: (k= expr1 ':' v= expr1 )
                # src/ll/UL4.g:229:3: k= expr1 ':' v= expr1
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_dictitem1100)
                k = self.expr1()

                self._state.following.pop()

                self.match(self.input, 42, self.FOLLOW_42_in_dictitem1104)

                self._state.following.append(self.FOLLOW_expr1_in_dictitem1110)
                v = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = (k, v) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictitem"



    # $ANTLR start "dict"
    # src/ll/UL4.g:234:1: dict returns [node] : ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' );
    def dict(self, ):
        node = None


        i1 = None

        i2 = None


        try:
            try:
                # src/ll/UL4.g:235:2: ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 57) :
                    LA8_1 = self.input.LA(2)

                    if (LA8_1 == 58) :
                        alt8 = 1
                    elif ((COLOR <= LA8_1 <= DATE) or (FALSE <= LA8_1 <= FLOAT) or (INT <= LA8_1 <= NONE) or LA8_1 == STRING or LA8_1 == TRUE or LA8_1 == 27 or LA8_1 == 35 or LA8_1 == 49 or LA8_1 == 55 or LA8_1 == 57) :
                        alt8 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 8, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae


                if alt8 == 1:
                    # src/ll/UL4.g:236:3: '{' '}'
                    pass 
                    self.match(self.input, 57, self.FOLLOW_57_in_dict1129)

                    self.match(self.input, 58, self.FOLLOW_58_in_dict1133)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict() 




                elif alt8 == 2:
                    # src/ll/UL4.g:239:3: '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}'
                    pass 
                    self.match(self.input, 57, self.FOLLOW_57_in_dict1142)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict() 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1150)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:241:3: ( ',' i2= dictitem )*
                    while True: #loop6
                        alt6 = 2
                        LA6_0 = self.input.LA(1)

                        if (LA6_0 == 34) :
                            LA6_1 = self.input.LA(2)

                            if ((COLOR <= LA6_1 <= DATE) or (FALSE <= LA6_1 <= FLOAT) or (INT <= LA6_1 <= NONE) or LA6_1 == STRING or LA6_1 == TRUE or LA6_1 == 27 or LA6_1 == 35 or LA6_1 == 49 or LA6_1 == 55 or LA6_1 == 57) :
                                alt6 = 1




                        if alt6 == 1:
                            # src/ll/UL4.g:242:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_dict1161)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1168)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop6


                    # src/ll/UL4.g:245:3: ( ',' )?
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == 34) :
                        alt7 = 1
                    if alt7 == 1:
                        # src/ll/UL4.g:245:3: ','
                        pass 
                        self.match(self.input, 34, self.FOLLOW_34_in_dict1179)




                    self.match(self.input, 58, self.FOLLOW_58_in_dict1184)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:249:1: dictcomprehension returns [node] : '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' ;
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
                # src/ll/UL4.g:254:2: ( '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' )
                # src/ll/UL4.g:255:3: '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}'
                pass 
                self.match(self.input, 57, self.FOLLOW_57_in_dictcomprehension1208)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1214)
                key = self.expr1()

                self._state.following.pop()

                self.match(self.input, 42, self.FOLLOW_42_in_dictcomprehension1218)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1224)
                value = self.expr1()

                self._state.following.pop()

                self.match(self.input, 52, self.FOLLOW_52_in_dictcomprehension1228)

                self._state.following.append(self.FOLLOW_nestedname_in_dictcomprehension1234)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_dictcomprehension1238)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1244)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:263:3: ( 'if' condition= expr1 )?
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 53) :
                    alt9 = 1
                if alt9 == 1:
                    # src/ll/UL4.g:264:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 53, self.FOLLOW_53_in_dictcomprehension1253)

                    self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1260)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                self.match(self.input, 58, self.FOLLOW_58_in_dictcomprehension1271)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.DictComp(key, value, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:270:1: generatorexpression returns [node] : item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ;
    def generatorexpression(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:275:2: (item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? )
                # src/ll/UL4.g:276:3: item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )?
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1299)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 52, self.FOLLOW_52_in_generatorexpression1303)

                self._state.following.append(self.FOLLOW_nestedname_in_generatorexpression1309)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_generatorexpression1313)

                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1319)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:281:3: ( 'if' condition= expr1 )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 53) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:282:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 53, self.FOLLOW_53_in_generatorexpression1328)

                    self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1335)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.GenExpr(item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:287:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' );
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
                # src/ll/UL4.g:288:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' )
                alt11 = 7
                LA11 = self.input.LA(1)
                if LA11 == COLOR or LA11 == DATE or LA11 == FALSE or LA11 == FLOAT or LA11 == INT or LA11 == NAME or LA11 == NONE or LA11 == STRING or LA11 == TRUE:
                    alt11 = 1
                elif LA11 == 49:
                    LA11_10 = self.input.LA(2)

                    if (self.synpred19_UL4()) :
                        alt11 = 2
                    elif (self.synpred20_UL4()) :
                        alt11 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 11, 10, self.input)

                        raise nvae


                elif LA11 == 57:
                    LA11_11 = self.input.LA(2)

                    if (self.synpred21_UL4()) :
                        alt11 = 4
                    elif (self.synpred22_UL4()) :
                        alt11 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 11, 11, self.input)

                        raise nvae


                elif LA11 == 27:
                    LA11_12 = self.input.LA(2)

                    if (self.synpred23_UL4()) :
                        alt11 = 6
                    elif (True) :
                        alt11 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 11, 12, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 11, 0, self.input)

                    raise nvae


                if alt11 == 1:
                    # src/ll/UL4.g:288:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1361)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt11 == 2:
                    # src/ll/UL4.g:289:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1370)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt11 == 3:
                    # src/ll/UL4.g:290:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1379)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt11 == 4:
                    # src/ll/UL4.g:291:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1388)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt11 == 5:
                    # src/ll/UL4.g:292:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1397)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt11 == 6:
                    # src/ll/UL4.g:293:4: '(' e_genexpr= generatorexpression ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_atom1404)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1408)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, 28, self.FOLLOW_28_in_atom1410)

                    if self._state.backtracking == 0:
                        pass
                        node =  e_genexpr 




                elif alt11 == 7:
                    # src/ll/UL4.g:294:4: '(' e_bracket= expr1 ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_atom1417)

                    self._state.following.append(self.FOLLOW_expr1_in_atom1421)
                    e_bracket = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, 28, self.FOLLOW_28_in_atom1423)

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
    # src/ll/UL4.g:298:1: nestedname returns [varname] : (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' );
    def nestedname(self, ):
        varname = None


        n = None

        n0 = None

        n1 = None

        n2 = None

        n3 = None


        try:
            try:
                # src/ll/UL4.g:299:2: (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' )
                alt14 = 3
                LA14_0 = self.input.LA(1)

                if (LA14_0 == NAME) :
                    alt14 = 1
                elif (LA14_0 == 27) :
                    LA14_2 = self.input.LA(2)

                    if (self.synpred25_UL4()) :
                        alt14 = 2
                    elif (True) :
                        alt14 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 14, 2, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 14, 0, self.input)

                    raise nvae


                if alt14 == 1:
                    # src/ll/UL4.g:300:3: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_nestedname1446)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname =  ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0] 




                elif alt14 == 2:
                    # src/ll/UL4.g:302:3: '(' n0= nestedname ',' ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_nestedname1455)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1459)
                    n0 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_nestedname1461)

                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1463)

                    if self._state.backtracking == 0:
                        pass
                        varname = (n0,) 




                elif alt14 == 3:
                    # src/ll/UL4.g:304:3: '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_nestedname1472)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1478)
                    n1 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_nestedname1482)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1488)
                    n2 = self.nestedname()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname = (n1, n2) 



                    # src/ll/UL4.g:308:3: ( ',' n3= nestedname )*
                    while True: #loop12
                        alt12 = 2
                        LA12_0 = self.input.LA(1)

                        if (LA12_0 == 34) :
                            LA12_1 = self.input.LA(2)

                            if (LA12_1 == NAME or LA12_1 == 27) :
                                alt12 = 1




                        if alt12 == 1:
                            # src/ll/UL4.g:309:4: ',' n3= nestedname
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_nestedname1499)

                            self._state.following.append(self.FOLLOW_nestedname_in_nestedname1506)
                            n3 = self.nestedname()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                varname += (n3,) 




                        else:
                            break #loop12


                    # src/ll/UL4.g:312:3: ( ',' )?
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == 34) :
                        alt13 = 1
                    if alt13 == 1:
                        # src/ll/UL4.g:312:3: ','
                        pass 
                        self.match(self.input, 34, self.FOLLOW_34_in_nestedname1517)




                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1522)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return varname

    # $ANTLR end "nestedname"



    # $ANTLR start "expr9"
    # src/ll/UL4.g:317:1: expr9 returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* ;
    def expr9(self, ):
        node = None


        e1 = None

        n = None

        rkwargs = None

        rargs = None

        a1 = None

        a2 = None

        an3 = None

        av3 = None

        an1 = None

        av1 = None

        an2 = None

        av2 = None

        e2 = None

        e3 = None


         
        callmeth = False
        index1 = None
        index2 = None
        slice = False
        	
        try:
            try:
                # src/ll/UL4.g:325:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* )
                # src/ll/UL4.g:326:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr91551)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:327:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                while True: #loop32
                    alt32 = 4
                    LA32 = self.input.LA(1)
                    if LA32 == 37:
                        alt32 = 1
                    elif LA32 == 27:
                        alt32 = 2
                    elif LA32 == 49:
                        alt32 = 3

                    if alt32 == 1:
                        # src/ll/UL4.g:329:4: '.' n= name
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_expr91567)

                        self._state.following.append(self.FOLLOW_name_in_expr91574)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.GetAttr(node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt32 == 2:
                        # src/ll/UL4.g:333:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')'
                        pass 
                        self.match(self.input, 27, self.FOLLOW_27_in_expr91590)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.CallMeth(node.obj, node.attrname) if isinstance(node, ul4c.GetAttr) else ul4c.CallFunc(node) 



                        # src/ll/UL4.g:334:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt27 = 5
                        LA27 = self.input.LA(1)
                        if LA27 == 28:
                            alt27 = 1
                        elif LA27 == 30:
                            alt27 = 2
                        elif LA27 == 29:
                            alt27 = 3
                        elif LA27 == COLOR or LA27 == DATE or LA27 == FALSE or LA27 == FLOAT or LA27 == INT or LA27 == NONE or LA27 == STRING or LA27 == TRUE or LA27 == 27 or LA27 == 35 or LA27 == 49 or LA27 == 55 or LA27 == 57:
                            alt27 = 4
                        elif LA27 == NAME:
                            LA27_5 = self.input.LA(2)

                            if ((24 <= LA27_5 <= 25) or (27 <= LA27_5 <= 29) or LA27_5 == 32 or (34 <= LA27_5 <= 35) or (37 <= LA27_5 <= 39) or (43 <= LA27_5 <= 44) or (46 <= LA27_5 <= 49) or (51 <= LA27_5 <= 52) or (54 <= LA27_5 <= 56)) :
                                alt27 = 4
                            elif (LA27_5 == 45) :
                                alt27 = 5
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 27, 5, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 27, 0, self.input)

                            raise nvae


                        if alt27 == 1:
                            # src/ll/UL4.g:336:4: 
                            pass 

                        elif alt27 == 2:
                            # src/ll/UL4.g:338:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 30, self.FOLLOW_30_in_expr91620)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91624)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:339:5: ( ',' )?
                            alt15 = 2
                            LA15_0 = self.input.LA(1)

                            if (LA15_0 == 34) :
                                alt15 = 1
                            if alt15 == 1:
                                # src/ll/UL4.g:339:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91632)





                        elif alt27 == 3:
                            # src/ll/UL4.g:342:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 29, self.FOLLOW_29_in_expr91650)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91654)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remargs = rargs; 



                            # src/ll/UL4.g:343:5: ( ',' '**' rkwargs= exprarg )?
                            alt16 = 2
                            LA16_0 = self.input.LA(1)

                            if (LA16_0 == 34) :
                                LA16_1 = self.input.LA(2)

                                if (LA16_1 == 30) :
                                    alt16 = 1
                            if alt16 == 1:
                                # src/ll/UL4.g:344:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91669)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91676)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91680)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:347:5: ( ',' )?
                            alt17 = 2
                            LA17_0 = self.input.LA(1)

                            if (LA17_0 == 34) :
                                alt17 = 1
                            if alt17 == 1:
                                # src/ll/UL4.g:347:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91695)





                        elif alt27 == 4:
                            # src/ll/UL4.g:350:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr91715)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.args.append(a1) 



                            # src/ll/UL4.g:351:5: ( ',' a2= exprarg )*
                            while True: #loop18
                                alt18 = 2
                                LA18_0 = self.input.LA(1)

                                if (LA18_0 == 34) :
                                    LA18_1 = self.input.LA(2)

                                    if (LA18_1 == NAME) :
                                        LA18_3 = self.input.LA(3)

                                        if ((24 <= LA18_3 <= 25) or (27 <= LA18_3 <= 29) or LA18_3 == 32 or (34 <= LA18_3 <= 35) or (37 <= LA18_3 <= 39) or (43 <= LA18_3 <= 44) or (46 <= LA18_3 <= 49) or (51 <= LA18_3 <= 52) or (54 <= LA18_3 <= 56)) :
                                            alt18 = 1


                                    elif ((COLOR <= LA18_1 <= DATE) or (FALSE <= LA18_1 <= FLOAT) or LA18_1 == INT or LA18_1 == NONE or LA18_1 == STRING or LA18_1 == TRUE or LA18_1 == 27 or LA18_1 == 35 or LA18_1 == 49 or LA18_1 == 55 or LA18_1 == 57) :
                                        alt18 = 1




                                if alt18 == 1:
                                    # src/ll/UL4.g:352:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91730)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91739)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.args.append(a2) 




                                else:
                                    break #loop18


                            # src/ll/UL4.g:355:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop19
                                alt19 = 2
                                LA19_0 = self.input.LA(1)

                                if (LA19_0 == 34) :
                                    LA19_1 = self.input.LA(2)

                                    if (LA19_1 == NAME) :
                                        alt19 = 1




                                if alt19 == 1:
                                    # src/ll/UL4.g:356:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91761)

                                    self._state.following.append(self.FOLLOW_name_in_expr91770)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 45, self.FOLLOW_45_in_expr91772)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91776)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop19


                            # src/ll/UL4.g:359:5: ( ',' '*' rargs= exprarg )?
                            alt20 = 2
                            LA20_0 = self.input.LA(1)

                            if (LA20_0 == 34) :
                                LA20_1 = self.input.LA(2)

                                if (LA20_1 == 29) :
                                    alt20 = 1
                            if alt20 == 1:
                                # src/ll/UL4.g:360:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91798)

                                self.match(self.input, 29, self.FOLLOW_29_in_expr91805)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91809)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:363:5: ( ',' '**' rkwargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 34) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 30) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:364:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91831)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91838)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91842)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:367:5: ( ',' )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 34) :
                                alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:367:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91857)





                        elif alt27 == 5:
                            # src/ll/UL4.g:370:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr91877)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 45, self.FOLLOW_45_in_expr91879)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91883)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:371:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop23
                                alt23 = 2
                                LA23_0 = self.input.LA(1)

                                if (LA23_0 == 34) :
                                    LA23_1 = self.input.LA(2)

                                    if (LA23_1 == NAME) :
                                        alt23 = 1




                                if alt23 == 1:
                                    # src/ll/UL4.g:372:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91898)

                                    self._state.following.append(self.FOLLOW_name_in_expr91907)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 45, self.FOLLOW_45_in_expr91909)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91913)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop23


                            # src/ll/UL4.g:375:5: ( ',' '*' rargs= exprarg )?
                            alt24 = 2
                            LA24_0 = self.input.LA(1)

                            if (LA24_0 == 34) :
                                LA24_1 = self.input.LA(2)

                                if (LA24_1 == 29) :
                                    alt24 = 1
                            if alt24 == 1:
                                # src/ll/UL4.g:376:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91935)

                                self.match(self.input, 29, self.FOLLOW_29_in_expr91942)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91946)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:379:5: ( ',' '**' rkwargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 34) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 30) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:380:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91968)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91975)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91979)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:383:5: ( ',' )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 34) :
                                alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:383:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91994)







                        self.match(self.input, 28, self.FOLLOW_28_in_expr92005)


                    elif alt32 == 3:
                        # src/ll/UL4.g:388:4: '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']'
                        pass 
                        self.match(self.input, 49, self.FOLLOW_49_in_expr92019)

                        # src/ll/UL4.g:389:4: ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? )
                        alt31 = 2
                        LA31_0 = self.input.LA(1)

                        if (LA31_0 == 42) :
                            alt31 = 1
                        elif ((COLOR <= LA31_0 <= DATE) or (FALSE <= LA31_0 <= FLOAT) or (INT <= LA31_0 <= NONE) or LA31_0 == STRING or LA31_0 == TRUE or LA31_0 == 27 or LA31_0 == 35 or LA31_0 == 49 or LA31_0 == 55 or LA31_0 == 57) :
                            alt31 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 31, 0, self.input)

                            raise nvae


                        if alt31 == 1:
                            # src/ll/UL4.g:390:5: ':' (e2= expr1 )?
                            pass 
                            self.match(self.input, 42, self.FOLLOW_42_in_expr92030)

                            # src/ll/UL4.g:391:5: (e2= expr1 )?
                            alt28 = 2
                            LA28_0 = self.input.LA(1)

                            if ((COLOR <= LA28_0 <= DATE) or (FALSE <= LA28_0 <= FLOAT) or (INT <= LA28_0 <= NONE) or LA28_0 == STRING or LA28_0 == TRUE or LA28_0 == 27 or LA28_0 == 35 or LA28_0 == 49 or LA28_0 == 55 or LA28_0 == 57) :
                                alt28 = 1
                            if alt28 == 1:
                                # src/ll/UL4.g:392:6: e2= expr1
                                pass 
                                self._state.following.append(self.FOLLOW_expr1_in_expr92045)
                                e2 = self.expr1()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(node, None, index2) 




                        elif alt31 == 2:
                            # src/ll/UL4.g:395:5: e2= expr1 ( ':' (e3= expr1 )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr1_in_expr92069)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:396:5: ( ':' (e3= expr1 )? )?
                            alt30 = 2
                            LA30_0 = self.input.LA(1)

                            if (LA30_0 == 42) :
                                alt30 = 1
                            if alt30 == 1:
                                # src/ll/UL4.g:397:6: ':' (e3= expr1 )?
                                pass 
                                self.match(self.input, 42, self.FOLLOW_42_in_expr92084)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:398:6: (e3= expr1 )?
                                alt29 = 2
                                LA29_0 = self.input.LA(1)

                                if ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or LA29_0 == STRING or LA29_0 == TRUE or LA29_0 == 27 or LA29_0 == 35 or LA29_0 == 49 or LA29_0 == 55 or LA29_0 == 57) :
                                    alt29 = 1
                                if alt29 == 1:
                                    # src/ll/UL4.g:399:7: e3= expr1
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr1_in_expr92103)
                                    e3 = self.expr1()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(node, index1, index2) if slice else ul4c.GetItem(node, index1) 






                        self.match(self.input, 50, self.FOLLOW_50_in_expr92132)


                    else:
                        break #loop32





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr9"



    # $ANTLR start "expr8"
    # src/ll/UL4.g:408:1: expr8 returns [node] : ( '-' )* e= expr9 ;
    def expr8(self, ):
        node = None


        e = None


         
        count = 0;
        	
        try:
            try:
                # src/ll/UL4.g:413:2: ( ( '-' )* e= expr9 )
                # src/ll/UL4.g:414:3: ( '-' )* e= expr9
                pass 
                # src/ll/UL4.g:414:3: ( '-' )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 35) :
                        alt33 = 1


                    if alt33 == 1:
                        # src/ll/UL4.g:415:4: '-'
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_expr82168)

                        if self._state.backtracking == 0:
                            pass
                            count += 1; 




                    else:
                        break #loop33


                self._state.following.append(self.FOLLOW_expr9_in_expr82181)
                e = self.expr9()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                              
                    node =  e
                    for i in range(count):
                    	node =  ul4c.Neg.make(node)
                    		






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr8"



    # $ANTLR start "expr7"
    # src/ll/UL4.g:425:1: expr7 returns [node] : e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* ;
    def expr7(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:426:2: (e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* )
                # src/ll/UL4.g:427:3: e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                pass 
                self._state.following.append(self.FOLLOW_expr8_in_expr72204)
                e1 = self.expr8()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:428:3: ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 25 or LA35_0 == 29 or (38 <= LA35_0 <= 39)) :
                        alt35 = 1


                    if alt35 == 1:
                        # src/ll/UL4.g:429:4: ( '*' | '/' | '//' | '%' ) e2= expr8
                        pass 
                        # src/ll/UL4.g:429:4: ( '*' | '/' | '//' | '%' )
                        alt34 = 4
                        LA34 = self.input.LA(1)
                        if LA34 == 29:
                            alt34 = 1
                        elif LA34 == 38:
                            alt34 = 2
                        elif LA34 == 39:
                            alt34 = 3
                        elif LA34 == 25:
                            alt34 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 34, 0, self.input)

                            raise nvae


                        if alt34 == 1:
                            # src/ll/UL4.g:430:5: '*'
                            pass 
                            self.match(self.input, 29, self.FOLLOW_29_in_expr72221)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt34 == 2:
                            # src/ll/UL4.g:432:5: '/'
                            pass 
                            self.match(self.input, 38, self.FOLLOW_38_in_expr72234)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt34 == 3:
                            # src/ll/UL4.g:434:5: '//'
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_expr72247)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt34 == 4:
                            # src/ll/UL4.g:436:5: '%'
                            pass 
                            self.match(self.input, 25, self.FOLLOW_25_in_expr72260)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr8_in_expr72274)
                        e2 = self.expr8()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(node, e2) 




                    else:
                        break #loop35





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr7"



    # $ANTLR start "expr6"
    # src/ll/UL4.g:443:1: expr6 returns [node] : e1= expr7 ( ( '+' | '-' ) e2= expr7 )* ;
    def expr6(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:444:2: (e1= expr7 ( ( '+' | '-' ) e2= expr7 )* )
                # src/ll/UL4.g:445:3: e1= expr7 ( ( '+' | '-' ) e2= expr7 )*
                pass 
                self._state.following.append(self.FOLLOW_expr7_in_expr62302)
                e1 = self.expr7()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:446:3: ( ( '+' | '-' ) e2= expr7 )*
                while True: #loop37
                    alt37 = 2
                    LA37_0 = self.input.LA(1)

                    if (LA37_0 == 32 or LA37_0 == 35) :
                        alt37 = 1


                    if alt37 == 1:
                        # src/ll/UL4.g:447:4: ( '+' | '-' ) e2= expr7
                        pass 
                        # src/ll/UL4.g:447:4: ( '+' | '-' )
                        alt36 = 2
                        LA36_0 = self.input.LA(1)

                        if (LA36_0 == 32) :
                            alt36 = 1
                        elif (LA36_0 == 35) :
                            alt36 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 36, 0, self.input)

                            raise nvae


                        if alt36 == 1:
                            # src/ll/UL4.g:448:5: '+'
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr62319)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt36 == 2:
                            # src/ll/UL4.g:450:5: '-'
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr62332)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr7_in_expr62346)
                        e2 = self.expr7()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(node, e2) 




                    else:
                        break #loop37





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr6"



    # $ANTLR start "expr5"
    # src/ll/UL4.g:457:1: expr5 returns [node] : e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* ;
    def expr5(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:458:2: (e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* )
                # src/ll/UL4.g:459:3: e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                pass 
                self._state.following.append(self.FOLLOW_expr6_in_expr52374)
                e1 = self.expr6()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:460:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                while True: #loop39
                    alt39 = 2
                    LA39_0 = self.input.LA(1)

                    if (LA39_0 == 24 or (43 <= LA39_0 <= 44) or (46 <= LA39_0 <= 48)) :
                        alt39 = 1


                    if alt39 == 1:
                        # src/ll/UL4.g:461:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6
                        pass 
                        # src/ll/UL4.g:461:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt38 = 6
                        LA38 = self.input.LA(1)
                        if LA38 == 46:
                            alt38 = 1
                        elif LA38 == 24:
                            alt38 = 2
                        elif LA38 == 43:
                            alt38 = 3
                        elif LA38 == 44:
                            alt38 = 4
                        elif LA38 == 47:
                            alt38 = 5
                        elif LA38 == 48:
                            alt38 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 38, 0, self.input)

                            raise nvae


                        if alt38 == 1:
                            # src/ll/UL4.g:462:5: '=='
                            pass 
                            self.match(self.input, 46, self.FOLLOW_46_in_expr52391)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt38 == 2:
                            # src/ll/UL4.g:464:5: '!='
                            pass 
                            self.match(self.input, 24, self.FOLLOW_24_in_expr52404)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt38 == 3:
                            # src/ll/UL4.g:466:5: '<'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr52417)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt38 == 4:
                            # src/ll/UL4.g:468:5: '<='
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr52430)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt38 == 5:
                            # src/ll/UL4.g:470:5: '>'
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr52443)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt38 == 6:
                            # src/ll/UL4.g:472:5: '>='
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr52456)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr6_in_expr52470)
                        e2 = self.expr6()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(node, e2) 




                    else:
                        break #loop39





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr5"



    # $ANTLR start "expr4"
    # src/ll/UL4.g:479:1: expr4 returns [node] : e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? ;
    def expr4(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:480:2: (e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? )
                # src/ll/UL4.g:481:3: e1= expr5 ( ( 'not' )? 'in' e2= expr5 )?
                pass 
                self._state.following.append(self.FOLLOW_expr5_in_expr42498)
                e1 = self.expr5()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:482:3: ( ( 'not' )? 'in' e2= expr5 )?
                alt41 = 2
                LA41_0 = self.input.LA(1)

                if ((54 <= LA41_0 <= 55)) :
                    alt41 = 1
                if alt41 == 1:
                    # src/ll/UL4.g:483:4: ( 'not' )? 'in' e2= expr5
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains; 



                    # src/ll/UL4.g:484:4: ( 'not' )?
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 55) :
                        alt40 = 1
                    if alt40 == 1:
                        # src/ll/UL4.g:485:5: 'not'
                        pass 
                        self.match(self.input, 55, self.FOLLOW_55_in_expr42520)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains; 






                    self.match(self.input, 54, self.FOLLOW_54_in_expr42533)

                    self._state.following.append(self.FOLLOW_expr5_in_expr42540)
                    e2 = self.expr5()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = cls.make(node, e2) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr4"



    # $ANTLR start "expr3"
    # src/ll/UL4.g:493:1: expr3 returns [node] : ( 'not' e= expr4 |e= expr4 );
    def expr3(self, ):
        node = None


        e = None


        try:
            try:
                # src/ll/UL4.g:494:2: ( 'not' e= expr4 |e= expr4 )
                alt42 = 2
                LA42_0 = self.input.LA(1)

                if (LA42_0 == 55) :
                    alt42 = 1
                elif ((COLOR <= LA42_0 <= DATE) or (FALSE <= LA42_0 <= FLOAT) or (INT <= LA42_0 <= NONE) or LA42_0 == STRING or LA42_0 == TRUE or LA42_0 == 27 or LA42_0 == 35 or LA42_0 == 49 or LA42_0 == 57) :
                    alt42 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 42, 0, self.input)

                    raise nvae


                if alt42 == 1:
                    # src/ll/UL4.g:495:3: 'not' e= expr4
                    pass 
                    self.match(self.input, 55, self.FOLLOW_55_in_expr32566)

                    self._state.following.append(self.FOLLOW_expr4_in_expr32572)
                    e = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(e) 




                elif alt42 == 2:
                    # src/ll/UL4.g:498:3: e= expr4
                    pass 
                    self._state.following.append(self.FOLLOW_expr4_in_expr32583)
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
    # src/ll/UL4.g:503:1: expr2 returns [node] : e1= expr3 ( 'and' e2= expr3 )* ;
    def expr2(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:504:2: (e1= expr3 ( 'and' e2= expr3 )* )
                # src/ll/UL4.g:505:3: e1= expr3 ( 'and' e2= expr3 )*
                pass 
                self._state.following.append(self.FOLLOW_expr3_in_expr22607)
                e1 = self.expr3()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:506:3: ( 'and' e2= expr3 )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 51) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:507:4: 'and' e2= expr3
                        pass 
                        self.match(self.input, 51, self.FOLLOW_51_in_expr22618)

                        self._state.following.append(self.FOLLOW_expr3_in_expr22625)
                        e2 = self.expr3()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr2"



    # $ANTLR start "expr1"
    # src/ll/UL4.g:513:1: expr1 returns [node] : e1= expr2 ( 'or' e2= expr2 )* ;
    def expr1(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:514:2: (e1= expr2 ( 'or' e2= expr2 )* )
                # src/ll/UL4.g:515:3: e1= expr2 ( 'or' e2= expr2 )*
                pass 
                self._state.following.append(self.FOLLOW_expr2_in_expr12653)
                e1 = self.expr2()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:516:3: ( 'or' e2= expr2 )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 56) :
                        alt44 = 1


                    if alt44 == 1:
                        # src/ll/UL4.g:517:4: 'or' e2= expr2
                        pass 
                        self.match(self.input, 56, self.FOLLOW_56_in_expr12664)

                        self._state.following.append(self.FOLLOW_expr2_in_expr12671)
                        e2 = self.expr2()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(node, e2) 




                    else:
                        break #loop44





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr1"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:522:1: exprarg returns [node] : (ege= generatorexpression |e1= expr1 );
    def exprarg(self, ):
        node = None


        ege = None

        e1 = None


        try:
            try:
                # src/ll/UL4.g:523:2: (ege= generatorexpression |e1= expr1 )
                alt45 = 2
                LA45 = self.input.LA(1)
                if LA45 == 55:
                    LA45_1 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 1, self.input)

                        raise nvae


                elif LA45 == 35:
                    LA45_2 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 2, self.input)

                        raise nvae


                elif LA45 == NONE:
                    LA45_3 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 3, self.input)

                        raise nvae


                elif LA45 == FALSE:
                    LA45_4 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 4, self.input)

                        raise nvae


                elif LA45 == TRUE:
                    LA45_5 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 5, self.input)

                        raise nvae


                elif LA45 == INT:
                    LA45_6 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 6, self.input)

                        raise nvae


                elif LA45 == FLOAT:
                    LA45_7 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 7, self.input)

                        raise nvae


                elif LA45 == STRING:
                    LA45_8 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 8, self.input)

                        raise nvae


                elif LA45 == DATE:
                    LA45_9 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
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

                    if (self.synpred69_UL4()) :
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

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 11, self.input)

                        raise nvae


                elif LA45 == 49:
                    LA45_12 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 12, self.input)

                        raise nvae


                elif LA45 == 57:
                    LA45_13 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 13, self.input)

                        raise nvae


                elif LA45 == 27:
                    LA45_14 = self.input.LA(2)

                    if (self.synpred69_UL4()) :
                        alt45 = 1
                    elif (True) :
                        alt45 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 45, 14, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 45, 0, self.input)

                    raise nvae


                if alt45 == 1:
                    # src/ll/UL4.g:523:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2695)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt45 == 2:
                    # src/ll/UL4.g:524:4: e1= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_exprarg2704)
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
    # src/ll/UL4.g:527:1: expression returns [node] : (ege= generatorexpression EOF |e= expr1 EOF );
    def expression(self, ):
        node = None


        ege = None

        e = None


        try:
            try:
                # src/ll/UL4.g:528:2: (ege= generatorexpression EOF |e= expr1 EOF )
                alt46 = 2
                LA46 = self.input.LA(1)
                if LA46 == 55:
                    LA46_1 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 1, self.input)

                        raise nvae


                elif LA46 == 35:
                    LA46_2 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 2, self.input)

                        raise nvae


                elif LA46 == NONE:
                    LA46_3 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 3, self.input)

                        raise nvae


                elif LA46 == FALSE:
                    LA46_4 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 4, self.input)

                        raise nvae


                elif LA46 == TRUE:
                    LA46_5 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 5, self.input)

                        raise nvae


                elif LA46 == INT:
                    LA46_6 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 6, self.input)

                        raise nvae


                elif LA46 == FLOAT:
                    LA46_7 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 7, self.input)

                        raise nvae


                elif LA46 == STRING:
                    LA46_8 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 8, self.input)

                        raise nvae


                elif LA46 == DATE:
                    LA46_9 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
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

                    if (self.synpred70_UL4()) :
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

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 11, self.input)

                        raise nvae


                elif LA46 == 49:
                    LA46_12 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 12, self.input)

                        raise nvae


                elif LA46 == 57:
                    LA46_13 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 13, self.input)

                        raise nvae


                elif LA46 == 27:
                    LA46_14 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 14, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 46, 0, self.input)

                    raise nvae


                if alt46 == 1:
                    # src/ll/UL4.g:528:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression2723)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2725)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:529:4: e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_expression2734)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2736)

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
    # src/ll/UL4.g:535:1: for_ returns [node] : n= nestedname 'in' e= expr1 EOF ;
    def for_(self, ):
        node = None


        n = None

        e = None


        try:
            try:
                # src/ll/UL4.g:536:2: (n= nestedname 'in' e= expr1 EOF )
                # src/ll/UL4.g:537:3: n= nestedname 'in' e= expr1 EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedname_in_for_2761)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_for_2765)

                self._state.following.append(self.FOLLOW_expr1_in_for_2771)
                e = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.For(self.location, n, e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_2777)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:546:1: statement returns [node] : (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None

        e = None

        n = None


        try:
            try:
                # src/ll/UL4.g:547:2: (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF )
                alt47 = 8
                LA47 = self.input.LA(1)
                if LA47 == NAME:
                    LA47_1 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (self.synpred72_UL4()) :
                        alt47 = 2
                    elif (self.synpred73_UL4()) :
                        alt47 = 3
                    elif (self.synpred74_UL4()) :
                        alt47 = 4
                    elif (self.synpred75_UL4()) :
                        alt47 = 5
                    elif (self.synpred76_UL4()) :
                        alt47 = 6
                    elif (self.synpred77_UL4()) :
                        alt47 = 7
                    elif (True) :
                        alt47 = 8
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 1, self.input)

                        raise nvae


                elif LA47 == 27:
                    LA47_2 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 8
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 2, self.input)

                        raise nvae


                elif LA47 == COLOR or LA47 == DATE or LA47 == FALSE or LA47 == FLOAT or LA47 == INT or LA47 == NONE or LA47 == STRING or LA47 == TRUE or LA47 == 35 or LA47 == 49 or LA47 == 55 or LA47 == 57:
                    alt47 = 8
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 47, 0, self.input)

                    raise nvae


                if alt47 == 1:
                    # src/ll/UL4.g:547:4: nn= nestedname '=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedname_in_statement2798)
                    nn = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement2800)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2804)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2806)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.StoreVar(self.location, nn, e) 




                elif alt47 == 2:
                    # src/ll/UL4.g:548:4: n= name '+=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2815)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 33, self.FOLLOW_33_in_statement2817)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2821)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2823)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 3:
                    # src/ll/UL4.g:549:4: n= name '-=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2832)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement2834)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2838)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2840)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 4:
                    # src/ll/UL4.g:550:4: n= name '*=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2849)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement2851)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2855)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2857)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 5:
                    # src/ll/UL4.g:551:4: n= name '/=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2866)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement2868)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2872)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2874)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 6:
                    # src/ll/UL4.g:552:4: n= name '//=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2883)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 40, self.FOLLOW_40_in_statement2885)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2889)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2891)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 7:
                    # src/ll/UL4.g:553:4: n= name '%=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2900)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 26, self.FOLLOW_26_in_statement2902)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2906)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2908)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt47 == 8:
                    # src/ll/UL4.g:554:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement2917)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2919)

                    if self._state.backtracking == 0:
                        pass
                        node = e 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "statement"

    # $ANTLR start "synpred19_UL4"
    def synpred19_UL4_fragment(self, ):
        e_list = None


        # src/ll/UL4.g:289:4: (e_list= list )
        # src/ll/UL4.g:289:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred19_UL41370)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred19_UL4"



    # $ANTLR start "synpred20_UL4"
    def synpred20_UL4_fragment(self, ):
        e_listcomp = None


        # src/ll/UL4.g:290:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:290:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred20_UL41379)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred20_UL4"



    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_dict = None


        # src/ll/UL4.g:291:4: (e_dict= dict )
        # src/ll/UL4.g:291:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred21_UL41388)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_dictcomp = None


        # src/ll/UL4.g:292:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:292:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred22_UL41397)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_genexpr = None


        # src/ll/UL4.g:293:4: ( '(' e_genexpr= generatorexpression ')' )
        # src/ll/UL4.g:293:4: '(' e_genexpr= generatorexpression ')'
        pass 
        self.match(self.input, 27, self.FOLLOW_27_in_synpred23_UL41404)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred23_UL41408)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, 28, self.FOLLOW_28_in_synpred23_UL41410)



    # $ANTLR end "synpred23_UL4"



    # $ANTLR start "synpred25_UL4"
    def synpred25_UL4_fragment(self, ):
        n0 = None


        # src/ll/UL4.g:302:3: ( '(' n0= nestedname ',' ')' )
        # src/ll/UL4.g:302:3: '(' n0= nestedname ',' ')'
        pass 
        self.match(self.input, 27, self.FOLLOW_27_in_synpred25_UL41455)

        self._state.following.append(self.FOLLOW_nestedname_in_synpred25_UL41459)
        n0 = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 34, self.FOLLOW_34_in_synpred25_UL41461)

        self.match(self.input, 28, self.FOLLOW_28_in_synpred25_UL41463)



    # $ANTLR end "synpred25_UL4"



    # $ANTLR start "synpred69_UL4"
    def synpred69_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:523:4: (ege= generatorexpression )
        # src/ll/UL4.g:523:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred69_UL42695)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred69_UL4"



    # $ANTLR start "synpred70_UL4"
    def synpred70_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:528:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:528:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred70_UL42723)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred70_UL42725)



    # $ANTLR end "synpred70_UL4"



    # $ANTLR start "synpred71_UL4"
    def synpred71_UL4_fragment(self, ):
        nn = None

        e = None


        # src/ll/UL4.g:547:4: (nn= nestedname '=' e= expr1 EOF )
        # src/ll/UL4.g:547:4: nn= nestedname '=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedname_in_synpred71_UL42798)
        nn = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 45, self.FOLLOW_45_in_synpred71_UL42800)

        self._state.following.append(self.FOLLOW_expr1_in_synpred71_UL42804)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred71_UL42806)



    # $ANTLR end "synpred71_UL4"



    # $ANTLR start "synpred72_UL4"
    def synpred72_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:548:4: (n= name '+=' e= expr1 EOF )
        # src/ll/UL4.g:548:4: n= name '+=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred72_UL42815)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 33, self.FOLLOW_33_in_synpred72_UL42817)

        self._state.following.append(self.FOLLOW_expr1_in_synpred72_UL42821)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred72_UL42823)



    # $ANTLR end "synpred72_UL4"



    # $ANTLR start "synpred73_UL4"
    def synpred73_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:549:4: (n= name '-=' e= expr1 EOF )
        # src/ll/UL4.g:549:4: n= name '-=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred73_UL42832)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred73_UL42834)

        self._state.following.append(self.FOLLOW_expr1_in_synpred73_UL42838)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred73_UL42840)



    # $ANTLR end "synpred73_UL4"



    # $ANTLR start "synpred74_UL4"
    def synpred74_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:550:4: (n= name '*=' e= expr1 EOF )
        # src/ll/UL4.g:550:4: n= name '*=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred74_UL42849)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 31, self.FOLLOW_31_in_synpred74_UL42851)

        self._state.following.append(self.FOLLOW_expr1_in_synpred74_UL42855)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred74_UL42857)



    # $ANTLR end "synpred74_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:551:4: (n= name '/=' e= expr1 EOF )
        # src/ll/UL4.g:551:4: n= name '/=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred75_UL42866)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred75_UL42868)

        self._state.following.append(self.FOLLOW_expr1_in_synpred75_UL42872)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred75_UL42874)



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:552:4: (n= name '//=' e= expr1 EOF )
        # src/ll/UL4.g:552:4: n= name '//=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred76_UL42883)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 40, self.FOLLOW_40_in_synpred76_UL42885)

        self._state.following.append(self.FOLLOW_expr1_in_synpred76_UL42889)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred76_UL42891)



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:553:4: (n= name '%=' e= expr1 EOF )
        # src/ll/UL4.g:553:4: n= name '%=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred77_UL42900)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 26, self.FOLLOW_26_in_synpred77_UL42902)

        self._state.following.append(self.FOLLOW_expr1_in_synpred77_UL42906)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL42908)



    # $ANTLR end "synpred77_UL4"




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

    def synpred70_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred70_UL4_fragment()
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

    def synpred20_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred20_UL4_fragment()
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

    def synpred72_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred72_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred69_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred69_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred19_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred19_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success

    def synpred71_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred71_UL4_fragment()
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

    def synpred73_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred73_UL4_fragment()
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

    def synpred74_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred74_UL4_fragment()
        except BacktrackingFailed:
            success = False
        else:
            success = True
        self.input.rewind(start)
        self._state.backtracking -= 1
        return success



 

    FOLLOW_NONE_in_none695 = frozenset([1])
    FOLLOW_TRUE_in_true_712 = frozenset([1])
    FOLLOW_FALSE_in_false_729 = frozenset([1])
    FOLLOW_INT_in_int_746 = frozenset([1])
    FOLLOW_FLOAT_in_float_763 = frozenset([1])
    FOLLOW_STRING_in_string780 = frozenset([1])
    FOLLOW_DATE_in_date797 = frozenset([1])
    FOLLOW_COLOR_in_color814 = frozenset([1])
    FOLLOW_NAME_in_name831 = frozenset([1])
    FOLLOW_none_in_literal850 = frozenset([1])
    FOLLOW_false__in_literal859 = frozenset([1])
    FOLLOW_true__in_literal868 = frozenset([1])
    FOLLOW_int__in_literal877 = frozenset([1])
    FOLLOW_float__in_literal886 = frozenset([1])
    FOLLOW_string_in_literal895 = frozenset([1])
    FOLLOW_date_in_literal904 = frozenset([1])
    FOLLOW_color_in_literal913 = frozenset([1])
    FOLLOW_name_in_literal922 = frozenset([1])
    FOLLOW_49_in_list943 = frozenset([50])
    FOLLOW_50_in_list947 = frozenset([1])
    FOLLOW_49_in_list956 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_list964 = frozenset([34, 50])
    FOLLOW_34_in_list975 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_list982 = frozenset([34, 50])
    FOLLOW_34_in_list993 = frozenset([50])
    FOLLOW_50_in_list998 = frozenset([1])
    FOLLOW_49_in_listcomprehension1022 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_listcomprehension1028 = frozenset([52])
    FOLLOW_52_in_listcomprehension1032 = frozenset([14, 27])
    FOLLOW_nestedname_in_listcomprehension1038 = frozenset([54])
    FOLLOW_54_in_listcomprehension1042 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_listcomprehension1048 = frozenset([50, 53])
    FOLLOW_53_in_listcomprehension1057 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_listcomprehension1064 = frozenset([50])
    FOLLOW_50_in_listcomprehension1075 = frozenset([1])
    FOLLOW_expr1_in_dictitem1100 = frozenset([42])
    FOLLOW_42_in_dictitem1104 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictitem1110 = frozenset([1])
    FOLLOW_57_in_dict1129 = frozenset([58])
    FOLLOW_58_in_dict1133 = frozenset([1])
    FOLLOW_57_in_dict1142 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_dictitem_in_dict1150 = frozenset([34, 58])
    FOLLOW_34_in_dict1161 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_dictitem_in_dict1168 = frozenset([34, 58])
    FOLLOW_34_in_dict1179 = frozenset([58])
    FOLLOW_58_in_dict1184 = frozenset([1])
    FOLLOW_57_in_dictcomprehension1208 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1214 = frozenset([42])
    FOLLOW_42_in_dictcomprehension1218 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1224 = frozenset([52])
    FOLLOW_52_in_dictcomprehension1228 = frozenset([14, 27])
    FOLLOW_nestedname_in_dictcomprehension1234 = frozenset([54])
    FOLLOW_54_in_dictcomprehension1238 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1244 = frozenset([53, 58])
    FOLLOW_53_in_dictcomprehension1253 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1260 = frozenset([58])
    FOLLOW_58_in_dictcomprehension1271 = frozenset([1])
    FOLLOW_expr1_in_generatorexpression1299 = frozenset([52])
    FOLLOW_52_in_generatorexpression1303 = frozenset([14, 27])
    FOLLOW_nestedname_in_generatorexpression1309 = frozenset([54])
    FOLLOW_54_in_generatorexpression1313 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_generatorexpression1319 = frozenset([1, 53])
    FOLLOW_53_in_generatorexpression1328 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_generatorexpression1335 = frozenset([1])
    FOLLOW_literal_in_atom1361 = frozenset([1])
    FOLLOW_list_in_atom1370 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1379 = frozenset([1])
    FOLLOW_dict_in_atom1388 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1397 = frozenset([1])
    FOLLOW_27_in_atom1404 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_generatorexpression_in_atom1408 = frozenset([28])
    FOLLOW_28_in_atom1410 = frozenset([1])
    FOLLOW_27_in_atom1417 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_atom1421 = frozenset([28])
    FOLLOW_28_in_atom1423 = frozenset([1])
    FOLLOW_name_in_nestedname1446 = frozenset([1])
    FOLLOW_27_in_nestedname1455 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1459 = frozenset([34])
    FOLLOW_34_in_nestedname1461 = frozenset([28])
    FOLLOW_28_in_nestedname1463 = frozenset([1])
    FOLLOW_27_in_nestedname1472 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1478 = frozenset([34])
    FOLLOW_34_in_nestedname1482 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1488 = frozenset([28, 34])
    FOLLOW_34_in_nestedname1499 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1506 = frozenset([28, 34])
    FOLLOW_34_in_nestedname1517 = frozenset([28])
    FOLLOW_28_in_nestedname1522 = frozenset([1])
    FOLLOW_atom_in_expr91551 = frozenset([1, 27, 37, 49])
    FOLLOW_37_in_expr91567 = frozenset([14])
    FOLLOW_name_in_expr91574 = frozenset([1, 27, 37, 49])
    FOLLOW_27_in_expr91590 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 28, 29, 30, 35, 49, 55, 57])
    FOLLOW_30_in_expr91620 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91624 = frozenset([28, 34])
    FOLLOW_34_in_expr91632 = frozenset([28])
    FOLLOW_29_in_expr91650 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91654 = frozenset([28, 34])
    FOLLOW_34_in_expr91669 = frozenset([30])
    FOLLOW_30_in_expr91676 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91680 = frozenset([28, 34])
    FOLLOW_34_in_expr91695 = frozenset([28])
    FOLLOW_exprarg_in_expr91715 = frozenset([28, 34])
    FOLLOW_34_in_expr91730 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91739 = frozenset([28, 34])
    FOLLOW_34_in_expr91761 = frozenset([14])
    FOLLOW_name_in_expr91770 = frozenset([45])
    FOLLOW_45_in_expr91772 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91776 = frozenset([28, 34])
    FOLLOW_34_in_expr91798 = frozenset([29])
    FOLLOW_29_in_expr91805 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91809 = frozenset([28, 34])
    FOLLOW_34_in_expr91831 = frozenset([30])
    FOLLOW_30_in_expr91838 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91842 = frozenset([28, 34])
    FOLLOW_34_in_expr91857 = frozenset([28])
    FOLLOW_name_in_expr91877 = frozenset([45])
    FOLLOW_45_in_expr91879 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91883 = frozenset([28, 34])
    FOLLOW_34_in_expr91898 = frozenset([14])
    FOLLOW_name_in_expr91907 = frozenset([45])
    FOLLOW_45_in_expr91909 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91913 = frozenset([28, 34])
    FOLLOW_34_in_expr91935 = frozenset([29])
    FOLLOW_29_in_expr91942 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91946 = frozenset([28, 34])
    FOLLOW_34_in_expr91968 = frozenset([30])
    FOLLOW_30_in_expr91975 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91979 = frozenset([28, 34])
    FOLLOW_34_in_expr91994 = frozenset([28])
    FOLLOW_28_in_expr92005 = frozenset([1, 27, 37, 49])
    FOLLOW_49_in_expr92019 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 42, 49, 55, 57])
    FOLLOW_42_in_expr92030 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 50, 55, 57])
    FOLLOW_expr1_in_expr92045 = frozenset([50])
    FOLLOW_expr1_in_expr92069 = frozenset([42, 50])
    FOLLOW_42_in_expr92084 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 50, 55, 57])
    FOLLOW_expr1_in_expr92103 = frozenset([50])
    FOLLOW_50_in_expr92132 = frozenset([1, 27, 37, 49])
    FOLLOW_35_in_expr82168 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr9_in_expr82181 = frozenset([1])
    FOLLOW_expr8_in_expr72204 = frozenset([1, 25, 29, 38, 39])
    FOLLOW_29_in_expr72221 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_38_in_expr72234 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_39_in_expr72247 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_25_in_expr72260 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr8_in_expr72274 = frozenset([1, 25, 29, 38, 39])
    FOLLOW_expr7_in_expr62302 = frozenset([1, 32, 35])
    FOLLOW_32_in_expr62319 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_35_in_expr62332 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr7_in_expr62346 = frozenset([1, 32, 35])
    FOLLOW_expr6_in_expr52374 = frozenset([1, 24, 43, 44, 46, 47, 48])
    FOLLOW_46_in_expr52391 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_24_in_expr52404 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_43_in_expr52417 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_44_in_expr52430 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_47_in_expr52443 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_48_in_expr52456 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr6_in_expr52470 = frozenset([1, 24, 43, 44, 46, 47, 48])
    FOLLOW_expr5_in_expr42498 = frozenset([1, 54, 55])
    FOLLOW_55_in_expr42520 = frozenset([54])
    FOLLOW_54_in_expr42533 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr5_in_expr42540 = frozenset([1])
    FOLLOW_55_in_expr32566 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr4_in_expr32572 = frozenset([1])
    FOLLOW_expr4_in_expr32583 = frozenset([1])
    FOLLOW_expr3_in_expr22607 = frozenset([1, 51])
    FOLLOW_51_in_expr22618 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr3_in_expr22625 = frozenset([1, 51])
    FOLLOW_expr2_in_expr12653 = frozenset([1, 56])
    FOLLOW_56_in_expr12664 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr2_in_expr12671 = frozenset([1, 56])
    FOLLOW_generatorexpression_in_exprarg2695 = frozenset([1])
    FOLLOW_expr1_in_exprarg2704 = frozenset([1])
    FOLLOW_generatorexpression_in_expression2723 = frozenset([])
    FOLLOW_EOF_in_expression2725 = frozenset([1])
    FOLLOW_expr1_in_expression2734 = frozenset([])
    FOLLOW_EOF_in_expression2736 = frozenset([1])
    FOLLOW_nestedname_in_for_2761 = frozenset([54])
    FOLLOW_54_in_for_2765 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_for_2771 = frozenset([])
    FOLLOW_EOF_in_for_2777 = frozenset([1])
    FOLLOW_nestedname_in_statement2798 = frozenset([45])
    FOLLOW_45_in_statement2800 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2804 = frozenset([])
    FOLLOW_EOF_in_statement2806 = frozenset([1])
    FOLLOW_name_in_statement2815 = frozenset([33])
    FOLLOW_33_in_statement2817 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2821 = frozenset([])
    FOLLOW_EOF_in_statement2823 = frozenset([1])
    FOLLOW_name_in_statement2832 = frozenset([36])
    FOLLOW_36_in_statement2834 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2838 = frozenset([])
    FOLLOW_EOF_in_statement2840 = frozenset([1])
    FOLLOW_name_in_statement2849 = frozenset([31])
    FOLLOW_31_in_statement2851 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2855 = frozenset([])
    FOLLOW_EOF_in_statement2857 = frozenset([1])
    FOLLOW_name_in_statement2866 = frozenset([41])
    FOLLOW_41_in_statement2868 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2872 = frozenset([])
    FOLLOW_EOF_in_statement2874 = frozenset([1])
    FOLLOW_name_in_statement2883 = frozenset([40])
    FOLLOW_40_in_statement2885 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2889 = frozenset([])
    FOLLOW_EOF_in_statement2891 = frozenset([1])
    FOLLOW_name_in_statement2900 = frozenset([26])
    FOLLOW_26_in_statement2902 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2906 = frozenset([])
    FOLLOW_EOF_in_statement2908 = frozenset([1])
    FOLLOW_expression_in_statement2917 = frozenset([])
    FOLLOW_EOF_in_statement2919 = frozenset([1])
    FOLLOW_list_in_synpred19_UL41370 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred20_UL41379 = frozenset([1])
    FOLLOW_dict_in_synpred21_UL41388 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred22_UL41397 = frozenset([1])
    FOLLOW_27_in_synpred23_UL41404 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_generatorexpression_in_synpred23_UL41408 = frozenset([28])
    FOLLOW_28_in_synpred23_UL41410 = frozenset([1])
    FOLLOW_27_in_synpred25_UL41455 = frozenset([14, 27])
    FOLLOW_nestedname_in_synpred25_UL41459 = frozenset([34])
    FOLLOW_34_in_synpred25_UL41461 = frozenset([28])
    FOLLOW_28_in_synpred25_UL41463 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred69_UL42695 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred70_UL42723 = frozenset([])
    FOLLOW_EOF_in_synpred70_UL42725 = frozenset([1])
    FOLLOW_nestedname_in_synpred71_UL42798 = frozenset([45])
    FOLLOW_45_in_synpred71_UL42800 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred71_UL42804 = frozenset([])
    FOLLOW_EOF_in_synpred71_UL42806 = frozenset([1])
    FOLLOW_name_in_synpred72_UL42815 = frozenset([33])
    FOLLOW_33_in_synpred72_UL42817 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred72_UL42821 = frozenset([])
    FOLLOW_EOF_in_synpred72_UL42823 = frozenset([1])
    FOLLOW_name_in_synpred73_UL42832 = frozenset([36])
    FOLLOW_36_in_synpred73_UL42834 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred73_UL42838 = frozenset([])
    FOLLOW_EOF_in_synpred73_UL42840 = frozenset([1])
    FOLLOW_name_in_synpred74_UL42849 = frozenset([31])
    FOLLOW_31_in_synpred74_UL42851 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred74_UL42855 = frozenset([])
    FOLLOW_EOF_in_synpred74_UL42857 = frozenset([1])
    FOLLOW_name_in_synpred75_UL42866 = frozenset([41])
    FOLLOW_41_in_synpred75_UL42868 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred75_UL42872 = frozenset([])
    FOLLOW_EOF_in_synpred75_UL42874 = frozenset([1])
    FOLLOW_name_in_synpred76_UL42883 = frozenset([40])
    FOLLOW_40_in_synpred76_UL42885 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred76_UL42889 = frozenset([])
    FOLLOW_EOF_in_synpred76_UL42891 = frozenset([1])
    FOLLOW_name_in_synpred77_UL42900 = frozenset([26])
    FOLLOW_26_in_synpred77_UL42902 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_synpred77_UL42906 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL42908 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
