# $ANTLR 3.5 src/ll/UL4.g 2013-12-28 13:05:43

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
    "'/='", "':'", "'<'", "'<<'", "'<<='", "'<='", "'='", "'=='", "'>'", 
    "'>='", "'>>'", "'>>='", "'['", "']'", "'and'", "'else'", "'for'", "'if'", 
    "'in'", "'not'", "'or'", "'{'", "'}'"
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




             
    def reportError(self, e):
    	raise e

    def mismatch(self, input, ttype, follow):
    	raise MismatchedTokenException(ttype, input)

    def recoverFromMismatchedSet(self, input, e, follow):
    	raise e

    def start(self, token):
    	return self.location.startcode + token.start

    def end(self, token):
    	return self.location.startcode + token.stop + 1



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
                    node = ul4c.Const(self.location, self.start(NONE1), self.end(NONE1), None) 






                       
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
                    node = ul4c.Const(self.location, self.start(TRUE2), self.end(TRUE2), True) 






                       
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
                    node = ul4c.Const(self.location, self.start(FALSE3), self.end(FALSE3), False) 






                       
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
                    node = ul4c.Const(self.location, self.start(INT4), self.end(INT4), int(INT4.text, 0)) 






                       
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
                    node = ul4c.Const(self.location, self.start(FLOAT5), self.end(FLOAT5), float(FLOAT5.text)) 






                       
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
                        node = ul4c.Const(self.location, self.start(STRING6), self.end(STRING6), ast.literal_eval(STRING6.text)) 




                elif alt1 == 2:
                    # src/ll/UL4.g:187:4: STRING3
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
                    node = ul4c.Const(self.location, self.start(DATE8), self.end(DATE8), datetime.datetime(*map(int, [f for f in ul4c._datesplitter.split(DATE8.text[2:-1]) if f]))) 






                       
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
                    retval.node = ul4c.Var(self.location, self.start(NAME10), self.end(NAME10), NAME10.text) 





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



    # $ANTLR start "list"
    # src/ll/UL4.g:215:1: list returns [node] : (open= '[' close= ']' |open= '[' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= ']' );
    def list(self, ):
        node = None


        open = None
        close = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:216:2: (open= '[' close= ']' |open= '[' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= ']' )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == 56) :
                    LA5_1 = self.input.LA(2)

                    if (LA5_1 == 57) :
                        alt5 = 1
                    elif ((COLOR <= LA5_1 <= DATE) or (FALSE <= LA5_1 <= FLOAT) or (INT <= LA5_1 <= NONE) or (STRING <= LA5_1 <= STRING3) or LA5_1 == TRUE or LA5_1 == 30 or LA5_1 == 38 or LA5_1 == 56 or LA5_1 == 63 or LA5_1 == 65) :
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
                    # src/ll/UL4.g:217:3: open= '[' close= ']'
                    pass 
                    open = self.match(self.input, 56, self.FOLLOW_56_in_list1056)

                    close = self.match(self.input, 57, self.FOLLOW_57_in_list1062)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), self.end(close)) 




                elif alt5 == 2:
                    # src/ll/UL4.g:220:3: open= '[' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 56, self.FOLLOW_56_in_list1073)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_expr_if_in_list1081)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1) 



                    # src/ll/UL4.g:222:3: ( ',' e2= expr_if )*
                    while True: #loop3
                        alt3 = 2
                        LA3_0 = self.input.LA(1)

                        if (LA3_0 == 37) :
                            LA3_1 = self.input.LA(2)

                            if ((COLOR <= LA3_1 <= DATE) or (FALSE <= LA3_1 <= FLOAT) or (INT <= LA3_1 <= NONE) or (STRING <= LA3_1 <= STRING3) or LA3_1 == TRUE or LA3_1 == 30 or LA3_1 == 38 or LA3_1 == 56 or LA3_1 == 63 or LA3_1 == 65) :
                                alt3 = 1




                        if alt3 == 1:
                            # src/ll/UL4.g:223:4: ',' e2= expr_if
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_list1092)

                            self._state.following.append(self.FOLLOW_expr_if_in_list1099)
                            e2 = self.expr_if()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2) 




                        else:
                            break #loop3


                    # src/ll/UL4.g:226:3: ( ',' )?
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == 37) :
                        alt4 = 1
                    if alt4 == 1:
                        # src/ll/UL4.g:226:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_list1110)




                    close = self.match(self.input, 57, self.FOLLOW_57_in_list1117)

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
    # src/ll/UL4.g:230:1: listcomprehension returns [node] : open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' ;
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
                # src/ll/UL4.g:235:2: (open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']' )
                # src/ll/UL4.g:236:3: open= '[' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= ']'
                pass 
                open = self.match(self.input, 56, self.FOLLOW_56_in_listcomprehension1145)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1151)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 60, self.FOLLOW_60_in_listcomprehension1155)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_listcomprehension1161)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 62, self.FOLLOW_62_in_listcomprehension1165)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1171)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:242:3: ( 'if' condition= expr_if )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 61) :
                    alt6 = 1
                if alt6 == 1:
                    # src/ll/UL4.g:243:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 61, self.FOLLOW_61_in_listcomprehension1180)

                    self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1187)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 57, self.FOLLOW_57_in_listcomprehension1200)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ListComp(self.location, self.start(open), self.end(close), item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "listcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:251:1: fragment dictitem returns [node] : k= expr_if ':' v= expr_if ;
    def dictitem(self, ):
        node = None


        k = None
        v = None

        try:
            try:
                # src/ll/UL4.g:252:2: (k= expr_if ':' v= expr_if )
                # src/ll/UL4.g:253:3: k= expr_if ':' v= expr_if
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_dictitem1225)
                k = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 45, self.FOLLOW_45_in_dictitem1229)

                self._state.following.append(self.FOLLOW_expr_if_in_dictitem1235)
                v = self.expr_if()

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
    # src/ll/UL4.g:258:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:259:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 65) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 66) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or (STRING <= LA9_1 <= STRING3) or LA9_1 == TRUE or LA9_1 == 30 or LA9_1 == 38 or LA9_1 == 56 or LA9_1 == 63 or LA9_1 == 65) :
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
                    # src/ll/UL4.g:260:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 65, self.FOLLOW_65_in_dict1256)

                    close = self.match(self.input, 66, self.FOLLOW_66_in_dict1262)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), self.end(close)) 




                elif alt9 == 2:
                    # src/ll/UL4.g:263:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 65, self.FOLLOW_65_in_dict1273)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1281)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:265:3: ( ',' i2= dictitem )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 37) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or (STRING <= LA7_1 <= STRING3) or LA7_1 == TRUE or LA7_1 == 30 or LA7_1 == 38 or LA7_1 == 56 or LA7_1 == 63 or LA7_1 == 65) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:266:4: ',' i2= dictitem
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


                    # src/ll/UL4.g:269:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 37) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:269:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_dict1310)




                    close = self.match(self.input, 66, self.FOLLOW_66_in_dict1317)

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
    # src/ll/UL4.g:273:1: dictcomprehension returns [node] : open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
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
                # src/ll/UL4.g:278:2: (open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:279:3: open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 65, self.FOLLOW_65_in_dictcomprehension1345)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1351)
                key = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 45, self.FOLLOW_45_in_dictcomprehension1355)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1361)
                value = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 60, self.FOLLOW_60_in_dictcomprehension1365)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_dictcomprehension1371)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 62, self.FOLLOW_62_in_dictcomprehension1375)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1381)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:287:3: ( 'if' condition= expr_if )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 61) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:288:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 61, self.FOLLOW_61_in_dictcomprehension1390)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1397)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 66, self.FOLLOW_66_in_dictcomprehension1410)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.DictComp(self.location, self.start(open), self.end(close), key, value, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "dictcomprehension"



    # $ANTLR start "generatorexpression"
    # src/ll/UL4.g:294:1: generatorexpression returns [node] : item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? ;
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
                # src/ll/UL4.g:300:2: (item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? )
                # src/ll/UL4.g:301:3: item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )?
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1438)
                item = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item.start 



                self.match(self.input, 60, self.FOLLOW_60_in_generatorexpression1444)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_generatorexpression1450)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 62, self.FOLLOW_62_in_generatorexpression1454)

                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1460)
                container = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _end = container.end 



                # src/ll/UL4.g:306:3: ( 'if' condition= expr_if )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 61) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:307:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 61, self.FOLLOW_61_in_generatorexpression1471)

                    self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1478)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; _end = condition.end 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.GenExpr(self.location, item.start, _end, item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "generatorexpression"



    # $ANTLR start "atom"
    # src/ll/UL4.g:312:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' );
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
                # src/ll/UL4.g:313:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' )
                alt12 = 7
                LA12 = self.input.LA(1)
                if LA12 == COLOR or LA12 == DATE or LA12 == FALSE or LA12 == FLOAT or LA12 == INT or LA12 == NAME or LA12 == NONE or LA12 == STRING or LA12 == STRING3 or LA12 == TRUE:
                    alt12 = 1
                elif LA12 == 56:
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


                elif LA12 == 65:
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
                    # src/ll/UL4.g:313:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1504)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt12 == 2:
                    # src/ll/UL4.g:314:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1513)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt12 == 3:
                    # src/ll/UL4.g:315:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1522)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt12 == 4:
                    # src/ll/UL4.g:316:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1531)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt12 == 5:
                    # src/ll/UL4.g:317:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1540)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt12 == 6:
                    # src/ll/UL4.g:318:4: open= '(' e_genexpr= generatorexpression close= ')'
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
                    # src/ll/UL4.g:323:4: open= '(' e_bracket= expr_if close= ')'
                    pass 
                    open = self.match(self.input, 30, self.FOLLOW_30_in_atom1566)

                    self._state.following.append(self.FOLLOW_expr_if_in_atom1570)
                    e_bracket = self.expr_if()

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


    class nestedlvalue_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.nestedlvalue_return, self).__init__()

            self.lvalue = None





    # $ANTLR start "nestedlvalue"
    # src/ll/UL4.g:331:1: nestedlvalue returns [lvalue] : (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' );
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
                # src/ll/UL4.g:332:2: (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' )
                alt15 = 3
                LA15_0 = self.input.LA(1)

                if ((COLOR <= LA15_0 <= DATE) or (FALSE <= LA15_0 <= FLOAT) or (INT <= LA15_0 <= NONE) or (STRING <= LA15_0 <= STRING3) or LA15_0 == TRUE or LA15_0 == 56 or LA15_0 == 65) :
                    alt15 = 1
                elif (LA15_0 == 30) :
                    LA15_13 = self.input.LA(2)

                    if (self.synpred25_UL4()) :
                        alt15 = 1
                    elif (self.synpred26_UL4()) :
                        alt15 = 2
                    elif (True) :
                        alt15 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 15, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 15, 0, self.input)

                    raise nvae


                if alt15 == 1:
                    # src/ll/UL4.g:333:3: n= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_nestedlvalue1597)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue =  ((n is not None) and [n.node] or [None])[0] 




                elif alt15 == 2:
                    # src/ll/UL4.g:335:3: '(' n0= nestedlvalue ',' ')'
                    pass 
                    self.match(self.input, 30, self.FOLLOW_30_in_nestedlvalue1606)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1610)
                    n0 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_nestedlvalue1612)

                    self.match(self.input, 31, self.FOLLOW_31_in_nestedlvalue1614)

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n0 is not None) and [n0.lvalue] or [None])[0],) 




                elif alt15 == 3:
                    # src/ll/UL4.g:337:3: '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 30, self.FOLLOW_30_in_nestedlvalue1623)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1629)
                    n1 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 37, self.FOLLOW_37_in_nestedlvalue1633)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1639)
                    n2 = self.nestedlvalue()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n1 is not None) and [n1.lvalue] or [None])[0], ((n2 is not None) and [n2.lvalue] or [None])[0]) 



                    # src/ll/UL4.g:341:3: ( ',' n3= nestedlvalue )*
                    while True: #loop13
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == 37) :
                            LA13_1 = self.input.LA(2)

                            if ((COLOR <= LA13_1 <= DATE) or (FALSE <= LA13_1 <= FLOAT) or (INT <= LA13_1 <= NONE) or (STRING <= LA13_1 <= STRING3) or LA13_1 == TRUE or LA13_1 == 30 or LA13_1 == 56 or LA13_1 == 65) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:342:4: ',' n3= nestedlvalue
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_nestedlvalue1650)

                            self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1657)
                            n3 = self.nestedlvalue()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.lvalue += (((n3 is not None) and [n3.lvalue] or [None])[0],) 




                        else:
                            break #loop13


                    # src/ll/UL4.g:345:3: ( ',' )?
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == 37) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:345:3: ','
                        pass 
                        self.match(self.input, 37, self.FOLLOW_37_in_nestedlvalue1668)




                    self.match(self.input, 31, self.FOLLOW_31_in_nestedlvalue1673)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedlvalue"


    class expr_subscript_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.expr_subscript_return, self).__init__()

            self.node = None





    # $ANTLR start "expr_subscript"
    # src/ll/UL4.g:350:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? ) close= ']' )* ;
    def expr_subscript(self, ):
        retval = self.expr_subscript_return()
        retval.start = self.input.LT(1)


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

         
        index1 = None
        index2 = None
        slice = False
        	
        try:
            try:
                # src/ll/UL4.g:357:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? ) close= ']' )* )
                # src/ll/UL4.g:358:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? ) close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript1701)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    retval.node =  e1 



                # src/ll/UL4.g:359:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? ) close= ']' )*
                while True: #loop33
                    alt33 = 4
                    LA33 = self.input.LA(1)
                    if LA33 == 40:
                        alt33 = 1
                    elif LA33 == 30:
                        alt33 = 2
                    elif LA33 == 56:
                        alt33 = 3

                    if alt33 == 1:
                        # src/ll/UL4.g:361:4: '.' n= name
                        pass 
                        self.match(self.input, 40, self.FOLLOW_40_in_expr_subscript1717)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript1724)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Attr(self.location, retval.node.start, self.end(n.stop), retval.node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt33 == 2:
                        # src/ll/UL4.g:365:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr_subscript1740)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Call(self.location, retval.node.start, None, retval.node) 



                        # src/ll/UL4.g:366:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt28 = 5
                        LA28 = self.input.LA(1)
                        if LA28 == 31:
                            alt28 = 1
                        elif LA28 == 33:
                            alt28 = 2
                        elif LA28 == 32:
                            alt28 = 3
                        elif LA28 == COLOR or LA28 == DATE or LA28 == FALSE or LA28 == FLOAT or LA28 == INT or LA28 == NONE or LA28 == STRING or LA28 == STRING3 or LA28 == TRUE or LA28 == 30 or LA28 == 38 or LA28 == 56 or LA28 == 63 or LA28 == 65:
                            alt28 = 4
                        elif LA28 == NAME:
                            LA28_5 = self.input.LA(2)

                            if ((27 <= LA28_5 <= 28) or (30 <= LA28_5 <= 32) or LA28_5 == 35 or (37 <= LA28_5 <= 38) or (40 <= LA28_5 <= 42) or (46 <= LA28_5 <= 47) or LA28_5 == 49 or (51 <= LA28_5 <= 54) or LA28_5 == 56 or LA28_5 == 58 or (60 <= LA28_5 <= 64)) :
                                alt28 = 4
                            elif (LA28_5 == 50) :
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
                            # src/ll/UL4.g:368:4: 
                            pass 

                        elif alt28 == 2:
                            # src/ll/UL4.g:370:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript1770)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1774)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:371:5: ( ',' )?
                            alt16 = 2
                            LA16_0 = self.input.LA(1)

                            if (LA16_0 == 37) :
                                alt16 = 1
                            if alt16 == 1:
                                # src/ll/UL4.g:371:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1782)





                        elif alt28 == 3:
                            # src/ll/UL4.g:374:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript1800)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1804)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remargs = rargs; 



                            # src/ll/UL4.g:375:5: ( ',' '**' rkwargs= exprarg )?
                            alt17 = 2
                            LA17_0 = self.input.LA(1)

                            if (LA17_0 == 37) :
                                LA17_1 = self.input.LA(2)

                                if (LA17_1 == 33) :
                                    alt17 = 1
                            if alt17 == 1:
                                # src/ll/UL4.g:376:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1819)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript1826)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1830)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:379:5: ( ',' )?
                            alt18 = 2
                            LA18_0 = self.input.LA(1)

                            if (LA18_0 == 37) :
                                alt18 = 1
                            if alt18 == 1:
                                # src/ll/UL4.g:379:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1845)





                        elif alt28 == 4:
                            # src/ll/UL4.g:382:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1865)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append(a1) 



                            # src/ll/UL4.g:383:5: ( ',' a2= exprarg )*
                            while True: #loop19
                                alt19 = 2
                                LA19_0 = self.input.LA(1)

                                if (LA19_0 == 37) :
                                    LA19_1 = self.input.LA(2)

                                    if (LA19_1 == NAME) :
                                        LA19_3 = self.input.LA(3)

                                        if ((27 <= LA19_3 <= 28) or (30 <= LA19_3 <= 32) or LA19_3 == 35 or (37 <= LA19_3 <= 38) or (40 <= LA19_3 <= 42) or (46 <= LA19_3 <= 47) or LA19_3 == 49 or (51 <= LA19_3 <= 54) or LA19_3 == 56 or LA19_3 == 58 or (60 <= LA19_3 <= 64)) :
                                            alt19 = 1


                                    elif ((COLOR <= LA19_1 <= DATE) or (FALSE <= LA19_1 <= FLOAT) or LA19_1 == INT or LA19_1 == NONE or (STRING <= LA19_1 <= STRING3) or LA19_1 == TRUE or LA19_1 == 30 or LA19_1 == 38 or LA19_1 == 56 or LA19_1 == 63 or LA19_1 == 65) :
                                        alt19 = 1




                                if alt19 == 1:
                                    # src/ll/UL4.g:384:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1880)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1889)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append(a2) 




                                else:
                                    break #loop19


                            # src/ll/UL4.g:387:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop20
                                alt20 = 2
                                LA20_0 = self.input.LA(1)

                                if (LA20_0 == 37) :
                                    LA20_1 = self.input.LA(2)

                                    if (LA20_1 == NAME) :
                                        alt20 = 1




                                if alt20 == 1:
                                    # src/ll/UL4.g:388:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1911)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript1920)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 50, self.FOLLOW_50_in_expr_subscript1922)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1926)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop20


                            # src/ll/UL4.g:391:5: ( ',' '*' rargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 37) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 32) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:392:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1948)

                                self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript1955)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1959)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:395:5: ( ',' '**' rkwargs= exprarg )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 37) :
                                LA22_1 = self.input.LA(2)

                                if (LA22_1 == 33) :
                                    alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:396:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript1981)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript1988)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1992)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:399:5: ( ',' )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 37) :
                                alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:399:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript2007)





                        elif alt28 == 5:
                            # src/ll/UL4.g:402:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr_subscript2027)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 50, self.FOLLOW_50_in_expr_subscript2029)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2033)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:403:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop24
                                alt24 = 2
                                LA24_0 = self.input.LA(1)

                                if (LA24_0 == 37) :
                                    LA24_1 = self.input.LA(2)

                                    if (LA24_1 == NAME) :
                                        alt24 = 1




                                if alt24 == 1:
                                    # src/ll/UL4.g:404:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript2048)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2057)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 50, self.FOLLOW_50_in_expr_subscript2059)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2063)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop24


                            # src/ll/UL4.g:407:5: ( ',' '*' rargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 37) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 32) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:408:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript2085)

                                self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript2092)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2096)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:411:5: ( ',' '**' rkwargs= exprarg )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 37) :
                                LA26_1 = self.input.LA(2)

                                if (LA26_1 == 33) :
                                    alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:412:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript2118)

                                self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2125)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2129)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:415:5: ( ',' )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 37) :
                                alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:415:5: ','
                                pass 
                                self.match(self.input, 37, self.FOLLOW_37_in_expr_subscript2144)







                        close = self.match(self.input, 31, self.FOLLOW_31_in_expr_subscript2157)

                        if self._state.backtracking == 0:
                            pass
                            retval.node.end = self.end(close) 




                    elif alt33 == 3:
                        # src/ll/UL4.g:420:4: '[' ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? ) close= ']'
                        pass 
                        self.match(self.input, 56, self.FOLLOW_56_in_expr_subscript2173)

                        # src/ll/UL4.g:421:4: ( ':' (e2= expr_if )? |e2= expr_if ( ':' (e3= expr_if )? )? )
                        alt32 = 2
                        LA32_0 = self.input.LA(1)

                        if (LA32_0 == 45) :
                            alt32 = 1
                        elif ((COLOR <= LA32_0 <= DATE) or (FALSE <= LA32_0 <= FLOAT) or (INT <= LA32_0 <= NONE) or (STRING <= LA32_0 <= STRING3) or LA32_0 == TRUE or LA32_0 == 30 or LA32_0 == 38 or LA32_0 == 56 or LA32_0 == 63 or LA32_0 == 65) :
                            alt32 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:422:5: ':' (e2= expr_if )?
                            pass 
                            self.match(self.input, 45, self.FOLLOW_45_in_expr_subscript2184)

                            # src/ll/UL4.g:423:5: (e2= expr_if )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if ((COLOR <= LA29_0 <= DATE) or (FALSE <= LA29_0 <= FLOAT) or (INT <= LA29_0 <= NONE) or (STRING <= LA29_0 <= STRING3) or LA29_0 == TRUE or LA29_0 == 30 or LA29_0 == 38 or LA29_0 == 56 or LA29_0 == 63 or LA29_0 == 65) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:424:6: e2= expr_if
                                pass 
                                self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2199)
                                e2 = self.expr_if()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    index2 = e2; 






                            if self._state.backtracking == 0:
                                pass
                                retval.node = ul4c.Slice(self.location, retval.node.start, None, retval.node, None, index2) 




                        elif alt32 == 2:
                            # src/ll/UL4.g:427:5: e2= expr_if ( ':' (e3= expr_if )? )?
                            pass 
                            self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2223)
                            e2 = self.expr_if()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index1 = e2; 



                            # src/ll/UL4.g:428:5: ( ':' (e3= expr_if )? )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 45) :
                                alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:429:6: ':' (e3= expr_if )?
                                pass 
                                self.match(self.input, 45, self.FOLLOW_45_in_expr_subscript2238)

                                if self._state.backtracking == 0:
                                    pass
                                    slice = True; 



                                # src/ll/UL4.g:430:6: (e3= expr_if )?
                                alt30 = 2
                                LA30_0 = self.input.LA(1)

                                if ((COLOR <= LA30_0 <= DATE) or (FALSE <= LA30_0 <= FLOAT) or (INT <= LA30_0 <= NONE) or (STRING <= LA30_0 <= STRING3) or LA30_0 == TRUE or LA30_0 == 30 or LA30_0 == 38 or LA30_0 == 56 or LA30_0 == 63 or LA30_0 == 65) :
                                    alt30 = 1
                                if alt30 == 1:
                                    # src/ll/UL4.g:431:7: e3= expr_if
                                    pass 
                                    self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2257)
                                    e3 = self.expr_if()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        index2 = e3; 









                            if self._state.backtracking == 0:
                                pass
                                retval.node = ul4c.Slice(self.location, retval.node.start, None, retval.node, index1, index2) if slice else ul4c.Item(self.location, e1.start, None, retval.node, index1) 






                        close = self.match(self.input, 57, self.FOLLOW_57_in_expr_subscript2288)

                        if self._state.backtracking == 0:
                            pass
                            retval.node.end = self.end(close) 




                    else:
                        break #loop33




                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "expr_subscript"



    # $ANTLR start "expr_neg"
    # src/ll/UL4.g:440:1: expr_neg returns [node] : (e1= expr_subscript |minus= '-' e2= expr_neg );
    def expr_neg(self, ):
        node = None


        minus = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:441:2: (e1= expr_subscript |minus= '-' e2= expr_neg )
                alt34 = 2
                LA34_0 = self.input.LA(1)

                if ((COLOR <= LA34_0 <= DATE) or (FALSE <= LA34_0 <= FLOAT) or (INT <= LA34_0 <= NONE) or (STRING <= LA34_0 <= STRING3) or LA34_0 == TRUE or LA34_0 == 30 or LA34_0 == 56 or LA34_0 == 65) :
                    alt34 = 1
                elif (LA34_0 == 38) :
                    alt34 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae


                if alt34 == 1:
                    # src/ll/UL4.g:442:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_neg2316)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ((e1 is not None) and [e1.node] or [None])[0] 




                elif alt34 == 2:
                    # src/ll/UL4.g:444:3: minus= '-' e2= expr_neg
                    pass 
                    minus = self.match(self.input, 38, self.FOLLOW_38_in_expr_neg2327)

                    self._state.following.append(self.FOLLOW_expr_neg_in_expr_neg2331)
                    e2 = self.expr_neg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.location, self.start(minus), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_neg"



    # $ANTLR start "expr_mul"
    # src/ll/UL4.g:448:1: expr_mul returns [node] : e1= expr_neg ( ( '*' | '/' | '//' | '%' ) e2= expr_neg )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:449:2: (e1= expr_neg ( ( '*' | '/' | '//' | '%' ) e2= expr_neg )* )
                # src/ll/UL4.g:450:3: e1= expr_neg ( ( '*' | '/' | '//' | '%' ) e2= expr_neg )*
                pass 
                self._state.following.append(self.FOLLOW_expr_neg_in_expr_mul2354)
                e1 = self.expr_neg()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:451:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_neg )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 28 or LA36_0 == 32 or (41 <= LA36_0 <= 42)) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:452:4: ( '*' | '/' | '//' | '%' ) e2= expr_neg
                        pass 
                        # src/ll/UL4.g:452:4: ( '*' | '/' | '//' | '%' )
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
                            # src/ll/UL4.g:453:5: '*'
                            pass 
                            self.match(self.input, 32, self.FOLLOW_32_in_expr_mul2371)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:455:5: '/'
                            pass 
                            self.match(self.input, 41, self.FOLLOW_41_in_expr_mul2384)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt35 == 3:
                            # src/ll/UL4.g:457:5: '//'
                            pass 
                            self.match(self.input, 42, self.FOLLOW_42_in_expr_mul2397)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt35 == 4:
                            # src/ll/UL4.g:459:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_mul2410)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_neg_in_expr_mul2424)
                        e2 = self.expr_neg()

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

    # $ANTLR end "expr_mul"



    # $ANTLR start "expr_add"
    # src/ll/UL4.g:466:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:467:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:468:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2452)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:469:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 35 or LA38_0 == 38) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:470:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:470:4: ( '+' | '-' )
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
                            # src/ll/UL4.g:471:5: '+'
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr_add2469)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:473:5: '-'
                            pass 
                            self.match(self.input, 38, self.FOLLOW_38_in_expr_add2482)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2496)
                        e2 = self.expr_mul()

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

    # $ANTLR end "expr_add"



    # $ANTLR start "expr_bitshift"
    # src/ll/UL4.g:480:1: expr_bitshift returns [AST node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:481:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:482:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2524)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:483:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 47 or LA40_0 == 54) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:484:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:484:4: ( '<<' | '>>' )
                        alt39 = 2
                        LA39_0 = self.input.LA(1)

                        if (LA39_0 == 47) :
                            alt39 = 1
                        elif (LA39_0 == 54) :
                            alt39 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:485:5: '<<'
                            pass 
                            self.match(self.input, 47, self.FOLLOW_47_in_expr_bitshift2541)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:487:5: '>>'
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_bitshift2554)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2568)
                        e2 = self.expr_add()

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

    # $ANTLR end "expr_bitshift"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:494:1: expr_cmp returns [node] : e1= expr_bitshift ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitshift )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:495:2: (e1= expr_bitshift ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitshift )* )
                # src/ll/UL4.g:496:3: e1= expr_bitshift ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_cmp2596)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:497:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitshift )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 27 or LA42_0 == 46 or LA42_0 == 49 or (51 <= LA42_0 <= 53)) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:498:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitshift
                        pass 
                        # src/ll/UL4.g:498:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt41 = 6
                        LA41 = self.input.LA(1)
                        if LA41 == 51:
                            alt41 = 1
                        elif LA41 == 27:
                            alt41 = 2
                        elif LA41 == 46:
                            alt41 = 3
                        elif LA41 == 49:
                            alt41 = 4
                        elif LA41 == 52:
                            alt41 = 5
                        elif LA41 == 53:
                            alt41 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 41, 0, self.input)

                            raise nvae


                        if alt41 == 1:
                            # src/ll/UL4.g:499:5: '=='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr_cmp2613)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt41 == 2:
                            # src/ll/UL4.g:501:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr_cmp2626)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt41 == 3:
                            # src/ll/UL4.g:503:5: '<'
                            pass 
                            self.match(self.input, 46, self.FOLLOW_46_in_expr_cmp2639)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt41 == 4:
                            # src/ll/UL4.g:505:5: '<='
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_cmp2652)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt41 == 5:
                            # src/ll/UL4.g:507:5: '>'
                            pass 
                            self.match(self.input, 52, self.FOLLOW_52_in_expr_cmp2665)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt41 == 6:
                            # src/ll/UL4.g:509:5: '>='
                            pass 
                            self.match(self.input, 53, self.FOLLOW_53_in_expr_cmp2678)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_cmp2692)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop42





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_contain"
    # src/ll/UL4.g:516:1: expr_contain returns [node] : e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? ;
    def expr_contain(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:517:2: (e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? )
                # src/ll/UL4.g:518:3: e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )?
                pass 
                self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2720)
                e1 = self.expr_cmp()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = e1 



                # src/ll/UL4.g:519:3: ( ( 'not' )? 'in' e2= expr_cmp )?
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if ((62 <= LA44_0 <= 63)) :
                    alt44 = 1
                if alt44 == 1:
                    # src/ll/UL4.g:520:4: ( 'not' )? 'in' e2= expr_cmp
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains 



                    # src/ll/UL4.g:521:4: ( 'not' )?
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 63) :
                        alt43 = 1
                    if alt43 == 1:
                        # src/ll/UL4.g:522:5: 'not'
                        pass 
                        self.match(self.input, 63, self.FOLLOW_63_in_expr_contain2742)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains 






                    self.match(self.input, 62, self.FOLLOW_62_in_expr_contain2755)

                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2762)
                    e2 = self.expr_cmp()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = cls.make(self.location, node.start, e2.end, node, e2) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_contain"



    # $ANTLR start "expr_not"
    # src/ll/UL4.g:530:1: expr_not returns [node] : (e1= expr_contain |n= 'not' e2= expr_not );
    def expr_not(self, ):
        node = None


        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:531:2: (e1= expr_contain |n= 'not' e2= expr_not )
                alt45 = 2
                LA45_0 = self.input.LA(1)

                if ((COLOR <= LA45_0 <= DATE) or (FALSE <= LA45_0 <= FLOAT) or (INT <= LA45_0 <= NONE) or (STRING <= LA45_0 <= STRING3) or LA45_0 == TRUE or LA45_0 == 30 or LA45_0 == 38 or LA45_0 == 56 or LA45_0 == 65) :
                    alt45 = 1
                elif (LA45_0 == 63) :
                    alt45 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 45, 0, self.input)

                    raise nvae


                if alt45 == 1:
                    # src/ll/UL4.g:532:3: e1= expr_contain
                    pass 
                    self._state.following.append(self.FOLLOW_expr_contain_in_expr_not2790)
                    e1 = self.expr_contain()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt45 == 2:
                    # src/ll/UL4.g:534:3: n= 'not' e2= expr_not
                    pass 
                    n = self.match(self.input, 63, self.FOLLOW_63_in_expr_not2801)

                    self._state.following.append(self.FOLLOW_expr_not_in_expr_not2805)
                    e2 = self.expr_not()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(self.location, self.start(n), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_not"



    # $ANTLR start "expr_and"
    # src/ll/UL4.g:539:1: expr_and returns [node] : e1= expr_not ( 'and' e2= expr_not )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:540:2: (e1= expr_not ( 'and' e2= expr_not )* )
                # src/ll/UL4.g:541:3: e1= expr_not ( 'and' e2= expr_not )*
                pass 
                self._state.following.append(self.FOLLOW_expr_not_in_expr_and2829)
                e1 = self.expr_not()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:542:3: ( 'and' e2= expr_not )*
                while True: #loop46
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == 58) :
                        alt46 = 1


                    if alt46 == 1:
                        # src/ll/UL4.g:543:4: 'and' e2= expr_not
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_and2840)

                        self._state.following.append(self.FOLLOW_expr_not_in_expr_and2847)
                        e2 = self.expr_not()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop46





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_and"



    # $ANTLR start "expr_or"
    # src/ll/UL4.g:549:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:550:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:551:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or2875)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:552:3: ( 'or' e2= expr_and )*
                while True: #loop47
                    alt47 = 2
                    LA47_0 = self.input.LA(1)

                    if (LA47_0 == 64) :
                        alt47 = 1


                    if alt47 == 1:
                        # src/ll/UL4.g:553:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 64, self.FOLLOW_64_in_expr_or2886)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or2893)
                        e2 = self.expr_and()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop47





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_or"



    # $ANTLR start "expr_if"
    # src/ll/UL4.g:559:1: expr_if returns [AST node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:560:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:561:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if2921)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:562:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if (LA48_0 == 61) :
                    LA48_1 = self.input.LA(2)

                    if (self.synpred72_UL4()) :
                        alt48 = 1
                if alt48 == 1:
                    # src/ll/UL4.g:563:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 61, self.FOLLOW_61_in_expr_if2932)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if2939)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 59, self.FOLLOW_59_in_expr_if2944)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if2951)
                    e3 = self.expr_or()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.IfExpr.make(self.location, e1.start, e3.end, node, e2, e3) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_if"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:570:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:571:2: (ege= generatorexpression |e1= expr_if )
                alt49 = 2
                LA49 = self.input.LA(1)
                if LA49 == NONE:
                    LA49_1 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 1, self.input)

                        raise nvae


                elif LA49 == FALSE:
                    LA49_2 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 2, self.input)

                        raise nvae


                elif LA49 == TRUE:
                    LA49_3 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 3, self.input)

                        raise nvae


                elif LA49 == INT:
                    LA49_4 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 4, self.input)

                        raise nvae


                elif LA49 == FLOAT:
                    LA49_5 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 5, self.input)

                        raise nvae


                elif LA49 == STRING:
                    LA49_6 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 6, self.input)

                        raise nvae


                elif LA49 == STRING3:
                    LA49_7 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 7, self.input)

                        raise nvae


                elif LA49 == DATE:
                    LA49_8 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 8, self.input)

                        raise nvae


                elif LA49 == COLOR:
                    LA49_9 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 9, self.input)

                        raise nvae


                elif LA49 == NAME:
                    LA49_10 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 10, self.input)

                        raise nvae


                elif LA49 == 56:
                    LA49_11 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 11, self.input)

                        raise nvae


                elif LA49 == 65:
                    LA49_12 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 12, self.input)

                        raise nvae


                elif LA49 == 30:
                    LA49_13 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 13, self.input)

                        raise nvae


                elif LA49 == 38:
                    LA49_14 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 14, self.input)

                        raise nvae


                elif LA49 == 63:
                    LA49_15 = self.input.LA(2)

                    if (self.synpred73_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 49, 0, self.input)

                    raise nvae


                if alt49 == 1:
                    # src/ll/UL4.g:571:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg2975)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt49 == 2:
                    # src/ll/UL4.g:572:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg2984)
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
    # src/ll/UL4.g:575:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:576:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt50 = 2
                LA50 = self.input.LA(1)
                if LA50 == NONE:
                    LA50_1 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 1, self.input)

                        raise nvae


                elif LA50 == FALSE:
                    LA50_2 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 2, self.input)

                        raise nvae


                elif LA50 == TRUE:
                    LA50_3 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 3, self.input)

                        raise nvae


                elif LA50 == INT:
                    LA50_4 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 4, self.input)

                        raise nvae


                elif LA50 == FLOAT:
                    LA50_5 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 5, self.input)

                        raise nvae


                elif LA50 == STRING:
                    LA50_6 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 6, self.input)

                        raise nvae


                elif LA50 == STRING3:
                    LA50_7 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 7, self.input)

                        raise nvae


                elif LA50 == DATE:
                    LA50_8 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 8, self.input)

                        raise nvae


                elif LA50 == COLOR:
                    LA50_9 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 9, self.input)

                        raise nvae


                elif LA50 == NAME:
                    LA50_10 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 10, self.input)

                        raise nvae


                elif LA50 == 56:
                    LA50_11 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 11, self.input)

                        raise nvae


                elif LA50 == 65:
                    LA50_12 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 12, self.input)

                        raise nvae


                elif LA50 == 30:
                    LA50_13 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 13, self.input)

                        raise nvae


                elif LA50 == 38:
                    LA50_14 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 14, self.input)

                        raise nvae


                elif LA50 == 63:
                    LA50_15 = self.input.LA(2)

                    if (self.synpred74_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 15, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 50, 0, self.input)

                    raise nvae


                if alt50 == 1:
                    # src/ll/UL4.g:576:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3003)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3005)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt50 == 2:
                    # src/ll/UL4.g:577:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3014)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3016)

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
    # src/ll/UL4.g:583:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:584:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:585:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3041)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 62, self.FOLLOW_62_in_for_3045)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3051)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.For(self.location, self.start(n.start), e.end, ((n is not None) and [n.lvalue] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3057)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:594:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:595:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |e= expression EOF )
                alt51 = 10
                LA51 = self.input.LA(1)
                if LA51 == NONE:
                    LA51_1 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 1, self.input)

                        raise nvae


                elif LA51 == FALSE:
                    LA51_2 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 2, self.input)

                        raise nvae


                elif LA51 == TRUE:
                    LA51_3 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 3, self.input)

                        raise nvae


                elif LA51 == INT:
                    LA51_4 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 4, self.input)

                        raise nvae


                elif LA51 == FLOAT:
                    LA51_5 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 5, self.input)

                        raise nvae


                elif LA51 == STRING:
                    LA51_6 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 6, self.input)

                        raise nvae


                elif LA51 == STRING3:
                    LA51_7 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 7, self.input)

                        raise nvae


                elif LA51 == DATE:
                    LA51_8 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 8, self.input)

                        raise nvae


                elif LA51 == COLOR:
                    LA51_9 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 9, self.input)

                        raise nvae


                elif LA51 == NAME:
                    LA51_10 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 10, self.input)

                        raise nvae


                elif LA51 == 56:
                    LA51_11 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 11, self.input)

                        raise nvae


                elif LA51 == 65:
                    LA51_12 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 12, self.input)

                        raise nvae


                elif LA51 == 30:
                    LA51_13 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt51 = 1
                    elif (self.synpred76_UL4()) :
                        alt51 = 2
                    elif (self.synpred77_UL4()) :
                        alt51 = 3
                    elif (self.synpred78_UL4()) :
                        alt51 = 4
                    elif (self.synpred79_UL4()) :
                        alt51 = 5
                    elif (self.synpred80_UL4()) :
                        alt51 = 6
                    elif (self.synpred81_UL4()) :
                        alt51 = 7
                    elif (self.synpred82_UL4()) :
                        alt51 = 8
                    elif (self.synpred83_UL4()) :
                        alt51 = 9
                    elif (True) :
                        alt51 = 10
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 13, self.input)

                        raise nvae


                elif LA51 == 38 or LA51 == 63:
                    alt51 = 10
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 51, 0, self.input)

                    raise nvae


                if alt51 == 1:
                    # src/ll/UL4.g:595:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3078)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 50, self.FOLLOW_50_in_statement3080)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3084)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3086)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.lvalue] or [None])[0], e) 




                elif alt51 == 2:
                    # src/ll/UL4.g:596:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3095)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement3097)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3101)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3103)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 3:
                    # src/ll/UL4.g:597:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3112)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_statement3114)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3118)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3120)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 4:
                    # src/ll/UL4.g:598:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3129)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 34, self.FOLLOW_34_in_statement3131)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3135)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3137)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 5:
                    # src/ll/UL4.g:599:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3146)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 44, self.FOLLOW_44_in_statement3148)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3152)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3154)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 6:
                    # src/ll/UL4.g:600:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3163)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 43, self.FOLLOW_43_in_statement3165)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3169)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3171)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 7:
                    # src/ll/UL4.g:601:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3180)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3182)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3186)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3188)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 8:
                    # src/ll/UL4.g:602:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3197)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 48, self.FOLLOW_48_in_statement3199)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3203)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3205)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 9:
                    # src/ll/UL4.g:603:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3214)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 55, self.FOLLOW_55_in_statement3216)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3220)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3222)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 10:
                    # src/ll/UL4.g:604:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3231)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3233)

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

        # src/ll/UL4.g:314:4: (e_list= list )
        # src/ll/UL4.g:314:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred20_UL41513)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred20_UL4"



    # $ANTLR start "synpred21_UL4"
    def synpred21_UL4_fragment(self, ):
        e_listcomp = None

        # src/ll/UL4.g:315:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:315:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred21_UL41522)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred21_UL4"



    # $ANTLR start "synpred22_UL4"
    def synpred22_UL4_fragment(self, ):
        e_dict = None

        # src/ll/UL4.g:316:4: (e_dict= dict )
        # src/ll/UL4.g:316:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred22_UL41531)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred22_UL4"



    # $ANTLR start "synpred23_UL4"
    def synpred23_UL4_fragment(self, ):
        e_dictcomp = None

        # src/ll/UL4.g:317:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:317:4: e_dictcomp= dictcomprehension
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

        # src/ll/UL4.g:318:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:318:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 30, self.FOLLOW_30_in_synpred24_UL41549)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred24_UL41553)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 31, self.FOLLOW_31_in_synpred24_UL41557)



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred25_UL4"
    def synpred25_UL4_fragment(self, ):
        n = None

        # src/ll/UL4.g:333:3: (n= expr_subscript )
        # src/ll/UL4.g:333:3: n= expr_subscript
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred25_UL41597)
        n = self.expr_subscript()

        self._state.following.pop()



    # $ANTLR end "synpred25_UL4"



    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        n0 = None

        # src/ll/UL4.g:335:3: ( '(' n0= nestedlvalue ',' ')' )
        # src/ll/UL4.g:335:3: '(' n0= nestedlvalue ',' ')'
        pass 
        self.match(self.input, 30, self.FOLLOW_30_in_synpred26_UL41606)

        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred26_UL41610)
        n0 = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 37, self.FOLLOW_37_in_synpred26_UL41612)

        self.match(self.input, 31, self.FOLLOW_31_in_synpred26_UL41614)



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred72_UL4"
    def synpred72_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:563:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:563:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 61, self.FOLLOW_61_in_synpred72_UL42932)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred72_UL42939)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 59, self.FOLLOW_59_in_synpred72_UL42944)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred72_UL42951)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred72_UL4"



    # $ANTLR start "synpred73_UL4"
    def synpred73_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:571:4: (ege= generatorexpression )
        # src/ll/UL4.g:571:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred73_UL42975)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred73_UL4"



    # $ANTLR start "synpred74_UL4"
    def synpred74_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:576:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:576:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred74_UL43003)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred74_UL43005)



    # $ANTLR end "synpred74_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:595:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:595:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred75_UL43078)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 50, self.FOLLOW_50_in_synpred75_UL43080)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred75_UL43084)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred75_UL43086)



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:596:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:596:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred76_UL43095)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred76_UL43097)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred76_UL43101)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred76_UL43103)



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:597:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:597:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred77_UL43112)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred77_UL43114)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred77_UL43118)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL43120)



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:598:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:598:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred78_UL43129)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 34, self.FOLLOW_34_in_synpred78_UL43131)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred78_UL43135)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43137)



    # $ANTLR end "synpred78_UL4"



    # $ANTLR start "synpred79_UL4"
    def synpred79_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:599:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:599:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred79_UL43146)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 44, self.FOLLOW_44_in_synpred79_UL43148)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred79_UL43152)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred79_UL43154)



    # $ANTLR end "synpred79_UL4"



    # $ANTLR start "synpred80_UL4"
    def synpred80_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:600:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:600:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred80_UL43163)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 43, self.FOLLOW_43_in_synpred80_UL43165)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred80_UL43169)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred80_UL43171)



    # $ANTLR end "synpred80_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:601:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:601:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred81_UL43180)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred81_UL43182)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred81_UL43186)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred81_UL43188)



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:602:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:602:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred82_UL43197)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 48, self.FOLLOW_48_in_synpred82_UL43199)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred82_UL43203)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred82_UL43205)



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:603:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:603:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred83_UL43214)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 55, self.FOLLOW_55_in_synpred83_UL43216)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred83_UL43220)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43222)



    # $ANTLR end "synpred83_UL4"




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
    FOLLOW_56_in_list1056 = frozenset([57])
    FOLLOW_57_in_list1062 = frozenset([1])
    FOLLOW_56_in_list1073 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_list1081 = frozenset([37, 57])
    FOLLOW_37_in_list1092 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_list1099 = frozenset([37, 57])
    FOLLOW_37_in_list1110 = frozenset([57])
    FOLLOW_57_in_list1117 = frozenset([1])
    FOLLOW_56_in_listcomprehension1145 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_listcomprehension1151 = frozenset([60])
    FOLLOW_60_in_listcomprehension1155 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_listcomprehension1161 = frozenset([62])
    FOLLOW_62_in_listcomprehension1165 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_listcomprehension1171 = frozenset([57, 61])
    FOLLOW_61_in_listcomprehension1180 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_listcomprehension1187 = frozenset([57])
    FOLLOW_57_in_listcomprehension1200 = frozenset([1])
    FOLLOW_expr_if_in_dictitem1225 = frozenset([45])
    FOLLOW_45_in_dictitem1229 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_dictitem1235 = frozenset([1])
    FOLLOW_65_in_dict1256 = frozenset([66])
    FOLLOW_66_in_dict1262 = frozenset([1])
    FOLLOW_65_in_dict1273 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_dictitem_in_dict1281 = frozenset([37, 66])
    FOLLOW_37_in_dict1292 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_dictitem_in_dict1299 = frozenset([37, 66])
    FOLLOW_37_in_dict1310 = frozenset([66])
    FOLLOW_66_in_dict1317 = frozenset([1])
    FOLLOW_65_in_dictcomprehension1345 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_dictcomprehension1351 = frozenset([45])
    FOLLOW_45_in_dictcomprehension1355 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_dictcomprehension1361 = frozenset([60])
    FOLLOW_60_in_dictcomprehension1365 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_dictcomprehension1371 = frozenset([62])
    FOLLOW_62_in_dictcomprehension1375 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_dictcomprehension1381 = frozenset([61, 66])
    FOLLOW_61_in_dictcomprehension1390 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_dictcomprehension1397 = frozenset([66])
    FOLLOW_66_in_dictcomprehension1410 = frozenset([1])
    FOLLOW_expr_if_in_generatorexpression1438 = frozenset([60])
    FOLLOW_60_in_generatorexpression1444 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_generatorexpression1450 = frozenset([62])
    FOLLOW_62_in_generatorexpression1454 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_generatorexpression1460 = frozenset([1, 61])
    FOLLOW_61_in_generatorexpression1471 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_generatorexpression1478 = frozenset([1])
    FOLLOW_literal_in_atom1504 = frozenset([1])
    FOLLOW_list_in_atom1513 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1522 = frozenset([1])
    FOLLOW_dict_in_atom1531 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1540 = frozenset([1])
    FOLLOW_30_in_atom1549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_generatorexpression_in_atom1553 = frozenset([31])
    FOLLOW_31_in_atom1557 = frozenset([1])
    FOLLOW_30_in_atom1566 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_atom1570 = frozenset([31])
    FOLLOW_31_in_atom1574 = frozenset([1])
    FOLLOW_expr_subscript_in_nestedlvalue1597 = frozenset([1])
    FOLLOW_30_in_nestedlvalue1606 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_nestedlvalue1610 = frozenset([37])
    FOLLOW_37_in_nestedlvalue1612 = frozenset([31])
    FOLLOW_31_in_nestedlvalue1614 = frozenset([1])
    FOLLOW_30_in_nestedlvalue1623 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_nestedlvalue1629 = frozenset([37])
    FOLLOW_37_in_nestedlvalue1633 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_nestedlvalue1639 = frozenset([31, 37])
    FOLLOW_37_in_nestedlvalue1650 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_nestedlvalue1657 = frozenset([31, 37])
    FOLLOW_37_in_nestedlvalue1668 = frozenset([31])
    FOLLOW_31_in_nestedlvalue1673 = frozenset([1])
    FOLLOW_atom_in_expr_subscript1701 = frozenset([1, 30, 40, 56])
    FOLLOW_40_in_expr_subscript1717 = frozenset([14])
    FOLLOW_name_in_expr_subscript1724 = frozenset([1, 30, 40, 56])
    FOLLOW_30_in_expr_subscript1740 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 31, 32, 33, 38, 56, 63, 65])
    FOLLOW_33_in_expr_subscript1770 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1774 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1782 = frozenset([31])
    FOLLOW_32_in_expr_subscript1800 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1804 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1819 = frozenset([33])
    FOLLOW_33_in_expr_subscript1826 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1830 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1845 = frozenset([31])
    FOLLOW_exprarg_in_expr_subscript1865 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1880 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1889 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1911 = frozenset([14])
    FOLLOW_name_in_expr_subscript1920 = frozenset([50])
    FOLLOW_50_in_expr_subscript1922 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1926 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1948 = frozenset([32])
    FOLLOW_32_in_expr_subscript1955 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1959 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript1981 = frozenset([33])
    FOLLOW_33_in_expr_subscript1988 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript1992 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript2007 = frozenset([31])
    FOLLOW_name_in_expr_subscript2027 = frozenset([50])
    FOLLOW_50_in_expr_subscript2029 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript2033 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript2048 = frozenset([14])
    FOLLOW_name_in_expr_subscript2057 = frozenset([50])
    FOLLOW_50_in_expr_subscript2059 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript2063 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript2085 = frozenset([32])
    FOLLOW_32_in_expr_subscript2092 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript2096 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript2118 = frozenset([33])
    FOLLOW_33_in_expr_subscript2125 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_exprarg_in_expr_subscript2129 = frozenset([31, 37])
    FOLLOW_37_in_expr_subscript2144 = frozenset([31])
    FOLLOW_31_in_expr_subscript2157 = frozenset([1, 30, 40, 56])
    FOLLOW_56_in_expr_subscript2173 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 45, 56, 63, 65])
    FOLLOW_45_in_expr_subscript2184 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 57, 63, 65])
    FOLLOW_expr_if_in_expr_subscript2199 = frozenset([57])
    FOLLOW_expr_if_in_expr_subscript2223 = frozenset([45, 57])
    FOLLOW_45_in_expr_subscript2238 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 57, 63, 65])
    FOLLOW_expr_if_in_expr_subscript2257 = frozenset([57])
    FOLLOW_57_in_expr_subscript2288 = frozenset([1, 30, 40, 56])
    FOLLOW_expr_subscript_in_expr_neg2316 = frozenset([1])
    FOLLOW_38_in_expr_neg2327 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_neg_in_expr_neg2331 = frozenset([1])
    FOLLOW_expr_neg_in_expr_mul2354 = frozenset([1, 28, 32, 41, 42])
    FOLLOW_32_in_expr_mul2371 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_41_in_expr_mul2384 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_42_in_expr_mul2397 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_28_in_expr_mul2410 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_neg_in_expr_mul2424 = frozenset([1, 28, 32, 41, 42])
    FOLLOW_expr_mul_in_expr_add2452 = frozenset([1, 35, 38])
    FOLLOW_35_in_expr_add2469 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_38_in_expr_add2482 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_mul_in_expr_add2496 = frozenset([1, 35, 38])
    FOLLOW_expr_add_in_expr_bitshift2524 = frozenset([1, 47, 54])
    FOLLOW_47_in_expr_bitshift2541 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_54_in_expr_bitshift2554 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_add_in_expr_bitshift2568 = frozenset([1, 47, 54])
    FOLLOW_expr_bitshift_in_expr_cmp2596 = frozenset([1, 27, 46, 49, 51, 52, 53])
    FOLLOW_51_in_expr_cmp2613 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_27_in_expr_cmp2626 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_46_in_expr_cmp2639 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_49_in_expr_cmp2652 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_52_in_expr_cmp2665 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_53_in_expr_cmp2678 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_bitshift_in_expr_cmp2692 = frozenset([1, 27, 46, 49, 51, 52, 53])
    FOLLOW_expr_cmp_in_expr_contain2720 = frozenset([1, 62, 63])
    FOLLOW_63_in_expr_contain2742 = frozenset([62])
    FOLLOW_62_in_expr_contain2755 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 65])
    FOLLOW_expr_cmp_in_expr_contain2762 = frozenset([1])
    FOLLOW_expr_contain_in_expr_not2790 = frozenset([1])
    FOLLOW_63_in_expr_not2801 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_not_in_expr_not2805 = frozenset([1])
    FOLLOW_expr_not_in_expr_and2829 = frozenset([1, 58])
    FOLLOW_58_in_expr_and2840 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_not_in_expr_and2847 = frozenset([1, 58])
    FOLLOW_expr_and_in_expr_or2875 = frozenset([1, 64])
    FOLLOW_64_in_expr_or2886 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_and_in_expr_or2893 = frozenset([1, 64])
    FOLLOW_expr_or_in_expr_if2921 = frozenset([1, 61])
    FOLLOW_61_in_expr_if2932 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_or_in_expr_if2939 = frozenset([59])
    FOLLOW_59_in_expr_if2944 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_or_in_expr_if2951 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg2975 = frozenset([1])
    FOLLOW_expr_if_in_exprarg2984 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3003 = frozenset([])
    FOLLOW_EOF_in_expression3005 = frozenset([1])
    FOLLOW_expr_if_in_expression3014 = frozenset([])
    FOLLOW_EOF_in_expression3016 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3041 = frozenset([62])
    FOLLOW_62_in_for_3045 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_for_3051 = frozenset([])
    FOLLOW_EOF_in_for_3057 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3078 = frozenset([50])
    FOLLOW_50_in_statement3080 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3084 = frozenset([])
    FOLLOW_EOF_in_statement3086 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3095 = frozenset([36])
    FOLLOW_36_in_statement3097 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3101 = frozenset([])
    FOLLOW_EOF_in_statement3103 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3112 = frozenset([39])
    FOLLOW_39_in_statement3114 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3118 = frozenset([])
    FOLLOW_EOF_in_statement3120 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3129 = frozenset([34])
    FOLLOW_34_in_statement3131 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3135 = frozenset([])
    FOLLOW_EOF_in_statement3137 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3146 = frozenset([44])
    FOLLOW_44_in_statement3148 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3152 = frozenset([])
    FOLLOW_EOF_in_statement3154 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3163 = frozenset([43])
    FOLLOW_43_in_statement3165 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3169 = frozenset([])
    FOLLOW_EOF_in_statement3171 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3180 = frozenset([29])
    FOLLOW_29_in_statement3182 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3186 = frozenset([])
    FOLLOW_EOF_in_statement3188 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3197 = frozenset([48])
    FOLLOW_48_in_statement3199 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3203 = frozenset([])
    FOLLOW_EOF_in_statement3205 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3214 = frozenset([55])
    FOLLOW_55_in_statement3216 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_statement3220 = frozenset([])
    FOLLOW_EOF_in_statement3222 = frozenset([1])
    FOLLOW_expression_in_statement3231 = frozenset([])
    FOLLOW_EOF_in_statement3233 = frozenset([1])
    FOLLOW_list_in_synpred20_UL41513 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred21_UL41522 = frozenset([1])
    FOLLOW_dict_in_synpred22_UL41531 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred23_UL41540 = frozenset([1])
    FOLLOW_30_in_synpred24_UL41549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_generatorexpression_in_synpred24_UL41553 = frozenset([31])
    FOLLOW_31_in_synpred24_UL41557 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred25_UL41597 = frozenset([1])
    FOLLOW_30_in_synpred26_UL41606 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 56, 65])
    FOLLOW_nestedlvalue_in_synpred26_UL41610 = frozenset([37])
    FOLLOW_37_in_synpred26_UL41612 = frozenset([31])
    FOLLOW_31_in_synpred26_UL41614 = frozenset([1])
    FOLLOW_61_in_synpred72_UL42932 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_or_in_synpred72_UL42939 = frozenset([59])
    FOLLOW_59_in_synpred72_UL42944 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_or_in_synpred72_UL42951 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred73_UL42975 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred74_UL43003 = frozenset([])
    FOLLOW_EOF_in_synpred74_UL43005 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred75_UL43078 = frozenset([50])
    FOLLOW_50_in_synpred75_UL43080 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred75_UL43084 = frozenset([])
    FOLLOW_EOF_in_synpred75_UL43086 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred76_UL43095 = frozenset([36])
    FOLLOW_36_in_synpred76_UL43097 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred76_UL43101 = frozenset([])
    FOLLOW_EOF_in_synpred76_UL43103 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred77_UL43112 = frozenset([39])
    FOLLOW_39_in_synpred77_UL43114 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred77_UL43118 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL43120 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred78_UL43129 = frozenset([34])
    FOLLOW_34_in_synpred78_UL43131 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred78_UL43135 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43137 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred79_UL43146 = frozenset([44])
    FOLLOW_44_in_synpred79_UL43148 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred79_UL43152 = frozenset([])
    FOLLOW_EOF_in_synpred79_UL43154 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred80_UL43163 = frozenset([43])
    FOLLOW_43_in_synpred80_UL43165 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred80_UL43169 = frozenset([])
    FOLLOW_EOF_in_synpred80_UL43171 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred81_UL43180 = frozenset([29])
    FOLLOW_29_in_synpred81_UL43182 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred81_UL43186 = frozenset([])
    FOLLOW_EOF_in_synpred81_UL43188 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred82_UL43197 = frozenset([48])
    FOLLOW_48_in_synpred82_UL43199 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred82_UL43203 = frozenset([])
    FOLLOW_EOF_in_synpred82_UL43205 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred83_UL43214 = frozenset([55])
    FOLLOW_55_in_synpred83_UL43216 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 30, 38, 56, 63, 65])
    FOLLOW_expr_if_in_synpred83_UL43220 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43222 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
