# Generated from src/ll/UL4Lexer.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2[")
        buf.write("\u0344\b\1\b\1\b\1\b\1\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5")
        buf.write("\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13")
        buf.write("\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t")
        buf.write("\21\4\22\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26")
        buf.write("\4\27\t\27\4\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34")
        buf.write("\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t")
        buf.write("\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4")
        buf.write("+\t+\4,\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62")
        buf.write("\t\62\4\63\t\63\4\64\t\64\4\65\t\65\4\66\t\66\4\67\t\67")
        buf.write("\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t")
        buf.write("@\4A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\t")
        buf.write("I\4J\tJ\4K\tK\4L\tL\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\t")
        buf.write("R\4S\tS\4T\tT\4U\tU\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t")
        buf.write("[\4\\\t\\\4]\t]\4^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4")
        buf.write("d\td\4e\te\4f\tf\3\2\6\2\u00d3\n\2\r\2\16\2\u00d4\3\2")
        buf.write("\3\2\3\3\5\3\u00da\n\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\5\6\5\u00e6\n\5\r\5\16\5\u00e7\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\7\6\7\u00f0\n\7\r\7\16\7\u00f1\3\b\6\b\u00f5\n")
        buf.write("\b\r\b\16\b\u00f6\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3")
        buf.write("\13\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3")
        buf.write("\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\26\6\26")
        buf.write("\u015c\n\26\r\26\16\26\u015d\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u016e")
        buf.write("\n\27\3\30\6\30\u0171\n\30\r\30\16\30\u0172\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33")
        buf.write("\3\33\3\34\3\34\3\34\3\35\3\35\3\35\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\37\3\37\3\37\3\37\3 \3 \3 \3!\3!\3!\3!\3\"\3\"")
        buf.write("\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3%\3")
        buf.write("&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3(\3")
        buf.write("(\3(\3(\3(\3(\3(\3)\3)\3)\3)\3)\3)\3)\3)\3)\3)\3)\3)\3")
        buf.write(")\3*\3*\3+\3+\3,\3,\3-\3-\3.\3.\3/\3/\3\60\3\60\3\60\3")
        buf.write("\61\3\61\3\62\3\62\3\63\3\63\3\64\3\64\3\64\3\65\3\65")
        buf.write("\3\66\3\66\3\67\3\67\3\67\38\38\38\39\39\39\3:\3:\3;\3")
        buf.write(";\3;\3<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3A\3A\3B\3B\3C\3C\3")
        buf.write("D\3D\3D\3E\3E\3E\3F\3F\3G\3G\3G\3H\3H\3H\3I\3I\3I\3J\3")
        buf.write("J\3J\3J\3K\3K\3K\3L\3L\3L\3M\3M\3M\3M\3N\3N\3N\3N\3O\3")
        buf.write("O\3O\3P\3P\3P\3Q\3Q\3Q\3R\3R\7R\u0237\nR\fR\16R\u023a")
        buf.write("\13R\3S\3S\3T\3T\3U\3U\3V\3V\3W\6W\u0245\nW\rW\16W\u0246")
        buf.write("\3W\3W\3W\6W\u024c\nW\rW\16W\u024d\3W\3W\3W\6W\u0253\n")
        buf.write("W\rW\16W\u0254\3W\3W\3W\6W\u025a\nW\rW\16W\u025b\5W\u025e")
        buf.write("\nW\3X\3X\5X\u0262\nX\3X\6X\u0265\nX\rX\16X\u0266\3Y\6")
        buf.write("Y\u026a\nY\rY\16Y\u026b\3Y\3Y\7Y\u0270\nY\fY\16Y\u0273")
        buf.write("\13Y\3Y\5Y\u0276\nY\3Y\3Y\6Y\u027a\nY\rY\16Y\u027b\3Y")
        buf.write("\5Y\u027f\nY\3Y\6Y\u0282\nY\rY\16Y\u0283\3Y\3Y\5Y\u0288")
        buf.write("\nY\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\3Z\5")
        buf.write("Z\u029a\nZ\5Z\u029c\nZ\3[\3[\3[\3[\3[\3[\3[\3[\3[\3[\3")
        buf.write("[\3[\3[\3[\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\\3\\")
        buf.write("\3\\\3\\\3\\\5\\\u02ba\n\\\3\\\3\\\3]\3]\3]\3]\3]\3]\3")
        buf.write("]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3]\3")
        buf.write("]\3]\3]\3]\3]\5]\u02db\n]\3^\3^\3^\3^\3_\3_\3_\7_\u02e4")
        buf.write("\n_\f_\16_\u02e7\13_\3_\3_\3_\3_\7_\u02ed\n_\f_\16_\u02f0")
        buf.write("\13_\3_\5_\u02f3\n_\3`\3`\3`\3`\3`\7`\u02fa\n`\f`\16`")
        buf.write("\u02fd\13`\3`\3`\3`\3`\3`\3`\3`\3`\7`\u0307\n`\f`\16`")
        buf.write("\u030a\13`\3`\3`\3`\5`\u030f\n`\3a\3a\3a\5a\u0314\na\3")
        buf.write("a\3a\6a\u0318\na\ra\16a\u0319\3b\3b\3b\5b\u031f\nb\3b")
        buf.write("\3b\6b\u0323\nb\rb\16b\u0324\3c\3c\3c\3c\3c\5c\u032c\n")
        buf.write("c\3d\3d\3d\3d\3d\3e\3e\3e\3e\3e\3e\3e\3f\3f\3f\3f\3f\3")
        buf.write("f\3f\3f\3f\3f\3f\7\u00e7\u00f1\u015d\u02fb\u0308\2g\7")
        buf.write("\3\t\4\13\5\r\6\17\7\21\b\23\t\25\n\27\13\31\f\33\r\35")
        buf.write("\16\37\17!\20#\21%\22\'\23)\24+\25-\26/\27\61\30\63\31")
        buf.write("\65\32\67\339\34;\35=\36?\37A C!E\"G#I$K%M&O\'Q(S)U*W")
        buf.write("+Y,[-]._/a\60c\61e\62g\63i\64k\65m\66o\67q8s9u:w;y<{=")
        buf.write("}>\177?\u0081@\u0083A\u0085B\u0087C\u0089D\u008bE\u008d")
        buf.write("F\u008fG\u0091H\u0093I\u0095J\u0097K\u0099L\u009bM\u009d")
        buf.write("N\u009fO\u00a1P\u00a3Q\u00a5R\u00a7S\u00a9\2\u00ab\2\u00ad")
        buf.write("\2\u00af\2\u00b1T\u00b3\2\u00b5U\u00b7\2\u00b9V\u00bb")
        buf.write("W\u00bdX\u00bfY\u00c1Z\u00c3[\u00c5\2\u00c7\2\u00c9\2")
        buf.write("\u00cb\2\u00cd\2\u00cf\2\7\2\3\4\5\6\21\4\2\13\13\"\"")
        buf.write("\5\2\13\f\17\17\"\"\5\2C\\aac|\6\2\62;C\\aac|\5\2\62;")
        buf.write("CHch\4\2DDdd\4\2QQqq\4\2ZZzz\4\2GGgg\4\2--//\6\2\f\f\17")
        buf.write("\17$$^^\6\2\f\f\17\17))^^\4\2$$^^\4\2))^^\n\2$$))^^cd")
        buf.write("hhppttvv\2\u0367\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\3\17\3\2\2\2\3\21\3\2\2\2\4\23\3\2\2\2\4")
        buf.write("\25\3\2\2\2\4\27\3\2\2\2\4\31\3\2\2\2\4\33\3\2\2\2\4\35")
        buf.write("\3\2\2\2\4\37\3\2\2\2\4!\3\2\2\2\4#\3\2\2\2\4%\3\2\2\2")
        buf.write("\4\'\3\2\2\2\4)\3\2\2\2\4+\3\2\2\2\4-\3\2\2\2\4/\3\2\2")
        buf.write("\2\5\61\3\2\2\2\5\63\3\2\2\2\5\65\3\2\2\2\6\67\3\2\2\2")
        buf.write("\69\3\2\2\2\6;\3\2\2\2\6=\3\2\2\2\6?\3\2\2\2\6A\3\2\2")
        buf.write("\2\6C\3\2\2\2\6E\3\2\2\2\6G\3\2\2\2\6I\3\2\2\2\6K\3\2")
        buf.write("\2\2\6M\3\2\2\2\6O\3\2\2\2\6Q\3\2\2\2\6S\3\2\2\2\6U\3")
        buf.write("\2\2\2\6W\3\2\2\2\6Y\3\2\2\2\6[\3\2\2\2\6]\3\2\2\2\6_")
        buf.write("\3\2\2\2\6a\3\2\2\2\6c\3\2\2\2\6e\3\2\2\2\6g\3\2\2\2\6")
        buf.write("i\3\2\2\2\6k\3\2\2\2\6m\3\2\2\2\6o\3\2\2\2\6q\3\2\2\2")
        buf.write("\6s\3\2\2\2\6u\3\2\2\2\6w\3\2\2\2\6y\3\2\2\2\6{\3\2\2")
        buf.write("\2\6}\3\2\2\2\6\177\3\2\2\2\6\u0081\3\2\2\2\6\u0083\3")
        buf.write("\2\2\2\6\u0085\3\2\2\2\6\u0087\3\2\2\2\6\u0089\3\2\2\2")
        buf.write("\6\u008b\3\2\2\2\6\u008d\3\2\2\2\6\u008f\3\2\2\2\6\u0091")
        buf.write("\3\2\2\2\6\u0093\3\2\2\2\6\u0095\3\2\2\2\6\u0097\3\2\2")
        buf.write("\2\6\u0099\3\2\2\2\6\u009b\3\2\2\2\6\u009d\3\2\2\2\6\u009f")
        buf.write("\3\2\2\2\6\u00a1\3\2\2\2\6\u00a3\3\2\2\2\6\u00a5\3\2\2")
        buf.write("\2\6\u00a7\3\2\2\2\6\u00b1\3\2\2\2\6\u00b5\3\2\2\2\6\u00b9")
        buf.write("\3\2\2\2\6\u00bb\3\2\2\2\6\u00bd\3\2\2\2\6\u00bf\3\2\2")
        buf.write("\2\6\u00c1\3\2\2\2\6\u00c3\3\2\2\2\7\u00d2\3\2\2\2\t\u00d9")
        buf.write("\3\2\2\2\13\u00df\3\2\2\2\r\u00e5\3\2\2\2\17\u00e9\3\2")
        buf.write("\2\2\21\u00ef\3\2\2\2\23\u00f4\3\2\2\2\25\u00f8\3\2\2")
        buf.write("\2\27\u0105\3\2\2\2\31\u0109\3\2\2\2\33\u010e\3\2\2\2")
        buf.write("\35\u0114\3\2\2\2\37\u011a\3\2\2\2!\u0120\3\2\2\2#\u0128")
        buf.write("\3\2\2\2%\u012d\3\2\2\2\'\u0134\3\2\2\2)\u0139\3\2\2\2")
        buf.write("+\u0147\3\2\2\2-\u0156\3\2\2\2/\u015b\3\2\2\2\61\u016d")
        buf.write("\3\2\2\2\63\u0170\3\2\2\2\65\u0174\3\2\2\2\67\u0179\3")
        buf.write("\2\2\29\u017e\3\2\2\2;\u0182\3\2\2\2=\u0185\3\2\2\2?\u0188")
        buf.write("\3\2\2\2A\u018d\3\2\2\2C\u0191\3\2\2\2E\u0194\3\2\2\2")
        buf.write("G\u0198\3\2\2\2I\u019b\3\2\2\2K\u01a0\3\2\2\2M\u01a5\3")
        buf.write("\2\2\2O\u01ab\3\2\2\2Q\u01af\3\2\2\2S\u01b5\3\2\2\2U\u01c1")
        buf.write("\3\2\2\2W\u01ce\3\2\2\2Y\u01d0\3\2\2\2[\u01d2\3\2\2\2")
        buf.write("]\u01d4\3\2\2\2_\u01d6\3\2\2\2a\u01d8\3\2\2\2c\u01da\3")
        buf.write("\2\2\2e\u01dd\3\2\2\2g\u01df\3\2\2\2i\u01e1\3\2\2\2k\u01e3")
        buf.write("\3\2\2\2m\u01e6\3\2\2\2o\u01e8\3\2\2\2q\u01ea\3\2\2\2")
        buf.write("s\u01ed\3\2\2\2u\u01f0\3\2\2\2w\u01f3\3\2\2\2y\u01f5\3")
        buf.write("\2\2\2{\u01f8\3\2\2\2}\u01fa\3\2\2\2\177\u01fc\3\2\2\2")
        buf.write("\u0081\u01fe\3\2\2\2\u0083\u0200\3\2\2\2\u0085\u0202\3")
        buf.write("\2\2\2\u0087\u0204\3\2\2\2\u0089\u0206\3\2\2\2\u008b\u0208")
        buf.write("\3\2\2\2\u008d\u020b\3\2\2\2\u008f\u020e\3\2\2\2\u0091")
        buf.write("\u0210\3\2\2\2\u0093\u0213\3\2\2\2\u0095\u0216\3\2\2\2")
        buf.write("\u0097\u0219\3\2\2\2\u0099\u021d\3\2\2\2\u009b\u0220\3")
        buf.write("\2\2\2\u009d\u0223\3\2\2\2\u009f\u0227\3\2\2\2\u00a1\u022b")
        buf.write("\3\2\2\2\u00a3\u022e\3\2\2\2\u00a5\u0231\3\2\2\2\u00a7")
        buf.write("\u0234\3\2\2\2\u00a9\u023b\3\2\2\2\u00ab\u023d\3\2\2\2")
        buf.write("\u00ad\u023f\3\2\2\2\u00af\u0241\3\2\2\2\u00b1\u025d\3")
        buf.write("\2\2\2\u00b3\u025f\3\2\2\2\u00b5\u0287\3\2\2\2\u00b7\u0289")
        buf.write("\3\2\2\2\u00b9\u029d\3\2\2\2\u00bb\u02ab\3\2\2\2\u00bd")
        buf.write("\u02da\3\2\2\2\u00bf\u02dc\3\2\2\2\u00c1\u02f2\3\2\2\2")
        buf.write("\u00c3\u030e\3\2\2\2\u00c5\u0313\3\2\2\2\u00c7\u031e\3")
        buf.write("\2\2\2\u00c9\u032b\3\2\2\2\u00cb\u032d\3\2\2\2\u00cd\u0332")
        buf.write("\3\2\2\2\u00cf\u0339\3\2\2\2\u00d1\u00d3\t\2\2\2\u00d2")
        buf.write("\u00d1\3\2\2\2\u00d3\u00d4\3\2\2\2\u00d4\u00d2\3\2\2\2")
        buf.write("\u00d4\u00d5\3\2\2\2\u00d5\u00d6\3\2\2\2\u00d6\u00d7\b")
        buf.write("\2\2\2\u00d7\b\3\2\2\2\u00d8\u00da\7\17\2\2\u00d9\u00d8")
        buf.write("\3\2\2\2\u00d9\u00da\3\2\2\2\u00da\u00db\3\2\2\2\u00db")
        buf.write("\u00dc\7\f\2\2\u00dc\u00dd\3\2\2\2\u00dd\u00de\b\3\3\2")
        buf.write("\u00de\n\3\2\2\2\u00df\u00e0\7>\2\2\u00e0\u00e1\7A\2\2")
        buf.write("\u00e1\u00e2\3\2\2\2\u00e2\u00e3\b\4\4\2\u00e3\f\3\2\2")
        buf.write("\2\u00e4\u00e6\13\2\2\2\u00e5\u00e4\3\2\2\2\u00e6\u00e7")
        buf.write("\3\2\2\2\u00e7\u00e8\3\2\2\2\u00e7\u00e5\3\2\2\2\u00e8")
        buf.write("\16\3\2\2\2\u00e9\u00ea\7>\2\2\u00ea\u00eb\7A\2\2\u00eb")
        buf.write("\u00ec\3\2\2\2\u00ec\u00ed\b\6\4\2\u00ed\20\3\2\2\2\u00ee")
        buf.write("\u00f0\13\2\2\2\u00ef\u00ee\3\2\2\2\u00f0\u00f1\3\2\2")
        buf.write("\2\u00f1\u00f2\3\2\2\2\u00f1\u00ef\3\2\2\2\u00f2\22\3")
        buf.write("\2\2\2\u00f3\u00f5\t\3\2\2\u00f4\u00f3\3\2\2\2\u00f5\u00f6")
        buf.write("\3\2\2\2\u00f6\u00f4\3\2\2\2\u00f6\u00f7\3\2\2\2\u00f7")
        buf.write("\24\3\2\2\2\u00f8\u00f9\7y\2\2\u00f9\u00fa\7j\2\2\u00fa")
        buf.write("\u00fb\7k\2\2\u00fb\u00fc\7v\2\2\u00fc\u00fd\7g\2\2\u00fd")
        buf.write("\u00fe\7u\2\2\u00fe\u00ff\7r\2\2\u00ff\u0100\7c\2\2\u0100")
        buf.write("\u0101\7e\2\2\u0101\u0102\7g\2\2\u0102\u0103\3\2\2\2\u0103")
        buf.write("\u0104\b\t\5\2\u0104\26\3\2\2\2\u0105\u0106\7f\2\2\u0106")
        buf.write("\u0107\7q\2\2\u0107\u0108\7e\2\2\u0108\30\3\2\2\2\u0109")
        buf.write("\u010a\7p\2\2\u010a\u010b\7q\2\2\u010b\u010c\7v\2\2\u010c")
        buf.write("\u010d\7g\2\2\u010d\32\3\2\2\2\u010e\u010f\7w\2\2\u010f")
        buf.write("\u0110\7n\2\2\u0110\u0111\7\66\2\2\u0111\u0112\3\2\2\2")
        buf.write("\u0112\u0113\b\f\6\2\u0113\34\3\2\2\2\u0114\u0115\7f\2")
        buf.write("\2\u0115\u0116\7g\2\2\u0116\u0117\7h\2\2\u0117\u0118\3")
        buf.write("\2\2\2\u0118\u0119\b\r\6\2\u0119\36\3\2\2\2\u011a\u011b")
        buf.write("\7h\2\2\u011b\u011c\7q\2\2\u011c\u011d\7t\2\2\u011d\u011e")
        buf.write("\3\2\2\2\u011e\u011f\b\16\6\2\u011f \3\2\2\2\u0120\u0121")
        buf.write("\7y\2\2\u0121\u0122\7j\2\2\u0122\u0123\7k\2\2\u0123\u0124")
        buf.write("\7n\2\2\u0124\u0125\7g\2\2\u0125\u0126\3\2\2\2\u0126\u0127")
        buf.write("\b\17\6\2\u0127\"\3\2\2\2\u0128\u0129\7k\2\2\u0129\u012a")
        buf.write("\7h\2\2\u012a\u012b\3\2\2\2\u012b\u012c\b\20\6\2\u012c")
        buf.write("$\3\2\2\2\u012d\u012e\7g\2\2\u012e\u012f\7n\2\2\u012f")
        buf.write("\u0130\7k\2\2\u0130\u0131\7h\2\2\u0131\u0132\3\2\2\2\u0132")
        buf.write("\u0133\b\21\6\2\u0133&\3\2\2\2\u0134\u0135\7g\2\2\u0135")
        buf.write("\u0136\7n\2\2\u0136\u0137\7u\2\2\u0137\u0138\7g\2\2\u0138")
        buf.write("(\3\2\2\2\u0139\u013a\7t\2\2\u013a\u013b\7g\2\2\u013b")
        buf.write("\u013c\7p\2\2\u013c\u013d\7f\2\2\u013d\u013e\7g\2\2\u013e")
        buf.write("\u013f\7t\2\2\u013f\u0140\7d\2\2\u0140\u0141\7n\2\2\u0141")
        buf.write("\u0142\7q\2\2\u0142\u0143\7e\2\2\u0143\u0144\7m\2\2\u0144")
        buf.write("\u0145\3\2\2\2\u0145\u0146\b\23\6\2\u0146*\3\2\2\2\u0147")
        buf.write("\u0148\7t\2\2\u0148\u0149\7g\2\2\u0149\u014a\7p\2\2\u014a")
        buf.write("\u014b\7f\2\2\u014b\u014c\7g\2\2\u014c\u014d\7t\2\2\u014d")
        buf.write("\u014e\7d\2\2\u014e\u014f\7n\2\2\u014f\u0150\7q\2\2\u0150")
        buf.write("\u0151\7e\2\2\u0151\u0152\7m\2\2\u0152\u0153\7u\2\2\u0153")
        buf.write("\u0154\3\2\2\2\u0154\u0155\b\24\6\2\u0155,\3\2\2\2\u0156")
        buf.write("\u0157\7g\2\2\u0157\u0158\7p\2\2\u0158\u0159\7f\2\2\u0159")
        buf.write(".\3\2\2\2\u015a\u015c\13\2\2\2\u015b\u015a\3\2\2\2\u015c")
        buf.write("\u015d\3\2\2\2\u015d\u015e\3\2\2\2\u015d\u015b\3\2\2\2")
        buf.write("\u015e\60\3\2\2\2\u015f\u0160\7m\2\2\u0160\u0161\7g\2")
        buf.write("\2\u0161\u0162\7g\2\2\u0162\u016e\7r\2\2\u0163\u0164\7")
        buf.write("u\2\2\u0164\u0165\7o\2\2\u0165\u0166\7c\2\2\u0166\u0167")
        buf.write("\7t\2\2\u0167\u016e\7v\2\2\u0168\u0169\7u\2\2\u0169\u016a")
        buf.write("\7v\2\2\u016a\u016b\7t\2\2\u016b\u016c\7k\2\2\u016c\u016e")
        buf.write("\7r\2\2\u016d\u015f\3\2\2\2\u016d\u0163\3\2\2\2\u016d")
        buf.write("\u0168\3\2\2\2\u016e\62\3\2\2\2\u016f\u0171\t\3\2\2\u0170")
        buf.write("\u016f\3\2\2\2\u0171\u0172\3\2\2\2\u0172\u0170\3\2\2\2")
        buf.write("\u0172\u0173\3\2\2\2\u0173\64\3\2\2\2\u0174\u0175\7A\2")
        buf.write("\2\u0175\u0176\7@\2\2\u0176\u0177\3\2\2\2\u0177\u0178")
        buf.write("\b\31\7\2\u0178\66\3\2\2\2\u0179\u017a\7A\2\2\u017a\u017b")
        buf.write("\7@\2\2\u017b\u017c\3\2\2\2\u017c\u017d\b\32\7\2\u017d")
        buf.write("8\3\2\2\2\u017e\u017f\7h\2\2\u017f\u0180\7q\2\2\u0180")
        buf.write("\u0181\7t\2\2\u0181:\3\2\2\2\u0182\u0183\7k\2\2\u0183")
        buf.write("\u0184\7p\2\2\u0184<\3\2\2\2\u0185\u0186\7k\2\2\u0186")
        buf.write("\u0187\7h\2\2\u0187>\3\2\2\2\u0188\u0189\7g\2\2\u0189")
        buf.write("\u018a\7n\2\2\u018a\u018b\7u\2\2\u018b\u018c\7g\2\2\u018c")
        buf.write("@\3\2\2\2\u018d\u018e\7p\2\2\u018e\u018f\7q\2\2\u018f")
        buf.write("\u0190\7v\2\2\u0190B\3\2\2\2\u0191\u0192\7k\2\2\u0192")
        buf.write("\u0193\7u\2\2\u0193D\3\2\2\2\u0194\u0195\7c\2\2\u0195")
        buf.write("\u0196\7p\2\2\u0196\u0197\7f\2\2\u0197F\3\2\2\2\u0198")
        buf.write("\u0199\7q\2\2\u0199\u019a\7t\2\2\u019aH\3\2\2\2\u019b")
        buf.write("\u019c\7P\2\2\u019c\u019d\7q\2\2\u019d\u019e\7p\2\2\u019e")
        buf.write("\u019f\7g\2\2\u019fJ\3\2\2\2\u01a0\u01a1\7V\2\2\u01a1")
        buf.write("\u01a2\7t\2\2\u01a2\u01a3\7w\2\2\u01a3\u01a4\7g\2\2\u01a4")
        buf.write("L\3\2\2\2\u01a5\u01a6\7H\2\2\u01a6\u01a7\7c\2\2\u01a7")
        buf.write("\u01a8\7n\2\2\u01a8\u01a9\7u\2\2\u01a9\u01aa\7g\2\2\u01aa")
        buf.write("N\3\2\2\2\u01ab\u01ac\7f\2\2\u01ac\u01ad\7g\2\2\u01ad")
        buf.write("\u01ae\7h\2\2\u01aeP\3\2\2\2\u01af\u01b0\7y\2\2\u01b0")
        buf.write("\u01b1\7j\2\2\u01b1\u01b2\7k\2\2\u01b2\u01b3\7n\2\2\u01b3")
        buf.write("\u01b4\7g\2\2\u01b4R\3\2\2\2\u01b5\u01b6\7t\2\2\u01b6")
        buf.write("\u01b7\7g\2\2\u01b7\u01b8\7p\2\2\u01b8\u01b9\7f\2\2\u01b9")
        buf.write("\u01ba\7g\2\2\u01ba\u01bb\7t\2\2\u01bb\u01bc\7d\2\2\u01bc")
        buf.write("\u01bd\7n\2\2\u01bd\u01be\7q\2\2\u01be\u01bf\7e\2\2\u01bf")
        buf.write("\u01c0\7m\2\2\u01c0T\3\2\2\2\u01c1\u01c2\7t\2\2\u01c2")
        buf.write("\u01c3\7g\2\2\u01c3\u01c4\7p\2\2\u01c4\u01c5\7f\2\2\u01c5")
        buf.write("\u01c6\7g\2\2\u01c6\u01c7\7t\2\2\u01c7\u01c8\7d\2\2\u01c8")
        buf.write("\u01c9\7n\2\2\u01c9\u01ca\7q\2\2\u01ca\u01cb\7e\2\2\u01cb")
        buf.write("\u01cc\7m\2\2\u01cc\u01cd\7u\2\2\u01cdV\3\2\2\2\u01ce")
        buf.write("\u01cf\7*\2\2\u01cfX\3\2\2\2\u01d0\u01d1\7+\2\2\u01d1")
        buf.write("Z\3\2\2\2\u01d2\u01d3\7]\2\2\u01d3\\\3\2\2\2\u01d4\u01d5")
        buf.write("\7_\2\2\u01d5^\3\2\2\2\u01d6\u01d7\7}\2\2\u01d7`\3\2\2")
        buf.write("\2\u01d8\u01d9\7\177\2\2\u01d9b\3\2\2\2\u01da\u01db\7")
        buf.write(",\2\2\u01db\u01dc\7,\2\2\u01dcd\3\2\2\2\u01dd\u01de\7")
        buf.write(",\2\2\u01def\3\2\2\2\u01df\u01e0\7-\2\2\u01e0h\3\2\2\2")
        buf.write("\u01e1\u01e2\7/\2\2\u01e2j\3\2\2\2\u01e3\u01e4\7\61\2")
        buf.write("\2\u01e4\u01e5\7\61\2\2\u01e5l\3\2\2\2\u01e6\u01e7\7\61")
        buf.write("\2\2\u01e7n\3\2\2\2\u01e8\u01e9\7\'\2\2\u01e9p\3\2\2\2")
        buf.write("\u01ea\u01eb\7?\2\2\u01eb\u01ec\7?\2\2\u01ecr\3\2\2\2")
        buf.write("\u01ed\u01ee\7#\2\2\u01ee\u01ef\7?\2\2\u01eft\3\2\2\2")
        buf.write("\u01f0\u01f1\7>\2\2\u01f1\u01f2\7?\2\2\u01f2v\3\2\2\2")
        buf.write("\u01f3\u01f4\7>\2\2\u01f4x\3\2\2\2\u01f5\u01f6\7@\2\2")
        buf.write("\u01f6\u01f7\7?\2\2\u01f7z\3\2\2\2\u01f8\u01f9\7@\2\2")
        buf.write("\u01f9|\3\2\2\2\u01fa\u01fb\7?\2\2\u01fb~\3\2\2\2\u01fc")
        buf.write("\u01fd\7.\2\2\u01fd\u0080\3\2\2\2\u01fe\u01ff\7<\2\2\u01ff")
        buf.write("\u0082\3\2\2\2\u0200\u0201\7\u0080\2\2\u0201\u0084\3\2")
        buf.write("\2\2\u0202\u0203\7(\2\2\u0203\u0086\3\2\2\2\u0204\u0205")
        buf.write("\7`\2\2\u0205\u0088\3\2\2\2\u0206\u0207\7\60\2\2\u0207")
        buf.write("\u008a\3\2\2\2\u0208\u0209\7>\2\2\u0209\u020a\7>\2\2\u020a")
        buf.write("\u008c\3\2\2\2\u020b\u020c\7@\2\2\u020c\u020d\7@\2\2\u020d")
        buf.write("\u008e\3\2\2\2\u020e\u020f\7~\2\2\u020f\u0090\3\2\2\2")
        buf.write("\u0210\u0211\7-\2\2\u0211\u0212\7?\2\2\u0212\u0092\3\2")
        buf.write("\2\2\u0213\u0214\7/\2\2\u0214\u0215\7?\2\2\u0215\u0094")
        buf.write("\3\2\2\2\u0216\u0217\7,\2\2\u0217\u0218\7?\2\2\u0218\u0096")
        buf.write("\3\2\2\2\u0219\u021a\7\61\2\2\u021a\u021b\7\61\2\2\u021b")
        buf.write("\u021c\7?\2\2\u021c\u0098\3\2\2\2\u021d\u021e\7\61\2\2")
        buf.write("\u021e\u021f\7?\2\2\u021f\u009a\3\2\2\2\u0220\u0221\7")
        buf.write("\'\2\2\u0221\u0222\7?\2\2\u0222\u009c\3\2\2\2\u0223\u0224")
        buf.write("\7>\2\2\u0224\u0225\7>\2\2\u0225\u0226\7?\2\2\u0226\u009e")
        buf.write("\3\2\2\2\u0227\u0228\7@\2\2\u0228\u0229\7@\2\2\u0229\u022a")
        buf.write("\7?\2\2\u022a\u00a0\3\2\2\2\u022b\u022c\7(\2\2\u022c\u022d")
        buf.write("\7?\2\2\u022d\u00a2\3\2\2\2\u022e\u022f\7`\2\2\u022f\u0230")
        buf.write("\7?\2\2\u0230\u00a4\3\2\2\2\u0231\u0232\7~\2\2\u0232\u0233")
        buf.write("\7?\2\2\u0233\u00a6\3\2\2\2\u0234\u0238\t\4\2\2\u0235")
        buf.write("\u0237\t\5\2\2\u0236\u0235\3\2\2\2\u0237\u023a\3\2\2\2")
        buf.write("\u0238\u0236\3\2\2\2\u0238\u0239\3\2\2\2\u0239\u00a8\3")
        buf.write("\2\2\2\u023a\u0238\3\2\2\2\u023b\u023c\4\62;\2\u023c\u00aa")
        buf.write("\3\2\2\2\u023d\u023e\4\62\63\2\u023e\u00ac\3\2\2\2\u023f")
        buf.write("\u0240\4\629\2\u0240\u00ae\3\2\2\2\u0241\u0242\t\6\2\2")
        buf.write("\u0242\u00b0\3\2\2\2\u0243\u0245\5\u00a9S\2\u0244\u0243")
        buf.write("\3\2\2\2\u0245\u0246\3\2\2\2\u0246\u0244\3\2\2\2\u0246")
        buf.write("\u0247\3\2\2\2\u0247\u025e\3\2\2\2\u0248\u0249\7\62\2")
        buf.write("\2\u0249\u024b\t\7\2\2\u024a\u024c\5\u00abT\2\u024b\u024a")
        buf.write("\3\2\2\2\u024c\u024d\3\2\2\2\u024d\u024b\3\2\2\2\u024d")
        buf.write("\u024e\3\2\2\2\u024e\u025e\3\2\2\2\u024f\u0250\7\62\2")
        buf.write("\2\u0250\u0252\t\b\2\2\u0251\u0253\5\u00adU\2\u0252\u0251")
        buf.write("\3\2\2\2\u0253\u0254\3\2\2\2\u0254\u0252\3\2\2\2\u0254")
        buf.write("\u0255\3\2\2\2\u0255\u025e\3\2\2\2\u0256\u0257\7\62\2")
        buf.write("\2\u0257\u0259\t\t\2\2\u0258\u025a\5\u00afV\2\u0259\u0258")
        buf.write("\3\2\2\2\u025a\u025b\3\2\2\2\u025b\u0259\3\2\2\2\u025b")
        buf.write("\u025c\3\2\2\2\u025c\u025e\3\2\2\2\u025d\u0244\3\2\2\2")
        buf.write("\u025d\u0248\3\2\2\2\u025d\u024f\3\2\2\2\u025d\u0256\3")
        buf.write("\2\2\2\u025e\u00b2\3\2\2\2\u025f\u0261\t\n\2\2\u0260\u0262")
        buf.write("\t\13\2\2\u0261\u0260\3\2\2\2\u0261\u0262\3\2\2\2\u0262")
        buf.write("\u0264\3\2\2\2\u0263\u0265\5\u00a9S\2\u0264\u0263\3\2")
        buf.write("\2\2\u0265\u0266\3\2\2\2\u0266\u0264\3\2\2\2\u0266\u0267")
        buf.write("\3\2\2\2\u0267\u00b4\3\2\2\2\u0268\u026a\5\u00a9S\2\u0269")
        buf.write("\u0268\3\2\2\2\u026a\u026b\3\2\2\2\u026b\u0269\3\2\2\2")
        buf.write("\u026b\u026c\3\2\2\2\u026c\u026d\3\2\2\2\u026d\u0271\7")
        buf.write("\60\2\2\u026e\u0270\5\u00a9S\2\u026f\u026e\3\2\2\2\u0270")
        buf.write("\u0273\3\2\2\2\u0271\u026f\3\2\2\2\u0271\u0272\3\2\2\2")
        buf.write("\u0272\u0275\3\2\2\2\u0273\u0271\3\2\2\2\u0274\u0276\5")
        buf.write("\u00b3X\2\u0275\u0274\3\2\2\2\u0275\u0276\3\2\2\2\u0276")
        buf.write("\u0288\3\2\2\2\u0277\u0279\7\60\2\2\u0278\u027a\5\u00a9")
        buf.write("S\2\u0279\u0278\3\2\2\2\u027a\u027b\3\2\2\2\u027b\u0279")
        buf.write("\3\2\2\2\u027b\u027c\3\2\2\2\u027c\u027e\3\2\2\2\u027d")
        buf.write("\u027f\5\u00b3X\2\u027e\u027d\3\2\2\2\u027e\u027f\3\2")
        buf.write("\2\2\u027f\u0288\3\2\2\2\u0280\u0282\5\u00a9S\2\u0281")
        buf.write("\u0280\3\2\2\2\u0282\u0283\3\2\2\2\u0283\u0281\3\2\2\2")
        buf.write("\u0283\u0284\3\2\2\2\u0284\u0285\3\2\2\2\u0285\u0286\5")
        buf.write("\u00b3X\2\u0286\u0288\3\2\2\2\u0287\u0269\3\2\2\2\u0287")
        buf.write("\u0277\3\2\2\2\u0287\u0281\3\2\2\2\u0288\u00b6\3\2\2\2")
        buf.write("\u0289\u028a\5\u00a9S\2\u028a\u028b\5\u00a9S\2\u028b\u028c")
        buf.write("\7<\2\2\u028c\u028d\5\u00a9S\2\u028d\u029b\5\u00a9S\2")
        buf.write("\u028e\u028f\7<\2\2\u028f\u0290\5\u00a9S\2\u0290\u0299")
        buf.write("\5\u00a9S\2\u0291\u0292\7\60\2\2\u0292\u0293\5\u00a9S")
        buf.write("\2\u0293\u0294\5\u00a9S\2\u0294\u0295\5\u00a9S\2\u0295")
        buf.write("\u0296\5\u00a9S\2\u0296\u0297\5\u00a9S\2\u0297\u0298\5")
        buf.write("\u00a9S\2\u0298\u029a\3\2\2\2\u0299\u0291\3\2\2\2\u0299")
        buf.write("\u029a\3\2\2\2\u029a\u029c\3\2\2\2\u029b\u028e\3\2\2\2")
        buf.write("\u029b\u029c\3\2\2\2\u029c\u00b8\3\2\2\2\u029d\u029e\7")
        buf.write("B\2\2\u029e\u029f\7*\2\2\u029f\u02a0\5\u00a9S\2\u02a0")
        buf.write("\u02a1\5\u00a9S\2\u02a1\u02a2\5\u00a9S\2\u02a2\u02a3\5")
        buf.write("\u00a9S\2\u02a3\u02a4\7/\2\2\u02a4\u02a5\5\u00a9S\2\u02a5")
        buf.write("\u02a6\5\u00a9S\2\u02a6\u02a7\7/\2\2\u02a7\u02a8\5\u00a9")
        buf.write("S\2\u02a8\u02a9\5\u00a9S\2\u02a9\u02aa\7+\2\2\u02aa\u00ba")
        buf.write("\3\2\2\2\u02ab\u02ac\7B\2\2\u02ac\u02ad\7*\2\2\u02ad\u02ae")
        buf.write("\5\u00a9S\2\u02ae\u02af\5\u00a9S\2\u02af\u02b0\5\u00a9")
        buf.write("S\2\u02b0\u02b1\5\u00a9S\2\u02b1\u02b2\7/\2\2\u02b2\u02b3")
        buf.write("\5\u00a9S\2\u02b3\u02b4\5\u00a9S\2\u02b4\u02b5\7/\2\2")
        buf.write("\u02b5\u02b6\5\u00a9S\2\u02b6\u02b7\5\u00a9S\2\u02b7\u02b9")
        buf.write("\7V\2\2\u02b8\u02ba\5\u00b7Z\2\u02b9\u02b8\3\2\2\2\u02b9")
        buf.write("\u02ba\3\2\2\2\u02ba\u02bb\3\2\2\2\u02bb\u02bc\7+\2\2")
        buf.write("\u02bc\u00bc\3\2\2\2\u02bd\u02be\7%\2\2\u02be\u02bf\5")
        buf.write("\u00afV\2\u02bf\u02c0\5\u00afV\2\u02c0\u02c1\5\u00afV")
        buf.write("\2\u02c1\u02db\3\2\2\2\u02c2\u02c3\7%\2\2\u02c3\u02c4")
        buf.write("\5\u00afV\2\u02c4\u02c5\5\u00afV\2\u02c5\u02c6\5\u00af")
        buf.write("V\2\u02c6\u02c7\5\u00afV\2\u02c7\u02db\3\2\2\2\u02c8\u02c9")
        buf.write("\7%\2\2\u02c9\u02ca\5\u00afV\2\u02ca\u02cb\5\u00afV\2")
        buf.write("\u02cb\u02cc\5\u00afV\2\u02cc\u02cd\5\u00afV\2\u02cd\u02ce")
        buf.write("\5\u00afV\2\u02ce\u02cf\5\u00afV\2\u02cf\u02db\3\2\2\2")
        buf.write("\u02d0\u02d1\7%\2\2\u02d1\u02d2\5\u00afV\2\u02d2\u02d3")
        buf.write("\5\u00afV\2\u02d3\u02d4\5\u00afV\2\u02d4\u02d5\5\u00af")
        buf.write("V\2\u02d5\u02d6\5\u00afV\2\u02d6\u02d7\5\u00afV\2\u02d7")
        buf.write("\u02d8\5\u00afV\2\u02d8\u02d9\5\u00afV\2\u02d9\u02db\3")
        buf.write("\2\2\2\u02da\u02bd\3\2\2\2\u02da\u02c2\3\2\2\2\u02da\u02c8")
        buf.write("\3\2\2\2\u02da\u02d0\3\2\2\2\u02db\u00be\3\2\2\2\u02dc")
        buf.write("\u02dd\t\3\2\2\u02dd\u02de\3\2\2\2\u02de\u02df\b^\b\2")
        buf.write("\u02df\u00c0\3\2\2\2\u02e0\u02e5\7$\2\2\u02e1\u02e4\5")
        buf.write("\u00c9c\2\u02e2\u02e4\n\f\2\2\u02e3\u02e1\3\2\2\2\u02e3")
        buf.write("\u02e2\3\2\2\2\u02e4\u02e7\3\2\2\2\u02e5\u02e3\3\2\2\2")
        buf.write("\u02e5\u02e6\3\2\2\2\u02e6\u02e8\3\2\2\2\u02e7\u02e5\3")
        buf.write("\2\2\2\u02e8\u02f3\7$\2\2\u02e9\u02ee\7)\2\2\u02ea\u02ed")
        buf.write("\5\u00c9c\2\u02eb\u02ed\n\r\2\2\u02ec\u02ea\3\2\2\2\u02ec")
        buf.write("\u02eb\3\2\2\2\u02ed\u02f0\3\2\2\2\u02ee\u02ec\3\2\2\2")
        buf.write("\u02ee\u02ef\3\2\2\2\u02ef\u02f1\3\2\2\2\u02f0\u02ee\3")
        buf.write("\2\2\2\u02f1\u02f3\7)\2\2\u02f2\u02e0\3\2\2\2\u02f2\u02e9")
        buf.write("\3\2\2\2\u02f3\u00c2\3\2\2\2\u02f4\u02f5\7$\2\2\u02f5")
        buf.write("\u02f6\7$\2\2\u02f6\u02f7\7$\2\2\u02f7\u02fb\3\2\2\2\u02f8")
        buf.write("\u02fa\5\u00c5a\2\u02f9\u02f8\3\2\2\2\u02fa\u02fd\3\2")
        buf.write("\2\2\u02fb\u02fc\3\2\2\2\u02fb\u02f9\3\2\2\2\u02fc\u02fe")
        buf.write("\3\2\2\2\u02fd\u02fb\3\2\2\2\u02fe\u02ff\7$\2\2\u02ff")
        buf.write("\u0300\7$\2\2\u0300\u030f\7$\2\2\u0301\u0302\7)\2\2\u0302")
        buf.write("\u0303\7)\2\2\u0303\u0304\7)\2\2\u0304\u0308\3\2\2\2\u0305")
        buf.write("\u0307\5\u00c7b\2\u0306\u0305\3\2\2\2\u0307\u030a\3\2")
        buf.write("\2\2\u0308\u0309\3\2\2\2\u0308\u0306\3\2\2\2\u0309\u030b")
        buf.write("\3\2\2\2\u030a\u0308\3\2\2\2\u030b\u030c\7)\2\2\u030c")
        buf.write("\u030d\7)\2\2\u030d\u030f\7)\2\2\u030e\u02f4\3\2\2\2\u030e")
        buf.write("\u0301\3\2\2\2\u030f\u00c4\3\2\2\2\u0310\u0314\7$\2\2")
        buf.write("\u0311\u0312\7$\2\2\u0312\u0314\7$\2\2\u0313\u0310\3\2")
        buf.write("\2\2\u0313\u0311\3\2\2\2\u0313\u0314\3\2\2\2\u0314\u0317")
        buf.write("\3\2\2\2\u0315\u0318\5\u00c9c\2\u0316\u0318\n\16\2\2\u0317")
        buf.write("\u0315\3\2\2\2\u0317\u0316\3\2\2\2\u0318\u0319\3\2\2\2")
        buf.write("\u0319\u0317\3\2\2\2\u0319\u031a\3\2\2\2\u031a\u00c6\3")
        buf.write("\2\2\2\u031b\u031f\7)\2\2\u031c\u031d\7)\2\2\u031d\u031f")
        buf.write("\7)\2\2\u031e\u031b\3\2\2\2\u031e\u031c\3\2\2\2\u031e")
        buf.write("\u031f\3\2\2\2\u031f\u0322\3\2\2\2\u0320\u0323\5\u00c9")
        buf.write("c\2\u0321\u0323\n\17\2\2\u0322\u0320\3\2\2\2\u0322\u0321")
        buf.write("\3\2\2\2\u0323\u0324\3\2\2\2\u0324\u0322\3\2\2\2\u0324")
        buf.write("\u0325\3\2\2\2\u0325\u00c8\3\2\2\2\u0326\u0327\7^\2\2")
        buf.write("\u0327\u032c\t\20\2\2\u0328\u032c\5\u00cbd\2\u0329\u032c")
        buf.write("\5\u00cde\2\u032a\u032c\5\u00cff\2\u032b\u0326\3\2\2\2")
        buf.write("\u032b\u0328\3\2\2\2\u032b\u0329\3\2\2\2\u032b\u032a\3")
        buf.write("\2\2\2\u032c\u00ca\3\2\2\2\u032d\u032e\7^\2\2\u032e\u032f")
        buf.write("\7z\2\2\u032f\u0330\5\u00afV\2\u0330\u0331\5\u00afV\2")
        buf.write("\u0331\u00cc\3\2\2\2\u0332\u0333\7^\2\2\u0333\u0334\7")
        buf.write("w\2\2\u0334\u0335\5\u00afV\2\u0335\u0336\5\u00afV\2\u0336")
        buf.write("\u0337\5\u00afV\2\u0337\u0338\5\u00afV\2\u0338\u00ce\3")
        buf.write("\2\2\2\u0339\u033a\7^\2\2\u033a\u033b\7W\2\2\u033b\u033c")
        buf.write("\5\u00afV\2\u033c\u033d\5\u00afV\2\u033d\u033e\5\u00af")
        buf.write("V\2\u033e\u033f\5\u00afV\2\u033f\u0340\5\u00afV\2\u0340")
        buf.write("\u0341\5\u00afV\2\u0341\u0342\5\u00afV\2\u0342\u0343\5")
        buf.write("\u00afV\2\u0343\u00d0\3\2\2\2\61\2\3\4\5\6\u00d4\u00d9")
        buf.write("\u00e7\u00f1\u00f6\u015d\u016d\u0172\u0238\u0246\u024d")
        buf.write("\u0254\u025b\u025d\u0261\u0266\u026b\u0271\u0275\u027b")
        buf.write("\u027e\u0283\u0287\u0299\u029b\u02b9\u02da\u02e3\u02e5")
        buf.write("\u02ec\u02ee\u02f2\u02fb\u0308\u030e\u0313\u0317\u0319")
        buf.write("\u031e\u0322\u0324\u032b\t\7\3\2\4\2\2\7\4\2\4\5\2\4\6")
        buf.write("\2\6\2\2\b\2\2")
        return buf.getvalue()


class UL4Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    TEXT_MODE = 1
    MAYBETAG_MODE = 2
    WHITESPACE_MODE = 3
    TAG_MODE = 4

    DEFAULT_INDENT = 1
    DEFAULT_LINEEND = 2
    DEFAULT_MAYBETAG = 3
    DEFAULT_TEXT = 4
    TEXT_MAYBETAG = 5
    TEXT_TEXT = 6
    MAYBETAG_WS = 7
    MAYBETAG_WHITESPACE = 8
    MAYBETAG_DOC = 9
    MAYBETAG_NOTE = 10
    MAYBETAG_UL4 = 11
    MAYBETAG_DEF = 12
    MAYBETAG_FOR = 13
    MAYBETAG_WHILE = 14
    MAYBETAG_IF = 15
    MAYBETAG_ELIF = 16
    MAYBETAG_ELSE = 17
    MAYBETAG_RENDERBLOCK = 18
    MAYBETAG_RENDERBLOCKS = 19
    MAYBETAG_END = 20
    MAYBETAG_OTHER = 21
    WHITESPACE_VALUE = 22
    WHITESPACE_WS = 23
    WHITESPACE_ENDDELIM = 24
    ENDDELIM = 25
    FOR = 26
    IN = 27
    IF = 28
    ELSE = 29
    NOT = 30
    IS = 31
    AND = 32
    OR = 33
    NONE = 34
    TRUE = 35
    FALSE = 36
    DEF = 37
    WHILE = 38
    RENDERBLOCK = 39
    RENDERBLOCKS = 40
    PARENS_OPEN = 41
    PARENS_CLOSE = 42
    BRACKET_OPEN = 43
    BRACKET_CLOSE = 44
    BRACE_OPEN = 45
    BRACE_CLOSE = 46
    STAR_STAR = 47
    STAR = 48
    PLUS = 49
    MINUS = 50
    SLASH_SLASH = 51
    SLASH = 52
    PERCENT = 53
    EQUAL = 54
    NOT_EQUAL = 55
    LESS_THAN_OR_EQUAL = 56
    LESS_THAN = 57
    GREATER_THAN_OR_EQUAL = 58
    GREATER_THAN = 59
    ASSIGN = 60
    COMMA = 61
    COLON = 62
    TILDE = 63
    AMPERSAND = 64
    CARET = 65
    DOT = 66
    SHIFTLEFT = 67
    SHIFTRIGHT = 68
    BAR = 69
    AUGADD = 70
    AUGSUB = 71
    AUGMUL = 72
    AUGFLOORDIV = 73
    AUGTRUEDIV = 74
    AUGMOD = 75
    AUGSHIFTLEFT = 76
    AUGSHIFTRIGHT = 77
    AUGAND = 78
    AUGXOR = 79
    AUGOR = 80
    NAME = 81
    INT = 82
    FLOAT = 83
    DATE = 84
    DATETIME = 85
    COLOR = 86
    WS = 87
    STRING = 88
    STRING3 = 89

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE", "TEXT_MODE", "MAYBETAG_MODE", "WHITESPACE_MODE", 
                  "TAG_MODE" ]

    literalNames = [ "<INVALID>",
            "'whitespace'", "'doc'", "'note'", "'ul4'", "'elif'", "'end'", 
            "'in'", "'not'", "'is'", "'and'", "'or'", "'None'", "'True'", 
            "'False'", "'('", "')'", "'['", "']'", "'{'", "'}'", "'**'", 
            "'*'", "'+'", "'-'", "'//'", "'/'", "'%'", "'=='", "'!='", "'<='", 
            "'<'", "'>='", "'>'", "'='", "','", "':'", "'~'", "'&'", "'^'", 
            "'.'", "'<<'", "'>>'", "'|'", "'+='", "'-='", "'*='", "'//='", 
            "'/='", "'%='", "'<<='", "'>>='", "'&='", "'^='", "'|='" ]

    symbolicNames = [ "<INVALID>",
            "DEFAULT_INDENT", "DEFAULT_LINEEND", "DEFAULT_MAYBETAG", "DEFAULT_TEXT", 
            "TEXT_MAYBETAG", "TEXT_TEXT", "MAYBETAG_WS", "MAYBETAG_WHITESPACE", 
            "MAYBETAG_DOC", "MAYBETAG_NOTE", "MAYBETAG_UL4", "MAYBETAG_DEF", 
            "MAYBETAG_FOR", "MAYBETAG_WHILE", "MAYBETAG_IF", "MAYBETAG_ELIF", 
            "MAYBETAG_ELSE", "MAYBETAG_RENDERBLOCK", "MAYBETAG_RENDERBLOCKS", 
            "MAYBETAG_END", "MAYBETAG_OTHER", "WHITESPACE_VALUE", "WHITESPACE_WS", 
            "WHITESPACE_ENDDELIM", "ENDDELIM", "FOR", "IN", "IF", "ELSE", 
            "NOT", "IS", "AND", "OR", "NONE", "TRUE", "FALSE", "DEF", "WHILE", 
            "RENDERBLOCK", "RENDERBLOCKS", "PARENS_OPEN", "PARENS_CLOSE", 
            "BRACKET_OPEN", "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", 
            "STAR_STAR", "STAR", "PLUS", "MINUS", "SLASH_SLASH", "SLASH", 
            "PERCENT", "EQUAL", "NOT_EQUAL", "LESS_THAN_OR_EQUAL", "LESS_THAN", 
            "GREATER_THAN_OR_EQUAL", "GREATER_THAN", "ASSIGN", "COMMA", 
            "COLON", "TILDE", "AMPERSAND", "CARET", "DOT", "SHIFTLEFT", 
            "SHIFTRIGHT", "BAR", "AUGADD", "AUGSUB", "AUGMUL", "AUGFLOORDIV", 
            "AUGTRUEDIV", "AUGMOD", "AUGSHIFTLEFT", "AUGSHIFTRIGHT", "AUGAND", 
            "AUGXOR", "AUGOR", "NAME", "INT", "FLOAT", "DATE", "DATETIME", 
            "COLOR", "WS", "STRING", "STRING3" ]

    ruleNames = [ "DEFAULT_INDENT", "DEFAULT_LINEEND", "DEFAULT_MAYBETAG", 
                  "DEFAULT_TEXT", "TEXT_MAYBETAG", "TEXT_TEXT", "MAYBETAG_WS", 
                  "MAYBETAG_WHITESPACE", "MAYBETAG_DOC", "MAYBETAG_NOTE", 
                  "MAYBETAG_UL4", "MAYBETAG_DEF", "MAYBETAG_FOR", "MAYBETAG_WHILE", 
                  "MAYBETAG_IF", "MAYBETAG_ELIF", "MAYBETAG_ELSE", "MAYBETAG_RENDERBLOCK", 
                  "MAYBETAG_RENDERBLOCKS", "MAYBETAG_END", "MAYBETAG_OTHER", 
                  "WHITESPACE_VALUE", "WHITESPACE_WS", "WHITESPACE_ENDDELIM", 
                  "ENDDELIM", "FOR", "IN", "IF", "ELSE", "NOT", "IS", "AND", 
                  "OR", "NONE", "TRUE", "FALSE", "DEF", "WHILE", "RENDERBLOCK", 
                  "RENDERBLOCKS", "PARENS_OPEN", "PARENS_CLOSE", "BRACKET_OPEN", 
                  "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", "STAR_STAR", 
                  "STAR", "PLUS", "MINUS", "SLASH_SLASH", "SLASH", "PERCENT", 
                  "EQUAL", "NOT_EQUAL", "LESS_THAN_OR_EQUAL", "LESS_THAN", 
                  "GREATER_THAN_OR_EQUAL", "GREATER_THAN", "ASSIGN", "COMMA", 
                  "COLON", "TILDE", "AMPERSAND", "CARET", "DOT", "SHIFTLEFT", 
                  "SHIFTRIGHT", "BAR", "AUGADD", "AUGSUB", "AUGMUL", "AUGFLOORDIV", 
                  "AUGTRUEDIV", "AUGMOD", "AUGSHIFTLEFT", "AUGSHIFTRIGHT", 
                  "AUGAND", "AUGXOR", "AUGOR", "NAME", "DIGIT", "BIN_DIGIT", 
                  "OCT_DIGIT", "HEX_DIGIT", "INT", "EXPONENT", "FLOAT", 
                  "TIME", "DATE", "DATETIME", "COLOR", "WS", "STRING", "STRING3", 
                  "TRIQUOTE", "TRIAPOS", "ESC_SEQ", "UNICODE1_ESC", "UNICODE2_ESC", 
                  "UNICODE4_ESC" ]

    grammarFileName = "UL4Lexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


