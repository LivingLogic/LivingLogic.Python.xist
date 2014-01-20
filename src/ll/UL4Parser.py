# $ANTLR 3.5 src/ll/UL4.g 2014-01-20 17:35:47

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



    # $ANTLR start "slice"
    # src/ll/UL4.g:350:1: slice returns [node] : (e1= expr_if )? colon= ':' (e2= expr_if )? ;
    def slice(self, ):
        node = None


        colon = None
        e1 = None
        e2 = None

         
        index1 = None
        index2 = None
        startpos = None
        endpos = None
        	
        try:
            try:
                # src/ll/UL4.g:358:2: ( (e1= expr_if )? colon= ':' (e2= expr_if )? )
                # src/ll/UL4.g:359:3: (e1= expr_if )? colon= ':' (e2= expr_if )?
                pass 
                # src/ll/UL4.g:359:3: (e1= expr_if )?
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if ((COLOR <= LA16_0 <= DATE) or (FALSE <= LA16_0 <= FLOAT) or (INT <= LA16_0 <= NONE) or (STRING <= LA16_0 <= STRING3) or LA16_0 == TRUE or LA16_0 == 32 or LA16_0 == 40 or LA16_0 == 58 or LA16_0 == 67 or LA16_0 == 69 or LA16_0 == 73) :
                    alt16 = 1
                if alt16 == 1:
                    # src/ll/UL4.g:360:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1706)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index1 = e1; startpos = e1.start; 






                colon = self.match(self.input, 47, self.FOLLOW_47_in_slice1719)

                if self._state.backtracking == 0:
                    pass
                                
                    if startpos is None:
                    	startpos = self.start(colon)
                    endpos = self.end(colon)
                    		



                # src/ll/UL4.g:367:3: (e2= expr_if )?
                alt17 = 2
                LA17_0 = self.input.LA(1)

                if ((COLOR <= LA17_0 <= DATE) or (FALSE <= LA17_0 <= FLOAT) or (INT <= LA17_0 <= NONE) or (STRING <= LA17_0 <= STRING3) or LA17_0 == TRUE or LA17_0 == 32 or LA17_0 == 40 or LA17_0 == 58 or LA17_0 == 67 or LA17_0 == 69 or LA17_0 == 73) :
                    alt17 = 1
                if alt17 == 1:
                    # src/ll/UL4.g:368:4: e2= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1732)
                    e2 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index2 = e2; endpos = e2.end; 






                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Slice(self.location, startpos, endpos, index1, index2) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "slice"


    class expr_subscript_return(ParserRuleReturnScope):
        def __init__(self):
            super(UL4Parser.expr_subscript_return, self).__init__()

            self.node = None





    # $ANTLR start "expr_subscript"
    # src/ll/UL4.g:373:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* ;
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
                # src/ll/UL4.g:374:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* )
                # src/ll/UL4.g:375:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript1762)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    retval.node =  e1 



                # src/ll/UL4.g:376:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                while True: #loop31
                    alt31 = 5
                    LA31 = self.input.LA(1)
                    if LA31 == 42:
                        alt31 = 1
                    elif LA31 == 32:
                        alt31 = 2
                    elif LA31 == 58:
                        LA31_45 = self.input.LA(2)

                        if (self.synpred49_UL4()) :
                            alt31 = 3
                        elif (self.synpred50_UL4()) :
                            alt31 = 4



                    if alt31 == 1:
                        # src/ll/UL4.g:378:4: '.' n= name
                        pass 
                        self.match(self.input, 42, self.FOLLOW_42_in_expr_subscript1778)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript1785)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Attr(self.location, retval.node.start, self.end(n.stop), retval.node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt31 == 2:
                        # src/ll/UL4.g:382:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript1801)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Call(self.location, retval.node.start, None, retval.node) 



                        # src/ll/UL4.g:383:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt30 = 5
                        LA30 = self.input.LA(1)
                        if LA30 == 33:
                            alt30 = 1
                        elif LA30 == 35:
                            alt30 = 2
                        elif LA30 == 34:
                            alt30 = 3
                        elif LA30 == COLOR or LA30 == DATE or LA30 == FALSE or LA30 == FLOAT or LA30 == INT or LA30 == NONE or LA30 == STRING or LA30 == STRING3 or LA30 == TRUE or LA30 == 32 or LA30 == 40 or LA30 == 58 or LA30 == 67 or LA30 == 69 or LA30 == 73:
                            alt30 = 4
                        elif LA30 == NAME:
                            LA30_5 = self.input.LA(2)

                            if ((27 <= LA30_5 <= 28) or LA30_5 == 30 or (32 <= LA30_5 <= 34) or LA30_5 == 37 or (39 <= LA30_5 <= 40) or (42 <= LA30_5 <= 44) or (48 <= LA30_5 <= 49) or LA30_5 == 51 or (53 <= LA30_5 <= 56) or LA30_5 == 58 or LA30_5 == 60 or LA30_5 == 62 or (64 <= LA30_5 <= 68) or LA30_5 == 70) :
                                alt30 = 4
                            elif (LA30_5 == 52) :
                                alt30 = 5
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 30, 5, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 30, 0, self.input)

                            raise nvae


                        if alt30 == 1:
                            # src/ll/UL4.g:385:4: 
                            pass 

                        elif alt30 == 2:
                            # src/ll/UL4.g:387:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript1831)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1835)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remkwargs = rkwargs; 



                            # src/ll/UL4.g:388:5: ( ',' )?
                            alt18 = 2
                            LA18_0 = self.input.LA(1)

                            if (LA18_0 == 39) :
                                alt18 = 1
                            if alt18 == 1:
                                # src/ll/UL4.g:388:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1843)





                        elif alt30 == 3:
                            # src/ll/UL4.g:391:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript1861)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1865)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.remargs = rargs; 



                            # src/ll/UL4.g:392:5: ( ',' '**' rkwargs= exprarg )?
                            alt19 = 2
                            LA19_0 = self.input.LA(1)

                            if (LA19_0 == 39) :
                                LA19_1 = self.input.LA(2)

                                if (LA19_1 == 35) :
                                    alt19 = 1
                            if alt19 == 1:
                                # src/ll/UL4.g:393:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1880)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript1887)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1891)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:396:5: ( ',' )?
                            alt20 = 2
                            LA20_0 = self.input.LA(1)

                            if (LA20_0 == 39) :
                                alt20 = 1
                            if alt20 == 1:
                                # src/ll/UL4.g:396:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1906)





                        elif alt30 == 4:
                            # src/ll/UL4.g:399:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1926)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append(a1) 



                            # src/ll/UL4.g:400:5: ( ',' a2= exprarg )*
                            while True: #loop21
                                alt21 = 2
                                LA21_0 = self.input.LA(1)

                                if (LA21_0 == 39) :
                                    LA21_1 = self.input.LA(2)

                                    if (LA21_1 == NAME) :
                                        LA21_3 = self.input.LA(3)

                                        if ((27 <= LA21_3 <= 28) or LA21_3 == 30 or (32 <= LA21_3 <= 34) or LA21_3 == 37 or (39 <= LA21_3 <= 40) or (42 <= LA21_3 <= 44) or (48 <= LA21_3 <= 49) or LA21_3 == 51 or (53 <= LA21_3 <= 56) or LA21_3 == 58 or LA21_3 == 60 or LA21_3 == 62 or (64 <= LA21_3 <= 68) or LA21_3 == 70) :
                                            alt21 = 1


                                    elif ((COLOR <= LA21_1 <= DATE) or (FALSE <= LA21_1 <= FLOAT) or LA21_1 == INT or LA21_1 == NONE or (STRING <= LA21_1 <= STRING3) or LA21_1 == TRUE or LA21_1 == 32 or LA21_1 == 40 or LA21_1 == 58 or LA21_1 == 67 or LA21_1 == 69 or LA21_1 == 73) :
                                        alt21 = 1




                                if alt21 == 1:
                                    # src/ll/UL4.g:401:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1941)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1950)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append(a2) 




                                else:
                                    break #loop21


                            # src/ll/UL4.g:404:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop22
                                alt22 = 2
                                LA22_0 = self.input.LA(1)

                                if (LA22_0 == 39) :
                                    LA22_1 = self.input.LA(2)

                                    if (LA22_1 == NAME) :
                                        alt22 = 1




                                if alt22 == 1:
                                    # src/ll/UL4.g:405:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript1972)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript1981)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript1983)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript1987)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)) 




                                else:
                                    break #loop22


                            # src/ll/UL4.g:408:5: ( ',' '*' rargs= exprarg )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 39) :
                                LA23_1 = self.input.LA(2)

                                if (LA23_1 == 34) :
                                    alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:409:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2009)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2016)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2020)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:412:5: ( ',' '**' rkwargs= exprarg )?
                            alt24 = 2
                            LA24_0 = self.input.LA(1)

                            if (LA24_0 == 39) :
                                LA24_1 = self.input.LA(2)

                                if (LA24_1 == 35) :
                                    alt24 = 1
                            if alt24 == 1:
                                # src/ll/UL4.g:413:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2042)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2049)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2053)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:416:5: ( ',' )?
                            alt25 = 2
                            LA25_0 = self.input.LA(1)

                            if (LA25_0 == 39) :
                                alt25 = 1
                            if alt25 == 1:
                                # src/ll/UL4.g:416:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2068)





                        elif alt30 == 5:
                            # src/ll/UL4.g:419:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr_subscript2088)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2090)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2094)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.kwargs.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)) 



                            # src/ll/UL4.g:420:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop26
                                alt26 = 2
                                LA26_0 = self.input.LA(1)

                                if (LA26_0 == 39) :
                                    LA26_1 = self.input.LA(2)

                                    if (LA26_1 == NAME) :
                                        alt26 = 1




                                if alt26 == 1:
                                    # src/ll/UL4.g:421:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2109)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2118)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2120)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2124)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.kwargs.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)) 




                                else:
                                    break #loop26


                            # src/ll/UL4.g:424:5: ( ',' '*' rargs= exprarg )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 39) :
                                LA27_1 = self.input.LA(2)

                                if (LA27_1 == 34) :
                                    alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:425:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2146)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2153)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2157)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remargs = rargs; 






                            # src/ll/UL4.g:428:5: ( ',' '**' rkwargs= exprarg )?
                            alt28 = 2
                            LA28_0 = self.input.LA(1)

                            if (LA28_0 == 39) :
                                LA28_1 = self.input.LA(2)

                                if (LA28_1 == 35) :
                                    alt28 = 1
                            if alt28 == 1:
                                # src/ll/UL4.g:429:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2179)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2186)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2190)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.remkwargs = rkwargs; 






                            # src/ll/UL4.g:432:5: ( ',' )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if (LA29_0 == 39) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:432:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2205)







                        close = self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2218)

                        if self._state.backtracking == 0:
                            pass
                            retval.node.end = self.end(close) 




                    elif alt31 == 3:
                        # src/ll/UL4.g:437:4: '[' e2= expr_if close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2234)

                        self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2242)
                        e2 = self.expr_if()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2249)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Item(self.location, e1.start, self.end(close), retval.node, e2) 




                    elif alt31 == 4:
                        # src/ll/UL4.g:442:4: '[' e2= slice close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2265)

                        self._state.following.append(self.FOLLOW_slice_in_expr_subscript2273)
                        e2 = self.slice()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2280)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Item(self.location, e1.start, self.end(close), retval.node, e2) 




                    else:
                        break #loop31




                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "expr_subscript"



    # $ANTLR start "expr_unary"
    # src/ll/UL4.g:449:1: expr_unary returns [node] : (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary |n= 'not' e2= expr_unary );
    def expr_unary(self, ):
        node = None


        minus = None
        bitnot = None
        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:450:2: (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary |n= 'not' e2= expr_unary )
                alt32 = 4
                LA32 = self.input.LA(1)
                if LA32 == COLOR or LA32 == DATE or LA32 == FALSE or LA32 == FLOAT or LA32 == INT or LA32 == NAME or LA32 == NONE or LA32 == STRING or LA32 == STRING3 or LA32 == TRUE or LA32 == 32 or LA32 == 58 or LA32 == 69:
                    alt32 = 1
                elif LA32 == 40:
                    alt32 = 2
                elif LA32 == 73:
                    alt32 = 3
                elif LA32 == 67:
                    alt32 = 4
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 32, 0, self.input)

                    raise nvae


                if alt32 == 1:
                    # src/ll/UL4.g:451:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_unary2308)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ((e1 is not None) and [e1.node] or [None])[0] 




                elif alt32 == 2:
                    # src/ll/UL4.g:453:3: minus= '-' e2= expr_unary
                    pass 
                    minus = self.match(self.input, 40, self.FOLLOW_40_in_expr_unary2319)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2323)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.location, self.start(minus), e2.end, e2) 




                elif alt32 == 3:
                    # src/ll/UL4.g:455:3: bitnot= '~' e2= expr_unary
                    pass 
                    bitnot = self.match(self.input, 73, self.FOLLOW_73_in_expr_unary2334)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2338)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitNot.make(self.location, self.start(bitnot), e2.end, e2) 




                elif alt32 == 4:
                    # src/ll/UL4.g:457:3: n= 'not' e2= expr_unary
                    pass 
                    n = self.match(self.input, 67, self.FOLLOW_67_in_expr_unary2349)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2353)
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
    # src/ll/UL4.g:462:1: expr_mul returns [node] : e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:463:2: (e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* )
                # src/ll/UL4.g:464:3: e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                pass 
                self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2377)
                e1 = self.expr_unary()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:465:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                while True: #loop34
                    alt34 = 2
                    LA34_0 = self.input.LA(1)

                    if (LA34_0 == 28 or LA34_0 == 34 or (43 <= LA34_0 <= 44)) :
                        alt34 = 1


                    if alt34 == 1:
                        # src/ll/UL4.g:466:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
                        pass 
                        # src/ll/UL4.g:466:4: ( '*' | '/' | '//' | '%' )
                        alt33 = 4
                        LA33 = self.input.LA(1)
                        if LA33 == 34:
                            alt33 = 1
                        elif LA33 == 43:
                            alt33 = 2
                        elif LA33 == 44:
                            alt33 = 3
                        elif LA33 == 28:
                            alt33 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 33, 0, self.input)

                            raise nvae


                        if alt33 == 1:
                            # src/ll/UL4.g:467:5: '*'
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_mul2394)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt33 == 2:
                            # src/ll/UL4.g:469:5: '/'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr_mul2407)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt33 == 3:
                            # src/ll/UL4.g:471:5: '//'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr_mul2420)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt33 == 4:
                            # src/ll/UL4.g:473:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_mul2433)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2447)
                        e2 = self.expr_unary()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop34





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_mul"



    # $ANTLR start "expr_add"
    # src/ll/UL4.g:480:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:481:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:482:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2475)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:483:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop36
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 37 or LA36_0 == 40) :
                        alt36 = 1


                    if alt36 == 1:
                        # src/ll/UL4.g:484:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:484:4: ( '+' | '-' )
                        alt35 = 2
                        LA35_0 = self.input.LA(1)

                        if (LA35_0 == 37) :
                            alt35 = 1
                        elif (LA35_0 == 40) :
                            alt35 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 35, 0, self.input)

                            raise nvae


                        if alt35 == 1:
                            # src/ll/UL4.g:485:5: '+'
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_expr_add2492)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt35 == 2:
                            # src/ll/UL4.g:487:5: '-'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr_add2505)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2519)
                        e2 = self.expr_mul()

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

    # $ANTLR end "expr_add"



    # $ANTLR start "expr_bitshift"
    # src/ll/UL4.g:494:1: expr_bitshift returns [AST node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:495:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:496:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2547)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:497:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 49 or LA38_0 == 56) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:498:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:498:4: ( '<<' | '>>' )
                        alt37 = 2
                        LA37_0 = self.input.LA(1)

                        if (LA37_0 == 49) :
                            alt37 = 1
                        elif (LA37_0 == 56) :
                            alt37 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:499:5: '<<'
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_bitshift2564)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:501:5: '>>'
                            pass 
                            self.match(self.input, 56, self.FOLLOW_56_in_expr_bitshift2577)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2591)
                        e2 = self.expr_add()

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

    # $ANTLR end "expr_bitshift"



    # $ANTLR start "expr_bitand"
    # src/ll/UL4.g:508:1: expr_bitand returns [AST node] : e1= expr_bitshift ( '&' e2= expr_bitshift )* ;
    def expr_bitand(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:509:2: (e1= expr_bitshift ( '&' e2= expr_bitshift )* )
                # src/ll/UL4.g:510:3: e1= expr_bitshift ( '&' e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2619)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:511:3: ( '&' e2= expr_bitshift )*
                while True: #loop39
                    alt39 = 2
                    LA39_0 = self.input.LA(1)

                    if (LA39_0 == 30) :
                        alt39 = 1


                    if alt39 == 1:
                        # src/ll/UL4.g:512:4: '&' e2= expr_bitshift
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr_bitand2630)

                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2637)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitAnd.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop39





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitand"



    # $ANTLR start "expr_bitxor"
    # src/ll/UL4.g:518:1: expr_bitxor returns [AST node] : e1= expr_bitand ( '^' e2= expr_bitand )* ;
    def expr_bitxor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:519:2: (e1= expr_bitand ( '^' e2= expr_bitand )* )
                # src/ll/UL4.g:520:3: e1= expr_bitand ( '^' e2= expr_bitand )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2665)
                e1 = self.expr_bitand()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:521:3: ( '^' e2= expr_bitand )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 60) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:522:4: '^' e2= expr_bitand
                        pass 
                        self.match(self.input, 60, self.FOLLOW_60_in_expr_bitxor2676)

                        self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2683)
                        e2 = self.expr_bitand()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitXOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop40





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitxor"



    # $ANTLR start "expr_bitor"
    # src/ll/UL4.g:528:1: expr_bitor returns [AST node] : e1= expr_bitxor ( '|' e2= expr_bitxor )* ;
    def expr_bitor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:529:2: (e1= expr_bitxor ( '|' e2= expr_bitxor )* )
                # src/ll/UL4.g:530:3: e1= expr_bitxor ( '|' e2= expr_bitxor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2711)
                e1 = self.expr_bitxor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:531:3: ( '|' e2= expr_bitxor )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 70) :
                        alt41 = 1


                    if alt41 == 1:
                        # src/ll/UL4.g:532:4: '|' e2= expr_bitxor
                        pass 
                        self.match(self.input, 70, self.FOLLOW_70_in_expr_bitor2722)

                        self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2729)
                        e2 = self.expr_bitxor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop41





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitor"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:538:1: expr_cmp returns [node] : e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:539:2: (e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )* )
                # src/ll/UL4.g:540:3: e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2757)
                e1 = self.expr_bitor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:541:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 27 or LA43_0 == 48 or LA43_0 == 51 or (53 <= LA43_0 <= 55)) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:542:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' ) e2= expr_bitor
                        pass 
                        # src/ll/UL4.g:542:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' )
                        alt42 = 6
                        LA42 = self.input.LA(1)
                        if LA42 == 53:
                            alt42 = 1
                        elif LA42 == 27:
                            alt42 = 2
                        elif LA42 == 48:
                            alt42 = 3
                        elif LA42 == 51:
                            alt42 = 4
                        elif LA42 == 54:
                            alt42 = 5
                        elif LA42 == 55:
                            alt42 = 6
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 42, 0, self.input)

                            raise nvae


                        if alt42 == 1:
                            # src/ll/UL4.g:543:5: '=='
                            pass 
                            self.match(self.input, 53, self.FOLLOW_53_in_expr_cmp2774)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt42 == 2:
                            # src/ll/UL4.g:545:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr_cmp2787)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt42 == 3:
                            # src/ll/UL4.g:547:5: '<'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr_cmp2800)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt42 == 4:
                            # src/ll/UL4.g:549:5: '<='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr_cmp2813)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt42 == 5:
                            # src/ll/UL4.g:551:5: '>'
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_cmp2826)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt42 == 6:
                            # src/ll/UL4.g:553:5: '>='
                            pass 
                            self.match(self.input, 55, self.FOLLOW_55_in_expr_cmp2839)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 






                        self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2853)
                        e2 = self.expr_bitor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_contain"
    # src/ll/UL4.g:560:1: expr_contain returns [node] : e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? ;
    def expr_contain(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:561:2: (e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )? )
                # src/ll/UL4.g:562:3: e1= expr_cmp ( ( 'not' )? 'in' e2= expr_cmp )?
                pass 
                self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2881)
                e1 = self.expr_cmp()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = e1 



                # src/ll/UL4.g:563:3: ( ( 'not' )? 'in' e2= expr_cmp )?
                alt45 = 2
                LA45_0 = self.input.LA(1)

                if ((66 <= LA45_0 <= 67)) :
                    alt45 = 1
                if alt45 == 1:
                    # src/ll/UL4.g:564:4: ( 'not' )? 'in' e2= expr_cmp
                    pass 
                    if self._state.backtracking == 0:
                        pass
                        cls = ul4c.Contains 



                    # src/ll/UL4.g:565:4: ( 'not' )?
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 67) :
                        alt44 = 1
                    if alt44 == 1:
                        # src/ll/UL4.g:566:5: 'not'
                        pass 
                        self.match(self.input, 67, self.FOLLOW_67_in_expr_contain2903)

                        if self._state.backtracking == 0:
                            pass
                            cls = ul4c.NotContains 






                    self.match(self.input, 66, self.FOLLOW_66_in_expr_contain2916)

                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_contain2923)
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
    # src/ll/UL4.g:574:1: expr_and returns [node] : e1= expr_contain ( 'and' e2= expr_contain )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:575:2: (e1= expr_contain ( 'and' e2= expr_contain )* )
                # src/ll/UL4.g:576:3: e1= expr_contain ( 'and' e2= expr_contain )*
                pass 
                self._state.following.append(self.FOLLOW_expr_contain_in_expr_and2951)
                e1 = self.expr_contain()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:577:3: ( 'and' e2= expr_contain )*
                while True: #loop46
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == 62) :
                        alt46 = 1


                    if alt46 == 1:
                        # src/ll/UL4.g:578:4: 'and' e2= expr_contain
                        pass 
                        self.match(self.input, 62, self.FOLLOW_62_in_expr_and2962)

                        self._state.following.append(self.FOLLOW_expr_contain_in_expr_and2969)
                        e2 = self.expr_contain()

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
    # src/ll/UL4.g:584:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:585:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:586:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or2997)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:587:3: ( 'or' e2= expr_and )*
                while True: #loop47
                    alt47 = 2
                    LA47_0 = self.input.LA(1)

                    if (LA47_0 == 68) :
                        alt47 = 1


                    if alt47 == 1:
                        # src/ll/UL4.g:588:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 68, self.FOLLOW_68_in_expr_or3008)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or3015)
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
    # src/ll/UL4.g:594:1: expr_if returns [AST node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:595:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:596:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if3043)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:597:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if (LA48_0 == 65) :
                    LA48_1 = self.input.LA(2)

                    if (self.synpred75_UL4()) :
                        alt48 = 1
                if alt48 == 1:
                    # src/ll/UL4.g:598:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_expr_if3054)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3061)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 63, self.FOLLOW_63_in_expr_if3066)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3073)
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
    # src/ll/UL4.g:605:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:606:2: (ege= generatorexpression |e1= expr_if )
                alt49 = 2
                LA49 = self.input.LA(1)
                if LA49 == NONE:
                    LA49_1 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
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

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 10, self.input)

                        raise nvae


                elif LA49 == 58:
                    LA49_11 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 11, self.input)

                        raise nvae


                elif LA49 == 69:
                    LA49_12 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 12, self.input)

                        raise nvae


                elif LA49 == 32:
                    LA49_13 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 13, self.input)

                        raise nvae


                elif LA49 == 40:
                    LA49_14 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 14, self.input)

                        raise nvae


                elif LA49 == 73:
                    LA49_15 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 15, self.input)

                        raise nvae


                elif LA49 == 67:
                    LA49_16 = self.input.LA(2)

                    if (self.synpred76_UL4()) :
                        alt49 = 1
                    elif (True) :
                        alt49 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 49, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 49, 0, self.input)

                    raise nvae


                if alt49 == 1:
                    # src/ll/UL4.g:606:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg3097)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt49 == 2:
                    # src/ll/UL4.g:607:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg3106)
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
    # src/ll/UL4.g:610:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:611:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt50 = 2
                LA50 = self.input.LA(1)
                if LA50 == NONE:
                    LA50_1 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
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

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 10, self.input)

                        raise nvae


                elif LA50 == 58:
                    LA50_11 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 11, self.input)

                        raise nvae


                elif LA50 == 69:
                    LA50_12 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 12, self.input)

                        raise nvae


                elif LA50 == 32:
                    LA50_13 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 13, self.input)

                        raise nvae


                elif LA50 == 40:
                    LA50_14 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 14, self.input)

                        raise nvae


                elif LA50 == 73:
                    LA50_15 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 15, self.input)

                        raise nvae


                elif LA50 == 67:
                    LA50_16 = self.input.LA(2)

                    if (self.synpred77_UL4()) :
                        alt50 = 1
                    elif (True) :
                        alt50 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 50, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 50, 0, self.input)

                    raise nvae


                if alt50 == 1:
                    # src/ll/UL4.g:611:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3125)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3127)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt50 == 2:
                    # src/ll/UL4.g:612:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3136)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3138)

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
    # src/ll/UL4.g:618:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:619:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:620:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3163)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_for_3167)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3173)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ForBlock(self.location, self.start(n.start), e.end, ((n is not None) and [n.lvalue] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3179)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:629:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:630:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF )
                alt51 = 13
                LA51 = self.input.LA(1)
                if LA51 == NONE:
                    LA51_1 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 1, self.input)

                        raise nvae


                elif LA51 == FALSE:
                    LA51_2 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 2, self.input)

                        raise nvae


                elif LA51 == TRUE:
                    LA51_3 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 3, self.input)

                        raise nvae


                elif LA51 == INT:
                    LA51_4 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 4, self.input)

                        raise nvae


                elif LA51 == FLOAT:
                    LA51_5 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 5, self.input)

                        raise nvae


                elif LA51 == STRING:
                    LA51_6 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 6, self.input)

                        raise nvae


                elif LA51 == STRING3:
                    LA51_7 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 7, self.input)

                        raise nvae


                elif LA51 == DATE:
                    LA51_8 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 8, self.input)

                        raise nvae


                elif LA51 == COLOR:
                    LA51_9 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 9, self.input)

                        raise nvae


                elif LA51 == NAME:
                    LA51_10 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 10, self.input)

                        raise nvae


                elif LA51 == 58:
                    LA51_11 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 11, self.input)

                        raise nvae


                elif LA51 == 69:
                    LA51_12 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 12, self.input)

                        raise nvae


                elif LA51 == 32:
                    LA51_13 = self.input.LA(2)

                    if (self.synpred78_UL4()) :
                        alt51 = 1
                    elif (self.synpred79_UL4()) :
                        alt51 = 2
                    elif (self.synpred80_UL4()) :
                        alt51 = 3
                    elif (self.synpred81_UL4()) :
                        alt51 = 4
                    elif (self.synpred82_UL4()) :
                        alt51 = 5
                    elif (self.synpred83_UL4()) :
                        alt51 = 6
                    elif (self.synpred84_UL4()) :
                        alt51 = 7
                    elif (self.synpred85_UL4()) :
                        alt51 = 8
                    elif (self.synpred86_UL4()) :
                        alt51 = 9
                    elif (self.synpred87_UL4()) :
                        alt51 = 10
                    elif (self.synpred88_UL4()) :
                        alt51 = 11
                    elif (self.synpred89_UL4()) :
                        alt51 = 12
                    elif (True) :
                        alt51 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 51, 13, self.input)

                        raise nvae


                elif LA51 == 40 or LA51 == 67 or LA51 == 73:
                    alt51 = 13
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 51, 0, self.input)

                    raise nvae


                if alt51 == 1:
                    # src/ll/UL4.g:630:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3200)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_statement3202)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3206)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3208)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.lvalue] or [None])[0], e) 




                elif alt51 == 2:
                    # src/ll/UL4.g:631:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3217)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 38, self.FOLLOW_38_in_statement3219)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3223)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3225)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 3:
                    # src/ll/UL4.g:632:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3234)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement3236)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3240)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3242)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 4:
                    # src/ll/UL4.g:633:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3251)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement3253)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3257)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3259)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 5:
                    # src/ll/UL4.g:634:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3268)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement3270)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3274)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3276)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 6:
                    # src/ll/UL4.g:635:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3285)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement3287)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3291)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3293)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 7:
                    # src/ll/UL4.g:636:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3302)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3304)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3308)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3310)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 8:
                    # src/ll/UL4.g:637:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3319)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 50, self.FOLLOW_50_in_statement3321)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3325)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3327)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 9:
                    # src/ll/UL4.g:638:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3336)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 57, self.FOLLOW_57_in_statement3338)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3342)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3344)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 10:
                    # src/ll/UL4.g:639:4: n= expr_subscript '&=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3353)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement3355)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3359)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3361)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitAndVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 11:
                    # src/ll/UL4.g:640:4: n= expr_subscript '^=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3370)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 61, self.FOLLOW_61_in_statement3372)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3376)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3378)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitXOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 12:
                    # src/ll/UL4.g:641:4: n= expr_subscript '|=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3387)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 71, self.FOLLOW_71_in_statement3389)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3393)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3395)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt51 == 13:
                    # src/ll/UL4.g:642:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3404)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3406)

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



    # $ANTLR start "synpred49_UL4"
    def synpred49_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:437:4: ( '[' e2= expr_if close= ']' )
        # src/ll/UL4.g:437:4: '[' e2= expr_if close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred49_UL42234)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred49_UL42242)
        e2 = self.expr_if()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred49_UL42249)



    # $ANTLR end "synpred49_UL4"



    # $ANTLR start "synpred50_UL4"
    def synpred50_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:442:4: ( '[' e2= slice close= ']' )
        # src/ll/UL4.g:442:4: '[' e2= slice close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred50_UL42265)

        self._state.following.append(self.FOLLOW_slice_in_synpred50_UL42273)
        e2 = self.slice()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred50_UL42280)



    # $ANTLR end "synpred50_UL4"



    # $ANTLR start "synpred75_UL4"
    def synpred75_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:598:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:598:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 65, self.FOLLOW_65_in_synpred75_UL43054)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred75_UL43061)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 63, self.FOLLOW_63_in_synpred75_UL43066)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred75_UL43073)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred75_UL4"



    # $ANTLR start "synpred76_UL4"
    def synpred76_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:606:4: (ege= generatorexpression )
        # src/ll/UL4.g:606:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred76_UL43097)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred76_UL4"



    # $ANTLR start "synpred77_UL4"
    def synpred77_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:611:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:611:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred77_UL43125)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred77_UL43127)



    # $ANTLR end "synpred77_UL4"



    # $ANTLR start "synpred78_UL4"
    def synpred78_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:630:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:630:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred78_UL43200)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 52, self.FOLLOW_52_in_synpred78_UL43202)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred78_UL43206)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred78_UL43208)



    # $ANTLR end "synpred78_UL4"



    # $ANTLR start "synpred79_UL4"
    def synpred79_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:631:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:631:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred79_UL43217)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 38, self.FOLLOW_38_in_synpred79_UL43219)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred79_UL43223)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred79_UL43225)



    # $ANTLR end "synpred79_UL4"



    # $ANTLR start "synpred80_UL4"
    def synpred80_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:632:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:632:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred80_UL43234)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred80_UL43236)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred80_UL43240)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred80_UL43242)



    # $ANTLR end "synpred80_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:633:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:633:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred81_UL43251)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred81_UL43253)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred81_UL43257)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred81_UL43259)



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:634:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:634:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred82_UL43268)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred82_UL43270)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred82_UL43274)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred82_UL43276)



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:635:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:635:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred83_UL43285)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 45, self.FOLLOW_45_in_synpred83_UL43287)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred83_UL43291)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43293)



    # $ANTLR end "synpred83_UL4"



    # $ANTLR start "synpred84_UL4"
    def synpred84_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:636:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:636:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred84_UL43302)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred84_UL43304)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred84_UL43308)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred84_UL43310)



    # $ANTLR end "synpred84_UL4"



    # $ANTLR start "synpred85_UL4"
    def synpred85_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:637:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:637:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred85_UL43319)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 50, self.FOLLOW_50_in_synpred85_UL43321)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred85_UL43325)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred85_UL43327)



    # $ANTLR end "synpred85_UL4"



    # $ANTLR start "synpred86_UL4"
    def synpred86_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:638:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:638:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred86_UL43336)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 57, self.FOLLOW_57_in_synpred86_UL43338)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred86_UL43342)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred86_UL43344)



    # $ANTLR end "synpred86_UL4"



    # $ANTLR start "synpred87_UL4"
    def synpred87_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:639:4: (n= expr_subscript '&=' e= expr_if EOF )
        # src/ll/UL4.g:639:4: n= expr_subscript '&=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred87_UL43353)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 31, self.FOLLOW_31_in_synpred87_UL43355)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred87_UL43359)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred87_UL43361)



    # $ANTLR end "synpred87_UL4"



    # $ANTLR start "synpred88_UL4"
    def synpred88_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:640:4: (n= expr_subscript '^=' e= expr_if EOF )
        # src/ll/UL4.g:640:4: n= expr_subscript '^=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred88_UL43370)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 61, self.FOLLOW_61_in_synpred88_UL43372)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred88_UL43376)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred88_UL43378)



    # $ANTLR end "synpred88_UL4"



    # $ANTLR start "synpred89_UL4"
    def synpred89_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:641:4: (n= expr_subscript '|=' e= expr_if EOF )
        # src/ll/UL4.g:641:4: n= expr_subscript '|=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred89_UL43387)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 71, self.FOLLOW_71_in_synpred89_UL43389)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred89_UL43393)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred89_UL43395)



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

    def synpred50_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred50_UL4_fragment()
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
    FOLLOW_expr_if_in_slice1706 = frozenset([47])
    FOLLOW_47_in_slice1719 = frozenset([1, 5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_slice1732 = frozenset([1])
    FOLLOW_atom_in_expr_subscript1762 = frozenset([1, 32, 42, 58])
    FOLLOW_42_in_expr_subscript1778 = frozenset([14])
    FOLLOW_name_in_expr_subscript1785 = frozenset([1, 32, 42, 58])
    FOLLOW_32_in_expr_subscript1801 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 67, 69, 73])
    FOLLOW_35_in_expr_subscript1831 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1835 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1843 = frozenset([33])
    FOLLOW_34_in_expr_subscript1861 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1865 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1880 = frozenset([35])
    FOLLOW_35_in_expr_subscript1887 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1891 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1906 = frozenset([33])
    FOLLOW_exprarg_in_expr_subscript1926 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1941 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1950 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript1972 = frozenset([14])
    FOLLOW_name_in_expr_subscript1981 = frozenset([52])
    FOLLOW_52_in_expr_subscript1983 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript1987 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2009 = frozenset([34])
    FOLLOW_34_in_expr_subscript2016 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2020 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2042 = frozenset([35])
    FOLLOW_35_in_expr_subscript2049 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2053 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2068 = frozenset([33])
    FOLLOW_name_in_expr_subscript2088 = frozenset([52])
    FOLLOW_52_in_expr_subscript2090 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2094 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2109 = frozenset([14])
    FOLLOW_name_in_expr_subscript2118 = frozenset([52])
    FOLLOW_52_in_expr_subscript2120 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2124 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2146 = frozenset([34])
    FOLLOW_34_in_expr_subscript2153 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2157 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2179 = frozenset([35])
    FOLLOW_35_in_expr_subscript2186 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2190 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2205 = frozenset([33])
    FOLLOW_33_in_expr_subscript2218 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2234 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_expr_subscript2242 = frozenset([59])
    FOLLOW_59_in_expr_subscript2249 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2265 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 67, 69, 73])
    FOLLOW_slice_in_expr_subscript2273 = frozenset([59])
    FOLLOW_59_in_expr_subscript2280 = frozenset([1, 32, 42, 58])
    FOLLOW_expr_subscript_in_expr_unary2308 = frozenset([1])
    FOLLOW_40_in_expr_unary2319 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2323 = frozenset([1])
    FOLLOW_73_in_expr_unary2334 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2338 = frozenset([1])
    FOLLOW_67_in_expr_unary2349 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2353 = frozenset([1])
    FOLLOW_expr_unary_in_expr_mul2377 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_34_in_expr_mul2394 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_43_in_expr_mul2407 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_44_in_expr_mul2420 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_28_in_expr_mul2433 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_unary_in_expr_mul2447 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_expr_mul_in_expr_add2475 = frozenset([1, 37, 40])
    FOLLOW_37_in_expr_add2492 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_40_in_expr_add2505 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_mul_in_expr_add2519 = frozenset([1, 37, 40])
    FOLLOW_expr_add_in_expr_bitshift2547 = frozenset([1, 49, 56])
    FOLLOW_49_in_expr_bitshift2564 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_56_in_expr_bitshift2577 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_add_in_expr_bitshift2591 = frozenset([1, 49, 56])
    FOLLOW_expr_bitshift_in_expr_bitand2619 = frozenset([1, 30])
    FOLLOW_30_in_expr_bitand2630 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitshift_in_expr_bitand2637 = frozenset([1, 30])
    FOLLOW_expr_bitand_in_expr_bitxor2665 = frozenset([1, 60])
    FOLLOW_60_in_expr_bitxor2676 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitand_in_expr_bitxor2683 = frozenset([1, 60])
    FOLLOW_expr_bitxor_in_expr_bitor2711 = frozenset([1, 70])
    FOLLOW_70_in_expr_bitor2722 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitxor_in_expr_bitor2729 = frozenset([1, 70])
    FOLLOW_expr_bitor_in_expr_cmp2757 = frozenset([1, 27, 48, 51, 53, 54, 55])
    FOLLOW_53_in_expr_cmp2774 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_27_in_expr_cmp2787 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_48_in_expr_cmp2800 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_51_in_expr_cmp2813 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_54_in_expr_cmp2826 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_55_in_expr_cmp2839 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_bitor_in_expr_cmp2853 = frozenset([1, 27, 48, 51, 53, 54, 55])
    FOLLOW_expr_cmp_in_expr_contain2881 = frozenset([1, 66, 67])
    FOLLOW_67_in_expr_contain2903 = frozenset([66])
    FOLLOW_66_in_expr_contain2916 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_cmp_in_expr_contain2923 = frozenset([1])
    FOLLOW_expr_contain_in_expr_and2951 = frozenset([1, 62])
    FOLLOW_62_in_expr_and2962 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_contain_in_expr_and2969 = frozenset([1, 62])
    FOLLOW_expr_and_in_expr_or2997 = frozenset([1, 68])
    FOLLOW_68_in_expr_or3008 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_and_in_expr_or3015 = frozenset([1, 68])
    FOLLOW_expr_or_in_expr_if3043 = frozenset([1, 65])
    FOLLOW_65_in_expr_if3054 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3061 = frozenset([63])
    FOLLOW_63_in_expr_if3066 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3073 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg3097 = frozenset([1])
    FOLLOW_expr_if_in_exprarg3106 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3125 = frozenset([])
    FOLLOW_EOF_in_expression3127 = frozenset([1])
    FOLLOW_expr_if_in_expression3136 = frozenset([])
    FOLLOW_EOF_in_expression3138 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3163 = frozenset([66])
    FOLLOW_66_in_for_3167 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_for_3173 = frozenset([])
    FOLLOW_EOF_in_for_3179 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3200 = frozenset([52])
    FOLLOW_52_in_statement3202 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3206 = frozenset([])
    FOLLOW_EOF_in_statement3208 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3217 = frozenset([38])
    FOLLOW_38_in_statement3219 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3223 = frozenset([])
    FOLLOW_EOF_in_statement3225 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3234 = frozenset([41])
    FOLLOW_41_in_statement3236 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3240 = frozenset([])
    FOLLOW_EOF_in_statement3242 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3251 = frozenset([36])
    FOLLOW_36_in_statement3253 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3257 = frozenset([])
    FOLLOW_EOF_in_statement3259 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3268 = frozenset([46])
    FOLLOW_46_in_statement3270 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3274 = frozenset([])
    FOLLOW_EOF_in_statement3276 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3285 = frozenset([45])
    FOLLOW_45_in_statement3287 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3291 = frozenset([])
    FOLLOW_EOF_in_statement3293 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3302 = frozenset([29])
    FOLLOW_29_in_statement3304 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3308 = frozenset([])
    FOLLOW_EOF_in_statement3310 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3319 = frozenset([50])
    FOLLOW_50_in_statement3321 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3325 = frozenset([])
    FOLLOW_EOF_in_statement3327 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3336 = frozenset([57])
    FOLLOW_57_in_statement3338 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3342 = frozenset([])
    FOLLOW_EOF_in_statement3344 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3353 = frozenset([31])
    FOLLOW_31_in_statement3355 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3359 = frozenset([])
    FOLLOW_EOF_in_statement3361 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3370 = frozenset([61])
    FOLLOW_61_in_statement3372 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3376 = frozenset([])
    FOLLOW_EOF_in_statement3378 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3387 = frozenset([71])
    FOLLOW_71_in_statement3389 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3393 = frozenset([])
    FOLLOW_EOF_in_statement3395 = frozenset([1])
    FOLLOW_expression_in_statement3404 = frozenset([])
    FOLLOW_EOF_in_statement3406 = frozenset([1])
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
    FOLLOW_58_in_synpred49_UL42234 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred49_UL42242 = frozenset([59])
    FOLLOW_59_in_synpred49_UL42249 = frozenset([1])
    FOLLOW_58_in_synpred50_UL42265 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 67, 69, 73])
    FOLLOW_slice_in_synpred50_UL42273 = frozenset([59])
    FOLLOW_59_in_synpred50_UL42280 = frozenset([1])
    FOLLOW_65_in_synpred75_UL43054 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred75_UL43061 = frozenset([63])
    FOLLOW_63_in_synpred75_UL43066 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred75_UL43073 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred76_UL43097 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred77_UL43125 = frozenset([])
    FOLLOW_EOF_in_synpred77_UL43127 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred78_UL43200 = frozenset([52])
    FOLLOW_52_in_synpred78_UL43202 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred78_UL43206 = frozenset([])
    FOLLOW_EOF_in_synpred78_UL43208 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred79_UL43217 = frozenset([38])
    FOLLOW_38_in_synpred79_UL43219 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred79_UL43223 = frozenset([])
    FOLLOW_EOF_in_synpred79_UL43225 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred80_UL43234 = frozenset([41])
    FOLLOW_41_in_synpred80_UL43236 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred80_UL43240 = frozenset([])
    FOLLOW_EOF_in_synpred80_UL43242 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred81_UL43251 = frozenset([36])
    FOLLOW_36_in_synpred81_UL43253 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred81_UL43257 = frozenset([])
    FOLLOW_EOF_in_synpred81_UL43259 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred82_UL43268 = frozenset([46])
    FOLLOW_46_in_synpred82_UL43270 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred82_UL43274 = frozenset([])
    FOLLOW_EOF_in_synpred82_UL43276 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred83_UL43285 = frozenset([45])
    FOLLOW_45_in_synpred83_UL43287 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred83_UL43291 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43293 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred84_UL43302 = frozenset([29])
    FOLLOW_29_in_synpred84_UL43304 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred84_UL43308 = frozenset([])
    FOLLOW_EOF_in_synpred84_UL43310 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred85_UL43319 = frozenset([50])
    FOLLOW_50_in_synpred85_UL43321 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred85_UL43325 = frozenset([])
    FOLLOW_EOF_in_synpred85_UL43327 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred86_UL43336 = frozenset([57])
    FOLLOW_57_in_synpred86_UL43338 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred86_UL43342 = frozenset([])
    FOLLOW_EOF_in_synpred86_UL43344 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred87_UL43353 = frozenset([31])
    FOLLOW_31_in_synpred87_UL43355 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred87_UL43359 = frozenset([])
    FOLLOW_EOF_in_synpred87_UL43361 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred88_UL43370 = frozenset([61])
    FOLLOW_61_in_synpred88_UL43372 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred88_UL43376 = frozenset([])
    FOLLOW_EOF_in_synpred88_UL43378 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred89_UL43387 = frozenset([71])
    FOLLOW_71_in_synpred89_UL43389 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred89_UL43393 = frozenset([])
    FOLLOW_EOF_in_synpred89_UL43395 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
