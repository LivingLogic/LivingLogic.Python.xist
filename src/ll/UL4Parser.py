# $ANTLR 3.5 src/ll/UL4.g 2013-06-20 18:31:48

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
    "UNICODE4_ESC", "WS", "'!='", "'%'", "'%='", "'('", "')'", "'*'", "'**'", 
    "'*='", "'+'", "'+='", "','", "'-'", "'-='", "'.'", "'/'", "'//'", "'//='", 
    "'/='", "':'", "'<'", "'<='", "'='", "'=='", "'>'", "'>='", "'['", "']'", 
    "'and'", "'for'", "'if'", "'in'", "'not'", "'or'", "'{'", "'}'"
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
    # src/ll/UL4.g:162:1: none returns [node] : NONE ;
    def none(self, ):
        node = None


        NONE1 = None

        try:
            try:
                # src/ll/UL4.g:163:2: ( NONE )
                # src/ll/UL4.g:163:4: NONE
                pass 
                NONE1 = self.match(self.input, NONE, self.FOLLOW_NONE_in_none799)

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
    # src/ll/UL4.g:166:1: true_ returns [node] : TRUE ;
    def true_(self, ):
        node = None


        TRUE2 = None

        try:
            try:
                # src/ll/UL4.g:167:2: ( TRUE )
                # src/ll/UL4.g:167:4: TRUE
                pass 
                TRUE2 = self.match(self.input, TRUE, self.FOLLOW_TRUE_in_true_816)

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
    # src/ll/UL4.g:170:1: false_ returns [node] : FALSE ;
    def false_(self, ):
        node = None


        FALSE3 = None

        try:
            try:
                # src/ll/UL4.g:171:2: ( FALSE )
                # src/ll/UL4.g:171:4: FALSE
                pass 
                FALSE3 = self.match(self.input, FALSE, self.FOLLOW_FALSE_in_false_833)

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
    # src/ll/UL4.g:174:1: int_ returns [node] : INT ;
    def int_(self, ):
        node = None


        INT4 = None

        try:
            try:
                # src/ll/UL4.g:175:2: ( INT )
                # src/ll/UL4.g:175:4: INT
                pass 
                INT4 = self.match(self.input, INT, self.FOLLOW_INT_in_int_850)

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
    # src/ll/UL4.g:178:1: float_ returns [node] : FLOAT ;
    def float_(self, ):
        node = None


        FLOAT5 = None

        try:
            try:
                # src/ll/UL4.g:179:2: ( FLOAT )
                # src/ll/UL4.g:179:4: FLOAT
                pass 
                FLOAT5 = self.match(self.input, FLOAT, self.FOLLOW_FLOAT_in_float_867)

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
    # src/ll/UL4.g:182:1: string returns [node] : ( STRING | STRING3 );
    def string(self, ):
        node = None


        STRING6 = None
        STRING37 = None

        try:
            try:
                # src/ll/UL4.g:183:2: ( STRING | STRING3 )
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
                    # src/ll/UL4.g:183:4: STRING
                    pass 
                    STRING6 = self.match(self.input, STRING, self.FOLLOW_STRING_in_string884)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.location, self.start(STRING6), self.end(STRING6), ast.literal_eval(STRING6.text)) 




                elif alt1 == 2:
                    # src/ll/UL4.g:184:4: STRING3
                    pass 
                    STRING37 = self.match(self.input, STRING3, self.FOLLOW_STRING3_in_string891)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Const(self.location, self.start(STRING37), self.end(STRING37), ast.literal_eval(STRING37.text.replace("\r", "\\r"))) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "string"



    # $ANTLR start "date"
    # src/ll/UL4.g:187:1: date returns [node] : DATE ;
    def date(self, ):
        node = None


        DATE8 = None

        try:
            try:
                # src/ll/UL4.g:188:2: ( DATE )
                # src/ll/UL4.g:188:4: DATE
                pass 
                DATE8 = self.match(self.input, DATE, self.FOLLOW_DATE_in_date908)

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
    # src/ll/UL4.g:191:1: color returns [node] : COLOR ;
    def color(self, ):
        node = None


        COLOR9 = None

        try:
            try:
                # src/ll/UL4.g:192:2: ( COLOR )
                # src/ll/UL4.g:192:4: COLOR
                pass 
                COLOR9 = self.match(self.input, COLOR, self.FOLLOW_COLOR_in_color925)

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
    # src/ll/UL4.g:195:1: name returns [node] : NAME ;
    def name(self, ):
        retval = self.name_return()
        retval.start = self.input.LT(1)


        NAME10 = None

        try:
            try:
                # src/ll/UL4.g:196:2: ( NAME )
                # src/ll/UL4.g:196:4: NAME
                pass 
                NAME10 = self.match(self.input, NAME, self.FOLLOW_NAME_in_name942)

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
    # src/ll/UL4.g:199:1: literal returns [node] : (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name );
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
                # src/ll/UL4.g:200:2: (e_none= none |e_false= false_ |e_true= true_ |e_int= int_ |e_float= float_ |e_string= string |e_date= date |e_color= color |e_name= name )
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
                    # src/ll/UL4.g:200:4: e_none= none
                    pass 
                    self._state.following.append(self.FOLLOW_none_in_literal961)
                    e_none = self.none()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_none 




                elif alt2 == 2:
                    # src/ll/UL4.g:201:4: e_false= false_
                    pass 
                    self._state.following.append(self.FOLLOW_false__in_literal970)
                    e_false = self.false_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_false 




                elif alt2 == 3:
                    # src/ll/UL4.g:202:4: e_true= true_
                    pass 
                    self._state.following.append(self.FOLLOW_true__in_literal979)
                    e_true = self.true_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_true 




                elif alt2 == 4:
                    # src/ll/UL4.g:203:4: e_int= int_
                    pass 
                    self._state.following.append(self.FOLLOW_int__in_literal988)
                    e_int = self.int_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_int 




                elif alt2 == 5:
                    # src/ll/UL4.g:204:4: e_float= float_
                    pass 
                    self._state.following.append(self.FOLLOW_float__in_literal997)
                    e_float = self.float_()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_float 




                elif alt2 == 6:
                    # src/ll/UL4.g:205:4: e_string= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_literal1006)
                    e_string = self.string()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_string 




                elif alt2 == 7:
                    # src/ll/UL4.g:206:4: e_date= date
                    pass 
                    self._state.following.append(self.FOLLOW_date_in_literal1015)
                    e_date = self.date()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_date 




                elif alt2 == 8:
                    # src/ll/UL4.g:207:4: e_color= color
                    pass 
                    self._state.following.append(self.FOLLOW_color_in_literal1024)
                    e_color = self.color()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_color 




                elif alt2 == 9:
                    # src/ll/UL4.g:208:4: e_name= name
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



    # $ANTLR start "list"
    # src/ll/UL4.g:212:1: list returns [node] : (open= '[' close= ']' |open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']' );
    def list(self, ):
        node = None


        open = None
        close = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:213:2: (open= '[' close= ']' |open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']' )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 52) :
                    LA5_1 = self.input.LA(2)

                    if (LA5_1 == 53) :
                        alt5 = 1
                    elif ((COLOR <= LA5_1 <= DATE) or (FALSE <= LA5_1 <= FLOAT) or (INT <= LA5_1 <= NONE) or (STRING <= LA5_1 <= STRING3) or LA5_1 == TRUE or LA5_1 == 30 or LA5_1 == 38 or LA5_1 == 52 or LA5_1 == 58 or LA5_1 == 60) :
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
                    # src/ll/UL4.g:214:3: open= '[' close= ']'
                    pass 
                    open = self.match(self.input, 52, self.FOLLOW_52_in_list1056)

                    close = self.match(self.input, 53, self.FOLLOW_53_in_list1062)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), self.end(close)) 




                elif alt5 == 2:
                    # src/ll/UL4.g:217:3: open= '[' e1= expr1 ( ',' e2= expr1 )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 52, self.FOLLOW_52_in_list1073)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_expr1_in_list1081)
                    e1 = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1) 



                    # src/ll/UL4.g:219:3: ( ',' e2= expr1 )*
                    while True: #loop3
                        alt3 = 2
                        LA3_0 = self.input.LA(1)

                        if (LA3_0 == 37) :
                            LA3_1 = self.input.LA(2)

                            if ((COLOR <= LA3_1 <= DATE) or (FALSE <= LA3_1 <= FLOAT) or (INT <= LA3_1 <= NONE) or (STRING <= LA3_1 <= STRING3) or LA3_1 == TRUE or LA3_1 == 30 or LA3_1 == 38 or LA3_1 == 52 or LA3_1 == 58 or LA3_1 == 60) :
                                alt3 = 1




                        if alt3 == 1:
                            # src/ll/UL4.g:220:4: ',' e2= expr1
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_list1092)

                            self._state.following.append(self.FOLLOW_expr1_in_list1099)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2) 




                        else:
                            break #loop3


                    # src/ll/UL4.g:223:3: ( ',' )?
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == 37) :
                        alt4 = 1
                    if alt4 == 1:
                        # src/ll/UL4.g:223:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_list1110)




                    close = self.match(self.input, 53, self.FOLLOW_53_in_list1117)

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
    # src/ll/UL4.g:227:1: listcomprehension returns [node] : open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']' ;
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
                # src/ll/UL4.g:232:2: (open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']' )
                # src/ll/UL4.g:233:3: open= '[' item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= ']'
                pass 
                open = self.match(self.input, 52, self.FOLLOW_52_in_listcomprehension1145)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1151)
                item = self.expr1()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_listcomprehension1155)

                self._state.following.append(self.FOLLOW_nestedname_in_listcomprehension1161)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 57, self.FOLLOW_57_in_listcomprehension1165)

                self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1171)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:239:3: ( 'if' condition= expr1 )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 56) :
                    alt6 = 1
                if alt6 == 1:
                    # src/ll/UL4.g:240:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 56, self.FOLLOW_56_in_listcomprehension1180)

                    self._state.following.append(self.FOLLOW_expr1_in_listcomprehension1187)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 53, self.FOLLOW_53_in_listcomprehension1200)

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
    # src/ll/UL4.g:248:1: fragment dictitem returns [node] : k= expr1 ':' v= expr1 ;
    def dictitem(self, ):
        node = None


        k = None
        v = None

        try:
            try:
                # src/ll/UL4.g:249:2: (k= expr1 ':' v= expr1 )
                # src/ll/UL4.g:250:3: k= expr1 ':' v= expr1
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_dictitem1225)
                k = self.expr1()

                self._state.following.pop()

                self.match(self.input, 45, self.FOLLOW_45_in_dictitem1229)

                self._state.following.append(self.FOLLOW_expr1_in_dictitem1235)
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
    # src/ll/UL4.g:255:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:256:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 60) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 61) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or (STRING <= LA9_1 <= STRING3) or LA9_1 == TRUE or LA9_1 == 30 or LA9_1 == 38 or LA9_1 == 52 or LA9_1 == 58 or LA9_1 == 60) :
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
                    # src/ll/UL4.g:257:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 60, self.FOLLOW_60_in_dict1256)

                    close = self.match(self.input, 61, self.FOLLOW_61_in_dict1262)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), self.end(close)) 




                elif alt9 == 2:
                    # src/ll/UL4.g:260:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 60, self.FOLLOW_60_in_dict1273)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1281)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:262:3: ( ',' i2= dictitem )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 37) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or (STRING <= LA7_1 <= STRING3) or LA7_1 == TRUE or LA7_1 == 30 or LA7_1 == 38 or LA7_1 == 52 or LA7_1 == 58 or LA7_1 == 60) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:263:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_dict1292)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1299)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop7


                    # src/ll/UL4.g:266:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 37) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:266:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_dict1310)




                    close = self.match(self.input, 61, self.FOLLOW_61_in_dict1317)

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
    # src/ll/UL4.g:270:1: dictcomprehension returns [node] : open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}' ;
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
                # src/ll/UL4.g:275:2: (open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}' )
                # src/ll/UL4.g:276:3: open= '{' key= expr1 ':' value= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? close= '}'
                pass 
                open = self.match(self.input, 60, self.FOLLOW_60_in_dictcomprehension1345)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1351)
                key = self.expr1()

                self._state.following.pop()

                self.match(self.input, 45, self.FOLLOW_45_in_dictcomprehension1355)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1361)
                value = self.expr1()

                self._state.following.pop()

                self.match(self.input, 55, self.FOLLOW_55_in_dictcomprehension1365)

                self._state.following.append(self.FOLLOW_nestedname_in_dictcomprehension1371)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 57, self.FOLLOW_57_in_dictcomprehension1375)

                self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1381)
                container = self.expr1()

                self._state.following.pop()

                # src/ll/UL4.g:284:3: ( 'if' condition= expr1 )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 56) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:285:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 56, self.FOLLOW_56_in_dictcomprehension1390)

                    self._state.following.append(self.FOLLOW_expr1_in_dictcomprehension1397)
                    condition = self.expr1()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 61, self.FOLLOW_61_in_dictcomprehension1410)

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
    # src/ll/UL4.g:291:1: generatorexpression returns [node] : item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? ;
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
                # src/ll/UL4.g:297:2: (item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )? )
                # src/ll/UL4.g:298:3: item= expr1 'for' n= nestedname 'in' container= expr1 ( 'if' condition= expr1 )?
                pass 
                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1438)
                item = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item.start 



                self.match(self.input, 55, self.FOLLOW_55_in_generatorexpression1444)

                self._state.following.append(self.FOLLOW_nestedname_in_generatorexpression1450)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 57, self.FOLLOW_57_in_generatorexpression1454)

                self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1460)
                container = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _end = container.end 



                # src/ll/UL4.g:303:3: ( 'if' condition= expr1 )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 56) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:304:4: 'if' condition= expr1
                    pass 
                    self.match(self.input, 56, self.FOLLOW_56_in_generatorexpression1471)

                    self._state.following.append(self.FOLLOW_expr1_in_generatorexpression1478)
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
    # src/ll/UL4.g:309:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr1 close= ')' );
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
                # src/ll/UL4.g:310:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr1 close= ')' )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == COLOR or LA12 == DATE or LA12 == FALSE or LA12 == FLOAT or LA12 == INT or LA12 == NAME or LA12 == NONE or LA12 == STRING or LA12 == STRING3 or LA12 == TRUE:
                    alt12 = 1
                elif LA12 == 52:
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


                elif LA12 == 60:
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


                elif LA12 == 30:
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
                    # src/ll/UL4.g:310:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1504)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt12 == 2:
                    # src/ll/UL4.g:311:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1513)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt12 == 3:
                    # src/ll/UL4.g:312:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1522)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt12 == 4:
                    # src/ll/UL4.g:313:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1531)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt12 == 5:
                    # src/ll/UL4.g:314:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1540)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt12 == 6:
                    # src/ll/UL4.g:315:4: open= '(' e_genexpr= generatorexpression close= ')'
                    pass 
                    open = self.match(self.input, 30, self.FOLLOW_30_in_atom1549)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1553)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 31, self.FOLLOW_31_in_atom1557)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.start = self.start(open)
                        node.end = self.end(close)
                        	




                elif alt12 == 7:
                    # src/ll/UL4.g:320:4: open= '(' e_bracket= expr1 close= ')'
                    pass 
                    open = self.match(self.input, 30, self.FOLLOW_30_in_atom1566)

                    self._state.following.append(self.FOLLOW_expr1_in_atom1570)
                    e_bracket = self.expr1()

                    self._state.following.pop()

                    close = self.match(self.input, 31, self.FOLLOW_31_in_atom1574)

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
    # src/ll/UL4.g:328:1: nestedname returns [varname] : (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' );
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
                # src/ll/UL4.g:329:2: (n= name | '(' n0= nestedname ',' ')' | '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')' )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if (LA15_0 == NAME) :
                    alt15 = 1
                elif (LA15_0 == 30) :
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
                    # src/ll/UL4.g:330:3: n= name
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_nestedname1597)
                    n = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.varname =  ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0] 




                elif alt15 == 2:
                    # src/ll/UL4.g:332:3: '(' n0= nestedname ',' ')'
                    pass 
                    self.match(self.input, 30, self.FOLLOW_30_in_nestedname1606)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1610)
                    n0 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_nestedname1612)

                    self.match(self.input, 31, self.FOLLOW_31_in_nestedname1614)

                    if self._state.backtracking == 0:
                        pass
                        retval.varname = (((n0 is not None) and [n0.varname] or [None])[0],) 




                elif alt15 == 3:
                    # src/ll/UL4.g:334:3: '(' n1= nestedname ',' n2= nestedname ( ',' n3= nestedname )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 30, self.FOLLOW_30_in_nestedname1623)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1629)
                    n1 = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_nestedname1633)

                    self._state.following.append(self.FOLLOW_nestedname_in_nestedname1639)
                    n2 = self.nestedname()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.varname = (((n1 is not None) and [n1.varname] or [None])[0], ((n2 is not None) and [n2.varname] or [None])[0]) 



                    # src/ll/UL4.g:338:3: ( ',' n3= nestedname )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 37) :
                            LA13_1 = self.input.LA(2)

                            if (LA13_1 == NAME or LA13_1 == 30) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:339:4: ',' n3= nestedname
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_nestedname1650)

                            self._state.following.append(self.FOLLOW_nestedname_in_nestedname1657)
                            n3 = self.nestedname()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.varname += (((n3 is not None) and [n3.varname] or [None])[0],) 




                        else:
                            break #loop13


                    # src/ll/UL4.g:342:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 37) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:342:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_nestedname1668)




                    self.match(self.input, 31, self.FOLLOW_31_in_nestedname1673)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedname"



    # $ANTLR start "expr9"
    # src/ll/UL4.g:347:1: expr9 returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )* ;
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
                # src/ll/UL4.g:355:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )* )
                # src/ll/UL4.g:356:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr91702)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:357:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']' )*
                while True: #loop33
                    alt33 = 4
                    LA33 = self.input.LA(1)
                    if LA33 == 40:
                        alt33 = 1
                    elif LA33 == 30:
                        alt33 = 2
                    elif LA33 == 52:
                        alt33 = 3

                    if alt33 == 1:
                        # src/ll/UL4.g:359:4: '.' n= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_expr91718)

                        self._state.following.append(self.FOLLOW_name_in_expr91725)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.GetAttr(self.location, node.start, self.end(n.stop), node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt33 == 2:
                        # src/ll/UL4.g:363:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr91741)

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.CallMeth(self.location, node.start, None, node.obj, node.attrname) if isinstance(node, ul4c.GetAttr) else ul4c.CallFunc(self.location, node.start, None, node) 



                        # src/ll/UL4.g:364:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt28 = 5
                        LA28 = self.input.LA(1)
                        if LA28 == 31:
                            alt28 = 1
                        elif LA28 == 33:
                            alt28 = 2
                        elif LA28 == 32:
                            alt28 = 3
                        elif LA28 == COLOR or LA28 == DATE or LA28 == FALSE or LA28 == FLOAT or LA28 == INT or LA28 == NONE or LA28 == STRING or LA28 == STRING3 or LA28 == TRUE or LA28 == 30 or LA28 == 38 or LA28 == 52 or LA28 == 58 or LA28 == 60:
                            alt28 = 4
                        elif LA28 == NAME:
                            LA28_5 = self.input.LA(2)

                            if ((27 <= LA28_5 <= 28) or (30 <= LA28_5 <= 32) or LA28_5 == 35 or (37 <= LA28_5 <= 38) or (40 <= LA28_5 <= 42) or (46 <= LA28_5 <= 47) or (49 <= LA28_5 <= 52) or (54 <= LA28_5 <= 55) or (57 <= LA28_5 <= 59)) :
                                alt28 = 4
                            elif (LA28_5 == 48) :
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
                            # src/ll/UL4.g:366:4: 
                            pass 

                        elif alt28 == 2:
                            # src/ll/UL4.g:368:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 33, self.FOLLOW_33_in_expr91771)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91775)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:369:5: ( ',' )?
                            alt16 = 2
                            LA16_0 = self.input.LA(1)

                            if (LA16_0 == 37) :
                                alt16 = 1
                            if alt16 == 1:
                                # src/ll/UL4.g:369:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr91783)





                        elif alt28 == 3:
                            # src/ll/UL4.g:372:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr91801)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr91805)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.remargs = rargs; 



                            # src/ll/UL4.g:373:5: ( ',' '**' rkwargs= exprarg )?
                            alt17 = 2
                            LA17_0 = self.input.LA(1)

                            if (LA17_0 == 37) :
                                LA17_1 = self.input.LA(2)

                                if (LA17_1 == 33) :
                                    alt17 = 1
                            if alt17 == 1:
                                # src/ll/UL4.g:374:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr91820)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr91827)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91831)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:377:5: ( ',' )?
                            alt18 = 2
                            LA18_0 = self.input.LA(1)

                            if (LA18_0 == 37) :
                                alt18 = 1
                            if alt18 == 1:
                                # src/ll/UL4.g:377:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr91846)





                        elif alt28 == 4:
                            # src/ll/UL4.g:380:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr91866)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.args.append(a1) 



                            # src/ll/UL4.g:381:5: ( ',' a2= exprarg )*
                            while True: #loop19
                                alt19 = 2
                                LA19_0 = self.input.LA(1)

                                if (LA19_0 == 37) :
                                    LA19_1 = self.input.LA(2)

                                    if (LA19_1 == NAME) :
                                        LA19_3 = self.input.LA(3)

                                        if ((27 <= LA19_3 <= 28) or (30 <= LA19_3 <= 32) or LA19_3 == 35 or (37 <= LA19_3 <= 38) or (40 <= LA19_3 <= 42) or (46 <= LA19_3 <= 47) or (49 <= LA19_3 <= 52) or (54 <= LA19_3 <= 55) or (57 <= LA19_3 <= 59)) :
                                            alt19 = 1


                                    elif ((COLOR <= LA19_1 <= DATE) or (FALSE <= LA19_1 <= FLOAT) or LA19_1 == INT or LA19_1 == NONE or (STRING <= LA19_1 <= STRING3) or LA19_1 == TRUE or LA19_1 == 30 or LA19_1 == 38 or LA19_1 == 52 or LA19_1 == 58 or LA19_1 == 60) :
                                        alt19 = 1




                                if alt19 == 1:
                                    # src/ll/UL4.g:382:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr91881)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91890)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.args.append(a2) 




                                else:
                                    break #loop19


                            # src/ll/UL4.g:385:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop20
                                alt20 = 2
                                LA20_0 = self.input.LA(1)

                                if (LA20_0 == 37) :
                                    LA20_1 = self.input.LA(2)

                                    if (LA20_1 == NAME) :
                                        alt20 = 1




                                if alt20 == 1:
                                    # src/ll/UL4.g:386:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr91912)

                                    self._state.following.append(self.FOLLOW_name_in_expr91921)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 48, self.FOLLOW_48_in_expr91923)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr91927)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop20


                            # src/ll/UL4.g:389:5: ( ',' '*' rargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 37) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 32) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:390:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr91949)

                                self.match(self.input, 32, self.FOLLOW_32_in_expr91956)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91960)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:393:5: ( ',' '**' rkwargs= exprarg )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 37) :
                                LA22_1 = self.input.LA(2)

                                if (LA22_1 == 33) :
                                    alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:394:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr91982)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr91989)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr91993)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:397:5: ( ',' )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 37) :
                                alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:397:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr92008)





                        elif alt28 == 5:
                            # src/ll/UL4.g:400:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr92028)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 48, self.FOLLOW_48_in_expr92030)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr92034)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:401:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop24
                                alt24 = 2
                                LA24_0 = self.input.LA(1)

                                if (LA24_0 == 37) :
                                    LA24_1 = self.input.LA(2)

                                    if (LA24_1 == NAME) :
                                        alt24 = 1




                                if alt24 == 1:
                                    # src/ll/UL4.g:402:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr92049)

                                    self._state.following.append(self.FOLLOW_name_in_expr92058)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 48, self.FOLLOW_48_in_expr92060)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr92064)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop24


                            # src/ll/UL4.g:405:5: ( ',' '*' rargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 37) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 32) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:406:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr92086)

                                self.match(self.input, 32, self.FOLLOW_32_in_expr92093)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr92097)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remargs = rargs; 






                            # src/ll/UL4.g:409:5: ( ',' '**' rkwargs= exprarg )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 37) :
                                LA26_1 = self.input.LA(2)

                                if (LA26_1 == 33) :
                                    alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:410:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr92119)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr92126)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr92130)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:413:5: ( ',' )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 37) :
                                alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:413:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr92145)







                        close = self.match(self.input, 31, self.FOLLOW_31_in_expr92158)

                        if self._state.backtracking == 0:
                            pass
                            node.end = self.end(close) 




                    elif alt33 == 3:
                        # src/ll/UL4.g:418:4: '[' ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? ) close= ']'
                        pass 
                        self.match(self.input, 52, self.FOLLOW_52_in_expr92174)

                        # src/ll/UL4.g:419:4: ( ':' (e2= expr1 )? |e2= expr1 ( ':' (e3= expr1 )? )? )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 45) :
                            alt32 = 1
                        elif ((COLOR <= LA32_0 <= DATE) or (FALSE <= LA32_0 <= FLOAT) or (INT <= LA32_0 <= NONE) or (STRING <= LA32_0 <= STRING3) or LA32_0 == TRUE or LA32_0 == 30 or LA32_0 == 38 or LA32_0 == 52 or LA32_0 == 58 or LA32_0 == 60) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:420:5: ':' (e2= expr1 )?
                            pass 
                            self.match(self.input, 45, self.FOLLOW_45_in_expr92185)

                            # src/ll/UL4.g:421:5: (e2= expr1 )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or (STRING <= LA29_0 <= STRING3) or LA29_0 == TRUE or LA29_0 == 30 or LA29_0 == 38 or LA29_0 == 52 or LA29_0 == 58 or LA29_0 == 60) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:422:6: e2= expr1
                                pass 
                                self._state.following.append(self.FOLLOW_expr1_in_expr92200)
                                e2 = self.expr1()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(self.location, node.start, None, node, None, index2) 




                        elif alt32 == 2:
                            # src/ll/UL4.g:425:5: e2= expr1 ( ':' (e3= expr1 )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr1_in_expr92224)
                            e2 = self.expr1()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:426:5: ( ':' (e3= expr1 )? )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 45) :
                                alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:427:6: ':' (e3= expr1 )?
                                pass 
                                self.match(self.input, 45, self.FOLLOW_45_in_expr92239)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:428:6: (e3= expr1 )?
                                alt30 = 2
                                LA30_0 = self.input.LA(1)

                                if ((COLOR <= LA30_0 <= DATE) or (FALSE <= LA30_0 <= FLOAT) or (INT <= LA30_0 <= NONE) or (STRING <= LA30_0 <= STRING3) or LA30_0 == TRUE or LA30_0 == 30 or LA30_0 == 38 or LA30_0 == 52 or LA30_0 == 58 or LA30_0 == 60) :
                                    alt30 = 1
                                if alt30 == 1:
                                    # src/ll/UL4.g:429:7: e3= expr1
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr1_in_expr92258)
                                    e3 = self.expr1()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                node = ul4c.GetSlice(self.location, node.start, None, node, index1, index2) if slice else ul4c.GetItem(self.location, e1.start, None, node, index1) 






                        close = self.match(self.input, 53, self.FOLLOW_53_in_expr92289)

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
    # src/ll/UL4.g:438:1: expr8 returns [node] : (e1= expr9 |minus= '-' e2= expr8 );
    def expr8(self, ):
        node = None


        minus = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:439:2: (e1= expr9 |minus= '-' e2= expr8 )
                alt34 = 2
                LA34_0 = self.input.LA(1)

                if ((COLOR <= LA34_0 <= DATE) or (FALSE <= LA34_0 <= FLOAT) or (INT <= LA34_0 <= NONE) or (STRING <= LA34_0 <= STRING3) or LA34_0 == TRUE or LA34_0 == 30 or LA34_0 == 52 or LA34_0 == 60) :
                    alt34 = 1
                elif (LA34_0 == 38) :
                    alt34 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae


                if alt34 == 1:
                    # src/ll/UL4.g:440:3: e1= expr9
                    pass 
                    self._state.following.append(self.FOLLOW_expr9_in_expr82317)
                    e1 = self.expr9()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt34 == 2:
                    # src/ll/UL4.g:442:3: minus= '-' e2= expr8
                    pass 
                    minus = self.match(self.input, 38, self.FOLLOW_38_in_expr82328)

                    self._state.following.append(self.FOLLOW_expr8_in_expr82332)
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
    # src/ll/UL4.g:446:1: expr7 returns [node] : e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* ;
    def expr7(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:447:2: (e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )* )
                # src/ll/UL4.g:448:3: e1= expr8 ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                pass 
                self._state.following.append(self.FOLLOW_expr8_in_expr72355)
                e1 = self.expr8()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:449:3: ( ( '*' | '/' | '//' | '%' ) e2= expr8 )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 28 or LA36_0 == 32 or (41 <= LA36_0 <= 42)) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:450:4: ( '*' | '/' | '//' | '%' ) e2= expr8
                        pass 
                        # src/ll/UL4.g:450:4: ( '*' | '/' | '//' | '%' )
                        alt35 = 4
                        LA35 = self.input.LA(1)
                        if LA35 == 32:
                            alt35 = 1
                        elif LA35 == 41:
                            alt35 = 2
                        elif LA35 == 42:
                            alt35 = 3
                        elif LA35 == 28:
                            alt35 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 35, 0, self.input)

                            raise nvae


                        if alt35 == 1:
                            # src/ll/UL4.g:451:5: '*'
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr72372)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:453:5: '/'
                            pass 
                            self.match(self.input, 41, self.FOLLOW_41_in_expr72385)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt35 == 3:
                            # src/ll/UL4.g:455:5: '//'
                            pass 
                            self.match(self.input, 42, self.FOLLOW_42_in_expr72398)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt35 == 4:
                            # src/ll/UL4.g:457:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr72411)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr8_in_expr72425)
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
    # src/ll/UL4.g:464:1: expr6 returns [node] : e1= expr7 ( ( '+' | '-' ) e2= expr7 )* ;
    def expr6(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:465:2: (e1= expr7 ( ( '+' | '-' ) e2= expr7 )* )
                # src/ll/UL4.g:466:3: e1= expr7 ( ( '+' | '-' ) e2= expr7 )*
                pass 
                self._state.following.append(self.FOLLOW_expr7_in_expr62453)
                e1 = self.expr7()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:467:3: ( ( '+' | '-' ) e2= expr7 )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 35 or LA38_0 == 38) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:468:4: ( '+' | '-' ) e2= expr7
                        pass 
                        # src/ll/UL4.g:468:4: ( '+' | '-' )
                        alt37 = 2
                        LA37_0 = self.input.LA(1)

                        if (LA37_0 == 35) :
                            alt37 = 1
                        elif (LA37_0 == 38) :
                            alt37 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:469:5: '+'
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr62470)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:471:5: '-'
                            pass 
                            self.match(self.input, 38, self.FOLLOW_38_in_expr62483)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr7_in_expr62497)
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
    # src/ll/UL4.g:478:1: expr5 returns [node] : e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* ;
    def expr5(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:479:2: (e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )* )
                # src/ll/UL4.g:480:3: e1= expr6 ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                pass 
                self._state.following.append(self.FOLLOW_expr6_in_expr52525)
                e1 = self.expr6()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:481:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6 )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 27 or (46 <= LA40_0 <= 47) or (49 <= LA40_0 <= 51)) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:482:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr6
                        pass 
                        # src/ll/UL4.g:482:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt39 = 6
                        LA39 = self.input.LA(1)
                        if LA39 == 49:
                            alt39 = 1
                        elif LA39 == 27:
                            alt39 = 2
                        elif LA39 == 46:
                            alt39 = 3
                        elif LA39 == 47:
                            alt39 = 4
                        elif LA39 == 50:
                            alt39 = 5
                        elif LA39 == 51:
                            alt39 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:483:5: '=='
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr52542)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:485:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr52555)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt39 == 3:
                            # src/ll/UL4.g:487:5: '<'
                            pass 
                            self.match(self.input, 46, self.FOLLOW_46_in_expr52568)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt39 == 4:
                            # src/ll/UL4.g:489:5: '<='
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr52581)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt39 == 5:
                            # src/ll/UL4.g:491:5: '>'
                            pass 
                            self.match(self.input, 50, self.FOLLOW_50_in_expr52594)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt39 == 6:
                            # src/ll/UL4.g:493:5: '>='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr52607)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr6_in_expr52621)
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
    # src/ll/UL4.g:500:1: expr4 returns [node] : e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? ;
    def expr4(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:501:2: (e1= expr5 ( ( 'not' )? 'in' e2= expr5 )? )
                # src/ll/UL4.g:502:3: e1= expr5 ( ( 'not' )? 'in' e2= expr5 )?
                pass 
                self._state.following.append(self.FOLLOW_expr5_in_expr42649)
                e1 = self.expr5()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = e1 



                # src/ll/UL4.g:503:3: ( ( 'not' )? 'in' e2= expr5 )?
                alt42 = 2
                LA42_0 = self.input.LA(1)

                if ((57 <= LA42_0 <= 58)) :
                    alt42 = 1
                if alt42 == 1:
                    # src/ll/UL4.g:504:4: ( 'not' )? 'in' e2= expr5
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains 



                    # src/ll/UL4.g:505:4: ( 'not' )?
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 58) :
                        alt41 = 1
                    if alt41 == 1:
                        # src/ll/UL4.g:506:5: 'not'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr42671)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains 






                    self.match(self.input, 57, self.FOLLOW_57_in_expr42684)

                    self._state.following.append(self.FOLLOW_expr5_in_expr42691)
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
    # src/ll/UL4.g:514:1: expr3 returns [node] : (e1= expr4 |n= 'not' e2= expr3 );
    def expr3(self, ):
        node = None


        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:515:2: (e1= expr4 |n= 'not' e2= expr3 )
                alt43 = 2
                LA43_0 = self.input.LA(1)

                if ((COLOR <= LA43_0 <= DATE) or (FALSE <= LA43_0 <= FLOAT) or (INT <= LA43_0 <= NONE) or (STRING <= LA43_0 <= STRING3) or LA43_0 == TRUE or LA43_0 == 30 or LA43_0 == 38 or LA43_0 == 52 or LA43_0 == 60) :
                    alt43 = 1
                elif (LA43_0 == 58) :
                    alt43 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 43, 0, self.input)

                    raise nvae


                if alt43 == 1:
                    # src/ll/UL4.g:516:3: e1= expr4
                    pass 
                    self._state.following.append(self.FOLLOW_expr4_in_expr32719)
                    e1 = self.expr4()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt43 == 2:
                    # src/ll/UL4.g:518:3: n= 'not' e2= expr3
                    pass 
                    n = self.match(self.input, 58, self.FOLLOW_58_in_expr32730)

                    self._state.following.append(self.FOLLOW_expr3_in_expr32734)
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
    # src/ll/UL4.g:523:1: expr2 returns [node] : e1= expr3 ( 'and' e2= expr3 )* ;
    def expr2(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:524:2: (e1= expr3 ( 'and' e2= expr3 )* )
                # src/ll/UL4.g:525:3: e1= expr3 ( 'and' e2= expr3 )*
                pass 
                self._state.following.append(self.FOLLOW_expr3_in_expr22758)
                e1 = self.expr3()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:526:3: ( 'and' e2= expr3 )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 54) :
                        alt44 = 1


                    if alt44 == 1:
                        # src/ll/UL4.g:527:4: 'and' e2= expr3
                        pass 
                        self.match(self.input, 54, self.FOLLOW_54_in_expr22769)

                        self._state.following.append(self.FOLLOW_expr3_in_expr22776)
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
    # src/ll/UL4.g:533:1: expr1 returns [node] : e1= expr2 ( 'or' e2= expr2 )* ;
    def expr1(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:534:2: (e1= expr2 ( 'or' e2= expr2 )* )
                # src/ll/UL4.g:535:3: e1= expr2 ( 'or' e2= expr2 )*
                pass 
                self._state.following.append(self.FOLLOW_expr2_in_expr12804)
                e1 = self.expr2()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:536:3: ( 'or' e2= expr2 )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 59) :
                        alt45 = 1


                    if alt45 == 1:
                        # src/ll/UL4.g:537:4: 'or' e2= expr2
                        pass 
                        self.match(self.input, 59, self.FOLLOW_59_in_expr12815)

                        self._state.following.append(self.FOLLOW_expr2_in_expr12822)
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
    # src/ll/UL4.g:542:1: exprarg returns [node] : (ege= generatorexpression |e1= expr1 );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:543:2: (ege= generatorexpression |e1= expr1 )
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


                elif LA46 == 52:
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


                elif LA46 == 60:
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


                elif LA46 == 30:
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


                elif LA46 == 38:
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


                elif LA46 == 58:
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
                    # src/ll/UL4.g:543:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2846)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt46 == 2:
                    # src/ll/UL4.g:544:4: e1= expr1
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_exprarg2855)
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
    # src/ll/UL4.g:547:1: expression returns [node] : (ege= generatorexpression EOF |e= expr1 EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:548:2: (ege= generatorexpression EOF |e= expr1 EOF )
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


                elif LA47 == 52:
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


                elif LA47 == 60:
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


                elif LA47 == 30:
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


                elif LA47 == 38:
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


                elif LA47 == 58:
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
                    # src/ll/UL4.g:548:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression2874)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2876)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt47 == 2:
                    # src/ll/UL4.g:549:4: e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr1_in_expression2885)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression2887)

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
    # src/ll/UL4.g:555:1: for_ returns [node] : n= nestedname 'in' e= expr1 EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:556:2: (n= nestedname 'in' e= expr1 EOF )
                # src/ll/UL4.g:557:3: n= nestedname 'in' e= expr1 EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedname_in_for_2912)
                n = self.nestedname()

                self._state.following.pop()

                self.match(self.input, 57, self.FOLLOW_57_in_for_2916)

                self._state.following.append(self.FOLLOW_expr1_in_for_2922)
                e = self.expr1()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.For(self.location, self.start(n.start), e.end, ((n is not None) and [n.varname] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_2928)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:566:1: statement returns [node] : (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:567:2: (nn= nestedname '=' e= expr1 EOF |n= name '+=' e= expr1 EOF |n= name '-=' e= expr1 EOF |n= name '*=' e= expr1 EOF |n= name '/=' e= expr1 EOF |n= name '//=' e= expr1 EOF |n= name '%=' e= expr1 EOF |e= expression EOF )
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


                elif LA48 == 30:
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


                elif LA48 == COLOR or LA48 == DATE or LA48 == FALSE or LA48 == FLOAT or LA48 == INT or LA48 == NONE or LA48 == STRING or LA48 == STRING3 or LA48 == TRUE or LA48 == 38 or LA48 == 52 or LA48 == 58 or LA48 == 60:
                    alt48 = 8
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 48, 0, self.input)

                    raise nvae


                if alt48 == 1:
                    # src/ll/UL4.g:567:4: nn= nestedname '=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedname_in_statement2949)
                    nn = self.nestedname()

                    self._state.following.pop()

                    self.match(self.input, 48, self.FOLLOW_48_in_statement2951)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2955)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2957)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.StoreVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.varname] or [None])[0], e) 




                elif alt48 == 2:
                    # src/ll/UL4.g:568:4: n= name '+=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2966)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement2968)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2972)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2974)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 3:
                    # src/ll/UL4.g:569:4: n= name '-=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement2983)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_statement2985)

                    self._state.following.append(self.FOLLOW_expr1_in_statement2989)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement2991)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 4:
                    # src/ll/UL4.g:570:4: n= name '*=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement3000)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_statement3002)

                    self._state.following.append(self.FOLLOW_expr1_in_statement3006)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3008)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 5:
                    # src/ll/UL4.g:571:4: n= name '/=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement3017)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 44, self.FOLLOW_44_in_statement3019)

                    self._state.following.append(self.FOLLOW_expr1_in_statement3023)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3025)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 6:
                    # src/ll/UL4.g:572:4: n= name '//=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement3034)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 43, self.FOLLOW_43_in_statement3036)

                    self._state.following.append(self.FOLLOW_expr1_in_statement3040)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3042)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 7:
                    # src/ll/UL4.g:573:4: n= name '%=' e= expr1 EOF
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_statement3051)
                    n = self.name()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3053)

                    self._state.following.append(self.FOLLOW_expr1_in_statement3057)
                    e = self.expr1()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3059)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], e) 




                elif alt48 == 8:
                    # src/ll/UL4.g:574:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3068)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3070)

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

        # src/ll/UL4.g:311:4: (e_list= list )
        # src/ll/UL4.g:311:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred20_UL41513)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred20_UL4"



    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_listcomp = None

        # src/ll/UL4.g:312:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:312:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred21_UL41522)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_dict = None

        # src/ll/UL4.g:313:4: (e_dict= dict )
        # src/ll/UL4.g:313:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred22_UL41531)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_dictcomp = None

        # src/ll/UL4.g:314:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:314:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred23_UL41540)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred23_UL4"



    # $ANTLR start "synpred24_UL4"
    def synpred24_UL4_fragment(self, ):
        open = None
        close = None
        e_genexpr = None

        # src/ll/UL4.g:315:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:315:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 30, self.FOLLOW_30_in_synpred24_UL41549)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred24_UL41553)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 31, self.FOLLOW_31_in_synpred24_UL41557)



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        n0 = None

        # src/ll/UL4.g:332:3: ( '(' n0= nestedname ',' ')' )
        # src/ll/UL4.g:332:3: '(' n0= nestedname ',' ')'
        pass 
        self.match(self.input, 30, self.FOLLOW_30_in_synpred26_UL41606)

        self._state.following.append(self.FOLLOW_nestedname_in_synpred26_UL41610)
        n0 = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 37, self.FOLLOW_37_in_synpred26_UL41612)

        self.match(self.input, 31, self.FOLLOW_31_in_synpred26_UL41614)



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred70_UL4"
    def synpred70_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:543:4: (ege= generatorexpression )
        # src/ll/UL4.g:543:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred70_UL42846)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred70_UL4"



    # $ANTLR start "synpred71_UL4"
    def synpred71_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:548:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:548:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred71_UL42874)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred71_UL42876)



    # $ANTLR end "synpred71_UL4"



    # $ANTLR start "synpred72_UL4"
    def synpred72_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:567:4: (nn= nestedname '=' e= expr1 EOF )
        # src/ll/UL4.g:567:4: nn= nestedname '=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedname_in_synpred72_UL42949)
        nn = self.nestedname()

        self._state.following.pop()

        self.match(self.input, 48, self.FOLLOW_48_in_synpred72_UL42951)

        self._state.following.append(self.FOLLOW_expr1_in_synpred72_UL42955)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred72_UL42957)



    # $ANTLR end "synpred72_UL4"



    # $ANTLR start "synpred73_UL4"
    def synpred73_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:568:4: (n= name '+=' e= expr1 EOF )
        # src/ll/UL4.g:568:4: n= name '+=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred73_UL42966)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred73_UL42968)

        self._state.following.append(self.FOLLOW_expr1_in_synpred73_UL42972)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred73_UL42974)



    # $ANTLR end "synpred73_UL4"



    # $ANTLR start "synpred74_UL4"
    def synpred74_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:569:4: (n= name '-=' e= expr1 EOF )
        # src/ll/UL4.g:569:4: n= name '-=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred74_UL42983)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred74_UL42985)

        self._state.following.append(self.FOLLOW_expr1_in_synpred74_UL42989)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred74_UL42991)



    # $ANTLR end "synpred74_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:570:4: (n= name '*=' e= expr1 EOF )
        # src/ll/UL4.g:570:4: n= name '*=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred75_UL43000)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 34, self.FOLLOW_34_in_synpred75_UL43002)

        self._state.following.append(self.FOLLOW_expr1_in_synpred75_UL43006)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred75_UL43008)



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:571:4: (n= name '/=' e= expr1 EOF )
        # src/ll/UL4.g:571:4: n= name '/=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred76_UL43017)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 44, self.FOLLOW_44_in_synpred76_UL43019)

        self._state.following.append(self.FOLLOW_expr1_in_synpred76_UL43023)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred76_UL43025)



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:572:4: (n= name '//=' e= expr1 EOF )
        # src/ll/UL4.g:572:4: n= name '//=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred77_UL43034)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 43, self.FOLLOW_43_in_synpred77_UL43036)

        self._state.following.append(self.FOLLOW_expr1_in_synpred77_UL43040)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL43042)



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:573:4: (n= name '%=' e= expr1 EOF )
        # src/ll/UL4.g:573:4: n= name '%=' e= expr1 EOF
        pass 
        self._state.following.append(self.FOLLOW_name_in_synpred78_UL43051)
        n = self.name()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred78_UL43053)

        self._state.following.append(self.FOLLOW_expr1_in_synpred78_UL43057)
        e = self.expr1()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43059)



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
    FOLLOW_52_in_list1056 = frozenset([53])
    FOLLOW_53_in_list1062 = frozenset([1])
    FOLLOW_52_in_list1073 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_list1081 = frozenset([37, 53])
    FOLLOW_37_in_list1092 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_list1099 = frozenset([37, 53])
    FOLLOW_37_in_list1110 = frozenset([53])
    FOLLOW_53_in_list1117 = frozenset([1])
    FOLLOW_52_in_listcomprehension1145 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_listcomprehension1151 = frozenset([55])
    FOLLOW_55_in_listcomprehension1155 = frozenset([14, 30])
    FOLLOW_nestedname_in_listcomprehension1161 = frozenset([57])
    FOLLOW_57_in_listcomprehension1165 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_listcomprehension1171 = frozenset([53, 56])
    FOLLOW_56_in_listcomprehension1180 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_listcomprehension1187 = frozenset([53])
    FOLLOW_53_in_listcomprehension1200 = frozenset([1])
    FOLLOW_expr1_in_dictitem1225 = frozenset([45])
    FOLLOW_45_in_dictitem1229 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_dictitem1235 = frozenset([1])
    FOLLOW_60_in_dict1256 = frozenset([61])
    FOLLOW_61_in_dict1262 = frozenset([1])
    FOLLOW_60_in_dict1273 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_dictitem_in_dict1281 = frozenset([37, 61])
    FOLLOW_37_in_dict1292 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_dictitem_in_dict1299 = frozenset([37, 61])
    FOLLOW_37_in_dict1310 = frozenset([61])
    FOLLOW_61_in_dict1317 = frozenset([1])
    FOLLOW_60_in_dictcomprehension1345 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_dictcomprehension1351 = frozenset([45])
    FOLLOW_45_in_dictcomprehension1355 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_dictcomprehension1361 = frozenset([55])
    FOLLOW_55_in_dictcomprehension1365 = frozenset([14, 30])
    FOLLOW_nestedname_in_dictcomprehension1371 = frozenset([57])
    FOLLOW_57_in_dictcomprehension1375 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_dictcomprehension1381 = frozenset([56, 61])
    FOLLOW_56_in_dictcomprehension1390 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_dictcomprehension1397 = frozenset([61])
    FOLLOW_61_in_dictcomprehension1410 = frozenset([1])
    FOLLOW_expr1_in_generatorexpression1438 = frozenset([55])
    FOLLOW_55_in_generatorexpression1444 = frozenset([14, 30])
    FOLLOW_nestedname_in_generatorexpression1450 = frozenset([57])
    FOLLOW_57_in_generatorexpression1454 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_generatorexpression1460 = frozenset([1, 56])
    FOLLOW_56_in_generatorexpression1471 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_generatorexpression1478 = frozenset([1])
    FOLLOW_literal_in_atom1504 = frozenset([1])
    FOLLOW_list_in_atom1513 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1522 = frozenset([1])
    FOLLOW_dict_in_atom1531 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1540 = frozenset([1])
    FOLLOW_30_in_atom1549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_generatorexpression_in_atom1553 = frozenset([31])
    FOLLOW_31_in_atom1557 = frozenset([1])
    FOLLOW_30_in_atom1566 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_atom1570 = frozenset([31])
    FOLLOW_31_in_atom1574 = frozenset([1])
    FOLLOW_name_in_nestedname1597 = frozenset([1])
    FOLLOW_30_in_nestedname1606 = frozenset([14, 30])
    FOLLOW_nestedname_in_nestedname1610 = frozenset([37])
    FOLLOW_37_in_nestedname1612 = frozenset([31])
    FOLLOW_31_in_nestedname1614 = frozenset([1])
    FOLLOW_30_in_nestedname1623 = frozenset([14, 30])
    FOLLOW_nestedname_in_nestedname1629 = frozenset([37])
    FOLLOW_37_in_nestedname1633 = frozenset([14, 30])
    FOLLOW_nestedname_in_nestedname1639 = frozenset([31, 37])
    FOLLOW_37_in_nestedname1650 = frozenset([14, 30])
    FOLLOW_nestedname_in_nestedname1657 = frozenset([31, 37])
    FOLLOW_37_in_nestedname1668 = frozenset([31])
    FOLLOW_31_in_nestedname1673 = frozenset([1])
    FOLLOW_atom_in_expr91702 = frozenset([1, 30, 40, 52])
    FOLLOW_40_in_expr91718 = frozenset([14])
    FOLLOW_name_in_expr91725 = frozenset([1, 30, 40, 52])
    FOLLOW_30_in_expr91741 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 31, 32, 33, 38, 52, 58, 60])
    FOLLOW_33_in_expr91771 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91775 = frozenset([31, 37])
    FOLLOW_37_in_expr91783 = frozenset([31])
    FOLLOW_32_in_expr91801 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91805 = frozenset([31, 37])
    FOLLOW_37_in_expr91820 = frozenset([33])
    FOLLOW_33_in_expr91827 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91831 = frozenset([31, 37])
    FOLLOW_37_in_expr91846 = frozenset([31])
    FOLLOW_exprarg_in_expr91866 = frozenset([31, 37])
    FOLLOW_37_in_expr91881 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91890 = frozenset([31, 37])
    FOLLOW_37_in_expr91912 = frozenset([14])
    FOLLOW_name_in_expr91921 = frozenset([48])
    FOLLOW_48_in_expr91923 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91927 = frozenset([31, 37])
    FOLLOW_37_in_expr91949 = frozenset([32])
    FOLLOW_32_in_expr91956 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91960 = frozenset([31, 37])
    FOLLOW_37_in_expr91982 = frozenset([33])
    FOLLOW_33_in_expr91989 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr91993 = frozenset([31, 37])
    FOLLOW_37_in_expr92008 = frozenset([31])
    FOLLOW_name_in_expr92028 = frozenset([48])
    FOLLOW_48_in_expr92030 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr92034 = frozenset([31, 37])
    FOLLOW_37_in_expr92049 = frozenset([14])
    FOLLOW_name_in_expr92058 = frozenset([48])
    FOLLOW_48_in_expr92060 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr92064 = frozenset([31, 37])
    FOLLOW_37_in_expr92086 = frozenset([32])
    FOLLOW_32_in_expr92093 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr92097 = frozenset([31, 37])
    FOLLOW_37_in_expr92119 = frozenset([33])
    FOLLOW_33_in_expr92126 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_exprarg_in_expr92130 = frozenset([31, 37])
    FOLLOW_37_in_expr92145 = frozenset([31])
    FOLLOW_31_in_expr92158 = frozenset([1, 30, 40, 52])
    FOLLOW_52_in_expr92174 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 45, 52, 58, 60])
    FOLLOW_45_in_expr92185 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 53, 58, 60])
    FOLLOW_expr1_in_expr92200 = frozenset([53])
    FOLLOW_expr1_in_expr92224 = frozenset([45, 53])
    FOLLOW_45_in_expr92239 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 53, 58, 60])
    FOLLOW_expr1_in_expr92258 = frozenset([53])
    FOLLOW_53_in_expr92289 = frozenset([1, 30, 40, 52])
    FOLLOW_expr9_in_expr82317 = frozenset([1])
    FOLLOW_38_in_expr82328 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_expr8_in_expr82332 = frozenset([1])
    FOLLOW_expr8_in_expr72355 = frozenset([1, 28, 32, 41, 42])
    FOLLOW_32_in_expr72372 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_41_in_expr72385 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_42_in_expr72398 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_28_in_expr72411 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_expr8_in_expr72425 = frozenset([1, 28, 32, 41, 42])
    FOLLOW_expr7_in_expr62453 = frozenset([1, 35, 38])
    FOLLOW_35_in_expr62470 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_38_in_expr62483 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_expr7_in_expr62497 = frozenset([1, 35, 38])
    FOLLOW_expr6_in_expr52525 = frozenset([1, 27, 46, 47, 49, 50, 51])
    FOLLOW_49_in_expr52542 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_27_in_expr52555 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_46_in_expr52568 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_47_in_expr52581 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_50_in_expr52594 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_51_in_expr52607 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_expr6_in_expr52621 = frozenset([1, 27, 46, 47, 49, 50, 51])
    FOLLOW_expr5_in_expr42649 = frozenset([1, 57, 58])
    FOLLOW_58_in_expr42671 = frozenset([57])
    FOLLOW_57_in_expr42684 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 60])
    FOLLOW_expr5_in_expr42691 = frozenset([1])
    FOLLOW_expr4_in_expr32719 = frozenset([1])
    FOLLOW_58_in_expr32730 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr3_in_expr32734 = frozenset([1])
    FOLLOW_expr3_in_expr22758 = frozenset([1, 54])
    FOLLOW_54_in_expr22769 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr3_in_expr22776 = frozenset([1, 54])
    FOLLOW_expr2_in_expr12804 = frozenset([1, 59])
    FOLLOW_59_in_expr12815 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr2_in_expr12822 = frozenset([1, 59])
    FOLLOW_generatorexpression_in_exprarg2846 = frozenset([1])
    FOLLOW_expr1_in_exprarg2855 = frozenset([1])
    FOLLOW_generatorexpression_in_expression2874 = frozenset([])
    FOLLOW_EOF_in_expression2876 = frozenset([1])
    FOLLOW_expr1_in_expression2885 = frozenset([])
    FOLLOW_EOF_in_expression2887 = frozenset([1])
    FOLLOW_nestedname_in_for_2912 = frozenset([57])
    FOLLOW_57_in_for_2916 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_for_2922 = frozenset([])
    FOLLOW_EOF_in_for_2928 = frozenset([1])
    FOLLOW_nestedname_in_statement2949 = frozenset([48])
    FOLLOW_48_in_statement2951 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement2955 = frozenset([])
    FOLLOW_EOF_in_statement2957 = frozenset([1])
    FOLLOW_name_in_statement2966 = frozenset([36])
    FOLLOW_36_in_statement2968 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement2972 = frozenset([])
    FOLLOW_EOF_in_statement2974 = frozenset([1])
    FOLLOW_name_in_statement2983 = frozenset([39])
    FOLLOW_39_in_statement2985 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement2989 = frozenset([])
    FOLLOW_EOF_in_statement2991 = frozenset([1])
    FOLLOW_name_in_statement3000 = frozenset([34])
    FOLLOW_34_in_statement3002 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement3006 = frozenset([])
    FOLLOW_EOF_in_statement3008 = frozenset([1])
    FOLLOW_name_in_statement3017 = frozenset([44])
    FOLLOW_44_in_statement3019 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement3023 = frozenset([])
    FOLLOW_EOF_in_statement3025 = frozenset([1])
    FOLLOW_name_in_statement3034 = frozenset([43])
    FOLLOW_43_in_statement3036 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement3040 = frozenset([])
    FOLLOW_EOF_in_statement3042 = frozenset([1])
    FOLLOW_name_in_statement3051 = frozenset([29])
    FOLLOW_29_in_statement3053 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_statement3057 = frozenset([])
    FOLLOW_EOF_in_statement3059 = frozenset([1])
    FOLLOW_expression_in_statement3068 = frozenset([])
    FOLLOW_EOF_in_statement3070 = frozenset([1])
    FOLLOW_list_in_synpred20_UL41513 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred21_UL41522 = frozenset([1])
    FOLLOW_dict_in_synpred22_UL41531 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred23_UL41540 = frozenset([1])
    FOLLOW_30_in_synpred24_UL41549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_generatorexpression_in_synpred24_UL41553 = frozenset([31])
    FOLLOW_31_in_synpred24_UL41557 = frozenset([1])
    FOLLOW_30_in_synpred26_UL41606 = frozenset([14, 30])
    FOLLOW_nestedname_in_synpred26_UL41610 = frozenset([37])
    FOLLOW_37_in_synpred26_UL41612 = frozenset([31])
    FOLLOW_31_in_synpred26_UL41614 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred70_UL42846 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred71_UL42874 = frozenset([])
    FOLLOW_EOF_in_synpred71_UL42876 = frozenset([1])
    FOLLOW_nestedname_in_synpred72_UL42949 = frozenset([48])
    FOLLOW_48_in_synpred72_UL42951 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred72_UL42955 = frozenset([])
    FOLLOW_EOF_in_synpred72_UL42957 = frozenset([1])
    FOLLOW_name_in_synpred73_UL42966 = frozenset([36])
    FOLLOW_36_in_synpred73_UL42968 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred73_UL42972 = frozenset([])
    FOLLOW_EOF_in_synpred73_UL42974 = frozenset([1])
    FOLLOW_name_in_synpred74_UL42983 = frozenset([39])
    FOLLOW_39_in_synpred74_UL42985 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred74_UL42989 = frozenset([])
    FOLLOW_EOF_in_synpred74_UL42991 = frozenset([1])
    FOLLOW_name_in_synpred75_UL43000 = frozenset([34])
    FOLLOW_34_in_synpred75_UL43002 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred75_UL43006 = frozenset([])
    FOLLOW_EOF_in_synpred75_UL43008 = frozenset([1])
    FOLLOW_name_in_synpred76_UL43017 = frozenset([44])
    FOLLOW_44_in_synpred76_UL43019 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred76_UL43023 = frozenset([])
    FOLLOW_EOF_in_synpred76_UL43025 = frozenset([1])
    FOLLOW_name_in_synpred77_UL43034 = frozenset([43])
    FOLLOW_43_in_synpred77_UL43036 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred77_UL43040 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL43042 = frozenset([1])
    FOLLOW_name_in_synpred78_UL43051 = frozenset([29])
    FOLLOW_29_in_synpred78_UL43053 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 52, 58, 60])
    FOLLOW_expr1_in_synpred78_UL43057 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43059 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
