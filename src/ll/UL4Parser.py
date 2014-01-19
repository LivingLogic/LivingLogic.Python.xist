# $ANTLR 3.5 src/ll/UL4.g 2014-01-16 17:34:13

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
    "'and'", "'else'", "'for'", "'if'", "'in'", "'not'", "'or'", "'{'", 
    "'|'", "'|='", "'}'", "'~'"
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

                if (LA5_0 == 58) :
                    LA5_1 = self.input.LA(2)

                    if (LA5_1 == 59) :
                        alt5 = 1
                    elif ((COLOR <= LA5_1 <= DATE) or (FALSE <= LA5_1 <= FLOAT) or (INT <= LA5_1 <= NONE) or (STRING <= LA5_1 <= STRING3) or LA5_1 == TRUE or LA5_1 == 32 or LA5_1 == 40 or LA5_1 == 58 or LA5_1 == 67 or LA5_1 == 69 or LA5_1 == 73) :
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
                    open = self.match(self.input, 58, self.FOLLOW_58_in_list1056)

                    close = self.match(self.input, 59, self.FOLLOW_59_in_list1062)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.List(self.location, self.start(open), self.end(close)) 




                elif alt5 == 2:
                    # src/ll/UL4.g:220:3: open= '[' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= ']'
                    pass 
                    open = self.match(self.input, 58, self.FOLLOW_58_in_list1073)

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

                        if (LA3_0 == 39) :
                            LA3_1 = self.input.LA(2)

                            if ((COLOR <= LA3_1 <= DATE) or (FALSE <= LA3_1 <= FLOAT) or (INT <= LA3_1 <= NONE) or (STRING <= LA3_1 <= STRING3) or LA3_1 == TRUE or LA3_1 == 32 or LA3_1 == 40 or LA3_1 == 58 or LA3_1 == 67 or LA3_1 == 69 or LA3_1 == 73) :
                                alt3 = 1




                        if alt3 == 1:
                            # src/ll/UL4.g:223:4: ',' e2= expr_if
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_list1092)

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

                    if (LA4_0 == 39) :
                        alt4 = 1
                    if alt4 == 1:
                        # src/ll/UL4.g:226:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_list1110)




                    close = self.match(self.input, 59, self.FOLLOW_59_in_list1117)

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
                open = self.match(self.input, 58, self.FOLLOW_58_in_listcomprehension1145)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1151)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_listcomprehension1155)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_listcomprehension1161)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_listcomprehension1165)

                self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1171)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:242:3: ( 'if' condition= expr_if )?
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 65) :
                    alt6 = 1
                if alt6 == 1:
                    # src/ll/UL4.g:243:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_listcomprehension1180)

                    self._state.following.append(self.FOLLOW_expr_if_in_listcomprehension1187)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 59, self.FOLLOW_59_in_listcomprehension1200)

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

                self.match(self.input, 47, self.FOLLOW_47_in_dictitem1229)

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

                if (LA9_0 == 69) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 72) :
                        alt9 = 1
                    elif ((COLOR <= LA9_1 <= DATE) or (FALSE <= LA9_1 <= FLOAT) or (INT <= LA9_1 <= NONE) or (STRING <= LA9_1 <= STRING3) or LA9_1 == TRUE or LA9_1 == 32 or LA9_1 == 40 or LA9_1 == 58 or LA9_1 == 67 or LA9_1 == 69 or LA9_1 == 73) :
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
                    open = self.match(self.input, 69, self.FOLLOW_69_in_dict1256)

                    close = self.match(self.input, 72, self.FOLLOW_72_in_dict1262)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), self.end(close)) 




                elif alt9 == 2:
                    # src/ll/UL4.g:263:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 69, self.FOLLOW_69_in_dict1273)

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

                        if (LA7_0 == 39) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or (STRING <= LA7_1 <= STRING3) or LA7_1 == TRUE or LA7_1 == 32 or LA7_1 == 40 or LA7_1 == 58 or LA7_1 == 67 or LA7_1 == 69 or LA7_1 == 73) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:266:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_dict1292)

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

                    if (LA8_0 == 39) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:269:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_dict1310)




                    close = self.match(self.input, 72, self.FOLLOW_72_in_dict1317)

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
                open = self.match(self.input, 69, self.FOLLOW_69_in_dictcomprehension1345)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1351)
                key = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 47, self.FOLLOW_47_in_dictcomprehension1355)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1361)
                value = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_dictcomprehension1365)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_dictcomprehension1371)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_dictcomprehension1375)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1381)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:287:3: ( 'if' condition= expr_if )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 65) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:288:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_dictcomprehension1390)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1397)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 72, self.FOLLOW_72_in_dictcomprehension1410)

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



                self.match(self.input, 64, self.FOLLOW_64_in_generatorexpression1444)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_generatorexpression1450)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_generatorexpression1454)

                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1460)
                container = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _end = container.end 



                # src/ll/UL4.g:306:3: ( 'if' condition= expr_if )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 65) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:307:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_generatorexpression1471)

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
                elif LA12 == 58:
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


                elif LA12 == 69:
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


                elif LA12 == 32:
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
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1549)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1553)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1557)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.start = self.start(open)
                        node.end = self.end(close)
                        	




                elif alt12 == 7:
                    # src/ll/UL4.g:323:4: open= '(' e_bracket= expr_if close= ')'
                    pass 
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1566)

                    self._state.following.append(self.FOLLOW_expr_if_in_atom1570)
                    e_bracket = self.expr_if()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1574)

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

                if ((COLOR <= LA15_0 <= DATE) or (FALSE <= LA15_0 <= FLOAT) or (INT <= LA15_0 <= NONE) or (STRING <= LA15_0 <= STRING3) or LA15_0 == TRUE or LA15_0 == 58 or LA15_0 == 69) :
                    alt15 = 1
                elif (LA15_0 == 32) :
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
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1606)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1610)
                    n0 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1612)

                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1614)

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n0 is not None) and [n0.lvalue] or [None])[0],) 




                elif alt15 == 3:
                    # src/ll/UL4.g:337:3: '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1623)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1629)
                    n1 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1633)

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

                        if (LA13_0 == 39) :
                            LA13_1 = self.input.LA(2)

                            if ((COLOR <= LA13_1 <= DATE) or (FALSE <= LA13_1 <= FLOAT) or (INT <= LA13_1 <= NONE) or (STRING <= LA13_1 <= STRING3) or LA13_1 == TRUE or LA13_1 == 32 or LA13_1 == 58 or LA13_1 == 69) :
                                alt13 = 1




                        if alt13 == 1:
                            # src/ll/UL4.g:342:4: ',' n3= nestedlvalue
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1650)

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

                    if (LA14_0 == 39) :
                        alt14 = 1
                    if alt14 == 1:
                        # src/ll/UL4.g:345:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1668)




                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1673)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedlvalue"



    # $ANTLR start "index"
    # src/ll/UL4.g:350:1: index returns [node] : (colon= ':' (e2= expr_if )? |e2= expr_if (colon= ':' (e3= expr_if )? )? );
    def index(self, ):
        node = None


        colon = None
        e2 = None
        e3 = None

         
        index1 = None
        index2 = None
        endpos = None
        slice = False
        	
        try:
            try:
                # src/ll/UL4.g:358:2: (colon= ':' (e2= expr_if )? |e2= expr_if (colon= ':' (e3= expr_if )? )? )
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == 47) :
                    alt19 = 1
                elif ((COLOR <= LA19_0 <= DATE) or (FALSE <= LA19_0 <= FLOAT) or (INT <= LA19_0 <= NONE) or (STRING <= LA19_0 <= STRING3) or LA19_0 == TRUE or LA19_0 == 32 or LA19_0 == 40 or LA19_0 == 58 or LA19_0 == 67 or LA19_0 == 69 or LA19_0 == 73) :
                    alt19 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 19, 0, self.input)

                    raise nvae


                if alt19 == 1:
                    # src/ll/UL4.g:359:3: colon= ':' (e2= expr_if )?
                    pass 
                    colon = self.match(self.input, 47, self.FOLLOW_47_in_index1701)

                    if self._state.backtracking == 0:
                        pass
                        endpos = self.end(colon); 



                    # src/ll/UL4.g:360:3: (e2= expr_if )?
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if ((COLOR <= LA16_0 <= DATE) or (FALSE <= LA16_0 <= FLOAT) or (INT <= LA16_0 <= NONE) or (STRING <= LA16_0 <= STRING3) or LA16_0 == TRUE or LA16_0 == 32 or LA16_0 == 40 or LA16_0 == 58 or LA16_0 == 67 or LA16_0 == 69 or LA16_0 == 73) :
                        alt16 = 1
                    if alt16 == 1:
                        # src/ll/UL4.g:361:4: e2= expr_if
                        pass 
                        self._state.following.append(self.FOLLOW_expr_if_in_index1714)
                        e2 = self.expr_if()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            index2 = e2; endpos = e2.end; 






                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Slice(self.location, self.start(colon), endpos, None, index2) 




                elif alt19 == 2:
                    # src/ll/UL4.g:364:3: e2= expr_if (colon= ':' (e3= expr_if )? )?
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_index1732)
                    e2 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index1 = e2; endpos = e2.end; 



                    # src/ll/UL4.g:365:3: (colon= ':' (e3= expr_if )? )?
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == 47) :
                        alt18 = 1
                    if alt18 == 1:
                        # src/ll/UL4.g:366:4: colon= ':' (e3= expr_if )?
                        pass 
                        colon = self.match(self.input, 47, self.FOLLOW_47_in_index1745)

                        if self._state.backtracking == 0:
                            pass
                            slice = True; endpos = self.end(colon); 



                        # src/ll/UL4.g:367:4: (e3= expr_if )?
                        alt17 = 2
                        LA17_0 = self.input.LA(1)

                        if ((COLOR <= LA17_0 <= DATE) or (FALSE <= LA17_0 <= FLOAT) or (INT <= LA17_0 <= NONE) or (STRING <= LA17_0 <= STRING3) or LA17_0 == TRUE or LA17_0 == 32 or LA17_0 == 40 or LA17_0 == 58 or LA17_0 == 67 or LA17_0 == 69 or LA17_0 == 73) :
                            alt17 = 1
                        if alt17 == 1:
                            # src/ll/UL4.g:368:5: e3= expr_if
                            pass 
                            self._state.following.append(self.FOLLOW_expr_if_in_index1760)
                            e3 = self.expr_if()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                index2 = e3; endpos = e3.end; 









                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Slice(self.location, e2.start, endpos, index1, index2) if slice else e2 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "index"


    class expr_subscript_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.expr_subscript_return, self).__init__()

            self.node = None





    # $ANTLR start "expr_subscript"
    # src/ll/UL4.g:374:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= index close= ']' )* ;
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

        try:
            try:
                # src/ll/UL4.g:375:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= index close= ']' )* )
                # src/ll/UL4.g:376:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= index close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript1796)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    retval.node =  e1 



                # src/ll/UL4.g:377:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= index close= ']' )*
                while True: #loop33
                    alt33 = 4
                    LA33 = self.input.LA(1)
                    if LA33 == 42:
                        alt33 = 1
                    elif LA33 == 32:
                        alt33 = 2
                    elif LA33 == 58:
                        alt33 = 3

                    if alt33 == 1:
                        # src/ll/UL4.g:379:4: '.' n= name
                        pass 
                        self.match(self.input, 42, self.FOLLOW_42_in_expr_subscript1812)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript1819)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Attr(self.location, retval.node.start, self.end(n.stop), retval.node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt33 == 2:
                        # src/ll/UL4.g:383:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript1835)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Call(self.location, retval.node.start, None, retval.node) 



                        # src/ll/UL4.g:384:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt32 = 5
                        LA32 = self.input.LA(1)
                        if LA32 == 33:
                            alt32 = 1
                        elif LA32 == 35:
                            alt32 = 2
                        elif LA32 == 34:
                            alt32 = 3
                        elif LA32 == COLOR or LA32 == DATE or LA32 == FALSE or LA32 == FLOAT or LA32 == INT or LA32 == NONE or LA32 == STRING or LA32 == STRING3 or LA32 == TRUE or LA32 == 32 or LA32 == 40 or LA32 == 58 or LA32 == 67 or LA32 == 69 or LA32 == 73:
                            alt32 = 4
                        elif LA32 == NAME:
                            LA32_5 = self.input.LA(2)

                            if ((27 <= LA32_5 <= 28) or LA32_5 == 30 or (32 <= LA32_5 <= 34) or LA32_5 == 37 or (39 <= LA32_5 <= 40) or (42 <= LA32_5 <= 44) or (48 <= LA32_5 <= 49) or LA32_5 == 51 or (53 <= LA32_5 <= 56) or LA32_5 == 58 or LA32_5 == 60 or LA32_5 == 62 or (64 <= LA32_5 <= 68) or LA32_5 == 70) :
                                alt32 = 4
                            elif (LA32_5 == 52) :
                                alt32 = 5
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 32, 5, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 32, 0, self.input)

                            raise nvae


                        if alt32 == 1:
                            # src/ll/UL4.g:386:4: 
                            pass 

                        elif alt32 == 2:
                            # src/ll/UL4.g:388:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript1865)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1869)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:389:5: ( ',' )?
                            alt20 = 2
                            LA20_0 = self.input.LA(1)

                            if (LA20_0 == 39) :
                                alt20 = 1
                            if alt20 == 1:
                                # src/ll/UL4.g:389:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1877)





                        elif alt32 == 3:
                            # src/ll/UL4.g:392:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript1895)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1899)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remargs = rargs; 



                            # src/ll/UL4.g:393:5: ( ',' '**' rkwargs= exprarg )?
                            alt21 = 2
                            LA21_0 = self.input.LA(1)

                            if (LA21_0 == 39) :
                                LA21_1 = self.input.LA(2)

                                if (LA21_1 == 35) :
                                    alt21 = 1
                            if alt21 == 1:
                                # src/ll/UL4.g:394:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1914)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript1921)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1925)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:397:5: ( ',' )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 39) :
                                alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:397:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1940)





                        elif alt32 == 4:
                            # src/ll/UL4.g:400:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1960)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append(a1) 



                            # src/ll/UL4.g:401:5: ( ',' a2= exprarg )*
                            while True: #loop23
                                alt23 = 2
                                LA23_0 = self.input.LA(1)

                                if (LA23_0 == 39) :
                                    LA23_1 = self.input.LA(2)

                                    if (LA23_1 == NAME) :
                                        LA23_3 = self.input.LA(3)

                                        if ((27 <= LA23_3 <= 28) or LA23_3 == 30 or (32 <= LA23_3 <= 34) or LA23_3 == 37 or (39 <= LA23_3 <= 40) or (42 <= LA23_3 <= 44) or (48 <= LA23_3 <= 49) or LA23_3 == 51 or (53 <= LA23_3 <= 56) or LA23_3 == 58 or LA23_3 == 60 or LA23_3 == 62 or (64 <= LA23_3 <= 68) or LA23_3 == 70) :
                                            alt23 = 1


                                    elif ((COLOR <= LA23_1 <= DATE) or (FALSE <= LA23_1 <= FLOAT) or LA23_1 == INT or LA23_1 == NONE or (STRING <= LA23_1 <= STRING3) or LA23_1 == TRUE or LA23_1 == 32 or LA23_1 == 40 or LA23_1 == 58 or LA23_1 == 67 or LA23_1 == 69 or LA23_1 == 73) :
                                        alt23 = 1




                                if alt23 == 1:
                                    # src/ll/UL4.g:402:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1975)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1984)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append(a2) 




                                else:
                                    break #loop23


                            # src/ll/UL4.g:405:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop24
                                alt24 = 2
                                LA24_0 = self.input.LA(1)

                                if (LA24_0 == 39) :
                                    LA24_1 = self.input.LA(2)

                                    if (LA24_1 == NAME) :
                                        alt24 = 1




                                if alt24 == 1:
                                    # src/ll/UL4.g:406:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2006)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2015)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2017)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2021)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop24


                            # src/ll/UL4.g:409:5: ( ',' '*' rargs= exprarg )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 39) :
                                LA25_1 = self.input.LA(2)

                                if (LA25_1 == 34) :
                                    alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:410:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2043)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2050)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2054)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:413:5: ( ',' '**' rkwargs= exprarg )?
                            alt26 = 2
                            LA26_0 = self.input.LA(1)

                            if (LA26_0 == 39) :
                                LA26_1 = self.input.LA(2)

                                if (LA26_1 == 35) :
                                    alt26 = 1
                            if alt26 == 1:
                                # src/ll/UL4.g:414:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2076)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2083)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2087)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:417:5: ( ',' )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 39) :
                                alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:417:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2102)





                        elif alt32 == 5:
                            # src/ll/UL4.g:420:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr_subscript2122)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2124)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2128)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:421:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop28
                                alt28 = 2
                                LA28_0 = self.input.LA(1)

                                if (LA28_0 == 39) :
                                    LA28_1 = self.input.LA(2)

                                    if (LA28_1 == NAME) :
                                        alt28 = 1




                                if alt28 == 1:
                                    # src/ll/UL4.g:422:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2143)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2152)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2154)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2158)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop28


                            # src/ll/UL4.g:425:5: ( ',' '*' rargs= exprarg )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if (LA29_0 == 39) :
                                LA29_1 = self.input.LA(2)

                                if (LA29_1 == 34) :
                                    alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:426:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2180)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2187)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2191)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:429:5: ( ',' '**' rkwargs= exprarg )?
                            alt30 = 2
                            LA30_0 = self.input.LA(1)

                            if (LA30_0 == 39) :
                                LA30_1 = self.input.LA(2)

                                if (LA30_1 == 35) :
                                    alt30 = 1
                            if alt30 == 1:
                                # src/ll/UL4.g:430:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2213)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2220)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2224)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:433:5: ( ',' )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 39) :
                                alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:433:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2239)







                        close = self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2252)

                        if self._state.backtracking == 0:
                            pass
                            retval.node.end = self.end(close) 




                    elif alt33 == 3:
                        # src/ll/UL4.g:438:4: '[' e2= index close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2268)

                        self._state.following.append(self.FOLLOW_index_in_expr_subscript2275)
                        e2 = self.index()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Item(self.location, e1.start, None, retval.node, e2) 



                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2284)

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



    # $ANTLR start "expr_unary"
    # src/ll/UL4.g:445:1: expr_unary returns [node] : (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary |n= 'not' e2= expr_unary );
    def expr_unary(self, ):
        node = None


        minus = None
        bitnot = None
        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:446:2: (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary |n= 'not' e2= expr_unary )
                alt34 = 4
                LA34 = self.input.LA(1)
                if LA34 == COLOR or LA34 == DATE or LA34 == FALSE or LA34 == FLOAT or LA34 == INT or LA34 == NAME or LA34 == NONE or LA34 == STRING or LA34 == STRING3 or LA34 == TRUE or LA34 == 32 or LA34 == 58 or LA34 == 69:
                    alt34 = 1
                elif LA34 == 40:
                    alt34 = 2
                elif LA34 == 73:
                    alt34 = 3
                elif LA34 == 67:
                    alt34 = 4
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 34, 0, self.input)

                    raise nvae


                if alt34 == 1:
                    # src/ll/UL4.g:447:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_unary2312)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ((e1 is not None) and [e1.node] or [None])[0] 




                elif alt34 == 2:
                    # src/ll/UL4.g:449:3: minus= '-' e2= expr_unary
                    pass 
                    minus = self.match(self.input, 40, self.FOLLOW_40_in_expr_unary2323)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2327)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.location, self.start(minus), e2.end, e2) 




                elif alt34 == 3:
                    # src/ll/UL4.g:451:3: bitnot= '~' e2= expr_unary
                    pass 
                    bitnot = self.match(self.input, 73, self.FOLLOW_73_in_expr_unary2338)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2342)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitNot.make(self.location, self.start(bitnot), e2.end, e2) 




                elif alt34 == 4:
                    # src/ll/UL4.g:453:3: n= 'not' e2= expr_unary
                    pass 
                    n = self.match(self.input, 67, self.FOLLOW_67_in_expr_unary2353)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2357)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Not.make(self.location, self.start(n), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_unary"



    # $ANTLR start "expr_mul"
    # src/ll/UL4.g:458:1: expr_mul returns [node] : e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:459:2: (e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* )
                # src/ll/UL4.g:460:3: e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                pass 
                self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2381)
                e1 = self.expr_unary()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:461:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 28 or LA36_0 == 34 or (43 <= LA36_0 <= 44)) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:462:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
                        pass 
                        # src/ll/UL4.g:462:4: ( '*' | '/' | '//' | '%' )
                        alt35 = 4
                        LA35 = self.input.LA(1)
                        if LA35 == 34:
                            alt35 = 1
                        elif LA35 == 43:
                            alt35 = 2
                        elif LA35 == 44:
                            alt35 = 3
                        elif LA35 == 28:
                            alt35 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 35, 0, self.input)

                            raise nvae


                        if alt35 == 1:
                            # src/ll/UL4.g:463:5: '*'
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_mul2398)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:465:5: '/'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr_mul2411)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt35 == 3:
                            # src/ll/UL4.g:467:5: '//'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr_mul2424)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt35 == 4:
                            # src/ll/UL4.g:469:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_mul2437)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2451)
                        e2 = self.expr_unary()

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
    # src/ll/UL4.g:476:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:477:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:478:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2479)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:479:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 37 or LA38_0 == 40) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:480:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:480:4: ( '+' | '-' )
                        alt37 = 2
                        LA37_0 = self.input.LA(1)

                        if (LA37_0 == 37) :
                            alt37 = 1
                        elif (LA37_0 == 40) :
                            alt37 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:481:5: '+'
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_expr_add2496)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:483:5: '-'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr_add2509)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2523)
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
    # src/ll/UL4.g:490:1: expr_bitshift returns [AST node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:491:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:492:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2551)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:493:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 49 or LA40_0 == 56) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:494:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:494:4: ( '<<' | '>>' )
                        alt39 = 2
                        LA39_0 = self.input.LA(1)

                        if (LA39_0 == 49) :
                            alt39 = 1
                        elif (LA39_0 == 56) :
                            alt39 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:495:5: '<<'
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_bitshift2568)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:497:5: '>>'
                            pass 
                            self.match(self.input, 56, self.FOLLOW_56_in_expr_bitshift2581)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2595)
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



    # $ANTLR start "expr_bitand"
    # src/ll/UL4.g:504:1: expr_bitand returns [AST node] : e1= expr_bitshift ( '&' e2= expr_bitshift )* ;
    def expr_bitand(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:505:2: (e1= expr_bitshift ( '&' e2= expr_bitshift )* )
                # src/ll/UL4.g:506:3: e1= expr_bitshift ( '&' e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2623)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:507:3: ( '&' e2= expr_bitshift )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 30) :
                        alt41 = 1


                    if alt41 == 1:
                        # src/ll/UL4.g:508:4: '&' e2= expr_bitshift
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr_bitand2634)

                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2641)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitAnd.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop41





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitand"



    # $ANTLR start "expr_bitxor"
    # src/ll/UL4.g:514:1: expr_bitxor returns [AST node] : e1= expr_bitand ( '^' e2= expr_bitand )* ;
    def expr_bitxor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:515:2: (e1= expr_bitand ( '^' e2= expr_bitand )* )
                # src/ll/UL4.g:516:3: e1= expr_bitand ( '^' e2= expr_bitand )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2669)
                e1 = self.expr_bitand()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:517:3: ( '^' e2= expr_bitand )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 60) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:518:4: '^' e2= expr_bitand
                        pass 
                        self.match(self.input, 60, self.FOLLOW_60_in_expr_bitxor2680)

                        self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2687)
                        e2 = self.expr_bitand()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitXOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop42





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitxor"



    # $ANTLR start "expr_bitor"
    # src/ll/UL4.g:524:1: expr_bitor returns [AST node] : e1= expr_bitxor ( '|' e2= expr_bitxor )* ;
    def expr_bitor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:525:2: (e1= expr_bitxor ( '|' e2= expr_bitxor )* )
                # src/ll/UL4.g:526:3: e1= expr_bitxor ( '|' e2= expr_bitxor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2715)
                e1 = self.expr_bitxor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:527:3: ( '|' e2= expr_bitxor )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 70) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:528:4: '|' e2= expr_bitxor
                        pass 
                        self.match(self.input, 70, self.FOLLOW_70_in_expr_bitor2726)

                        self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2733)
                        e2 = self.expr_bitxor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitor"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:534:1: expr_cmp returns [node] : e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:535:2: (e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )* )
                # src/ll/UL4.g:536:3: e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2761)
                e1 = self.expr_bitor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:537:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 27 or LA45_0 == 48 or LA45_0 == 51 or (53 <= LA45_0 <= 55)) :
                        alt45 = 1


                    if alt45 == 1:
                        # src/ll/UL4.g:538:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor
                        pass 
                        # src/ll/UL4.g:538:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt44 = 6
                        LA44 = self.input.LA(1)
                        if LA44 == 53:
                            alt44 = 1
                        elif LA44 == 27:
                            alt44 = 2
                        elif LA44 == 48:
                            alt44 = 3
                        elif LA44 == 51:
                            alt44 = 4
                        elif LA44 == 54:
                            alt44 = 5
                        elif LA44 == 55:
                            alt44 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 44, 0, self.input)

                            raise nvae


                        if alt44 == 1:
                            # src/ll/UL4.g:539:5: '=='
                            pass 
                            self.match(self.input, 53, self.FOLLOW_53_in_expr_cmp2778)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt44 == 2:
                            # src/ll/UL4.g:541:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr_cmp2791)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt44 == 3:
                            # src/ll/UL4.g:543:5: '<'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr_cmp2804)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt44 == 4:
                            # src/ll/UL4.g:545:5: '<='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr_cmp2817)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt44 == 5:
                            # src/ll/UL4.g:547:5: '>'
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_cmp2830)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt44 == 6:
                            # src/ll/UL4.g:549:5: '>='
                            pass 
                            self.match(self.input, 55, self.FOLLOW_55_in_expr_cmp2843)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2857)
                        e2 = self.expr_bitor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop45





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_contain"
    # src/ll/UL4.g:556:1: expr_contain returns [node] : e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? ;
    def expr_contain(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:557:2: (e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? )
                # src/ll/UL4.g:558:3: e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )?
                pass 
                self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2885)
                e1 = self.expr_cmp()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = e1 



                # src/ll/UL4.g:559:3: ( ( 'not' )? 'in' e2= expr_cmp )?
                alt47 = 2
                LA47_0 = self.input.LA(1)

                if ((66 <= LA47_0 <= 67)) :
                    alt47 = 1
                if alt47 == 1:
                    # src/ll/UL4.g:560:4: ( 'not' )? 'in' e2= expr_cmp
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains 



                    # src/ll/UL4.g:561:4: ( 'not' )?
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == 67) :
                        alt46 = 1
                    if alt46 == 1:
                        # src/ll/UL4.g:562:5: 'not'
                        pass 
                        self.match(self.input, 67, self.FOLLOW_67_in_expr_contain2907)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains 






                    self.match(self.input, 66, self.FOLLOW_66_in_expr_contain2920)

                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2927)
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



    # $ANTLR start "expr_and"
    # src/ll/UL4.g:570:1: expr_and returns [node] : e1= expr_contain ( 'and' e2= expr_contain )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:571:2: (e1= expr_contain ( 'and' e2= expr_contain )* )
                # src/ll/UL4.g:572:3: e1= expr_contain ( 'and' e2= expr_contain )*
                pass 
                self._state.following.append(self.FOLLOW_expr_contain_in_expr_and2955)
                e1 = self.expr_contain()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:573:3: ( 'and' e2= expr_contain )*
                while True: #loop48
                    alt48 = 2
                    LA48_0 = self.input.LA(1)

                    if (LA48_0 == 62) :
                        alt48 = 1


                    if alt48 == 1:
                        # src/ll/UL4.g:574:4: 'and' e2= expr_contain
                        pass 
                        self.match(self.input, 62, self.FOLLOW_62_in_expr_and2966)

                        self._state.following.append(self.FOLLOW_expr_contain_in_expr_and2973)
                        e2 = self.expr_contain()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop48





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_and"



    # $ANTLR start "expr_or"
    # src/ll/UL4.g:580:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:581:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:582:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or3001)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:583:3: ( 'or' e2= expr_and )*
                while True: #loop49
                    alt49 = 2
                    LA49_0 = self.input.LA(1)

                    if (LA49_0 == 68) :
                        alt49 = 1


                    if alt49 == 1:
                        # src/ll/UL4.g:584:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 68, self.FOLLOW_68_in_expr_or3012)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or3019)
                        e2 = self.expr_and()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop49





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_or"



    # $ANTLR start "expr_if"
    # src/ll/UL4.g:590:1: expr_if returns [AST node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:591:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:592:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if3047)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:593:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt50 = 2
                LA50_0 = self.input.LA(1)

                if (LA50_0 == 65) :
                    LA50_1 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt50 = 1
                if alt50 == 1:
                    # src/ll/UL4.g:594:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_expr_if3058)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3065)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 63, self.FOLLOW_63_in_expr_if3070)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3077)
                    e3 = self.expr_or()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ul4c.If.make(self.location, e1.start, e3.end, node, e2, e3) 









                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_if"



    # $ANTLR start "exprarg"
    # src/ll/UL4.g:601:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:602:2: (ege= generatorexpression |e1= expr_if )
                alt51 = 2
                LA51 = self.input.LA(1)
                if LA51 == NONE:
                    LA51_1 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 1, self.input)

                        raise nvae


                elif LA51 == FALSE:
                    LA51_2 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 2, self.input)

                        raise nvae


                elif LA51 == TRUE:
                    LA51_3 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 3, self.input)

                        raise nvae


                elif LA51 == INT:
                    LA51_4 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 4, self.input)

                        raise nvae


                elif LA51 == FLOAT:
                    LA51_5 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 5, self.input)

                        raise nvae


                elif LA51 == STRING:
                    LA51_6 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 6, self.input)

                        raise nvae


                elif LA51 == STRING3:
                    LA51_7 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 7, self.input)

                        raise nvae


                elif LA51 == DATE:
                    LA51_8 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 8, self.input)

                        raise nvae


                elif LA51 == COLOR:
                    LA51_9 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 9, self.input)

                        raise nvae


                elif LA51 == NAME:
                    LA51_10 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 10, self.input)

                        raise nvae


                elif LA51 == 58:
                    LA51_11 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 11, self.input)

                        raise nvae


                elif LA51 == 69:
                    LA51_12 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 12, self.input)

                        raise nvae


                elif LA51 == 32:
                    LA51_13 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 13, self.input)

                        raise nvae


                elif LA51 == 40:
                    LA51_14 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 14, self.input)

                        raise nvae


                elif LA51 == 73:
                    LA51_15 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 15, self.input)

                        raise nvae


                elif LA51 == 67:
                    LA51_16 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt51 = 1
                    elif (True) :
                        alt51 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 51, 0, self.input)

                    raise nvae


                if alt51 == 1:
                    # src/ll/UL4.g:602:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg3101)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt51 == 2:
                    # src/ll/UL4.g:603:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg3110)
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
    # src/ll/UL4.g:606:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:607:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt52 = 2
                LA52 = self.input.LA(1)
                if LA52 == NONE:
                    LA52_1 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 1, self.input)

                        raise nvae


                elif LA52 == FALSE:
                    LA52_2 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 2, self.input)

                        raise nvae


                elif LA52 == TRUE:
                    LA52_3 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 3, self.input)

                        raise nvae


                elif LA52 == INT:
                    LA52_4 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 4, self.input)

                        raise nvae


                elif LA52 == FLOAT:
                    LA52_5 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 5, self.input)

                        raise nvae


                elif LA52 == STRING:
                    LA52_6 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 6, self.input)

                        raise nvae


                elif LA52 == STRING3:
                    LA52_7 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 7, self.input)

                        raise nvae


                elif LA52 == DATE:
                    LA52_8 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 8, self.input)

                        raise nvae


                elif LA52 == COLOR:
                    LA52_9 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 9, self.input)

                        raise nvae


                elif LA52 == NAME:
                    LA52_10 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 10, self.input)

                        raise nvae


                elif LA52 == 58:
                    LA52_11 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 11, self.input)

                        raise nvae


                elif LA52 == 69:
                    LA52_12 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 12, self.input)

                        raise nvae


                elif LA52 == 32:
                    LA52_13 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 13, self.input)

                        raise nvae


                elif LA52 == 40:
                    LA52_14 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 14, self.input)

                        raise nvae


                elif LA52 == 73:
                    LA52_15 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 15, self.input)

                        raise nvae


                elif LA52 == 67:
                    LA52_16 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt52 = 1
                    elif (True) :
                        alt52 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 52, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 52, 0, self.input)

                    raise nvae


                if alt52 == 1:
                    # src/ll/UL4.g:607:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3129)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3131)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt52 == 2:
                    # src/ll/UL4.g:608:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3140)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3142)

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
    # src/ll/UL4.g:614:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:615:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:616:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3167)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_for_3171)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3177)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ForBlock(self.location, self.start(n.start), e.end, ((n is not None) and [n.lvalue] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3183)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:625:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:626:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF )
                alt53 = 13
                LA53 = self.input.LA(1)
                if LA53 == NONE:
                    LA53_1 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 1, self.input)

                        raise nvae


                elif LA53 == FALSE:
                    LA53_2 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 2, self.input)

                        raise nvae


                elif LA53 == TRUE:
                    LA53_3 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 3, self.input)

                        raise nvae


                elif LA53 == INT:
                    LA53_4 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 4, self.input)

                        raise nvae


                elif LA53 == FLOAT:
                    LA53_5 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 5, self.input)

                        raise nvae


                elif LA53 == STRING:
                    LA53_6 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 6, self.input)

                        raise nvae


                elif LA53 == STRING3:
                    LA53_7 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 7, self.input)

                        raise nvae


                elif LA53 == DATE:
                    LA53_8 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 8, self.input)

                        raise nvae


                elif LA53 == COLOR:
                    LA53_9 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 9, self.input)

                        raise nvae


                elif LA53 == NAME:
                    LA53_10 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 10, self.input)

                        raise nvae


                elif LA53 == 58:
                    LA53_11 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 11, self.input)

                        raise nvae


                elif LA53 == 69:
                    LA53_12 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 12, self.input)

                        raise nvae


                elif LA53 == 32:
                    LA53_13 = self.input.LA(2)

                    if (self.synpred79_UL4()) :
                        alt53 = 1
                    elif (self.synpred80_UL4()) :
                        alt53 = 2
                    elif (self.synpred81_UL4()) :
                        alt53 = 3
                    elif (self.synpred82_UL4()) :
                        alt53 = 4
                    elif (self.synpred83_UL4()) :
                        alt53 = 5
                    elif (self.synpred84_UL4()) :
                        alt53 = 6
                    elif (self.synpred85_UL4()) :
                        alt53 = 7
                    elif (self.synpred86_UL4()) :
                        alt53 = 8
                    elif (self.synpred87_UL4()) :
                        alt53 = 9
                    elif (self.synpred88_UL4()) :
                        alt53 = 10
                    elif (self.synpred89_UL4()) :
                        alt53 = 11
                    elif (self.synpred90_UL4()) :
                        alt53 = 12
                    elif (True) :
                        alt53 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 13, self.input)

                        raise nvae


                elif LA53 == 40 or LA53 == 67 or LA53 == 73:
                    alt53 = 13
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 53, 0, self.input)

                    raise nvae


                if alt53 == 1:
                    # src/ll/UL4.g:626:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3204)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_statement3206)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3210)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3212)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.lvalue] or [None])[0], e) 




                elif alt53 == 2:
                    # src/ll/UL4.g:627:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3221)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 38, self.FOLLOW_38_in_statement3223)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3227)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3229)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 3:
                    # src/ll/UL4.g:628:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3238)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement3240)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3244)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3246)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 4:
                    # src/ll/UL4.g:629:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3255)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement3257)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3261)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3263)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 5:
                    # src/ll/UL4.g:630:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3272)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement3274)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3278)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3280)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 6:
                    # src/ll/UL4.g:631:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3289)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement3291)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3295)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3297)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 7:
                    # src/ll/UL4.g:632:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3306)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3308)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3312)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3314)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 8:
                    # src/ll/UL4.g:633:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3323)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 50, self.FOLLOW_50_in_statement3325)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3329)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3331)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 9:
                    # src/ll/UL4.g:634:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3340)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 57, self.FOLLOW_57_in_statement3342)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3346)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3348)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 10:
                    # src/ll/UL4.g:635:4: n= expr_subscript '&=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3357)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement3359)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3363)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3365)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitAndVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 11:
                    # src/ll/UL4.g:636:4: n= expr_subscript '^=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3374)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 61, self.FOLLOW_61_in_statement3376)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3380)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3382)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitXOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 12:
                    # src/ll/UL4.g:637:4: n= expr_subscript '|=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3391)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 71, self.FOLLOW_71_in_statement3393)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3397)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3399)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt53 == 13:
                    # src/ll/UL4.g:638:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3408)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3410)

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
        open = self.match(self.input, 32, self.FOLLOW_32_in_synpred24_UL41549)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred24_UL41553)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 33, self.FOLLOW_33_in_synpred24_UL41557)



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
        self.match(self.input, 32, self.FOLLOW_32_in_synpred26_UL41606)

        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred26_UL41610)
        n0 = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred26_UL41612)

        self.match(self.input, 33, self.FOLLOW_33_in_synpred26_UL41614)



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:594:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:594:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 65, self.FOLLOW_65_in_synpred76_UL43058)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred76_UL43065)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 63, self.FOLLOW_63_in_synpred76_UL43070)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred76_UL43077)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:602:4: (ege= generatorexpression )
        # src/ll/UL4.g:602:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred77_UL43101)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:607:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:607:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred78_UL43129)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43131)



    # $ANTLR end "synpred78_UL4"



    # $ANTLR start "synpred79_UL4"
    def synpred79_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:626:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:626:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred79_UL43204)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 52, self.FOLLOW_52_in_synpred79_UL43206)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred79_UL43210)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred79_UL43212)



    # $ANTLR end "synpred79_UL4"



    # $ANTLR start "synpred80_UL4"
    def synpred80_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:627:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:627:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred80_UL43221)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 38, self.FOLLOW_38_in_synpred80_UL43223)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred80_UL43227)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred80_UL43229)



    # $ANTLR end "synpred80_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:628:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:628:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred81_UL43238)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred81_UL43240)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred81_UL43244)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred81_UL43246)



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:629:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:629:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred82_UL43255)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred82_UL43257)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred82_UL43261)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred82_UL43263)



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:630:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:630:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred83_UL43272)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred83_UL43274)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred83_UL43278)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43280)



    # $ANTLR end "synpred83_UL4"



    # $ANTLR start "synpred84_UL4"
    def synpred84_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:631:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:631:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred84_UL43289)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 45, self.FOLLOW_45_in_synpred84_UL43291)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred84_UL43295)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred84_UL43297)



    # $ANTLR end "synpred84_UL4"



    # $ANTLR start "synpred85_UL4"
    def synpred85_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:632:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:632:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred85_UL43306)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred85_UL43308)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred85_UL43312)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred85_UL43314)



    # $ANTLR end "synpred85_UL4"



    # $ANTLR start "synpred86_UL4"
    def synpred86_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:633:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:633:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred86_UL43323)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 50, self.FOLLOW_50_in_synpred86_UL43325)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred86_UL43329)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred86_UL43331)



    # $ANTLR end "synpred86_UL4"



    # $ANTLR start "synpred87_UL4"
    def synpred87_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:634:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:634:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred87_UL43340)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 57, self.FOLLOW_57_in_synpred87_UL43342)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred87_UL43346)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred87_UL43348)



    # $ANTLR end "synpred87_UL4"



    # $ANTLR start "synpred88_UL4"
    def synpred88_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:635:4: (n= expr_subscript '&=' e= expr_if EOF )
        # src/ll/UL4.g:635:4: n= expr_subscript '&=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred88_UL43357)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 31, self.FOLLOW_31_in_synpred88_UL43359)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred88_UL43363)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred88_UL43365)



    # $ANTLR end "synpred88_UL4"



    # $ANTLR start "synpred89_UL4"
    def synpred89_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:636:4: (n= expr_subscript '^=' e= expr_if EOF )
        # src/ll/UL4.g:636:4: n= expr_subscript '^=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred89_UL43374)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 61, self.FOLLOW_61_in_synpred89_UL43376)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred89_UL43380)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred89_UL43382)



    # $ANTLR end "synpred89_UL4"



    # $ANTLR start "synpred90_UL4"
    def synpred90_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:637:4: (n= expr_subscript '|=' e= expr_if EOF )
        # src/ll/UL4.g:637:4: n= expr_subscript '|=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred90_UL43391)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 71, self.FOLLOW_71_in_synpred90_UL43393)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred90_UL43397)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred90_UL43399)



    # $ANTLR end "synpred90_UL4"




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
    FOLLOW_58_in_list1056 = frozenset([59])
    FOLLOW_59_in_list1062 = frozenset([1])
    FOLLOW_58_in_list1073 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_list1081 = frozenset([39, 59])
    FOLLOW_39_in_list1092 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_list1099 = frozenset([39, 59])
    FOLLOW_39_in_list1110 = frozenset([59])
    FOLLOW_59_in_list1117 = frozenset([1])
    FOLLOW_58_in_listcomprehension1145 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_listcomprehension1151 = frozenset([64])
    FOLLOW_64_in_listcomprehension1155 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_listcomprehension1161 = frozenset([66])
    FOLLOW_66_in_listcomprehension1165 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_listcomprehension1171 = frozenset([59, 65])
    FOLLOW_65_in_listcomprehension1180 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_listcomprehension1187 = frozenset([59])
    FOLLOW_59_in_listcomprehension1200 = frozenset([1])
    FOLLOW_expr_if_in_dictitem1225 = frozenset([47])
    FOLLOW_47_in_dictitem1229 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictitem1235 = frozenset([1])
    FOLLOW_69_in_dict1256 = frozenset([72])
    FOLLOW_72_in_dict1262 = frozenset([1])
    FOLLOW_69_in_dict1273 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_dictitem_in_dict1281 = frozenset([39, 72])
    FOLLOW_39_in_dict1292 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_dictitem_in_dict1299 = frozenset([39, 72])
    FOLLOW_39_in_dict1310 = frozenset([72])
    FOLLOW_72_in_dict1317 = frozenset([1])
    FOLLOW_69_in_dictcomprehension1345 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1351 = frozenset([47])
    FOLLOW_47_in_dictcomprehension1355 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1361 = frozenset([64])
    FOLLOW_64_in_dictcomprehension1365 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_dictcomprehension1371 = frozenset([66])
    FOLLOW_66_in_dictcomprehension1375 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1381 = frozenset([65, 72])
    FOLLOW_65_in_dictcomprehension1390 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1397 = frozenset([72])
    FOLLOW_72_in_dictcomprehension1410 = frozenset([1])
    FOLLOW_expr_if_in_generatorexpression1438 = frozenset([64])
    FOLLOW_64_in_generatorexpression1444 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_generatorexpression1450 = frozenset([66])
    FOLLOW_66_in_generatorexpression1454 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_generatorexpression1460 = frozenset([1, 65])
    FOLLOW_65_in_generatorexpression1471 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_generatorexpression1478 = frozenset([1])
    FOLLOW_literal_in_atom1504 = frozenset([1])
    FOLLOW_list_in_atom1513 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1522 = frozenset([1])
    FOLLOW_dict_in_atom1531 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1540 = frozenset([1])
    FOLLOW_32_in_atom1549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_generatorexpression_in_atom1553 = frozenset([33])
    FOLLOW_33_in_atom1557 = frozenset([1])
    FOLLOW_32_in_atom1566 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_atom1570 = frozenset([33])
    FOLLOW_33_in_atom1574 = frozenset([1])
    FOLLOW_expr_subscript_in_nestedlvalue1597 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1606 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1610 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1612 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1614 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1623 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1629 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1633 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1639 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1650 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1657 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1668 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1673 = frozenset([1])
    FOLLOW_47_in_index1701 = frozenset([1, 5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_index1714 = frozenset([1])
    FOLLOW_expr_if_in_index1732 = frozenset([1, 47])
    FOLLOW_47_in_index1745 = frozenset([1, 5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_index1760 = frozenset([1])
    FOLLOW_atom_in_expr_subscript1796 = frozenset([1, 32, 42, 58])
    FOLLOW_42_in_expr_subscript1812 = frozenset([14])
    FOLLOW_name_in_expr_subscript1819 = frozenset([1, 32, 42, 58])
    FOLLOW_32_in_expr_subscript1835 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 67, 69, 73])
    FOLLOW_35_in_expr_subscript1865 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1869 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1877 = frozenset([33])
    FOLLOW_34_in_expr_subscript1895 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1899 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1914 = frozenset([35])
    FOLLOW_35_in_expr_subscript1921 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1925 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1940 = frozenset([33])
    FOLLOW_exprarg_in_expr_subscript1960 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1975 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1984 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2006 = frozenset([14])
    FOLLOW_name_in_expr_subscript2015 = frozenset([52])
    FOLLOW_52_in_expr_subscript2017 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2021 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2043 = frozenset([34])
    FOLLOW_34_in_expr_subscript2050 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2054 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2076 = frozenset([35])
    FOLLOW_35_in_expr_subscript2083 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2087 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2102 = frozenset([33])
    FOLLOW_name_in_expr_subscript2122 = frozenset([52])
    FOLLOW_52_in_expr_subscript2124 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2128 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2143 = frozenset([14])
    FOLLOW_name_in_expr_subscript2152 = frozenset([52])
    FOLLOW_52_in_expr_subscript2154 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2158 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2180 = frozenset([34])
    FOLLOW_34_in_expr_subscript2187 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2191 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2213 = frozenset([35])
    FOLLOW_35_in_expr_subscript2220 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2224 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2239 = frozenset([33])
    FOLLOW_33_in_expr_subscript2252 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2268 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 67, 69, 73])
    FOLLOW_index_in_expr_subscript2275 = frozenset([59])
    FOLLOW_59_in_expr_subscript2284 = frozenset([1, 32, 42, 58])
    FOLLOW_expr_subscript_in_expr_unary2312 = frozenset([1])
    FOLLOW_40_in_expr_unary2323 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2327 = frozenset([1])
    FOLLOW_73_in_expr_unary2338 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2342 = frozenset([1])
    FOLLOW_67_in_expr_unary2353 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2357 = frozenset([1])
    FOLLOW_expr_unary_in_expr_mul2381 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_34_in_expr_mul2398 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_43_in_expr_mul2411 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_44_in_expr_mul2424 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_28_in_expr_mul2437 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_mul2451 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_expr_mul_in_expr_add2479 = frozenset([1, 37, 40])
    FOLLOW_37_in_expr_add2496 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_40_in_expr_add2509 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_mul_in_expr_add2523 = frozenset([1, 37, 40])
    FOLLOW_expr_add_in_expr_bitshift2551 = frozenset([1, 49, 56])
    FOLLOW_49_in_expr_bitshift2568 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_56_in_expr_bitshift2581 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_add_in_expr_bitshift2595 = frozenset([1, 49, 56])
    FOLLOW_expr_bitshift_in_expr_bitand2623 = frozenset([1, 30])
    FOLLOW_30_in_expr_bitand2634 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitshift_in_expr_bitand2641 = frozenset([1, 30])
    FOLLOW_expr_bitand_in_expr_bitxor2669 = frozenset([1, 60])
    FOLLOW_60_in_expr_bitxor2680 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitand_in_expr_bitxor2687 = frozenset([1, 60])
    FOLLOW_expr_bitxor_in_expr_bitor2715 = frozenset([1, 70])
    FOLLOW_70_in_expr_bitor2726 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitxor_in_expr_bitor2733 = frozenset([1, 70])
    FOLLOW_expr_bitor_in_expr_cmp2761 = frozenset([1, 27, 48, 51, 53, 54, 55])
    FOLLOW_53_in_expr_cmp2778 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_27_in_expr_cmp2791 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_48_in_expr_cmp2804 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_51_in_expr_cmp2817 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_54_in_expr_cmp2830 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_55_in_expr_cmp2843 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitor_in_expr_cmp2857 = frozenset([1, 27, 48, 51, 53, 54, 55])
    FOLLOW_expr_cmp_in_expr_contain2885 = frozenset([1, 66, 67])
    FOLLOW_67_in_expr_contain2907 = frozenset([66])
    FOLLOW_66_in_expr_contain2920 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_cmp_in_expr_contain2927 = frozenset([1])
    FOLLOW_expr_contain_in_expr_and2955 = frozenset([1, 62])
    FOLLOW_62_in_expr_and2966 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_contain_in_expr_and2973 = frozenset([1, 62])
    FOLLOW_expr_and_in_expr_or3001 = frozenset([1, 68])
    FOLLOW_68_in_expr_or3012 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_and_in_expr_or3019 = frozenset([1, 68])
    FOLLOW_expr_or_in_expr_if3047 = frozenset([1, 65])
    FOLLOW_65_in_expr_if3058 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3065 = frozenset([63])
    FOLLOW_63_in_expr_if3070 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3077 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg3101 = frozenset([1])
    FOLLOW_expr_if_in_exprarg3110 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3129 = frozenset([])
    FOLLOW_EOF_in_expression3131 = frozenset([1])
    FOLLOW_expr_if_in_expression3140 = frozenset([])
    FOLLOW_EOF_in_expression3142 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3167 = frozenset([66])
    FOLLOW_66_in_for_3171 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_for_3177 = frozenset([])
    FOLLOW_EOF_in_for_3183 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3204 = frozenset([52])
    FOLLOW_52_in_statement3206 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3210 = frozenset([])
    FOLLOW_EOF_in_statement3212 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3221 = frozenset([38])
    FOLLOW_38_in_statement3223 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3227 = frozenset([])
    FOLLOW_EOF_in_statement3229 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3238 = frozenset([41])
    FOLLOW_41_in_statement3240 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3244 = frozenset([])
    FOLLOW_EOF_in_statement3246 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3255 = frozenset([36])
    FOLLOW_36_in_statement3257 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3261 = frozenset([])
    FOLLOW_EOF_in_statement3263 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3272 = frozenset([46])
    FOLLOW_46_in_statement3274 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3278 = frozenset([])
    FOLLOW_EOF_in_statement3280 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3289 = frozenset([45])
    FOLLOW_45_in_statement3291 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3295 = frozenset([])
    FOLLOW_EOF_in_statement3297 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3306 = frozenset([29])
    FOLLOW_29_in_statement3308 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3312 = frozenset([])
    FOLLOW_EOF_in_statement3314 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3323 = frozenset([50])
    FOLLOW_50_in_statement3325 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3329 = frozenset([])
    FOLLOW_EOF_in_statement3331 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3340 = frozenset([57])
    FOLLOW_57_in_statement3342 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3346 = frozenset([])
    FOLLOW_EOF_in_statement3348 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3357 = frozenset([31])
    FOLLOW_31_in_statement3359 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3363 = frozenset([])
    FOLLOW_EOF_in_statement3365 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3374 = frozenset([61])
    FOLLOW_61_in_statement3376 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3380 = frozenset([])
    FOLLOW_EOF_in_statement3382 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3391 = frozenset([71])
    FOLLOW_71_in_statement3393 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3397 = frozenset([])
    FOLLOW_EOF_in_statement3399 = frozenset([1])
    FOLLOW_expression_in_statement3408 = frozenset([])
    FOLLOW_EOF_in_statement3410 = frozenset([1])
    FOLLOW_list_in_synpred20_UL41513 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred21_UL41522 = frozenset([1])
    FOLLOW_dict_in_synpred22_UL41531 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred23_UL41540 = frozenset([1])
    FOLLOW_32_in_synpred24_UL41549 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_generatorexpression_in_synpred24_UL41553 = frozenset([33])
    FOLLOW_33_in_synpred24_UL41557 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred25_UL41597 = frozenset([1])
    FOLLOW_32_in_synpred26_UL41606 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_synpred26_UL41610 = frozenset([39])
    FOLLOW_39_in_synpred26_UL41612 = frozenset([33])
    FOLLOW_33_in_synpred26_UL41614 = frozenset([1])
    FOLLOW_65_in_synpred76_UL43058 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred76_UL43065 = frozenset([63])
    FOLLOW_63_in_synpred76_UL43070 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred76_UL43077 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred77_UL43101 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred78_UL43129 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43131 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred79_UL43204 = frozenset([52])
    FOLLOW_52_in_synpred79_UL43206 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred79_UL43210 = frozenset([])
    FOLLOW_EOF_in_synpred79_UL43212 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred80_UL43221 = frozenset([38])
    FOLLOW_38_in_synpred80_UL43223 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred80_UL43227 = frozenset([])
    FOLLOW_EOF_in_synpred80_UL43229 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred81_UL43238 = frozenset([41])
    FOLLOW_41_in_synpred81_UL43240 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred81_UL43244 = frozenset([])
    FOLLOW_EOF_in_synpred81_UL43246 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred82_UL43255 = frozenset([36])
    FOLLOW_36_in_synpred82_UL43257 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred82_UL43261 = frozenset([])
    FOLLOW_EOF_in_synpred82_UL43263 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred83_UL43272 = frozenset([46])
    FOLLOW_46_in_synpred83_UL43274 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred83_UL43278 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43280 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred84_UL43289 = frozenset([45])
    FOLLOW_45_in_synpred84_UL43291 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred84_UL43295 = frozenset([])
    FOLLOW_EOF_in_synpred84_UL43297 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred85_UL43306 = frozenset([29])
    FOLLOW_29_in_synpred85_UL43308 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred85_UL43312 = frozenset([])
    FOLLOW_EOF_in_synpred85_UL43314 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred86_UL43323 = frozenset([50])
    FOLLOW_50_in_synpred86_UL43325 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred86_UL43329 = frozenset([])
    FOLLOW_EOF_in_synpred86_UL43331 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred87_UL43340 = frozenset([57])
    FOLLOW_57_in_synpred87_UL43342 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred87_UL43346 = frozenset([])
    FOLLOW_EOF_in_synpred87_UL43348 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred88_UL43357 = frozenset([31])
    FOLLOW_31_in_synpred88_UL43359 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred88_UL43363 = frozenset([])
    FOLLOW_EOF_in_synpred88_UL43365 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred89_UL43374 = frozenset([61])
    FOLLOW_61_in_synpred89_UL43376 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred89_UL43380 = frozenset([])
    FOLLOW_EOF_in_synpred89_UL43382 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred90_UL43391 = frozenset([71])
    FOLLOW_71_in_synpred90_UL43393 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred90_UL43397 = frozenset([])
    FOLLOW_EOF_in_synpred90_UL43399 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
