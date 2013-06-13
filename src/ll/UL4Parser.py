# $ANTLR 3.4 src/ll/UL4.g 2013-06-13 14:22:44

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
STRING3=18
TIME=19
TRUE=20
UNICODE1_ESC=21
UNICODE2_ESC=22
UNICODE4_ESC=23
WS=24

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "BIN_DIGIT", "COLOR", "DATE", "DIGIT", "ESC_SEQ", "EXPONENT", "FALSE", 
    "FLOAT", "HEX_DIGIT", "INT", "NAME", "NONE", "OCT_DIGIT", "STRING", 
    "STRING3", "TIME", "TRUE", "UNICODE1_ESC", "UNICODE2_ESC", "UNICODE4_ESC", 
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

    def start(self, token):
    	return self.location.startcode + token.start

    def end(self, token):
    	return self.location.startcode + token.stop + 1



    # $ANTLR start "none"
    # src/ll/UL4.g:152:1: none returns [node] : NONE ;
    def none(self, ):
        node = None


        NONE1 = None

        try:
            try:
                # src/ll/UL4.g:153:2: ( NONE )
                # src/ll/UL4.g:153:4: NONE
                pass 
                NONE1 = self.match(self.input, NONE, self.FOLLOW_NONE_in_none746)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(NONE1), self.end(NONE1), None) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "none"



    # $ANTLR start "true_"
    # src/ll/UL4.g:156:1: true_ returns [node] : TRUE ;
    def true_(self, ):
        node = None


        TRUE2 = None

        try:
            try:
                # src/ll/UL4.g:157:2: ( TRUE )
                # src/ll/UL4.g:157:4: TRUE
                pass 
                TRUE2 = self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_763)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(TRUE2), self.end(TRUE2), True) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "true_"



    # $ANTLR start "false_"
    # src/ll/UL4.g:160:1: false_ returns [node] : FALSE ;
    def false_(self, ):
        node = None


        FALSE3 = None

        try:
            try:
                # src/ll/UL4.g:161:2: ( FALSE )
                # src/ll/UL4.g:161:4: FALSE
                pass 
                FALSE3 = self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_780)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(FALSE3), self.end(FALSE3), False) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "false_"



    # $ANTLR start "int_"
    # src/ll/UL4.g:164:1: int_ returns [node] : INT ;
    def int_(self, ):
        node = None


        INT4 = None

        try:
            try:
                # src/ll/UL4.g:165:2: ( INT )
                # src/ll/UL4.g:165:4: INT
                pass 
                INT4 = self.match(self.input, INT, self.FOLLOW_INT_in_int_797)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(INT4), self.end(INT4), int(INT4.text, 0)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "int_"



    # $ANTLR start "float_"
    # src/ll/UL4.g:168:1: float_ returns [node] : FLOAT ;
    def float_(self, ):
        node = None


        FLOAT5 = None

        try:
            try:
                # src/ll/UL4.g:169:2: ( FLOAT )
                # src/ll/UL4.g:169:4: FLOAT
                pass 
                FLOAT5 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_814)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(FLOAT5), self.end(FLOAT5), float(FLOAT5.text)) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "float_"



    # $ANTLR start "string"
    # src/ll/UL4.g:172:1: string returns [node] : ( STRING | STRING3 );
    def string(self, ):
        node = None


        STRING6 = None
        STRING37 = None

        try:
            try:
                # src/ll/UL4.g:173:2: ( STRING | STRING3 )
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
                    # src/ll/UL4.g:173:4: STRING
                    pass 
                    STRING6 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string831)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.location, self.start(STRING6), self.end(STRING6), ast.literal_eval(STRING6.text)) 




                elif alt1 == 2:
                    # src/ll/UL4.g:174:4: STRING3
                    pass 
                    STRING37 = self.match(self.input, STRING3, self.FOLLOW_STRING3_in_string838)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.location, self.start(STRING37), self.end(STRING37), ast.literal_eval(STRING37.text)) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "string"



    # $ANTLR start "date"
    # src/ll/UL4.g:177:1: date returns [node] : DATE ;
    def date(self, ):
        node = None


        DATE8 = None

        try:
            try:
                # src/ll/UL4.g:178:2: ( DATE )
                # src/ll/UL4.g:178:4: DATE
                pass 
                DATE8 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date855)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(DATE8), self.end(DATE8), datetime.datetime(*map(int, [f for f in ul4c.datesplitter.split(DATE8.text[2:-1]) if f]))) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "date"



    # $ANTLR start "color"
    # src/ll/UL4.g:181:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR9 = None

        try:
            try:
                # src/ll/UL4.g:182:2: ( COLOR )
                # src/ll/UL4.g:182:4: COLOR
                pass 
                COLOR9 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color872)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Const(self.location, self.start(COLOR9), self.end(COLOR9), color.Color.fromrepr(COLOR9.text)) 






                       
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
    # src/ll/UL4.g:185:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME10 = None

        try:
            try:
                # src/ll/UL4.g:186:2: ( NAME )
                # src/ll/UL4.g:186:4: NAME
                pass 
                NAME10 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name889)

                if self._state.backtracking == 0:
                    pass
                    retval.node = ul4c.Var(self.location, self.start(NAME10), self.end(NAME10), NAME10.text) 





                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "name"



    # $ANTLR start "literal"
    # src/ll/UL4.g:189:1: literal returns [node] : (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name );
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
                # src/ll/UL4.g:190:2: (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name )
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
                    # src/ll/UL4.g:190:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal908)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt2 == 2:
                    # src/ll/UL4.g:191:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal917)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt2 == 3:
                    # src/ll/UL4.g:192:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal926)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt2 == 4:
                    # src/ll/UL4.g:193:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal935)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt2 == 5:
                    # src/ll/UL4.g:194:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal944)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt2 == 6:
                    # src/ll/UL4.g:195:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal953)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt2 == 7:
                    # src/ll/UL4.g:196:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal962)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt2 == 8:
                    # src/ll/UL4.g:197:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal971)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt2 == 9:
                    # src/ll/UL4.g:198:4: e_name= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_literal980)
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
    # src/ll/UL4.g:202:1: list returns [node] : (open= '[' close= ']' |open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']' );
    def list(self, ):
        node = None


        open = None
        close = None
        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:203:2: (open= '[' close= ']' |open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']' )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 50) :
                    LA5_1 = self.input.LA(2)

                    if (LA5_1 == 51) :
                        alt5 = 1
                    elif ((COLOR <= LA5_1 <= DATE) or (FALSE <= LA5_1 <= FLOAT) or (INT <= LA5_1 <= NONE) or (STRING <= LA5_1 <= STRING3) or LA5_1 == TRUE or LA5_1 == 28 or LA5_1 == 36 or LA5_1 == 50 or LA5_1 == 56 or LA5_1 == 58) :
                        alt5 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 5, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 5, 0, self.input)

                    raise nvae


                if alt5 == 1:
                    # src/ll/UL4.g:204:3: open= '[' close= ']'
                    pass 
                    open = self.match(self.input, 50, self.FOLLOW_50_in_list1003)

                    close = self.match(self.input, 51, self.FOLLOW_51_in_list1009)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), self.end(close)) 




                elif alt5 == 2:
                    # src/ll/UL4.g:207:3: open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 50, self.FOLLOW_50_in_list1020)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_expr1_in_list1028)
                    e1 = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1) 



                    # src/ll/UL4.g:209:3: ( ',' e2= expr1 )*
                    while True: #loop3
                        alt3 = 2
                        LA3_0 = self.input.LA(1)

                        if (LA3_0 == 35) :
                            LA3_1 = self.input.LA(2)

                            if ((COLOR <= LA3_1 <= DATE) or (FALSE <= LA3_1 <= FLOAT) or (INT <= LA3_1 <= NONE) or (STRING <= LA3_1 <= STRING3) or LA3_1 == TRUE or LA3_1 == 28 or LA3_1 == 36 or LA3_1 == 50 or LA3_1 == 56 or LA3_1 == 58) :
                                alt3 = 1




                        if alt3 == 1:
                            # src/ll/UL4.g:210:4: ',' e2= expr1
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_list1039)

                            self._state.following.append(self.FOLLOW_expr1_in_list1046)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2) 




                        else:
                            break #loop3


                    # src/ll/UL4.g:213:3: ( ',' )?
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == 35) :
                        alt4 = 1
                    if alt4 == 1:
                        # src/ll/UL4.g:213:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_list1057)




                    close = self.match(self.input, 51, self.FOLLOW_51_in_list1064)

                    if self._state.backtracking == 0:
                        pass
                        node.end = self.end(close) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "list"



    # $ANTLR start "listcomprehension"
    # src/ll/UL4.g:217:1: listcomprehension returns [node] : open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']' ;
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
                # src/ll/UL4.g:222:2: (open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']' )
                # src/ll/UL4.g:223:3: open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']'
                pass 
                open = self.match(self.input, 50, self.FOLLOW_50_in_listcomprehension1092)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1098)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 53, self.FOLLOW_53_in_listcomprehension1102)

                self._state.following.append(self.FOLLOW_nestedname_in_listcomprehension1108)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_listcomprehension1112)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1118)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:229:3: ( 'if' condition= expr1 )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 54) :
                    alt6 = 1
                if alt6 == 1:
                    # src/ll/UL4.g:230:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_listcomprehension1127)

                    self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1134)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 51, self.FOLLOW_51_in_listcomprehension1147)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ListComp(self.location, self.start(open), self.end(close), item, ((n is not None) and [n.varname] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:238:1: fragment dictitem returns [node] : k= expr1 ':' v= expr1 ;
    def dictitem(self, ):
        node = None


        k = None

        v = None


        try:
            try:
                # src/ll/UL4.g:239:2: (k= expr1 ':' v= expr1 )
                # src/ll/UL4.g:240:3: k= expr1 ':' v= expr1
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_dictitem1172)
                k = self.expr1()

                self._state.following.pop()

                self.match(self.input, 43, self.FOLLOW_43_in_dictitem1176)

                self._state.following.append(self.FOLLOW_expr1_in_dictitem1182)
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
    # src/ll/UL4.g:245:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None

        i2 = None


        try:
            try:
                # src/ll/UL4.g:246:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 58) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 59) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or (STRING <= LA9_1 <= STRING3) or LA9_1 == TRUE or LA9_1 == 28 or LA9_1 == 36 or LA9_1 == 50 or LA9_1 == 56 or LA9_1 == 58) :
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
                    # src/ll/UL4.g:247:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 58, self.FOLLOW_58_in_dict1203)

                    close = self.match(self.input, 59, self.FOLLOW_59_in_dict1209)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), self.end(close)) 




                elif alt9 == 2:
                    # src/ll/UL4.g:250:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 58, self.FOLLOW_58_in_dict1220)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1228)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:252:3: ( ',' i2= dictitem )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 35) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or (STRING <= LA7_1 <= STRING3) or LA7_1 == TRUE or LA7_1 == 28 or LA7_1 == 36 or LA7_1 == 50 or LA7_1 == 56 or LA7_1 == 58) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:253:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_dict1239)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1246)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop7


                    # src/ll/UL4.g:256:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 35) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:256:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_dict1257)




                    close = self.match(self.input, 59, self.FOLLOW_59_in_dict1264)

                    if self._state.backtracking == 0:
                        pass
                        node.end = self.end(close) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dict"



    # $ANTLR start "dictcomprehension"
    # src/ll/UL4.g:260:1: dictcomprehension returns [node] : open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}' ;
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
                # src/ll/UL4.g:265:2: (open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}' )
                # src/ll/UL4.g:266:3: open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}'
                pass 
                open = self.match(self.input, 58, self.FOLLOW_58_in_dictcomprehension1292)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1298)
                key = self.expr1()

                self._state.following.pop()

                self.match(self.input, 43, self.FOLLOW_43_in_dictcomprehension1302)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1308)
                value = self.expr1()

                self._state.following.pop()

                self.match(self.input, 53, self.FOLLOW_53_in_dictcomprehension1312)

                self._state.following.append(self.FOLLOW_nestedname_in_dictcomprehension1318)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_dictcomprehension1322)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1328)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:274:3: ( 'if' condition= expr1 )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 54) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:275:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_dictcomprehension1337)

                    self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1344)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 59, self.FOLLOW_59_in_dictcomprehension1357)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.DictComp(self.location, self.start(open), self.end(close), key, value, ((n is not None) and [n.varname] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:281:1: generatorexpression returns [node] : item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ;
    def generatorexpression(self, ):
        node = None


        item = None

        n = None

        container = None

        condition = None


         
        _condition = None
        _end = None
        	
        try:
            try:
                # src/ll/UL4.g:287:2: (item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? )
                # src/ll/UL4.g:288:3: item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )?
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1385)
                item = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item.start 



                self.match(self.input, 53, self.FOLLOW_53_in_generatorexpression1391)

                self._state.following.append(self.FOLLOW_nestedname_in_generatorexpression1397)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_generatorexpression1401)

                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1407)
                container = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _end = container.end 



                # src/ll/UL4.g:293:3: ( 'if' condition= expr1 )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 54) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:294:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 54, self.FOLLOW_54_in_generatorexpression1418)

                    self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1425)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; _end = condition.end 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.GenExpr(self.location, item.start, _end, item, ((n is not None) and [n.varname] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:299:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr1 close= ')' );
    def atom(self, ):
        node = None


        open = None
        close = None
        e_literal = None

        e_list = None

        e_listcomp = None

        e_dict = None

        e_dictcomp = None

        e_genexpr = None

        e_bracket = None


        try:
            try:
                # src/ll/UL4.g:300:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr1 close= ')' )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == COLOR or LA12 == DATE or LA12 == FALSE or LA12 == FLOAT or LA12 == INT or LA12 == NAME or LA12 == NONE or LA12 == STRING or LA12 == STRING3 or LA12 == TRUE:
                    alt12 = 1
                elif LA12 == 50:
                    LA12_11 = self.input.LA(2)

                    if (self.synpred20_UL4()) :
                        alt12 = 2
                    elif (self.synpred21_UL4()) :
                        alt12 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 11, self.input)

                        raise nvae


                elif LA12 == 58:
                    LA12_12 = self.input.LA(2)

                    if (self.synpred22_UL4()) :
                        alt12 = 4
                    elif (self.synpred23_UL4()) :
                        alt12 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 12, 12, self.input)

                        raise nvae


                elif LA12 == 28:
                    LA12_13 = self.input.LA(2)

                    if (self.synpred24_UL4()) :
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
                    self._state.following.append(self.FOLLOW_literal_in_atom1451)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt12 == 2:
                    # src/ll/UL4.g:301:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1460)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt12 == 3:
                    # src/ll/UL4.g:302:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1469)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt12 == 4:
                    # src/ll/UL4.g:303:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1478)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt12 == 5:
                    # src/ll/UL4.g:304:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1487)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt12 == 6:
                    # src/ll/UL4.g:305:4: open= '(' e_genexpr= generatorexpression close= ')'
                    pass 
                    open = self.match(self.input, 28, self.FOLLOW_28_in_atom1496)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1500)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 29, self.FOLLOW_29_in_atom1504)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.start = self.start(open)
                        node.end = self.end(close)
                        	




                elif alt12 == 7:
                    # src/ll/UL4.g:310:4: open= '(' e_bracket= expr1 close= ')'
                    pass 
                    open = self.match(self.input, 28, self.FOLLOW_28_in_atom1513)

                    self._state.following.append(self.FOLLOW_expr1_in_atom1517)
                    e_bracket = self.expr1()

                    self._state.following.pop()

                    close = self.match(self.input, 29, self.FOLLOW_29_in_atom1521)

                    if self._state.backtracking == 0:
                        pass
                                                              
                        node = e_bracket
                        node.start = self.start(open)
                        node.end = self.end(close)
                        	





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "atom"


    class nestedname_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.nestedname_return, self).__init__()

            self.varname = None





    # $ANTLR start "nestedname"
    # src/ll/UL4.g:318:1: nestedname returns [varname] : (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' );
    def nestedname(self, ):
        retval = self.nestedname_return()
        retval.start = self.input.LT(1)


        n = None

        n0 = None

        n1 = None

        n2 = None

        n3 = None


        try:
            try:
                # src/ll/UL4.g:319:2: (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if (LA15_0 == NAME) :
                    alt15 = 1
                elif (LA15_0 == 28) :
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
                    # src/ll/UL4.g:320:3: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_nestedname1544)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.varname =  ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0] 




                elif alt15 == 2:
                    # src/ll/UL4.g:322:3: '(' n0= nestedname ',' ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1553)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1557)
                    n0 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 35, self.FOLLOW_35_in_nestedname1559)

                    self.match(self.input, 29, self.FOLLOW_29_in_nestedname1561)

                    if self._state.backtracking == 0:
                        pass
                        retval.varname = (((n0 is not None) and [n0.varname] or [None])[0],) 




                elif alt15 == 3:
                    # src/ll/UL4.g:324:3: '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 28, self.FOLLOW_28_in_nestedname1570)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1576)
                    n1 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 35, self.FOLLOW_35_in_nestedname1580)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1586)
                    n2 = self.nestedname()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.varname = (((n1 is not None) and [n1.varname] or [None])[0], ((n2 is not None) and [n2.varname] or [None])[0]) 



                    # src/ll/UL4.g:328:3: ( ',' n3= nestedname )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 35) :
                            LA13_1 = self.input.LA(2)

                            if (LA13_1 == NAME or LA13_1 == 28) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:329:4: ',' n3= nestedname
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_nestedname1597)

                            self._state.following.append(self.FOLLOW_nestedname_in_nestedname1604)
                            n3 = self.nestedname()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.varname += (((n3 is not None) and [n3.varname] or [None])[0],) 




                        else:
                            break #loop13


                    # src/ll/UL4.g:332:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 35) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:332:3: ','
                        pass 
                        self.match(self.input, 35, self.FOLLOW_35_in_nestedname1615)




                    self.match(self.input, 29, self.FOLLOW_29_in_nestedname1620)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedname"



    # $ANTLR start "expr9"
    # src/ll/UL4.g:337:1: expr9 returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )* ;
    def expr9(self, ):
        node = None


        close = None
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
                # src/ll/UL4.g:345:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )* )
                # src/ll/UL4.g:346:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr91649)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:347:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )*
                while True: #loop33
                    alt33 = 4
                    LA33 = self.input.LA(1)
                    if LA33 == 38:
                        alt33 = 1
                    elif LA33 == 28:
                        alt33 = 2
                    elif LA33 == 50:
                        alt33 = 3

                    if alt33 == 1:
                        # src/ll/UL4.g:349:4: '.' n= name
                        pass 
                        self.match(self.input, 38, self.FOLLOW_38_in_expr91665)

                        self._state.following.append(self.FOLLOW_name_in_expr91672)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.GetAttr(self.location, node.start, self.end(n.stop), node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt33 == 2:
                        # src/ll/UL4.g:353:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 28, self.FOLLOW_28_in_expr91688)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.CallMeth(self.location, node.start, None, node.obj, node.attrname) if isinstance(node, ul4c.GetAttr) else ul4c.CallFunc(self.location, node.start, None, node) 



                        # src/ll/UL4.g:354:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt28 = 5
                        LA28 = self.input.LA(1)
                        if LA28 == 29:
                            alt28 = 1
                        elif LA28 == 31:
                            alt28 = 2
                        elif LA28 == 30:
                            alt28 = 3
                        elif LA28 == COLOR or LA28 == DATE or LA28 == FALSE or LA28 == FLOAT or LA28 == INT or LA28 == NONE or LA28 == STRING or LA28 == STRING3 or LA28 == TRUE or LA28 == 28 or LA28 == 36 or LA28 == 50 or LA28 == 56 or LA28 == 58:
                            alt28 = 4
                        elif LA28 == NAME:
                            LA28_5 = self.input.LA(2)

                            if ((25 <= LA28_5 <= 26) or (28 <= LA28_5 <= 30) or LA28_5 == 33 or (35 <= LA28_5 <= 36) or (38 <= LA28_5 <= 40) or (44 <= LA28_5 <= 45) or (47 <= LA28_5 <= 50) or (52 <= LA28_5 <= 53) or (55 <= LA28_5 <= 57)) :
                                alt28 = 4
                            elif (LA28_5 == 46) :
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
                            # src/ll/UL4.g:356:4: 
                            pass 

                        elif alt28 == 2:
                            # src/ll/UL4.g:358:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 31, self.FOLLOW_31_in_expr91718)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91722)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:359:5: ( ',' )?
                            alt16 = 2
                            LA16_0 = self.input.LA(1)

                            if (LA16_0 == 35) :
                                alt16 = 1
                            if alt16 == 1:
                                # src/ll/UL4.g:359:5: ','
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91730)





                        elif alt28 == 3:
                            # src/ll/UL4.g:362:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 30, self.FOLLOW_30_in_expr91748)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91752)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remargs = rargs; 



                            # src/ll/UL4.g:363:5: ( ',' '**' rkwargs= exprarg )?
                            alt17 = 2
                            LA17_0 = self.input.LA(1)

                            if (LA17_0 == 35) :
                                LA17_1 = self.input.LA(2)

                                if (LA17_1 == 31) :
                                    alt17 = 1
                            if alt17 == 1:
                                # src/ll/UL4.g:364:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91767)

                                self.match(self.input, 31, self.FOLLOW_31_in_expr91774)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91778)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:367:5: ( ',' )?
                            alt18 = 2
                            LA18_0 = self.input.LA(1)

                            if (LA18_0 == 35) :
                                alt18 = 1
                            if alt18 == 1:
                                # src/ll/UL4.g:367:5: ','
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91793)





                        elif alt28 == 4:
                            # src/ll/UL4.g:370:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr91813)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.args.append(a1) 



                            # src/ll/UL4.g:371:5: ( ',' a2= exprarg )*
                            while True: #loop19
                                alt19 = 2
                                LA19_0 = self.input.LA(1)

                                if (LA19_0 == 35) :
                                    LA19_1 = self.input.LA(2)

                                    if (LA19_1 == NAME) :
                                        LA19_3 = self.input.LA(3)

                                        if ((25 <= LA19_3 <= 26) or (28 <= LA19_3 <= 30) or LA19_3 == 33 or (35 <= LA19_3 <= 36) or (38 <= LA19_3 <= 40) or (44 <= LA19_3 <= 45) or (47 <= LA19_3 <= 50) or (52 <= LA19_3 <= 53) or (55 <= LA19_3 <= 57)) :
                                            alt19 = 1


                                    elif ((COLOR <= LA19_1 <= DATE) or (FALSE <= LA19_1 <= FLOAT) or LA19_1 == INT or LA19_1 == NONE or (STRING <= LA19_1 <= STRING3) or LA19_1 == TRUE or LA19_1 == 28 or LA19_1 == 36 or LA19_1 == 50 or LA19_1 == 56 or LA19_1 == 58) :
                                        alt19 = 1




                                if alt19 == 1:
                                    # src/ll/UL4.g:372:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 35, self.FOLLOW_35_in_expr91828)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91837)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.args.append(a2) 




                                else:
                                    break #loop19


                            # src/ll/UL4.g:375:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop20
                                alt20 = 2
                                LA20_0 = self.input.LA(1)

                                if (LA20_0 == 35) :
                                    LA20_1 = self.input.LA(2)

                                    if (LA20_1 == NAME) :
                                        alt20 = 1




                                if alt20 == 1:
                                    # src/ll/UL4.g:376:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 35, self.FOLLOW_35_in_expr91859)

                                    self._state.following.append(self.FOLLOW_name_in_expr91868)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 46, self.FOLLOW_46_in_expr91870)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91874)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop20


                            # src/ll/UL4.g:379:5: ( ',' '*' rargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 35) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 30) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:380:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91896)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr91903)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91907)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:383:5: ( ',' '**' rkwargs= exprarg )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 35) :
                                LA22_1 = self.input.LA(2)

                                if (LA22_1 == 31) :
                                    alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:384:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91929)

                                self.match(self.input, 31, self.FOLLOW_31_in_expr91936)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91940)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:387:5: ( ',' )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 35) :
                                alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:387:5: ','
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr91955)





                        elif alt28 == 5:
                            # src/ll/UL4.g:390:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr91975)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 46, self.FOLLOW_46_in_expr91977)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91981)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:391:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop24
                                alt24 = 2
                                LA24_0 = self.input.LA(1)

                                if (LA24_0 == 35) :
                                    LA24_1 = self.input.LA(2)

                                    if (LA24_1 == NAME) :
                                        alt24 = 1




                                if alt24 == 1:
                                    # src/ll/UL4.g:392:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 35, self.FOLLOW_35_in_expr91996)

                                    self._state.following.append(self.FOLLOW_name_in_expr92005)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 46, self.FOLLOW_46_in_expr92007)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr92011)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop24


                            # src/ll/UL4.g:395:5: ( ',' '*' rargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 35) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 30) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:396:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr92033)

                                self.match(self.input, 30, self.FOLLOW_30_in_expr92040)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr92044)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:399:5: ( ',' '**' rkwargs= exprarg )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 35) :
                                LA26_1 = self.input.LA(2)

                                if (LA26_1 == 31) :
                                    alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:400:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr92066)

                                self.match(self.input, 31, self.FOLLOW_31_in_expr92073)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr92077)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:403:5: ( ',' )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 35) :
                                alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:403:5: ','
                                pass 
                                self.match(self.input, 35, self.FOLLOW_35_in_expr92092)







                        close = self.match(self.input, 29, self.FOLLOW_29_in_expr92105)

                        if self._state.backtracking == 0:
                            pass
                            node.end = self.end(close) 




                    elif alt33 == 3:
                        # src/ll/UL4.g:408:4: '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']'
                        pass 
                        self.match(self.input, 50, self.FOLLOW_50_in_expr92121)

                        # src/ll/UL4.g:409:4: ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 43) :
                            alt32 = 1
                        elif ((COLOR <= LA32_0 <= DATE) or (FALSE <= LA32_0 <= FLOAT) or (INT <= LA32_0 <= NONE) or (STRING <= LA32_0 <= STRING3) or LA32_0 == TRUE or LA32_0 == 28 or LA32_0 == 36 or LA32_0 == 50 or LA32_0 == 56 or LA32_0 == 58) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:410:5: ':' (e2= expr1 )?
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr92132)

                            # src/ll/UL4.g:411:5: (e2= expr1 )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or (STRING <= LA29_0 <= STRING3) or LA29_0 == TRUE or LA29_0 == 28 or LA29_0 == 36 or LA29_0 == 50 or LA29_0 == 56 or LA29_0 == 58) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:412:6: e2= expr1
                                pass 
                                self._state.following.append(self.FOLLOW_expr1_in_expr92147)
                                e2 = self.expr1()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(self.location, node.start, None, node, None, index2) 




                        elif alt32 == 2:
                            # src/ll/UL4.g:415:5: e2= expr1 ( ':' (e3= expr1 )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr1_in_expr92171)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:416:5: ( ':' (e3= expr1 )? )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 43) :
                                alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:417:6: ':' (e3= expr1 )?
                                pass 
                                self.match(self.input, 43, self.FOLLOW_43_in_expr92186)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:418:6: (e3= expr1 )?
                                alt30 = 2
                                LA30_0 = self.input.LA(1)

                                if ((COLOR <= LA30_0 <= DATE) or (FALSE <= LA30_0 <= FLOAT) or (INT <= LA30_0 <= NONE) or (STRING <= LA30_0 <= STRING3) or LA30_0 == TRUE or LA30_0 == 28 or LA30_0 == 36 or LA30_0 == 50 or LA30_0 == 56 or LA30_0 == 58) :
                                    alt30 = 1
                                if alt30 == 1:
                                    # src/ll/UL4.g:419:7: e3= expr1
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr1_in_expr92205)
                                    e3 = self.expr1()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(self.location, node.start, None, node, index1, index2) if slice else ul4c.GetItem(self.location, e1.start, None, node, index1) 






                        close = self.match(self.input, 51, self.FOLLOW_51_in_expr92236)

                        if self._state.backtracking == 0:
                            pass
                            node.end = self.end(close) 




                    else:
                        break #loop33





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr9"



    # $ANTLR start "expr8"
    # src/ll/UL4.g:428:1: expr8 returns [node] : (e1= expr9 |minus= '-' e2= expr8 );
    def expr8(self, ):
        node = None


        minus = None
        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:429:2: (e1= expr9 |minus= '-' e2= expr8 )
                alt34 = 2
                LA34_0 = self.input.LA(1)

                if ((COLOR <= LA34_0 <= DATE) or (FALSE <= LA34_0 <= FLOAT) or (INT <= LA34_0 <= NONE) or (STRING <= LA34_0 <= STRING3) or LA34_0 == TRUE or LA34_0 == 28 or LA34_0 == 50 or LA34_0 == 58) :
                    alt34 = 1
                elif (LA34_0 == 36) :
                    alt34 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae


                if alt34 == 1:
                    # src/ll/UL4.g:430:3: e1= expr9
                    pass 
                    self._state.following.append(self.FOLLOW_expr9_in_expr82264)
                    e1 = self.expr9()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt34 == 2:
                    # src/ll/UL4.g:432:3: minus= '-' e2= expr8
                    pass 
                    minus = self.match(self.input, 36, self.FOLLOW_36_in_expr82275)

                    self._state.following.append(self.FOLLOW_expr8_in_expr82279)
                    e2 = self.expr8()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.location, self.start(minus), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr8"



    # $ANTLR start "expr7"
    # src/ll/UL4.g:436:1: expr7 returns [node] : e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* ;
    def expr7(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:437:2: (e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* )
                # src/ll/UL4.g:438:3: e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                pass 
                self._state.following.append(self.FOLLOW_expr8_in_expr72302)
                e1 = self.expr8()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:439:3: ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 26 or LA36_0 == 30 or (39 <= LA36_0 <= 40)) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:440:4: ( '*' | '/' | '//' | '%' ) e2= expr8
                        pass 
                        # src/ll/UL4.g:440:4: ( '*' | '/' | '//' | '%' )
                        alt35 = 4
                        LA35 = self.input.LA(1)
                        if LA35 == 30:
                            alt35 = 1
                        elif LA35 == 39:
                            alt35 = 2
                        elif LA35 == 40:
                            alt35 = 3
                        elif LA35 == 26:
                            alt35 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 35, 0, self.input)

                            raise nvae


                        if alt35 == 1:
                            # src/ll/UL4.g:441:5: '*'
                            pass 
                            self.match(self.input, 30, self.FOLLOW_30_in_expr72319)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:443:5: '/'
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_expr72332)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt35 == 3:
                            # src/ll/UL4.g:445:5: '//'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr72345)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt35 == 4:
                            # src/ll/UL4.g:447:5: '%'
                            pass 
                            self.match(self.input, 26, self.FOLLOW_26_in_expr72358)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr8_in_expr72372)
                        e2 = self.expr8()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop36





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr7"



    # $ANTLR start "expr6"
    # src/ll/UL4.g:454:1: expr6 returns [node] : e1= expr7 ( ( '+' | '-' ) e2= expr7 )* ;
    def expr6(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:455:2: (e1= expr7 ( ( '+' | '-' ) e2= expr7 )* )
                # src/ll/UL4.g:456:3: e1= expr7 ( ( '+' | '-' ) e2= expr7 )*
                pass 
                self._state.following.append(self.FOLLOW_expr7_in_expr62400)
                e1 = self.expr7()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:457:3: ( ( '+' | '-' ) e2= expr7 )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 33 or LA38_0 == 36) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:458:4: ( '+' | '-' ) e2= expr7
                        pass 
                        # src/ll/UL4.g:458:4: ( '+' | '-' )
                        alt37 = 2
                        LA37_0 = self.input.LA(1)

                        if (LA37_0 == 33) :
                            alt37 = 1
                        elif (LA37_0 == 36) :
                            alt37 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:459:5: '+'
                            pass 
                            self.match(self.input, 33, self.FOLLOW_33_in_expr62417)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:461:5: '-'
                            pass 
                            self.match(self.input, 36, self.FOLLOW_36_in_expr62430)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr7_in_expr62444)
                        e2 = self.expr7()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop38





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr6"



    # $ANTLR start "expr5"
    # src/ll/UL4.g:468:1: expr5 returns [node] : e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* ;
    def expr5(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:469:2: (e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* )
                # src/ll/UL4.g:470:3: e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                pass 
                self._state.following.append(self.FOLLOW_expr6_in_expr52472)
                e1 = self.expr6()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:471:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 25 or (44 <= LA40_0 <= 45) or (47 <= LA40_0 <= 49)) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:472:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6
                        pass 
                        # src/ll/UL4.g:472:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt39 = 6
                        LA39 = self.input.LA(1)
                        if LA39 == 47:
                            alt39 = 1
                        elif LA39 == 25:
                            alt39 = 2
                        elif LA39 == 44:
                            alt39 = 3
                        elif LA39 == 45:
                            alt39 = 4
                        elif LA39 == 48:
                            alt39 = 5
                        elif LA39 == 49:
                            alt39 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:473:5: '=='
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr52489)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:475:5: '!='
                            pass 
                            self.match(self.input, 25, self.FOLLOW_25_in_expr52502)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt39 == 3:
                            # src/ll/UL4.g:477:5: '<'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr52515)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt39 == 4:
                            # src/ll/UL4.g:479:5: '<='
                            pass 
                            self.match(self.input, 45, self.FOLLOW_45_in_expr52528)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt39 == 5:
                            # src/ll/UL4.g:481:5: '>'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr52541)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt39 == 6:
                            # src/ll/UL4.g:483:5: '>='
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr52554)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr6_in_expr52568)
                        e2 = self.expr6()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop40





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr5"



    # $ANTLR start "expr4"
    # src/ll/UL4.g:490:1: expr4 returns [node] : e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? ;
    def expr4(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:491:2: (e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? )
                # src/ll/UL4.g:492:3: e1= expr5 ( ( 'not' )? 'in' e2= expr5 )?
                pass 
                self._state.following.append(self.FOLLOW_expr5_in_expr42596)
                e1 = self.expr5()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = e1 



                # src/ll/UL4.g:493:3: ( ( 'not' )? 'in' e2= expr5 )?
                alt42 = 2
                LA42_0 = self.input.LA(1)

                if ((55 <= LA42_0 <= 56)) :
                    alt42 = 1
                if alt42 == 1:
                    # src/ll/UL4.g:494:4: ( 'not' )? 'in' e2= expr5
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains 



                    # src/ll/UL4.g:495:4: ( 'not' )?
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 56) :
                        alt41 = 1
                    if alt41 == 1:
                        # src/ll/UL4.g:496:5: 'not'
                        pass 
                        self.match(self.input, 56, self.FOLLOW_56_in_expr42618)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains 






                    self.match(self.input, 55, self.FOLLOW_55_in_expr42631)

                    self._state.following.append(self.FOLLOW_expr5_in_expr42638)
                    e2 = self.expr5()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = cls.make(self.location, node.start, e2.end, node, e2) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr4"



    # $ANTLR start "expr3"
    # src/ll/UL4.g:504:1: expr3 returns [node] : (e1= expr4 |n= 'not' e2= expr3 );
    def expr3(self, ):
        node = None


        n = None
        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:505:2: (e1= expr4 |n= 'not' e2= expr3 )
                alt43 = 2
                LA43_0 = self.input.LA(1)

                if ((COLOR <= LA43_0 <= DATE) or (FALSE <= LA43_0 <= FLOAT) or (INT <= LA43_0 <= NONE) or (STRING <= LA43_0 <= STRING3) or LA43_0 == TRUE or LA43_0 == 28 or LA43_0 == 36 or LA43_0 == 50 or LA43_0 == 58) :
                    alt43 = 1
                elif (LA43_0 == 56) :
                    alt43 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 43, 0, self.input)

                    raise nvae


                if alt43 == 1:
                    # src/ll/UL4.g:506:3: e1= expr4
                    pass 
                    self._state.following.append(self.FOLLOW_expr4_in_expr32666)
                    e1 = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt43 == 2:
                    # src/ll/UL4.g:508:3: n= 'not' e2= expr3
                    pass 
                    n = self.match(self.input, 56, self.FOLLOW_56_in_expr32677)

                    self._state.following.append(self.FOLLOW_expr3_in_expr32681)
                    e2 = self.expr3()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(self.location, self.start(n), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr3"



    # $ANTLR start "expr2"
    # src/ll/UL4.g:513:1: expr2 returns [node] : e1= expr3 ( 'and' e2= expr3 )* ;
    def expr2(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:514:2: (e1= expr3 ( 'and' e2= expr3 )* )
                # src/ll/UL4.g:515:3: e1= expr3 ( 'and' e2= expr3 )*
                pass 
                self._state.following.append(self.FOLLOW_expr3_in_expr22705)
                e1 = self.expr3()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:516:3: ( 'and' e2= expr3 )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 52) :
                        alt44 = 1


                    if alt44 == 1:
                        # src/ll/UL4.g:517:4: 'and' e2= expr3
                        pass 
                        self.match(self.input, 52, self.FOLLOW_52_in_expr22716)

                        self._state.following.append(self.FOLLOW_expr3_in_expr22723)
                        e2 = self.expr3()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop44





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr2"



    # $ANTLR start "expr1"
    # src/ll/UL4.g:523:1: expr1 returns [node] : e1= expr2 ( 'or' e2= expr2 )* ;
    def expr1(self, ):
        node = None


        e1 = None

        e2 = None


        try:
            try:
                # src/ll/UL4.g:524:2: (e1= expr2 ( 'or' e2= expr2 )* )
                # src/ll/UL4.g:525:3: e1= expr2 ( 'or' e2= expr2 )*
                pass 
                self._state.following.append(self.FOLLOW_expr2_in_expr12751)
                e1 = self.expr2()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:526:3: ( 'or' e2= expr2 )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 57) :
                        alt45 = 1


                    if alt45 == 1:
                        # src/ll/UL4.g:527:4: 'or' e2= expr2
                        pass 
                        self.match(self.input, 57, self.FOLLOW_57_in_expr12762)

                        self._state.following.append(self.FOLLOW_expr2_in_expr12769)
                        e2 = self.expr2()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop45





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr1"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:532:1: exprarg returns [node] : (ege= generatorexpression |e1= expr1 );
    def exprarg(self, ):
        node = None


        ege = None

        e1 = None


        try:
            try:
                # src/ll/UL4.g:533:2: (ege= generatorexpression |e1= expr1 )
                alt46 = 2
                LA46 = self.input.LA(1)
                if LA46 == NONE:
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


                elif LA46 == FALSE:
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


                elif LA46 == TRUE:
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


                elif LA46 == INT:
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


                elif LA46 == FLOAT:
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


                elif LA46 == STRING:
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


                elif LA46 == STRING3:
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


                elif LA46 == DATE:
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


                elif LA46 == COLOR:
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


                elif LA46 == NAME:
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


                elif LA46 == 50:
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


                elif LA46 == 58:
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


                elif LA46 == 28:
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


                elif LA46 == 36:
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


                elif LA46 == 56:
                    LA46_15 = self.input.LA(2)

                    if (self.synpred70_UL4()) :
                        alt46 = 1
                    elif (True) :
                        alt46 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 46, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 46, 0, self.input)

                    raise nvae


                if alt46 == 1:
                    # src/ll/UL4.g:533:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2793)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:534:4: e1= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_exprarg2802)
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
    # src/ll/UL4.g:537:1: expression returns [node] : (ege= generatorexpression EOF |e= expr1 EOF );
    def expression(self, ):
        node = None


        ege = None

        e = None


        try:
            try:
                # src/ll/UL4.g:538:2: (ege= generatorexpression EOF |e= expr1 EOF )
                alt47 = 2
                LA47 = self.input.LA(1)
                if LA47 == NONE:
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


                elif LA47 == FALSE:
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


                elif LA47 == TRUE:
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


                elif LA47 == INT:
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


                elif LA47 == FLOAT:
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


                elif LA47 == STRING:
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


                elif LA47 == STRING3:
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


                elif LA47 == DATE:
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


                elif LA47 == COLOR:
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


                elif LA47 == NAME:
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


                elif LA47 == 50:
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


                elif LA47 == 58:
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


                elif LA47 == 28:
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


                elif LA47 == 36:
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


                elif LA47 == 56:
                    LA47_15 = self.input.LA(2)

                    if (self.synpred71_UL4()) :
                        alt47 = 1
                    elif (True) :
                        alt47 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 47, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 47, 0, self.input)

                    raise nvae


                if alt47 == 1:
                    # src/ll/UL4.g:538:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression2821)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2823)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt47 == 2:
                    # src/ll/UL4.g:539:4: e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_expression2832)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2834)

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
    # src/ll/UL4.g:545:1: for_ returns [node] : n= nestedname 'in' e= expr1 EOF ;
    def for_(self, ):
        node = None


        n = None

        e = None


        try:
            try:
                # src/ll/UL4.g:546:2: (n= nestedname 'in' e= expr1 EOF )
                # src/ll/UL4.g:547:3: n= nestedname 'in' e= expr1 EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedname_in_for_2859)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_for_2863)

                self._state.following.append(self.FOLLOW_expr1_in_for_2869)
                e = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.For(self.location, self.start(n.start), e.end, ((n is not None) and [n.varname] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_2875)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:556:1: statement returns [node] : (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None

        e = None

        n = None


        try:
            try:
                # src/ll/UL4.g:557:2: (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF )
                alt48 = 8
                LA48 = self.input.LA(1)
                if LA48 == NAME:
                    LA48_1 = self.input.LA(2)

                    if (self.synpred72_UL4()) :
                        alt48 = 1
                    elif (self.synpred73_UL4()) :
                        alt48 = 2
                    elif (self.synpred74_UL4()) :
                        alt48 = 3
                    elif (self.synpred75_UL4()) :
                        alt48 = 4
                    elif (self.synpred76_UL4()) :
                        alt48 = 5
                    elif (self.synpred77_UL4()) :
                        alt48 = 6
                    elif (self.synpred78_UL4()) :
                        alt48 = 7
                    elif (True) :
                        alt48 = 8
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 48, 1, self.input)

                        raise nvae


                elif LA48 == 28:
                    LA48_2 = self.input.LA(2)

                    if (self.synpred72_UL4()) :
                        alt48 = 1
                    elif (True) :
                        alt48 = 8
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 48, 2, self.input)

                        raise nvae


                elif LA48 == COLOR or LA48 == DATE or LA48 == FALSE or LA48 == FLOAT or LA48 == INT or LA48 == NONE or LA48 == STRING or LA48 == STRING3 or LA48 == TRUE or LA48 == 36 or LA48 == 50 or LA48 == 56 or LA48 == 58:
                    alt48 = 8
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 48, 0, self.input)

                    raise nvae


                if alt48 == 1:
                    # src/ll/UL4.g:557:4: nn= nestedname '=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedname_in_statement2896)
                    nn = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement2898)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2902)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2904)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.StoreVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.varname] or [None])[0], e) 




                elif alt48 == 2:
                    # src/ll/UL4.g:558:4: n= name '+=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2913)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_statement2915)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2919)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2921)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 3:
                    # src/ll/UL4.g:559:4: n= name '-=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2930)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_statement2932)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2936)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2938)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 4:
                    # src/ll/UL4.g:560:4: n= name '*=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2947)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 32, self.FOLLOW_32_in_statement2949)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2953)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2955)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 5:
                    # src/ll/UL4.g:561:4: n= name '/=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2964)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 42, self.FOLLOW_42_in_statement2966)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2970)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2972)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 6:
                    # src/ll/UL4.g:562:4: n= name '//=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2981)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement2983)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2987)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2989)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 7:
                    # src/ll/UL4.g:563:4: n= name '%=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2998)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 27, self.FOLLOW_27_in_statement3000)

                    self._state.following.append(self.FOLLOW_expr1_in_statement3004)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3006)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 8:
                    # src/ll/UL4.g:564:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3015)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3017)

                    if self._state.backtracking == 0:
                        pass
                        node = e 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "statement"

    # $ANTLR start "synpred20_UL4"
    def synpred20_UL4_fragment(self, ):
        e_list = None


        # src/ll/UL4.g:301:4: (e_list= list )
        # src/ll/UL4.g:301:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred20_UL41460)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred20_UL4"



    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_listcomp = None


        # src/ll/UL4.g:302:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:302:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred21_UL41469)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_dict = None


        # src/ll/UL4.g:303:4: (e_dict= dict )
        # src/ll/UL4.g:303:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred22_UL41478)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_dictcomp = None


        # src/ll/UL4.g:304:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:304:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred23_UL41487)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred23_UL4"



    # $ANTLR start "synpred24_UL4"
    def synpred24_UL4_fragment(self, ):
        open = None
        close = None
        e_genexpr = None


        # src/ll/UL4.g:305:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:305:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 28, self.FOLLOW_28_in_synpred24_UL41496)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred24_UL41500)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 29, self.FOLLOW_29_in_synpred24_UL41504)



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        n0 = None


        # src/ll/UL4.g:322:3: ( '(' n0= nestedname ',' ')' )
        # src/ll/UL4.g:322:3: '(' n0= nestedname ',' ')'
        pass 
        self.match(self.input, 28, self.FOLLOW_28_in_synpred26_UL41553)

        self._state.following.append(self.FOLLOW_nestedname_in_synpred26_UL41557)
        n0 = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 35, self.FOLLOW_35_in_synpred26_UL41559)

        self.match(self.input, 29, self.FOLLOW_29_in_synpred26_UL41561)



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred70_UL4"
    def synpred70_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:533:4: (ege= generatorexpression )
        # src/ll/UL4.g:533:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred70_UL42793)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred70_UL4"



    # $ANTLR start "synpred71_UL4"
    def synpred71_UL4_fragment(self, ):
        ege = None


        # src/ll/UL4.g:538:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:538:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred71_UL42821)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred71_UL42823)



    # $ANTLR end "synpred71_UL4"



    # $ANTLR start "synpred72_UL4"
    def synpred72_UL4_fragment(self, ):
        nn = None

        e = None


        # src/ll/UL4.g:557:4: (nn= nestedname '=' e= expr1 EOF )
        # src/ll/UL4.g:557:4: nn= nestedname '=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedname_in_synpred72_UL42896)
        nn = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred72_UL42898)

        self._state.following.append(self.FOLLOW_expr1_in_synpred72_UL42902)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred72_UL42904)



    # $ANTLR end "synpred72_UL4"



    # $ANTLR start "synpred73_UL4"
    def synpred73_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:558:4: (n= name '+=' e= expr1 EOF )
        # src/ll/UL4.g:558:4: n= name '+=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred73_UL42913)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 34, self.FOLLOW_34_in_synpred73_UL42915)

        self._state.following.append(self.FOLLOW_expr1_in_synpred73_UL42919)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred73_UL42921)



    # $ANTLR end "synpred73_UL4"



    # $ANTLR start "synpred74_UL4"
    def synpred74_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:559:4: (n= name '-=' e= expr1 EOF )
        # src/ll/UL4.g:559:4: n= name '-=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred74_UL42930)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 37, self.FOLLOW_37_in_synpred74_UL42932)

        self._state.following.append(self.FOLLOW_expr1_in_synpred74_UL42936)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred74_UL42938)



    # $ANTLR end "synpred74_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:560:4: (n= name '*=' e= expr1 EOF )
        # src/ll/UL4.g:560:4: n= name '*=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred75_UL42947)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 32, self.FOLLOW_32_in_synpred75_UL42949)

        self._state.following.append(self.FOLLOW_expr1_in_synpred75_UL42953)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred75_UL42955)



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:561:4: (n= name '/=' e= expr1 EOF )
        # src/ll/UL4.g:561:4: n= name '/=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred76_UL42964)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 42, self.FOLLOW_42_in_synpred76_UL42966)

        self._state.following.append(self.FOLLOW_expr1_in_synpred76_UL42970)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred76_UL42972)



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:562:4: (n= name '//=' e= expr1 EOF )
        # src/ll/UL4.g:562:4: n= name '//=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred77_UL42981)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred77_UL42983)

        self._state.following.append(self.FOLLOW_expr1_in_synpred77_UL42987)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL42989)



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        n = None

        e = None


        # src/ll/UL4.g:563:4: (n= name '%=' e= expr1 EOF )
        # src/ll/UL4.g:563:4: n= name '%=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred78_UL42998)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 27, self.FOLLOW_27_in_synpred78_UL43000)

        self._state.following.append(self.FOLLOW_expr1_in_synpred78_UL43004)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43006)



    # $ANTLR end "synpred78_UL4"




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



 

    FOLLOW_NONE_in_none746 = frozenset([1])
    FOLLOW_TRUE_in_true_763 = frozenset([1])
    FOLLOW_FALSE_in_false_780 = frozenset([1])
    FOLLOW_INT_in_int_797 = frozenset([1])
    FOLLOW_FLOAT_in_float_814 = frozenset([1])
    FOLLOW_STRING_in_string831 = frozenset([1])
    FOLLOW_STRING3_in_string838 = frozenset([1])
    FOLLOW_DATE_in_date855 = frozenset([1])
    FOLLOW_COLOR_in_color872 = frozenset([1])
    FOLLOW_NAME_in_name889 = frozenset([1])
    FOLLOW_none_in_literal908 = frozenset([1])
    FOLLOW_false__in_literal917 = frozenset([1])
    FOLLOW_true__in_literal926 = frozenset([1])
    FOLLOW_int__in_literal935 = frozenset([1])
    FOLLOW_float__in_literal944 = frozenset([1])
    FOLLOW_string_in_literal953 = frozenset([1])
    FOLLOW_date_in_literal962 = frozenset([1])
    FOLLOW_color_in_literal971 = frozenset([1])
    FOLLOW_name_in_literal980 = frozenset([1])
    FOLLOW_50_in_list1003 = frozenset([51])
    FOLLOW_51_in_list1009 = frozenset([1])
    FOLLOW_50_in_list1020 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_list1028 = frozenset([35, 51])
    FOLLOW_35_in_list1039 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_list1046 = frozenset([35, 51])
    FOLLOW_35_in_list1057 = frozenset([51])
    FOLLOW_51_in_list1064 = frozenset([1])
    FOLLOW_50_in_listcomprehension1092 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1098 = frozenset([53])
    FOLLOW_53_in_listcomprehension1102 = frozenset([14, 28])
    FOLLOW_nestedname_in_listcomprehension1108 = frozenset([55])
    FOLLOW_55_in_listcomprehension1112 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1118 = frozenset([51, 54])
    FOLLOW_54_in_listcomprehension1127 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_listcomprehension1134 = frozenset([51])
    FOLLOW_51_in_listcomprehension1147 = frozenset([1])
    FOLLOW_expr1_in_dictitem1172 = frozenset([43])
    FOLLOW_43_in_dictitem1176 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictitem1182 = frozenset([1])
    FOLLOW_58_in_dict1203 = frozenset([59])
    FOLLOW_59_in_dict1209 = frozenset([1])
    FOLLOW_58_in_dict1220 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_dictitem_in_dict1228 = frozenset([35, 59])
    FOLLOW_35_in_dict1239 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_dictitem_in_dict1246 = frozenset([35, 59])
    FOLLOW_35_in_dict1257 = frozenset([59])
    FOLLOW_59_in_dict1264 = frozenset([1])
    FOLLOW_58_in_dictcomprehension1292 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1298 = frozenset([43])
    FOLLOW_43_in_dictcomprehension1302 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1308 = frozenset([53])
    FOLLOW_53_in_dictcomprehension1312 = frozenset([14, 28])
    FOLLOW_nestedname_in_dictcomprehension1318 = frozenset([55])
    FOLLOW_55_in_dictcomprehension1322 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1328 = frozenset([54, 59])
    FOLLOW_54_in_dictcomprehension1337 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_dictcomprehension1344 = frozenset([59])
    FOLLOW_59_in_dictcomprehension1357 = frozenset([1])
    FOLLOW_expr1_in_generatorexpression1385 = frozenset([53])
    FOLLOW_53_in_generatorexpression1391 = frozenset([14, 28])
    FOLLOW_nestedname_in_generatorexpression1397 = frozenset([55])
    FOLLOW_55_in_generatorexpression1401 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_generatorexpression1407 = frozenset([1, 54])
    FOLLOW_54_in_generatorexpression1418 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_generatorexpression1425 = frozenset([1])
    FOLLOW_literal_in_atom1451 = frozenset([1])
    FOLLOW_list_in_atom1460 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1469 = frozenset([1])
    FOLLOW_dict_in_atom1478 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1487 = frozenset([1])
    FOLLOW_28_in_atom1496 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_generatorexpression_in_atom1500 = frozenset([29])
    FOLLOW_29_in_atom1504 = frozenset([1])
    FOLLOW_28_in_atom1513 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_atom1517 = frozenset([29])
    FOLLOW_29_in_atom1521 = frozenset([1])
    FOLLOW_name_in_nestedname1544 = frozenset([1])
    FOLLOW_28_in_nestedname1553 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1557 = frozenset([35])
    FOLLOW_35_in_nestedname1559 = frozenset([29])
    FOLLOW_29_in_nestedname1561 = frozenset([1])
    FOLLOW_28_in_nestedname1570 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1576 = frozenset([35])
    FOLLOW_35_in_nestedname1580 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1586 = frozenset([29, 35])
    FOLLOW_35_in_nestedname1597 = frozenset([14, 28])
    FOLLOW_nestedname_in_nestedname1604 = frozenset([29, 35])
    FOLLOW_35_in_nestedname1615 = frozenset([29])
    FOLLOW_29_in_nestedname1620 = frozenset([1])
    FOLLOW_atom_in_expr91649 = frozenset([1, 28, 38, 50])
    FOLLOW_38_in_expr91665 = frozenset([14])
    FOLLOW_name_in_expr91672 = frozenset([1, 28, 38, 50])
    FOLLOW_28_in_expr91688 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 29, 30, 31, 36, 50, 56, 58])
    FOLLOW_31_in_expr91718 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91722 = frozenset([29, 35])
    FOLLOW_35_in_expr91730 = frozenset([29])
    FOLLOW_30_in_expr91748 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91752 = frozenset([29, 35])
    FOLLOW_35_in_expr91767 = frozenset([31])
    FOLLOW_31_in_expr91774 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91778 = frozenset([29, 35])
    FOLLOW_35_in_expr91793 = frozenset([29])
    FOLLOW_exprarg_in_expr91813 = frozenset([29, 35])
    FOLLOW_35_in_expr91828 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91837 = frozenset([29, 35])
    FOLLOW_35_in_expr91859 = frozenset([14])
    FOLLOW_name_in_expr91868 = frozenset([46])
    FOLLOW_46_in_expr91870 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91874 = frozenset([29, 35])
    FOLLOW_35_in_expr91896 = frozenset([30])
    FOLLOW_30_in_expr91903 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91907 = frozenset([29, 35])
    FOLLOW_35_in_expr91929 = frozenset([31])
    FOLLOW_31_in_expr91936 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91940 = frozenset([29, 35])
    FOLLOW_35_in_expr91955 = frozenset([29])
    FOLLOW_name_in_expr91975 = frozenset([46])
    FOLLOW_46_in_expr91977 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr91981 = frozenset([29, 35])
    FOLLOW_35_in_expr91996 = frozenset([14])
    FOLLOW_name_in_expr92005 = frozenset([46])
    FOLLOW_46_in_expr92007 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr92011 = frozenset([29, 35])
    FOLLOW_35_in_expr92033 = frozenset([30])
    FOLLOW_30_in_expr92040 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr92044 = frozenset([29, 35])
    FOLLOW_35_in_expr92066 = frozenset([31])
    FOLLOW_31_in_expr92073 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_exprarg_in_expr92077 = frozenset([29, 35])
    FOLLOW_35_in_expr92092 = frozenset([29])
    FOLLOW_29_in_expr92105 = frozenset([1, 28, 38, 50])
    FOLLOW_50_in_expr92121 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 43, 50, 56, 58])
    FOLLOW_43_in_expr92132 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 51, 56, 58])
    FOLLOW_expr1_in_expr92147 = frozenset([51])
    FOLLOW_expr1_in_expr92171 = frozenset([43, 51])
    FOLLOW_43_in_expr92186 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 51, 56, 58])
    FOLLOW_expr1_in_expr92205 = frozenset([51])
    FOLLOW_51_in_expr92236 = frozenset([1, 28, 38, 50])
    FOLLOW_expr9_in_expr82264 = frozenset([1])
    FOLLOW_36_in_expr82275 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_expr8_in_expr82279 = frozenset([1])
    FOLLOW_expr8_in_expr72302 = frozenset([1, 26, 30, 39, 40])
    FOLLOW_30_in_expr72319 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_39_in_expr72332 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_40_in_expr72345 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_26_in_expr72358 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_expr8_in_expr72372 = frozenset([1, 26, 30, 39, 40])
    FOLLOW_expr7_in_expr62400 = frozenset([1, 33, 36])
    FOLLOW_33_in_expr62417 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_36_in_expr62430 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_expr7_in_expr62444 = frozenset([1, 33, 36])
    FOLLOW_expr6_in_expr52472 = frozenset([1, 25, 44, 45, 47, 48, 49])
    FOLLOW_47_in_expr52489 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_25_in_expr52502 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_44_in_expr52515 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_45_in_expr52528 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_48_in_expr52541 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_49_in_expr52554 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_expr6_in_expr52568 = frozenset([1, 25, 44, 45, 47, 48, 49])
    FOLLOW_expr5_in_expr42596 = frozenset([1, 55, 56])
    FOLLOW_56_in_expr42618 = frozenset([55])
    FOLLOW_55_in_expr42631 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 58])
    FOLLOW_expr5_in_expr42638 = frozenset([1])
    FOLLOW_expr4_in_expr32666 = frozenset([1])
    FOLLOW_56_in_expr32677 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr3_in_expr32681 = frozenset([1])
    FOLLOW_expr3_in_expr22705 = frozenset([1, 52])
    FOLLOW_52_in_expr22716 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr3_in_expr22723 = frozenset([1, 52])
    FOLLOW_expr2_in_expr12751 = frozenset([1, 57])
    FOLLOW_57_in_expr12762 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr2_in_expr12769 = frozenset([1, 57])
    FOLLOW_generatorexpression_in_exprarg2793 = frozenset([1])
    FOLLOW_expr1_in_exprarg2802 = frozenset([1])
    FOLLOW_generatorexpression_in_expression2821 = frozenset([])
    FOLLOW_EOF_in_expression2823 = frozenset([1])
    FOLLOW_expr1_in_expression2832 = frozenset([])
    FOLLOW_EOF_in_expression2834 = frozenset([1])
    FOLLOW_nestedname_in_for_2859 = frozenset([55])
    FOLLOW_55_in_for_2863 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_for_2869 = frozenset([])
    FOLLOW_EOF_in_for_2875 = frozenset([1])
    FOLLOW_nestedname_in_statement2896 = frozenset([46])
    FOLLOW_46_in_statement2898 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2902 = frozenset([])
    FOLLOW_EOF_in_statement2904 = frozenset([1])
    FOLLOW_name_in_statement2913 = frozenset([34])
    FOLLOW_34_in_statement2915 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2919 = frozenset([])
    FOLLOW_EOF_in_statement2921 = frozenset([1])
    FOLLOW_name_in_statement2930 = frozenset([37])
    FOLLOW_37_in_statement2932 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2936 = frozenset([])
    FOLLOW_EOF_in_statement2938 = frozenset([1])
    FOLLOW_name_in_statement2947 = frozenset([32])
    FOLLOW_32_in_statement2949 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2953 = frozenset([])
    FOLLOW_EOF_in_statement2955 = frozenset([1])
    FOLLOW_name_in_statement2964 = frozenset([42])
    FOLLOW_42_in_statement2966 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2970 = frozenset([])
    FOLLOW_EOF_in_statement2972 = frozenset([1])
    FOLLOW_name_in_statement2981 = frozenset([41])
    FOLLOW_41_in_statement2983 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement2987 = frozenset([])
    FOLLOW_EOF_in_statement2989 = frozenset([1])
    FOLLOW_name_in_statement2998 = frozenset([27])
    FOLLOW_27_in_statement3000 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_statement3004 = frozenset([])
    FOLLOW_EOF_in_statement3006 = frozenset([1])
    FOLLOW_expression_in_statement3015 = frozenset([])
    FOLLOW_EOF_in_statement3017 = frozenset([1])
    FOLLOW_list_in_synpred20_UL41460 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred21_UL41469 = frozenset([1])
    FOLLOW_dict_in_synpred22_UL41478 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred23_UL41487 = frozenset([1])
    FOLLOW_28_in_synpred24_UL41496 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_generatorexpression_in_synpred24_UL41500 = frozenset([29])
    FOLLOW_29_in_synpred24_UL41504 = frozenset([1])
    FOLLOW_28_in_synpred26_UL41553 = frozenset([14, 28])
    FOLLOW_nestedname_in_synpred26_UL41557 = frozenset([35])
    FOLLOW_35_in_synpred26_UL41559 = frozenset([29])
    FOLLOW_29_in_synpred26_UL41561 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred70_UL42793 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred71_UL42821 = frozenset([])
    FOLLOW_EOF_in_synpred71_UL42823 = frozenset([1])
    FOLLOW_nestedname_in_synpred72_UL42896 = frozenset([46])
    FOLLOW_46_in_synpred72_UL42898 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred72_UL42902 = frozenset([])
    FOLLOW_EOF_in_synpred72_UL42904 = frozenset([1])
    FOLLOW_name_in_synpred73_UL42913 = frozenset([34])
    FOLLOW_34_in_synpred73_UL42915 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred73_UL42919 = frozenset([])
    FOLLOW_EOF_in_synpred73_UL42921 = frozenset([1])
    FOLLOW_name_in_synpred74_UL42930 = frozenset([37])
    FOLLOW_37_in_synpred74_UL42932 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred74_UL42936 = frozenset([])
    FOLLOW_EOF_in_synpred74_UL42938 = frozenset([1])
    FOLLOW_name_in_synpred75_UL42947 = frozenset([32])
    FOLLOW_32_in_synpred75_UL42949 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred75_UL42953 = frozenset([])
    FOLLOW_EOF_in_synpred75_UL42955 = frozenset([1])
    FOLLOW_name_in_synpred76_UL42964 = frozenset([42])
    FOLLOW_42_in_synpred76_UL42966 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred76_UL42970 = frozenset([])
    FOLLOW_EOF_in_synpred76_UL42972 = frozenset([1])
    FOLLOW_name_in_synpred77_UL42981 = frozenset([41])
    FOLLOW_41_in_synpred77_UL42983 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred77_UL42987 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL42989 = frozenset([1])
    FOLLOW_name_in_synpred78_UL42998 = frozenset([27])
    FOLLOW_27_in_synpred78_UL43000 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 20, 28, 36, 50, 56, 58])
    FOLLOW_expr1_in_synpred78_UL43004 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43006 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
