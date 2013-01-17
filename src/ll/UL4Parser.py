# $ANTLR 3.4 src/ll/UL4.g 2013-01-17 15:59:24

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
                    node =  ul4c.Const(None) 






                       
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
                    node =  ul4c.Const(True) 






                       
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
                    node =  ul4c.Const(False) 






                       
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
                    node =  ul4c.Const(int(INT1.text, 0)) 






                       
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
                    node =  ul4c.Const(float(FLOAT2.text)) 






                       
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
                    node =  ul4c.Const(ast.literal_eval(STRING3.text)) 






                       
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
                    node =  ul4c.Const(datetime.datetime(*map(int, [f for f in ul4c.datesplitter.split(DATE4.text[2:-1]) if f]))) 






                       
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
                    node =  ul4c.Const(color.Color.fromrepr(COLOR5.text)) 






                       
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
                    retval.node =  ul4c.Var(NAME6.text) 





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
                        node =  ul4c.List() 




                elif alt4 == 2:
                    # src/ll/UL4.g:196:3: '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? ']'
                    pass 
                    self.match(self.input, 49, self.FOLLOW_49_in_list956)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.List() 



                    self._state.following.append(self.FOLLOW_expr1_in_list964)
                    e1 = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1); 



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
                                node.items.append(e2); 




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
                    node =  ul4c.ListComp(item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:227:1: fragment dictitem returns [node] : (k= expr1 ':' v= expr1 | '**' d= expr1 );
    def dictitem(self, ):
        node = None


        k = None

        v = None

        d = None


        try:
            try:
                # src/ll/UL4.g:228:2: (k= expr1 ':' v= expr1 | '**' d= expr1 )
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if ((COLOR <= LA6_0 <= DATE) or (FALSE <= LA6_0 <= FLOAT) or (INT <= LA6_0 <= NONE) or LA6_0 == STRING or LA6_0 == TRUE or LA6_0 == 27 or LA6_0 == 35 or LA6_0 == 49 or LA6_0 == 55 or LA6_0 == 57) :
                    alt6 = 1
                elif (LA6_0 == 30) :
                    alt6 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 6, 0, self.input)

                    raise nvae


                if alt6 == 1:
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
                        node =  (k, v) 




                elif alt6 == 2:
                    # src/ll/UL4.g:233:3: '**' d= expr1
                    pass 
                    self.match(self.input, 30, self.FOLLOW_30_in_dictitem1119)

                    self._state.following.append(self.FOLLOW_expr1_in_dictitem1125)
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
    # src/ll/UL4.g:237:1: dict returns [node] : ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' );
    def dict(self, ):
        node = None


        i1 = None

        i2 = None


        try:
            try:
                # src/ll/UL4.g:238:2: ( '{' '}' | '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 57) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 58) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or LA9_1 == STRING or LA9_1 == TRUE or LA9_1 == 27 or LA9_1 == 30 or LA9_1 == 35 or LA9_1 == 49 or LA9_1 == 55 or LA9_1 == 57) :
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
                    # src/ll/UL4.g:239:3: '{' '}'
                    pass 
                    self.match(self.input, 57, self.FOLLOW_57_in_dict1144)

                    self.match(self.input, 58, self.FOLLOW_58_in_dict1148)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Dict() 




                elif alt9 == 2:
                    # src/ll/UL4.g:242:3: '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? '}'
                    pass 
                    self.match(self.input, 57, self.FOLLOW_57_in_dict1157)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Dict() 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1165)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1); 



                    # src/ll/UL4.g:244:3: ( ',' i2= dictitem )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 34) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or LA7_1 == STRING or LA7_1 == TRUE or LA7_1 == 27 or LA7_1 == 30 or LA7_1 == 35 or LA7_1 == 49 or LA7_1 == 55 or LA7_1 == 57) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:245:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_dict1176)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1183)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2); 




                        else:
                            break #loop7


                    # src/ll/UL4.g:248:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 34) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:248:3: ','
                        pass 
                        self.match(self.input, 34, self.FOLLOW_34_in_dict1194)




                    self.match(self.input, 58, self.FOLLOW_58_in_dict1199)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:252:1: dictcomprehension returns [node] : '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' ;
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
                # src/ll/UL4.g:257:2: ( '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}' )
                # src/ll/UL4.g:258:3: '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? '}'
                pass 
                self.match(self.input, 57, self.FOLLOW_57_in_dictcomprehension1223)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1229)
                key = self.expr1()

                self._state.following.pop()

                self.match(self.input, 42, self.FOLLOW_42_in_dictcomprehension1233)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1239)
                value = self.expr1()

                self._state.following.pop()

                self.match(self.input, 52, self.FOLLOW_52_in_dictcomprehension1243)

                self._state.following.append(self.FOLLOW_nestedname_in_dictcomprehension1249)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_dictcomprehension1253)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1259)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:266:3: ( 'if' condition= expr1 )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 53) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:267:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 53, self.FOLLOW_53_in_dictcomprehension1268)

                    self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1275)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                self.match(self.input, 58, self.FOLLOW_58_in_dictcomprehension1286)

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.DictComp(key, value, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:273:1: generatorexpression returns [node] : item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ;
    def generatorexpression(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None;
        	
        try:
            try:
                # src/ll/UL4.g:278:2: (item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? )
                # src/ll/UL4.g:279:3: item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )?
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1314)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 52, self.FOLLOW_52_in_generatorexpression1318)

                self._state.following.append(self.FOLLOW_nestedname_in_generatorexpression1324)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_generatorexpression1328)

                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1334)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:284:3: ( 'if' condition= expr1 )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 53) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:285:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 53, self.FOLLOW_53_in_generatorexpression1343)

                    self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1350)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.GenExpr(item, n, container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:290:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' );
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
                # src/ll/UL4.g:291:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension | '(' e_genexpr= generatorexpression ')' | '(' e_bracket= expr1 ')' )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == COLOR or LA12 == DATE or LA12 == FALSE or LA12 == FLOAT or LA12 == INT or LA12 == NAME or LA12 == NONE or LA12 == STRING or LA12 == TRUE:
                    alt12 = 1
                elif LA12 == 49:
                    LA12_10 = self.input.LA(2)

                    if (self.synpred20_UL4()) :
                        alt12 = 2
                    elif (self.synpred21_UL4()) :
                        alt12 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 10, self.input)

                        raise nvae


                elif LA12 == 57:
                    LA12_11 = self.input.LA(2)

                    if (self.synpred22_UL4()) :
                        alt12 = 4
                    elif (self.synpred23_UL4()) :
                        alt12 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 11, self.input)

                        raise nvae


                elif LA12 == 27:
                    LA12_12 = self.input.LA(2)

                    if (self.synpred24_UL4()) :
                        alt12 = 6
                    elif (True) :
                        alt12 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 12, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae


                if alt12 == 1:
                    # src/ll/UL4.g:291:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1376)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt12 == 2:
                    # src/ll/UL4.g:292:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1385)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt12 == 3:
                    # src/ll/UL4.g:293:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1394)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt12 == 4:
                    # src/ll/UL4.g:294:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1403)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt12 == 5:
                    # src/ll/UL4.g:295:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1412)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt12 == 6:
                    # src/ll/UL4.g:296:4: '(' e_genexpr= generatorexpression ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_atom1419)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1423)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, 28, self.FOLLOW_28_in_atom1425)

                    if self._state.backtracking == 0:
                        pass
                        node =  e_genexpr 




                elif alt12 == 7:
                    # src/ll/UL4.g:297:4: '(' e_bracket= expr1 ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_atom1432)

                    self._state.following.append(self.FOLLOW_expr1_in_atom1436)
                    e_bracket = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, 28, self.FOLLOW_28_in_atom1438)

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
    # src/ll/UL4.g:301:1: nestedname returns [varname] : (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' );
    def nestedname(self, ):
        varname = None


        n = None

        n0 = None

        n1 = None

        n2 = None

        n3 = None


        try:
            try:
                # src/ll/UL4.g:302:2: (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if (LA15_0 == NAME) :
                    alt15 = 1
                elif (LA15_0 == 27) :
                    LA15_2 = self.input.LA(2)

                    if (self.synpred26_UL4()) :
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
                    # src/ll/UL4.g:303:3: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_nestedname1461)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname =  ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0] 




                elif alt15 == 2:
                    # src/ll/UL4.g:305:3: '(' n0= nestedname ',' ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_nestedname1470)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1474)
                    n0 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_nestedname1476)

                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1478)

                    if self._state.backtracking == 0:
                        pass
                        varname =  (n0,) 




                elif alt15 == 3:
                    # src/ll/UL4.g:307:3: '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 27, self.FOLLOW_27_in_nestedname1487)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1493)
                    n1 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_nestedname1497)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1503)
                    n2 = self.nestedname()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        varname =  (n1, n2) 



                    # src/ll/UL4.g:311:3: ( ',' n3= nestedname )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 34) :
                            LA13_1 = self.input.LA(2)

                            if (LA13_1 == NAME or LA13_1 == 27) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:312:4: ',' n3= nestedname
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_nestedname1514)

                            self._state.following.append(self.FOLLOW_nestedname_in_nestedname1521)
                            n3 = self.nestedname()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                varname += (n3,); 




                        else:
                            break #loop13


                    # src/ll/UL4.g:315:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 34) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:315:3: ','
                        pass 
                        self.match(self.input, 34, self.FOLLOW_34_in_nestedname1532)




                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1537)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return varname

    # $ANTLR end "nestedname"



    # $ANTLR start "expr9"
    # src/ll/UL4.g:320:1: expr9 returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* ;
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
                # src/ll/UL4.g:328:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )* )
                # src/ll/UL4.g:329:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr91566)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:330:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']' )*
                while True: #loop33
                    alt33 = 4
                    LA33 = self.input.LA(1)
                    if LA33 == 37:
                        alt33 = 1
                    elif LA33 == 27:
                        alt33 = 2
                    elif LA33 == 49:
                        alt33 = 3

                    if alt33 == 1:
                        # src/ll/UL4.g:332:4: '.' n= name
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_expr91582)

                        self._state.following.append(self.FOLLOW_name_in_expr91589)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.GetAttr(node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt33 == 2:
                        # src/ll/UL4.g:336:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) ')'
                        pass 
                        self.match(self.input, 27, self.FOLLOW_27_in_expr91605)

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.CallMeth(node.obj, node.attrname) if isinstance(node, ul4c.GetAttr) else ul4c.CallFunc(node) 



                        # src/ll/UL4.g:337:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt28 = 5
                        LA28 = self.input.LA(1)
                        if LA28 == 28:
                            alt28 = 1
                        elif LA28 == 30:
                            alt28 = 2
                        elif LA28 == 29:
                            alt28 = 3
                        elif LA28 == COLOR or LA28 == DATE or LA28 == FALSE or LA28 == FLOAT or LA28 == INT or LA28 == NONE or LA28 == STRING or LA28 == TRUE or LA28 == 27 or LA28 == 35 or LA28 == 49 or LA28 == 55 or LA28 == 57:
                            alt28 = 4
                        elif LA28 == NAME:
                            LA28_5 = self.input.LA(2)

                            if ((24 <= LA28_5 <= 25) or (27 <= LA28_5 <= 29) or LA28_5 == 32 or (34 <= LA28_5 <= 35) or (37 <= LA28_5 <= 39) or (43 <= LA28_5 <= 44) or (46 <= LA28_5 <= 49) or (51 <= LA28_5 <= 52) or (54 <= LA28_5 <= 56)) :
                                alt28 = 4
                            elif (LA28_5 == 45) :
                                alt28 = 5
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 28, 5, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 28, 0, self.input)

                            raise nvae


                        if alt28 == 1:
                            # src/ll/UL4.g:339:4: 
                            pass 

                        elif alt28 == 2:
                            # src/ll/UL4.g:341:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 30, self.FOLLOW_30_in_expr91635)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91639)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:342:5: ( ',' )?
                            alt16 = 2
                            LA16_0 = self.input.LA(1)

                            if (LA16_0 == 34) :
                                alt16 = 1
                            if alt16 == 1:
                                # src/ll/UL4.g:342:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91647)





                        elif alt28 == 3:
                            # src/ll/UL4.g:345:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 29, self.FOLLOW_29_in_expr91665)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91669)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remargs = rargs; 



                            # src/ll/UL4.g:346:5: ( ',' '**' rkwargs= exprarg )?
                            alt17 = 2
                            LA17_0 = self.input.LA(1)

                            if (LA17_0 == 34) :
                                LA17_1 = self.input.LA(2)

                                if (LA17_1 == 30) :
                                    alt17 = 1
                            if alt17 == 1:
                                # src/ll/UL4.g:347:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91684)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91691)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91695)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:350:5: ( ',' )?
                            alt18 = 2
                            LA18_0 = self.input.LA(1)

                            if (LA18_0 == 34) :
                                alt18 = 1
                            if alt18 == 1:
                                # src/ll/UL4.g:350:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91710)





                        elif alt28 == 4:
                            # src/ll/UL4.g:353:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr91730)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.args.append(a1); 



                            # src/ll/UL4.g:354:5: ( ',' a2= exprarg )*
                            while True: #loop19
                                alt19 = 2
                                LA19_0 = self.input.LA(1)

                                if (LA19_0 == 34) :
                                    LA19_1 = self.input.LA(2)

                                    if (LA19_1 == NAME) :
                                        LA19_3 = self.input.LA(3)

                                        if ((24 <= LA19_3 <= 25) or (27 <= LA19_3 <= 29) or LA19_3 == 32 or (34 <= LA19_3 <= 35) or (37 <= LA19_3 <= 39) or (43 <= LA19_3 <= 44) or (46 <= LA19_3 <= 49) or (51 <= LA19_3 <= 52) or (54 <= LA19_3 <= 56)) :
                                            alt19 = 1


                                    elif ((COLOR <= LA19_1 <= DATE) or (FALSE <= LA19_1 <= FLOAT) or LA19_1 == INT or LA19_1 == NONE or LA19_1 == STRING or LA19_1 == TRUE or LA19_1 == 27 or LA19_1 == 35 or LA19_1 == 49 or LA19_1 == 55 or LA19_1 == 57) :
                                        alt19 = 1




                                if alt19 == 1:
                                    # src/ll/UL4.g:355:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91745)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91754)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.args.append(a2); 




                                else:
                                    break #loop19


                            # src/ll/UL4.g:358:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop20
                                alt20 = 2
                                LA20_0 = self.input.LA(1)

                                if (LA20_0 == 34) :
                                    LA20_1 = self.input.LA(2)

                                    if (LA20_1 == NAME) :
                                        alt20 = 1




                                if alt20 == 1:
                                    # src/ll/UL4.g:359:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91776)

                                    self._state.following.append(self.FOLLOW_name_in_expr91785)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 45, self.FOLLOW_45_in_expr91787)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91791)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)); 




                                else:
                                    break #loop20


                            # src/ll/UL4.g:362:5: ( ',' '*' rargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 34) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 29) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:363:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91813)

                                self.match(self.input, 29, self.FOLLOW_29_in_expr91820)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91824)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:366:5: ( ',' '**' rkwargs= exprarg )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 34) :
                                LA22_1 = self.input.LA(2)

                                if (LA22_1 == 30) :
                                    alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:367:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91846)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91853)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91857)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:370:5: ( ',' )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 34) :
                                alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:370:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91872)





                        elif alt28 == 5:
                            # src/ll/UL4.g:373:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr91892)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 45, self.FOLLOW_45_in_expr91894)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91898)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)); 



                            # src/ll/UL4.g:374:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop24
                                alt24 = 2
                                LA24_0 = self.input.LA(1)

                                if (LA24_0 == 34) :
                                    LA24_1 = self.input.LA(2)

                                    if (LA24_1 == NAME) :
                                        alt24 = 1




                                if alt24 == 1:
                                    # src/ll/UL4.g:375:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 34, self.FOLLOW_34_in_expr91913)

                                    self._state.following.append(self.FOLLOW_name_in_expr91922)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 45, self.FOLLOW_45_in_expr91924)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91928)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)); 




                                else:
                                    break #loop24


                            # src/ll/UL4.g:378:5: ( ',' '*' rargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 34) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 29) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:379:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91950)

                                self.match(self.input, 29, self.FOLLOW_29_in_expr91957)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91961)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:382:5: ( ',' '**' rkwargs= exprarg )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 34) :
                                LA26_1 = self.input.LA(2)

                                if (LA26_1 == 30) :
                                    alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:383:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr91983)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91990)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91994)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:386:5: ( ',' )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 34) :
                                alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:386:5: ','
                                pass 
                                self.match(self.input, 34, self.FOLLOW_34_in_expr92009)







                        self.match(self.input, 28, self.FOLLOW_28_in_expr92020)


                    elif alt33 == 3:
                        # src/ll/UL4.g:391:4: '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) ']'
                        pass 
                        self.match(self.input, 49, self.FOLLOW_49_in_expr92034)

                        # src/ll/UL4.g:392:4: ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 42) :
                            alt32 = 1
                        elif ((COLOR <= LA32_0 <= DATE) or (FALSE <= LA32_0 <= FLOAT) or (INT <= LA32_0 <= NONE) or LA32_0 == STRING or LA32_0 == TRUE or LA32_0 == 27 or LA32_0 == 35 or LA32_0 == 49 or LA32_0 == 55 or LA32_0 == 57) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:393:5: ':' (e2= expr1 )?
                            pass 
                            self.match(self.input, 42, self.FOLLOW_42_in_expr92045)

                            # src/ll/UL4.g:394:5: (e2= expr1 )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or LA29_0 == STRING or LA29_0 == TRUE or LA29_0 == 27 or LA29_0 == 35 or LA29_0 == 49 or LA29_0 == 55 or LA29_0 == 57) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:395:6: e2= expr1
                                pass 
                                self._state.following.append(self.FOLLOW_expr1_in_expr92060)
                                e2 = self.expr1()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                node =  ul4c.GetSlice(node, None, index2) 




                        elif alt32 == 2:
                            # src/ll/UL4.g:398:5: e2= expr1 ( ':' (e3= expr1 )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr1_in_expr92084)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:399:5: ( ':' (e3= expr1 )? )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 42) :
                                alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:400:6: ':' (e3= expr1 )?
                                pass 
                                self.match(self.input, 42, self.FOLLOW_42_in_expr92099)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:401:6: (e3= expr1 )?
                                alt30 = 2
                                LA30_0 = self.input.LA(1)

                                if ((COLOR <= LA30_0 <= DATE) or (FALSE <= LA30_0 <= FLOAT) or (INT <= LA30_0 <= NONE) or LA30_0 == STRING or LA30_0 == TRUE or LA30_0 == 27 or LA30_0 == 35 or LA30_0 == 49 or LA30_0 == 55 or LA30_0 == 57) :
                                    alt30 = 1
                                if alt30 == 1:
                                    # src/ll/UL4.g:402:7: e3= expr1
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr1_in_expr92118)
                                    e3 = self.expr1()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                node =  ul4c.GetSlice(node, index1, index2) if slice else ul4c.GetItem(node, index1) 






                        self.match(self.input, 50, self.FOLLOW_50_in_expr92147)


                    else:
                        break #loop33





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr9"



    # $ANTLR start "expr8"
    # src/ll/UL4.g:411:1: expr8 returns [node] : ( '-' )* e= expr9 ;
    def expr8(self, ):
        node = None


        e = None


         
        count = 0;
        	
        try:
            try:
                # src/ll/UL4.g:416:2: ( ( '-' )* e= expr9 )
                # src/ll/UL4.g:417:3: ( '-' )* e= expr9
                pass 
                # src/ll/UL4.g:417:3: ( '-' )*
                while True: #loop34
                    alt34 = 2
                    LA34_0 = self.input.LA(1)

                    if (LA34_0 == 35) :
                        alt34 = 1


                    if alt34 == 1:
                        # src/ll/UL4.g:418:4: '-'
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_expr82183)

                        if self._state.backtracking == 0:
                            pass
                            count += 1; 




                    else:
                        break #loop34


                self._state.following.append(self.FOLLOW_expr9_in_expr82196)
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
    # src/ll/UL4.g:428:1: expr7 returns [node] : e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* ;
    def expr7(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:429:2: (e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* )
                # src/ll/UL4.g:430:3: e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                pass 
                self._state.following.append(self.FOLLOW_expr8_in_expr72219)
                e1 = self.expr8()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:431:3: ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 25 or LA36_0 == 29 or (38 <= LA36_0 <= 39)) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:432:4: ( '*' | '/' | '//' | '%' ) e2= expr8
                        pass 
                        # src/ll/UL4.g:432:4: ( '*' | '/' | '//' | '%' )
                        alt35 = 4
                        LA35 = self.input.LA(1)
                        if LA35 == 29:
                            alt35 = 1
                        elif LA35 == 38:
                            alt35 = 2
                        elif LA35 == 39:
                            alt35 = 3
                        elif LA35 == 25:
                            alt35 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 35, 0, self.input)

                            raise nvae


                        if alt35 == 1:
                            # src/ll/UL4.g:433:5: '*'
                            pass 
                            self.match(self.input, 29, self.FOLLOW_29_in_expr72236)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:435:5: '/'
                            pass 
                            self.match(self.input, 38, self.FOLLOW_38_in_expr72249)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt35 == 3:
                            # src/ll/UL4.g:437:5: '//'
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_expr72262)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt35 == 4:
                            # src/ll/UL4.g:439:5: '%'
                            pass 
                            self.match(self.input, 25, self.FOLLOW_25_in_expr72275)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr8_in_expr72289)
                        e2 = self.expr8()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  cls.make(node, e2) 




                    else:
                        break #loop36





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr7"



    # $ANTLR start "expr6"
    # src/ll/UL4.g:446:1: expr6 returns [node] : e1= expr7 ( ( '+' | '-' ) e2= expr7 )* ;
    def expr6(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:447:2: (e1= expr7 ( ( '+' | '-' ) e2= expr7 )* )
                # src/ll/UL4.g:448:3: e1= expr7 ( ( '+' | '-' ) e2= expr7 )*
                pass 
                self._state.following.append(self.FOLLOW_expr7_in_expr62317)
                e1 = self.expr7()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:449:3: ( ( '+' | '-' ) e2= expr7 )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 32 or LA38_0 == 35) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:450:4: ( '+' | '-' ) e2= expr7
                        pass 
                        # src/ll/UL4.g:450:4: ( '+' | '-' )
                        alt37 = 2
                        LA37_0 = self.input.LA(1)

                        if (LA37_0 == 32) :
                            alt37 = 1
                        elif (LA37_0 == 35) :
                            alt37 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:451:5: '+'
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr62334)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:453:5: '-'
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr62347)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr7_in_expr62361)
                        e2 = self.expr7()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(node, e2) 




                    else:
                        break #loop38





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr6"



    # $ANTLR start "expr5"
    # src/ll/UL4.g:460:1: expr5 returns [node] : e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* ;
    def expr5(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:461:2: (e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* )
                # src/ll/UL4.g:462:3: e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                pass 
                self._state.following.append(self.FOLLOW_expr6_in_expr52389)
                e1 = self.expr6()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:463:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 24 or (43 <= LA40_0 <= 44) or (46 <= LA40_0 <= 48)) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:464:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6
                        pass 
                        # src/ll/UL4.g:464:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt39 = 6
                        LA39 = self.input.LA(1)
                        if LA39 == 46:
                            alt39 = 1
                        elif LA39 == 24:
                            alt39 = 2
                        elif LA39 == 43:
                            alt39 = 3
                        elif LA39 == 44:
                            alt39 = 4
                        elif LA39 == 47:
                            alt39 = 5
                        elif LA39 == 48:
                            alt39 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:465:5: '=='
                            pass 
                            self.match(self.input, 46, self.FOLLOW_46_in_expr52406)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:467:5: '!='
                            pass 
                            self.match(self.input, 24, self.FOLLOW_24_in_expr52419)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt39 == 3:
                            # src/ll/UL4.g:469:5: '<'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr52432)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt39 == 4:
                            # src/ll/UL4.g:471:5: '<='
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr52445)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt39 == 5:
                            # src/ll/UL4.g:473:5: '>'
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr52458)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt39 == 6:
                            # src/ll/UL4.g:475:5: '>='
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr52471)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr6_in_expr52485)
                        e2 = self.expr6()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  cls.make(node, e2) 




                    else:
                        break #loop40





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr5"



    # $ANTLR start "expr4"
    # src/ll/UL4.g:482:1: expr4 returns [node] : e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? ;
    def expr4(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:483:2: (e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? )
                # src/ll/UL4.g:484:3: e1= expr5 ( ( 'not' )? 'in' e2= expr5 )?
                pass 
                self._state.following.append(self.FOLLOW_expr5_in_expr42513)
                e1 = self.expr5()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:485:3: ( ( 'not' )? 'in' e2= expr5 )?
                alt42 = 2
                LA42_0 = self.input.LA(1)

                if ((54 <= LA42_0 <= 55)) :
                    alt42 = 1
                if alt42 == 1:
                    # src/ll/UL4.g:486:4: ( 'not' )? 'in' e2= expr5
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains; 



                    # src/ll/UL4.g:487:4: ( 'not' )?
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 55) :
                        alt41 = 1
                    if alt41 == 1:
                        # src/ll/UL4.g:488:5: 'not'
                        pass 
                        self.match(self.input, 55, self.FOLLOW_55_in_expr42535)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains; 






                    self.match(self.input, 54, self.FOLLOW_54_in_expr42548)

                    self._state.following.append(self.FOLLOW_expr5_in_expr42555)
                    e2 = self.expr5()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  cls.make(node, e2) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr4"



    # $ANTLR start "expr3"
    # src/ll/UL4.g:496:1: expr3 returns [node] : ( 'not' e= expr4 |e= expr4 );
    def expr3(self, ):
        node = None


        e = None


        try:
            try:
                # src/ll/UL4.g:497:2: ( 'not' e= expr4 |e= expr4 )
                alt43 = 2
                LA43_0 = self.input.LA(1)

                if (LA43_0 == 55) :
                    alt43 = 1
                elif ((COLOR <= LA43_0 <= DATE) or (FALSE <= LA43_0 <= FLOAT) or (INT <= LA43_0 <= NONE) or LA43_0 == STRING or LA43_0 == TRUE or LA43_0 == 27 or LA43_0 == 35 or LA43_0 == 49 or LA43_0 == 57) :
                    alt43 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 43, 0, self.input)

                    raise nvae


                if alt43 == 1:
                    # src/ll/UL4.g:498:3: 'not' e= expr4
                    pass 
                    self.match(self.input, 55, self.FOLLOW_55_in_expr32581)

                    self._state.following.append(self.FOLLOW_expr4_in_expr32587)
                    e = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.Not.make(e) 




                elif alt43 == 2:
                    # src/ll/UL4.g:501:3: e= expr4
                    pass 
                    self._state.following.append(self.FOLLOW_expr4_in_expr32598)
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
    # src/ll/UL4.g:506:1: expr2 returns [node] : e1= expr3 ( 'and' e2= expr3 )* ;
    def expr2(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:507:2: (e1= expr3 ( 'and' e2= expr3 )* )
                # src/ll/UL4.g:508:3: e1= expr3 ( 'and' e2= expr3 )*
                pass 
                self._state.following.append(self.FOLLOW_expr3_in_expr22622)
                e1 = self.expr3()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:509:3: ( 'and' e2= expr3 )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 51) :
                        alt44 = 1


                    if alt44 == 1:
                        # src/ll/UL4.g:510:4: 'and' e2= expr3
                        pass 
                        self.match(self.input, 51, self.FOLLOW_51_in_expr22633)

                        self._state.following.append(self.FOLLOW_expr3_in_expr22640)
                        e2 = self.expr3()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.And.make(node, e2) 




                    else:
                        break #loop44





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr2"



    # $ANTLR start "expr1"
    # src/ll/UL4.g:516:1: expr1 returns [node] : e1= expr2 ( 'or' e2= expr2 )* ;
    def expr1(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:517:2: (e1= expr2 ( 'or' e2= expr2 )* )
                # src/ll/UL4.g:518:3: e1= expr2 ( 'or' e2= expr2 )*
                pass 
                self._state.following.append(self.FOLLOW_expr2_in_expr12668)
                e1 = self.expr2()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:519:3: ( 'or' e2= expr2 )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 56) :
                        alt45 = 1


                    if alt45 == 1:
                        # src/ll/UL4.g:520:4: 'or' e2= expr2
                        pass 
                        self.match(self.input, 56, self.FOLLOW_56_in_expr12679)

                        self._state.following.append(self.FOLLOW_expr2_in_expr12686)
                        e2 = self.expr2()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node =  ul4c.Or.make(node, e2) 




                    else:
                        break #loop45





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr1"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:525:1: exprarg returns [node] : (ege= generatorexpression |e1= expr1 );
    def exprarg(self, ):
        node = None


        ege = None

        e1 = None


        try:
            try:
                # src/ll/UL4.g:526:2: (ege= generatorexpression |e1= expr1 )
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
                    # src/ll/UL4.g:526:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2710)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:527:4: e1= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_exprarg2719)
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
    # src/ll/UL4.g:530:1: expression returns [node] : (ege= generatorexpression EOF |e= expr1 EOF );
    def expression(self, ):
        node = None


        ege = None

        e = None


        try:
            try:
                # src/ll/UL4.g:531:2: (ege= generatorexpression EOF |e= expr1 EOF )
                alt47 = 2
                LA47 = self.input.LA(1)
                if LA47 == 55:
                    LA47_1 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 1, self.input)

                        raise nvae


                elif LA47 == 35:
                    LA47_2 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 2, self.input)

                        raise nvae


                elif LA47 == NONE:
                    LA47_3 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 3, self.input)

                        raise nvae


                elif LA47 == FALSE:
                    LA47_4 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 4, self.input)

                        raise nvae


                elif LA47 == TRUE:
                    LA47_5 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 5, self.input)

                        raise nvae


                elif LA47 == INT:
                    LA47_6 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 6, self.input)

                        raise nvae


                elif LA47 == FLOAT:
                    LA47_7 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 7, self.input)

                        raise nvae


                elif LA47 == STRING:
                    LA47_8 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 8, self.input)

                        raise nvae


                elif LA47 == DATE:
                    LA47_9 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 9, self.input)

                        raise nvae


                elif LA47 == COLOR:
                    LA47_10 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 10, self.input)

                        raise nvae


                elif LA47 == NAME:
                    LA47_11 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 11, self.input)

                        raise nvae


                elif LA47 == 49:
                    LA47_12 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 12, self.input)

                        raise nvae


                elif LA47 == 57:
                    LA47_13 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 13, self.input)

                        raise nvae


                elif LA47 == 27:
                    LA47_14 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 14, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 47, 0, self.input)

                    raise nvae


                if alt47 == 1:
                    # src/ll/UL4.g:531:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression2738)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2740)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt47 == 2:
                    # src/ll/UL4.g:532:4: e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_expression2749)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2751)

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
    # src/ll/UL4.g:538:1: for_ returns [node] : n= nestedname 'in' e= expr1 EOF ;
    def for_(self, ):
        node = None


        n = None

        e = None


        try:
            try:
                # src/ll/UL4.g:539:2: (n= nestedname 'in' e= expr1 EOF )
                # src/ll/UL4.g:540:3: n= nestedname 'in' e= expr1 EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedname_in_for_2776)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 54, self.FOLLOW_54_in_for_2780)

                self._state.following.append(self.FOLLOW_expr1_in_for_2786)
                e = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  ul4c.For(self.location, n, e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_2792)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:549:1: statement returns [node] : (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF );
    def statement(self, ):
        node = None


        nn = None

        e = None

        n = None


        try:
            try:
                # src/ll/UL4.g:550:2: (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF )
                alt48 = 7
                LA48_0 = self.input.LA(1)

                if (LA48_0 == NAME) :
                    LA48 = self.input.LA(2)
                    if LA48 == 45:
                        alt48 = 1
                    elif LA48 == 33:
                        alt48 = 2
                    elif LA48 == 36:
                        alt48 = 3
                    elif LA48 == 31:
                        alt48 = 4
                    elif LA48 == 41:
                        alt48 = 5
                    elif LA48 == 40:
                        alt48 = 6
                    elif LA48 == 26:
                        alt48 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 48, 1, self.input)

                        raise nvae


                elif (LA48_0 == 27) :
                    alt48 = 1
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 48, 0, self.input)

                    raise nvae


                if alt48 == 1:
                    # src/ll/UL4.g:550:4: nn= nestedname '=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedname_in_statement2813)
                    nn = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement2815)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2819)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2821)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.StoreVar(self.location, nn, e) 




                elif alt48 == 2:
                    # src/ll/UL4.g:551:4: n= name '+=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2830)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 33, self.FOLLOW_33_in_statement2832)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2836)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2838)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.AddVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 3:
                    # src/ll/UL4.g:552:4: n= name '-=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2847)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement2849)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2853)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2855)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.SubVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 4:
                    # src/ll/UL4.g:553:4: n= name '*=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2864)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement2866)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2870)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2872)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.MulVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 5:
                    # src/ll/UL4.g:554:4: n= name '/=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2881)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement2883)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2887)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2889)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.TrueDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 6:
                    # src/ll/UL4.g:555:4: n= name '//=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2898)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 40, self.FOLLOW_40_in_statement2900)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2904)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2906)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.FloorDivVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 7:
                    # src/ll/UL4.g:556:4: n= name '%=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2915)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 26, self.FOLLOW_26_in_statement2917)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2921)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2923)

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.ModVar(self.location, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "statement"

    # $ANTLR start "synpred20_UL4"
    def synpred20_UL4_fragment(self, ):
        e_list = None


        # src/ll/UL4.g:292:4: (e_list= list )
        # src/ll/UL4.g:292:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred20_UL41385)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred20_UL4"



    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_listcomp = None


        # src/ll/UL4.g:293:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:293:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred21_UL41394)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_dict = None


        # src/ll/UL4.g:294:4: (e_dict= dict )
        # src/ll/UL4.g:294:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred22_UL41403)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_dictcomp = None


        # src/ll/UL4.g:295:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:295:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred23_UL41412)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred23_UL4"



    # $ANTLR start "synpred24_UL4"
    def synpred24_UL4_fragment(self, ):
        e_genexpr = None


        # src/ll/UL4.g:296:4: ( '(' e_genexpr= generatorexpression ')' )
        # src/ll/UL4.g:296:4: '(' e_genexpr= generatorexpression ')'
        pass 
        self.match(self.input, 27, self.FOLLOW_27_in_synpred24_UL41419)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred24_UL41423)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, 28, self.FOLLOW_28_in_synpred24_UL41425)



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        n0 = None


        # src/ll/UL4.g:305:3: ( '(' n0= nestedname ',' ')' )
        # src/ll/UL4.g:305:3: '(' n0= nestedname ',' ')'
        pass 
        self.match(self.input, 27, self.FOLLOW_27_in_synpred26_UL41470)

        self._state.following.append(self.FOLLOW_nestedname_in_synpred26_UL41474)
        n0 = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 34, self.FOLLOW_34_in_synpred26_UL41476)

        self.match(self.input, 28, self.FOLLOW_28_in_synpred26_UL41478)



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred70_UL4"
    def synpred70_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:526:4: (ege= generatorexpression )
        # src/ll/UL4.g:526:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred70_UL42710)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred70_UL4"



    # $ANTLR start "synpred71_UL4"
    def synpred71_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:531:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:531:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred71_UL42738)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred71_UL42740)



    # $ANTLR end "synpred71_UL4"




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
    FOLLOW_30_in_dictitem1119 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictitem1125 = frozenset([1])
    FOLLOW_57_in_dict1144 = frozenset([58])
    FOLLOW_58_in_dict1148 = frozenset([1])
    FOLLOW_57_in_dict1157 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 30, 35, 49, 55, 57])
    FOLLOW_dictitem_in_dict1165 = frozenset([34, 58])
    FOLLOW_34_in_dict1176 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 30, 35, 49, 55, 57])
    FOLLOW_dictitem_in_dict1183 = frozenset([34, 58])
    FOLLOW_34_in_dict1194 = frozenset([58])
    FOLLOW_58_in_dict1199 = frozenset([1])
    FOLLOW_57_in_dictcomprehension1223 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1229 = frozenset([42])
    FOLLOW_42_in_dictcomprehension1233 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1239 = frozenset([52])
    FOLLOW_52_in_dictcomprehension1243 = frozenset([14, 27])
    FOLLOW_nestedname_in_dictcomprehension1249 = frozenset([54])
    FOLLOW_54_in_dictcomprehension1253 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1259 = frozenset([53, 58])
    FOLLOW_53_in_dictcomprehension1268 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_dictcomprehension1275 = frozenset([58])
    FOLLOW_58_in_dictcomprehension1286 = frozenset([1])
    FOLLOW_expr1_in_generatorexpression1314 = frozenset([52])
    FOLLOW_52_in_generatorexpression1318 = frozenset([14, 27])
    FOLLOW_nestedname_in_generatorexpression1324 = frozenset([54])
    FOLLOW_54_in_generatorexpression1328 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_generatorexpression1334 = frozenset([1, 53])
    FOLLOW_53_in_generatorexpression1343 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_generatorexpression1350 = frozenset([1])
    FOLLOW_literal_in_atom1376 = frozenset([1])
    FOLLOW_list_in_atom1385 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1394 = frozenset([1])
    FOLLOW_dict_in_atom1403 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1412 = frozenset([1])
    FOLLOW_27_in_atom1419 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_generatorexpression_in_atom1423 = frozenset([28])
    FOLLOW_28_in_atom1425 = frozenset([1])
    FOLLOW_27_in_atom1432 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_atom1436 = frozenset([28])
    FOLLOW_28_in_atom1438 = frozenset([1])
    FOLLOW_name_in_nestedname1461 = frozenset([1])
    FOLLOW_27_in_nestedname1470 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1474 = frozenset([34])
    FOLLOW_34_in_nestedname1476 = frozenset([28])
    FOLLOW_28_in_nestedname1478 = frozenset([1])
    FOLLOW_27_in_nestedname1487 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1493 = frozenset([34])
    FOLLOW_34_in_nestedname1497 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1503 = frozenset([28, 34])
    FOLLOW_34_in_nestedname1514 = frozenset([14, 27])
    FOLLOW_nestedname_in_nestedname1521 = frozenset([28, 34])
    FOLLOW_34_in_nestedname1532 = frozenset([28])
    FOLLOW_28_in_nestedname1537 = frozenset([1])
    FOLLOW_atom_in_expr91566 = frozenset([1, 27, 37, 49])
    FOLLOW_37_in_expr91582 = frozenset([14])
    FOLLOW_name_in_expr91589 = frozenset([1, 27, 37, 49])
    FOLLOW_27_in_expr91605 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 28, 29, 30, 35, 49, 55, 57])
    FOLLOW_30_in_expr91635 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91639 = frozenset([28, 34])
    FOLLOW_34_in_expr91647 = frozenset([28])
    FOLLOW_29_in_expr91665 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91669 = frozenset([28, 34])
    FOLLOW_34_in_expr91684 = frozenset([30])
    FOLLOW_30_in_expr91691 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91695 = frozenset([28, 34])
    FOLLOW_34_in_expr91710 = frozenset([28])
    FOLLOW_exprarg_in_expr91730 = frozenset([28, 34])
    FOLLOW_34_in_expr91745 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91754 = frozenset([28, 34])
    FOLLOW_34_in_expr91776 = frozenset([14])
    FOLLOW_name_in_expr91785 = frozenset([45])
    FOLLOW_45_in_expr91787 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91791 = frozenset([28, 34])
    FOLLOW_34_in_expr91813 = frozenset([29])
    FOLLOW_29_in_expr91820 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91824 = frozenset([28, 34])
    FOLLOW_34_in_expr91846 = frozenset([30])
    FOLLOW_30_in_expr91853 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91857 = frozenset([28, 34])
    FOLLOW_34_in_expr91872 = frozenset([28])
    FOLLOW_name_in_expr91892 = frozenset([45])
    FOLLOW_45_in_expr91894 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91898 = frozenset([28, 34])
    FOLLOW_34_in_expr91913 = frozenset([14])
    FOLLOW_name_in_expr91922 = frozenset([45])
    FOLLOW_45_in_expr91924 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91928 = frozenset([28, 34])
    FOLLOW_34_in_expr91950 = frozenset([29])
    FOLLOW_29_in_expr91957 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91961 = frozenset([28, 34])
    FOLLOW_34_in_expr91983 = frozenset([30])
    FOLLOW_30_in_expr91990 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_exprarg_in_expr91994 = frozenset([28, 34])
    FOLLOW_34_in_expr92009 = frozenset([28])
    FOLLOW_28_in_expr92020 = frozenset([1, 27, 37, 49])
    FOLLOW_49_in_expr92034 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 42, 49, 55, 57])
    FOLLOW_42_in_expr92045 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 50, 55, 57])
    FOLLOW_expr1_in_expr92060 = frozenset([50])
    FOLLOW_expr1_in_expr92084 = frozenset([42, 50])
    FOLLOW_42_in_expr92099 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 50, 55, 57])
    FOLLOW_expr1_in_expr92118 = frozenset([50])
    FOLLOW_50_in_expr92147 = frozenset([1, 27, 37, 49])
    FOLLOW_35_in_expr82183 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr9_in_expr82196 = frozenset([1])
    FOLLOW_expr8_in_expr72219 = frozenset([1, 25, 29, 38, 39])
    FOLLOW_29_in_expr72236 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_38_in_expr72249 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_39_in_expr72262 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_25_in_expr72275 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr8_in_expr72289 = frozenset([1, 25, 29, 38, 39])
    FOLLOW_expr7_in_expr62317 = frozenset([1, 32, 35])
    FOLLOW_32_in_expr62334 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_35_in_expr62347 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr7_in_expr62361 = frozenset([1, 32, 35])
    FOLLOW_expr6_in_expr52389 = frozenset([1, 24, 43, 44, 46, 47, 48])
    FOLLOW_46_in_expr52406 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_24_in_expr52419 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_43_in_expr52432 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_44_in_expr52445 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_47_in_expr52458 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_48_in_expr52471 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr6_in_expr52485 = frozenset([1, 24, 43, 44, 46, 47, 48])
    FOLLOW_expr5_in_expr42513 = frozenset([1, 54, 55])
    FOLLOW_55_in_expr42535 = frozenset([54])
    FOLLOW_54_in_expr42548 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr5_in_expr42555 = frozenset([1])
    FOLLOW_55_in_expr32581 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 57])
    FOLLOW_expr4_in_expr32587 = frozenset([1])
    FOLLOW_expr4_in_expr32598 = frozenset([1])
    FOLLOW_expr3_in_expr22622 = frozenset([1, 51])
    FOLLOW_51_in_expr22633 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr3_in_expr22640 = frozenset([1, 51])
    FOLLOW_expr2_in_expr12668 = frozenset([1, 56])
    FOLLOW_56_in_expr12679 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr2_in_expr12686 = frozenset([1, 56])
    FOLLOW_generatorexpression_in_exprarg2710 = frozenset([1])
    FOLLOW_expr1_in_exprarg2719 = frozenset([1])
    FOLLOW_generatorexpression_in_expression2738 = frozenset([])
    FOLLOW_EOF_in_expression2740 = frozenset([1])
    FOLLOW_expr1_in_expression2749 = frozenset([])
    FOLLOW_EOF_in_expression2751 = frozenset([1])
    FOLLOW_nestedname_in_for_2776 = frozenset([54])
    FOLLOW_54_in_for_2780 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_for_2786 = frozenset([])
    FOLLOW_EOF_in_for_2792 = frozenset([1])
    FOLLOW_nestedname_in_statement2813 = frozenset([45])
    FOLLOW_45_in_statement2815 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2819 = frozenset([])
    FOLLOW_EOF_in_statement2821 = frozenset([1])
    FOLLOW_name_in_statement2830 = frozenset([33])
    FOLLOW_33_in_statement2832 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2836 = frozenset([])
    FOLLOW_EOF_in_statement2838 = frozenset([1])
    FOLLOW_name_in_statement2847 = frozenset([36])
    FOLLOW_36_in_statement2849 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2853 = frozenset([])
    FOLLOW_EOF_in_statement2855 = frozenset([1])
    FOLLOW_name_in_statement2864 = frozenset([31])
    FOLLOW_31_in_statement2866 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2870 = frozenset([])
    FOLLOW_EOF_in_statement2872 = frozenset([1])
    FOLLOW_name_in_statement2881 = frozenset([41])
    FOLLOW_41_in_statement2883 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2887 = frozenset([])
    FOLLOW_EOF_in_statement2889 = frozenset([1])
    FOLLOW_name_in_statement2898 = frozenset([40])
    FOLLOW_40_in_statement2900 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2904 = frozenset([])
    FOLLOW_EOF_in_statement2906 = frozenset([1])
    FOLLOW_name_in_statement2915 = frozenset([26])
    FOLLOW_26_in_statement2917 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_expr1_in_statement2921 = frozenset([])
    FOLLOW_EOF_in_statement2923 = frozenset([1])
    FOLLOW_list_in_synpred20_UL41385 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred21_UL41394 = frozenset([1])
    FOLLOW_dict_in_synpred22_UL41403 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred23_UL41412 = frozenset([1])
    FOLLOW_27_in_synpred24_UL41419 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 19, 27, 35, 49, 55, 57])
    FOLLOW_generatorexpression_in_synpred24_UL41423 = frozenset([28])
    FOLLOW_28_in_synpred24_UL41425 = frozenset([1])
    FOLLOW_27_in_synpred26_UL41470 = frozenset([14, 27])
    FOLLOW_nestedname_in_synpred26_UL41474 = frozenset([34])
    FOLLOW_34_in_synpred26_UL41476 = frozenset([28])
    FOLLOW_28_in_synpred26_UL41478 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred70_UL42710 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred71_UL42738 = frozenset([])
    FOLLOW_EOF_in_synpred71_UL42740 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
