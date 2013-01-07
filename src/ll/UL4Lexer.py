# $ANTLR 3.4 src/ll/UL4.g 2013-01-07 15:07:34

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

        
from ll import ul4c



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

        self.dfa25 = self.DFA25(
            self, 25,
            eot = self.DFA25_eot,
            eof = self.DFA25_eof,
            min = self.DFA25_min,
            max = self.DFA25_max,
            accept = self.DFA25_accept,
            special = self.DFA25_special,
            transition = self.DFA25_transition
            )




                             
    def reportError(self, e):
       raise e



    # $ANTLR start "T__24"
    def mT__24(self, ):
        try:
            _type = T__24
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:15:7: ( '!=' )
            # src/ll/UL4.g:15:9: '!='
            pass 
            self.match("!=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__24"



    # $ANTLR start "T__25"
    def mT__25(self, ):
        try:
            _type = T__25
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:16:7: ( '%' )
            # src/ll/UL4.g:16:9: '%'
            pass 
            self.match(37)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__25"



    # $ANTLR start "T__26"
    def mT__26(self, ):
        try:
            _type = T__26
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:17:7: ( '%=' )
            # src/ll/UL4.g:17:9: '%='
            pass 
            self.match("%=")




            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__26"



    # $ANTLR start "T__27"
    def mT__27(self, ):
        try:
            _type = T__27
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:18:7: ( '(' )
            # src/ll/UL4.g:18:9: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__27"



    # $ANTLR start "T__28"
    def mT__28(self, ):
        try:
            _type = T__28
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:19:7: ( ')' )
            # src/ll/UL4.g:19:9: ')'
            pass 
            self.match(41)



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

            # src/ll/UL4.g:20:7: ( '*' )
            # src/ll/UL4.g:20:9: '*'
            pass 
            self.match(42)



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

            # src/ll/UL4.g:21:7: ( '**' )
            # src/ll/UL4.g:21:9: '**'
            pass 
            self.match("**")




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

            # src/ll/UL4.g:22:7: ( '*=' )
            # src/ll/UL4.g:22:9: '*='
            pass 
            self.match("*=")




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

            # src/ll/UL4.g:23:7: ( '+' )
            # src/ll/UL4.g:23:9: '+'
            pass 
            self.match(43)



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

            # src/ll/UL4.g:24:7: ( '+=' )
            # src/ll/UL4.g:24:9: '+='
            pass 
            self.match("+=")




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

            # src/ll/UL4.g:25:7: ( ',' )
            # src/ll/UL4.g:25:9: ','
            pass 
            self.match(44)



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

            # src/ll/UL4.g:26:7: ( '-' )
            # src/ll/UL4.g:26:9: '-'
            pass 
            self.match(45)



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

            # src/ll/UL4.g:27:7: ( '-=' )
            # src/ll/UL4.g:27:9: '-='
            pass 
            self.match("-=")




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

            # src/ll/UL4.g:28:7: ( '.' )
            # src/ll/UL4.g:28:9: '.'
            pass 
            self.match(46)



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

            # src/ll/UL4.g:29:7: ( '/' )
            # src/ll/UL4.g:29:9: '/'
            pass 
            self.match(47)



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

            # src/ll/UL4.g:30:7: ( '//' )
            # src/ll/UL4.g:30:9: '//'
            pass 
            self.match("//")




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

            # src/ll/UL4.g:31:7: ( '//=' )
            # src/ll/UL4.g:31:9: '//='
            pass 
            self.match("//=")




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

            # src/ll/UL4.g:32:7: ( '/=' )
            # src/ll/UL4.g:32:9: '/='
            pass 
            self.match("/=")




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

            # src/ll/UL4.g:33:7: ( ':' )
            # src/ll/UL4.g:33:9: ':'
            pass 
            self.match(58)



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

            # src/ll/UL4.g:34:7: ( '<' )
            # src/ll/UL4.g:34:9: '<'
            pass 
            self.match(60)



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

            # src/ll/UL4.g:35:7: ( '<=' )
            # src/ll/UL4.g:35:9: '<='
            pass 
            self.match("<=")




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

            # src/ll/UL4.g:36:7: ( '=' )
            # src/ll/UL4.g:36:9: '='
            pass 
            self.match(61)



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

            # src/ll/UL4.g:37:7: ( '==' )
            # src/ll/UL4.g:37:9: '=='
            pass 
            self.match("==")




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

            # src/ll/UL4.g:38:7: ( '>' )
            # src/ll/UL4.g:38:9: '>'
            pass 
            self.match(62)



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

            # src/ll/UL4.g:39:7: ( '>=' )
            # src/ll/UL4.g:39:9: '>='
            pass 
            self.match(">=")




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

            # src/ll/UL4.g:40:7: ( '[' )
            # src/ll/UL4.g:40:9: '['
            pass 
            self.match(91)



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

            # src/ll/UL4.g:41:7: ( ']' )
            # src/ll/UL4.g:41:9: ']'
            pass 
            self.match(93)



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

            # src/ll/UL4.g:42:7: ( 'and' )
            # src/ll/UL4.g:42:9: 'and'
            pass 
            self.match("and")




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

            # src/ll/UL4.g:43:7: ( 'for' )
            # src/ll/UL4.g:43:9: 'for'
            pass 
            self.match("for")




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

            # src/ll/UL4.g:44:7: ( 'if' )
            # src/ll/UL4.g:44:9: 'if'
            pass 
            self.match("if")




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

            # src/ll/UL4.g:45:7: ( 'in' )
            # src/ll/UL4.g:45:9: 'in'
            pass 
            self.match("in")




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

            # src/ll/UL4.g:46:7: ( 'not' )
            # src/ll/UL4.g:46:9: 'not'
            pass 
            self.match("not")




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

            # src/ll/UL4.g:47:7: ( 'or' )
            # src/ll/UL4.g:47:9: 'or'
            pass 
            self.match("or")




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

            # src/ll/UL4.g:48:7: ( '{' )
            # src/ll/UL4.g:48:9: '{'
            pass 
            self.match(123)



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

            # src/ll/UL4.g:49:7: ( '}' )
            # src/ll/UL4.g:49:9: '}'
            pass 
            self.match(125)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "T__58"



    # $ANTLR start "NONE"
    def mNONE(self, ):
        try:
            _type = NONE
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:39:2: ( 'None' )
            # src/ll/UL4.g:39:4: 'None'
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

            # src/ll/UL4.g:43:2: ( 'True' )
            # src/ll/UL4.g:43:4: 'True'
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

            # src/ll/UL4.g:47:2: ( 'False' )
            # src/ll/UL4.g:47:4: 'False'
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

            # src/ll/UL4.g:51:2: ( ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )* )
            # src/ll/UL4.g:51:4: ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
            pass 
            if (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            # src/ll/UL4.g:51:28: ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
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
            # src/ll/UL4.g:57:2: ( '0' .. '9' )
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
            # src/ll/UL4.g:62:2: ( ( '0' | '1' ) )
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
            # src/ll/UL4.g:67:2: ( '0' .. '7' )
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
            # src/ll/UL4.g:72:2: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
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

            # src/ll/UL4.g:76:2: ( ( DIGIT )+ | '0' ( 'b' | 'B' ) ( BIN_DIGIT )+ | '0' ( 'o' | 'O' ) ( OCT_DIGIT )+ | '0' ( 'x' | 'X' ) ( HEX_DIGIT )+ )
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
                # src/ll/UL4.g:76:4: ( DIGIT )+
                pass 
                # src/ll/UL4.g:76:4: ( DIGIT )+
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
                # src/ll/UL4.g:77:4: '0' ( 'b' | 'B' ) ( BIN_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 66 or self.input.LA(1) == 98:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:77:18: ( BIN_DIGIT )+
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
                # src/ll/UL4.g:78:4: '0' ( 'o' | 'O' ) ( OCT_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 79 or self.input.LA(1) == 111:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:78:18: ( OCT_DIGIT )+
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
                # src/ll/UL4.g:79:4: '0' ( 'x' | 'X' ) ( HEX_DIGIT )+
                pass 
                self.match(48)

                if self.input.LA(1) == 88 or self.input.LA(1) == 120:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



                # src/ll/UL4.g:79:18: ( HEX_DIGIT )+
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
            # src/ll/UL4.g:85:2: ( ( 'e' | 'E' ) ( '+' | '-' )? ( DIGIT )+ )
            # src/ll/UL4.g:85:4: ( 'e' | 'E' ) ( '+' | '-' )? ( DIGIT )+
            pass 
            if self.input.LA(1) == 69 or self.input.LA(1) == 101:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse



            # src/ll/UL4.g:85:14: ( '+' | '-' )?
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






            # src/ll/UL4.g:85:25: ( DIGIT )+
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

            # src/ll/UL4.g:88:2: ( ( DIGIT )+ '.' ( DIGIT )* ( EXPONENT )? | '.' ( DIGIT )+ ( EXPONENT )? | ( DIGIT )+ EXPONENT )
            alt15 = 3
            alt15 = self.dfa15.predict(self.input)
            if alt15 == 1:
                # src/ll/UL4.g:88:4: ( DIGIT )+ '.' ( DIGIT )* ( EXPONENT )?
                pass 
                # src/ll/UL4.g:88:4: ( DIGIT )+
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

                # src/ll/UL4.g:88:15: ( DIGIT )*
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


                # src/ll/UL4.g:88:22: ( EXPONENT )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 69 or LA11_0 == 101) :
                    alt11 = 1
                if alt11 == 1:
                    # src/ll/UL4.g:88:22: EXPONENT
                    pass 
                    self.mEXPONENT()






            elif alt15 == 2:
                # src/ll/UL4.g:89:4: '.' ( DIGIT )+ ( EXPONENT )?
                pass 
                self.match(46)

                # src/ll/UL4.g:89:8: ( DIGIT )+
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


                # src/ll/UL4.g:89:15: ( EXPONENT )?
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if (LA13_0 == 69 or LA13_0 == 101) :
                    alt13 = 1
                if alt13 == 1:
                    # src/ll/UL4.g:89:15: EXPONENT
                    pass 
                    self.mEXPONENT()






            elif alt15 == 3:
                # src/ll/UL4.g:90:4: ( DIGIT )+ EXPONENT
                pass 
                # src/ll/UL4.g:90:4: ( DIGIT )+
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
            # src/ll/UL4.g:96:2: ( DIGIT DIGIT ':' DIGIT DIGIT ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )? )
            # src/ll/UL4.g:96:4: DIGIT DIGIT ':' DIGIT DIGIT ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )?
            pass 
            self.mDIGIT()


            self.mDIGIT()


            self.match(58)

            self.mDIGIT()


            self.mDIGIT()


            # src/ll/UL4.g:96:32: ( ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )? )?
            alt17 = 2
            LA17_0 = self.input.LA(1)

            if (LA17_0 == 58) :
                alt17 = 1
            if alt17 == 1:
                # src/ll/UL4.g:96:34: ':' DIGIT DIGIT ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )?
                pass 
                self.match(58)

                self.mDIGIT()


                self.mDIGIT()


                # src/ll/UL4.g:96:50: ( '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT )?
                alt16 = 2
                LA16_0 = self.input.LA(1)

                if (LA16_0 == 46) :
                    alt16 = 1
                if alt16 == 1:
                    # src/ll/UL4.g:96:52: '.' DIGIT DIGIT DIGIT DIGIT DIGIT DIGIT
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

            # src/ll/UL4.g:98:2: ( '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ( 'T' ( TIME )? )? ')' )
            # src/ll/UL4.g:98:4: '@' '(' DIGIT DIGIT DIGIT DIGIT '-' DIGIT DIGIT '-' DIGIT DIGIT ( 'T' ( TIME )? )? ')'
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


            # src/ll/UL4.g:98:68: ( 'T' ( TIME )? )?
            alt19 = 2
            LA19_0 = self.input.LA(1)

            if (LA19_0 == 84) :
                alt19 = 1
            if alt19 == 1:
                # src/ll/UL4.g:98:69: 'T' ( TIME )?
                pass 
                self.match(84)

                # src/ll/UL4.g:98:73: ( TIME )?
                alt18 = 2
                LA18_0 = self.input.LA(1)

                if ((48 <= LA18_0 <= 57)) :
                    alt18 = 1
                if alt18 == 1:
                    # src/ll/UL4.g:98:73: TIME
                    pass 
                    self.mTIME()








            self.match(41)



            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "DATE"



    # $ANTLR start "COLOR"
    def mCOLOR(self, ):
        try:
            _type = COLOR
            _channel = DEFAULT_CHANNEL

            # src/ll/UL4.g:101:2: ( '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            alt20 = 4
            LA20_0 = self.input.LA(1)

            if (LA20_0 == 35) :
                LA20_1 = self.input.LA(2)

                if ((48 <= LA20_1 <= 57) or (65 <= LA20_1 <= 70) or (97 <= LA20_1 <= 102)) :
                    LA20_2 = self.input.LA(3)

                    if ((48 <= LA20_2 <= 57) or (65 <= LA20_2 <= 70) or (97 <= LA20_2 <= 102)) :
                        LA20_3 = self.input.LA(4)

                        if ((48 <= LA20_3 <= 57) or (65 <= LA20_3 <= 70) or (97 <= LA20_3 <= 102)) :
                            LA20_4 = self.input.LA(5)

                            if ((48 <= LA20_4 <= 57) or (65 <= LA20_4 <= 70) or (97 <= LA20_4 <= 102)) :
                                LA20_6 = self.input.LA(6)

                                if ((48 <= LA20_6 <= 57) or (65 <= LA20_6 <= 70) or (97 <= LA20_6 <= 102)) :
                                    LA20_8 = self.input.LA(7)

                                    if ((48 <= LA20_8 <= 57) or (65 <= LA20_8 <= 70) or (97 <= LA20_8 <= 102)) :
                                        LA20_9 = self.input.LA(8)

                                        if ((48 <= LA20_9 <= 57) or (65 <= LA20_9 <= 70) or (97 <= LA20_9 <= 102)) :
                                            alt20 = 4
                                        else:
                                            alt20 = 3

                                    else:
                                        nvae = NoViableAltException("", 20, 8, self.input)

                                        raise nvae


                                else:
                                    alt20 = 2

                            else:
                                alt20 = 1

                        else:
                            nvae = NoViableAltException("", 20, 3, self.input)

                            raise nvae


                    else:
                        nvae = NoViableAltException("", 20, 2, self.input)

                        raise nvae


                else:
                    nvae = NoViableAltException("", 20, 1, self.input)

                    raise nvae


            else:
                nvae = NoViableAltException("", 20, 0, self.input)

                raise nvae


            if alt20 == 1:
                # src/ll/UL4.g:101:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt20 == 2:
                # src/ll/UL4.g:102:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt20 == 3:
                # src/ll/UL4.g:103:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
                pass 
                self.match(35)

                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()


                self.mHEX_DIGIT()



            elif alt20 == 4:
                # src/ll/UL4.g:104:4: '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
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

            # src/ll/UL4.g:108:2: ( ( ' ' | '\\t' | '\\r' | '\\n' ) )
            # src/ll/UL4.g:108:4: ( ' ' | '\\t' | '\\r' | '\\n' )
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

            # src/ll/UL4.g:112:2: ( '\"' ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )* '\"' | '\\'' ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )* '\\'' )
            alt23 = 2
            LA23_0 = self.input.LA(1)

            if (LA23_0 == 34) :
                alt23 = 1
            elif (LA23_0 == 39) :
                alt23 = 2
            else:
                nvae = NoViableAltException("", 23, 0, self.input)

                raise nvae


            if alt23 == 1:
                # src/ll/UL4.g:112:4: '\"' ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )* '\"'
                pass 
                self.match(34)

                # src/ll/UL4.g:112:8: ( ESC_SEQ |~ ( '\\\\' | '\"' | '\\r' | '\\n' ) )*
                while True: #loop21
                    alt21 = 3
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == 92) :
                        alt21 = 1
                    elif ((0 <= LA21_0 <= 9) or (11 <= LA21_0 <= 12) or (14 <= LA21_0 <= 33) or (35 <= LA21_0 <= 91) or (93 <= LA21_0 <= 65535)) :
                        alt21 = 2


                    if alt21 == 1:
                        # src/ll/UL4.g:112:10: ESC_SEQ
                        pass 
                        self.mESC_SEQ()



                    elif alt21 == 2:
                        # src/ll/UL4.g:112:20: ~ ( '\\\\' | '\"' | '\\r' | '\\n' )
                        pass 
                        if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 33) or (35 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        break #loop21


                self.match(34)


            elif alt23 == 2:
                # src/ll/UL4.g:113:4: '\\'' ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )* '\\''
                pass 
                self.match(39)

                # src/ll/UL4.g:113:9: ( ESC_SEQ |~ ( '\\\\' | '\\'' | '\\r' | '\\n' ) )*
                while True: #loop22
                    alt22 = 3
                    LA22_0 = self.input.LA(1)

                    if (LA22_0 == 92) :
                        alt22 = 1
                    elif ((0 <= LA22_0 <= 9) or (11 <= LA22_0 <= 12) or (14 <= LA22_0 <= 38) or (40 <= LA22_0 <= 91) or (93 <= LA22_0 <= 65535)) :
                        alt22 = 2


                    if alt22 == 1:
                        # src/ll/UL4.g:113:11: ESC_SEQ
                        pass 
                        self.mESC_SEQ()



                    elif alt22 == 2:
                        # src/ll/UL4.g:113:21: ~ ( '\\\\' | '\\'' | '\\r' | '\\n' )
                        pass 
                        if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 38) or (40 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse




                    else:
                        break #loop22


                self.match(39)


            self._state.type = _type
            self._state.channel = _channel
        finally:
            pass

    # $ANTLR end "STRING"



    # $ANTLR start "ESC_SEQ"
    def mESC_SEQ(self, ):
        try:
            # src/ll/UL4.g:119:2: ( '\\\\' ( 'a' | 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | UNICODE1_ESC | UNICODE2_ESC | UNICODE4_ESC )
            alt24 = 4
            LA24_0 = self.input.LA(1)

            if (LA24_0 == 92) :
                LA24 = self.input.LA(2)
                if LA24 == 34 or LA24 == 39 or LA24 == 92 or LA24 == 97 or LA24 == 98 or LA24 == 102 or LA24 == 110 or LA24 == 114 or LA24 == 116:
                    alt24 = 1
                elif LA24 == 120:
                    alt24 = 2
                elif LA24 == 117:
                    alt24 = 3
                elif LA24 == 85:
                    alt24 = 4
                else:
                    nvae = NoViableAltException("", 24, 1, self.input)

                    raise nvae


            else:
                nvae = NoViableAltException("", 24, 0, self.input)

                raise nvae


            if alt24 == 1:
                # src/ll/UL4.g:119:4: '\\\\' ( 'a' | 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
                pass 
                self.match(92)

                if self.input.LA(1) == 34 or self.input.LA(1) == 39 or self.input.LA(1) == 92 or (97 <= self.input.LA(1) <= 98) or self.input.LA(1) == 102 or self.input.LA(1) == 110 or self.input.LA(1) == 114 or self.input.LA(1) == 116:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse




            elif alt24 == 2:
                # src/ll/UL4.g:120:4: UNICODE1_ESC
                pass 
                self.mUNICODE1_ESC()



            elif alt24 == 3:
                # src/ll/UL4.g:121:4: UNICODE2_ESC
                pass 
                self.mUNICODE2_ESC()



            elif alt24 == 4:
                # src/ll/UL4.g:122:4: UNICODE4_ESC
                pass 
                self.mUNICODE4_ESC()




        finally:
            pass

    # $ANTLR end "ESC_SEQ"



    # $ANTLR start "UNICODE1_ESC"
    def mUNICODE1_ESC(self, ):
        try:
            # src/ll/UL4.g:127:2: ( '\\\\' 'x' HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:127:4: '\\\\' 'x' HEX_DIGIT HEX_DIGIT
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
            # src/ll/UL4.g:132:2: ( '\\\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:132:4: '\\\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
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
            # src/ll/UL4.g:137:2: ( '\\\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT )
            # src/ll/UL4.g:137:4: '\\\\' 'U' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
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
        # src/ll/UL4.g:1:8: ( T__24 | T__25 | T__26 | T__27 | T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | T__52 | T__53 | T__54 | T__55 | T__56 | T__57 | T__58 | NONE | TRUE | FALSE | NAME | INT | FLOAT | DATE | COLOR | WS | STRING )
        alt25 = 45
        alt25 = self.dfa25.predict(self.input)
        if alt25 == 1:
            # src/ll/UL4.g:1:10: T__24
            pass 
            self.mT__24()



        elif alt25 == 2:
            # src/ll/UL4.g:1:16: T__25
            pass 
            self.mT__25()



        elif alt25 == 3:
            # src/ll/UL4.g:1:22: T__26
            pass 
            self.mT__26()



        elif alt25 == 4:
            # src/ll/UL4.g:1:28: T__27
            pass 
            self.mT__27()



        elif alt25 == 5:
            # src/ll/UL4.g:1:34: T__28
            pass 
            self.mT__28()



        elif alt25 == 6:
            # src/ll/UL4.g:1:40: T__29
            pass 
            self.mT__29()



        elif alt25 == 7:
            # src/ll/UL4.g:1:46: T__30
            pass 
            self.mT__30()



        elif alt25 == 8:
            # src/ll/UL4.g:1:52: T__31
            pass 
            self.mT__31()



        elif alt25 == 9:
            # src/ll/UL4.g:1:58: T__32
            pass 
            self.mT__32()



        elif alt25 == 10:
            # src/ll/UL4.g:1:64: T__33
            pass 
            self.mT__33()



        elif alt25 == 11:
            # src/ll/UL4.g:1:70: T__34
            pass 
            self.mT__34()



        elif alt25 == 12:
            # src/ll/UL4.g:1:76: T__35
            pass 
            self.mT__35()



        elif alt25 == 13:
            # src/ll/UL4.g:1:82: T__36
            pass 
            self.mT__36()



        elif alt25 == 14:
            # src/ll/UL4.g:1:88: T__37
            pass 
            self.mT__37()



        elif alt25 == 15:
            # src/ll/UL4.g:1:94: T__38
            pass 
            self.mT__38()



        elif alt25 == 16:
            # src/ll/UL4.g:1:100: T__39
            pass 
            self.mT__39()



        elif alt25 == 17:
            # src/ll/UL4.g:1:106: T__40
            pass 
            self.mT__40()



        elif alt25 == 18:
            # src/ll/UL4.g:1:112: T__41
            pass 
            self.mT__41()



        elif alt25 == 19:
            # src/ll/UL4.g:1:118: T__42
            pass 
            self.mT__42()



        elif alt25 == 20:
            # src/ll/UL4.g:1:124: T__43
            pass 
            self.mT__43()



        elif alt25 == 21:
            # src/ll/UL4.g:1:130: T__44
            pass 
            self.mT__44()



        elif alt25 == 22:
            # src/ll/UL4.g:1:136: T__45
            pass 
            self.mT__45()



        elif alt25 == 23:
            # src/ll/UL4.g:1:142: T__46
            pass 
            self.mT__46()



        elif alt25 == 24:
            # src/ll/UL4.g:1:148: T__47
            pass 
            self.mT__47()



        elif alt25 == 25:
            # src/ll/UL4.g:1:154: T__48
            pass 
            self.mT__48()



        elif alt25 == 26:
            # src/ll/UL4.g:1:160: T__49
            pass 
            self.mT__49()



        elif alt25 == 27:
            # src/ll/UL4.g:1:166: T__50
            pass 
            self.mT__50()



        elif alt25 == 28:
            # src/ll/UL4.g:1:172: T__51
            pass 
            self.mT__51()



        elif alt25 == 29:
            # src/ll/UL4.g:1:178: T__52
            pass 
            self.mT__52()



        elif alt25 == 30:
            # src/ll/UL4.g:1:184: T__53
            pass 
            self.mT__53()



        elif alt25 == 31:
            # src/ll/UL4.g:1:190: T__54
            pass 
            self.mT__54()



        elif alt25 == 32:
            # src/ll/UL4.g:1:196: T__55
            pass 
            self.mT__55()



        elif alt25 == 33:
            # src/ll/UL4.g:1:202: T__56
            pass 
            self.mT__56()



        elif alt25 == 34:
            # src/ll/UL4.g:1:208: T__57
            pass 
            self.mT__57()



        elif alt25 == 35:
            # src/ll/UL4.g:1:214: T__58
            pass 
            self.mT__58()



        elif alt25 == 36:
            # src/ll/UL4.g:1:220: NONE
            pass 
            self.mNONE()



        elif alt25 == 37:
            # src/ll/UL4.g:1:225: TRUE
            pass 
            self.mTRUE()



        elif alt25 == 38:
            # src/ll/UL4.g:1:230: FALSE
            pass 
            self.mFALSE()



        elif alt25 == 39:
            # src/ll/UL4.g:1:236: NAME
            pass 
            self.mNAME()



        elif alt25 == 40:
            # src/ll/UL4.g:1:241: INT
            pass 
            self.mINT()



        elif alt25 == 41:
            # src/ll/UL4.g:1:245: FLOAT
            pass 
            self.mFLOAT()



        elif alt25 == 42:
            # src/ll/UL4.g:1:251: DATE
            pass 
            self.mDATE()



        elif alt25 == 43:
            # src/ll/UL4.g:1:256: COLOR
            pass 
            self.mCOLOR()



        elif alt25 == 44:
            # src/ll/UL4.g:1:262: WS
            pass 
            self.mWS()



        elif alt25 == 45:
            # src/ll/UL4.g:1:265: STRING
            pass 
            self.mSTRING()








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


    # lookup tables for DFA #25

    DFA25_eot = DFA.unpack(
        "\2\uffff\1\43\2\uffff\1\46\1\50\1\uffff\1\52\1\53\1\57\1\uffff"
        "\1\61\1\63\1\65\2\uffff\5\33\2\uffff\3\33\1\uffff\2\77\17\uffff"
        "\1\101\10\uffff\2\33\1\104\1\105\1\33\1\107\3\33\3\uffff\1\113"
        "\1\114\2\uffff\1\115\1\uffff\3\33\3\uffff\1\121\1\122\1\33\2\uffff"
        "\1\124\1\uffff"
        )

    DFA25_eof = DFA.unpack(
        "\125\uffff"
        )

    DFA25_min = DFA.unpack(
        "\1\11\1\uffff\1\75\2\uffff\1\52\1\75\1\uffff\1\75\1\60\1\57\1\uffff"
        "\3\75\2\uffff\1\156\1\157\1\146\1\157\1\162\2\uffff\1\157\1\162"
        "\1\141\1\uffff\2\56\17\uffff\1\75\10\uffff\1\144\1\162\2\60\1\164"
        "\1\60\1\156\1\165\1\154\3\uffff\2\60\2\uffff\1\60\1\uffff\2\145"
        "\1\163\3\uffff\2\60\1\145\2\uffff\1\60\1\uffff"
        )

    DFA25_max = DFA.unpack(
        "\1\175\1\uffff\1\75\2\uffff\2\75\1\uffff\1\75\1\71\1\75\1\uffff"
        "\3\75\2\uffff\1\156\1\157\1\156\1\157\1\162\2\uffff\1\157\1\162"
        "\1\141\1\uffff\2\145\17\uffff\1\75\10\uffff\1\144\1\162\2\172\1"
        "\164\1\172\1\156\1\165\1\154\3\uffff\2\172\2\uffff\1\172\1\uffff"
        "\2\145\1\163\3\uffff\2\172\1\145\2\uffff\1\172\1\uffff"
        )

    DFA25_accept = DFA.unpack(
        "\1\uffff\1\1\1\uffff\1\4\1\5\2\uffff\1\13\3\uffff\1\23\3\uffff"
        "\1\32\1\33\5\uffff\1\42\1\43\3\uffff\1\47\2\uffff\1\52\1\53\1\54"
        "\1\55\1\3\1\2\1\7\1\10\1\6\1\12\1\11\1\15\1\14\1\16\1\51\1\uffff"
        "\1\22\1\17\1\25\1\24\1\27\1\26\1\31\1\30\11\uffff\1\50\1\21\1\20"
        "\2\uffff\1\36\1\37\1\uffff\1\41\3\uffff\1\34\1\35\1\40\3\uffff"
        "\1\44\1\45\1\uffff\1\46"
        )

    DFA25_special = DFA.unpack(
        "\125\uffff"
        )


    DFA25_transition = [
        DFA.unpack("\2\40\2\uffff\1\40\22\uffff\1\40\1\1\1\41\1\37\1\uffff"
        "\1\2\1\uffff\1\41\1\3\1\4\1\5\1\6\1\7\1\10\1\11\1\12\1\34\11\35"
        "\1\13\1\uffff\1\14\1\15\1\16\1\uffff\1\36\5\33\1\32\7\33\1\30\5"
        "\33\1\31\6\33\1\17\1\uffff\1\20\1\uffff\1\33\1\uffff\1\21\4\33"
        "\1\22\2\33\1\23\4\33\1\24\1\25\13\33\1\26\1\uffff\1\27"),
        DFA.unpack(""),
        DFA.unpack("\1\42"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\44\22\uffff\1\45"),
        DFA.unpack("\1\47"),
        DFA.unpack(""),
        DFA.unpack("\1\51"),
        DFA.unpack("\12\54"),
        DFA.unpack("\1\55\15\uffff\1\56"),
        DFA.unpack(""),
        DFA.unpack("\1\60"),
        DFA.unpack("\1\62"),
        DFA.unpack("\1\64"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\66"),
        DFA.unpack("\1\67"),
        DFA.unpack("\1\70\7\uffff\1\71"),
        DFA.unpack("\1\72"),
        DFA.unpack("\1\73"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\74"),
        DFA.unpack("\1\75"),
        DFA.unpack("\1\76"),
        DFA.unpack(""),
        DFA.unpack("\1\54\1\uffff\12\35\13\uffff\1\54\37\uffff\1\54"),
        DFA.unpack("\1\54\1\uffff\12\35\13\uffff\1\54\37\uffff\1\54"),
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
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\100"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\1\102"),
        DFA.unpack("\1\103"),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\1\106"),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\1\110"),
        DFA.unpack("\1\111"),
        DFA.unpack("\1\112"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack(""),
        DFA.unpack("\1\116"),
        DFA.unpack("\1\117"),
        DFA.unpack("\1\120"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("\1\123"),
        DFA.unpack(""),
        DFA.unpack(""),
        DFA.unpack("\12\33\7\uffff\32\33\4\uffff\1\33\1\uffff\32\33"),
        DFA.unpack("")
    ]

    # class definition for DFA #25

    class DFA25(DFA):
        pass


 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(UL4Lexer)

    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)



if __name__ == '__main__':
    main(sys.argv)
