# Generated from src/ll/UL4Parser.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3[")
        buf.write("\u0321\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\3\2\5\2J\n")
        buf.write("\2\3\2\7\2M\n\2\f\2\16\2P\13\2\3\3\3\3\5\3T\n\3\3\3\3")
        buf.write("\3\5\3X\n\3\3\3\5\3[\n\3\3\3\5\3^\n\3\3\3\3\3\3\4\3\4")
        buf.write("\5\4d\n\4\3\4\3\4\5\4h\n\4\3\4\3\4\5\4l\n\4\3\4\3\4\3")
        buf.write("\5\3\5\5\5r\n\5\3\5\3\5\5\5v\n\5\3\5\3\5\3\6\3\6\5\6|")
        buf.write("\n\6\3\6\3\6\5\6\u0080\n\6\3\6\3\6\3\7\3\7\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u0091\n\b\3\t\3\t")
        buf.write("\3\t\5\t\u0096\n\t\3\n\3\n\3\n\3\n\3\n\3\n\7\n\u009e\n")
        buf.write("\n\f\n\16\n\u00a1\13\n\3\n\5\n\u00a4\n\n\3\n\3\n\5\n\u00a8")
        buf.write("\n\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\13\5\13\u00b2")
        buf.write("\n\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\7\f\u00bd")
        buf.write("\n\f\f\f\16\f\u00c0\13\f\3\f\5\f\u00c3\n\f\3\f\3\f\5\f")
        buf.write("\u00c7\n\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r\5\r\u00d1\n")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u00db\n")
        buf.write("\16\3\17\3\17\3\17\3\17\3\17\3\17\7\17\u00e3\n\17\f\17")
        buf.write("\16\17\u00e6\13\17\3\17\5\17\u00e9\n\17\3\17\3\17\5\17")
        buf.write("\u00ed\n\17\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3")
        buf.write("\20\3\20\5\20\u00f9\n\20\3\20\3\20\3\21\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\5\21\u0104\n\21\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\5\22\u0115\n\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3")
        buf.write("\23\3\23\3\23\3\23\3\23\7\23\u0123\n\23\f\23\16\23\u0126")
        buf.write("\13\23\3\23\5\23\u0129\n\23\3\23\3\23\5\23\u012d\n\23")
        buf.write("\3\24\5\24\u0130\n\24\3\24\3\24\5\24\u0134\n\24\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u013f\n\25")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\5\26\u0149\n")
        buf.write("\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\7\26\u01a0")
        buf.write("\n\26\f\26\16\26\u01a3\13\26\3\26\5\26\u01a6\n\26\7\26")
        buf.write("\u01a8\n\26\f\26\16\26\u01ab\13\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\7\26\u01b8\n\26\f")
        buf.write("\26\16\26\u01bb\13\26\3\27\3\27\5\27\u01bf\n\27\3\30\3")
        buf.write("\30\3\30\3\30\3\30\3\30\5\30\u01c7\n\30\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\5\32")
        buf.write("\u020d\n\32\3\33\3\33\3\33\3\33\3\33\3\33\5\33\u0215\n")
        buf.write("\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\5\33\u021f")
        buf.write("\n\33\3\33\5\33\u0222\n\33\3\33\3\33\3\33\3\33\3\33\3")
        buf.write("\33\3\33\3\33\3\33\3\33\3\33\7\33\u022f\n\33\f\33\16\33")
        buf.write("\u0232\13\33\3\33\3\33\3\33\5\33\u0237\n\33\3\33\3\33")
        buf.write("\3\33\5\33\u023c\n\33\3\33\5\33\u023f\n\33\3\33\3\33\3")
        buf.write("\33\3\33\3\33\3\33\7\33\u0247\n\33\f\33\16\33\u024a\13")
        buf.write("\33\3\33\3\33\3\33\3\33\3\33\7\33\u0251\n\33\f\33\16\33")
        buf.write("\u0254\13\33\3\33\3\33\3\33\5\33\u0259\n\33\3\33\3\33")
        buf.write("\3\33\5\33\u025e\n\33\3\33\5\33\u0261\n\33\3\33\3\33\5")
        buf.write("\33\u0265\n\33\3\34\5\34\u0268\n\34\3\34\5\34\u026b\n")
        buf.write("\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\7\35\u0274\n\35")
        buf.write("\f\35\16\35\u0277\13\35\3\35\3\35\3\35\5\35\u027c\n\35")
        buf.write("\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\7\36\u0287")
        buf.write("\n\36\f\36\16\36\u028a\13\36\3\36\3\36\3\36\5\36\u028f")
        buf.write("\n\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\7\37\u0298\n")
        buf.write("\37\f\37\16\37\u029b\13\37\3\37\3\37\3\37\5\37\u02a0\n")
        buf.write("\37\3\37\3\37\3 \3 \3 \3 \3 \7 \u02a9\n \f \16 \u02ac")
        buf.write("\13 \3 \3 \3 \3 \3 \7 \u02b3\n \f \16 \u02b6\13 \7 \u02b8")
        buf.write("\n \f \16 \u02bb\13 \3 \3 \3 \3 \7 \u02c1\n \f \16 \u02c4")
        buf.write("\13 \3 \3 \3 \5 \u02c9\n \3 \3 \3!\3!\3!\3!\3!\3!\3!\7")
        buf.write("!\u02d4\n!\f!\16!\u02d7\13!\3!\5!\u02da\n!\7!\u02dc\n")
        buf.write("!\f!\16!\u02df\13!\3!\3!\3!\7!\u02e4\n!\f!\16!\u02e7\13")
        buf.write("!\3!\3!\3!\5!\u02ec\n!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"\3")
        buf.write("\"\7\"\u02f7\n\"\f\"\16\"\u02fa\13\"\3\"\5\"\u02fd\n\"")
        buf.write("\7\"\u02ff\n\"\f\"\16\"\u0302\13\"\3\"\3\"\3\"\7\"\u0307")
        buf.write("\n\"\f\"\16\"\u030a\13\"\3\"\3\"\3\"\5\"\u030f\n\"\3\"")
        buf.write("\3\"\3#\3#\3#\3#\5#\u0317\n#\3$\3$\3$\3$\3$\3$\5$\u031f")
        buf.write("\n$\3$\2\3*%\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"")
        buf.write("$&(*,.\60\62\64\668:<>@BDF\2\3\4\2\5\5\7\7\2\u0393\2I")
        buf.write("\3\2\2\2\4Q\3\2\2\2\6a\3\2\2\2\bo\3\2\2\2\ny\3\2\2\2\f")
        buf.write("\u0083\3\2\2\2\16\u0090\3\2\2\2\20\u0095\3\2\2\2\22\u00a7")
        buf.write("\3\2\2\2\24\u00a9\3\2\2\2\26\u00c6\3\2\2\2\30\u00c8\3")
        buf.write("\2\2\2\32\u00da\3\2\2\2\34\u00ec\3\2\2\2\36\u00ee\3\2")
        buf.write("\2\2 \u00fc\3\2\2\2\"\u0114\3\2\2\2$\u012c\3\2\2\2&\u012f")
        buf.write("\3\2\2\2(\u013e\3\2\2\2*\u0148\3\2\2\2,\u01be\3\2\2\2")
        buf.write(".\u01c6\3\2\2\2\60\u01c8\3\2\2\2\62\u020c\3\2\2\2\64\u0264")
        buf.write("\3\2\2\2\66\u0267\3\2\2\28\u026e\3\2\2\2:\u027f\3\2\2")
        buf.write("\2<\u0292\3\2\2\2>\u02a3\3\2\2\2@\u02cc\3\2\2\2B\u02ef")
        buf.write("\3\2\2\2D\u0316\3\2\2\2F\u031e\3\2\2\2HJ\5\4\3\2IH\3\2")
        buf.write("\2\2IJ\3\2\2\2JN\3\2\2\2KM\5F$\2LK\3\2\2\2MP\3\2\2\2N")
        buf.write("L\3\2\2\2NO\3\2\2\2O\3\3\2\2\2PN\3\2\2\2QS\t\2\2\2RT\7")
        buf.write("\t\2\2SR\3\2\2\2ST\3\2\2\2TU\3\2\2\2UW\7\r\2\2VX\7\t\2")
        buf.write("\2WV\3\2\2\2WX\3\2\2\2XZ\3\2\2\2Y[\5\f\7\2ZY\3\2\2\2Z")
        buf.write("[\3\2\2\2[]\3\2\2\2\\^\5\64\33\2]\\\3\2\2\2]^\3\2\2\2")
        buf.write("^_\3\2\2\2_`\7\33\2\2`\5\3\2\2\2ac\t\2\2\2bd\7\t\2\2c")
        buf.write("b\3\2\2\2cd\3\2\2\2de\3\2\2\2eg\7\n\2\2fh\7\31\2\2gf\3")
        buf.write("\2\2\2gh\3\2\2\2hi\3\2\2\2ik\7\30\2\2jl\7\31\2\2kj\3\2")
        buf.write("\2\2kl\3\2\2\2lm\3\2\2\2mn\7\32\2\2n\7\3\2\2\2oq\t\2\2")
        buf.write("\2pr\7\t\2\2qp\3\2\2\2qr\3\2\2\2rs\3\2\2\2su\7\13\2\2")
        buf.write("tv\7\t\2\2ut\3\2\2\2uv\3\2\2\2vw\3\2\2\2wx\7\33\2\2x\t")
        buf.write("\3\2\2\2y{\t\2\2\2z|\7\t\2\2{z\3\2\2\2{|\3\2\2\2|}\3\2")
        buf.write("\2\2}\177\7\f\2\2~\u0080\7\t\2\2\177~\3\2\2\2\177\u0080")
        buf.write("\3\2\2\2\u0080\u0081\3\2\2\2\u0081\u0082\7\33\2\2\u0082")
        buf.write("\13\3\2\2\2\u0083\u0084\7S\2\2\u0084\r\3\2\2\2\u0085\u0091")
        buf.write("\7$\2\2\u0086\u0091\7&\2\2\u0087\u0091\7%\2\2\u0088\u0091")
        buf.write("\7T\2\2\u0089\u0091\7U\2\2\u008a\u0091\7Z\2\2\u008b\u0091")
        buf.write("\7[\2\2\u008c\u0091\7V\2\2\u008d\u0091\7W\2\2\u008e\u0091")
        buf.write("\7X\2\2\u008f\u0091\5\f\7\2\u0090\u0085\3\2\2\2\u0090")
        buf.write("\u0086\3\2\2\2\u0090\u0087\3\2\2\2\u0090\u0088\3\2\2\2")
        buf.write("\u0090\u0089\3\2\2\2\u0090\u008a\3\2\2\2\u0090\u008b\3")
        buf.write("\2\2\2\u0090\u008c\3\2\2\2\u0090\u008d\3\2\2\2\u0090\u008e")
        buf.write("\3\2\2\2\u0090\u008f\3\2\2\2\u0091\17\3\2\2\2\u0092\u0096")
        buf.write("\5*\26\2\u0093\u0094\7\62\2\2\u0094\u0096\5*\26\2\u0095")
        buf.write("\u0092\3\2\2\2\u0095\u0093\3\2\2\2\u0096\21\3\2\2\2\u0097")
        buf.write("\u0098\7-\2\2\u0098\u00a8\7.\2\2\u0099\u009a\7-\2\2\u009a")
        buf.write("\u009f\5\20\t\2\u009b\u009c\7?\2\2\u009c\u009e\5\20\t")
        buf.write("\2\u009d\u009b\3\2\2\2\u009e\u00a1\3\2\2\2\u009f\u009d")
        buf.write("\3\2\2\2\u009f\u00a0\3\2\2\2\u00a0\u00a3\3\2\2\2\u00a1")
        buf.write("\u009f\3\2\2\2\u00a2\u00a4\7?\2\2\u00a3\u00a2\3\2\2\2")
        buf.write("\u00a3\u00a4\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5\u00a6\7")
        buf.write(".\2\2\u00a6\u00a8\3\2\2\2\u00a7\u0097\3\2\2\2\u00a7\u0099")
        buf.write("\3\2\2\2\u00a8\23\3\2\2\2\u00a9\u00aa\7-\2\2\u00aa\u00ab")
        buf.write("\5*\26\2\u00ab\u00ac\7\34\2\2\u00ac\u00ad\5$\23\2\u00ad")
        buf.write("\u00ae\7\35\2\2\u00ae\u00b1\5*\26\2\u00af\u00b0\7\36\2")
        buf.write("\2\u00b0\u00b2\5*\26\2\u00b1\u00af\3\2\2\2\u00b1\u00b2")
        buf.write("\3\2\2\2\u00b2\u00b3\3\2\2\2\u00b3\u00b4\7.\2\2\u00b4")
        buf.write("\25\3\2\2\2\u00b5\u00b6\7/\2\2\u00b6\u00b7\7\66\2\2\u00b7")
        buf.write("\u00c7\7\60\2\2\u00b8\u00b9\7/\2\2\u00b9\u00be\5\20\t")
        buf.write("\2\u00ba\u00bb\7?\2\2\u00bb\u00bd\5\20\t\2\u00bc\u00ba")
        buf.write("\3\2\2\2\u00bd\u00c0\3\2\2\2\u00be\u00bc\3\2\2\2\u00be")
        buf.write("\u00bf\3\2\2\2\u00bf\u00c2\3\2\2\2\u00c0\u00be\3\2\2\2")
        buf.write("\u00c1\u00c3\7?\2\2\u00c2\u00c1\3\2\2\2\u00c2\u00c3\3")
        buf.write("\2\2\2\u00c3\u00c4\3\2\2\2\u00c4\u00c5\7\60\2\2\u00c5")
        buf.write("\u00c7\3\2\2\2\u00c6\u00b5\3\2\2\2\u00c6\u00b8\3\2\2\2")
        buf.write("\u00c7\27\3\2\2\2\u00c8\u00c9\7/\2\2\u00c9\u00ca\5*\26")
        buf.write("\2\u00ca\u00cb\7\34\2\2\u00cb\u00cc\5$\23\2\u00cc\u00cd")
        buf.write("\7\35\2\2\u00cd\u00d0\5*\26\2\u00ce\u00cf\7\36\2\2\u00cf")
        buf.write("\u00d1\5*\26\2\u00d0\u00ce\3\2\2\2\u00d0\u00d1\3\2\2\2")
        buf.write("\u00d1\u00d2\3\2\2\2\u00d2\u00d3\7\60\2\2\u00d3\31\3\2")
        buf.write("\2\2\u00d4\u00d5\5*\26\2\u00d5\u00d6\7@\2\2\u00d6\u00d7")
        buf.write("\5*\26\2\u00d7\u00db\3\2\2\2\u00d8\u00d9\7\61\2\2\u00d9")
        buf.write("\u00db\5*\26\2\u00da\u00d4\3\2\2\2\u00da\u00d8\3\2\2\2")
        buf.write("\u00db\33\3\2\2\2\u00dc\u00dd\7/\2\2\u00dd\u00ed\7\60")
        buf.write("\2\2\u00de\u00df\7/\2\2\u00df\u00e4\5\32\16\2\u00e0\u00e1")
        buf.write("\7?\2\2\u00e1\u00e3\5\32\16\2\u00e2\u00e0\3\2\2\2\u00e3")
        buf.write("\u00e6\3\2\2\2\u00e4\u00e2\3\2\2\2\u00e4\u00e5\3\2\2\2")
        buf.write("\u00e5\u00e8\3\2\2\2\u00e6\u00e4\3\2\2\2\u00e7\u00e9\7")
        buf.write("?\2\2\u00e8\u00e7\3\2\2\2\u00e8\u00e9\3\2\2\2\u00e9\u00ea")
        buf.write("\3\2\2\2\u00ea\u00eb\7\60\2\2\u00eb\u00ed\3\2\2\2\u00ec")
        buf.write("\u00dc\3\2\2\2\u00ec\u00de\3\2\2\2\u00ed\35\3\2\2\2\u00ee")
        buf.write("\u00ef\7/\2\2\u00ef\u00f0\5*\26\2\u00f0\u00f1\7@\2\2\u00f1")
        buf.write("\u00f2\5*\26\2\u00f2\u00f3\7\34\2\2\u00f3\u00f4\5$\23")
        buf.write("\2\u00f4\u00f5\7\35\2\2\u00f5\u00f8\5*\26\2\u00f6\u00f7")
        buf.write("\7\36\2\2\u00f7\u00f9\5*\26\2\u00f8\u00f6\3\2\2\2\u00f8")
        buf.write("\u00f9\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa\u00fb\7\60\2")
        buf.write("\2\u00fb\37\3\2\2\2\u00fc\u00fd\5*\26\2\u00fd\u00fe\7")
        buf.write("\34\2\2\u00fe\u00ff\5$\23\2\u00ff\u0100\7\35\2\2\u0100")
        buf.write("\u0103\5*\26\2\u0101\u0102\7\36\2\2\u0102\u0104\5*\26")
        buf.write("\2\u0103\u0101\3\2\2\2\u0103\u0104\3\2\2\2\u0104!\3\2")
        buf.write("\2\2\u0105\u0115\5\16\b\2\u0106\u0115\5\22\n\2\u0107\u0115")
        buf.write("\5\24\13\2\u0108\u0115\5\26\f\2\u0109\u0115\5\30\r\2\u010a")
        buf.write("\u0115\5\34\17\2\u010b\u0115\5\36\20\2\u010c\u010d\7+")
        buf.write("\2\2\u010d\u010e\5 \21\2\u010e\u010f\7,\2\2\u010f\u0115")
        buf.write("\3\2\2\2\u0110\u0111\7+\2\2\u0111\u0112\5*\26\2\u0112")
        buf.write("\u0113\7,\2\2\u0113\u0115\3\2\2\2\u0114\u0105\3\2\2\2")
        buf.write("\u0114\u0106\3\2\2\2\u0114\u0107\3\2\2\2\u0114\u0108\3")
        buf.write("\2\2\2\u0114\u0109\3\2\2\2\u0114\u010a\3\2\2\2\u0114\u010b")
        buf.write("\3\2\2\2\u0114\u010c\3\2\2\2\u0114\u0110\3\2\2\2\u0115")
        buf.write("#\3\2\2\2\u0116\u012d\5*\26\2\u0117\u0118\7+\2\2\u0118")
        buf.write("\u0119\5$\23\2\u0119\u011a\7?\2\2\u011a\u011b\7,\2\2\u011b")
        buf.write("\u012d\3\2\2\2\u011c\u011d\7+\2\2\u011d\u011e\5$\23\2")
        buf.write("\u011e\u011f\7?\2\2\u011f\u0124\5$\23\2\u0120\u0121\7")
        buf.write("?\2\2\u0121\u0123\5$\23\2\u0122\u0120\3\2\2\2\u0123\u0126")
        buf.write("\3\2\2\2\u0124\u0122\3\2\2\2\u0124\u0125\3\2\2\2\u0125")
        buf.write("\u0128\3\2\2\2\u0126\u0124\3\2\2\2\u0127\u0129\7?\2\2")
        buf.write("\u0128\u0127\3\2\2\2\u0128\u0129\3\2\2\2\u0129\u012a\3")
        buf.write("\2\2\2\u012a\u012b\7,\2\2\u012b\u012d\3\2\2\2\u012c\u0116")
        buf.write("\3\2\2\2\u012c\u0117\3\2\2\2\u012c\u011c\3\2\2\2\u012d")
        buf.write("%\3\2\2\2\u012e\u0130\5*\26\2\u012f\u012e\3\2\2\2\u012f")
        buf.write("\u0130\3\2\2\2\u0130\u0131\3\2\2\2\u0131\u0133\7@\2\2")
        buf.write("\u0132\u0134\5*\26\2\u0133\u0132\3\2\2\2\u0133\u0134\3")
        buf.write("\2\2\2\u0134\'\3\2\2\2\u0135\u013f\5,\27\2\u0136\u0137")
        buf.write("\5\f\7\2\u0137\u0138\7>\2\2\u0138\u0139\5,\27\2\u0139")
        buf.write("\u013f\3\2\2\2\u013a\u013b\7\62\2\2\u013b\u013f\5,\27")
        buf.write("\2\u013c\u013d\7\61\2\2\u013d\u013f\5,\27\2\u013e\u0135")
        buf.write("\3\2\2\2\u013e\u0136\3\2\2\2\u013e\u013a\3\2\2\2\u013e")
        buf.write("\u013c\3\2\2\2\u013f)\3\2\2\2\u0140\u0141\b\26\1\2\u0141")
        buf.write("\u0149\5\"\22\2\u0142\u0143\7\64\2\2\u0143\u0149\5*\26")
        buf.write("\35\u0144\u0145\7A\2\2\u0145\u0149\5*\26\34\u0146\u0147")
        buf.write("\7 \2\2\u0147\u0149\5*\26\6\u0148\u0140\3\2\2\2\u0148")
        buf.write("\u0142\3\2\2\2\u0148\u0144\3\2\2\2\u0148\u0146\3\2\2\2")
        buf.write("\u0149\u01b9\3\2\2\2\u014a\u014b\f\33\2\2\u014b\u014c")
        buf.write("\7\62\2\2\u014c\u01b8\5*\26\34\u014d\u014e\f\32\2\2\u014e")
        buf.write("\u014f\7\66\2\2\u014f\u01b8\5*\26\33\u0150\u0151\f\31")
        buf.write("\2\2\u0151\u0152\7\65\2\2\u0152\u01b8\5*\26\32\u0153\u0154")
        buf.write("\f\30\2\2\u0154\u0155\7\67\2\2\u0155\u01b8\5*\26\31\u0156")
        buf.write("\u0157\f\27\2\2\u0157\u0158\7\63\2\2\u0158\u01b8\5*\26")
        buf.write("\30\u0159\u015a\f\26\2\2\u015a\u015b\7\64\2\2\u015b\u01b8")
        buf.write("\5*\26\27\u015c\u015d\f\25\2\2\u015d\u015e\7E\2\2\u015e")
        buf.write("\u01b8\5*\26\26\u015f\u0160\f\24\2\2\u0160\u0161\7F\2")
        buf.write("\2\u0161\u01b8\5*\26\25\u0162\u0163\f\23\2\2\u0163\u0164")
        buf.write("\7B\2\2\u0164\u01b8\5*\26\24\u0165\u0166\f\22\2\2\u0166")
        buf.write("\u0167\7C\2\2\u0167\u01b8\5*\26\23\u0168\u0169\f\21\2")
        buf.write("\2\u0169\u016a\7G\2\2\u016a\u01b8\5*\26\22\u016b\u016c")
        buf.write("\f\20\2\2\u016c\u016d\78\2\2\u016d\u01b8\5*\26\21\u016e")
        buf.write("\u016f\f\17\2\2\u016f\u0170\79\2\2\u0170\u01b8\5*\26\20")
        buf.write("\u0171\u0172\f\16\2\2\u0172\u0173\7;\2\2\u0173\u01b8\5")
        buf.write("*\26\17\u0174\u0175\f\r\2\2\u0175\u0176\7:\2\2\u0176\u01b8")
        buf.write("\5*\26\16\u0177\u0178\f\f\2\2\u0178\u0179\7=\2\2\u0179")
        buf.write("\u01b8\5*\26\r\u017a\u017b\f\13\2\2\u017b\u017c\7<\2\2")
        buf.write("\u017c\u01b8\5*\26\f\u017d\u017e\f\n\2\2\u017e\u017f\7")
        buf.write("\35\2\2\u017f\u01b8\5*\26\13\u0180\u0181\f\t\2\2\u0181")
        buf.write("\u0182\7 \2\2\u0182\u0183\7\35\2\2\u0183\u01b8\5*\26\n")
        buf.write("\u0184\u0185\f\b\2\2\u0185\u0186\7!\2\2\u0186\u01b8\5")
        buf.write("*\26\t\u0187\u0188\f\7\2\2\u0188\u0189\7!\2\2\u0189\u018a")
        buf.write("\7 \2\2\u018a\u01b8\5*\26\b\u018b\u018c\f\5\2\2\u018c")
        buf.write("\u018d\7\"\2\2\u018d\u01b8\5*\26\6\u018e\u018f\f\4\2\2")
        buf.write("\u018f\u0190\7#\2\2\u0190\u01b8\5*\26\5\u0191\u0192\f")
        buf.write("\3\2\2\u0192\u0193\7\36\2\2\u0193\u0194\5*\26\2\u0194")
        buf.write("\u0195\7\37\2\2\u0195\u0196\5*\26\4\u0196\u01b8\3\2\2")
        buf.write("\2\u0197\u0198\f!\2\2\u0198\u0199\7D\2\2\u0199\u01b8\5")
        buf.write("\f\7\2\u019a\u019b\f \2\2\u019b\u01a9\7+\2\2\u019c\u01a1")
        buf.write("\5(\25\2\u019d\u019e\7?\2\2\u019e\u01a0\5(\25\2\u019f")
        buf.write("\u019d\3\2\2\2\u01a0\u01a3\3\2\2\2\u01a1\u019f\3\2\2\2")
        buf.write("\u01a1\u01a2\3\2\2\2\u01a2\u01a5\3\2\2\2\u01a3\u01a1\3")
        buf.write("\2\2\2\u01a4\u01a6\7?\2\2\u01a5\u01a4\3\2\2\2\u01a5\u01a6")
        buf.write("\3\2\2\2\u01a6\u01a8\3\2\2\2\u01a7\u019c\3\2\2\2\u01a8")
        buf.write("\u01ab\3\2\2\2\u01a9\u01a7\3\2\2\2\u01a9\u01aa\3\2\2\2")
        buf.write("\u01aa\u01ac\3\2\2\2\u01ab\u01a9\3\2\2\2\u01ac\u01b8\7")
        buf.write(",\2\2\u01ad\u01ae\f\37\2\2\u01ae\u01af\7-\2\2\u01af\u01b0")
        buf.write("\5*\26\2\u01b0\u01b1\7.\2\2\u01b1\u01b8\3\2\2\2\u01b2")
        buf.write("\u01b3\f\36\2\2\u01b3\u01b4\7-\2\2\u01b4\u01b5\5&\24\2")
        buf.write("\u01b5\u01b6\7.\2\2\u01b6\u01b8\3\2\2\2\u01b7\u014a\3")
        buf.write("\2\2\2\u01b7\u014d\3\2\2\2\u01b7\u0150\3\2\2\2\u01b7\u0153")
        buf.write("\3\2\2\2\u01b7\u0156\3\2\2\2\u01b7\u0159\3\2\2\2\u01b7")
        buf.write("\u015c\3\2\2\2\u01b7\u015f\3\2\2\2\u01b7\u0162\3\2\2\2")
        buf.write("\u01b7\u0165\3\2\2\2\u01b7\u0168\3\2\2\2\u01b7\u016b\3")
        buf.write("\2\2\2\u01b7\u016e\3\2\2\2\u01b7\u0171\3\2\2\2\u01b7\u0174")
        buf.write("\3\2\2\2\u01b7\u0177\3\2\2\2\u01b7\u017a\3\2\2\2\u01b7")
        buf.write("\u017d\3\2\2\2\u01b7\u0180\3\2\2\2\u01b7\u0184\3\2\2\2")
        buf.write("\u01b7\u0187\3\2\2\2\u01b7\u018b\3\2\2\2\u01b7\u018e\3")
        buf.write("\2\2\2\u01b7\u0191\3\2\2\2\u01b7\u0197\3\2\2\2\u01b7\u019a")
        buf.write("\3\2\2\2\u01b7\u01ad\3\2\2\2\u01b7\u01b2\3\2\2\2\u01b8")
        buf.write("\u01bb\3\2\2\2\u01b9\u01b7\3\2\2\2\u01b9\u01ba\3\2\2\2")
        buf.write("\u01ba+\3\2\2\2\u01bb\u01b9\3\2\2\2\u01bc\u01bf\5 \21")
        buf.write("\2\u01bd\u01bf\5*\26\2\u01be\u01bc\3\2\2\2\u01be\u01bd")
        buf.write("\3\2\2\2\u01bf-\3\2\2\2\u01c0\u01c1\5 \21\2\u01c1\u01c2")
        buf.write("\7\2\2\3\u01c2\u01c7\3\2\2\2\u01c3\u01c4\5*\26\2\u01c4")
        buf.write("\u01c5\7\2\2\3\u01c5\u01c7\3\2\2\2\u01c6\u01c0\3\2\2\2")
        buf.write("\u01c6\u01c3\3\2\2\2\u01c7/\3\2\2\2\u01c8\u01c9\5$\23")
        buf.write("\2\u01c9\u01ca\7\35\2\2\u01ca\u01cb\5*\26\2\u01cb\u01cc")
        buf.write("\7\2\2\3\u01cc\61\3\2\2\2\u01cd\u01ce\5$\23\2\u01ce\u01cf")
        buf.write("\7>\2\2\u01cf\u01d0\5*\26\2\u01d0\u01d1\7\2\2\3\u01d1")
        buf.write("\u020d\3\2\2\2\u01d2\u01d3\5*\26\2\u01d3\u01d4\7H\2\2")
        buf.write("\u01d4\u01d5\5*\26\2\u01d5\u01d6\7\2\2\3\u01d6\u020d\3")
        buf.write("\2\2\2\u01d7\u01d8\5*\26\2\u01d8\u01d9\7I\2\2\u01d9\u01da")
        buf.write("\5*\26\2\u01da\u01db\7\2\2\3\u01db\u020d\3\2\2\2\u01dc")
        buf.write("\u01dd\5*\26\2\u01dd\u01de\7J\2\2\u01de\u01df\5*\26\2")
        buf.write("\u01df\u01e0\7\2\2\3\u01e0\u020d\3\2\2\2\u01e1\u01e2\5")
        buf.write("*\26\2\u01e2\u01e3\7K\2\2\u01e3\u01e4\5*\26\2\u01e4\u01e5")
        buf.write("\7\2\2\3\u01e5\u020d\3\2\2\2\u01e6\u01e7\5*\26\2\u01e7")
        buf.write("\u01e8\7L\2\2\u01e8\u01e9\5*\26\2\u01e9\u01ea\7\2\2\3")
        buf.write("\u01ea\u020d\3\2\2\2\u01eb\u01ec\5*\26\2\u01ec\u01ed\7")
        buf.write("M\2\2\u01ed\u01ee\5*\26\2\u01ee\u01ef\7\2\2\3\u01ef\u020d")
        buf.write("\3\2\2\2\u01f0\u01f1\5*\26\2\u01f1\u01f2\7N\2\2\u01f2")
        buf.write("\u01f3\5*\26\2\u01f3\u01f4\7\2\2\3\u01f4\u020d\3\2\2\2")
        buf.write("\u01f5\u01f6\5*\26\2\u01f6\u01f7\7O\2\2\u01f7\u01f8\5")
        buf.write("*\26\2\u01f8\u01f9\7\2\2\3\u01f9\u020d\3\2\2\2\u01fa\u01fb")
        buf.write("\5*\26\2\u01fb\u01fc\7P\2\2\u01fc\u01fd\5*\26\2\u01fd")
        buf.write("\u01fe\7\2\2\3\u01fe\u020d\3\2\2\2\u01ff\u0200\5*\26\2")
        buf.write("\u0200\u0201\7Q\2\2\u0201\u0202\5*\26\2\u0202\u0203\7")
        buf.write("\2\2\3\u0203\u020d\3\2\2\2\u0204\u0205\5*\26\2\u0205\u0206")
        buf.write("\7R\2\2\u0206\u0207\5*\26\2\u0207\u0208\7\2\2\3\u0208")
        buf.write("\u020d\3\2\2\2\u0209\u020a\5.\30\2\u020a\u020b\7\2\2\3")
        buf.write("\u020b\u020d\3\2\2\2\u020c\u01cd\3\2\2\2\u020c\u01d2\3")
        buf.write("\2\2\2\u020c\u01d7\3\2\2\2\u020c\u01dc\3\2\2\2\u020c\u01e1")
        buf.write("\3\2\2\2\u020c\u01e6\3\2\2\2\u020c\u01eb\3\2\2\2\u020c")
        buf.write("\u01f0\3\2\2\2\u020c\u01f5\3\2\2\2\u020c\u01fa\3\2\2\2")
        buf.write("\u020c\u01ff\3\2\2\2\u020c\u0204\3\2\2\2\u020c\u0209\3")
        buf.write("\2\2\2\u020d\63\3\2\2\2\u020e\u020f\7+\2\2\u020f\u0265")
        buf.write("\7,\2\2\u0210\u0211\7+\2\2\u0211\u0212\7\61\2\2\u0212")
        buf.write("\u0214\5\f\7\2\u0213\u0215\7?\2\2\u0214\u0213\3\2\2\2")
        buf.write("\u0214\u0215\3\2\2\2\u0215\u0216\3\2\2\2\u0216\u0217\7")
        buf.write(",\2\2\u0217\u0265\3\2\2\2\u0218\u0219\7+\2\2\u0219\u021a")
        buf.write("\7\62\2\2\u021a\u021e\5\f\7\2\u021b\u021c\7?\2\2\u021c")
        buf.write("\u021d\7\61\2\2\u021d\u021f\5\f\7\2\u021e\u021b\3\2\2")
        buf.write("\2\u021e\u021f\3\2\2\2\u021f\u0221\3\2\2\2\u0220\u0222")
        buf.write("\7?\2\2\u0221\u0220\3\2\2\2\u0221\u0222\3\2\2\2\u0222")
        buf.write("\u0223\3\2\2\2\u0223\u0224\7,\2\2\u0224\u0265\3\2\2\2")
        buf.write("\u0225\u0226\7+\2\2\u0226\u0227\5\f\7\2\u0227\u0228\7")
        buf.write(">\2\2\u0228\u0230\5,\27\2\u0229\u022a\7?\2\2\u022a\u022b")
        buf.write("\5\f\7\2\u022b\u022c\7>\2\2\u022c\u022d\5,\27\2\u022d")
        buf.write("\u022f\3\2\2\2\u022e\u0229\3\2\2\2\u022f\u0232\3\2\2\2")
        buf.write("\u0230\u022e\3\2\2\2\u0230\u0231\3\2\2\2\u0231\u0236\3")
        buf.write("\2\2\2\u0232\u0230\3\2\2\2\u0233\u0234\7?\2\2\u0234\u0235")
        buf.write("\7\62\2\2\u0235\u0237\5\f\7\2\u0236\u0233\3\2\2\2\u0236")
        buf.write("\u0237\3\2\2\2\u0237\u023b\3\2\2\2\u0238\u0239\7?\2\2")
        buf.write("\u0239\u023a\7\61\2\2\u023a\u023c\5\f\7\2\u023b\u0238")
        buf.write("\3\2\2\2\u023b\u023c\3\2\2\2\u023c\u023e\3\2\2\2\u023d")
        buf.write("\u023f\7?\2\2\u023e\u023d\3\2\2\2\u023e\u023f\3\2\2\2")
        buf.write("\u023f\u0240\3\2\2\2\u0240\u0241\7,\2\2\u0241\u0265\3")
        buf.write("\2\2\2\u0242\u0243\7+\2\2\u0243\u0248\5\f\7\2\u0244\u0245")
        buf.write("\7?\2\2\u0245\u0247\5\f\7\2\u0246\u0244\3\2\2\2\u0247")
        buf.write("\u024a\3\2\2\2\u0248\u0246\3\2\2\2\u0248\u0249\3\2\2\2")
        buf.write("\u0249\u0252\3\2\2\2\u024a\u0248\3\2\2\2\u024b\u024c\7")
        buf.write("?\2\2\u024c\u024d\5\f\7\2\u024d\u024e\7>\2\2\u024e\u024f")
        buf.write("\5,\27\2\u024f\u0251\3\2\2\2\u0250\u024b\3\2\2\2\u0251")
        buf.write("\u0254\3\2\2\2\u0252\u0250\3\2\2\2\u0252\u0253\3\2\2\2")
        buf.write("\u0253\u0258\3\2\2\2\u0254\u0252\3\2\2\2\u0255\u0256\7")
        buf.write("?\2\2\u0256\u0257\7\62\2\2\u0257\u0259\5\f\7\2\u0258\u0255")
        buf.write("\3\2\2\2\u0258\u0259\3\2\2\2\u0259\u025d\3\2\2\2\u025a")
        buf.write("\u025b\7?\2\2\u025b\u025c\7\61\2\2\u025c\u025e\5\f\7\2")
        buf.write("\u025d\u025a\3\2\2\2\u025d\u025e\3\2\2\2\u025e\u0260\3")
        buf.write("\2\2\2\u025f\u0261\7?\2\2\u0260\u025f\3\2\2\2\u0260\u0261")
        buf.write("\3\2\2\2\u0261\u0262\3\2\2\2\u0262\u0263\7,\2\2\u0263")
        buf.write("\u0265\3\2\2\2\u0264\u020e\3\2\2\2\u0264\u0210\3\2\2\2")
        buf.write("\u0264\u0218\3\2\2\2\u0264\u0225\3\2\2\2\u0264\u0242\3")
        buf.write("\2\2\2\u0265\65\3\2\2\2\u0266\u0268\5\f\7\2\u0267\u0266")
        buf.write("\3\2\2\2\u0267\u0268\3\2\2\2\u0268\u026a\3\2\2\2\u0269")
        buf.write("\u026b\5\64\33\2\u026a\u0269\3\2\2\2\u026a\u026b\3\2\2")
        buf.write("\2\u026b\u026c\3\2\2\2\u026c\u026d\7\2\2\3\u026d\67\3")
        buf.write("\2\2\2\u026e\u026f\t\2\2\2\u026f\u0270\7\16\2\2\u0270")
        buf.write("\u0271\5\66\34\2\u0271\u0275\7\33\2\2\u0272\u0274\5D#")
        buf.write("\2\u0273\u0272\3\2\2\2\u0274\u0277\3\2\2\2\u0275\u0273")
        buf.write("\3\2\2\2\u0275\u0276\3\2\2\2\u0276\u0278\3\2\2\2\u0277")
        buf.write("\u0275\3\2\2\2\u0278\u0279\t\2\2\2\u0279\u027b\7\26\2")
        buf.write("\2\u027a\u027c\7\'\2\2\u027b\u027a\3\2\2\2\u027b\u027c")
        buf.write("\3\2\2\2\u027c\u027d\3\2\2\2\u027d\u027e\7\33\2\2\u027e")
        buf.write("9\3\2\2\2\u027f\u0280\t\2\2\2\u0280\u0281\7\17\2\2\u0281")
        buf.write("\u0282\5$\23\2\u0282\u0283\7\35\2\2\u0283\u0284\5*\26")
        buf.write("\2\u0284\u0288\7\33\2\2\u0285\u0287\5D#\2\u0286\u0285")
        buf.write("\3\2\2\2\u0287\u028a\3\2\2\2\u0288\u0286\3\2\2\2\u0288")
        buf.write("\u0289\3\2\2\2\u0289\u028b\3\2\2\2\u028a\u0288\3\2\2\2")
        buf.write("\u028b\u028c\t\2\2\2\u028c\u028e\7\26\2\2\u028d\u028f")
        buf.write("\7\34\2\2\u028e\u028d\3\2\2\2\u028e\u028f\3\2\2\2\u028f")
        buf.write("\u0290\3\2\2\2\u0290\u0291\7\33\2\2\u0291;\3\2\2\2\u0292")
        buf.write("\u0293\t\2\2\2\u0293\u0294\7\20\2\2\u0294\u0295\5*\26")
        buf.write("\2\u0295\u0299\7\33\2\2\u0296\u0298\5D#\2\u0297\u0296")
        buf.write("\3\2\2\2\u0298\u029b\3\2\2\2\u0299\u0297\3\2\2\2\u0299")
        buf.write("\u029a\3\2\2\2\u029a\u029c\3\2\2\2\u029b\u0299\3\2\2\2")
        buf.write("\u029c\u029d\t\2\2\2\u029d\u029f\7\26\2\2\u029e\u02a0")
        buf.write("\7(\2\2\u029f\u029e\3\2\2\2\u029f\u02a0\3\2\2\2\u02a0")
        buf.write("\u02a1\3\2\2\2\u02a1\u02a2\7\33\2\2\u02a2=\3\2\2\2\u02a3")
        buf.write("\u02a4\t\2\2\2\u02a4\u02a5\7\21\2\2\u02a5\u02a6\5*\26")
        buf.write("\2\u02a6\u02aa\7\33\2\2\u02a7\u02a9\5D#\2\u02a8\u02a7")
        buf.write("\3\2\2\2\u02a9\u02ac\3\2\2\2\u02aa\u02a8\3\2\2\2\u02aa")
        buf.write("\u02ab\3\2\2\2\u02ab\u02b9\3\2\2\2\u02ac\u02aa\3\2\2\2")
        buf.write("\u02ad\u02ae\t\2\2\2\u02ae\u02af\7\22\2\2\u02af\u02b0")
        buf.write("\5*\26\2\u02b0\u02b4\7\33\2\2\u02b1\u02b3\5D#\2\u02b2")
        buf.write("\u02b1\3\2\2\2\u02b3\u02b6\3\2\2\2\u02b4\u02b2\3\2\2\2")
        buf.write("\u02b4\u02b5\3\2\2\2\u02b5\u02b8\3\2\2\2\u02b6\u02b4\3")
        buf.write("\2\2\2\u02b7\u02ad\3\2\2\2\u02b8\u02bb\3\2\2\2\u02b9\u02b7")
        buf.write("\3\2\2\2\u02b9\u02ba\3\2\2\2\u02ba\u02bc\3\2\2\2\u02bb")
        buf.write("\u02b9\3\2\2\2\u02bc\u02bd\t\2\2\2\u02bd\u02be\7\23\2")
        buf.write("\2\u02be\u02c2\7\33\2\2\u02bf\u02c1\5D#\2\u02c0\u02bf")
        buf.write("\3\2\2\2\u02c1\u02c4\3\2\2\2\u02c2\u02c0\3\2\2\2\u02c2")
        buf.write("\u02c3\3\2\2\2\u02c3\u02c5\3\2\2\2\u02c4\u02c2\3\2\2\2")
        buf.write("\u02c5\u02c6\t\2\2\2\u02c6\u02c8\7\26\2\2\u02c7\u02c9")
        buf.write("\7\36\2\2\u02c8\u02c7\3\2\2\2\u02c8\u02c9\3\2\2\2\u02c9")
        buf.write("\u02ca\3\2\2\2\u02ca\u02cb\7\33\2\2\u02cb?\3\2\2\2\u02cc")
        buf.write("\u02cd\t\2\2\2\u02cd\u02ce\7\24\2\2\u02ce\u02cf\5*\26")
        buf.write("\2\u02cf\u02dd\7+\2\2\u02d0\u02d5\5(\25\2\u02d1\u02d2")
        buf.write("\7?\2\2\u02d2\u02d4\5(\25\2\u02d3\u02d1\3\2\2\2\u02d4")
        buf.write("\u02d7\3\2\2\2\u02d5\u02d3\3\2\2\2\u02d5\u02d6\3\2\2\2")
        buf.write("\u02d6\u02d9\3\2\2\2\u02d7\u02d5\3\2\2\2\u02d8\u02da\7")
        buf.write("?\2\2\u02d9\u02d8\3\2\2\2\u02d9\u02da\3\2\2\2\u02da\u02dc")
        buf.write("\3\2\2\2\u02db\u02d0\3\2\2\2\u02dc\u02df\3\2\2\2\u02dd")
        buf.write("\u02db\3\2\2\2\u02dd\u02de\3\2\2\2\u02de\u02e0\3\2\2\2")
        buf.write("\u02df\u02dd\3\2\2\2\u02e0\u02e1\7,\2\2\u02e1\u02e5\7")
        buf.write("\33\2\2\u02e2\u02e4\5D#\2\u02e3\u02e2\3\2\2\2\u02e4\u02e7")
        buf.write("\3\2\2\2\u02e5\u02e3\3\2\2\2\u02e5\u02e6\3\2\2\2\u02e6")
        buf.write("\u02e8\3\2\2\2\u02e7\u02e5\3\2\2\2\u02e8\u02e9\t\2\2\2")
        buf.write("\u02e9\u02eb\7\26\2\2\u02ea\u02ec\7)\2\2\u02eb\u02ea\3")
        buf.write("\2\2\2\u02eb\u02ec\3\2\2\2\u02ec\u02ed\3\2\2\2\u02ed\u02ee")
        buf.write("\7\33\2\2\u02eeA\3\2\2\2\u02ef\u02f0\t\2\2\2\u02f0\u02f1")
        buf.write("\7\25\2\2\u02f1\u02f2\5*\26\2\u02f2\u0300\7+\2\2\u02f3")
        buf.write("\u02f8\5(\25\2\u02f4\u02f5\7?\2\2\u02f5\u02f7\5(\25\2")
        buf.write("\u02f6\u02f4\3\2\2\2\u02f7\u02fa\3\2\2\2\u02f8\u02f6\3")
        buf.write("\2\2\2\u02f8\u02f9\3\2\2\2\u02f9\u02fc\3\2\2\2\u02fa\u02f8")
        buf.write("\3\2\2\2\u02fb\u02fd\7?\2\2\u02fc\u02fb\3\2\2\2\u02fc")
        buf.write("\u02fd\3\2\2\2\u02fd\u02ff\3\2\2\2\u02fe\u02f3\3\2\2\2")
        buf.write("\u02ff\u0302\3\2\2\2\u0300\u02fe\3\2\2\2\u0300\u0301\3")
        buf.write("\2\2\2\u0301\u0303\3\2\2\2\u0302\u0300\3\2\2\2\u0303\u0304")
        buf.write("\7,\2\2\u0304\u0308\7\33\2\2\u0305\u0307\5D#\2\u0306\u0305")
        buf.write("\3\2\2\2\u0307\u030a\3\2\2\2\u0308\u0306\3\2\2\2\u0308")
        buf.write("\u0309\3\2\2\2\u0309\u030b\3\2\2\2\u030a\u0308\3\2\2\2")
        buf.write("\u030b\u030c\t\2\2\2\u030c\u030e\7\26\2\2\u030d\u030f")
        buf.write("\7*\2\2\u030e\u030d\3\2\2\2\u030e\u030f\3\2\2\2\u030f")
        buf.write("\u0310\3\2\2\2\u0310\u0311\7\33\2\2\u0311C\3\2\2\2\u0312")
        buf.write("\u0317\58\35\2\u0313\u0317\5:\36\2\u0314\u0317\5<\37\2")
        buf.write("\u0315\u0317\5> \2\u0316\u0312\3\2\2\2\u0316\u0313\3\2")
        buf.write("\2\2\u0316\u0314\3\2\2\2\u0316\u0315\3\2\2\2\u0317E\3")
        buf.write("\2\2\2\u0318\u031f\5\6\4\2\u0319\u031f\5\n\6\2\u031a\u031f")
        buf.write("\58\35\2\u031b\u031f\5:\36\2\u031c\u031f\5<\37\2\u031d")
        buf.write("\u031f\5> \2\u031e\u0318\3\2\2\2\u031e\u0319\3\2\2\2\u031e")
        buf.write("\u031a\3\2\2\2\u031e\u031b\3\2\2\2\u031e\u031c\3\2\2\2")
        buf.write("\u031e\u031d\3\2\2\2\u031fG\3\2\2\2UINSWZ]cgkqu{\177\u0090")
        buf.write("\u0095\u009f\u00a3\u00a7\u00b1\u00be\u00c2\u00c6\u00d0")
        buf.write("\u00da\u00e4\u00e8\u00ec\u00f8\u0103\u0114\u0124\u0128")
        buf.write("\u012c\u012f\u0133\u013e\u0148\u01a1\u01a5\u01a9\u01b7")
        buf.write("\u01b9\u01be\u01c6\u020c\u0214\u021e\u0221\u0230\u0236")
        buf.write("\u023b\u023e\u0248\u0252\u0258\u025d\u0260\u0264\u0267")
        buf.write("\u026a\u0275\u027b\u0288\u028e\u0299\u029f\u02aa\u02b4")
        buf.write("\u02b9\u02c2\u02c8\u02d5\u02d9\u02dd\u02e5\u02eb\u02f8")
        buf.write("\u02fc\u0300\u0308\u030e\u0316\u031e")
        return buf.getvalue()


class UL4Parser ( Parser ):

    grammarFileName = "UL4Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'whitespace'", "'doc'", "'note'", "'ul4'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'elif'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'end'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'in'", "<INVALID>", "<INVALID>", "'not'", "'is'", 
                     "'and'", "'or'", "'None'", "'True'", "'False'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'('", "')'", 
                     "'['", "']'", "'{'", "'}'", "'**'", "'*'", "'+'", "'-'", 
                     "'//'", "'/'", "'%'", "'=='", "'!='", "'<='", "'<'", 
                     "'>='", "'>'", "'='", "','", "':'", "'~'", "'&'", "'^'", 
                     "'.'", "'<<'", "'>>'", "'|'", "'+='", "'-='", "'*='", 
                     "'//='", "'/='", "'%='", "'<<='", "'>>='", "'&='", 
                     "'^='", "'|='" ]

    symbolicNames = [ "<INVALID>", "DEFAULT_INDENT", "DEFAULT_LINEEND", 
                      "DEFAULT_MAYBETAG", "DEFAULT_TEXT", "TEXT_MAYBETAG", 
                      "TEXT_TEXT", "MAYBETAG_WS", "MAYBETAG_WHITESPACE", 
                      "MAYBETAG_DOC", "MAYBETAG_NOTE", "MAYBETAG_UL4", "MAYBETAG_DEF", 
                      "MAYBETAG_FOR", "MAYBETAG_WHILE", "MAYBETAG_IF", "MAYBETAG_ELIF", 
                      "MAYBETAG_ELSE", "MAYBETAG_RENDERBLOCK", "MAYBETAG_RENDERBLOCKS", 
                      "MAYBETAG_END", "MAYBETAG_OTHER", "WHITESPACE_VALUE", 
                      "WHITESPACE_WS", "WHITESPACE_ENDDELIM", "ENDDELIM", 
                      "FOR", "IN", "IF", "ELSE", "NOT", "IS", "AND", "OR", 
                      "NONE", "TRUE", "FALSE", "DEF", "WHILE", "RENDERBLOCK", 
                      "RENDERBLOCKS", "PARENS_OPEN", "PARENS_CLOSE", "BRACKET_OPEN", 
                      "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", "STAR_STAR", 
                      "STAR", "PLUS", "MINUS", "SLASH_SLASH", "SLASH", "PERCENT", 
                      "EQUAL", "NOT_EQUAL", "LESS_THAN_OR_EQUAL", "LESS_THAN", 
                      "GREATER_THAN_OR_EQUAL", "GREATER_THAN", "ASSIGN", 
                      "COMMA", "COLON", "TILDE", "AMPERSAND", "CARET", "DOT", 
                      "SHIFTLEFT", "SHIFTRIGHT", "BAR", "AUGADD", "AUGSUB", 
                      "AUGMUL", "AUGFLOORDIV", "AUGTRUEDIV", "AUGMOD", "AUGSHIFTLEFT", 
                      "AUGSHIFTRIGHT", "AUGAND", "AUGXOR", "AUGOR", "NAME", 
                      "INT", "FLOAT", "DATE", "DATETIME", "COLOR", "WS", 
                      "STRING", "STRING3" ]

    RULE_template = 0
    RULE_ul4tag = 1
    RULE_whitespacetag = 2
    RULE_doctag = 3
    RULE_notetag = 4
    RULE_name = 5
    RULE_literal = 6
    RULE_seqitem = 7
    RULE_list_ = 8
    RULE_listcomprehension = 9
    RULE_set_ = 10
    RULE_setcomprehension = 11
    RULE_dictitem = 12
    RULE_dict_ = 13
    RULE_dictcomprehension = 14
    RULE_generatorexpression = 15
    RULE_atom = 16
    RULE_nestedlvalue = 17
    RULE_slice_ = 18
    RULE_argument = 19
    RULE_expr = 20
    RULE_exprarg = 21
    RULE_expression = 22
    RULE_for_ = 23
    RULE_stmt = 24
    RULE_signature = 25
    RULE_definition = 26
    RULE_defblock = 27
    RULE_forblock = 28
    RULE_whileblock = 29
    RULE_ifblock = 30
    RULE_renderblockblock = 31
    RULE_renderblocksblock = 32
    RULE_blockitem = 33
    RULE_templatebodyitem = 34

    ruleNames =  [ "template", "ul4tag", "whitespacetag", "doctag", "notetag", 
                   "name", "literal", "seqitem", "list_", "listcomprehension", 
                   "set_", "setcomprehension", "dictitem", "dict_", "dictcomprehension", 
                   "generatorexpression", "atom", "nestedlvalue", "slice_", 
                   "argument", "expr", "exprarg", "expression", "for_", 
                   "stmt", "signature", "definition", "defblock", "forblock", 
                   "whileblock", "ifblock", "renderblockblock", "renderblocksblock", 
                   "blockitem", "templatebodyitem" ]

    EOF = Token.EOF
    DEFAULT_INDENT=1
    DEFAULT_LINEEND=2
    DEFAULT_MAYBETAG=3
    DEFAULT_TEXT=4
    TEXT_MAYBETAG=5
    TEXT_TEXT=6
    MAYBETAG_WS=7
    MAYBETAG_WHITESPACE=8
    MAYBETAG_DOC=9
    MAYBETAG_NOTE=10
    MAYBETAG_UL4=11
    MAYBETAG_DEF=12
    MAYBETAG_FOR=13
    MAYBETAG_WHILE=14
    MAYBETAG_IF=15
    MAYBETAG_ELIF=16
    MAYBETAG_ELSE=17
    MAYBETAG_RENDERBLOCK=18
    MAYBETAG_RENDERBLOCKS=19
    MAYBETAG_END=20
    MAYBETAG_OTHER=21
    WHITESPACE_VALUE=22
    WHITESPACE_WS=23
    WHITESPACE_ENDDELIM=24
    ENDDELIM=25
    FOR=26
    IN=27
    IF=28
    ELSE=29
    NOT=30
    IS=31
    AND=32
    OR=33
    NONE=34
    TRUE=35
    FALSE=36
    DEF=37
    WHILE=38
    RENDERBLOCK=39
    RENDERBLOCKS=40
    PARENS_OPEN=41
    PARENS_CLOSE=42
    BRACKET_OPEN=43
    BRACKET_CLOSE=44
    BRACE_OPEN=45
    BRACE_CLOSE=46
    STAR_STAR=47
    STAR=48
    PLUS=49
    MINUS=50
    SLASH_SLASH=51
    SLASH=52
    PERCENT=53
    EQUAL=54
    NOT_EQUAL=55
    LESS_THAN_OR_EQUAL=56
    LESS_THAN=57
    GREATER_THAN_OR_EQUAL=58
    GREATER_THAN=59
    ASSIGN=60
    COMMA=61
    COLON=62
    TILDE=63
    AMPERSAND=64
    CARET=65
    DOT=66
    SHIFTLEFT=67
    SHIFTRIGHT=68
    BAR=69
    AUGADD=70
    AUGSUB=71
    AUGMUL=72
    AUGFLOORDIV=73
    AUGTRUEDIV=74
    AUGMOD=75
    AUGSHIFTLEFT=76
    AUGSHIFTRIGHT=77
    AUGAND=78
    AUGXOR=79
    AUGOR=80
    NAME=81
    INT=82
    FLOAT=83
    DATE=84
    DATETIME=85
    COLOR=86
    WS=87
    STRING=88
    STRING3=89

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TemplateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_template

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TopLevelContext(TemplateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.TemplateContext
            super().__init__(parser)
            self.head = None # Ul4tagContext
            self._templatebodyitem = None # TemplatebodyitemContext
            self.content = list() # of TemplatebodyitemContexts
            self.copyFrom(ctx)

        def ul4tag(self):
            return self.getTypedRuleContext(UL4Parser.Ul4tagContext,0)

        def templatebodyitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.TemplatebodyitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.TemplatebodyitemContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTopLevel" ):
                return visitor.visitTopLevel(self)
            else:
                return visitor.visitChildren(self)



    def template(self):

        localctx = UL4Parser.TemplateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_template)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.TopLevelContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 70
                localctx.head = self.ul4tag()


            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG:
                self.state = 73
                localctx._templatebodyitem = self.templatebodyitem()
                localctx.content.append(localctx._templatebodyitem)
                self.state = 78
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ul4tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_ul4tag

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TagUL4Context(Ul4tagContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Ul4tagContext
            super().__init__(parser)
            self.templatename = None # NameContext
            self.templatesignature = None # SignatureContext
            self.copyFrom(ctx)

        def MAYBETAG_UL4(self):
            return self.getToken(UL4Parser.MAYBETAG_UL4, 0)
        def ENDDELIM(self):
            return self.getToken(UL4Parser.ENDDELIM, 0)
        def DEFAULT_MAYBETAG(self):
            return self.getToken(UL4Parser.DEFAULT_MAYBETAG, 0)
        def TEXT_MAYBETAG(self):
            return self.getToken(UL4Parser.TEXT_MAYBETAG, 0)
        def MAYBETAG_WS(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.MAYBETAG_WS)
            else:
                return self.getToken(UL4Parser.MAYBETAG_WS, i)
        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)

        def signature(self):
            return self.getTypedRuleContext(UL4Parser.SignatureContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTagUL4" ):
                return visitor.visitTagUL4(self)
            else:
                return visitor.visitChildren(self)



    def ul4tag(self):

        localctx = UL4Parser.Ul4tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_ul4tag)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.TagUL4Context(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 80
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 83
            self.match(UL4Parser.MAYBETAG_UL4)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 84
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.NAME:
                self.state = 87
                localctx.templatename = self.name()


            self.state = 91
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.PARENS_OPEN:
                self.state = 90
                localctx.templatesignature = self.signature()


            self.state = 93
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhitespacetagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_whitespacetag

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TagWhitespaceContext(WhitespacetagContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.WhitespacetagContext
            super().__init__(parser)
            self.whitespace = None # Token
            self.copyFrom(ctx)

        def MAYBETAG_WHITESPACE(self):
            return self.getToken(UL4Parser.MAYBETAG_WHITESPACE, 0)
        def WHITESPACE_ENDDELIM(self):
            return self.getToken(UL4Parser.WHITESPACE_ENDDELIM, 0)
        def DEFAULT_MAYBETAG(self):
            return self.getToken(UL4Parser.DEFAULT_MAYBETAG, 0)
        def TEXT_MAYBETAG(self):
            return self.getToken(UL4Parser.TEXT_MAYBETAG, 0)
        def WHITESPACE_VALUE(self):
            return self.getToken(UL4Parser.WHITESPACE_VALUE, 0)
        def MAYBETAG_WS(self):
            return self.getToken(UL4Parser.MAYBETAG_WS, 0)
        def WHITESPACE_WS(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.WHITESPACE_WS)
            else:
                return self.getToken(UL4Parser.WHITESPACE_WS, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTagWhitespace" ):
                return visitor.visitTagWhitespace(self)
            else:
                return visitor.visitChildren(self)



    def whitespacetag(self):

        localctx = UL4Parser.WhitespacetagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_whitespacetag)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.TagWhitespaceContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 97
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 96
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 99
            self.match(UL4Parser.MAYBETAG_WHITESPACE)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.WHITESPACE_WS:
                self.state = 100
                self.match(UL4Parser.WHITESPACE_WS)


            self.state = 103
            localctx.whitespace = self.match(UL4Parser.WHITESPACE_VALUE)
            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.WHITESPACE_WS:
                self.state = 104
                self.match(UL4Parser.WHITESPACE_WS)


            self.state = 107
            self.match(UL4Parser.WHITESPACE_ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoctagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAYBETAG_DOC(self):
            return self.getToken(UL4Parser.MAYBETAG_DOC, 0)

        def ENDDELIM(self):
            return self.getToken(UL4Parser.ENDDELIM, 0)

        def DEFAULT_MAYBETAG(self):
            return self.getToken(UL4Parser.DEFAULT_MAYBETAG, 0)

        def TEXT_MAYBETAG(self):
            return self.getToken(UL4Parser.TEXT_MAYBETAG, 0)

        def MAYBETAG_WS(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.MAYBETAG_WS)
            else:
                return self.getToken(UL4Parser.MAYBETAG_WS, i)

        def getRuleIndex(self):
            return UL4Parser.RULE_doctag

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoctag" ):
                return visitor.visitDoctag(self)
            else:
                return visitor.visitChildren(self)




    def doctag(self):

        localctx = UL4Parser.DoctagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_doctag)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 110
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 113
            self.match(UL4Parser.MAYBETAG_DOC)
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 114
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 117
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NotetagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAYBETAG_NOTE(self):
            return self.getToken(UL4Parser.MAYBETAG_NOTE, 0)

        def ENDDELIM(self):
            return self.getToken(UL4Parser.ENDDELIM, 0)

        def DEFAULT_MAYBETAG(self):
            return self.getToken(UL4Parser.DEFAULT_MAYBETAG, 0)

        def TEXT_MAYBETAG(self):
            return self.getToken(UL4Parser.TEXT_MAYBETAG, 0)

        def MAYBETAG_WS(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.MAYBETAG_WS)
            else:
                return self.getToken(UL4Parser.MAYBETAG_WS, i)

        def getRuleIndex(self):
            return UL4Parser.RULE_notetag

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotetag" ):
                return visitor.visitNotetag(self)
            else:
                return visitor.visitChildren(self)




    def notetag(self):

        localctx = UL4Parser.NotetagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_notetag)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 120
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 123
            self.match(UL4Parser.MAYBETAG_NOTE)
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.MAYBETAG_WS:
                self.state = 124
                self.match(UL4Parser.MAYBETAG_WS)


            self.state = 127
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(UL4Parser.NAME, 0)

        def getRuleIndex(self):
            return UL4Parser.RULE_name

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName" ):
                return visitor.visitName(self)
            else:
                return visitor.visitChildren(self)




    def name(self):

        localctx = UL4Parser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(UL4Parser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_literal

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LiteralIntegerContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_integer = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(UL4Parser.INT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralInteger" ):
                return visitor.visitLiteralInteger(self)
            else:
                return visitor.visitChildren(self)


    class LiteralFloatContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_float = None # Token
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(UL4Parser.FLOAT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralFloat" ):
                return visitor.visitLiteralFloat(self)
            else:
                return visitor.visitChildren(self)


    class LiteralDateContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_date = None # Token
            self.copyFrom(ctx)

        def DATE(self):
            return self.getToken(UL4Parser.DATE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralDate" ):
                return visitor.visitLiteralDate(self)
            else:
                return visitor.visitChildren(self)


    class LiteralFalseContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_false = None # Token
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(UL4Parser.FALSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralFalse" ):
                return visitor.visitLiteralFalse(self)
            else:
                return visitor.visitChildren(self)


    class LiteralStringContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_string = None # Token
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(UL4Parser.STRING, 0)
        def STRING3(self):
            return self.getToken(UL4Parser.STRING3, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralString" ):
                return visitor.visitLiteralString(self)
            else:
                return visitor.visitChildren(self)


    class LiteralDatetimeContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_datetime = None # Token
            self.copyFrom(ctx)

        def DATETIME(self):
            return self.getToken(UL4Parser.DATETIME, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralDatetime" ):
                return visitor.visitLiteralDatetime(self)
            else:
                return visitor.visitChildren(self)


    class LiteralNoneContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_none = None # Token
            self.copyFrom(ctx)

        def NONE(self):
            return self.getToken(UL4Parser.NONE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralNone" ):
                return visitor.visitLiteralNone(self)
            else:
                return visitor.visitChildren(self)


    class LiteralColorContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_color = None # Token
            self.copyFrom(ctx)

        def COLOR(self):
            return self.getToken(UL4Parser.COLOR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralColor" ):
                return visitor.visitLiteralColor(self)
            else:
                return visitor.visitChildren(self)


    class LiteralNameContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_name = None # NameContext
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralName" ):
                return visitor.visitLiteralName(self)
            else:
                return visitor.visitChildren(self)


    class LiteralTrueContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.LiteralContext
            super().__init__(parser)
            self.e_true = None # Token
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(UL4Parser.TRUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralTrue" ):
                return visitor.visitLiteralTrue(self)
            else:
                return visitor.visitChildren(self)



    def literal(self):

        localctx = UL4Parser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_literal)
        try:
            self.state = 142
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UL4Parser.NONE]:
                localctx = UL4Parser.LiteralNoneContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                localctx.e_none = self.match(UL4Parser.NONE)
                pass
            elif token in [UL4Parser.FALSE]:
                localctx = UL4Parser.LiteralFalseContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                localctx.e_false = self.match(UL4Parser.FALSE)
                pass
            elif token in [UL4Parser.TRUE]:
                localctx = UL4Parser.LiteralTrueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 133
                localctx.e_true = self.match(UL4Parser.TRUE)
                pass
            elif token in [UL4Parser.INT]:
                localctx = UL4Parser.LiteralIntegerContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 134
                localctx.e_integer = self.match(UL4Parser.INT)
                pass
            elif token in [UL4Parser.FLOAT]:
                localctx = UL4Parser.LiteralFloatContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 135
                localctx.e_float = self.match(UL4Parser.FLOAT)
                pass
            elif token in [UL4Parser.STRING]:
                localctx = UL4Parser.LiteralStringContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 136
                localctx.e_string = self.match(UL4Parser.STRING)
                pass
            elif token in [UL4Parser.STRING3]:
                localctx = UL4Parser.LiteralStringContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 137
                localctx.e_string = self.match(UL4Parser.STRING3)
                pass
            elif token in [UL4Parser.DATE]:
                localctx = UL4Parser.LiteralDateContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 138
                localctx.e_date = self.match(UL4Parser.DATE)
                pass
            elif token in [UL4Parser.DATETIME]:
                localctx = UL4Parser.LiteralDatetimeContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 139
                localctx.e_datetime = self.match(UL4Parser.DATETIME)
                pass
            elif token in [UL4Parser.COLOR]:
                localctx = UL4Parser.LiteralColorContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 140
                localctx.e_color = self.match(UL4Parser.COLOR)
                pass
            elif token in [UL4Parser.NAME]:
                localctx = UL4Parser.LiteralNameContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 141
                localctx.e_name = self.name()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SeqitemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_seqitem

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class UnpackSeqItemContext(SeqitemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SeqitemContext
            super().__init__(parser)
            self.star = None # Token
            self.unpackitem = None # ExprContext
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnpackSeqItem" ):
                return visitor.visitUnpackSeqItem(self)
            else:
                return visitor.visitChildren(self)


    class SeqItemContext(SeqitemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SeqitemContext
            super().__init__(parser)
            self.item = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeqItem" ):
                return visitor.visitSeqItem(self)
            else:
                return visitor.visitChildren(self)



    def seqitem(self):

        localctx = UL4Parser.SeqitemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_seqitem)
        try:
            self.state = 147
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UL4Parser.NOT, UL4Parser.NONE, UL4Parser.TRUE, UL4Parser.FALSE, UL4Parser.PARENS_OPEN, UL4Parser.BRACKET_OPEN, UL4Parser.BRACE_OPEN, UL4Parser.MINUS, UL4Parser.TILDE, UL4Parser.NAME, UL4Parser.INT, UL4Parser.FLOAT, UL4Parser.DATE, UL4Parser.DATETIME, UL4Parser.COLOR, UL4Parser.STRING, UL4Parser.STRING3]:
                localctx = UL4Parser.SeqItemContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 144
                localctx.item = self.expr(0)
                pass
            elif token in [UL4Parser.STAR]:
                localctx = UL4Parser.UnpackSeqItemContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 145
                localctx.star = self.match(UL4Parser.STAR)
                self.state = 146
                localctx.unpackitem = self.expr(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_Context(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_list_

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ListEmptyContext(List_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.List_Context
            super().__init__(parser)
            self.open_ = None # Token
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACKET_OPEN(self):
            return self.getToken(UL4Parser.BRACKET_OPEN, 0)
        def BRACKET_CLOSE(self):
            return self.getToken(UL4Parser.BRACKET_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListEmpty" ):
                return visitor.visitListEmpty(self)
            else:
                return visitor.visitChildren(self)


    class ListContext(List_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.List_Context
            super().__init__(parser)
            self.open_ = None # Token
            self._seqitem = None # SeqitemContext
            self.items = list() # of SeqitemContexts
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACKET_OPEN(self):
            return self.getToken(UL4Parser.BRACKET_OPEN, 0)
        def seqitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.SeqitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.SeqitemContext,i)

        def BRACKET_CLOSE(self):
            return self.getToken(UL4Parser.BRACKET_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList" ):
                return visitor.visitList(self)
            else:
                return visitor.visitChildren(self)



    def list_(self):

        localctx = UL4Parser.List_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_list_)
        self._la = 0 # Token type
        try:
            self.state = 165
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.ListEmptyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                localctx.open_ = self.match(UL4Parser.BRACKET_OPEN)
                self.state = 150
                localctx.close = self.match(UL4Parser.BRACKET_CLOSE)
                pass

            elif la_ == 2:
                localctx = UL4Parser.ListContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                localctx.open_ = self.match(UL4Parser.BRACKET_OPEN)
                self.state = 152
                localctx._seqitem = self.seqitem()
                localctx.items.append(localctx._seqitem)
                self.state = 157
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 153
                        self.match(UL4Parser.COMMA)
                        self.state = 154
                        localctx._seqitem = self.seqitem()
                        localctx.items.append(localctx._seqitem) 
                    self.state = 159
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 160
                    self.match(UL4Parser.COMMA)


                self.state = 163
                localctx.close = self.match(UL4Parser.BRACKET_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListcomprehensionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_listcomprehension

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ListComprehensionContext(ListcomprehensionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ListcomprehensionContext
            super().__init__(parser)
            self.open_ = None # Token
            self.item = None # ExprContext
            self.varname = None # NestedlvalueContext
            self.container = None # ExprContext
            self.condition = None # ExprContext
            self.close = None # Token
            self.copyFrom(ctx)

        def FOR(self):
            return self.getToken(UL4Parser.FOR, 0)
        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def BRACKET_OPEN(self):
            return self.getToken(UL4Parser.BRACKET_OPEN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)

        def BRACKET_CLOSE(self):
            return self.getToken(UL4Parser.BRACKET_CLOSE, 0)
        def IF(self):
            return self.getToken(UL4Parser.IF, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListComprehension" ):
                return visitor.visitListComprehension(self)
            else:
                return visitor.visitChildren(self)



    def listcomprehension(self):

        localctx = UL4Parser.ListcomprehensionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_listcomprehension)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.ListComprehensionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            localctx.open_ = self.match(UL4Parser.BRACKET_OPEN)
            self.state = 168
            localctx.item = self.expr(0)
            self.state = 169
            self.match(UL4Parser.FOR)
            self.state = 170
            localctx.varname = self.nestedlvalue()
            self.state = 171
            self.match(UL4Parser.IN)
            self.state = 172
            localctx.container = self.expr(0)
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.IF:
                self.state = 173
                self.match(UL4Parser.IF)
                self.state = 174
                localctx.condition = self.expr(0)


            self.state = 177
            localctx.close = self.match(UL4Parser.BRACKET_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Set_Context(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_set_

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SetEmptyContext(Set_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Set_Context
            super().__init__(parser)
            self.open_ = None # Token
            self.close = None # Token
            self.copyFrom(ctx)

        def SLASH(self):
            return self.getToken(UL4Parser.SLASH, 0)
        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetEmpty" ):
                return visitor.visitSetEmpty(self)
            else:
                return visitor.visitChildren(self)


    class SetContext(Set_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Set_Context
            super().__init__(parser)
            self.open_ = None # Token
            self._seqitem = None # SeqitemContext
            self.items = list() # of SeqitemContexts
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def seqitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.SeqitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.SeqitemContext,i)

        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSet" ):
                return visitor.visitSet(self)
            else:
                return visitor.visitChildren(self)



    def set_(self):

        localctx = UL4Parser.Set_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_set_)
        self._la = 0 # Token type
        try:
            self.state = 196
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.SetEmptyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 179
                localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
                self.state = 180
                self.match(UL4Parser.SLASH)
                self.state = 181
                localctx.close = self.match(UL4Parser.BRACE_CLOSE)
                pass

            elif la_ == 2:
                localctx = UL4Parser.SetContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
                self.state = 183
                localctx._seqitem = self.seqitem()
                localctx.items.append(localctx._seqitem)
                self.state = 188
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 184
                        self.match(UL4Parser.COMMA)
                        self.state = 185
                        localctx._seqitem = self.seqitem()
                        localctx.items.append(localctx._seqitem) 
                    self.state = 190
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 191
                    self.match(UL4Parser.COMMA)


                self.state = 194
                localctx.close = self.match(UL4Parser.BRACE_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetcomprehensionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_setcomprehension

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SetComprehensionContext(SetcomprehensionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SetcomprehensionContext
            super().__init__(parser)
            self.open_ = None # Token
            self.item = None # ExprContext
            self.varname = None # NestedlvalueContext
            self.container = None # ExprContext
            self.condition = None # ExprContext
            self.close = None # Token
            self.copyFrom(ctx)

        def FOR(self):
            return self.getToken(UL4Parser.FOR, 0)
        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)

        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)
        def IF(self):
            return self.getToken(UL4Parser.IF, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetComprehension" ):
                return visitor.visitSetComprehension(self)
            else:
                return visitor.visitChildren(self)



    def setcomprehension(self):

        localctx = UL4Parser.SetcomprehensionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_setcomprehension)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.SetComprehensionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
            self.state = 199
            localctx.item = self.expr(0)
            self.state = 200
            self.match(UL4Parser.FOR)
            self.state = 201
            localctx.varname = self.nestedlvalue()
            self.state = 202
            self.match(UL4Parser.IN)
            self.state = 203
            localctx.container = self.expr(0)
            self.state = 206
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.IF:
                self.state = 204
                self.match(UL4Parser.IF)
                self.state = 205
                localctx.condition = self.expr(0)


            self.state = 208
            localctx.close = self.match(UL4Parser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictitemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_dictitem

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DictItemContext(DictitemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.DictitemContext
            super().__init__(parser)
            self.key = None # ExprContext
            self.value = None # ExprContext
            self.copyFrom(ctx)

        def COLON(self):
            return self.getToken(UL4Parser.COLON, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictItem" ):
                return visitor.visitDictItem(self)
            else:
                return visitor.visitChildren(self)


    class UnpackDictItemContext(DictitemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.DictitemContext
            super().__init__(parser)
            self.star = None # Token
            self.unpackitem = None # ExprContext
            self.copyFrom(ctx)

        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnpackDictItem" ):
                return visitor.visitUnpackDictItem(self)
            else:
                return visitor.visitChildren(self)



    def dictitem(self):

        localctx = UL4Parser.DictitemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_dictitem)
        try:
            self.state = 216
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UL4Parser.NOT, UL4Parser.NONE, UL4Parser.TRUE, UL4Parser.FALSE, UL4Parser.PARENS_OPEN, UL4Parser.BRACKET_OPEN, UL4Parser.BRACE_OPEN, UL4Parser.MINUS, UL4Parser.TILDE, UL4Parser.NAME, UL4Parser.INT, UL4Parser.FLOAT, UL4Parser.DATE, UL4Parser.DATETIME, UL4Parser.COLOR, UL4Parser.STRING, UL4Parser.STRING3]:
                localctx = UL4Parser.DictItemContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                localctx.key = self.expr(0)
                self.state = 211
                self.match(UL4Parser.COLON)
                self.state = 212
                localctx.value = self.expr(0)
                pass
            elif token in [UL4Parser.STAR_STAR]:
                localctx = UL4Parser.UnpackDictItemContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 214
                localctx.star = self.match(UL4Parser.STAR_STAR)
                self.state = 215
                localctx.unpackitem = self.expr(0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dict_Context(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_dict_

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DictEmptyContext(Dict_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Dict_Context
            super().__init__(parser)
            self.open_ = None # Token
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictEmpty" ):
                return visitor.visitDictEmpty(self)
            else:
                return visitor.visitChildren(self)


    class DictContext(Dict_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Dict_Context
            super().__init__(parser)
            self.open_ = None # Token
            self._dictitem = None # DictitemContext
            self.items = list() # of DictitemContexts
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def dictitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.DictitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.DictitemContext,i)

        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDict" ):
                return visitor.visitDict(self)
            else:
                return visitor.visitChildren(self)



    def dict_(self):

        localctx = UL4Parser.Dict_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_dict_)
        self._la = 0 # Token type
        try:
            self.state = 234
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.DictEmptyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 218
                localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
                self.state = 219
                localctx.close = self.match(UL4Parser.BRACE_CLOSE)
                pass

            elif la_ == 2:
                localctx = UL4Parser.DictContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
                self.state = 221
                localctx._dictitem = self.dictitem()
                localctx.items.append(localctx._dictitem)
                self.state = 226
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,24,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 222
                        self.match(UL4Parser.COMMA)
                        self.state = 223
                        localctx._dictitem = self.dictitem()
                        localctx.items.append(localctx._dictitem) 
                    self.state = 228
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,24,self._ctx)

                self.state = 230
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 229
                    self.match(UL4Parser.COMMA)


                self.state = 232
                localctx.close = self.match(UL4Parser.BRACE_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictcomprehensionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_dictcomprehension

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DictComprehensionContext(DictcomprehensionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.DictcomprehensionContext
            super().__init__(parser)
            self.open_ = None # Token
            self.key = None # ExprContext
            self.value = None # ExprContext
            self.varname = None # NestedlvalueContext
            self.container = None # ExprContext
            self.condition = None # ExprContext
            self.close = None # Token
            self.copyFrom(ctx)

        def COLON(self):
            return self.getToken(UL4Parser.COLON, 0)
        def FOR(self):
            return self.getToken(UL4Parser.FOR, 0)
        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def BRACE_OPEN(self):
            return self.getToken(UL4Parser.BRACE_OPEN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)

        def BRACE_CLOSE(self):
            return self.getToken(UL4Parser.BRACE_CLOSE, 0)
        def IF(self):
            return self.getToken(UL4Parser.IF, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictComprehension" ):
                return visitor.visitDictComprehension(self)
            else:
                return visitor.visitChildren(self)



    def dictcomprehension(self):

        localctx = UL4Parser.DictcomprehensionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_dictcomprehension)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.DictComprehensionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            localctx.open_ = self.match(UL4Parser.BRACE_OPEN)
            self.state = 237
            localctx.key = self.expr(0)
            self.state = 238
            self.match(UL4Parser.COLON)
            self.state = 239
            localctx.value = self.expr(0)
            self.state = 240
            self.match(UL4Parser.FOR)
            self.state = 241
            localctx.varname = self.nestedlvalue()
            self.state = 242
            self.match(UL4Parser.IN)
            self.state = 243
            localctx.container = self.expr(0)
            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.IF:
                self.state = 244
                self.match(UL4Parser.IF)
                self.state = 245
                localctx.condition = self.expr(0)


            self.state = 248
            localctx.close = self.match(UL4Parser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GeneratorexpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_generatorexpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class GeneratorExpresssionContext(GeneratorexpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.GeneratorexpressionContext
            super().__init__(parser)
            self.item = None # ExprContext
            self.varname = None # NestedlvalueContext
            self.container = None # ExprContext
            self.condition = None # ExprContext
            self.copyFrom(ctx)

        def FOR(self):
            return self.getToken(UL4Parser.FOR, 0)
        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)

        def IF(self):
            return self.getToken(UL4Parser.IF, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneratorExpresssion" ):
                return visitor.visitGeneratorExpresssion(self)
            else:
                return visitor.visitChildren(self)



    def generatorexpression(self):

        localctx = UL4Parser.GeneratorexpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_generatorexpression)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.GeneratorExpresssionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            localctx.item = self.expr(0)
            self.state = 251
            self.match(UL4Parser.FOR)
            self.state = 252
            localctx.varname = self.nestedlvalue()
            self.state = 253
            self.match(UL4Parser.IN)
            self.state = 254
            localctx.container = self.expr(0)
            self.state = 257
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.IF:
                self.state = 255
                self.match(UL4Parser.IF)
                self.state = 256
                localctx.condition = self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AtomListContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # List_Context
            self.copyFrom(ctx)

        def list_(self):
            return self.getTypedRuleContext(UL4Parser.List_Context,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomList" ):
                return visitor.visitAtomList(self)
            else:
                return visitor.visitChildren(self)


    class AtomLiteralContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # LiteralContext
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(UL4Parser.LiteralContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomLiteral" ):
                return visitor.visitAtomLiteral(self)
            else:
                return visitor.visitChildren(self)


    class AtomDictComprehensionContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # DictcomprehensionContext
            self.copyFrom(ctx)

        def dictcomprehension(self):
            return self.getTypedRuleContext(UL4Parser.DictcomprehensionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomDictComprehension" ):
                return visitor.visitAtomDictComprehension(self)
            else:
                return visitor.visitChildren(self)


    class AtomListComprehensionContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # ListcomprehensionContext
            self.copyFrom(ctx)

        def listcomprehension(self):
            return self.getTypedRuleContext(UL4Parser.ListcomprehensionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomListComprehension" ):
                return visitor.visitAtomListComprehension(self)
            else:
                return visitor.visitChildren(self)


    class AtomSetContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # Set_Context
            self.copyFrom(ctx)

        def set_(self):
            return self.getTypedRuleContext(UL4Parser.Set_Context,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomSet" ):
                return visitor.visitAtomSet(self)
            else:
                return visitor.visitChildren(self)


    class AtomSetComprehensionContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # SetcomprehensionContext
            self.copyFrom(ctx)

        def setcomprehension(self):
            return self.getTypedRuleContext(UL4Parser.SetcomprehensionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomSetComprehension" ):
                return visitor.visitAtomSetComprehension(self)
            else:
                return visitor.visitChildren(self)


    class AtomGeneratorExpressionContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.open_ = None # Token
            self.arg = None # GeneratorexpressionContext
            self.close = None # Token
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def generatorexpression(self):
            return self.getTypedRuleContext(UL4Parser.GeneratorexpressionContext,0)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomGeneratorExpression" ):
                return visitor.visitAtomGeneratorExpression(self)
            else:
                return visitor.visitChildren(self)


    class AtomBracketContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.open_ = None # Token
            self.arg = None # ExprContext
            self.close = None # Token
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomBracket" ):
                return visitor.visitAtomBracket(self)
            else:
                return visitor.visitChildren(self)


    class AtomDictContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.AtomContext
            super().__init__(parser)
            self.arg = None # Dict_Context
            self.copyFrom(ctx)

        def dict_(self):
            return self.getTypedRuleContext(UL4Parser.Dict_Context,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomDict" ):
                return visitor.visitAtomDict(self)
            else:
                return visitor.visitChildren(self)



    def atom(self):

        localctx = UL4Parser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_atom)
        try:
            self.state = 274
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.AtomLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 259
                localctx.arg = self.literal()
                pass

            elif la_ == 2:
                localctx = UL4Parser.AtomListContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 260
                localctx.arg = self.list_()
                pass

            elif la_ == 3:
                localctx = UL4Parser.AtomListComprehensionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 261
                localctx.arg = self.listcomprehension()
                pass

            elif la_ == 4:
                localctx = UL4Parser.AtomSetContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 262
                localctx.arg = self.set_()
                pass

            elif la_ == 5:
                localctx = UL4Parser.AtomSetComprehensionContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 263
                localctx.arg = self.setcomprehension()
                pass

            elif la_ == 6:
                localctx = UL4Parser.AtomDictContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 264
                localctx.arg = self.dict_()
                pass

            elif la_ == 7:
                localctx = UL4Parser.AtomDictComprehensionContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 265
                localctx.arg = self.dictcomprehension()
                pass

            elif la_ == 8:
                localctx = UL4Parser.AtomGeneratorExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 266
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 267
                localctx.arg = self.generatorexpression()
                self.state = 268
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 9:
                localctx = UL4Parser.AtomBracketContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 270
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 271
                localctx.arg = self.expr(0)
                self.state = 272
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NestedlvalueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_nestedlvalue

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LValueMultiContext(NestedlvalueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.NestedlvalueContext
            super().__init__(parser)
            self._nestedlvalue = None # NestedlvalueContext
            self.lvalue = list() # of NestedlvalueContexts
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)
        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def nestedlvalue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.NestedlvalueContext)
            else:
                return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLValueMulti" ):
                return visitor.visitLValueMulti(self)
            else:
                return visitor.visitChildren(self)


    class LValueSimpleContext(NestedlvalueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.NestedlvalueContext
            super().__init__(parser)
            self.lvalue = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLValueSimple" ):
                return visitor.visitLValueSimple(self)
            else:
                return visitor.visitChildren(self)


    class LValueOneContext(NestedlvalueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.NestedlvalueContext
            super().__init__(parser)
            self.lvalue = None # NestedlvalueContext
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def COMMA(self):
            return self.getToken(UL4Parser.COMMA, 0)
        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLValueOne" ):
                return visitor.visitLValueOne(self)
            else:
                return visitor.visitChildren(self)



    def nestedlvalue(self):

        localctx = UL4Parser.NestedlvalueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_nestedlvalue)
        self._la = 0 # Token type
        try:
            self.state = 298
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.LValueSimpleContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                localctx.lvalue = self.expr(0)
                pass

            elif la_ == 2:
                localctx = UL4Parser.LValueOneContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 277
                self.match(UL4Parser.PARENS_OPEN)
                self.state = 278
                localctx.lvalue = self.nestedlvalue()
                self.state = 279
                self.match(UL4Parser.COMMA)
                self.state = 280
                self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 3:
                localctx = UL4Parser.LValueMultiContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 282
                self.match(UL4Parser.PARENS_OPEN)
                self.state = 283
                localctx._nestedlvalue = self.nestedlvalue()
                localctx.lvalue.append(localctx._nestedlvalue)
                self.state = 284
                self.match(UL4Parser.COMMA)
                self.state = 285
                localctx._nestedlvalue = self.nestedlvalue()
                localctx.lvalue.append(localctx._nestedlvalue)
                self.state = 290
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,30,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 286
                        self.match(UL4Parser.COMMA)
                        self.state = 287
                        localctx._nestedlvalue = self.nestedlvalue()
                        localctx.lvalue.append(localctx._nestedlvalue) 
                    self.state = 292
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,30,self._ctx)

                self.state = 294
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 293
                    self.match(UL4Parser.COMMA)


                self.state = 296
                self.match(UL4Parser.PARENS_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Slice_Context(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_slice_

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SliceContext(Slice_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.Slice_Context
            super().__init__(parser)
            self.index1 = None # ExprContext
            self.colon = None # Token
            self.index2 = None # ExprContext
            self.copyFrom(ctx)

        def COLON(self):
            return self.getToken(UL4Parser.COLON, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSlice" ):
                return visitor.visitSlice(self)
            else:
                return visitor.visitChildren(self)



    def slice_(self):

        localctx = UL4Parser.Slice_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_slice_)
        self._la = 0 # Token type
        try:
            localctx = UL4Parser.SliceContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 301
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 30)) & ~0x3f) == 0 and ((1 << (_la - 30)) & ((1 << (UL4Parser.NOT - 30)) | (1 << (UL4Parser.NONE - 30)) | (1 << (UL4Parser.TRUE - 30)) | (1 << (UL4Parser.FALSE - 30)) | (1 << (UL4Parser.PARENS_OPEN - 30)) | (1 << (UL4Parser.BRACKET_OPEN - 30)) | (1 << (UL4Parser.BRACE_OPEN - 30)) | (1 << (UL4Parser.MINUS - 30)) | (1 << (UL4Parser.TILDE - 30)) | (1 << (UL4Parser.NAME - 30)) | (1 << (UL4Parser.INT - 30)) | (1 << (UL4Parser.FLOAT - 30)) | (1 << (UL4Parser.DATE - 30)) | (1 << (UL4Parser.DATETIME - 30)) | (1 << (UL4Parser.COLOR - 30)) | (1 << (UL4Parser.STRING - 30)) | (1 << (UL4Parser.STRING3 - 30)))) != 0):
                self.state = 300
                localctx.index1 = self.expr(0)


            self.state = 303
            localctx.colon = self.match(UL4Parser.COLON)
            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 30)) & ~0x3f) == 0 and ((1 << (_la - 30)) & ((1 << (UL4Parser.NOT - 30)) | (1 << (UL4Parser.NONE - 30)) | (1 << (UL4Parser.TRUE - 30)) | (1 << (UL4Parser.FALSE - 30)) | (1 << (UL4Parser.PARENS_OPEN - 30)) | (1 << (UL4Parser.BRACKET_OPEN - 30)) | (1 << (UL4Parser.BRACE_OPEN - 30)) | (1 << (UL4Parser.MINUS - 30)) | (1 << (UL4Parser.TILDE - 30)) | (1 << (UL4Parser.NAME - 30)) | (1 << (UL4Parser.INT - 30)) | (1 << (UL4Parser.FLOAT - 30)) | (1 << (UL4Parser.DATE - 30)) | (1 << (UL4Parser.DATETIME - 30)) | (1 << (UL4Parser.COLOR - 30)) | (1 << (UL4Parser.STRING - 30)) | (1 << (UL4Parser.STRING3 - 30)))) != 0):
                self.state = 304
                localctx.index2 = self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_argument

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class UnpackDictArgContext(ArgumentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ArgumentContext
            super().__init__(parser)
            self.star = None # Token
            self.argvalue = None # ExprargContext
            self.copyFrom(ctx)

        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)
        def exprarg(self):
            return self.getTypedRuleContext(UL4Parser.ExprargContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnpackDictArg" ):
                return visitor.visitUnpackDictArg(self)
            else:
                return visitor.visitChildren(self)


    class PosArgContext(ArgumentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ArgumentContext
            super().__init__(parser)
            self.argvalue = None # ExprargContext
            self.copyFrom(ctx)

        def exprarg(self):
            return self.getTypedRuleContext(UL4Parser.ExprargContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPosArg" ):
                return visitor.visitPosArg(self)
            else:
                return visitor.visitChildren(self)


    class KeywordArgContext(ArgumentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ArgumentContext
            super().__init__(parser)
            self.argname = None # NameContext
            self.argvalue = None # ExprargContext
            self.copyFrom(ctx)

        def ASSIGN(self):
            return self.getToken(UL4Parser.ASSIGN, 0)
        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)

        def exprarg(self):
            return self.getTypedRuleContext(UL4Parser.ExprargContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeywordArg" ):
                return visitor.visitKeywordArg(self)
            else:
                return visitor.visitChildren(self)


    class UnpackListArgContext(ArgumentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ArgumentContext
            super().__init__(parser)
            self.star = None # Token
            self.argvalue = None # ExprargContext
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def exprarg(self):
            return self.getTypedRuleContext(UL4Parser.ExprargContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnpackListArg" ):
                return visitor.visitUnpackListArg(self)
            else:
                return visitor.visitChildren(self)



    def argument(self):

        localctx = UL4Parser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_argument)
        try:
            self.state = 316
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.PosArgContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 307
                localctx.argvalue = self.exprarg()
                pass

            elif la_ == 2:
                localctx = UL4Parser.KeywordArgContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 308
                localctx.argname = self.name()
                self.state = 309
                self.match(UL4Parser.ASSIGN)
                self.state = 310
                localctx.argvalue = self.exprarg()
                pass

            elif la_ == 3:
                localctx = UL4Parser.UnpackListArgContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 312
                localctx.star = self.match(UL4Parser.STAR)
                self.state = 313
                localctx.argvalue = self.exprarg()
                pass

            elif la_ == 4:
                localctx = UL4Parser.UnpackDictArgContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 314
                localctx.star = self.match(UL4Parser.STAR_STAR)
                self.state = 315
                localctx.argvalue = self.exprarg()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AddContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def PLUS(self):
            return self.getToken(UL4Parser.PLUS, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdd" ):
                return visitor.visitAdd(self)
            else:
                return visitor.visitChildren(self)


    class ShiftRightContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def SHIFTRIGHT(self):
            return self.getToken(UL4Parser.SHIFTRIGHT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitShiftRight" ):
                return visitor.visitShiftRight(self)
            else:
                return visitor.visitChildren(self)


    class OrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def OR(self):
            return self.getToken(UL4Parser.OR, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr" ):
                return visitor.visitOr(self)
            else:
                return visitor.visitChildren(self)


    class LTContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def LESS_THAN(self):
            return self.getToken(UL4Parser.LESS_THAN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLT" ):
                return visitor.visitLT(self)
            else:
                return visitor.visitChildren(self)


    class IsContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def IS(self):
            return self.getToken(UL4Parser.IS, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIs" ):
                return visitor.visitIs(self)
            else:
                return visitor.visitChildren(self)


    class AttrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e1 = None # ExprContext
            self.n = None # NameContext
            self.copyFrom(ctx)

        def DOT(self):
            return self.getToken(UL4Parser.DOT, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)

        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)


    class ItemContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e1 = None # ExprContext
            self.index = None # ExprContext
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACKET_OPEN(self):
            return self.getToken(UL4Parser.BRACKET_OPEN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)

        def BRACKET_CLOSE(self):
            return self.getToken(UL4Parser.BRACKET_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitItem" ):
                return visitor.visitItem(self)
            else:
                return visitor.visitChildren(self)


    class BitXOrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def CARET(self):
            return self.getToken(UL4Parser.CARET, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitXOr" ):
                return visitor.visitBitXOr(self)
            else:
                return visitor.visitChildren(self)


    class IsNotContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def IS(self):
            return self.getToken(UL4Parser.IS, 0)
        def NOT(self):
            return self.getToken(UL4Parser.NOT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIsNot" ):
                return visitor.visitIsNot(self)
            else:
                return visitor.visitChildren(self)


    class GEContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def GREATER_THAN_OR_EQUAL(self):
            return self.getToken(UL4Parser.GREATER_THAN_OR_EQUAL, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGE" ):
                return visitor.visitGE(self)
            else:
                return visitor.visitChildren(self)


    class SubContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(UL4Parser.MINUS, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSub" ):
                return visitor.visitSub(self)
            else:
                return visitor.visitChildren(self)


    class CallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e1 = None # ExprContext
            self._argument = None # ArgumentContext
            self.args = list() # of ArgumentContexts
            self.close = None # Token
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ArgumentContext,i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)


    class NotContainsContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(UL4Parser.NOT, 0)
        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotContains" ):
                return visitor.visitNotContains(self)
            else:
                return visitor.visitChildren(self)


    class ModContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def PERCENT(self):
            return self.getToken(UL4Parser.PERCENT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMod" ):
                return visitor.visitMod(self)
            else:
                return visitor.visitChildren(self)


    class BitOrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def BAR(self):
            return self.getToken(UL4Parser.BAR, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitOr" ):
                return visitor.visitBitOr(self)
            else:
                return visitor.visitChildren(self)


    class ShiftLeftContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def SHIFTLEFT(self):
            return self.getToken(UL4Parser.SHIFTLEFT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitShiftLeft" ):
                return visitor.visitShiftLeft(self)
            else:
                return visitor.visitChildren(self)


    class MulContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMul" ):
                return visitor.visitMul(self)
            else:
                return visitor.visitChildren(self)


    class ExprAtomContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e = None # AtomContext
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(UL4Parser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprAtom" ):
                return visitor.visitExprAtom(self)
            else:
                return visitor.visitChildren(self)


    class FloorDivContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def SLASH_SLASH(self):
            return self.getToken(UL4Parser.SLASH_SLASH, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloorDiv" ):
                return visitor.visitFloorDiv(self)
            else:
                return visitor.visitChildren(self)


    class EQContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def EQUAL(self):
            return self.getToken(UL4Parser.EQUAL, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEQ" ):
                return visitor.visitEQ(self)
            else:
                return visitor.visitChildren(self)


    class GTContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def GREATER_THAN(self):
            return self.getToken(UL4Parser.GREATER_THAN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGT" ):
                return visitor.visitGT(self)
            else:
                return visitor.visitChildren(self)


    class TrueDivContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def SLASH(self):
            return self.getToken(UL4Parser.SLASH, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrueDiv" ):
                return visitor.visitTrueDiv(self)
            else:
                return visitor.visitChildren(self)


    class NegContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.arg = None # ExprContext
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(UL4Parser.MINUS, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNeg" ):
                return visitor.visitNeg(self)
            else:
                return visitor.visitChildren(self)


    class NotContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e = None # ExprContext
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(UL4Parser.NOT, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot" ):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)


    class AndContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def AND(self):
            return self.getToken(UL4Parser.AND, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd" ):
                return visitor.visitAnd(self)
            else:
                return visitor.visitChildren(self)


    class BitAndContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def AMPERSAND(self):
            return self.getToken(UL4Parser.AMPERSAND, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitAnd" ):
                return visitor.visitBitAnd(self)
            else:
                return visitor.visitChildren(self)


    class NEContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def NOT_EQUAL(self):
            return self.getToken(UL4Parser.NOT_EQUAL, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNE" ):
                return visitor.visitNE(self)
            else:
                return visitor.visitChildren(self)


    class ContainsContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContains" ):
                return visitor.visitContains(self)
            else:
                return visitor.visitChildren(self)


    class LEContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def LESS_THAN_OR_EQUAL(self):
            return self.getToken(UL4Parser.LESS_THAN_OR_EQUAL, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLE" ):
                return visitor.visitLE(self)
            else:
                return visitor.visitChildren(self)


    class ItemSliceContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.e1 = None # ExprContext
            self.index = None # Slice_Context
            self.close = None # Token
            self.copyFrom(ctx)

        def BRACKET_OPEN(self):
            return self.getToken(UL4Parser.BRACKET_OPEN, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)

        def slice_(self):
            return self.getTypedRuleContext(UL4Parser.Slice_Context,0)

        def BRACKET_CLOSE(self):
            return self.getToken(UL4Parser.BRACKET_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitItemSlice" ):
                return visitor.visitItemSlice(self)
            else:
                return visitor.visitChildren(self)


    class BitNotContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.arg = None # ExprContext
            self.copyFrom(ctx)

        def TILDE(self):
            return self.getToken(UL4Parser.TILDE, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitNot" ):
                return visitor.visitBitNot(self)
            else:
                return visitor.visitChildren(self)


    class IfContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExprContext
            super().__init__(parser)
            self.argif = None # ExprContext
            self.argcond = None # ExprContext
            self.argelse = None # ExprContext
            self.copyFrom(ctx)

        def IF(self):
            return self.getToken(UL4Parser.IF, 0)
        def ELSE(self):
            return self.getToken(UL4Parser.ELSE, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf" ):
                return visitor.visitIf(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = UL4Parser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [UL4Parser.NONE, UL4Parser.TRUE, UL4Parser.FALSE, UL4Parser.PARENS_OPEN, UL4Parser.BRACKET_OPEN, UL4Parser.BRACE_OPEN, UL4Parser.NAME, UL4Parser.INT, UL4Parser.FLOAT, UL4Parser.DATE, UL4Parser.DATETIME, UL4Parser.COLOR, UL4Parser.STRING, UL4Parser.STRING3]:
                localctx = UL4Parser.ExprAtomContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 319
                localctx.e = self.atom()
                pass
            elif token in [UL4Parser.MINUS]:
                localctx = UL4Parser.NegContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 320
                self.match(UL4Parser.MINUS)
                self.state = 321
                localctx.arg = self.expr(27)
                pass
            elif token in [UL4Parser.TILDE]:
                localctx = UL4Parser.BitNotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 322
                self.match(UL4Parser.TILDE)
                self.state = 323
                localctx.arg = self.expr(26)
                pass
            elif token in [UL4Parser.NOT]:
                localctx = UL4Parser.NotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 324
                self.match(UL4Parser.NOT)
                self.state = 325
                localctx.e = self.expr(4)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 439
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,41,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 437
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
                    if la_ == 1:
                        localctx = UL4Parser.MulContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 328
                        if not self.precpred(self._ctx, 25):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 25)")
                        self.state = 329
                        self.match(UL4Parser.STAR)
                        self.state = 330
                        localctx.right = self.expr(26)
                        pass

                    elif la_ == 2:
                        localctx = UL4Parser.TrueDivContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 331
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 332
                        self.match(UL4Parser.SLASH)
                        self.state = 333
                        localctx.right = self.expr(25)
                        pass

                    elif la_ == 3:
                        localctx = UL4Parser.FloorDivContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 334
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 335
                        self.match(UL4Parser.SLASH_SLASH)
                        self.state = 336
                        localctx.right = self.expr(24)
                        pass

                    elif la_ == 4:
                        localctx = UL4Parser.ModContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 337
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 338
                        self.match(UL4Parser.PERCENT)
                        self.state = 339
                        localctx.right = self.expr(23)
                        pass

                    elif la_ == 5:
                        localctx = UL4Parser.AddContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 340
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 341
                        self.match(UL4Parser.PLUS)
                        self.state = 342
                        localctx.right = self.expr(22)
                        pass

                    elif la_ == 6:
                        localctx = UL4Parser.SubContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 343
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 344
                        self.match(UL4Parser.MINUS)
                        self.state = 345
                        localctx.right = self.expr(21)
                        pass

                    elif la_ == 7:
                        localctx = UL4Parser.ShiftLeftContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 346
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 347
                        self.match(UL4Parser.SHIFTLEFT)
                        self.state = 348
                        localctx.right = self.expr(20)
                        pass

                    elif la_ == 8:
                        localctx = UL4Parser.ShiftRightContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 349
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 350
                        self.match(UL4Parser.SHIFTRIGHT)
                        self.state = 351
                        localctx.right = self.expr(19)
                        pass

                    elif la_ == 9:
                        localctx = UL4Parser.BitAndContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 352
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 353
                        self.match(UL4Parser.AMPERSAND)
                        self.state = 354
                        localctx.right = self.expr(18)
                        pass

                    elif la_ == 10:
                        localctx = UL4Parser.BitXOrContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 355
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 356
                        self.match(UL4Parser.CARET)
                        self.state = 357
                        localctx.right = self.expr(17)
                        pass

                    elif la_ == 11:
                        localctx = UL4Parser.BitOrContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 358
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 359
                        self.match(UL4Parser.BAR)
                        self.state = 360
                        localctx.right = self.expr(16)
                        pass

                    elif la_ == 12:
                        localctx = UL4Parser.EQContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 361
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 362
                        self.match(UL4Parser.EQUAL)
                        self.state = 363
                        localctx.right = self.expr(15)
                        pass

                    elif la_ == 13:
                        localctx = UL4Parser.NEContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 364
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 365
                        self.match(UL4Parser.NOT_EQUAL)
                        self.state = 366
                        localctx.right = self.expr(14)
                        pass

                    elif la_ == 14:
                        localctx = UL4Parser.LTContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 367
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 368
                        self.match(UL4Parser.LESS_THAN)
                        self.state = 369
                        localctx.right = self.expr(13)
                        pass

                    elif la_ == 15:
                        localctx = UL4Parser.LEContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 370
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 371
                        self.match(UL4Parser.LESS_THAN_OR_EQUAL)
                        self.state = 372
                        localctx.right = self.expr(12)
                        pass

                    elif la_ == 16:
                        localctx = UL4Parser.GTContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 373
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 374
                        self.match(UL4Parser.GREATER_THAN)
                        self.state = 375
                        localctx.right = self.expr(11)
                        pass

                    elif la_ == 17:
                        localctx = UL4Parser.GEContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 376
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 377
                        self.match(UL4Parser.GREATER_THAN_OR_EQUAL)
                        self.state = 378
                        localctx.right = self.expr(10)
                        pass

                    elif la_ == 18:
                        localctx = UL4Parser.ContainsContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 379
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 380
                        self.match(UL4Parser.IN)
                        self.state = 381
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 19:
                        localctx = UL4Parser.NotContainsContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 382
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 383
                        self.match(UL4Parser.NOT)
                        self.state = 384
                        self.match(UL4Parser.IN)
                        self.state = 385
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 20:
                        localctx = UL4Parser.IsContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 386
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 387
                        self.match(UL4Parser.IS)
                        self.state = 388
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 21:
                        localctx = UL4Parser.IsNotContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 389
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 390
                        self.match(UL4Parser.IS)
                        self.state = 391
                        self.match(UL4Parser.NOT)
                        self.state = 392
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 22:
                        localctx = UL4Parser.AndContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 393
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 394
                        self.match(UL4Parser.AND)
                        self.state = 395
                        localctx.right = self.expr(4)
                        pass

                    elif la_ == 23:
                        localctx = UL4Parser.OrContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 396
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 397
                        self.match(UL4Parser.OR)
                        self.state = 398
                        localctx.right = self.expr(3)
                        pass

                    elif la_ == 24:
                        localctx = UL4Parser.IfContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.argif = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 399
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 400
                        self.match(UL4Parser.IF)
                        self.state = 401
                        localctx.argcond = self.expr(0)
                        self.state = 402
                        self.match(UL4Parser.ELSE)
                        self.state = 403
                        localctx.argelse = self.expr(2)
                        pass

                    elif la_ == 25:
                        localctx = UL4Parser.AttrContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.e1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 405
                        if not self.precpred(self._ctx, 31):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 31)")
                        self.state = 406
                        self.match(UL4Parser.DOT)
                        self.state = 407
                        localctx.n = self.name()
                        pass

                    elif la_ == 26:
                        localctx = UL4Parser.CallContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.e1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 408
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 409
                        self.match(UL4Parser.PARENS_OPEN)
                        self.state = 423
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while ((((_la - 30)) & ~0x3f) == 0 and ((1 << (_la - 30)) & ((1 << (UL4Parser.NOT - 30)) | (1 << (UL4Parser.NONE - 30)) | (1 << (UL4Parser.TRUE - 30)) | (1 << (UL4Parser.FALSE - 30)) | (1 << (UL4Parser.PARENS_OPEN - 30)) | (1 << (UL4Parser.BRACKET_OPEN - 30)) | (1 << (UL4Parser.BRACE_OPEN - 30)) | (1 << (UL4Parser.STAR_STAR - 30)) | (1 << (UL4Parser.STAR - 30)) | (1 << (UL4Parser.MINUS - 30)) | (1 << (UL4Parser.TILDE - 30)) | (1 << (UL4Parser.NAME - 30)) | (1 << (UL4Parser.INT - 30)) | (1 << (UL4Parser.FLOAT - 30)) | (1 << (UL4Parser.DATE - 30)) | (1 << (UL4Parser.DATETIME - 30)) | (1 << (UL4Parser.COLOR - 30)) | (1 << (UL4Parser.STRING - 30)) | (1 << (UL4Parser.STRING3 - 30)))) != 0):
                            self.state = 410
                            localctx._argument = self.argument()
                            localctx.args.append(localctx._argument)
                            self.state = 415
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,37,self._ctx)
                            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                                if _alt==1:
                                    self.state = 411
                                    self.match(UL4Parser.COMMA)
                                    self.state = 412
                                    localctx._argument = self.argument()
                                    localctx.args.append(localctx._argument) 
                                self.state = 417
                                self._errHandler.sync(self)
                                _alt = self._interp.adaptivePredict(self._input,37,self._ctx)

                            self.state = 419
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la==UL4Parser.COMMA:
                                self.state = 418
                                self.match(UL4Parser.COMMA)


                            self.state = 425
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 426
                        localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                        pass

                    elif la_ == 27:
                        localctx = UL4Parser.ItemContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.e1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 427
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 428
                        self.match(UL4Parser.BRACKET_OPEN)
                        self.state = 429
                        localctx.index = self.expr(0)
                        self.state = 430
                        localctx.close = self.match(UL4Parser.BRACKET_CLOSE)
                        pass

                    elif la_ == 28:
                        localctx = UL4Parser.ItemSliceContext(self, UL4Parser.ExprContext(self, _parentctx, _parentState))
                        localctx.e1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 432
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 433
                        self.match(UL4Parser.BRACKET_OPEN)
                        self.state = 434
                        localctx.index = self.slice_()
                        self.state = 435
                        localctx.close = self.match(UL4Parser.BRACKET_CLOSE)
                        pass

             
                self.state = 441
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,41,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExprargContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.ege = None # GeneratorexpressionContext
            self.e1 = None # ExprContext

        def generatorexpression(self):
            return self.getTypedRuleContext(UL4Parser.GeneratorexpressionContext,0)


        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def getRuleIndex(self):
            return UL4Parser.RULE_exprarg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprarg" ):
                return visitor.visitExprarg(self)
            else:
                return visitor.visitChildren(self)




    def exprarg(self):

        localctx = UL4Parser.ExprargContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_exprarg)
        try:
            self.state = 444
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 442
                localctx.ege = self.generatorexpression()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 443
                localctx.e1 = self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ExpressionGeneratorExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExpressionContext
            super().__init__(parser)
            self.ege = None # GeneratorexpressionContext
            self.copyFrom(ctx)

        def EOF(self):
            return self.getToken(UL4Parser.EOF, 0)
        def generatorexpression(self):
            return self.getTypedRuleContext(UL4Parser.GeneratorexpressionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionGeneratorExpression" ):
                return visitor.visitExpressionGeneratorExpression(self)
            else:
                return visitor.visitChildren(self)


    class ExpressionExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.ExpressionContext
            super().__init__(parser)
            self.e = None # ExprContext
            self.copyFrom(ctx)

        def EOF(self):
            return self.getToken(UL4Parser.EOF, 0)
        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionExpression" ):
                return visitor.visitExpressionExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self):

        localctx = UL4Parser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_expression)
        try:
            self.state = 452
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.ExpressionGeneratorExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 446
                localctx.ege = self.generatorexpression()
                self.state = 447
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 2:
                localctx = UL4Parser.ExpressionExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 449
                localctx.e = self.expr(0)
                self.state = 450
                self.match(UL4Parser.EOF)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_Context(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_for_

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ForContext(For_Context):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.For_Context
            super().__init__(parser)
            self.var = None # NestedlvalueContext
            self.container = None # ExprContext
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(UL4Parser.IN, 0)
        def EOF(self):
            return self.getToken(UL4Parser.EOF, 0)
        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor" ):
                return visitor.visitFor(self)
            else:
                return visitor.visitChildren(self)



    def for_(self):

        localctx = UL4Parser.For_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_for_)
        try:
            localctx = UL4Parser.ForContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 454
            localctx.var = self.nestedlvalue()
            self.state = 455
            self.match(UL4Parser.IN)
            self.state = 456
            localctx.container = self.expr(0)
            self.state = 457
            self.match(UL4Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.nn = None # NestedlvalueContext
            self.e = None # ExprContext
            self.n = None # ExprContext
            self.ex = None # ExpressionContext

        def ASSIGN(self):
            return self.getToken(UL4Parser.ASSIGN, 0)

        def EOF(self):
            return self.getToken(UL4Parser.EOF, 0)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def AUGADD(self):
            return self.getToken(UL4Parser.AUGADD, 0)

        def AUGSUB(self):
            return self.getToken(UL4Parser.AUGSUB, 0)

        def AUGMUL(self):
            return self.getToken(UL4Parser.AUGMUL, 0)

        def AUGFLOORDIV(self):
            return self.getToken(UL4Parser.AUGFLOORDIV, 0)

        def AUGTRUEDIV(self):
            return self.getToken(UL4Parser.AUGTRUEDIV, 0)

        def AUGMOD(self):
            return self.getToken(UL4Parser.AUGMOD, 0)

        def AUGSHIFTLEFT(self):
            return self.getToken(UL4Parser.AUGSHIFTLEFT, 0)

        def AUGSHIFTRIGHT(self):
            return self.getToken(UL4Parser.AUGSHIFTRIGHT, 0)

        def AUGAND(self):
            return self.getToken(UL4Parser.AUGAND, 0)

        def AUGXOR(self):
            return self.getToken(UL4Parser.AUGXOR, 0)

        def AUGOR(self):
            return self.getToken(UL4Parser.AUGOR, 0)

        def expression(self):
            return self.getTypedRuleContext(UL4Parser.ExpressionContext,0)


        def getRuleIndex(self):
            return UL4Parser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = UL4Parser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_stmt)
        try:
            self.state = 522
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 459
                localctx.nn = self.nestedlvalue()
                self.state = 460
                self.match(UL4Parser.ASSIGN)
                self.state = 461
                localctx.e = self.expr(0)
                self.state = 462
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 464
                localctx.n = self.expr(0)
                self.state = 465
                self.match(UL4Parser.AUGADD)
                self.state = 466
                localctx.e = self.expr(0)
                self.state = 467
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 469
                localctx.n = self.expr(0)
                self.state = 470
                self.match(UL4Parser.AUGSUB)
                self.state = 471
                localctx.e = self.expr(0)
                self.state = 472
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 474
                localctx.n = self.expr(0)
                self.state = 475
                self.match(UL4Parser.AUGMUL)
                self.state = 476
                localctx.e = self.expr(0)
                self.state = 477
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 479
                localctx.n = self.expr(0)
                self.state = 480
                self.match(UL4Parser.AUGFLOORDIV)
                self.state = 481
                localctx.e = self.expr(0)
                self.state = 482
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 484
                localctx.n = self.expr(0)
                self.state = 485
                self.match(UL4Parser.AUGTRUEDIV)
                self.state = 486
                localctx.e = self.expr(0)
                self.state = 487
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 489
                localctx.n = self.expr(0)
                self.state = 490
                self.match(UL4Parser.AUGMOD)
                self.state = 491
                localctx.e = self.expr(0)
                self.state = 492
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 494
                localctx.n = self.expr(0)
                self.state = 495
                self.match(UL4Parser.AUGSHIFTLEFT)
                self.state = 496
                localctx.e = self.expr(0)
                self.state = 497
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 499
                localctx.n = self.expr(0)
                self.state = 500
                self.match(UL4Parser.AUGSHIFTRIGHT)
                self.state = 501
                localctx.e = self.expr(0)
                self.state = 502
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 504
                localctx.n = self.expr(0)
                self.state = 505
                self.match(UL4Parser.AUGAND)
                self.state = 506
                localctx.e = self.expr(0)
                self.state = 507
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 509
                localctx.n = self.expr(0)
                self.state = 510
                self.match(UL4Parser.AUGXOR)
                self.state = 511
                localctx.e = self.expr(0)
                self.state = 512
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 514
                localctx.n = self.expr(0)
                self.state = 515
                self.match(UL4Parser.AUGOR)
                self.state = 516
                localctx.e = self.expr(0)
                self.state = 517
                self.match(UL4Parser.EOF)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 519
                localctx.ex = self.expression()
                self.state = 520
                self.match(UL4Parser.EOF)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignatureContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_signature

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SignatureUnpackDictParamsContext(SignatureContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SignatureContext
            super().__init__(parser)
            self.open_ = None # Token
            self.rkwargsname = None # NameContext
            self.close = None # Token
            self.copyFrom(ctx)

        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)
        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def COMMA(self):
            return self.getToken(UL4Parser.COMMA, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignatureUnpackDictParams" ):
                return visitor.visitSignatureUnpackDictParams(self)
            else:
                return visitor.visitChildren(self)


    class SignatureDefaultParamsContext(SignatureContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SignatureContext
            super().__init__(parser)
            self.open_ = None # Token
            self._name = None # NameContext
            self.names = list() # of NameContexts
            self._exprarg = None # ExprargContext
            self.defaults = list() # of ExprargContexts
            self.rargsname = None # NameContext
            self.rkwargsname = None # NameContext
            self.close = None # Token
            self.copyFrom(ctx)

        def ASSIGN(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ASSIGN)
            else:
                return self.getToken(UL4Parser.ASSIGN, i)
        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.NameContext)
            else:
                return self.getTypedRuleContext(UL4Parser.NameContext,i)

        def exprarg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprargContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprargContext,i)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)
        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignatureDefaultParams" ):
                return visitor.visitSignatureDefaultParams(self)
            else:
                return visitor.visitChildren(self)


    class SignatureUnpackParamsContext(SignatureContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SignatureContext
            super().__init__(parser)
            self.open_ = None # Token
            self.rargsname = None # NameContext
            self.rkwargsname = None # NameContext
            self.close = None # Token
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.NameContext)
            else:
                return self.getTypedRuleContext(UL4Parser.NameContext,i)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)
        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignatureUnpackParams" ):
                return visitor.visitSignatureUnpackParams(self)
            else:
                return visitor.visitChildren(self)


    class SignatureNoParamsContext(SignatureContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SignatureContext
            super().__init__(parser)
            self.open_ = None # Token
            self.close = None # Token
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignatureNoParams" ):
                return visitor.visitSignatureNoParams(self)
            else:
                return visitor.visitChildren(self)


    class SignatureAnyParamsContext(SignatureContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.SignatureContext
            super().__init__(parser)
            self.open_ = None # Token
            self._name = None # NameContext
            self.names_without_defaults = list() # of NameContexts
            self.names_with_defaults = list() # of NameContexts
            self._exprarg = None # ExprargContext
            self.defaults = list() # of ExprargContexts
            self.rargsname = None # NameContext
            self.rkwargsname = None # NameContext
            self.close = None # Token
            self.copyFrom(ctx)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)
        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.NameContext)
            else:
                return self.getTypedRuleContext(UL4Parser.NameContext,i)

        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)
        def ASSIGN(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ASSIGN)
            else:
                return self.getToken(UL4Parser.ASSIGN, i)
        def STAR(self):
            return self.getToken(UL4Parser.STAR, 0)
        def STAR_STAR(self):
            return self.getToken(UL4Parser.STAR_STAR, 0)
        def exprarg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprargContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprargContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignatureAnyParams" ):
                return visitor.visitSignatureAnyParams(self)
            else:
                return visitor.visitChildren(self)



    def signature(self):

        localctx = UL4Parser.SignatureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_signature)
        self._la = 0 # Token type
        try:
            self.state = 610
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                localctx = UL4Parser.SignatureNoParamsContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 524
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 525
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 2:
                localctx = UL4Parser.SignatureUnpackDictParamsContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 526
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 527
                self.match(UL4Parser.STAR_STAR)
                self.state = 528
                localctx.rkwargsname = self.name()
                self.state = 530
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 529
                    self.match(UL4Parser.COMMA)


                self.state = 532
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 3:
                localctx = UL4Parser.SignatureUnpackParamsContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 534
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 535
                self.match(UL4Parser.STAR)
                self.state = 536
                localctx.rargsname = self.name()
                self.state = 540
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
                if la_ == 1:
                    self.state = 537
                    self.match(UL4Parser.COMMA)
                    self.state = 538
                    self.match(UL4Parser.STAR_STAR)
                    self.state = 539
                    localctx.rkwargsname = self.name()


                self.state = 543
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 542
                    self.match(UL4Parser.COMMA)


                self.state = 545
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 4:
                localctx = UL4Parser.SignatureDefaultParamsContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 547
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 548
                localctx._name = self.name()
                localctx.names.append(localctx._name)
                self.state = 549
                self.match(UL4Parser.ASSIGN)
                self.state = 550
                localctx._exprarg = self.exprarg()
                localctx.defaults.append(localctx._exprarg)
                self.state = 558
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,48,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 551
                        self.match(UL4Parser.COMMA)
                        self.state = 552
                        localctx._name = self.name()
                        localctx.names.append(localctx._name)
                        self.state = 553
                        self.match(UL4Parser.ASSIGN)
                        self.state = 554
                        localctx._exprarg = self.exprarg()
                        localctx.defaults.append(localctx._exprarg) 
                    self.state = 560
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,48,self._ctx)

                self.state = 564
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
                if la_ == 1:
                    self.state = 561
                    self.match(UL4Parser.COMMA)
                    self.state = 562
                    self.match(UL4Parser.STAR)
                    self.state = 563
                    localctx.rargsname = self.name()


                self.state = 569
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
                if la_ == 1:
                    self.state = 566
                    self.match(UL4Parser.COMMA)
                    self.state = 567
                    self.match(UL4Parser.STAR_STAR)
                    self.state = 568
                    localctx.rkwargsname = self.name()


                self.state = 572
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 571
                    self.match(UL4Parser.COMMA)


                self.state = 574
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass

            elif la_ == 5:
                localctx = UL4Parser.SignatureAnyParamsContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 576
                localctx.open_ = self.match(UL4Parser.PARENS_OPEN)
                self.state = 577
                localctx._name = self.name()
                localctx.names_without_defaults.append(localctx._name)
                self.state = 582
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,52,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 578
                        self.match(UL4Parser.COMMA)
                        self.state = 579
                        localctx._name = self.name()
                        localctx.names_without_defaults.append(localctx._name) 
                    self.state = 584
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,52,self._ctx)

                self.state = 592
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,53,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 585
                        self.match(UL4Parser.COMMA)
                        self.state = 586
                        localctx._name = self.name()
                        localctx.names_with_defaults.append(localctx._name)
                        self.state = 587
                        self.match(UL4Parser.ASSIGN)
                        self.state = 588
                        localctx._exprarg = self.exprarg()
                        localctx.defaults.append(localctx._exprarg) 
                    self.state = 594
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,53,self._ctx)

                self.state = 598
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
                if la_ == 1:
                    self.state = 595
                    self.match(UL4Parser.COMMA)
                    self.state = 596
                    self.match(UL4Parser.STAR)
                    self.state = 597
                    localctx.rargsname = self.name()


                self.state = 603
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
                if la_ == 1:
                    self.state = 600
                    self.match(UL4Parser.COMMA)
                    self.state = 601
                    self.match(UL4Parser.STAR_STAR)
                    self.state = 602
                    localctx.rkwargsname = self.name()


                self.state = 606
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 605
                    self.match(UL4Parser.COMMA)


                self.state = 608
                localctx.close = self.match(UL4Parser.PARENS_CLOSE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.n = None # NameContext
            self.sig = None # SignatureContext

        def EOF(self):
            return self.getToken(UL4Parser.EOF, 0)

        def name(self):
            return self.getTypedRuleContext(UL4Parser.NameContext,0)


        def signature(self):
            return self.getTypedRuleContext(UL4Parser.SignatureContext,0)


        def getRuleIndex(self):
            return UL4Parser.RULE_definition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = UL4Parser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_definition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 613
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.NAME:
                self.state = 612
                localctx.n = self.name()


            self.state = 616
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.PARENS_OPEN:
                self.state = 615
                localctx.sig = self.signature()


            self.state = 618
            self.match(UL4Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.content = None # BlockitemContext

        def MAYBETAG_DEF(self):
            return self.getToken(UL4Parser.MAYBETAG_DEF, 0)

        def definition(self):
            return self.getTypedRuleContext(UL4Parser.DefinitionContext,0)


        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def DEF(self):
            return self.getToken(UL4Parser.DEF, 0)

        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def getRuleIndex(self):
            return UL4Parser.RULE_defblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefblock" ):
                return visitor.visitDefblock(self)
            else:
                return visitor.visitChildren(self)




    def defblock(self):

        localctx = UL4Parser.DefblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_defblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 620
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 621
            self.match(UL4Parser.MAYBETAG_DEF)
            self.state = 622
            self.definition()
            self.state = 623
            self.match(UL4Parser.ENDDELIM)
            self.state = 627
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,60,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 624
                    localctx.content = self.blockitem() 
                self.state = 629
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,60,self._ctx)

            self.state = 630
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 631
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 633
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.DEF:
                self.state = 632
                self.match(UL4Parser.DEF)


            self.state = 635
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.var = None # NestedlvalueContext
            self.container = None # ExprContext
            self.content = None # BlockitemContext

        def MAYBETAG_FOR(self):
            return self.getToken(UL4Parser.MAYBETAG_FOR, 0)

        def IN(self):
            return self.getToken(UL4Parser.IN, 0)

        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def nestedlvalue(self):
            return self.getTypedRuleContext(UL4Parser.NestedlvalueContext,0)


        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def FOR(self):
            return self.getToken(UL4Parser.FOR, 0)

        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def getRuleIndex(self):
            return UL4Parser.RULE_forblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForblock" ):
                return visitor.visitForblock(self)
            else:
                return visitor.visitChildren(self)




    def forblock(self):

        localctx = UL4Parser.ForblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_forblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 637
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 638
            self.match(UL4Parser.MAYBETAG_FOR)
            self.state = 639
            localctx.var = self.nestedlvalue()
            self.state = 640
            self.match(UL4Parser.IN)
            self.state = 641
            localctx.container = self.expr(0)
            self.state = 642
            self.match(UL4Parser.ENDDELIM)
            self.state = 646
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,62,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 643
                    localctx.content = self.blockitem() 
                self.state = 648
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,62,self._ctx)

            self.state = 649
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 650
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 652
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.FOR:
                self.state = 651
                self.match(UL4Parser.FOR)


            self.state = 654
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.cond = None # ExprContext
            self.content = None # BlockitemContext

        def MAYBETAG_WHILE(self):
            return self.getToken(UL4Parser.MAYBETAG_WHILE, 0)

        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def WHILE(self):
            return self.getToken(UL4Parser.WHILE, 0)

        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def getRuleIndex(self):
            return UL4Parser.RULE_whileblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileblock" ):
                return visitor.visitWhileblock(self)
            else:
                return visitor.visitChildren(self)




    def whileblock(self):

        localctx = UL4Parser.WhileblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_whileblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 656
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 657
            self.match(UL4Parser.MAYBETAG_WHILE)
            self.state = 658
            localctx.cond = self.expr(0)
            self.state = 659
            self.match(UL4Parser.ENDDELIM)
            self.state = 663
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,64,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 660
                    localctx.content = self.blockitem() 
                self.state = 665
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,64,self._ctx)

            self.state = 666
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 667
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 669
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.WHILE:
                self.state = 668
                self.match(UL4Parser.WHILE)


            self.state = 671
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.cond = None # ExprContext
            self.content = None # BlockitemContext

        def MAYBETAG_IF(self):
            return self.getToken(UL4Parser.MAYBETAG_IF, 0)

        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ExprContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ExprContext,i)


        def MAYBETAG_ELSE(self):
            return self.getToken(UL4Parser.MAYBETAG_ELSE, 0)

        def MAYBETAG_ELIF(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.MAYBETAG_ELIF)
            else:
                return self.getToken(UL4Parser.MAYBETAG_ELIF, i)

        def IF(self):
            return self.getToken(UL4Parser.IF, 0)

        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def getRuleIndex(self):
            return UL4Parser.RULE_ifblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfblock" ):
                return visitor.visitIfblock(self)
            else:
                return visitor.visitChildren(self)




    def ifblock(self):

        localctx = UL4Parser.IfblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_ifblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 673
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 674
            self.match(UL4Parser.MAYBETAG_IF)
            self.state = 675
            localctx.cond = self.expr(0)
            self.state = 676
            self.match(UL4Parser.ENDDELIM)
            self.state = 680
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,66,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 677
                    localctx.content = self.blockitem() 
                self.state = 682
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,66,self._ctx)

            self.state = 695
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,68,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 683
                    _la = self._input.LA(1)
                    if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 684
                    self.match(UL4Parser.MAYBETAG_ELIF)
                    self.state = 685
                    localctx.cond = self.expr(0)
                    self.state = 686
                    self.match(UL4Parser.ENDDELIM)
                    self.state = 690
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,67,self._ctx)
                    while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                        if _alt==1:
                            self.state = 687
                            localctx.content = self.blockitem() 
                        self.state = 692
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,67,self._ctx)
             
                self.state = 697
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,68,self._ctx)

            self.state = 698
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 699
            self.match(UL4Parser.MAYBETAG_ELSE)
            self.state = 700
            self.match(UL4Parser.ENDDELIM)
            self.state = 704
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,69,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 701
                    localctx.content = self.blockitem() 
                self.state = 706
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,69,self._ctx)

            self.state = 707
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 708
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 710
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.IF:
                self.state = 709
                self.match(UL4Parser.IF)


            self.state = 712
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RenderblockblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.e1 = None # ExprContext
            self._argument = None # ArgumentContext
            self.args = list() # of ArgumentContexts
            self.close = None # Token
            self.content = None # BlockitemContext

        def MAYBETAG_RENDERBLOCK(self):
            return self.getToken(UL4Parser.MAYBETAG_RENDERBLOCK, 0)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)

        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)

        def RENDERBLOCK(self):
            return self.getToken(UL4Parser.RENDERBLOCK, 0)

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ArgumentContext,i)


        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def getRuleIndex(self):
            return UL4Parser.RULE_renderblockblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRenderblockblock" ):
                return visitor.visitRenderblockblock(self)
            else:
                return visitor.visitChildren(self)




    def renderblockblock(self):

        localctx = UL4Parser.RenderblockblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_renderblockblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 714
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 715
            self.match(UL4Parser.MAYBETAG_RENDERBLOCK)
            self.state = 716
            localctx.e1 = self.expr(0)
            self.state = 717
            self.match(UL4Parser.PARENS_OPEN)
            self.state = 731
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 30)) & ~0x3f) == 0 and ((1 << (_la - 30)) & ((1 << (UL4Parser.NOT - 30)) | (1 << (UL4Parser.NONE - 30)) | (1 << (UL4Parser.TRUE - 30)) | (1 << (UL4Parser.FALSE - 30)) | (1 << (UL4Parser.PARENS_OPEN - 30)) | (1 << (UL4Parser.BRACKET_OPEN - 30)) | (1 << (UL4Parser.BRACE_OPEN - 30)) | (1 << (UL4Parser.STAR_STAR - 30)) | (1 << (UL4Parser.STAR - 30)) | (1 << (UL4Parser.MINUS - 30)) | (1 << (UL4Parser.TILDE - 30)) | (1 << (UL4Parser.NAME - 30)) | (1 << (UL4Parser.INT - 30)) | (1 << (UL4Parser.FLOAT - 30)) | (1 << (UL4Parser.DATE - 30)) | (1 << (UL4Parser.DATETIME - 30)) | (1 << (UL4Parser.COLOR - 30)) | (1 << (UL4Parser.STRING - 30)) | (1 << (UL4Parser.STRING3 - 30)))) != 0):
                self.state = 718
                localctx._argument = self.argument()
                localctx.args.append(localctx._argument)
                self.state = 723
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,71,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 719
                        self.match(UL4Parser.COMMA)
                        self.state = 720
                        localctx._argument = self.argument()
                        localctx.args.append(localctx._argument) 
                    self.state = 725
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,71,self._ctx)

                self.state = 727
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 726
                    self.match(UL4Parser.COMMA)


                self.state = 733
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 734
            localctx.close = self.match(UL4Parser.PARENS_CLOSE)
            self.state = 735
            self.match(UL4Parser.ENDDELIM)
            self.state = 739
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,74,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 736
                    localctx.content = self.blockitem() 
                self.state = 741
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,74,self._ctx)

            self.state = 742
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 743
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 745
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.RENDERBLOCK:
                self.state = 744
                self.match(UL4Parser.RENDERBLOCK)


            self.state = 747
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RenderblocksblockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.e1 = None # ExprContext
            self._argument = None # ArgumentContext
            self.args = list() # of ArgumentContexts
            self.close = None # Token
            self.content = None # BlockitemContext

        def MAYBETAG_RENDERBLOCKS(self):
            return self.getToken(UL4Parser.MAYBETAG_RENDERBLOCKS, 0)

        def PARENS_OPEN(self):
            return self.getToken(UL4Parser.PARENS_OPEN, 0)

        def ENDDELIM(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.ENDDELIM)
            else:
                return self.getToken(UL4Parser.ENDDELIM, i)

        def MAYBETAG_END(self):
            return self.getToken(UL4Parser.MAYBETAG_END, 0)

        def DEFAULT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.DEFAULT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.DEFAULT_MAYBETAG, i)

        def TEXT_MAYBETAG(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.TEXT_MAYBETAG)
            else:
                return self.getToken(UL4Parser.TEXT_MAYBETAG, i)

        def expr(self):
            return self.getTypedRuleContext(UL4Parser.ExprContext,0)


        def PARENS_CLOSE(self):
            return self.getToken(UL4Parser.PARENS_CLOSE, 0)

        def RENDERBLOCKS(self):
            return self.getToken(UL4Parser.RENDERBLOCKS, 0)

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(UL4Parser.ArgumentContext,i)


        def blockitem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UL4Parser.BlockitemContext)
            else:
                return self.getTypedRuleContext(UL4Parser.BlockitemContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(UL4Parser.COMMA)
            else:
                return self.getToken(UL4Parser.COMMA, i)

        def getRuleIndex(self):
            return UL4Parser.RULE_renderblocksblock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRenderblocksblock" ):
                return visitor.visitRenderblocksblock(self)
            else:
                return visitor.visitChildren(self)




    def renderblocksblock(self):

        localctx = UL4Parser.RenderblocksblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_renderblocksblock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 749
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 750
            self.match(UL4Parser.MAYBETAG_RENDERBLOCKS)
            self.state = 751
            localctx.e1 = self.expr(0)
            self.state = 752
            self.match(UL4Parser.PARENS_OPEN)
            self.state = 766
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 30)) & ~0x3f) == 0 and ((1 << (_la - 30)) & ((1 << (UL4Parser.NOT - 30)) | (1 << (UL4Parser.NONE - 30)) | (1 << (UL4Parser.TRUE - 30)) | (1 << (UL4Parser.FALSE - 30)) | (1 << (UL4Parser.PARENS_OPEN - 30)) | (1 << (UL4Parser.BRACKET_OPEN - 30)) | (1 << (UL4Parser.BRACE_OPEN - 30)) | (1 << (UL4Parser.STAR_STAR - 30)) | (1 << (UL4Parser.STAR - 30)) | (1 << (UL4Parser.MINUS - 30)) | (1 << (UL4Parser.TILDE - 30)) | (1 << (UL4Parser.NAME - 30)) | (1 << (UL4Parser.INT - 30)) | (1 << (UL4Parser.FLOAT - 30)) | (1 << (UL4Parser.DATE - 30)) | (1 << (UL4Parser.DATETIME - 30)) | (1 << (UL4Parser.COLOR - 30)) | (1 << (UL4Parser.STRING - 30)) | (1 << (UL4Parser.STRING3 - 30)))) != 0):
                self.state = 753
                localctx._argument = self.argument()
                localctx.args.append(localctx._argument)
                self.state = 758
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,76,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 754
                        self.match(UL4Parser.COMMA)
                        self.state = 755
                        localctx._argument = self.argument()
                        localctx.args.append(localctx._argument) 
                    self.state = 760
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,76,self._ctx)

                self.state = 762
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==UL4Parser.COMMA:
                    self.state = 761
                    self.match(UL4Parser.COMMA)


                self.state = 768
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 769
            localctx.close = self.match(UL4Parser.PARENS_CLOSE)
            self.state = 770
            self.match(UL4Parser.ENDDELIM)
            self.state = 774
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,79,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 771
                    localctx.content = self.blockitem() 
                self.state = 776
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,79,self._ctx)

            self.state = 777
            _la = self._input.LA(1)
            if not(_la==UL4Parser.DEFAULT_MAYBETAG or _la==UL4Parser.TEXT_MAYBETAG):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 778
            self.match(UL4Parser.MAYBETAG_END)
            self.state = 780
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==UL4Parser.RENDERBLOCKS:
                self.state = 779
                self.match(UL4Parser.RENDERBLOCKS)


            self.state = 782
            self.match(UL4Parser.ENDDELIM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockitemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def defblock(self):
            return self.getTypedRuleContext(UL4Parser.DefblockContext,0)


        def forblock(self):
            return self.getTypedRuleContext(UL4Parser.ForblockContext,0)


        def whileblock(self):
            return self.getTypedRuleContext(UL4Parser.WhileblockContext,0)


        def ifblock(self):
            return self.getTypedRuleContext(UL4Parser.IfblockContext,0)


        def getRuleIndex(self):
            return UL4Parser.RULE_blockitem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockitem" ):
                return visitor.visitBlockitem(self)
            else:
                return visitor.visitChildren(self)




    def blockitem(self):

        localctx = UL4Parser.BlockitemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_blockitem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 788
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,81,self._ctx)
            if la_ == 1:
                self.state = 784
                self.defblock()
                pass

            elif la_ == 2:
                self.state = 785
                self.forblock()
                pass

            elif la_ == 3:
                self.state = 786
                self.whileblock()
                pass

            elif la_ == 4:
                self.state = 787
                self.ifblock()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TemplatebodyitemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return UL4Parser.RULE_templatebodyitem

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TemplateBodyItemContext(TemplatebodyitemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a UL4Parser.TemplatebodyitemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def whitespacetag(self):
            return self.getTypedRuleContext(UL4Parser.WhitespacetagContext,0)

        def notetag(self):
            return self.getTypedRuleContext(UL4Parser.NotetagContext,0)

        def defblock(self):
            return self.getTypedRuleContext(UL4Parser.DefblockContext,0)

        def forblock(self):
            return self.getTypedRuleContext(UL4Parser.ForblockContext,0)

        def whileblock(self):
            return self.getTypedRuleContext(UL4Parser.WhileblockContext,0)

        def ifblock(self):
            return self.getTypedRuleContext(UL4Parser.IfblockContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemplateBodyItem" ):
                return visitor.visitTemplateBodyItem(self)
            else:
                return visitor.visitChildren(self)



    def templatebodyitem(self):

        localctx = UL4Parser.TemplatebodyitemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_templatebodyitem)
        try:
            localctx = UL4Parser.TemplateBodyItemContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 796
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,82,self._ctx)
            if la_ == 1:
                self.state = 790
                self.whitespacetag()
                pass

            elif la_ == 2:
                self.state = 791
                self.notetag()
                pass

            elif la_ == 3:
                self.state = 792
                self.defblock()
                pass

            elif la_ == 4:
                self.state = 793
                self.forblock()
                pass

            elif la_ == 5:
                self.state = 794
                self.whileblock()
                pass

            elif la_ == 6:
                self.state = 795
                self.ifblock()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[20] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 25)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 24)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 23)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 22)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 14:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 16:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 17:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 18:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 19:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 20:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 21:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 22:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 23:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 24:
                return self.precpred(self._ctx, 31)
         

            if predIndex == 25:
                return self.precpred(self._ctx, 30)
         

            if predIndex == 26:
                return self.precpred(self._ctx, 29)
         

            if predIndex == 27:
                return self.precpred(self._ctx, 28)
         




