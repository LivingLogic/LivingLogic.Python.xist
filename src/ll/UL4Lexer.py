# $ANTLR 3.5.2 src/ll/UL4.g 2019-06-19 15:10:05

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

        
from ll import ul4c



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


class UL4Lexer(Lexer):

    grammarFileName = "src/ll/UL4.g"
    api_version = 1

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(UL4Lexer, self).__init__(input, state)

        self.delegates = []

        self.dfa15 = self.DFA15(
            self, 15,
            eot = self.DFA15_eot,
            eof = self.DFA15_eof,
            min = self.DFA15_min,
            max = self.DFA15_max,
            accept = self.DFA15_accept,
            special = self.DFA15_special,
            transition = self.DFA15_transition
            )

        self.dfa31 = self.DFA31(
            self, 31,
            eot = self.DFA31_eot,
            eof = self.DFA31_eof,
            min = self.DFA31_min,
            max = self.DFA31_max,
            accept = self.DFA31_accept,
            special = self.DFA31_special,
            transition = self.DFA31_transition
            )




                             
    def reportError(self, e):
    	raise e



    # $ANTLR start "T__28"
    def mT__28(self, ):
        try:
            _type = T__28
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:15:7: ( '!=' )
            # src/ll/UL4.g:15:9: '!='
            pass 
            self.match("!=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__28"



    # $ANTLR start "T__29"
    def mT__29(self, ):
        try:
            _type = T__29
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:16:7: ( '%' )
            # src/ll/UL4.g:16:9: '%'
            pass 
            self.match(37)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__29"



    # $ANTLR start "T__30"
    def mT__30(self, ):
        try:
            _type = T__30
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:17:7: ( '%=' )
            # src/ll/UL4.g:17:9: '%='
            pass 
            self.match("%=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__30"



    # $ANTLR start "T__31"
    def mT__31(self, ):
        try:
            _type = T__31
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:18:7: ( '&' )
            # src/ll/UL4.g:18:9: '&'
            pass 
            self.match(38)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__31"



    # $ANTLR start "T__32"
    def mT__32(self, ):
        try:
            _type = T__32
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:19:7: ( '&=' )
            # src/ll/UL4.g:19:9: '&='
            pass 
            self.match("&=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__32"



    # $ANTLR start "T__33"
    def mT__33(self, ):
        try:
            _type = T__33
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:20:7: ( '(' )
            # src/ll/UL4.g:20:9: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__33"



    # $ANTLR start "T__34"
    def mT__34(self, ):
        try:
            _type = T__34
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:21:7: ( ')' )
            # src/ll/UL4.g:21:9: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__34"



    # $ANTLR start "T__35"
    def mT__35(self, ):
        try:
            _type = T__35
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:22:7: ( '*' )
            # src/ll/UL4.g:22:9: '*'
            pass 
            self.match(42)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__35"



    # $ANTLR start "T__36"
    def mT__36(self, ):
        try:
            _type = T__36
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:23:7: ( '**' )
            # src/ll/UL4.g:23:9: '**'
            pass 
            self.match("**")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__36"



    # $ANTLR start "T__37"
    def mT__37(self, ):
        try:
            _type = T__37
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:24:7: ( '*=' )
            # src/ll/UL4.g:24:9: '*='
            pass 
            self.match("*=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__37"



    # $ANTLR start "T__38"
    def mT__38(self, ):
        try:
            _type = T__38
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:25:7: ( '+' )
            # src/ll/UL4.g:25:9: '+'
            pass 
            self.match(43)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__38"



    # $ANTLR start "T__39"
    def mT__39(self, ):
        try:
            _type = T__39
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:26:7: ( '+=' )
            # src/ll/UL4.g:26:9: '+='
            pass 
            self.match("+=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__39"



    # $ANTLR start "T__40"
    def mT__40(self, ):
        try:
            _type = T__40
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:27:7: ( ',' )
            # src/ll/UL4.g:27:9: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__40"



    # $ANTLR start "T__41"
    def mT__41(self, ):
        try:
            _type = T__41
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:28:7: ( '-' )
            # src/ll/UL4.g:28:9: '-'
            pass 
            self.match(45)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__41"



    # $ANTLR start "T__42"
    def mT__42(self, ):
        try:
            _type = T__42
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:29:7: ( '-=' )
            # src/ll/UL4.g:29:9: '-='
            pass 
            self.match("-=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__42"



    # $ANTLR start "T__43"
    def mT__43(self, ):
        try:
            _type = T__43
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:30:7: ( '.' )
            # src/ll/UL4.g:30:9: '.'
            pass 
            self.match(46)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__43"



    # $ANTLR start "T__44"
    def mT__44(self, ):
        try:
            _type = T__44
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:31:7: ( '/' )
            # src/ll/UL4.g:31:9: '/'
            pass 
            self.match(47)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__44"



    # $ANTLR start "T__45"
    def mT__45(self, ):
        try:
            _type = T__45
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:32:7: ( '//' )
            # src/ll/UL4.g:32:9: '//'
            pass 
            self.match("//")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__45"



    # $ANTLR start "T__46"
    def mT__46(self, ):
        try:
            _type = T__46
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:33:7: ( '//=' )
            # src/ll/UL4.g:33:9: '//='
            pass 
            self.match("//=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__46"



    # $ANTLR start "T__47"
    def mT__47(self, ):
        try:
            _type = T__47
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:34:7: ( '/=' )
            # src/ll/UL4.g:34:9: '/='
            pass 
            self.match("/=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__47"



    # $ANTLR start "T__48"
    def mT__48(self, ):
        try:
            _type = T__48
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:35:7: ( ':' )
            # src/ll/UL4.g:35:9: ':'
            pass 
            self.match(58)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__48"



    # $ANTLR start "T__49"
    def mT__49(self, ):
        try:
            _type = T__49
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:36:7: ( '<' )
            # src/ll/UL4.g:36:9: '<'
            pass 
            self.match(60)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__49"



    # $ANTLR start "T__50"
    def mT__50(self, ):
        try:
            _type = T__50
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:37:7: ( '<<' )
            # src/ll/UL4.g:37:9: '<<'
            pass 
            self.match("<<")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__50"



    # $ANTLR start "T__51"
    def mT__51(self, ):
        try:
            _type = T__51
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:38:7: ( '<<=' )
            # src/ll/UL4.g:38:9: '<<='
            pass 
            self.match("<<=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__51"



    # $ANTLR start "T__52"
    def mT__52(self, ):
        try:
            _type = T__52
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:39:7: ( '<=' )
            # src/ll/UL4.g:39:9: '<='
            pass 
            self.match("<=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__52"



    # $ANTLR start "T__53"
    def mT__53(self, ):
        try:
            _type = T__53
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:40:7: ( '=' )
            # src/ll/UL4.g:40:9: '='
            pass 
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__53"



    # $ANTLR start "T__54"
    def mT__54(self, ):
        try:
            _type = T__54
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:41:7: ( '==' )
            # src/ll/UL4.g:41:9: '=='
            pass 
            self.match("==")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__54"



    # $ANTLR start "T__55"
    def mT__55(self, ):
        try:
            _type = T__55
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:42:7: ( '>' )
            # src/ll/UL4.g:42:9: '>'
            pass 
            self.match(62)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__55"



    # $ANTLR start "T__56"
    def mT__56(self, ):
        try:
            _type = T__56
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:43:7: ( '>=' )
            # src/ll/UL4.g:43:9: '>='
            pass 
            self.match(">=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__56"



    # $ANTLR start "T__57"
    def mT__57(self, ):
        try:
            _type = T__57
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:44:7: ( '>>' )
            # src/ll/UL4.g:44:9: '>>'
            pass 
            self.match(">>")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__57"



    # $ANTLR start "T__58"
    def mT__58(self, ):
        try:
            _type = T__58
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:45:7: ( '>>=' )
            # src/ll/UL4.g:45:9: '>>='
            pass 
            self.match(">>=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__58"



    # $ANTLR start "T__59"
    def mT__59(self, ):
        try:
            _type = T__59
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:46:7: ( '[' )
            # src/ll/UL4.g:46:9: '['
            pass 
            self.match(91)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__59"



    # $ANTLR start "T__60"
    def mT__60(self, ):
        try:
            _type = T__60
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:47:7: ( ']' )
            # src/ll/UL4.g:47:9: ']'
            pass 
            self.match(93)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__60"



    # $ANTLR start "T__61"
    def mT__61(self, ):
        try:
            _type = T__61
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:48:7: ( '^' )
            # src/ll/UL4.g:48:9: '^'
            pass 
            self.match(94)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__61"



    # $ANTLR start "T__62"
    def mT__62(self, ):
        try:
            _type = T__62
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:49:7: ( '^=' )
            # src/ll/UL4.g:49:9: '^='
            pass 
            self.match("^=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__62"



    # $ANTLR start "T__63"
    def mT__63(self, ):
        try:
            _type = T__63
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:50:7: ( 'and' )
            # src/ll/UL4.g:50:9: 'and'
            pass 
            self.match("and")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__63"



    # $ANTLR start "T__64"
    def mT__64(self, ):
        try:
            _type = T__64
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:51:7: ( 'else' )
            # src/ll/UL4.g:51:9: 'else'
            pass 
            self.match("else")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__64"



    # $ANTLR start "T__65"
    def mT__65(self, ):
        try:
            _type = T__65
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:52:7: ( 'for' )
            # src/ll/UL4.g:52:9: 'for'
            pass 
            self.match("for")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__65"



    # $ANTLR start "T__66"
    def mT__66(self, ):
        try:
            _type = T__66
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:53:7: ( 'if' )
            # src/ll/UL4.g:53:9: 'if'
            pass 
            self.match("if")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__66"



    # $ANTLR start "T__67"
    def mT__67(self, ):
        try:
            _type = T__67
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:54:7: ( 'in' )
            # src/ll/UL4.g:54:9: 'in'
            pass 
            self.match("in")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__67"



    # $ANTLR start "T__68"
    def mT__68(self, ):
        try:
            _type = T__68
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:55:7: ( 'is' )
            # src/ll/UL4.g:55:9: 'is'
            pass 
            self.match("is")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__68"



    # $ANTLR start "T__69"
    def mT__69(self, ):
        try:
            _type = T__69
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:56:7: ( 'not' )
            # src/ll/UL4.g:56:9: 'not'
            pass 
            self.match("not")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__69"



    # $ANTLR start "T__70"
    def mT__70(self, ):
        try:
            _type = T__70
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:57:7: ( 'or' )
            # src/ll/UL4.g:57:9: 'or'
            pass 
            self.match("or")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__70"



    # $ANTLR start "T__71"
    def mT__71(self, ):
        try:
            _type = T__71
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:58:7: ( '{' )
            # src/ll/UL4.g:58:9: '{'
            pass 
            self.match(123)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__71"



    # $ANTLR start "T__72"
    def mT__72(self, ):
        try:
            _type = T__72
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:59:7: ( '|' )
            # src/ll/UL4.g:59:9: '|'
            pass 
            self.match(124)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__72"



    # $ANTLR start "T__73"
    def mT__73(self, ):
        try:
            _type = T__73
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:60:7: ( '|=' )
            # src/ll/UL4.g:60:9: '|='
            pass 
            self.match("|=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__73"



    # $ANTLR start "T__74"
    def mT__74(self, ):
        try:
            _type = T__74
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:61:7: ( '}' )
            # src/ll/UL4.g:61:9: '}'
            pass 
            self.match(125)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__74"



    # $ANTLR start "T__75"
    def mT__75(self, ):
        try:
            _type = T__75
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:62:7: ( '~' )
            # src/ll/UL4.g:62:9: '~'
            pass 
            self.match(126)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__75"



    # $ANTLR start "NONE"
    def mNONE(self, ):
        try:
            _type = NONE
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:45:2: ( 'None' )
            # src/ll/UL4.g:45:4: 'None'
            pass 
            self.match("None")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "NONE"



    # $ANTLR start "TRUE"
    def mTRUE(self, ):
        try:
            _type = TRUE
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:49:2: ( 'True' )
            # src/ll/UL4.g:49:4: 'True'
            pass 
            self.match("True")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "TRUE"



    # $ANTLR start "FALSE"
    def mFALSE(self, ):
        try:
            _type = FALSE
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:53:2: ( 'False' )
            # src/ll/UL4.g:53:4: 'False'
            pass 
            self.match("False")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "FALSE"



    # $ANTLR start "NAME"
    def mNAME(self, ):
        try:
            _type = NAME
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:57:2: ( ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )* )
            # src/ll/UL4.g:57:4: ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
            pass 
            if (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            # src/ll/UL4.g:57:28: ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((48 <= LA1_0 <= 57) or (65 <= LA1_0 <= 90) or LA1_0 == 95 or (97 <= LA1_0 <= 122)) :
                    alt1 = 1


                if alt1 == 1:
                    # src/ll/UL4.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop1




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "NAME"



    # $ANTLR start "DIGIT"
    def mDIGIT(self, ):
        try:
            # src/ll/UL4.g:63:2: ( '0' .. '9' )
            # src/ll/UL4.g:
            pass 
            if (48 <= self.input.LA(1) <= 57):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "DIGIT"



    # $ANTLR start "BIN_DIGIT"
    def mBIN_DIGIT(self, ):
        try:
            # src/ll/UL4.g:68:2: ( ( '0' | '1' ) )
            # src/ll/UL4.g:
            pass 
            if (48 <= self.input.LA(1) <= 49):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "BIN_DIGIT"



    # $ANTLR start "OCT_DIGIT"
    def mOCT_DIGIT(self, ):
        try:
            # src/ll/UL4.g:73:2: ( '0' .. '7' )
            # src/ll/UL4.g:
            pass 
            if (48 <= self.input.LA(1) <= 55):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "OCT_DIGIT"



    # $ANTLR start "HEX_DIGIT"
    def mHEX_DIGIT(self, ):
        try:
            # src/ll/UL4.g:78:2: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
            # src/ll/UL4.g:
            pass 
            if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 70) or (97 <= self.input.LA(1) <= 102):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:
            pass

    # $ANTLR end "HEX_DIGIT"



    # $ANTLR start "INT"
    def mINT(self, ):
        try:
            _type = INT
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:82:2: ( ( DIGIT )+ | '0' ( 'b' | 'B' ) ( BIN_DIGIT )+ | '0' ( 'o' | 'O' ) ( OCT_DIGIT )+ | '0' ( 'x' | 'X' ) ( HEX_DIGIT )+ )
            alt6 = 4
            LA6_0 = self.input.LA(1)

            if (LA6_0 == 48) :
                LA6 = self.input.LA(2)
                if LA6 == 66 or LA6 == 98:
                    alt6 = 2
                elif LA6 == 79 or LA6 == 111:
                    alt6 = 3
                elif LA6 == 88 or LA6 == 120:
                    alt6 = 4
                else:
                    alt6 = 1

            elif ((49 <= LA6_0 <= 57)) :
                alt6 = 1
            else:
                nvae = NoViableAltException("", 6, 0, self.input)

                raise nvae


            if alt6 == 1:
                # src/ll/UL4.g:82:4: ( DIGIT )+
                pass 
                # src/ll/UL4.g:82:4: ( DIGIT )+
                cnt2 = 0
                while True: #loop2
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if ((48 <= LA2_0 <= 57)) :
                        alt2 = 1


                    if alt2 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt2 >= 1:
                            break #loop2

                        eee = EarlyExitException(2, self.input)
                        raise eee

                    cnt2 += 1



            elif alt6 == 2:
                # src/ll/UL4.g:83:4: '0' ( 'b' | 'B' ) ( BIN_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 66 or self.input.LA(1) == 98:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:83:18: ( BIN_DIGIT )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if ((48 <= LA3_0 <= 49)) :
                        alt3 = 1


                    if alt3 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 49):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt3 >= 1:
                            break #loop3

                        eee = EarlyExitException(3, self.input)
                        raise eee

                    cnt3 += 1



            elif alt6 == 3:
                # src/ll/UL4.g:84:4: '0' ( 'o' | 'O' ) ( OCT_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 79 or self.input.LA(1) == 111:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:84:18: ( OCT_DIGIT )+
                cnt4 = 0
                while True: #loop4
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if ((48 <= LA4_0 <= 55)) :
                        alt4 = 1


                    if alt4 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 55):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt4 >= 1:
                            break #loop4

                        eee = EarlyExitException(4, self.input)
                        raise eee

                    cnt4 += 1



            elif alt6 == 4:
                # src/ll/UL4.g:85:4: '0' ( 'x' | 'X' ) ( HEX_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 88 or self.input.LA(1) == 120:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:85:18: ( HEX_DIGIT )+
                cnt5 = 0
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if ((48 <= LA5_0 <= 57) or (65 <= LA5_0 <= 70) or (97 <= LA5_0 <= 102)) :
                        alt5 = 1


                    if alt5 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 70) or (97 <= self.input.LA(1) <= 102):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt5 >= 1:
                            break #loop5

                        eee = EarlyExitException(5, self.input)
                        raise eee

                    cnt5 += 1



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "INT"



    # $ANTLR start "EXPONENT"
    def mEXPONENT(self, ):
        try:
            # src/ll/UL4.g:91:2: ( ( 'e' | 'E' ) ( '+' | '-' )? ( DIGIT )+ )
            # src/ll/UL4.g:91:4: ( 'e' | 'E' ) ( '+' | '-' )? ( DIGIT )+
            pass 
            if self.input.LA(1) == 69 or self.input.LA(1) == 101:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            # src/ll/UL4.g:91:14: ( '+' | '-' )?
            alt7 = 2
            LA7_0 = self.input.LA(1)

            if (LA7_0 == 43 or LA7_0 == 45) :
                alt7 = 1
            if alt7 == 1:
                # src/ll/UL4.g:
                pass 
                if self.input.LA(1) == 43 or self.input.LA(1) == 45:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse






            # src/ll/UL4.g:91:25: ( DIGIT )+
            cnt8 = 0
            while True: #loop8
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if ((48 <= LA8_0 <= 57)) :
                    alt8 = 1


                if alt8 == 1:
                    # src/ll/UL4.g:
                    pass 
                    if (48 <= self.input.LA(1) <= 57):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt8 >= 1:
                        break #loop8

                    eee = EarlyExitException(8, self.input)
                    raise eee

                cnt8 += 1





        finally:
            pass

    # $ANTLR end "EXPONENT"



    # $ANTLR start "FLOAT"
    def mFLOAT(self, ):
        try:
            _type = FLOAT
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:94:2: ( ( DIGIT )+ '.' ( DIGIT )* ( EXPONENT )? | '.' ( DIGIT )+ ( EXPONENT )? | ( DIGIT )+ EXPONENT )
            alt15 = 3
            alt15 = self.dfa15.predict(self.input)
            if alt15 == 1:
                # src/ll/UL4.g:94:4: ( DIGIT )+ '.' ( DIGIT )* ( EXPONENT )?
                pass 
                # src/ll/UL4.g:94:4: ( DIGIT )+
                cnt9 = 0
                while True: #loop9
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if ((48 <= LA9_0 <= 57)) :
                        alt9 = 1


                    if alt9 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt9 >= 1:
                            break #loop9

                        eee = EarlyExitException(9, self.input)
                        raise eee

                    cnt9 += 1


                self.match(46)

                # src/ll/UL4.g:94:15: ( DIGIT )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if ((48 <= LA10_0 <= 57)) :
                        alt10 = 1


                    if alt10 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        break #loop10


                # src/ll/UL4.g:94:22: ( EXPONENT )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 69 or LA11_0 == 101) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:94:22: EXPONENT
                    pass 
                    self.mEXPONENT()






            elif alt15 == 2:
                # src/ll/UL4.g:95:4: '.' ( DIGIT )+ ( EXPONENT )?
                pass 
                self.match(46)

                # src/ll/UL4.g:95:8: ( DIGIT )+
                cnt12 = 0
                while True: #loop12
                    alt12 = 2
                    LA12_0 = self.input.LA(1)

                    if ((48 <= LA12_0 <= 57)) :
                        alt12 = 1


                    if alt12 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt12 >= 1:
                            break #loop12

                        eee = EarlyExitException(12, self.input)
                        raise eee

                    cnt12 += 1


                # src/ll/UL4.g:95:15: ( EXPONENT )?
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if (LA13_0 == 69 or LA13_0 == 101) :
                    alt13 = 1
                if alt13 == 1:
                    # src/ll/UL4.g:95:15: EXPONENT
                    pass 
                    self.mEXPONENT()






            elif alt15 == 3:
                # src/ll/UL4.g:96:4: ( DIGIT )+ EXPONENT
                pass 
                # src/ll/UL4.g:96:4: ( DIGIT )+
                cnt14 = 0
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if ((48 <= LA14_0 <= 57)) :
                        alt14 = 1


                    if alt14 == 1:
                        # src/ll/UL4.g:
                        pass 
                        if (48 <= self.input.LA(1) <= 57):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        if cnt14 >= 1:
                            break #loop14

                        eee = EarlyExitException(14, self.input)
                        raise eee

                    cnt14 += 1


                self.mEXPONENT()



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "FLOAT"



    # $ANTLR start "TIME"
    def mTIME(self, ):
        try:
            # src/ll/UL4.g:102:2: ( DIGIT DIGIT ':' DIGIT DIGIT ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )? )
            # src/ll/UL4.g:102:4: DIGIT DIGIT ':' DIGIT DIGIT ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )?
            pass 
            self.mDIGIT()


            self.mDIGIT()


            self.match(58)

            self.mDIGIT()


            self.mDIGIT()


            # src/ll/UL4.g:102:32: ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )?
            alt17 = 2
            LA17_0 = self.input.LA(1)

            if (LA17_0 == 58) :
                alt17 = 1
            if alt17 == 1:
                # src/ll/UL4.g:102:34: ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )?
                pass 
                self.match(58)

                self.mDIGIT()


                self.mDIGIT()


                # src/ll/UL4.g:102:50: ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )?
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if (LA16_0 == 46) :
                    alt16 = 1
                if alt16 == 1:
                    # src/ll/UL4.g:102:52: '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT
                    pass 
                    self.match(46)

                    self.mDIGIT()


                    self.mDIGIT()


                    self.mDIGIT()


                    self.mDIGIT()


                    self.mDIGIT()


                    self.mDIGIT()











        finally:
            pass

    # $ANTLR end "TIME"



    # $ANTLR start "DATE"
    def mDATE(self, ):
        try:
            _type = DATE
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:104:2: ( '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ')' )
            # src/ll/UL4.g:104:4: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ')'
            pass 
            self.match(64)

            self.match(40)

            self.mDIGIT()


            self.mDIGIT()


            self.mDIGIT()


            self.mDIGIT()


            self.match(45)

            self.mDIGIT()


            self.mDIGIT()


            self.match(45)

            self.mDIGIT()


            self.mDIGIT()


            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "DATE"



    # $ANTLR start "DATETIME"
    def mDATETIME(self, ):
        try:
            _type = DATETIME
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:107:2: ( '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT 'T' ( TIME )? ')' )
            # src/ll/UL4.g:107:4: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT 'T' ( TIME )? ')'
            pass 
            self.match(64)

            self.match(40)

            self.mDIGIT()


            self.mDIGIT()


            self.mDIGIT()


            self.mDIGIT()


            self.match(45)

            self.mDIGIT()


            self.mDIGIT()


            self.match(45)

            self.mDIGIT()


            self.mDIGIT()


            self.match(84)

            # src/ll/UL4.g:107:72: ( TIME )?
            alt18 = 2
            LA18_0 = self.input.LA(1)

            if ((48 <= LA18_0 <= 57)) :
                alt18 = 1
            if alt18 == 1:
                # src/ll/UL4.g:107:72: TIME
                pass 
                self.mTIME()





            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "DATETIME"



    # $ANTLR start "COLOR"
    def mCOLOR(self, ):
        try:
            _type = COLOR
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:110:2: ( '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            alt19 = 4
            LA19_0 = self.input.LA(1)

            if (LA19_0 == 35) :
                LA19_1 = self.input.LA(2)

                if ((48 <= LA19_1 <= 57) or (65 <= LA19_1 <= 70) or (97 <= LA19_1 <= 102)) :
                    LA19_2 = self.input.LA(3)

                    if ((48 <= LA19_2 <= 57) or (65 <= LA19_2 <= 70) or (97 <= LA19_2 <= 102)) :
                        LA19_3 = self.input.LA(4)

                        if ((48 <= LA19_3 <= 57) or (65 <= LA19_3 <= 70) or (97 <= LA19_3 <= 102)) :
                            LA19_4 = self.input.LA(5)

                            if ((48 <= LA19_4 <= 57) or (65 <= LA19_4 <= 70) or (97 <= LA19_4 <= 102)) :
                                LA19_6 = self.input.LA(6)

                                if ((48 <= LA19_6 <= 57) or (65 <= LA19_6 <= 70) or (97 <= LA19_6 <= 102)) :
                                    LA19_8 = self.input.LA(7)

                                    if ((48 <= LA19_8 <= 57) or (65 <= LA19_8 <= 70) or (97 <= LA19_8 <= 102)) :
                                        LA19_9 = self.input.LA(8)

                                        if ((48 <= LA19_9 <= 57) or (65 <= LA19_9 <= 70) or (97 <= LA19_9 <= 102)) :
                                            alt19 = 4
                                        else:
                                            alt19 = 3

                                    else:
                                        nvae = NoViableAltException("", 19, 8, self.input)

                                        raise nvae


                                else:
                                    alt19 = 2

                            else:
                                alt19 = 1

                        else:
                            nvae = NoViableAltException("", 19, 3, self.input)

                            raise nvae


                    else:
                        nvae = NoViableAltException("", 19, 2, self.input)

                        raise nvae


                else:
                    nvae = NoViableAltException("", 19, 1, self.input)

                    raise nvae


            else:
                nvae = NoViableAltException("", 19, 0, self.input)

                raise nvae


            if alt19 == 1:
                # src/ll/UL4.g:110:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt19 == 2:
                # src/ll/UL4.g:111:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt19 == 3:
                # src/ll/UL4.g:112:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt19 == 4:
                # src/ll/UL4.g:113:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "COLOR"



    # $ANTLR start "WS"
    def mWS(self, ):
        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:117:2: ( ( ' ' | '\\t' | '\\r' | '\\n' ) )
            # src/ll/UL4.g:117:4: ( ' ' | '\\t' | '\\r' | '\\n' )
            pass 
            if (9 <= self.input.LA(1) <= 10) or self.input.LA(1) == 13 or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            #action start
            _channel=HIDDEN; 
            #action end




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "WS"



    # $ANTLR start "STRING"
    def mSTRING(self, ):
        try:
            _type = STRING
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:121:2: ( '\"' ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )* '\"' | '\\'' ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )* '\\'' )
            alt22 = 2
            LA22_0 = self.input.LA(1)

            if (LA22_0 == 34) :
                alt22 = 1
            elif (LA22_0 == 39) :
                alt22 = 2
            else:
                nvae = NoViableAltException("", 22, 0, self.input)

                raise nvae


            if alt22 == 1:
                # src/ll/UL4.g:121:4: '\"' ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )* '\"'
                pass 
                self.match(34)

                # src/ll/UL4.g:121:8: ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )*
                while True: #loop20
                    alt20 = 3
                    LA20_0 = self.input.LA(1)

                    if (LA20_0 == 92) :
                        alt20 = 1
                    elif ((0 <= LA20_0 <= 9) or (11 <= LA20_0 <= 12) or (14 <= LA20_0 <= 33) or (35 <= LA20_0 <= 91) or (93 <= LA20_0 <= 65535)) :
                        alt20 = 2


                    if alt20 == 1:
                        # src/ll/UL4.g:121:10: ESC_SEQ
                        pass 
                        self.mESC_SEQ()



                    elif alt20 == 2:
                        # src/ll/UL4.g:121:20: ~ ( '\\\\' | '\"' | '\\r' | '\\n' )
                        pass 
                        if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 33) or (35 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        break #loop20


                self.match(34)


            elif alt22 == 2:
                # src/ll/UL4.g:122:4: '\\'' ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )* '\\''
                pass 
                self.match(39)

                # src/ll/UL4.g:122:9: ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )*
                while True: #loop21
                    alt21 = 3
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == 92) :
                        alt21 = 1
                    elif ((0 <= LA21_0 <= 9) or (11 <= LA21_0 <= 12) or (14 <= LA21_0 <= 38) or (40 <= LA21_0 <= 91) or (93 <= LA21_0 <= 65535)) :
                        alt21 = 2


                    if alt21 == 1:
                        # src/ll/UL4.g:122:11: ESC_SEQ
                        pass 
                        self.mESC_SEQ()



                    elif alt21 == 2:
                        # src/ll/UL4.g:122:21: ~ ( '\\\\' | '\\'' | '\\r' | '\\n' )
                        pass 
                        if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 38) or (40 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        break #loop21


                self.match(39)


            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "STRING"



    # $ANTLR start "STRING3"
    def mSTRING3(self, ):
        try:
            _type = STRING3
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:126:2: ( '\"\"\"' ( options {greedy=false; } : TRIQUOTE )* '\"\"\"' | '\\'\\'\\'' ( options {greedy=false; } : TRIAPOS )* '\\'\\'\\'' )
            alt25 = 2
            LA25_0 = self.input.LA(1)

            if (LA25_0 == 34) :
                alt25 = 1
            elif (LA25_0 == 39) :
                alt25 = 2
            else:
                nvae = NoViableAltException("", 25, 0, self.input)

                raise nvae


            if alt25 == 1:
                # src/ll/UL4.g:126:4: '\"\"\"' ( options {greedy=false; } : TRIQUOTE )* '\"\"\"'
                pass 
                self.match("\"\"\"")


                # src/ll/UL4.g:126:10: ( options {greedy=false; } : TRIQUOTE )*
                while True: #loop23
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == 34) :
                        LA23_1 = self.input.LA(2)

                        if (LA23_1 == 34) :
                            LA23_3 = self.input.LA(3)

                            if (LA23_3 == 34) :
                                alt23 = 2
                            elif ((0 <= LA23_3 <= 33) or (35 <= LA23_3 <= 65535)) :
                                alt23 = 1


                        elif ((0 <= LA23_1 <= 33) or (35 <= LA23_1 <= 65535)) :
                            alt23 = 1


                    elif ((0 <= LA23_0 <= 33) or (35 <= LA23_0 <= 65535)) :
                        alt23 = 1


                    if alt23 == 1:
                        # src/ll/UL4.g:126:35: TRIQUOTE
                        pass 
                        self.mTRIQUOTE()



                    else:
                        break #loop23


                self.match("\"\"\"")



            elif alt25 == 2:
                # src/ll/UL4.g:127:5: '\\'\\'\\'' ( options {greedy=false; } : TRIAPOS )* '\\'\\'\\''
                pass 
                self.match("'''")


                # src/ll/UL4.g:127:14: ( options {greedy=false; } : TRIAPOS )*
                while True: #loop24
                    alt24 = 2
                    LA24_0 = self.input.LA(1)

                    if (LA24_0 == 39) :
                        LA24_1 = self.input.LA(2)

                        if (LA24_1 == 39) :
                            LA24_3 = self.input.LA(3)

                            if (LA24_3 == 39) :
                                alt24 = 2
                            elif ((0 <= LA24_3 <= 38) or (40 <= LA24_3 <= 65535)) :
                                alt24 = 1


                        elif ((0 <= LA24_1 <= 38) or (40 <= LA24_1 <= 65535)) :
                            alt24 = 1


                    elif ((0 <= LA24_0 <= 38) or (40 <= LA24_0 <= 65535)) :
                        alt24 = 1


                    if alt24 == 1:
                        # src/ll/UL4.g:127:39: TRIAPOS
                        pass 
                        self.mTRIAPOS()



                    else:
                        break #loop24


                self.match("'''")



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "STRING3"



    # $ANTLR start "TRIQUOTE"
    def mTRIQUOTE(self, ):
        try:
            # src/ll/UL4.g:133:2: ( ( '\"' | '\"\"' )? ( ESC_SEQ |~ ( '\\\\' | '\"' ) )+ )
            # src/ll/UL4.g:133:4: ( '\"' | '\"\"' )? ( ESC_SEQ |~ ( '\\\\' | '\"' ) )+
            pass 
            # src/ll/UL4.g:133:4: ( '\"' | '\"\"' )?
            alt26 = 3
            LA26_0 = self.input.LA(1)

            if (LA26_0 == 34) :
                LA26_1 = self.input.LA(2)

                if (LA26_1 == 34) :
                    alt26 = 2
                elif ((0 <= LA26_1 <= 33) or (35 <= LA26_1 <= 65535)) :
                    alt26 = 1
            if alt26 == 1:
                # src/ll/UL4.g:133:5: '\"'
                pass 
                self.match(34)


            elif alt26 == 2:
                # src/ll/UL4.g:133:9: '\"\"'
                pass 
                self.match("\"\"")





            # src/ll/UL4.g:133:16: ( ESC_SEQ |~ ( '\\\\' | '\"' ) )+
            cnt27 = 0
            while True: #loop27
                alt27 = 3
                LA27_0 = self.input.LA(1)

                if (LA27_0 == 92) :
                    alt27 = 1
                elif ((0 <= LA27_0 <= 33) or (35 <= LA27_0 <= 91) or (93 <= LA27_0 <= 65535)) :
                    alt27 = 2


                if alt27 == 1:
                    # src/ll/UL4.g:133:17: ESC_SEQ
                    pass 
                    self.mESC_SEQ()



                elif alt27 == 2:
                    # src/ll/UL4.g:133:25: ~ ( '\\\\' | '\"' )
                    pass 
                    if (0 <= self.input.LA(1) <= 33) or (35 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt27 >= 1:
                        break #loop27

                    eee = EarlyExitException(27, self.input)
                    raise eee

                cnt27 += 1





        finally:
            pass

    # $ANTLR end "TRIQUOTE"



    # $ANTLR start "TRIAPOS"
    def mTRIAPOS(self, ):
        try:
            # src/ll/UL4.g:138:2: ( ( '\\'' | '\\'\\'' )? ( ESC_SEQ |~ ( '\\\\' | '\\'' ) )+ )
            # src/ll/UL4.g:138:4: ( '\\'' | '\\'\\'' )? ( ESC_SEQ |~ ( '\\\\' | '\\'' ) )+
            pass 
            # src/ll/UL4.g:138:4: ( '\\'' | '\\'\\'' )?
            alt28 = 3
            LA28_0 = self.input.LA(1)

            if (LA28_0 == 39) :
                LA28_1 = self.input.LA(2)

                if (LA28_1 == 39) :
                    alt28 = 2
                elif ((0 <= LA28_1 <= 38) or (40 <= LA28_1 <= 65535)) :
                    alt28 = 1
            if alt28 == 1:
                # src/ll/UL4.g:138:5: '\\''
                pass 
                self.match(39)


            elif alt28 == 2:
                # src/ll/UL4.g:138:10: '\\'\\''
                pass 
                self.match("''")





            # src/ll/UL4.g:138:19: ( ESC_SEQ |~ ( '\\\\' | '\\'' ) )+
            cnt29 = 0
            while True: #loop29
                alt29 = 3
                LA29_0 = self.input.LA(1)

                if (LA29_0 == 92) :
                    alt29 = 1
                elif ((0 <= LA29_0 <= 38) or (40 <= LA29_0 <= 91) or (93 <= LA29_0 <= 65535)) :
                    alt29 = 2


                if alt29 == 1:
                    # src/ll/UL4.g:138:20: ESC_SEQ
                    pass 
                    self.mESC_SEQ()



                elif alt29 == 2:
                    # src/ll/UL4.g:138:28: ~ ( '\\\\' | '\\'' )
                    pass 
                    if (0 <= self.input.LA(1) <= 38) or (40 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt29 >= 1:
                        break #loop29

                    eee = EarlyExitException(29, self.input)
                    raise eee

                cnt29 += 1





        finally:
            pass

    # $ANTLR end "TRIAPOS"



    # $ANTLR start "ESC_SEQ"
    def mESC_SEQ(self, ):
        try:
            # src/ll/UL4.g:143:2: ( '\\\\' ( 'a' | 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | UNICODE1_ESC | UNICODE2_ESC | UNICODE4_ESC )
            alt30 = 4
            LA30_0 = self.input.LA(1)

            if (LA30_0 == 92) :
                LA30 = self.input.LA(2)
                if LA30 == 34 or LA30 == 39 or LA30 == 92 or LA30 == 97 or LA30 == 98 or LA30 == 102 or LA30 == 110 or LA30 == 114 or LA30 == 116:
                    alt30 = 1
                elif LA30 == 120:
                    alt30 = 2
                elif LA30 == 117:
                    alt30 = 3
                elif LA30 == 85:
                    alt30 = 4
                else:
                    nvae = NoViableAltException("", 30, 1, self.input)

                    raise nvae


            else:
                nvae = NoViableAltException("", 30, 0, self.input)

                raise nvae


            if alt30 == 1:
                # src/ll/UL4.g:143:4: '\\\\' ( 'a' | 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
                pass 
                self.match(92)

                if self.input.LA(1) == 34 or self.input.LA(1) == 39 or self.input.LA(1) == 92 or (97 <= self.input.LA(1) <= 98) or self.input.LA(1) == 102 or self.input.LA(1) == 110 or self.input.LA(1) == 114 or self.input.LA(1) == 116:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse




            elif alt30 == 2:
                # src/ll/UL4.g:144:4: UNICODE1_ESC
                pass 
                self.mUNICODE1_ESC()



            elif alt30 == 3:
                # src/ll/UL4.g:145:4: UNICODE2_ESC
                pass 
                self.mUNICODE2_ESC()



            elif alt30 == 4:
                # src/ll/UL4.g:146:4: UNICODE4_ESC
                pass 
                self.mUNICODE4_ESC()




        finally:
            pass

    # $ANTLR end "ESC_SEQ"



    # $ANTLR start "UNICODE1_ESC"
    def mUNICODE1_ESC(self, ):
        try:
            # src/ll/UL4.g:151:2: ( '\\\\' 'x' HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:151:4: '\\\\' 'x' HEX_DIGIT HEX_DIGIT
            pass 
            self.match(92)

            self.match(120)

            self.mHEX_DIGIT()


            self.mHEX_DIGIT()





        finally:
            pass

    # $ANTLR end "UNICODE1_ESC"



    # $ANTLR start "UNICODE2_ESC"
    def mUNICODE2_ESC(self, ):
        try:
            # src/ll/UL4.g:156:2: ( '\\\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:156:4: '\\\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
            pass 
            self.match(92)

            self.match(117)

            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()





        finally:
            pass

    # $ANTLR end "UNICODE2_ESC"



    # $ANTLR start "UNICODE4_ESC"
    def mUNICODE4_ESC(self, ):
        try:
            # src/ll/UL4.g:161:2: ( '\\\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:161:4: '\\\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
            pass 
            self.match(92)

            self.match(85)

            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()


            self.mHEX_DIGIT()





        finally:
            pass

    # $ANTLR end "UNICODE4_ESC"



    def mTokens(self):
        # src/ll/UL4.g:1:8: ( T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | T__52 | T__53 | T__54 | T__55 | T__56 | T__57 | T__58 | T__59 | T__60 | T__61 | T__62 | T__63 | T__64 | T__65 | T__66 | T__67 | T__68 | T__69 | T__70 | T__71 | T__72 | T__73 | T__74 | T__75 | NONE | TRUE | FALSE | NAME | INT | FLOAT | DATE | DATETIME | COLOR | WS | STRING | STRING3 )
        alt31 = 60
        alt31 = self.dfa31.predict(self.input)
        if alt31 == 1:
            # src/ll/UL4.g:1:10: T__28
            pass 
            self.mT__28()



        elif alt31 == 2:
            # src/ll/UL4.g:1:16: T__29
            pass 
            self.mT__29()



        elif alt31 == 3:
            # src/ll/UL4.g:1:22: T__30
            pass 
            self.mT__30()



        elif alt31 == 4:
            # src/ll/UL4.g:1:28: T__31
            pass 
            self.mT__31()



        elif alt31 == 5:
            # src/ll/UL4.g:1:34: T__32
            pass 
            self.mT__32()



        elif alt31 == 6:
            # src/ll/UL4.g:1:40: T__33
            pass 
            self.mT__33()



        elif alt31 == 7:
            # src/ll/UL4.g:1:46: T__34
            pass 
            self.mT__34()



        elif alt31 == 8:
            # src/ll/UL4.g:1:52: T__35
            pass 
            self.mT__35()



        elif alt31 == 9:
            # src/ll/UL4.g:1:58: T__36
            pass 
            self.mT__36()



        elif alt31 == 10:
            # src/ll/UL4.g:1:64: T__37
            pass 
            self.mT__37()



        elif alt31 == 11:
            # src/ll/UL4.g:1:70: T__38
            pass 
            self.mT__38()



        elif alt31 == 12:
            # src/ll/UL4.g:1:76: T__39
            pass 
            self.mT__39()



        elif alt31 == 13:
            # src/ll/UL4.g:1:82: T__40
            pass 
            self.mT__40()



        elif alt31 == 14:
            # src/ll/UL4.g:1:88: T__41
            pass 
            self.mT__41()



        elif alt31 == 15:
            # src/ll/UL4.g:1:94: T__42
            pass 
            self.mT__42()



        elif alt31 == 16:
            # src/ll/UL4.g:1:100: T__43
            pass 
            self.mT__43()



        elif alt31 == 17:
            # src/ll/UL4.g:1:106: T__44
            pass 
            self.mT__44()



        elif alt31 == 18:
            # src/ll/UL4.g:1:112: T__45
            pass 
            self.mT__45()



        elif alt31 == 19:
            # src/ll/UL4.g:1:118: T__46
            pass 
            self.mT__46()



        elif alt31 == 20:
            # src/ll/UL4.g:1:124: T__47
            pass 
            self.mT__47()



        elif alt31 == 21:
            # src/ll/UL4.g:1:130: T__48
            pass 
            self.mT__48()



        elif alt31 == 22:
            # src/ll/UL4.g:1:136: T__49
            pass 
            self.mT__49()



        elif alt31 == 23:
            # src/ll/UL4.g:1:142: T__50
            pass 
            self.mT__50()



        elif alt31 == 24:
            # src/ll/UL4.g:1:148: T__51
            pass 
            self.mT__51()



        elif alt31 == 25:
            # src/ll/UL4.g:1:154: T__52
            pass 
            self.mT__52()



        elif alt31 == 26:
            # src/ll/UL4.g:1:160: T__53
            pass 
            self.mT__53()



        elif alt31 == 27:
            # src/ll/UL4.g:1:166: T__54
            pass 
            self.mT__54()



        elif alt31 == 28:
            # src/ll/UL4.g:1:172: T__55
            pass 
            self.mT__55()



        elif alt31 == 29:
            # src/ll/UL4.g:1:178: T__56
            pass 
            self.mT__56()



        elif alt31 == 30:
            # src/ll/UL4.g:1:184: T__57
            pass 
            self.mT__57()



        elif alt31 == 31:
            # src/ll/UL4.g:1:190: T__58
            pass 
            self.mT__58()



        elif alt31 == 32:
            # src/ll/UL4.g:1:196: T__59
            pass 
            self.mT__59()



        elif alt31 == 33:
            # src/ll/UL4.g:1:202: T__60
            pass 
            self.mT__60()



        elif alt31 == 34:
            # src/ll/UL4.g:1:208: T__61
            pass 
            self.mT__61()



        elif alt31 == 35:
            # src/ll/UL4.g:1:214: T__62
            pass 
            self.mT__62()



        elif alt31 == 36:
            # src/ll/UL4.g:1:220: T__63
            pass 
            self.mT__63()



        elif alt31 == 37:
            # src/ll/UL4.g:1:226: T__64
            pass 
            self.mT__64()



        elif alt31 == 38:
            # src/ll/UL4.g:1:232: T__65
            pass 
            self.mT__65()



        elif alt31 == 39:
            # src/ll/UL4.g:1:238: T__66
            pass 
            self.mT__66()



        elif alt31 == 40:
            # src/ll/UL4.g:1:244: T__67
            pass 
            self.mT__67()



        elif alt31 == 41:
            # src/ll/UL4.g:1:250: T__68
            pass 
            self.mT__68()



        elif alt31 == 42:
            # src/ll/UL4.g:1:256: T__69
            pass 
            self.mT__69()



        elif alt31 == 43:
            # src/ll/UL4.g:1:262: T__70
            pass 
            self.mT__70()



        elif alt31 == 44:
            # src/ll/UL4.g:1:268: T__71
            pass 
            self.mT__71()



        elif alt31 == 45:
            # src/ll/UL4.g:1:274: T__72
            pass 
            self.mT__72()



        elif alt31 == 46:
            # src/ll/UL4.g:1:280: T__73
            pass 
            self.mT__73()



        elif alt31 == 47:
            # src/ll/UL4.g:1:286: T__74
            pass 
            self.mT__74()



        elif alt31 == 48:
            # src/ll/UL4.g:1:292: T__75
            pass 
            self.mT__75()



        elif alt31 == 49:
            # src/ll/UL4.g:1:298: NONE
            pass 
            self.mNONE()



        elif alt31 == 50:
            # src/ll/UL4.g:1:303: TRUE
            pass 
            self.mTRUE()



        elif alt31 == 51:
            # src/ll/UL4.g:1:308: FALSE
            pass 
            self.mFALSE()



        elif alt31 == 52:
            # src/ll/UL4.g:1:314: NAME
            pass 
            self.mNAME()



        elif alt31 == 53:
            # src/ll/UL4.g:1:319: INT
            pass 
            self.mINT()



        elif alt31 == 54:
            # src/ll/UL4.g:1:323: FLOAT
            pass 
            self.mFLOAT()



        elif alt31 == 55:
            # src/ll/UL4.g:1:329: DATE
            pass 
            self.mDATE()



        elif alt31 == 56:
            # src/ll/UL4.g:1:334: DATETIME
            pass 
            self.mDATETIME()



        elif alt31 == 57:
            # src/ll/UL4.g:1:343: COLOR
            pass 
            self.mCOLOR()



        elif alt31 == 58:
            # src/ll/UL4.g:1:349: WS
            pass 
            self.mWS()



        elif alt31 == 59:
            # src/ll/UL4.g:1:352: STRING
            pass 
            self.mSTRING()



        elif alt31 == 60:
            # src/ll/UL4.g:1:359: STRING3
            pass 
            self.mSTRING3()








    # lookup tables for DFA #15

    DFA15_eot = DFA.unpack(
        "\5\uffff"
        )

    DFA15_eof = DFA.unpack(
        "\5\uffff"
        )

    DFA15_min = DFA.unpack(
        "\2\56\3\uffff"
        )

    DFA15_max = DFA.unpack(
        "\1\71\1\145\3\uffff"
        )

    DFA15_accept = DFA.unpack(
        "\2\uffff\1\2\1\1\1\3"
        )

    DFA15_special = DFA.unpack(
        "\5\uffff"
        )


    DFA15_transition = [
        DFA.unpack("\1\2\1\uffff\12\1"),
        DFA.unpack("\1\3\1\uffff\12\1\13\uffff\1\4\37\uffff\1\4"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("")
    ]

    # class definition for DFA #15

    class DFA15(DFA):
        pass


    # lookup tables for DFA #31

    DFA31_eot = DFA.unpack(
        "\2\uffff\1\51\1\53\2\uffff\1\56\1\60\1\uffff\1\62\1\63\1\67\1\uffff"
        "\1\72\1\74\1\77\2\uffff\1\101\6\40\1\uffff\1\113\2\uffff\3\40\1"
        "\uffff\2\117\22\uffff\1\125\2\uffff\1\127\5\uffff\1\131\3\uffff"
        "\3\40\1\135\1\136\1\137\1\40\1\141\2\uffff\3\40\2\uffff\1\122\1"
        "\uffff\1\122\6\uffff\1\147\1\40\1\151\3\uffff\1\152\1\uffff\3\40"
        "\3\uffff\1\157\2\uffff\1\160\1\161\1\40\4\uffff\1\164\13\uffff"
        )

    DFA31_eof = DFA.unpack(
        "\176\uffff"
        )

    DFA31_min = DFA.unpack(
        "\1\11\1\uffff\2\75\2\uffff\1\52\1\75\1\uffff\1\75\1\60\1\57\1\uffff"
        "\1\74\2\75\2\uffff\1\75\1\156\1\154\1\157\1\146\1\157\1\162\1\uffff"
        "\1\75\2\uffff\1\157\1\162\1\141\1\uffff\2\56\1\50\2\uffff\2\0\15"
        "\uffff\1\75\2\uffff\1\75\5\uffff\1\75\3\uffff\1\144\1\163\1\162"
        "\3\60\1\164\1\60\2\uffff\1\156\1\165\1\154\1\uffff\1\60\1\42\1"
        "\uffff\1\47\6\uffff\1\60\1\145\1\60\3\uffff\1\60\1\uffff\2\145"
        "\1\163\1\60\2\uffff\1\60\2\uffff\2\60\1\145\1\60\3\uffff\2\60\1"
        "\uffff\1\55\2\60\1\55\2\60\1\51\2\uffff"
        )

    DFA31_max = DFA.unpack(
        "\1\176\1\uffff\2\75\2\uffff\2\75\1\uffff\1\75\1\71\1\75\1\uffff"
        "\2\75\1\76\2\uffff\1\75\1\156\1\154\1\157\1\163\1\157\1\162\1\uffff"
        "\1\75\2\uffff\1\157\1\162\1\141\1\uffff\2\145\1\50\2\uffff\2\uffff"
        "\15\uffff\1\75\2\uffff\1\75\5\uffff\1\75\3\uffff\1\144\1\163\1"
        "\162\3\172\1\164\1\172\2\uffff\1\156\1\165\1\154\1\uffff\1\71\1"
        "\42\1\uffff\1\47\6\uffff\1\172\1\145\1\172\3\uffff\1\172\1\uffff"
        "\2\145\1\163\1\71\2\uffff\1\172\2\uffff\2\172\1\145\1\71\3\uffff"
        "\1\172\1\71\1\uffff\1\55\2\71\1\55\2\71\1\124\2\uffff"
        )

    DFA31_accept = DFA.unpack(
        "\1\uffff\1\1\2\uffff\1\6\1\7\2\uffff\1\15\3\uffff\1\25\3\uffff"
        "\1\40\1\41\7\uffff\1\54\1\uffff\1\57\1\60\3\uffff\1\64\3\uffff"
        "\1\71\1\72\2\uffff\1\3\1\2\1\5\1\4\1\11\1\12\1\10\1\14\1\13\1\17"
        "\1\16\1\20\1\66\1\uffff\1\24\1\21\1\uffff\1\31\1\26\1\33\1\32\1"
        "\35\1\uffff\1\34\1\43\1\42\10\uffff\1\56\1\55\3\uffff\1\65\2\uffff"
        "\1\73\1\uffff\1\23\1\22\1\30\1\27\1\37\1\36\3\uffff\1\47\1\50\1"
        "\51\1\uffff\1\53\4\uffff\1\74\1\44\1\uffff\1\46\1\52\4\uffff\1"
        "\45\1\61\1\62\2\uffff\1\63\7\uffff\1\67\1\70"
        )

    DFA31_special = DFA.unpack(
        "\46\uffff\1\1\1\0\126\uffff"
        )


    DFA31_transition = [
        DFA.unpack("\2\45\2\uffff\1\45\22\uffff\1\45\1\1\1\46\1\44\1\uffff"
        "\1\2\1\3\1\47\1\4\1\5\1\6\1\7\1\10\1\11\1\12\1\13\1\41\11\42\1"
        "\14\1\uffff\1\15\1\16\1\17\1\uffff\1\43\5\40\1\37\7\40\1\35\5\40"
        "\1\36\6\40\1\20\1\uffff\1\21\1\22\1\40\1\uffff\1\23\3\40\1\24\1"
        "\25\2\40\1\26\4\40\1\27\1\30\13\40\1\31\1\32\1\33\1\34"),
        DFA.unpack(""),
        DFA.unpack("\1\50"),
        DFA.unpack("\1\52"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\54\22\uffff\1\55"),
        DFA.unpack("\1\57"),
        DFA.unpack(""),
        DFA.unpack("\1\61"),
        DFA.unpack("\12\64"),
        DFA.unpack("\1\65\15\uffff\1\66"),
        DFA.unpack(""),
        DFA.unpack("\1\70\1\71"),
        DFA.unpack("\1\73"),
        DFA.unpack("\1\75\1\76"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\100"),
        DFA.unpack("\1\102"),
        DFA.unpack("\1\103"),
        DFA.unpack("\1\104"),
        DFA.unpack("\1\105\7\uffff\1\106\4\uffff\1\107"),
        DFA.unpack("\1\110"),
        DFA.unpack("\1\111"),
        DFA.unpack(""),
        DFA.unpack("\1\112"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\114"),
        DFA.unpack("\1\115"),
        DFA.unpack("\1\116"),
        DFA.unpack(""),
        DFA.unpack("\1\64\1\uffff\12\42\13\uffff\1\64\37\uffff\1\64"),
        DFA.unpack("\1\64\1\uffff\12\42\13\uffff\1\64\37\uffff\1\64"),
        DFA.unpack("\1\120"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\122\1\uffff\2\122\1\uffff\24\122\1\121\uffdd\122"),
        DFA.unpack("\12\122\1\uffff\2\122\1\uffff\31\122\1\123\uffd8\122"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\124"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\126"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\130"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\132"),
        DFA.unpack("\1\133"),
        DFA.unpack("\1\134"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\1\140"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\142"),
        DFA.unpack("\1\143"),
        DFA.unpack("\1\144"),
        DFA.unpack(""),
        DFA.unpack("\12\145"),
        DFA.unpack("\1\146"),
        DFA.unpack(""),
        DFA.unpack("\1\146"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\1\150"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack(""),
        DFA.unpack("\1\153"),
        DFA.unpack("\1\154"),
        DFA.unpack("\1\155"),
        DFA.unpack("\12\156"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\1\162"),
        DFA.unpack("\12\163"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\40\7\uffff\32\40\4\uffff\1\40\1\uffff\32\40"),
        DFA.unpack("\12\165"),
        DFA.unpack(""),
        DFA.unpack("\1\166"),
        DFA.unpack("\12\167"),
        DFA.unpack("\12\170"),
        DFA.unpack("\1\171"),
        DFA.unpack("\12\172"),
        DFA.unpack("\12\173"),
        DFA.unpack("\1\174\52\uffff\1\175"),
        DFA.unpack(""),
        DFA.unpack("")
    ]

    # class definition for DFA #31

    class DFA31(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA31_39 = input.LA(1)

                s = -1
                if (LA31_39 == 39):
                    s = 83

                elif ((0 <= LA31_39 <= 9) or (11 <= LA31_39 <= 12) or (14 <= LA31_39 <= 38) or (40 <= LA31_39 <= 65535)):
                    s = 82

                if s >= 0:
                    return s
            elif s == 1: 
                LA31_38 = input.LA(1)

                s = -1
                if (LA31_38 == 34):
                    s = 81

                elif ((0 <= LA31_38 <= 9) or (11 <= LA31_38 <= 12) or (14 <= LA31_38 <= 33) or (35 <= LA31_38 <= 65535)):
                    s = 82

                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 31, _s, input)
            self_.error(nvae)
            raise nvae

 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(UL4Lexer)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
