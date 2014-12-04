# $ANTLR 3.5 src/ll/UL4.g 2014-12-04 16:45:10

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



    # $ANTLR start "set"
    # src/ll/UL4.g:250:1: set returns [node] : (open= '{' '/' close= '}' |open= '{' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= '}' );
    def set(self, ):
        node = None


        open = None
        close = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:251:2: (open= '{' '/' close= '}' |open= '{' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= '}' )
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 69) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 43) :
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
                    # src/ll/UL4.g:252:3: open= '{' '/' close= '}'
                    pass 
                    open = self.match(self.input, 69, self.FOLLOW_69_in_set1223)

                    self.match(self.input, 43, self.FOLLOW_43_in_set1227)

                    close = self.match(self.input, 72, self.FOLLOW_72_in_set1233)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.location, self.start(open), self.end(close)) 




                elif alt9 == 2:
                    # src/ll/UL4.g:256:3: open= '{' e1= expr_if ( ',' e2= expr_if )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 69, self.FOLLOW_69_in_set1244)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Set(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_expr_if_in_set1252)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(e1) 



                    # src/ll/UL4.g:258:3: ( ',' e2= expr_if )*
                    while True: #loop7
                        alt7 = 2
                        LA7_0 = self.input.LA(1)

                        if (LA7_0 == 39) :
                            LA7_1 = self.input.LA(2)

                            if ((COLOR <= LA7_1 <= DATE) or (FALSE <= LA7_1 <= FLOAT) or (INT <= LA7_1 <= NONE) or (STRING <= LA7_1 <= STRING3) or LA7_1 == TRUE or LA7_1 == 32 or LA7_1 == 40 or LA7_1 == 58 or LA7_1 == 67 or LA7_1 == 69 or LA7_1 == 73) :
                                alt7 = 1




                        if alt7 == 1:
                            # src/ll/UL4.g:259:4: ',' e2= expr_if
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_set1263)

                            self._state.following.append(self.FOLLOW_expr_if_in_set1270)
                            e2 = self.expr_if()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(e2) 




                        else:
                            break #loop7


                    # src/ll/UL4.g:262:3: ( ',' )?
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == 39) :
                        alt8 = 1
                    if alt8 == 1:
                        # src/ll/UL4.g:262:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_set1281)




                    close = self.match(self.input, 72, self.FOLLOW_72_in_set1288)

                    if self._state.backtracking == 0:
                        pass
                        node.end = self.end(close) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "set"



    # $ANTLR start "setcomprehension"
    # src/ll/UL4.g:266:1: setcomprehension returns [node] : open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
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
                # src/ll/UL4.g:271:2: (open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:272:3: open= '{' item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 69, self.FOLLOW_69_in_setcomprehension1316)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1322)
                item = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_setcomprehension1326)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_setcomprehension1332)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_setcomprehension1336)

                self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1342)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:278:3: ( 'if' condition= expr_if )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == 65) :
                    alt10 = 1
                if alt10 == 1:
                    # src/ll/UL4.g:279:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_setcomprehension1351)

                    self._state.following.append(self.FOLLOW_expr_if_in_setcomprehension1358)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 72, self.FOLLOW_72_in_setcomprehension1371)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.SetComp(self.location, self.start(open), self.end(close), item, ((n is not None) and [n.lvalue] or [None])[0], container, _condition) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "setcomprehension"



    # $ANTLR start "dictitem"
    # src/ll/UL4.g:287:1: fragment dictitem returns [node] : k= expr_if ':' v= expr_if ;
    def dictitem(self, ):
        node = None


        k = None
        v = None

        try:
            try:
                # src/ll/UL4.g:288:2: (k= expr_if ':' v= expr_if )
                # src/ll/UL4.g:289:3: k= expr_if ':' v= expr_if
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_dictitem1396)
                k = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 47, self.FOLLOW_47_in_dictitem1400)

                self._state.following.append(self.FOLLOW_expr_if_in_dictitem1406)
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
    # src/ll/UL4.g:294:1: dict returns [node] : (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' );
    def dict(self, ):
        node = None


        open = None
        close = None
        i1 = None
        i2 = None

        try:
            try:
                # src/ll/UL4.g:295:2: (open= '{' close= '}' |open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}' )
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if (LA13_0 == 69) :
                    LA13_1 = self.input.LA(2)

                    if (LA13_1 == 72) :
                        alt13 = 1
                    elif ((COLOR <= LA13_1 <= DATE) or (FALSE <= LA13_1 <= FLOAT) or (INT <= LA13_1 <= NONE) or (STRING <= LA13_1 <= STRING3) or LA13_1 == TRUE or LA13_1 == 32 or LA13_1 == 40 or LA13_1 == 58 or LA13_1 == 67 or LA13_1 == 69 or LA13_1 == 73) :
                        alt13 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 13, 1, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 13, 0, self.input)

                    raise nvae


                if alt13 == 1:
                    # src/ll/UL4.g:296:3: open= '{' close= '}'
                    pass 
                    open = self.match(self.input, 69, self.FOLLOW_69_in_dict1427)

                    close = self.match(self.input, 72, self.FOLLOW_72_in_dict1433)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), self.end(close)) 




                elif alt13 == 2:
                    # src/ll/UL4.g:299:3: open= '{' i1= dictitem ( ',' i2= dictitem )* ( ',' )? close= '}'
                    pass 
                    open = self.match(self.input, 69, self.FOLLOW_69_in_dict1444)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Dict(self.location, self.start(open), None) 



                    self._state.following.append(self.FOLLOW_dictitem_in_dict1452)
                    i1 = self.dictitem()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.items.append(i1) 



                    # src/ll/UL4.g:301:3: ( ',' i2= dictitem )*
                    while True: #loop11
                        alt11 = 2
                        LA11_0 = self.input.LA(1)

                        if (LA11_0 == 39) :
                            LA11_1 = self.input.LA(2)

                            if ((COLOR <= LA11_1 <= DATE) or (FALSE <= LA11_1 <= FLOAT) or (INT <= LA11_1 <= NONE) or (STRING <= LA11_1 <= STRING3) or LA11_1 == TRUE or LA11_1 == 32 or LA11_1 == 40 or LA11_1 == 58 or LA11_1 == 67 or LA11_1 == 69 or LA11_1 == 73) :
                                alt11 = 1




                        if alt11 == 1:
                            # src/ll/UL4.g:302:4: ',' i2= dictitem
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_dict1463)

                            self._state.following.append(self.FOLLOW_dictitem_in_dict1470)
                            i2 = self.dictitem()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.items.append(i2) 




                        else:
                            break #loop11


                    # src/ll/UL4.g:305:3: ( ',' )?
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if (LA12_0 == 39) :
                        alt12 = 1
                    if alt12 == 1:
                        # src/ll/UL4.g:305:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_dict1481)




                    close = self.match(self.input, 72, self.FOLLOW_72_in_dict1488)

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
    # src/ll/UL4.g:309:1: dictcomprehension returns [node] : open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' ;
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
                # src/ll/UL4.g:314:2: (open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}' )
                # src/ll/UL4.g:315:3: open= '{' key= expr_if ':' value= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? close= '}'
                pass 
                open = self.match(self.input, 69, self.FOLLOW_69_in_dictcomprehension1516)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1522)
                key = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 47, self.FOLLOW_47_in_dictcomprehension1526)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1532)
                value = self.expr_if()

                self._state.following.pop()

                self.match(self.input, 64, self.FOLLOW_64_in_dictcomprehension1536)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_dictcomprehension1542)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_dictcomprehension1546)

                self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1552)
                container = self.expr_if()

                self._state.following.pop()

                # src/ll/UL4.g:323:3: ( 'if' condition= expr_if )?
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if (LA14_0 == 65) :
                    alt14 = 1
                if alt14 == 1:
                    # src/ll/UL4.g:324:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_dictcomprehension1561)

                    self._state.following.append(self.FOLLOW_expr_if_in_dictcomprehension1568)
                    condition = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        _condition = condition; 






                close = self.match(self.input, 72, self.FOLLOW_72_in_dictcomprehension1581)

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
    # src/ll/UL4.g:330:1: generatorexpression returns [node] : item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? ;
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
                # src/ll/UL4.g:336:2: (item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )? )
                # src/ll/UL4.g:337:3: item= expr_if 'for' n= nestedlvalue 'in' container= expr_if ( 'if' condition= expr_if )?
                pass 
                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1609)
                item = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _start = item.start 



                self.match(self.input, 64, self.FOLLOW_64_in_generatorexpression1615)

                self._state.following.append(self.FOLLOW_nestedlvalue_in_generatorexpression1621)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_generatorexpression1625)

                self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1631)
                container = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    _end = container.end 



                # src/ll/UL4.g:342:3: ( 'if' condition= expr_if )?
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == 65) :
                    alt15 = 1
                if alt15 == 1:
                    # src/ll/UL4.g:343:4: 'if' condition= expr_if
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_generatorexpression1642)

                    self._state.following.append(self.FOLLOW_expr_if_in_generatorexpression1649)
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
    # src/ll/UL4.g:348:1: atom returns [node] : (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' );
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
                # src/ll/UL4.g:349:2: (e_literal= literal |e_list= list |e_listcomp= listcomprehension |e_set= set |e_setcomp= setcomprehension |e_dict= dict |e_dictcomp= dictcomprehension |open= '(' e_genexpr= generatorexpression close= ')' |open= '(' e_bracket= expr_if close= ')' )
                alt16 = 9
                LA16 = self.input.LA(1)
                if LA16 == COLOR or LA16 == DATE or LA16 == FALSE or LA16 == FLOAT or LA16 == INT or LA16 == NAME or LA16 == NONE or LA16 == STRING or LA16 == STRING3 or LA16 == TRUE:
                    alt16 = 1
                elif LA16 == 58:
                    LA16_11 = self.input.LA(2)

                    if (self.synpred24_UL4()) :
                        alt16 = 2
                    elif (self.synpred25_UL4()) :
                        alt16 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 16, 11, self.input)

                        raise nvae


                elif LA16 == 69:
                    LA16_12 = self.input.LA(2)

                    if (self.synpred26_UL4()) :
                        alt16 = 4
                    elif (self.synpred27_UL4()) :
                        alt16 = 5
                    elif (self.synpred28_UL4()) :
                        alt16 = 6
                    elif (self.synpred29_UL4()) :
                        alt16 = 7
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 16, 12, self.input)

                        raise nvae


                elif LA16 == 32:
                    LA16_13 = self.input.LA(2)

                    if (self.synpred30_UL4()) :
                        alt16 = 8
                    elif (True) :
                        alt16 = 9
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 16, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 16, 0, self.input)

                    raise nvae


                if alt16 == 1:
                    # src/ll/UL4.g:349:4: e_literal= literal
                    pass 
                    self._state.following.append(self.FOLLOW_literal_in_atom1675)
                    e_literal = self.literal()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_literal 




                elif alt16 == 2:
                    # src/ll/UL4.g:350:4: e_list= list
                    pass 
                    self._state.following.append(self.FOLLOW_list_in_atom1684)
                    e_list = self.list()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_list 




                elif alt16 == 3:
                    # src/ll/UL4.g:351:4: e_listcomp= listcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_listcomprehension_in_atom1693)
                    e_listcomp = self.listcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_listcomp 




                elif alt16 == 4:
                    # src/ll/UL4.g:352:4: e_set= set
                    pass 
                    self._state.following.append(self.FOLLOW_set_in_atom1702)
                    e_set = self.set()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_set 




                elif alt16 == 5:
                    # src/ll/UL4.g:353:4: e_setcomp= setcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_setcomprehension_in_atom1711)
                    e_setcomp = self.setcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_setcomp 




                elif alt16 == 6:
                    # src/ll/UL4.g:354:4: e_dict= dict
                    pass 
                    self._state.following.append(self.FOLLOW_dict_in_atom1720)
                    e_dict = self.dict()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dict 




                elif alt16 == 7:
                    # src/ll/UL4.g:355:4: e_dictcomp= dictcomprehension
                    pass 
                    self._state.following.append(self.FOLLOW_dictcomprehension_in_atom1729)
                    e_dictcomp = self.dictcomprehension()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e_dictcomp 




                elif alt16 == 8:
                    # src/ll/UL4.g:356:4: open= '(' e_genexpr= generatorexpression close= ')'
                    pass 
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1738)

                    self._state.following.append(self.FOLLOW_generatorexpression_in_atom1742)
                    e_genexpr = self.generatorexpression()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1746)

                    if self._state.backtracking == 0:
                        pass
                                                                            
                        node = e_genexpr
                        node.start = self.start(open)
                        node.end = self.end(close)
                        	




                elif alt16 == 9:
                    # src/ll/UL4.g:361:4: open= '(' e_bracket= expr_if close= ')'
                    pass 
                    open = self.match(self.input, 32, self.FOLLOW_32_in_atom1755)

                    self._state.following.append(self.FOLLOW_expr_if_in_atom1759)
                    e_bracket = self.expr_if()

                    self._state.following.pop()

                    close = self.match(self.input, 33, self.FOLLOW_33_in_atom1763)

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
    # src/ll/UL4.g:369:1: nestedlvalue returns [lvalue] : (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' );
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
                # src/ll/UL4.g:370:2: (n= expr_subscript | '(' n0= nestedlvalue ',' ')' | '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')' )
                alt19 = 3
                LA19_0 = self.input.LA(1)

                if ((COLOR <= LA19_0 <= DATE) or (FALSE <= LA19_0 <= FLOAT) or (INT <= LA19_0 <= NONE) or (STRING <= LA19_0 <= STRING3) or LA19_0 == TRUE or LA19_0 == 58 or LA19_0 == 69) :
                    alt19 = 1
                elif (LA19_0 == 32) :
                    LA19_13 = self.input.LA(2)

                    if (self.synpred31_UL4()) :
                        alt19 = 1
                    elif (self.synpred32_UL4()) :
                        alt19 = 2
                    elif (True) :
                        alt19 = 3
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 19, 13, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 19, 0, self.input)

                    raise nvae


                if alt19 == 1:
                    # src/ll/UL4.g:371:3: n= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_nestedlvalue1786)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue =  ((n is not None) and [n.node] or [None])[0] 




                elif alt19 == 2:
                    # src/ll/UL4.g:373:3: '(' n0= nestedlvalue ',' ')'
                    pass 
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1795)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1799)
                    n0 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1801)

                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1803)

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n0 is not None) and [n0.lvalue] or [None])[0],) 




                elif alt19 == 3:
                    # src/ll/UL4.g:375:3: '(' n1= nestedlvalue ',' n2= nestedlvalue ( ',' n3= nestedlvalue )* ( ',' )? ')'
                    pass 
                    self.match(self.input, 32, self.FOLLOW_32_in_nestedlvalue1812)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1818)
                    n1 = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1822)

                    self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1828)
                    n2 = self.nestedlvalue()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        retval.lvalue = (((n1 is not None) and [n1.lvalue] or [None])[0], ((n2 is not None) and [n2.lvalue] or [None])[0]) 



                    # src/ll/UL4.g:379:3: ( ',' n3= nestedlvalue )*
                    while True: #loop17
                        alt17 = 2
                        LA17_0 = self.input.LA(1)

                        if (LA17_0 == 39) :
                            LA17_1 = self.input.LA(2)

                            if ((COLOR <= LA17_1 <= DATE) or (FALSE <= LA17_1 <= FLOAT) or (INT <= LA17_1 <= NONE) or (STRING <= LA17_1 <= STRING3) or LA17_1 == TRUE or LA17_1 == 32 or LA17_1 == 58 or LA17_1 == 69) :
                                alt17 = 1




                        if alt17 == 1:
                            # src/ll/UL4.g:380:4: ',' n3= nestedlvalue
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1839)

                            self._state.following.append(self.FOLLOW_nestedlvalue_in_nestedlvalue1846)
                            n3 = self.nestedlvalue()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.lvalue += (((n3 is not None) and [n3.lvalue] or [None])[0],) 




                        else:
                            break #loop17


                    # src/ll/UL4.g:383:3: ( ',' )?
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == 39) :
                        alt18 = 1
                    if alt18 == 1:
                        # src/ll/UL4.g:383:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_nestedlvalue1857)




                    self.match(self.input, 33, self.FOLLOW_33_in_nestedlvalue1862)


                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "nestedlvalue"



    # $ANTLR start "slice"
    # src/ll/UL4.g:388:1: slice returns [node] : (e1= expr_if )? colon= ':' (e2= expr_if )? ;
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
                # src/ll/UL4.g:396:2: ( (e1= expr_if )? colon= ':' (e2= expr_if )? )
                # src/ll/UL4.g:397:3: (e1= expr_if )? colon= ':' (e2= expr_if )?
                pass 
                # src/ll/UL4.g:397:3: (e1= expr_if )?
                alt20 = 2
                LA20_0 = self.input.LA(1)

                if ((COLOR <= LA20_0 <= DATE) or (FALSE <= LA20_0 <= FLOAT) or (INT <= LA20_0 <= NONE) or (STRING <= LA20_0 <= STRING3) or LA20_0 == TRUE or LA20_0 == 32 or LA20_0 == 40 or LA20_0 == 58 or LA20_0 == 67 or LA20_0 == 69 or LA20_0 == 73) :
                    alt20 = 1
                if alt20 == 1:
                    # src/ll/UL4.g:398:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1895)
                    e1 = self.expr_if()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        index1 = e1; startpos = e1.start; 






                colon = self.match(self.input, 47, self.FOLLOW_47_in_slice1908)

                if self._state.backtracking == 0:
                    pass
                                
                    if startpos is None:
                    	startpos = self.start(colon)
                    endpos = self.end(colon)
                    		



                # src/ll/UL4.g:405:3: (e2= expr_if )?
                alt21 = 2
                LA21_0 = self.input.LA(1)

                if ((COLOR <= LA21_0 <= DATE) or (FALSE <= LA21_0 <= FLOAT) or (INT <= LA21_0 <= NONE) or (STRING <= LA21_0 <= STRING3) or LA21_0 == TRUE or LA21_0 == 32 or LA21_0 == 40 or LA21_0 == 58 or LA21_0 == 67 or LA21_0 == 69 or LA21_0 == 73) :
                    alt21 = 1
                if alt21 == 1:
                    # src/ll/UL4.g:406:4: e2= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_slice1921)
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
    # src/ll/UL4.g:411:1: expr_subscript returns [node] : e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* ;
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
                # src/ll/UL4.g:412:2: (e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )* )
                # src/ll/UL4.g:413:3: e1= atom ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                pass 
                self._state.following.append(self.FOLLOW_atom_in_expr_subscript1951)
                e1 = self.atom()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    retval.node =  e1 



                # src/ll/UL4.g:414:3: ( '.' n= name | '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')' | '[' e2= expr_if close= ']' | '[' e2= slice close= ']' )*
                while True: #loop35
                    alt35 = 5
                    LA35 = self.input.LA(1)
                    if LA35 == 42:
                        alt35 = 1
                    elif LA35 == 32:
                        alt35 = 2
                    elif LA35 == 58:
                        LA35_45 = self.input.LA(2)

                        if (self.synpred55_UL4()) :
                            alt35 = 3
                        elif (self.synpred56_UL4()) :
                            alt35 = 4



                    if alt35 == 1:
                        # src/ll/UL4.g:416:4: '.' n= name
                        pass 
                        self.match(self.input, 42, self.FOLLOW_42_in_expr_subscript1967)

                        self._state.following.append(self.FOLLOW_name_in_expr_subscript1974)
                        n = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Attr(self.location, retval.node.start, self.end(n.stop), retval.node, ((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0]) 




                    elif alt35 == 2:
                        # src/ll/UL4.g:420:4: '(' (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? ) close= ')'
                        pass 
                        self.match(self.input, 32, self.FOLLOW_32_in_expr_subscript1990)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Call(self.location, retval.node.start, None, retval.node) 



                        # src/ll/UL4.g:421:4: (| '**' rkwargs= exprarg ( ',' )? | '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )? |a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? |an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )? )
                        alt34 = 5
                        LA34 = self.input.LA(1)
                        if LA34 == 33:
                            alt34 = 1
                        elif LA34 == 35:
                            alt34 = 2
                        elif LA34 == 34:
                            alt34 = 3
                        elif LA34 == COLOR or LA34 == DATE or LA34 == FALSE or LA34 == FLOAT or LA34 == INT or LA34 == NONE or LA34 == STRING or LA34 == STRING3 or LA34 == TRUE or LA34 == 32 or LA34 == 40 or LA34 == 58 or LA34 == 67 or LA34 == 69 or LA34 == 73:
                            alt34 = 4
                        elif LA34 == NAME:
                            LA34_5 = self.input.LA(2)

                            if ((27 <= LA34_5 <= 28) or LA34_5 == 30 or (32 <= LA34_5 <= 34) or LA34_5 == 37 or (39 <= LA34_5 <= 40) or (42 <= LA34_5 <= 44) or (48 <= LA34_5 <= 49) or LA34_5 == 51 or (53 <= LA34_5 <= 56) or LA34_5 == 58 or LA34_5 == 60 or LA34_5 == 62 or (64 <= LA34_5 <= 68) or LA34_5 == 70) :
                                alt34 = 4
                            elif (LA34_5 == 52) :
                                alt34 = 5
                            else:
                                if self._state.backtracking > 0:
                                    raise BacktrackingFailed


                                nvae = NoViableAltException("", 34, 5, self.input)

                                raise nvae


                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 34, 0, self.input)

                            raise nvae


                        if alt34 == 1:
                            # src/ll/UL4.g:423:4: 
                            pass 

                        elif alt34 == 2:
                            # src/ll/UL4.g:425:5: '**' rkwargs= exprarg ( ',' )?
                            pass 
                            self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2020)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2024)
                            rkwargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append(("**", rkwargs)); 



                            # src/ll/UL4.g:426:5: ( ',' )?
                            alt22 = 2
                            LA22_0 = self.input.LA(1)

                            if (LA22_0 == 39) :
                                alt22 = 1
                            if alt22 == 1:
                                # src/ll/UL4.g:426:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2032)





                        elif alt34 == 3:
                            # src/ll/UL4.g:429:5: '*' rargs= exprarg ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2050)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2054)
                            rargs = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append(("*", rargs)); 



                            # src/ll/UL4.g:430:5: ( ',' '**' rkwargs= exprarg )?
                            alt23 = 2
                            LA23_0 = self.input.LA(1)

                            if (LA23_0 == 39) :
                                LA23_1 = self.input.LA(2)

                                if (LA23_1 == 35) :
                                    alt23 = 1
                            if alt23 == 1:
                                # src/ll/UL4.g:431:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2069)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2076)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2080)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.args.append(("**", rkwargs)); 






                            # src/ll/UL4.g:434:5: ( ',' )?
                            alt24 = 2
                            LA24_0 = self.input.LA(1)

                            if (LA24_0 == 39) :
                                alt24 = 1
                            if alt24 == 1:
                                # src/ll/UL4.g:434:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2095)





                        elif alt34 == 4:
                            # src/ll/UL4.g:437:5: a1= exprarg ( ',' a2= exprarg )* ( ',' an3= name '=' av3= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2115)
                            a1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append((None, a1)); 



                            # src/ll/UL4.g:438:5: ( ',' a2= exprarg )*
                            while True: #loop25
                                alt25 = 2
                                LA25_0 = self.input.LA(1)

                                if (LA25_0 == 39) :
                                    LA25_1 = self.input.LA(2)

                                    if (LA25_1 == NAME) :
                                        LA25_3 = self.input.LA(3)

                                        if ((27 <= LA25_3 <= 28) or LA25_3 == 30 or (32 <= LA25_3 <= 34) or LA25_3 == 37 or (39 <= LA25_3 <= 40) or (42 <= LA25_3 <= 44) or (48 <= LA25_3 <= 49) or LA25_3 == 51 or (53 <= LA25_3 <= 56) or LA25_3 == 58 or LA25_3 == 60 or LA25_3 == 62 or (64 <= LA25_3 <= 68) or LA25_3 == 70) :
                                            alt25 = 1


                                    elif ((COLOR <= LA25_1 <= DATE) or (FALSE <= LA25_1 <= FLOAT) or LA25_1 == INT or LA25_1 == NONE or (STRING <= LA25_1 <= STRING3) or LA25_1 == TRUE or LA25_1 == 32 or LA25_1 == 40 or LA25_1 == 58 or LA25_1 == 67 or LA25_1 == 69 or LA25_1 == 73) :
                                        alt25 = 1




                                if alt25 == 1:
                                    # src/ll/UL4.g:439:6: ',' a2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2130)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2139)
                                    a2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append((None, a2)); 




                                else:
                                    break #loop25


                            # src/ll/UL4.g:442:5: ( ',' an3= name '=' av3= exprarg )*
                            while True: #loop26
                                alt26 = 2
                                LA26_0 = self.input.LA(1)

                                if (LA26_0 == 39) :
                                    LA26_1 = self.input.LA(2)

                                    if (LA26_1 == NAME) :
                                        alt26 = 1




                                if alt26 == 1:
                                    # src/ll/UL4.g:443:6: ',' an3= name '=' av3= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2161)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2170)
                                    an3 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2172)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2176)
                                    av3 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append((((an3 is not None) and [self.input.toString(an3.start,an3.stop)] or [None])[0], av3)); 




                                else:
                                    break #loop26


                            # src/ll/UL4.g:446:5: ( ',' '*' rargs= exprarg )?
                            alt27 = 2
                            LA27_0 = self.input.LA(1)

                            if (LA27_0 == 39) :
                                LA27_1 = self.input.LA(2)

                                if (LA27_1 == 34) :
                                    alt27 = 1
                            if alt27 == 1:
                                # src/ll/UL4.g:447:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2198)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2205)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2209)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.args.append(("*", rargs)); 






                            # src/ll/UL4.g:450:5: ( ',' '**' rkwargs= exprarg )?
                            alt28 = 2
                            LA28_0 = self.input.LA(1)

                            if (LA28_0 == 39) :
                                LA28_1 = self.input.LA(2)

                                if (LA28_1 == 35) :
                                    alt28 = 1
                            if alt28 == 1:
                                # src/ll/UL4.g:451:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2231)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2238)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2242)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.args.append(("**", rkwargs)); 






                            # src/ll/UL4.g:454:5: ( ',' )?
                            alt29 = 2
                            LA29_0 = self.input.LA(1)

                            if (LA29_0 == 39) :
                                alt29 = 1
                            if alt29 == 1:
                                # src/ll/UL4.g:454:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2257)





                        elif alt34 == 5:
                            # src/ll/UL4.g:457:5: an1= name '=' av1= exprarg ( ',' an2= name '=' av2= exprarg )* ( ',' '*' rargs= exprarg )? ( ',' '**' rkwargs= exprarg )? ( ',' )?
                            pass 
                            self._state.following.append(self.FOLLOW_name_in_expr_subscript2277)
                            an1 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2279)

                            self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2283)
                            av1 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                retval.node.args.append((((an1 is not None) and [self.input.toString(an1.start,an1.stop)] or [None])[0], av1)); 



                            # src/ll/UL4.g:458:5: ( ',' an2= name '=' av2= exprarg )*
                            while True: #loop30
                                alt30 = 2
                                LA30_0 = self.input.LA(1)

                                if (LA30_0 == 39) :
                                    LA30_1 = self.input.LA(2)

                                    if (LA30_1 == NAME) :
                                        alt30 = 1




                                if alt30 == 1:
                                    # src/ll/UL4.g:459:6: ',' an2= name '=' av2= exprarg
                                    pass 
                                    self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2298)

                                    self._state.following.append(self.FOLLOW_name_in_expr_subscript2307)
                                    an2 = self.name()

                                    self._state.following.pop()

                                    self.match(self.input, 52, self.FOLLOW_52_in_expr_subscript2309)

                                    self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2313)
                                    av2 = self.exprarg()

                                    self._state.following.pop()

                                    if self._state.backtracking == 0:
                                        pass
                                        retval.node.args.append((((an2 is not None) and [self.input.toString(an2.start,an2.stop)] or [None])[0], av2)); 




                                else:
                                    break #loop30


                            # src/ll/UL4.g:462:5: ( ',' '*' rargs= exprarg )?
                            alt31 = 2
                            LA31_0 = self.input.LA(1)

                            if (LA31_0 == 39) :
                                LA31_1 = self.input.LA(2)

                                if (LA31_1 == 34) :
                                    alt31 = 1
                            if alt31 == 1:
                                # src/ll/UL4.g:463:6: ',' '*' rargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2335)

                                self.match(self.input, 34, self.FOLLOW_34_in_expr_subscript2342)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2346)
                                rargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.args.append(("*", rargs)); 






                            # src/ll/UL4.g:466:5: ( ',' '**' rkwargs= exprarg )?
                            alt32 = 2
                            LA32_0 = self.input.LA(1)

                            if (LA32_0 == 39) :
                                LA32_1 = self.input.LA(2)

                                if (LA32_1 == 35) :
                                    alt32 = 1
                            if alt32 == 1:
                                # src/ll/UL4.g:467:6: ',' '**' rkwargs= exprarg
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2368)

                                self.match(self.input, 35, self.FOLLOW_35_in_expr_subscript2375)

                                self._state.following.append(self.FOLLOW_exprarg_in_expr_subscript2379)
                                rkwargs = self.exprarg()

                                self._state.following.pop()

                                if self._state.backtracking == 0:
                                    pass
                                    retval.node.args.append(("**", rkwargs)); 






                            # src/ll/UL4.g:470:5: ( ',' )?
                            alt33 = 2
                            LA33_0 = self.input.LA(1)

                            if (LA33_0 == 39) :
                                alt33 = 1
                            if alt33 == 1:
                                # src/ll/UL4.g:470:5: ','
                                pass 
                                self.match(self.input, 39, self.FOLLOW_39_in_expr_subscript2394)







                        close = self.match(self.input, 33, self.FOLLOW_33_in_expr_subscript2407)

                        if self._state.backtracking == 0:
                            pass
                            retval.node.end = self.end(close) 




                    elif alt35 == 3:
                        # src/ll/UL4.g:475:4: '[' e2= expr_if close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2423)

                        self._state.following.append(self.FOLLOW_expr_if_in_expr_subscript2431)
                        e2 = self.expr_if()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2438)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Item(self.location, e1.start, self.end(close), retval.node, e2) 




                    elif alt35 == 4:
                        # src/ll/UL4.g:480:4: '[' e2= slice close= ']'
                        pass 
                        self.match(self.input, 58, self.FOLLOW_58_in_expr_subscript2454)

                        self._state.following.append(self.FOLLOW_slice_in_expr_subscript2462)
                        e2 = self.slice()

                        self._state.following.pop()

                        close = self.match(self.input, 59, self.FOLLOW_59_in_expr_subscript2469)

                        if self._state.backtracking == 0:
                            pass
                            retval.node = ul4c.Item(self.location, e1.start, self.end(close), retval.node, e2) 




                    else:
                        break #loop35




                retval.stop = self.input.LT(-1)



                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return retval

    # $ANTLR end "expr_subscript"



    # $ANTLR start "expr_unary"
    # src/ll/UL4.g:487:1: expr_unary returns [node] : (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary );
    def expr_unary(self, ):
        node = None


        minus = None
        bitnot = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:488:2: (e1= expr_subscript |minus= '-' e2= expr_unary |bitnot= '~' e2= expr_unary )
                alt36 = 3
                LA36 = self.input.LA(1)
                if LA36 == COLOR or LA36 == DATE or LA36 == FALSE or LA36 == FLOAT or LA36 == INT or LA36 == NAME or LA36 == NONE or LA36 == STRING or LA36 == STRING3 or LA36 == TRUE or LA36 == 32 or LA36 == 58 or LA36 == 69:
                    alt36 = 1
                elif LA36 == 40:
                    alt36 = 2
                elif LA36 == 73:
                    alt36 = 3
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 36, 0, self.input)

                    raise nvae


                if alt36 == 1:
                    # src/ll/UL4.g:489:3: e1= expr_subscript
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_expr_unary2497)
                    e1 = self.expr_subscript()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ((e1 is not None) and [e1.node] or [None])[0] 




                elif alt36 == 2:
                    # src/ll/UL4.g:491:3: minus= '-' e2= expr_unary
                    pass 
                    minus = self.match(self.input, 40, self.FOLLOW_40_in_expr_unary2508)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2512)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.Neg.make(self.location, self.start(minus), e2.end, e2) 




                elif alt36 == 3:
                    # src/ll/UL4.g:493:3: bitnot= '~' e2= expr_unary
                    pass 
                    bitnot = self.match(self.input, 73, self.FOLLOW_73_in_expr_unary2523)

                    self._state.following.append(self.FOLLOW_expr_unary_in_expr_unary2527)
                    e2 = self.expr_unary()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitNot.make(self.location, self.start(bitnot), e2.end, e2) 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_unary"



    # $ANTLR start "expr_mul"
    # src/ll/UL4.g:498:1: expr_mul returns [node] : e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* ;
    def expr_mul(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:499:2: (e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )* )
                # src/ll/UL4.g:500:3: e1= expr_unary ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                pass 
                self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2551)
                e1 = self.expr_unary()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:501:3: ( ( '*' | '/' | '//' | '%' ) e2= expr_unary )*
                while True: #loop38
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 28 or LA38_0 == 34 or (43 <= LA38_0 <= 44)) :
                        alt38 = 1


                    if alt38 == 1:
                        # src/ll/UL4.g:502:4: ( '*' | '/' | '//' | '%' ) e2= expr_unary
                        pass 
                        # src/ll/UL4.g:502:4: ( '*' | '/' | '//' | '%' )
                        alt37 = 4
                        LA37 = self.input.LA(1)
                        if LA37 == 34:
                            alt37 = 1
                        elif LA37 == 43:
                            alt37 = 2
                        elif LA37 == 44:
                            alt37 = 3
                        elif LA37 == 28:
                            alt37 = 4
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 37, 0, self.input)

                            raise nvae


                        if alt37 == 1:
                            # src/ll/UL4.g:503:5: '*'
                            pass 
                            self.match(self.input, 34, self.FOLLOW_34_in_expr_mul2568)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mul; 




                        elif alt37 == 2:
                            # src/ll/UL4.g:505:5: '/'
                            pass 
                            self.match(self.input, 43, self.FOLLOW_43_in_expr_mul2581)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.TrueDiv; 




                        elif alt37 == 3:
                            # src/ll/UL4.g:507:5: '//'
                            pass 
                            self.match(self.input, 44, self.FOLLOW_44_in_expr_mul2594)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.FloorDiv; 




                        elif alt37 == 4:
                            # src/ll/UL4.g:509:5: '%'
                            pass 
                            self.match(self.input, 28, self.FOLLOW_28_in_expr_mul2607)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Mod; 






                        self._state.following.append(self.FOLLOW_expr_unary_in_expr_mul2621)
                        e2 = self.expr_unary()

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

    # $ANTLR end "expr_mul"



    # $ANTLR start "expr_add"
    # src/ll/UL4.g:516:1: expr_add returns [node] : e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* ;
    def expr_add(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:517:2: (e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )* )
                # src/ll/UL4.g:518:3: e1= expr_mul ( ( '+' | '-' ) e2= expr_mul )*
                pass 
                self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2649)
                e1 = self.expr_mul()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:519:3: ( ( '+' | '-' ) e2= expr_mul )*
                while True: #loop40
                    alt40 = 2
                    LA40_0 = self.input.LA(1)

                    if (LA40_0 == 37 or LA40_0 == 40) :
                        alt40 = 1


                    if alt40 == 1:
                        # src/ll/UL4.g:520:4: ( '+' | '-' ) e2= expr_mul
                        pass 
                        # src/ll/UL4.g:520:4: ( '+' | '-' )
                        alt39 = 2
                        LA39_0 = self.input.LA(1)

                        if (LA39_0 == 37) :
                            alt39 = 1
                        elif (LA39_0 == 40) :
                            alt39 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 39, 0, self.input)

                            raise nvae


                        if alt39 == 1:
                            # src/ll/UL4.g:521:5: '+'
                            pass 
                            self.match(self.input, 37, self.FOLLOW_37_in_expr_add2666)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Add; 




                        elif alt39 == 2:
                            # src/ll/UL4.g:523:5: '-'
                            pass 
                            self.match(self.input, 40, self.FOLLOW_40_in_expr_add2679)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Sub; 






                        self._state.following.append(self.FOLLOW_expr_mul_in_expr_add2693)
                        e2 = self.expr_mul()

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

    # $ANTLR end "expr_add"



    # $ANTLR start "expr_bitshift"
    # src/ll/UL4.g:530:1: expr_bitshift returns [AST node] : e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* ;
    def expr_bitshift(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:531:2: (e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )* )
                # src/ll/UL4.g:532:3: e1= expr_add ( ( '<<' | '>>' ) e2= expr_add )*
                pass 
                self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2721)
                e1 = self.expr_add()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:533:3: ( ( '<<' | '>>' ) e2= expr_add )*
                while True: #loop42
                    alt42 = 2
                    LA42_0 = self.input.LA(1)

                    if (LA42_0 == 49 or LA42_0 == 56) :
                        alt42 = 1


                    if alt42 == 1:
                        # src/ll/UL4.g:534:4: ( '<<' | '>>' ) e2= expr_add
                        pass 
                        # src/ll/UL4.g:534:4: ( '<<' | '>>' )
                        alt41 = 2
                        LA41_0 = self.input.LA(1)

                        if (LA41_0 == 49) :
                            alt41 = 1
                        elif (LA41_0 == 56) :
                            alt41 = 2
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 41, 0, self.input)

                            raise nvae


                        if alt41 == 1:
                            # src/ll/UL4.g:535:5: '<<'
                            pass 
                            self.match(self.input, 49, self.FOLLOW_49_in_expr_bitshift2738)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftLeft; 




                        elif alt41 == 2:
                            # src/ll/UL4.g:537:5: '>>'
                            pass 
                            self.match(self.input, 56, self.FOLLOW_56_in_expr_bitshift2751)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.ShiftRight; 






                        self._state.following.append(self.FOLLOW_expr_add_in_expr_bitshift2765)
                        e2 = self.expr_add()

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

    # $ANTLR end "expr_bitshift"



    # $ANTLR start "expr_bitand"
    # src/ll/UL4.g:544:1: expr_bitand returns [AST node] : e1= expr_bitshift ( '&' e2= expr_bitshift )* ;
    def expr_bitand(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:545:2: (e1= expr_bitshift ( '&' e2= expr_bitshift )* )
                # src/ll/UL4.g:546:3: e1= expr_bitshift ( '&' e2= expr_bitshift )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2793)
                e1 = self.expr_bitshift()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:547:3: ( '&' e2= expr_bitshift )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 30) :
                        alt43 = 1


                    if alt43 == 1:
                        # src/ll/UL4.g:548:4: '&' e2= expr_bitshift
                        pass 
                        self.match(self.input, 30, self.FOLLOW_30_in_expr_bitand2804)

                        self._state.following.append(self.FOLLOW_expr_bitshift_in_expr_bitand2811)
                        e2 = self.expr_bitshift()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitAnd.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop43





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitand"



    # $ANTLR start "expr_bitxor"
    # src/ll/UL4.g:554:1: expr_bitxor returns [AST node] : e1= expr_bitand ( '^' e2= expr_bitand )* ;
    def expr_bitxor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:555:2: (e1= expr_bitand ( '^' e2= expr_bitand )* )
                # src/ll/UL4.g:556:3: e1= expr_bitand ( '^' e2= expr_bitand )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2839)
                e1 = self.expr_bitand()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:557:3: ( '^' e2= expr_bitand )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 60) :
                        alt44 = 1


                    if alt44 == 1:
                        # src/ll/UL4.g:558:4: '^' e2= expr_bitand
                        pass 
                        self.match(self.input, 60, self.FOLLOW_60_in_expr_bitxor2850)

                        self._state.following.append(self.FOLLOW_expr_bitand_in_expr_bitxor2857)
                        e2 = self.expr_bitand()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitXOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop44





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitxor"



    # $ANTLR start "expr_bitor"
    # src/ll/UL4.g:564:1: expr_bitor returns [AST node] : e1= expr_bitxor ( '|' e2= expr_bitxor )* ;
    def expr_bitor(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:565:2: (e1= expr_bitxor ( '|' e2= expr_bitxor )* )
                # src/ll/UL4.g:566:3: e1= expr_bitxor ( '|' e2= expr_bitxor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2885)
                e1 = self.expr_bitxor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:567:3: ( '|' e2= expr_bitxor )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 70) :
                        alt45 = 1


                    if alt45 == 1:
                        # src/ll/UL4.g:568:4: '|' e2= expr_bitxor
                        pass 
                        self.match(self.input, 70, self.FOLLOW_70_in_expr_bitor2896)

                        self._state.following.append(self.FOLLOW_expr_bitxor_in_expr_bitor2903)
                        e2 = self.expr_bitxor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.BitOr.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop45





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_bitor"



    # $ANTLR start "expr_cmp"
    # src/ll/UL4.g:574:1: expr_cmp returns [node] : e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' ) e2= expr_bitor )* ;
    def expr_cmp(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:575:2: (e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' ) e2= expr_bitor )* )
                # src/ll/UL4.g:576:3: e1= expr_bitor ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' ) e2= expr_bitor )*
                pass 
                self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp2931)
                e1 = self.expr_bitor()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:577:3: ( ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' ) e2= expr_bitor )*
                while True: #loop47
                    alt47 = 2
                    LA47_0 = self.input.LA(1)

                    if (LA47_0 == 27 or LA47_0 == 48 or LA47_0 == 51 or (53 <= LA47_0 <= 55) or (66 <= LA47_0 <= 67)) :
                        alt47 = 1


                    if alt47 == 1:
                        # src/ll/UL4.g:578:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' ) e2= expr_bitor
                        pass 
                        # src/ll/UL4.g:578:4: ( '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not' 'in' )
                        alt46 = 8
                        LA46 = self.input.LA(1)
                        if LA46 == 53:
                            alt46 = 1
                        elif LA46 == 27:
                            alt46 = 2
                        elif LA46 == 48:
                            alt46 = 3
                        elif LA46 == 51:
                            alt46 = 4
                        elif LA46 == 54:
                            alt46 = 5
                        elif LA46 == 55:
                            alt46 = 6
                        elif LA46 == 66:
                            alt46 = 7
                        elif LA46 == 67:
                            alt46 = 8
                        else:
                            if self._state.backtracking > 0:
                                raise BacktrackingFailed


                            nvae = NoViableAltException("", 46, 0, self.input)

                            raise nvae


                        if alt46 == 1:
                            # src/ll/UL4.g:579:5: '=='
                            pass 
                            self.match(self.input, 53, self.FOLLOW_53_in_expr_cmp2948)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.EQ; 




                        elif alt46 == 2:
                            # src/ll/UL4.g:581:5: '!='
                            pass 
                            self.match(self.input, 27, self.FOLLOW_27_in_expr_cmp2961)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NE; 




                        elif alt46 == 3:
                            # src/ll/UL4.g:583:5: '<'
                            pass 
                            self.match(self.input, 48, self.FOLLOW_48_in_expr_cmp2974)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LT; 




                        elif alt46 == 4:
                            # src/ll/UL4.g:585:5: '<='
                            pass 
                            self.match(self.input, 51, self.FOLLOW_51_in_expr_cmp2987)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.LE; 




                        elif alt46 == 5:
                            # src/ll/UL4.g:587:5: '>'
                            pass 
                            self.match(self.input, 54, self.FOLLOW_54_in_expr_cmp3000)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GT; 




                        elif alt46 == 6:
                            # src/ll/UL4.g:589:5: '>='
                            pass 
                            self.match(self.input, 55, self.FOLLOW_55_in_expr_cmp3013)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.GE; 




                        elif alt46 == 7:
                            # src/ll/UL4.g:591:5: 'in'
                            pass 
                            self.match(self.input, 66, self.FOLLOW_66_in_expr_cmp3026)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.Contains; 




                        elif alt46 == 8:
                            # src/ll/UL4.g:593:5: 'not' 'in'
                            pass 
                            self.match(self.input, 67, self.FOLLOW_67_in_expr_cmp3039)

                            self.match(self.input, 66, self.FOLLOW_66_in_expr_cmp3041)

                            if self._state.backtracking == 0:
                                pass
                                cls = ul4c.NotContains; 






                        self._state.following.append(self.FOLLOW_expr_bitor_in_expr_cmp3055)
                        e2 = self.expr_bitor()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = cls.make(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop47





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_cmp"



    # $ANTLR start "expr_not"
    # src/ll/UL4.g:600:1: expr_not returns [node] : (e1= expr_cmp |n= 'not' e2= expr_not );
    def expr_not(self, ):
        node = None


        n = None
        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:601:2: (e1= expr_cmp |n= 'not' e2= expr_not )
                alt48 = 2
                LA48_0 = self.input.LA(1)

                if ((COLOR <= LA48_0 <= DATE) or (FALSE <= LA48_0 <= FLOAT) or (INT <= LA48_0 <= NONE) or (STRING <= LA48_0 <= STRING3) or LA48_0 == TRUE or LA48_0 == 32 or LA48_0 == 40 or LA48_0 == 58 or LA48_0 == 69 or LA48_0 == 73) :
                    alt48 = 1
                elif (LA48_0 == 67) :
                    alt48 = 2
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 48, 0, self.input)

                    raise nvae


                if alt48 == 1:
                    # src/ll/UL4.g:602:3: e1= expr_cmp
                    pass 
                    self._state.following.append(self.FOLLOW_expr_cmp_in_expr_not3083)
                    e1 = self.expr_cmp()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  e1 




                elif alt48 == 2:
                    # src/ll/UL4.g:604:3: n= 'not' e2= expr_not
                    pass 
                    n = self.match(self.input, 67, self.FOLLOW_67_in_expr_not3094)

                    self._state.following.append(self.FOLLOW_expr_not_in_expr_not3098)
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
    # src/ll/UL4.g:609:1: expr_and returns [node] : e1= expr_not ( 'and' e2= expr_not )* ;
    def expr_and(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:610:2: (e1= expr_not ( 'and' e2= expr_not )* )
                # src/ll/UL4.g:611:3: e1= expr_not ( 'and' e2= expr_not )*
                pass 
                self._state.following.append(self.FOLLOW_expr_not_in_expr_and3122)
                e1 = self.expr_not()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:612:3: ( 'and' e2= expr_not )*
                while True: #loop49
                    alt49 = 2
                    LA49_0 = self.input.LA(1)

                    if (LA49_0 == 62) :
                        alt49 = 1


                    if alt49 == 1:
                        # src/ll/UL4.g:613:4: 'and' e2= expr_not
                        pass 
                        self.match(self.input, 62, self.FOLLOW_62_in_expr_and3133)

                        self._state.following.append(self.FOLLOW_expr_not_in_expr_and3140)
                        e2 = self.expr_not()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.And(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop49





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_and"



    # $ANTLR start "expr_or"
    # src/ll/UL4.g:619:1: expr_or returns [node] : e1= expr_and ( 'or' e2= expr_and )* ;
    def expr_or(self, ):
        node = None


        e1 = None
        e2 = None

        try:
            try:
                # src/ll/UL4.g:620:2: (e1= expr_and ( 'or' e2= expr_and )* )
                # src/ll/UL4.g:621:3: e1= expr_and ( 'or' e2= expr_and )*
                pass 
                self._state.following.append(self.FOLLOW_expr_and_in_expr_or3168)
                e1 = self.expr_and()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:622:3: ( 'or' e2= expr_and )*
                while True: #loop50
                    alt50 = 2
                    LA50_0 = self.input.LA(1)

                    if (LA50_0 == 68) :
                        alt50 = 1


                    if alt50 == 1:
                        # src/ll/UL4.g:623:4: 'or' e2= expr_and
                        pass 
                        self.match(self.input, 68, self.FOLLOW_68_in_expr_or3179)

                        self._state.following.append(self.FOLLOW_expr_and_in_expr_or3186)
                        e2 = self.expr_and()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node = ul4c.Or(self.location, node.start, e2.end, node, e2) 




                    else:
                        break #loop50





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "expr_or"



    # $ANTLR start "expr_if"
    # src/ll/UL4.g:629:1: expr_if returns [node] : e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? ;
    def expr_if(self, ):
        node = None


        e1 = None
        e2 = None
        e3 = None

        try:
            try:
                # src/ll/UL4.g:630:2: (e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )? )
                # src/ll/UL4.g:631:3: e1= expr_or ( 'if' e2= expr_or 'else' e3= expr_or )?
                pass 
                self._state.following.append(self.FOLLOW_expr_or_in_expr_if3214)
                e1 = self.expr_or()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  e1 



                # src/ll/UL4.g:632:3: ( 'if' e2= expr_or 'else' e3= expr_or )?
                alt51 = 2
                LA51_0 = self.input.LA(1)

                if (LA51_0 == 65) :
                    LA51_1 = self.input.LA(2)

                    if (self.synpred81_UL4()) :
                        alt51 = 1
                if alt51 == 1:
                    # src/ll/UL4.g:633:4: 'if' e2= expr_or 'else' e3= expr_or
                    pass 
                    self.match(self.input, 65, self.FOLLOW_65_in_expr_if3225)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3232)
                    e2 = self.expr_or()

                    self._state.following.pop()

                    self.match(self.input, 63, self.FOLLOW_63_in_expr_if3237)

                    self._state.following.append(self.FOLLOW_expr_or_in_expr_if3244)
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
    # src/ll/UL4.g:640:1: exprarg returns [node] : (ege= generatorexpression |e1= expr_if );
    def exprarg(self, ):
        node = None


        ege = None
        e1 = None

        try:
            try:
                # src/ll/UL4.g:641:2: (ege= generatorexpression |e1= expr_if )
                alt52 = 2
                LA52 = self.input.LA(1)
                if LA52 == NONE:
                    LA52_1 = self.input.LA(2)

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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

                    if (self.synpred82_UL4()) :
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
                    # src/ll/UL4.g:641:4: ege= generatorexpression
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_exprarg3268)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt52 == 2:
                    # src/ll/UL4.g:642:4: e1= expr_if
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_exprarg3277)
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
    # src/ll/UL4.g:645:1: expression returns [node] : (ege= generatorexpression EOF |e= expr_if EOF );
    def expression(self, ):
        node = None


        ege = None
        e = None

        try:
            try:
                # src/ll/UL4.g:646:2: (ege= generatorexpression EOF |e= expr_if EOF )
                alt53 = 2
                LA53 = self.input.LA(1)
                if LA53 == NONE:
                    LA53_1 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 1, self.input)

                        raise nvae


                elif LA53 == FALSE:
                    LA53_2 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 2, self.input)

                        raise nvae


                elif LA53 == TRUE:
                    LA53_3 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 3, self.input)

                        raise nvae


                elif LA53 == INT:
                    LA53_4 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 4, self.input)

                        raise nvae


                elif LA53 == FLOAT:
                    LA53_5 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 5, self.input)

                        raise nvae


                elif LA53 == STRING:
                    LA53_6 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 6, self.input)

                        raise nvae


                elif LA53 == STRING3:
                    LA53_7 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 7, self.input)

                        raise nvae


                elif LA53 == DATE:
                    LA53_8 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 8, self.input)

                        raise nvae


                elif LA53 == COLOR:
                    LA53_9 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 9, self.input)

                        raise nvae


                elif LA53 == NAME:
                    LA53_10 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 10, self.input)

                        raise nvae


                elif LA53 == 58:
                    LA53_11 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 11, self.input)

                        raise nvae


                elif LA53 == 69:
                    LA53_12 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 12, self.input)

                        raise nvae


                elif LA53 == 32:
                    LA53_13 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 13, self.input)

                        raise nvae


                elif LA53 == 40:
                    LA53_14 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 14, self.input)

                        raise nvae


                elif LA53 == 73:
                    LA53_15 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 15, self.input)

                        raise nvae


                elif LA53 == 67:
                    LA53_16 = self.input.LA(2)

                    if (self.synpred83_UL4()) :
                        alt53 = 1
                    elif (True) :
                        alt53 = 2
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 53, 16, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 53, 0, self.input)

                    raise nvae


                if alt53 == 1:
                    # src/ll/UL4.g:646:4: ege= generatorexpression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_generatorexpression_in_expression3296)
                    ege = self.generatorexpression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3298)

                    if self._state.backtracking == 0:
                        pass
                        node =  ege 




                elif alt53 == 2:
                    # src/ll/UL4.g:647:4: e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_if_in_expression3307)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_expression3309)

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
    # src/ll/UL4.g:653:1: for_ returns [node] : n= nestedlvalue 'in' e= expr_if EOF ;
    def for_(self, ):
        node = None


        n = None
        e = None

        try:
            try:
                # src/ll/UL4.g:654:2: (n= nestedlvalue 'in' e= expr_if EOF )
                # src/ll/UL4.g:655:3: n= nestedlvalue 'in' e= expr_if EOF
                pass 
                self._state.following.append(self.FOLLOW_nestedlvalue_in_for_3334)
                n = self.nestedlvalue()

                self._state.following.pop()

                self.match(self.input, 66, self.FOLLOW_66_in_for_3338)

                self._state.following.append(self.FOLLOW_expr_if_in_for_3344)
                e = self.expr_if()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.ForBlock(self.location, self.start(n.start), e.end, ((n is not None) and [n.lvalue] or [None])[0], e) 



                self.match(self.input, EOF, self.FOLLOW_EOF_in_for_3350)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "for_"



    # $ANTLR start "statement"
    # src/ll/UL4.g:664:1: statement returns [node] : (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF );
    def statement(self, ):
        node = None


        nn = None
        e = None
        n = None

        try:
            try:
                # src/ll/UL4.g:665:2: (nn= nestedlvalue '=' e= expr_if EOF |n= expr_subscript '+=' e= expr_if EOF |n= expr_subscript '-=' e= expr_if EOF |n= expr_subscript '*=' e= expr_if EOF |n= expr_subscript '/=' e= expr_if EOF |n= expr_subscript '//=' e= expr_if EOF |n= expr_subscript '%=' e= expr_if EOF |n= expr_subscript '<<=' e= expr_if EOF |n= expr_subscript '>>=' e= expr_if EOF |n= expr_subscript '&=' e= expr_if EOF |n= expr_subscript '^=' e= expr_if EOF |n= expr_subscript '|=' e= expr_if EOF |e= expression EOF )
                alt54 = 13
                LA54 = self.input.LA(1)
                if LA54 == NONE:
                    LA54_1 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 1, self.input)

                        raise nvae


                elif LA54 == FALSE:
                    LA54_2 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 2, self.input)

                        raise nvae


                elif LA54 == TRUE:
                    LA54_3 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 3, self.input)

                        raise nvae


                elif LA54 == INT:
                    LA54_4 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 4, self.input)

                        raise nvae


                elif LA54 == FLOAT:
                    LA54_5 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 5, self.input)

                        raise nvae


                elif LA54 == STRING:
                    LA54_6 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 6, self.input)

                        raise nvae


                elif LA54 == STRING3:
                    LA54_7 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 7, self.input)

                        raise nvae


                elif LA54 == DATE:
                    LA54_8 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 8, self.input)

                        raise nvae


                elif LA54 == COLOR:
                    LA54_9 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 9, self.input)

                        raise nvae


                elif LA54 == NAME:
                    LA54_10 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 10, self.input)

                        raise nvae


                elif LA54 == 58:
                    LA54_11 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 11, self.input)

                        raise nvae


                elif LA54 == 69:
                    LA54_12 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 12, self.input)

                        raise nvae


                elif LA54 == 32:
                    LA54_13 = self.input.LA(2)

                    if (self.synpred84_UL4()) :
                        alt54 = 1
                    elif (self.synpred85_UL4()) :
                        alt54 = 2
                    elif (self.synpred86_UL4()) :
                        alt54 = 3
                    elif (self.synpred87_UL4()) :
                        alt54 = 4
                    elif (self.synpred88_UL4()) :
                        alt54 = 5
                    elif (self.synpred89_UL4()) :
                        alt54 = 6
                    elif (self.synpred90_UL4()) :
                        alt54 = 7
                    elif (self.synpred91_UL4()) :
                        alt54 = 8
                    elif (self.synpred92_UL4()) :
                        alt54 = 9
                    elif (self.synpred93_UL4()) :
                        alt54 = 10
                    elif (self.synpred94_UL4()) :
                        alt54 = 11
                    elif (self.synpred95_UL4()) :
                        alt54 = 12
                    elif (True) :
                        alt54 = 13
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 54, 13, self.input)

                        raise nvae


                elif LA54 == 40 or LA54 == 67 or LA54 == 73:
                    alt54 = 13
                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 54, 0, self.input)

                    raise nvae


                if alt54 == 1:
                    # src/ll/UL4.g:665:4: nn= nestedlvalue '=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_nestedlvalue_in_statement3371)
                    nn = self.nestedlvalue()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_statement3373)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3377)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3379)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SetVar(self.location, self.start(nn.start), e.end, ((nn is not None) and [nn.lvalue] or [None])[0], e) 




                elif alt54 == 2:
                    # src/ll/UL4.g:666:4: n= expr_subscript '+=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3388)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 38, self.FOLLOW_38_in_statement3390)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3394)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3396)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.AddVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 3:
                    # src/ll/UL4.g:667:4: n= expr_subscript '-=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3405)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 41, self.FOLLOW_41_in_statement3407)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3411)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3413)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.SubVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 4:
                    # src/ll/UL4.g:668:4: n= expr_subscript '*=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3422)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 36, self.FOLLOW_36_in_statement3424)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3428)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3430)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.MulVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 5:
                    # src/ll/UL4.g:669:4: n= expr_subscript '/=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3439)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 46, self.FOLLOW_46_in_statement3441)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3445)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3447)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.TrueDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 6:
                    # src/ll/UL4.g:670:4: n= expr_subscript '//=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3456)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 45, self.FOLLOW_45_in_statement3458)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3462)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3464)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.FloorDivVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 7:
                    # src/ll/UL4.g:671:4: n= expr_subscript '%=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3473)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 29, self.FOLLOW_29_in_statement3475)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3479)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3481)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ModVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 8:
                    # src/ll/UL4.g:672:4: n= expr_subscript '<<=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3490)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 50, self.FOLLOW_50_in_statement3492)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3496)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3498)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftLeftVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 9:
                    # src/ll/UL4.g:673:4: n= expr_subscript '>>=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3507)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 57, self.FOLLOW_57_in_statement3509)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3513)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3515)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.ShiftRightVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 10:
                    # src/ll/UL4.g:674:4: n= expr_subscript '&=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3524)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 31, self.FOLLOW_31_in_statement3526)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3530)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3532)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitAndVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 11:
                    # src/ll/UL4.g:675:4: n= expr_subscript '^=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3541)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 61, self.FOLLOW_61_in_statement3543)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3547)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3549)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitXOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 12:
                    # src/ll/UL4.g:676:4: n= expr_subscript '|=' e= expr_if EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expr_subscript_in_statement3558)
                    n = self.expr_subscript()

                    self._state.following.pop()

                    self.match(self.input, 71, self.FOLLOW_71_in_statement3560)

                    self._state.following.append(self.FOLLOW_expr_if_in_statement3564)
                    e = self.expr_if()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3566)

                    if self._state.backtracking == 0:
                        pass
                        node = ul4c.BitOrVar(self.location, self.start(n.start), e.end, ((n is not None) and [n.node] or [None])[0], e) 




                elif alt54 == 13:
                    # src/ll/UL4.g:677:4: e= expression EOF
                    pass 
                    self._state.following.append(self.FOLLOW_expression_in_statement3575)
                    e = self.expression()

                    self._state.following.pop()

                    self.match(self.input, EOF, self.FOLLOW_EOF_in_statement3577)

                    if self._state.backtracking == 0:
                        pass
                        node = e 





                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "statement"



    # $ANTLR start "signature"
    # src/ll/UL4.g:682:1: signature returns [node] : open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' ;
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
                # src/ll/UL4.g:683:2: (open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')' )
                # src/ll/UL4.g:684:2: open= '(' (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? ) close= ')'
                pass 
                open = self.match(self.input, 32, self.FOLLOW_32_in_signature3600)

                if self._state.backtracking == 0:
                    pass
                    node = ul4c.Signature(self.location, self.start(open), None) 



                # src/ll/UL4.g:685:2: (| '**' rkwargsname= name ( ',' )? | '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? |aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )? )
                alt67 = 5
                LA67 = self.input.LA(1)
                if LA67 == 33:
                    alt67 = 1
                elif LA67 == 35:
                    alt67 = 2
                elif LA67 == 34:
                    alt67 = 3
                elif LA67 == NAME:
                    LA67_4 = self.input.LA(2)

                    if (LA67_4 == 52) :
                        alt67 = 4
                    elif (LA67_4 == 33 or LA67_4 == 39) :
                        alt67 = 5
                    else:
                        if self._state.backtracking > 0:
                            raise BacktrackingFailed


                        nvae = NoViableAltException("", 67, 4, self.input)

                        raise nvae


                else:
                    if self._state.backtracking > 0:
                        raise BacktrackingFailed


                    nvae = NoViableAltException("", 67, 0, self.input)

                    raise nvae


                if alt67 == 1:
                    # src/ll/UL4.g:687:2: 
                    pass 

                elif alt67 == 2:
                    # src/ll/UL4.g:689:3: '**' rkwargsname= name ( ',' )?
                    pass 
                    self.match(self.input, 35, self.FOLLOW_35_in_signature3620)

                    self._state.following.append(self.FOLLOW_name_in_signature3624)
                    rkwargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:690:3: ( ',' )?
                    alt55 = 2
                    LA55_0 = self.input.LA(1)

                    if (LA55_0 == 39) :
                        alt55 = 1
                    if alt55 == 1:
                        # src/ll/UL4.g:690:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3630)





                elif alt67 == 3:
                    # src/ll/UL4.g:693:3: '*' rargsname= name ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self.match(self.input, 34, self.FOLLOW_34_in_signature3642)

                    self._state.following.append(self.FOLLOW_name_in_signature3646)
                    rargsname = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:694:3: ( ',' '**' rkwargsname= name )?
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 39) :
                        LA56_1 = self.input.LA(2)

                        if (LA56_1 == 35) :
                            alt56 = 1
                    if alt56 == 1:
                        # src/ll/UL4.g:695:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3657)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3662)

                        self._state.following.append(self.FOLLOW_name_in_signature3666)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:698:3: ( ',' )?
                    alt57 = 2
                    LA57_0 = self.input.LA(1)

                    if (LA57_0 == 39) :
                        alt57 = 1
                    if alt57 == 1:
                        # src/ll/UL4.g:698:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3677)





                elif alt67 == 4:
                    # src/ll/UL4.g:701:3: aname1= name '=' adefault1= exprarg ( ',' aname2= name '=' adefault2= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3691)
                    aname1 = self.name()

                    self._state.following.pop()

                    self.match(self.input, 52, self.FOLLOW_52_in_signature3695)

                    self._state.following.append(self.FOLLOW_exprarg_in_signature3701)
                    adefault1 = self.exprarg()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], adefault1)); 



                    # src/ll/UL4.g:704:3: ( ',' aname2= name '=' adefault2= exprarg )*
                    while True: #loop58
                        alt58 = 2
                        LA58_0 = self.input.LA(1)

                        if (LA58_0 == 39) :
                            LA58_1 = self.input.LA(2)

                            if (LA58_1 == NAME) :
                                alt58 = 1




                        if alt58 == 1:
                            # src/ll/UL4.g:705:4: ',' aname2= name '=' adefault2= exprarg
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3712)

                            self._state.following.append(self.FOLLOW_name_in_signature3719)
                            aname2 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_signature3724)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3731)
                            adefault2 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], adefault2)); 




                        else:
                            break #loop58


                    # src/ll/UL4.g:710:3: ( ',' '*' rargsname= name )?
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if (LA59_0 == 39) :
                        LA59_1 = self.input.LA(2)

                        if (LA59_1 == 34) :
                            alt59 = 1
                    if alt59 == 1:
                        # src/ll/UL4.g:711:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3747)

                        self.match(self.input, 34, self.FOLLOW_34_in_signature3752)

                        self._state.following.append(self.FOLLOW_name_in_signature3756)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:714:3: ( ',' '**' rkwargsname= name )?
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == 39) :
                        LA60_1 = self.input.LA(2)

                        if (LA60_1 == 35) :
                            alt60 = 1
                    if alt60 == 1:
                        # src/ll/UL4.g:715:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3772)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3777)

                        self._state.following.append(self.FOLLOW_name_in_signature3781)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:718:3: ( ',' )?
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if (LA61_0 == 39) :
                        alt61 = 1
                    if alt61 == 1:
                        # src/ll/UL4.g:718:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3792)





                elif alt67 == 5:
                    # src/ll/UL4.g:721:3: aname1= name ( ',' aname2= name )* ( ',' aname3= name '=' adefault3= exprarg )* ( ',' '*' rargsname= name )? ( ',' '**' rkwargsname= name )? ( ',' )?
                    pass 
                    self._state.following.append(self.FOLLOW_name_in_signature3806)
                    aname1 = self.name()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node.params.append((((aname1 is not None) and [self.input.toString(aname1.start,aname1.stop)] or [None])[0], None)); 



                    # src/ll/UL4.g:722:3: ( ',' aname2= name )*
                    while True: #loop62
                        alt62 = 2
                        LA62_0 = self.input.LA(1)

                        if (LA62_0 == 39) :
                            LA62_1 = self.input.LA(2)

                            if (LA62_1 == NAME) :
                                LA62_3 = self.input.LA(3)

                                if (LA62_3 == 33 or LA62_3 == 39) :
                                    alt62 = 1






                        if alt62 == 1:
                            # src/ll/UL4.g:723:4: ',' aname2= name
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3817)

                            self._state.following.append(self.FOLLOW_name_in_signature3824)
                            aname2 = self.name()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname2 is not None) and [self.input.toString(aname2.start,aname2.stop)] or [None])[0], None)); 




                        else:
                            break #loop62


                    # src/ll/UL4.g:726:3: ( ',' aname3= name '=' adefault3= exprarg )*
                    while True: #loop63
                        alt63 = 2
                        LA63_0 = self.input.LA(1)

                        if (LA63_0 == 39) :
                            LA63_1 = self.input.LA(2)

                            if (LA63_1 == NAME) :
                                alt63 = 1




                        if alt63 == 1:
                            # src/ll/UL4.g:727:4: ',' aname3= name '=' adefault3= exprarg
                            pass 
                            self.match(self.input, 39, self.FOLLOW_39_in_signature3840)

                            self._state.following.append(self.FOLLOW_name_in_signature3847)
                            aname3 = self.name()

                            self._state.following.pop()

                            self.match(self.input, 52, self.FOLLOW_52_in_signature3852)

                            self._state.following.append(self.FOLLOW_exprarg_in_signature3859)
                            adefault3 = self.exprarg()

                            self._state.following.pop()

                            if self._state.backtracking == 0:
                                pass
                                node.params.append((((aname3 is not None) and [self.input.toString(aname3.start,aname3.stop)] or [None])[0], adefault3)); 




                        else:
                            break #loop63


                    # src/ll/UL4.g:732:3: ( ',' '*' rargsname= name )?
                    alt64 = 2
                    LA64_0 = self.input.LA(1)

                    if (LA64_0 == 39) :
                        LA64_1 = self.input.LA(2)

                        if (LA64_1 == 34) :
                            alt64 = 1
                    if alt64 == 1:
                        # src/ll/UL4.g:733:4: ',' '*' rargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3875)

                        self.match(self.input, 34, self.FOLLOW_34_in_signature3880)

                        self._state.following.append(self.FOLLOW_name_in_signature3884)
                        rargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("*" + ((rargsname is not None) and [self.input.toString(rargsname.start,rargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:736:3: ( ',' '**' rkwargsname= name )?
                    alt65 = 2
                    LA65_0 = self.input.LA(1)

                    if (LA65_0 == 39) :
                        LA65_1 = self.input.LA(2)

                        if (LA65_1 == 35) :
                            alt65 = 1
                    if alt65 == 1:
                        # src/ll/UL4.g:737:4: ',' '**' rkwargsname= name
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3900)

                        self.match(self.input, 35, self.FOLLOW_35_in_signature3905)

                        self._state.following.append(self.FOLLOW_name_in_signature3909)
                        rkwargsname = self.name()

                        self._state.following.pop()

                        if self._state.backtracking == 0:
                            pass
                            node.params.append(("**" + ((rkwargsname is not None) and [self.input.toString(rkwargsname.start,rkwargsname.stop)] or [None])[0], None)); 






                    # src/ll/UL4.g:740:3: ( ',' )?
                    alt66 = 2
                    LA66_0 = self.input.LA(1)

                    if (LA66_0 == 39) :
                        alt66 = 1
                    if alt66 == 1:
                        # src/ll/UL4.g:740:3: ','
                        pass 
                        self.match(self.input, 39, self.FOLLOW_39_in_signature3920)







                close = self.match(self.input, 33, self.FOLLOW_33_in_signature3929)

                if self._state.backtracking == 0:
                    pass
                    node.end = self.end(close) 






                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "signature"



    # $ANTLR start "definition"
    # src/ll/UL4.g:748:1: definition returns [node] : n= name (sig= signature )? EOF ;
    def definition(self, ):
        node = None


        n = None
        sig = None

        try:
            try:
                # src/ll/UL4.g:749:2: (n= name (sig= signature )? EOF )
                # src/ll/UL4.g:750:3: n= name (sig= signature )? EOF
                pass 
                self._state.following.append(self.FOLLOW_name_in_definition3953)
                n = self.name()

                self._state.following.pop()

                if self._state.backtracking == 0:
                    pass
                    node =  (((n is not None) and [self.input.toString(n.start,n.stop)] or [None])[0], None) 



                # src/ll/UL4.g:751:3: (sig= signature )?
                alt68 = 2
                LA68_0 = self.input.LA(1)

                if (LA68_0 == 32) :
                    alt68 = 1
                if alt68 == 1:
                    # src/ll/UL4.g:752:4: sig= signature
                    pass 
                    self._state.following.append(self.FOLLOW_signature_in_definition3966)
                    sig = self.signature()

                    self._state.following.pop()

                    if self._state.backtracking == 0:
                        pass
                        node =  (node[0], sig) 






                self.match(self.input, EOF, self.FOLLOW_EOF_in_definition3977)




                       
            except RecognitionException as e:
                raise

        finally:
            pass
        return node

    # $ANTLR end "definition"

    # $ANTLR start "synpred24_UL4"
    def synpred24_UL4_fragment(self, ):
        e_list = None

        # src/ll/UL4.g:350:4: (e_list= list )
        # src/ll/UL4.g:350:4: e_list= list
        pass 
        self._state.following.append(self.FOLLOW_list_in_synpred24_UL41684)
        e_list = self.list()

        self._state.following.pop()



    # $ANTLR end "synpred24_UL4"



    # $ANTLR start "synpred25_UL4"
    def synpred25_UL4_fragment(self, ):
        e_listcomp = None

        # src/ll/UL4.g:351:4: (e_listcomp= listcomprehension )
        # src/ll/UL4.g:351:4: e_listcomp= listcomprehension
        pass 
        self._state.following.append(self.FOLLOW_listcomprehension_in_synpred25_UL41693)
        e_listcomp = self.listcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred25_UL4"



    # $ANTLR start "synpred26_UL4"
    def synpred26_UL4_fragment(self, ):
        e_set = None

        # src/ll/UL4.g:352:4: (e_set= set )
        # src/ll/UL4.g:352:4: e_set= set
        pass 
        self._state.following.append(self.FOLLOW_set_in_synpred26_UL41702)
        e_set = self.set()

        self._state.following.pop()



    # $ANTLR end "synpred26_UL4"



    # $ANTLR start "synpred27_UL4"
    def synpred27_UL4_fragment(self, ):
        e_setcomp = None

        # src/ll/UL4.g:353:4: (e_setcomp= setcomprehension )
        # src/ll/UL4.g:353:4: e_setcomp= setcomprehension
        pass 
        self._state.following.append(self.FOLLOW_setcomprehension_in_synpred27_UL41711)
        e_setcomp = self.setcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred27_UL4"



    # $ANTLR start "synpred28_UL4"
    def synpred28_UL4_fragment(self, ):
        e_dict = None

        # src/ll/UL4.g:354:4: (e_dict= dict )
        # src/ll/UL4.g:354:4: e_dict= dict
        pass 
        self._state.following.append(self.FOLLOW_dict_in_synpred28_UL41720)
        e_dict = self.dict()

        self._state.following.pop()



    # $ANTLR end "synpred28_UL4"



    # $ANTLR start "synpred29_UL4"
    def synpred29_UL4_fragment(self, ):
        e_dictcomp = None

        # src/ll/UL4.g:355:4: (e_dictcomp= dictcomprehension )
        # src/ll/UL4.g:355:4: e_dictcomp= dictcomprehension
        pass 
        self._state.following.append(self.FOLLOW_dictcomprehension_in_synpred29_UL41729)
        e_dictcomp = self.dictcomprehension()

        self._state.following.pop()



    # $ANTLR end "synpred29_UL4"



    # $ANTLR start "synpred30_UL4"
    def synpred30_UL4_fragment(self, ):
        open = None
        close = None
        e_genexpr = None

        # src/ll/UL4.g:356:4: (open= '(' e_genexpr= generatorexpression close= ')' )
        # src/ll/UL4.g:356:4: open= '(' e_genexpr= generatorexpression close= ')'
        pass 
        open = self.match(self.input, 32, self.FOLLOW_32_in_synpred30_UL41738)

        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred30_UL41742)
        e_genexpr = self.generatorexpression()

        self._state.following.pop()

        close = self.match(self.input, 33, self.FOLLOW_33_in_synpred30_UL41746)



    # $ANTLR end "synpred30_UL4"



    # $ANTLR start "synpred31_UL4"
    def synpred31_UL4_fragment(self, ):
        n = None

        # src/ll/UL4.g:371:3: (n= expr_subscript )
        # src/ll/UL4.g:371:3: n= expr_subscript
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred31_UL41786)
        n = self.expr_subscript()

        self._state.following.pop()



    # $ANTLR end "synpred31_UL4"



    # $ANTLR start "synpred32_UL4"
    def synpred32_UL4_fragment(self, ):
        n0 = None

        # src/ll/UL4.g:373:3: ( '(' n0= nestedlvalue ',' ')' )
        # src/ll/UL4.g:373:3: '(' n0= nestedlvalue ',' ')'
        pass 
        self.match(self.input, 32, self.FOLLOW_32_in_synpred32_UL41795)

        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred32_UL41799)
        n0 = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 39, self.FOLLOW_39_in_synpred32_UL41801)

        self.match(self.input, 33, self.FOLLOW_33_in_synpred32_UL41803)



    # $ANTLR end "synpred32_UL4"



    # $ANTLR start "synpred55_UL4"
    def synpred55_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:475:4: ( '[' e2= expr_if close= ']' )
        # src/ll/UL4.g:475:4: '[' e2= expr_if close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred55_UL42423)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred55_UL42431)
        e2 = self.expr_if()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred55_UL42438)



    # $ANTLR end "synpred55_UL4"



    # $ANTLR start "synpred56_UL4"
    def synpred56_UL4_fragment(self, ):
        close = None
        e2 = None

        # src/ll/UL4.g:480:4: ( '[' e2= slice close= ']' )
        # src/ll/UL4.g:480:4: '[' e2= slice close= ']'
        pass 
        self.match(self.input, 58, self.FOLLOW_58_in_synpred56_UL42454)

        self._state.following.append(self.FOLLOW_slice_in_synpred56_UL42462)
        e2 = self.slice()

        self._state.following.pop()

        close = self.match(self.input, 59, self.FOLLOW_59_in_synpred56_UL42469)



    # $ANTLR end "synpred56_UL4"



    # $ANTLR start "synpred81_UL4"
    def synpred81_UL4_fragment(self, ):
        e2 = None
        e3 = None

        # src/ll/UL4.g:633:4: ( 'if' e2= expr_or 'else' e3= expr_or )
        # src/ll/UL4.g:633:4: 'if' e2= expr_or 'else' e3= expr_or
        pass 
        self.match(self.input, 65, self.FOLLOW_65_in_synpred81_UL43225)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred81_UL43232)
        e2 = self.expr_or()

        self._state.following.pop()

        self.match(self.input, 63, self.FOLLOW_63_in_synpred81_UL43237)

        self._state.following.append(self.FOLLOW_expr_or_in_synpred81_UL43244)
        e3 = self.expr_or()

        self._state.following.pop()



    # $ANTLR end "synpred81_UL4"



    # $ANTLR start "synpred82_UL4"
    def synpred82_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:641:4: (ege= generatorexpression )
        # src/ll/UL4.g:641:4: ege= generatorexpression
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred82_UL43268)
        ege = self.generatorexpression()

        self._state.following.pop()



    # $ANTLR end "synpred82_UL4"



    # $ANTLR start "synpred83_UL4"
    def synpred83_UL4_fragment(self, ):
        ege = None

        # src/ll/UL4.g:646:4: (ege= generatorexpression EOF )
        # src/ll/UL4.g:646:4: ege= generatorexpression EOF
        pass 
        self._state.following.append(self.FOLLOW_generatorexpression_in_synpred83_UL43296)
        ege = self.generatorexpression()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred83_UL43298)



    # $ANTLR end "synpred83_UL4"



    # $ANTLR start "synpred84_UL4"
    def synpred84_UL4_fragment(self, ):
        nn = None
        e = None

        # src/ll/UL4.g:665:4: (nn= nestedlvalue '=' e= expr_if EOF )
        # src/ll/UL4.g:665:4: nn= nestedlvalue '=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_nestedlvalue_in_synpred84_UL43371)
        nn = self.nestedlvalue()

        self._state.following.pop()

        self.match(self.input, 52, self.FOLLOW_52_in_synpred84_UL43373)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred84_UL43377)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred84_UL43379)



    # $ANTLR end "synpred84_UL4"



    # $ANTLR start "synpred85_UL4"
    def synpred85_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:666:4: (n= expr_subscript '+=' e= expr_if EOF )
        # src/ll/UL4.g:666:4: n= expr_subscript '+=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred85_UL43388)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 38, self.FOLLOW_38_in_synpred85_UL43390)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred85_UL43394)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred85_UL43396)



    # $ANTLR end "synpred85_UL4"



    # $ANTLR start "synpred86_UL4"
    def synpred86_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:667:4: (n= expr_subscript '-=' e= expr_if EOF )
        # src/ll/UL4.g:667:4: n= expr_subscript '-=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred86_UL43405)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 41, self.FOLLOW_41_in_synpred86_UL43407)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred86_UL43411)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred86_UL43413)



    # $ANTLR end "synpred86_UL4"



    # $ANTLR start "synpred87_UL4"
    def synpred87_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:668:4: (n= expr_subscript '*=' e= expr_if EOF )
        # src/ll/UL4.g:668:4: n= expr_subscript '*=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred87_UL43422)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 36, self.FOLLOW_36_in_synpred87_UL43424)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred87_UL43428)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred87_UL43430)



    # $ANTLR end "synpred87_UL4"



    # $ANTLR start "synpred88_UL4"
    def synpred88_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:669:4: (n= expr_subscript '/=' e= expr_if EOF )
        # src/ll/UL4.g:669:4: n= expr_subscript '/=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred88_UL43439)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 46, self.FOLLOW_46_in_synpred88_UL43441)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred88_UL43445)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred88_UL43447)



    # $ANTLR end "synpred88_UL4"



    # $ANTLR start "synpred89_UL4"
    def synpred89_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:670:4: (n= expr_subscript '//=' e= expr_if EOF )
        # src/ll/UL4.g:670:4: n= expr_subscript '//=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred89_UL43456)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 45, self.FOLLOW_45_in_synpred89_UL43458)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred89_UL43462)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred89_UL43464)



    # $ANTLR end "synpred89_UL4"



    # $ANTLR start "synpred90_UL4"
    def synpred90_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:671:4: (n= expr_subscript '%=' e= expr_if EOF )
        # src/ll/UL4.g:671:4: n= expr_subscript '%=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred90_UL43473)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 29, self.FOLLOW_29_in_synpred90_UL43475)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred90_UL43479)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred90_UL43481)



    # $ANTLR end "synpred90_UL4"



    # $ANTLR start "synpred91_UL4"
    def synpred91_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:672:4: (n= expr_subscript '<<=' e= expr_if EOF )
        # src/ll/UL4.g:672:4: n= expr_subscript '<<=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred91_UL43490)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 50, self.FOLLOW_50_in_synpred91_UL43492)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred91_UL43496)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred91_UL43498)



    # $ANTLR end "synpred91_UL4"



    # $ANTLR start "synpred92_UL4"
    def synpred92_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:673:4: (n= expr_subscript '>>=' e= expr_if EOF )
        # src/ll/UL4.g:673:4: n= expr_subscript '>>=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred92_UL43507)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 57, self.FOLLOW_57_in_synpred92_UL43509)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred92_UL43513)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred92_UL43515)



    # $ANTLR end "synpred92_UL4"



    # $ANTLR start "synpred93_UL4"
    def synpred93_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:674:4: (n= expr_subscript '&=' e= expr_if EOF )
        # src/ll/UL4.g:674:4: n= expr_subscript '&=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred93_UL43524)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 31, self.FOLLOW_31_in_synpred93_UL43526)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred93_UL43530)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred93_UL43532)



    # $ANTLR end "synpred93_UL4"



    # $ANTLR start "synpred94_UL4"
    def synpred94_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:675:4: (n= expr_subscript '^=' e= expr_if EOF )
        # src/ll/UL4.g:675:4: n= expr_subscript '^=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred94_UL43541)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 61, self.FOLLOW_61_in_synpred94_UL43543)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred94_UL43547)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred94_UL43549)



    # $ANTLR end "synpred94_UL4"



    # $ANTLR start "synpred95_UL4"
    def synpred95_UL4_fragment(self, ):
        n = None
        e = None

        # src/ll/UL4.g:676:4: (n= expr_subscript '|=' e= expr_if EOF )
        # src/ll/UL4.g:676:4: n= expr_subscript '|=' e= expr_if EOF
        pass 
        self._state.following.append(self.FOLLOW_expr_subscript_in_synpred95_UL43558)
        n = self.expr_subscript()

        self._state.following.pop()

        self.match(self.input, 71, self.FOLLOW_71_in_synpred95_UL43560)

        self._state.following.append(self.FOLLOW_expr_if_in_synpred95_UL43564)
        e = self.expr_if()

        self._state.following.pop()

        self.match(self.input, EOF, self.FOLLOW_EOF_in_synpred95_UL43566)



    # $ANTLR end "synpred95_UL4"




    def synpred95_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred95_UL4_fragment()
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

    def synpred94_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred94_UL4_fragment()
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

    def synpred92_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred92_UL4_fragment()
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

    def synpred91_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred91_UL4_fragment()
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

    def synpred93_UL4(self):
        self._state.backtracking += 1
        start = self.input.mark()
        try:
            self.synpred93_UL4_fragment()
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
    FOLLOW_69_in_set1223 = frozenset([43])
    FOLLOW_43_in_set1227 = frozenset([72])
    FOLLOW_72_in_set1233 = frozenset([1])
    FOLLOW_69_in_set1244 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_set1252 = frozenset([39, 72])
    FOLLOW_39_in_set1263 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_set1270 = frozenset([39, 72])
    FOLLOW_39_in_set1281 = frozenset([72])
    FOLLOW_72_in_set1288 = frozenset([1])
    FOLLOW_69_in_setcomprehension1316 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_setcomprehension1322 = frozenset([64])
    FOLLOW_64_in_setcomprehension1326 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_setcomprehension1332 = frozenset([66])
    FOLLOW_66_in_setcomprehension1336 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_setcomprehension1342 = frozenset([65, 72])
    FOLLOW_65_in_setcomprehension1351 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_setcomprehension1358 = frozenset([72])
    FOLLOW_72_in_setcomprehension1371 = frozenset([1])
    FOLLOW_expr_if_in_dictitem1396 = frozenset([47])
    FOLLOW_47_in_dictitem1400 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictitem1406 = frozenset([1])
    FOLLOW_69_in_dict1427 = frozenset([72])
    FOLLOW_72_in_dict1433 = frozenset([1])
    FOLLOW_69_in_dict1444 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_dictitem_in_dict1452 = frozenset([39, 72])
    FOLLOW_39_in_dict1463 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_dictitem_in_dict1470 = frozenset([39, 72])
    FOLLOW_39_in_dict1481 = frozenset([72])
    FOLLOW_72_in_dict1488 = frozenset([1])
    FOLLOW_69_in_dictcomprehension1516 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1522 = frozenset([47])
    FOLLOW_47_in_dictcomprehension1526 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1532 = frozenset([64])
    FOLLOW_64_in_dictcomprehension1536 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_dictcomprehension1542 = frozenset([66])
    FOLLOW_66_in_dictcomprehension1546 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1552 = frozenset([65, 72])
    FOLLOW_65_in_dictcomprehension1561 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_dictcomprehension1568 = frozenset([72])
    FOLLOW_72_in_dictcomprehension1581 = frozenset([1])
    FOLLOW_expr_if_in_generatorexpression1609 = frozenset([64])
    FOLLOW_64_in_generatorexpression1615 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_generatorexpression1621 = frozenset([66])
    FOLLOW_66_in_generatorexpression1625 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_generatorexpression1631 = frozenset([1, 65])
    FOLLOW_65_in_generatorexpression1642 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_generatorexpression1649 = frozenset([1])
    FOLLOW_literal_in_atom1675 = frozenset([1])
    FOLLOW_list_in_atom1684 = frozenset([1])
    FOLLOW_listcomprehension_in_atom1693 = frozenset([1])
    FOLLOW_set_in_atom1702 = frozenset([1])
    FOLLOW_setcomprehension_in_atom1711 = frozenset([1])
    FOLLOW_dict_in_atom1720 = frozenset([1])
    FOLLOW_dictcomprehension_in_atom1729 = frozenset([1])
    FOLLOW_32_in_atom1738 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_generatorexpression_in_atom1742 = frozenset([33])
    FOLLOW_33_in_atom1746 = frozenset([1])
    FOLLOW_32_in_atom1755 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_atom1759 = frozenset([33])
    FOLLOW_33_in_atom1763 = frozenset([1])
    FOLLOW_expr_subscript_in_nestedlvalue1786 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1799 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1801 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1803 = frozenset([1])
    FOLLOW_32_in_nestedlvalue1812 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1818 = frozenset([39])
    FOLLOW_39_in_nestedlvalue1822 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1828 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1839 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_nestedlvalue1846 = frozenset([33, 39])
    FOLLOW_39_in_nestedlvalue1857 = frozenset([33])
    FOLLOW_33_in_nestedlvalue1862 = frozenset([1])
    FOLLOW_expr_if_in_slice1895 = frozenset([47])
    FOLLOW_47_in_slice1908 = frozenset([1, 5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_slice1921 = frozenset([1])
    FOLLOW_atom_in_expr_subscript1951 = frozenset([1, 32, 42, 58])
    FOLLOW_42_in_expr_subscript1967 = frozenset([14])
    FOLLOW_name_in_expr_subscript1974 = frozenset([1, 32, 42, 58])
    FOLLOW_32_in_expr_subscript1990 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 33, 34, 35, 40, 58, 67, 69, 73])
    FOLLOW_35_in_expr_subscript2020 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2024 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2032 = frozenset([33])
    FOLLOW_34_in_expr_subscript2050 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2054 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2069 = frozenset([35])
    FOLLOW_35_in_expr_subscript2076 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2080 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2095 = frozenset([33])
    FOLLOW_exprarg_in_expr_subscript2115 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2130 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2139 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2161 = frozenset([14])
    FOLLOW_name_in_expr_subscript2170 = frozenset([52])
    FOLLOW_52_in_expr_subscript2172 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2176 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2198 = frozenset([34])
    FOLLOW_34_in_expr_subscript2205 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2209 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2231 = frozenset([35])
    FOLLOW_35_in_expr_subscript2238 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2242 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2257 = frozenset([33])
    FOLLOW_name_in_expr_subscript2277 = frozenset([52])
    FOLLOW_52_in_expr_subscript2279 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2283 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2298 = frozenset([14])
    FOLLOW_name_in_expr_subscript2307 = frozenset([52])
    FOLLOW_52_in_expr_subscript2309 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2313 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2335 = frozenset([34])
    FOLLOW_34_in_expr_subscript2342 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2346 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2368 = frozenset([35])
    FOLLOW_35_in_expr_subscript2375 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_expr_subscript2379 = frozenset([33, 39])
    FOLLOW_39_in_expr_subscript2394 = frozenset([33])
    FOLLOW_33_in_expr_subscript2407 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2423 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_expr_subscript2431 = frozenset([59])
    FOLLOW_59_in_expr_subscript2438 = frozenset([1, 32, 42, 58])
    FOLLOW_58_in_expr_subscript2454 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 67, 69, 73])
    FOLLOW_slice_in_expr_subscript2462 = frozenset([59])
    FOLLOW_59_in_expr_subscript2469 = frozenset([1, 32, 42, 58])
    FOLLOW_expr_subscript_in_expr_unary2497 = frozenset([1])
    FOLLOW_40_in_expr_unary2508 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2512 = frozenset([1])
    FOLLOW_73_in_expr_unary2523 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_unary_in_expr_unary2527 = frozenset([1])
    FOLLOW_expr_unary_in_expr_mul2551 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_34_in_expr_mul2568 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_43_in_expr_mul2581 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_44_in_expr_mul2594 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_28_in_expr_mul2607 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_unary_in_expr_mul2621 = frozenset([1, 28, 34, 43, 44])
    FOLLOW_expr_mul_in_expr_add2649 = frozenset([1, 37, 40])
    FOLLOW_37_in_expr_add2666 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_40_in_expr_add2679 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_mul_in_expr_add2693 = frozenset([1, 37, 40])
    FOLLOW_expr_add_in_expr_bitshift2721 = frozenset([1, 49, 56])
    FOLLOW_49_in_expr_bitshift2738 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_56_in_expr_bitshift2751 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_add_in_expr_bitshift2765 = frozenset([1, 49, 56])
    FOLLOW_expr_bitshift_in_expr_bitand2793 = frozenset([1, 30])
    FOLLOW_30_in_expr_bitand2804 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_bitshift_in_expr_bitand2811 = frozenset([1, 30])
    FOLLOW_expr_bitand_in_expr_bitxor2839 = frozenset([1, 60])
    FOLLOW_60_in_expr_bitxor2850 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_bitand_in_expr_bitxor2857 = frozenset([1, 60])
    FOLLOW_expr_bitxor_in_expr_bitor2885 = frozenset([1, 70])
    FOLLOW_70_in_expr_bitor2896 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_bitxor_in_expr_bitor2903 = frozenset([1, 70])
    FOLLOW_expr_bitor_in_expr_cmp2931 = frozenset([1, 27, 48, 51, 53, 54, 55, 66, 67])
    FOLLOW_53_in_expr_cmp2948 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_27_in_expr_cmp2961 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_48_in_expr_cmp2974 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_51_in_expr_cmp2987 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_54_in_expr_cmp3000 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_55_in_expr_cmp3013 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_66_in_expr_cmp3026 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_67_in_expr_cmp3039 = frozenset([66])
    FOLLOW_66_in_expr_cmp3041 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 69, 73])
    FOLLOW_expr_bitor_in_expr_cmp3055 = frozenset([1, 27, 48, 51, 53, 54, 55, 66, 67])
    FOLLOW_expr_cmp_in_expr_not3083 = frozenset([1])
    FOLLOW_67_in_expr_not3094 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_not_in_expr_not3098 = frozenset([1])
    FOLLOW_expr_not_in_expr_and3122 = frozenset([1, 62])
    FOLLOW_62_in_expr_and3133 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_not_in_expr_and3140 = frozenset([1, 62])
    FOLLOW_expr_and_in_expr_or3168 = frozenset([1, 68])
    FOLLOW_68_in_expr_or3179 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_and_in_expr_or3186 = frozenset([1, 68])
    FOLLOW_expr_or_in_expr_if3214 = frozenset([1, 65])
    FOLLOW_65_in_expr_if3225 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3232 = frozenset([63])
    FOLLOW_63_in_expr_if3237 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_expr_if3244 = frozenset([1])
    FOLLOW_generatorexpression_in_exprarg3268 = frozenset([1])
    FOLLOW_expr_if_in_exprarg3277 = frozenset([1])
    FOLLOW_generatorexpression_in_expression3296 = frozenset([])
    FOLLOW_EOF_in_expression3298 = frozenset([1])
    FOLLOW_expr_if_in_expression3307 = frozenset([])
    FOLLOW_EOF_in_expression3309 = frozenset([1])
    FOLLOW_nestedlvalue_in_for_3334 = frozenset([66])
    FOLLOW_66_in_for_3338 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_for_3344 = frozenset([])
    FOLLOW_EOF_in_for_3350 = frozenset([1])
    FOLLOW_nestedlvalue_in_statement3371 = frozenset([52])
    FOLLOW_52_in_statement3373 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3377 = frozenset([])
    FOLLOW_EOF_in_statement3379 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3388 = frozenset([38])
    FOLLOW_38_in_statement3390 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3394 = frozenset([])
    FOLLOW_EOF_in_statement3396 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3405 = frozenset([41])
    FOLLOW_41_in_statement3407 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3411 = frozenset([])
    FOLLOW_EOF_in_statement3413 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3422 = frozenset([36])
    FOLLOW_36_in_statement3424 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3428 = frozenset([])
    FOLLOW_EOF_in_statement3430 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3439 = frozenset([46])
    FOLLOW_46_in_statement3441 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3445 = frozenset([])
    FOLLOW_EOF_in_statement3447 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3456 = frozenset([45])
    FOLLOW_45_in_statement3458 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3462 = frozenset([])
    FOLLOW_EOF_in_statement3464 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3473 = frozenset([29])
    FOLLOW_29_in_statement3475 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3479 = frozenset([])
    FOLLOW_EOF_in_statement3481 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3490 = frozenset([50])
    FOLLOW_50_in_statement3492 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3496 = frozenset([])
    FOLLOW_EOF_in_statement3498 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3507 = frozenset([57])
    FOLLOW_57_in_statement3509 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3513 = frozenset([])
    FOLLOW_EOF_in_statement3515 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3524 = frozenset([31])
    FOLLOW_31_in_statement3526 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3530 = frozenset([])
    FOLLOW_EOF_in_statement3532 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3541 = frozenset([61])
    FOLLOW_61_in_statement3543 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3547 = frozenset([])
    FOLLOW_EOF_in_statement3549 = frozenset([1])
    FOLLOW_expr_subscript_in_statement3558 = frozenset([71])
    FOLLOW_71_in_statement3560 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_statement3564 = frozenset([])
    FOLLOW_EOF_in_statement3566 = frozenset([1])
    FOLLOW_expression_in_statement3575 = frozenset([])
    FOLLOW_EOF_in_statement3577 = frozenset([1])
    FOLLOW_32_in_signature3600 = frozenset([14, 33, 34, 35])
    FOLLOW_35_in_signature3620 = frozenset([14])
    FOLLOW_name_in_signature3624 = frozenset([33, 39])
    FOLLOW_39_in_signature3630 = frozenset([33])
    FOLLOW_34_in_signature3642 = frozenset([14])
    FOLLOW_name_in_signature3646 = frozenset([33, 39])
    FOLLOW_39_in_signature3657 = frozenset([35])
    FOLLOW_35_in_signature3662 = frozenset([14])
    FOLLOW_name_in_signature3666 = frozenset([33, 39])
    FOLLOW_39_in_signature3677 = frozenset([33])
    FOLLOW_name_in_signature3691 = frozenset([52])
    FOLLOW_52_in_signature3695 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_signature3701 = frozenset([33, 39])
    FOLLOW_39_in_signature3712 = frozenset([14])
    FOLLOW_name_in_signature3719 = frozenset([52])
    FOLLOW_52_in_signature3724 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_signature3731 = frozenset([33, 39])
    FOLLOW_39_in_signature3747 = frozenset([34])
    FOLLOW_34_in_signature3752 = frozenset([14])
    FOLLOW_name_in_signature3756 = frozenset([33, 39])
    FOLLOW_39_in_signature3772 = frozenset([35])
    FOLLOW_35_in_signature3777 = frozenset([14])
    FOLLOW_name_in_signature3781 = frozenset([33, 39])
    FOLLOW_39_in_signature3792 = frozenset([33])
    FOLLOW_name_in_signature3806 = frozenset([33, 39])
    FOLLOW_39_in_signature3817 = frozenset([14])
    FOLLOW_name_in_signature3824 = frozenset([33, 39])
    FOLLOW_39_in_signature3840 = frozenset([14])
    FOLLOW_name_in_signature3847 = frozenset([52])
    FOLLOW_52_in_signature3852 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_exprarg_in_signature3859 = frozenset([33, 39])
    FOLLOW_39_in_signature3875 = frozenset([34])
    FOLLOW_34_in_signature3880 = frozenset([14])
    FOLLOW_name_in_signature3884 = frozenset([33, 39])
    FOLLOW_39_in_signature3900 = frozenset([35])
    FOLLOW_35_in_signature3905 = frozenset([14])
    FOLLOW_name_in_signature3909 = frozenset([33, 39])
    FOLLOW_39_in_signature3920 = frozenset([33])
    FOLLOW_33_in_signature3929 = frozenset([1])
    FOLLOW_name_in_definition3953 = frozenset([32])
    FOLLOW_signature_in_definition3966 = frozenset([])
    FOLLOW_EOF_in_definition3977 = frozenset([1])
    FOLLOW_list_in_synpred24_UL41684 = frozenset([1])
    FOLLOW_listcomprehension_in_synpred25_UL41693 = frozenset([1])
    FOLLOW_set_in_synpred26_UL41702 = frozenset([1])
    FOLLOW_setcomprehension_in_synpred27_UL41711 = frozenset([1])
    FOLLOW_dict_in_synpred28_UL41720 = frozenset([1])
    FOLLOW_dictcomprehension_in_synpred29_UL41729 = frozenset([1])
    FOLLOW_32_in_synpred30_UL41738 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_generatorexpression_in_synpred30_UL41742 = frozenset([33])
    FOLLOW_33_in_synpred30_UL41746 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred31_UL41786 = frozenset([1])
    FOLLOW_32_in_synpred32_UL41795 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 58, 69])
    FOLLOW_nestedlvalue_in_synpred32_UL41799 = frozenset([39])
    FOLLOW_39_in_synpred32_UL41801 = frozenset([33])
    FOLLOW_33_in_synpred32_UL41803 = frozenset([1])
    FOLLOW_58_in_synpred55_UL42423 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred55_UL42431 = frozenset([59])
    FOLLOW_59_in_synpred55_UL42438 = frozenset([1])
    FOLLOW_58_in_synpred56_UL42454 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 47, 58, 67, 69, 73])
    FOLLOW_slice_in_synpred56_UL42462 = frozenset([59])
    FOLLOW_59_in_synpred56_UL42469 = frozenset([1])
    FOLLOW_65_in_synpred81_UL43225 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred81_UL43232 = frozenset([63])
    FOLLOW_63_in_synpred81_UL43237 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_or_in_synpred81_UL43244 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred82_UL43268 = frozenset([1])
    FOLLOW_generatorexpression_in_synpred83_UL43296 = frozenset([])
    FOLLOW_EOF_in_synpred83_UL43298 = frozenset([1])
    FOLLOW_nestedlvalue_in_synpred84_UL43371 = frozenset([52])
    FOLLOW_52_in_synpred84_UL43373 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred84_UL43377 = frozenset([])
    FOLLOW_EOF_in_synpred84_UL43379 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred85_UL43388 = frozenset([38])
    FOLLOW_38_in_synpred85_UL43390 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred85_UL43394 = frozenset([])
    FOLLOW_EOF_in_synpred85_UL43396 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred86_UL43405 = frozenset([41])
    FOLLOW_41_in_synpred86_UL43407 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred86_UL43411 = frozenset([])
    FOLLOW_EOF_in_synpred86_UL43413 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred87_UL43422 = frozenset([36])
    FOLLOW_36_in_synpred87_UL43424 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred87_UL43428 = frozenset([])
    FOLLOW_EOF_in_synpred87_UL43430 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred88_UL43439 = frozenset([46])
    FOLLOW_46_in_synpred88_UL43441 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred88_UL43445 = frozenset([])
    FOLLOW_EOF_in_synpred88_UL43447 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred89_UL43456 = frozenset([45])
    FOLLOW_45_in_synpred89_UL43458 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred89_UL43462 = frozenset([])
    FOLLOW_EOF_in_synpred89_UL43464 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred90_UL43473 = frozenset([29])
    FOLLOW_29_in_synpred90_UL43475 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred90_UL43479 = frozenset([])
    FOLLOW_EOF_in_synpred90_UL43481 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred91_UL43490 = frozenset([50])
    FOLLOW_50_in_synpred91_UL43492 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred91_UL43496 = frozenset([])
    FOLLOW_EOF_in_synpred91_UL43498 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred92_UL43507 = frozenset([57])
    FOLLOW_57_in_synpred92_UL43509 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred92_UL43513 = frozenset([])
    FOLLOW_EOF_in_synpred92_UL43515 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred93_UL43524 = frozenset([31])
    FOLLOW_31_in_synpred93_UL43526 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred93_UL43530 = frozenset([])
    FOLLOW_EOF_in_synpred93_UL43532 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred94_UL43541 = frozenset([61])
    FOLLOW_61_in_synpred94_UL43543 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred94_UL43547 = frozenset([])
    FOLLOW_EOF_in_synpred94_UL43549 = frozenset([1])
    FOLLOW_expr_subscript_in_synpred95_UL43558 = frozenset([71])
    FOLLOW_71_in_synpred95_UL43560 = frozenset([5, 6, 10, 11, 13, 14, 15, 17, 18, 22, 32, 40, 58, 67, 69, 73])
    FOLLOW_expr_if_in_synpred95_UL43564 = frozenset([])
    FOLLOW_EOF_in_synpred95_UL43566 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("UL4Lexer", UL4Parser)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
