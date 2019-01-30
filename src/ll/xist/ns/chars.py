# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST namespace that contains all the character entities defined in HTML.
"""


from ll.xist import xsc


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/chars"


# Latin 1 characters
class nbsp(xsc.CharRef): "no-break space = non-breaking space, U+00A0 ISOnum"; codepoint = 160
class iexcl(xsc.CharRef): "inverted exclamation mark, U+00A1 ISOnum"; codepoint = 161
class cent(xsc.CharRef): "cent sign, U+00A2 ISOnum"; codepoint = 162
class pound(xsc.CharRef): "pound sign, U+00A3 ISOnum"; codepoint = 163
class curren(xsc.CharRef): "currency sign, U+00A4 ISOnum"; codepoint = 164
class yen(xsc.CharRef): "yen sign = yuan sign, U+00A5 ISOnum"; codepoint = 165
class brvbar(xsc.CharRef): "broken bar = broken vertical bar, U+00A6 ISOnum"; codepoint = 166
class sect(xsc.CharRef): "section sign, U+00A7 ISOnum"; codepoint = 167
class uml(xsc.CharRef): "diaeresis = spacing diaeresis, U+00A8 ISOdia"; codepoint = 168
class copy(xsc.CharRef): "copyright sign, U+00A9 ISOnum"; codepoint = 169
class ordf(xsc.CharRef): "feminine ordinal indicator, U+00AA ISOnum"; codepoint = 170
class laquo(xsc.CharRef): "left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum"; codepoint = 171
class not_(xsc.CharRef): "not sign, U+00AC ISOnum"; codepoint = 172
class shy(xsc.CharRef): "soft hyphen = discretionary hyphen, U+00AD ISOnum"; codepoint = 173
class reg(xsc.CharRef): "registered sign = registered trade mark sign, U+00AE ISOnum"; codepoint = 174
class macr(xsc.CharRef): "macron = spacing macron = overline = APL overbar, U+00AF ISOdia"; codepoint = 175
class deg(xsc.CharRef): "degree sign, U+00B0 ISOnum"; codepoint = 176
class plusmn(xsc.CharRef): "plus-minus sign = plus-or-minus sign, U+00B1 ISOnum"; codepoint = 177
class sup2(xsc.CharRef): "superscript two = superscript digit two = squared, U+00B2 ISOnum"; codepoint = 178
class sup3(xsc.CharRef): "superscript three = superscript digit three = cubed, U+00B3 ISOnum"; codepoint = 179
class acute(xsc.CharRef): "acute accent = spacing acute, U+00B4 ISOdia"; codepoint = 180
class micro(xsc.CharRef): "micro sign, U+00B5 ISOnum"; codepoint = 181
class para(xsc.CharRef): "pilcrow sign = paragraph sign, U+00B6 ISOnum"; codepoint = 182
class middot(xsc.CharRef): "middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum"; codepoint = 183
class cedil(xsc.CharRef): "cedilla = spacing cedilla, U+00B8 ISOdia"; codepoint = 184
class sup1(xsc.CharRef): "superscript one = superscript digit one, U+00B9 ISOnum"; codepoint = 185
class ordm(xsc.CharRef): "masculine ordinal indicator, U+00BA ISOnum"; codepoint = 186
class raquo(xsc.CharRef): "right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum"; codepoint = 187
class frac14(xsc.CharRef): "vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum"; codepoint = 188
class frac12(xsc.CharRef): "vulgar fraction one half = fraction one half, U+00BD ISOnum"; codepoint = 189
class frac34(xsc.CharRef): "vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum"; codepoint = 190
class iquest(xsc.CharRef): "inverted question mark = turned question mark, U+00BF ISOnum"; codepoint = 191
class Agrave(xsc.CharRef): "latin capital letter A with grave = latin capital letter A grave, U+00C0 ISOlat1"; codepoint = 192
class Aacute(xsc.CharRef): "latin capital letter A with acute, U+00C1 ISOlat1"; codepoint = 193
class Acirc(xsc.CharRef): "latin capital letter A with circumflex, U+00C2 ISOlat1"; codepoint = 194
class Atilde(xsc.CharRef): "latin capital letter A with tilde, U+00C3 ISOlat1"; codepoint = 195
class Auml(xsc.CharRef): "latin capital letter A with diaeresis, U+00C4 ISOlat1"; codepoint = 196
class Aring(xsc.CharRef): "latin capital letter A with ring above = latin capital letter A ring, U+00C5 ISOlat1"; codepoint = 197
class AElig(xsc.CharRef): "latin capital letter AE = latin capital ligature AE, U+00C6 ISOlat1"; codepoint = 198
class Ccedil(xsc.CharRef): "latin capital letter C with cedilla, U+00C7 ISOlat1"; codepoint = 199
class Egrave(xsc.CharRef): "latin capital letter E with grave, U+00C8 ISOlat1"; codepoint = 200
class Eacute(xsc.CharRef): "latin capital letter E with acute, U+00C9 ISOlat1"; codepoint = 201
class Ecirc(xsc.CharRef): "latin capital letter E with circumflex, U+00CA ISOlat1"; codepoint = 202
class Euml(xsc.CharRef): "latin capital letter E with diaeresis, U+00CB ISOlat1"; codepoint = 203
class Igrave(xsc.CharRef): "latin capital letter I with grave, U+00CC ISOlat1"; codepoint = 204
class Iacute(xsc.CharRef): "latin capital letter I with acute, U+00CD ISOlat1"; codepoint = 205
class Icirc(xsc.CharRef): "latin capital letter I with circumflex, U+00CE ISOlat1"; codepoint = 206
class Iuml(xsc.CharRef): "latin capital letter I with diaeresis, U+00CF ISOlat1"; codepoint = 207
class ETH(xsc.CharRef): "latin capital letter ETH, U+00D0 ISOlat1"; codepoint = 208
class Ntilde(xsc.CharRef): "latin capital letter N with tilde, U+00D1 ISOlat1"; codepoint = 209
class Ograve(xsc.CharRef): "latin capital letter O with grave, U+00D2 ISOlat1"; codepoint = 210
class Oacute(xsc.CharRef): "latin capital letter O with acute, U+00D3 ISOlat1"; codepoint = 211
class Ocirc(xsc.CharRef): "latin capital letter O with circumflex, U+00D4 ISOlat1"; codepoint = 212
class Otilde(xsc.CharRef): "latin capital letter O with tilde, U+00D5 ISOlat1"; codepoint = 213
class Ouml(xsc.CharRef): "latin capital letter O with diaeresis, U+00D6 ISOlat1"; codepoint = 214
class times(xsc.CharRef): "multiplication sign, U+00D7 ISOnum"; codepoint = 215
class Oslash(xsc.CharRef): "latin capital letter O with stroke = latin capital letter O slash, U+00D8 ISOlat1"; codepoint = 216
class Ugrave(xsc.CharRef): "latin capital letter U with grave, U+00D9 ISOlat1"; codepoint = 217
class Uacute(xsc.CharRef): "latin capital letter U with acute, U+00DA ISOlat1"; codepoint = 218
class Ucirc(xsc.CharRef): "latin capital letter U with circumflex, U+00DB ISOlat1"; codepoint = 219
class Uuml(xsc.CharRef): "latin capital letter U with diaeresis, U+00DC ISOlat1"; codepoint = 220
class Yacute(xsc.CharRef): "latin capital letter Y with acute, U+00DD ISOlat1"; codepoint = 221
class THORN(xsc.CharRef): "latin capital letter THORN, U+00DE ISOlat1"; codepoint = 222
class szlig(xsc.CharRef): "latin small letter sharp s = ess-zed, U+00DF ISOlat1"; codepoint = 223
class agrave(xsc.CharRef): "latin small letter a with grave = latin small letter a grave, U+00E0 ISOlat1"; codepoint = 224
class aacute(xsc.CharRef): "latin small letter a with acute, U+00E1 ISOlat1"; codepoint = 225
class acirc(xsc.CharRef): "latin small letter a with circumflex, U+00E2 ISOlat1"; codepoint = 226
class atilde(xsc.CharRef): "latin small letter a with tilde, U+00E3 ISOlat1"; codepoint = 227
class auml(xsc.CharRef): "latin small letter a with diaeresis, U+00E4 ISOlat1"; codepoint = 228
class aring(xsc.CharRef): "latin small letter a with ring above = latin small letter a ring, U+00E5 ISOlat1"; codepoint = 229
class aelig(xsc.CharRef): "latin small letter ae = latin small ligature ae, U+00E6 ISOlat1"; codepoint = 230
class ccedil(xsc.CharRef): "latin small letter c with cedilla, U+00E7 ISOlat1"; codepoint = 231
class egrave(xsc.CharRef): "latin small letter e with grave, U+00E8 ISOlat1"; codepoint = 232
class eacute(xsc.CharRef): "latin small letter e with acute, U+00E9 ISOlat1"; codepoint = 233
class ecirc(xsc.CharRef): "latin small letter e with circumflex, U+00EA ISOlat1"; codepoint = 234
class euml(xsc.CharRef): "latin small letter e with diaeresis, U+00EB ISOlat1"; codepoint = 235
class igrave(xsc.CharRef): "latin small letter i with grave, U+00EC ISOlat1"; codepoint = 236
class iacute(xsc.CharRef): "latin small letter i with acute, U+00ED ISOlat1"; codepoint = 237
class icirc(xsc.CharRef): "latin small letter i with circumflex, U+00EE ISOlat1"; codepoint = 238
class iuml(xsc.CharRef): "latin small letter i with diaeresis, U+00EF ISOlat1"; codepoint = 239
class eth(xsc.CharRef): "latin small letter eth, U+00F0 ISOlat1"; codepoint = 240
class ntilde(xsc.CharRef): "latin small letter n with tilde, U+00F1 ISOlat1"; codepoint = 241
class ograve(xsc.CharRef): "latin small letter o with grave, U+00F2 ISOlat1"; codepoint = 242
class oacute(xsc.CharRef): "latin small letter o with acute, U+00F3 ISOlat1"; codepoint = 243
class ocirc(xsc.CharRef): "latin small letter o with circumflex, U+00F4 ISOlat1"; codepoint = 244
class otilde(xsc.CharRef): "latin small letter o with tilde, U+00F5 ISOlat1"; codepoint = 245
class ouml(xsc.CharRef): "latin small letter o with diaeresis, U+00F6 ISOlat1"; codepoint = 246
class divide(xsc.CharRef): "division sign, U+00F7 ISOnum"; codepoint = 247
class oslash(xsc.CharRef): "latin small letter o with stroke, = latin small letter o slash, U+00F8 ISOlat1"; codepoint = 248
class ugrave(xsc.CharRef): "latin small letter u with grave, U+00F9 ISOlat1"; codepoint = 249
class uacute(xsc.CharRef): "latin small letter u with acute, U+00FA ISOlat1"; codepoint = 250
class ucirc(xsc.CharRef): "latin small letter u with circumflex, U+00FB ISOlat1"; codepoint = 251
class uuml(xsc.CharRef): "latin small letter u with diaeresis, U+00FC ISOlat1"; codepoint = 252
class yacute(xsc.CharRef): "latin small letter y with acute, U+00FD ISOlat1"; codepoint = 253
class thorn(xsc.CharRef): "latin small letter thorn, U+00FE ISOlat1"; codepoint = 254
class yuml(xsc.CharRef): "latin small letter y with diaeresis, U+00FF ISOlat1"; codepoint = 255

# Latin Extended-A
class OElig(xsc.CharRef): "latin capital ligature OE, U+0152 ISOlat2"; codepoint = 338
class oelig(xsc.CharRef): "latin small ligature oe, U+0153 ISOlat2"; codepoint = 339
class Scaron(xsc.CharRef): "latin capital letter S with caron, U+0160 ISOlat2"; codepoint = 352
class scaron(xsc.CharRef): "latin small letter s with caron, U+0161 ISOlat2"; codepoint = 353
class Yuml(xsc.CharRef): "latin capital letter Y with diaeresis, U+0178 ISOlat2"; codepoint = 376

# Spacing Modifier Letters
class circ(xsc.CharRef): "modifier letter circumflex accent, U+02C6 ISOpub"; codepoint = 710
class tilde(xsc.CharRef): "small tilde, U+02DC ISOdia"; codepoint = 732

# General Punctuation
class ensp(xsc.CharRef): "en space, U+2002 ISOpub"; codepoint = 8194
class emsp(xsc.CharRef): "em space, U+2003 ISOpub"; codepoint = 8195
class thinsp(xsc.CharRef): "thin space, U+2009 ISOpub"; codepoint = 8201
class zwnj(xsc.CharRef): "zero width non-joiner, U+200C NEW RFC 2070"; codepoint = 8204
class zwj(xsc.CharRef): "zero width joiner, U+200D NEW RFC 2070"; codepoint = 8205
class lrm(xsc.CharRef): "left-to-right mark, U+200E NEW RFC 2070"; codepoint = 8206
class rlm(xsc.CharRef): "right-to-left mark, U+200F NEW RFC 2070"; codepoint = 8207
class ndash(xsc.CharRef): "en dash, U+2013 ISOpub"; codepoint = 8211
class mdash(xsc.CharRef): "em dash, U+2014 ISOpub"; codepoint = 8212
class lsquo(xsc.CharRef): "left single quotation mark, U+2018 ISOnum"; codepoint = 8216
class rsquo(xsc.CharRef): "right single quotation mark, U+2019 ISOnum"; codepoint = 8217
class sbquo(xsc.CharRef): "single low-9 quotation mark, U+201A NEW"; codepoint = 8218
class ldquo(xsc.CharRef): "left double quotation mark, U+201C ISOnum"; codepoint = 8220
class rdquo(xsc.CharRef): "right double quotation mark, U+201D ISOnum"; codepoint = 8221
class bdquo(xsc.CharRef): "double low-9 quotation mark, U+201E NEW"; codepoint = 8222
class dagger(xsc.CharRef): "dagger, U+2020 ISOpub"; codepoint = 8224
class Dagger(xsc.CharRef): "double dagger, U+2021 ISOpub"; codepoint = 8225
class permil(xsc.CharRef): "per mille sign, U+2030 ISOtech"; codepoint = 8240
class lsaquo(xsc.CharRef): "single left-pointing angle quotation mark, U+2039 ISO proposed"; codepoint = 8249
class rsaquo(xsc.CharRef): "single right-pointing angle quotation mark, U+203A ISO proposed"; codepoint = 8250
class euro(xsc.CharRef): "euro sign, U+20AC NEW"; codepoint = 8364

# Mathematical, Greek and Symbolic characters
# Latin Extended-B
class fnof(xsc.CharRef): "latin small f with hook = function = florin, U+0192 ISOtech"; codepoint = 402

# Greek
class Alpha(xsc.CharRef): "greek capital letter alpha, U+0391"; codepoint = 913
class Beta(xsc.CharRef): "greek capital letter beta, U+0392"; codepoint = 914
class Gamma(xsc.CharRef): "greek capital letter gamma, U+0393 ISOgrk3"; codepoint = 915
class Delta(xsc.CharRef): "greek capital letter delta, U+0394 ISOgrk3"; codepoint = 916
class Epsilon(xsc.CharRef): "greek capital letter epsilon, U+0395"; codepoint = 917
class Zeta(xsc.CharRef): "greek capital letter zeta, U+0396"; codepoint = 918
class Eta(xsc.CharRef): "greek capital letter eta, U+0397"; codepoint = 919
class Theta(xsc.CharRef): "greek capital letter theta, U+0398 ISOgrk3"; codepoint = 920
class Iota(xsc.CharRef): "greek capital letter iota, U+0399"; codepoint = 921
class Kappa(xsc.CharRef): "greek capital letter kappa, U+039A"; codepoint = 922
class Lambda(xsc.CharRef): "greek capital letter lambda, U+039B ISOgrk3"; codepoint = 923
class Mu(xsc.CharRef): "greek capital letter mu, U+039C"; codepoint = 924
class Nu(xsc.CharRef): "greek capital letter nu, U+039D"; codepoint = 925
class Xi(xsc.CharRef): "greek capital letter xi, U+039E ISOgrk3"; codepoint = 926
class Omicron(xsc.CharRef): "greek capital letter omicron, U+039F"; codepoint = 927
class Pi(xsc.CharRef): "greek capital letter pi, U+03A0 ISOgrk3"; codepoint = 928
class Rho(xsc.CharRef): "greek capital letter rho, U+03A1"; codepoint = 929
class Sigma(xsc.CharRef): "greek capital letter sigma, U+03A3 ISOgrk3"; codepoint = 931
class Tau(xsc.CharRef): "greek capital letter tau, U+03A4"; codepoint = 932
class Upsilon(xsc.CharRef): "greek capital letter upsilon, U+03A5 ISOgrk3"; codepoint = 933
class Phi(xsc.CharRef): "greek capital letter phi, U+03A6 ISOgrk3"; codepoint = 934
class Chi(xsc.CharRef): "greek capital letter chi, U+03A7"; codepoint = 935
class Psi(xsc.CharRef): "greek capital letter psi, U+03A8 ISOgrk3"; codepoint = 936
class Omega(xsc.CharRef): "greek capital letter omega, U+03A9 ISOgrk3"; codepoint = 937
class alpha(xsc.CharRef): "greek small letter alpha, U+03B1 ISOgrk3"; codepoint = 945
class beta(xsc.CharRef): "greek small letter beta, U+03B2 ISOgrk3"; codepoint = 946
class gamma(xsc.CharRef): "greek small letter gamma, U+03B3 ISOgrk3"; codepoint = 947
class delta(xsc.CharRef): "greek small letter delta, U+03B4 ISOgrk3"; codepoint = 948
class epsilon(xsc.CharRef): "greek small letter epsilon, U+03B5 ISOgrk3"; codepoint = 949
class zeta(xsc.CharRef): "greek small letter zeta, U+03B6 ISOgrk3"; codepoint = 950
class eta(xsc.CharRef): "greek small letter eta, U+03B7 ISOgrk3"; codepoint = 951
class theta(xsc.CharRef): "greek small letter theta, U+03B8 ISOgrk3"; codepoint = 952
class iota(xsc.CharRef): "greek small letter iota, U+03B9 ISOgrk3"; codepoint = 953
class kappa(xsc.CharRef): "greek small letter kappa, U+03BA ISOgrk3"; codepoint = 954
class lambda_(xsc.CharRef): "greek small letter lambda, U+03BB ISOgrk3"; codepoint = 955
class mu(xsc.CharRef): "greek small letter mu, U+03BC ISOgrk3"; codepoint = 956
class nu(xsc.CharRef): "greek small letter nu, U+03BD ISOgrk3"; codepoint = 957
class xi(xsc.CharRef): "greek small letter xi, U+03BE ISOgrk3"; codepoint = 958
class omicron(xsc.CharRef): "greek small letter omicron, U+03BF NEW"; codepoint = 959
class pi(xsc.CharRef): "greek small letter pi, U+03C0 ISOgrk3"; codepoint = 960
class rho(xsc.CharRef): "greek small letter rho, U+03C1 ISOgrk3"; codepoint = 961
class sigmaf(xsc.CharRef): "greek small letter final sigma, U+03C2 ISOgrk3"; codepoint = 962
class sigma(xsc.CharRef): "greek small letter sigma, U+03C3 ISOgrk3"; codepoint = 963
class tau(xsc.CharRef): "greek small letter tau, U+03C4 ISOgrk3"; codepoint = 964
class upsilon(xsc.CharRef): "greek small letter upsilon, U+03C5 ISOgrk3"; codepoint = 965
class phi(xsc.CharRef): "greek small letter phi, U+03C6 ISOgrk3"; codepoint = 966
class chi(xsc.CharRef): "greek small letter chi, U+03C7 ISOgrk3"; codepoint = 967
class psi(xsc.CharRef): "greek small letter psi, U+03C8 ISOgrk3"; codepoint = 968
class omega(xsc.CharRef): "greek small letter omega, U+03C9 ISOgrk3"; codepoint = 969
class thetasym(xsc.CharRef): "greek small letter theta symbol, U+03D1 NEW"; codepoint = 977
class upsih(xsc.CharRef): "greek upsilon with hook symbol, U+03D2 NEW"; codepoint = 978
class piv(xsc.CharRef): "greek pi symbol, U+03D6 ISOgrk3"; codepoint = 982

# General Punctuation
class bull(xsc.CharRef): "bullet = black small circle, U+2022 ISOpub"; codepoint = 8226
class hellip(xsc.CharRef): "horizontal ellipsis = three dot leader, U+2026 ISOpub"; codepoint = 8230
class prime(xsc.CharRef): "prime = minutes = feet, U+2032 ISOtech"; codepoint = 8242
class Prime(xsc.CharRef): "double prime = seconds = inches, U+2033 ISOtech"; codepoint = 8243
class oline(xsc.CharRef): "overline = spacing overscore, U+203E NEW"; codepoint = 8254
class frasl(xsc.CharRef): "fraction slash, U+2044 NEW"; codepoint = 8260

# Letterlike Symbols
class weierp(xsc.CharRef): "script capital P = power set = Weierstrass p, U+2118 ISOamso"; codepoint = 8472
class image(xsc.CharRef): "blackletter capital I = imaginary part, U+2111 ISOamso"; codepoint = 8465
class real(xsc.CharRef): "blackletter capital R = real part symbol, U+211C ISOamso"; codepoint = 8476
class trade(xsc.CharRef): "trade mark sign, U+2122 ISOnum"; codepoint = 8482
class alefsym(xsc.CharRef): "alef symbol = first transfinite cardinal, U+2135 NEW"; codepoint = 8501

# Arrows
class larr(xsc.CharRef): "leftwards arrow, U+2190 ISOnum"; codepoint = 8592
class uarr(xsc.CharRef): "upwards arrow, U+2191 ISOnu"; codepoint = 8593
class rarr(xsc.CharRef): "rightwards arrow, U+2192 ISOnum"; codepoint = 8594
class darr(xsc.CharRef): "downwards arrow, U+2193 ISOnum"; codepoint = 8595
class harr(xsc.CharRef): "left right arrow, U+2194 ISOamsa"; codepoint = 8596
class crarr(xsc.CharRef): "downwards arrow with corner leftwards = carriage return, U+21B5 NEW"; codepoint = 8629
class lArr(xsc.CharRef): "leftwards double arrow, U+21D0 ISOtech"; codepoint = 8656
class uArr(xsc.CharRef): "upwards double arrow, U+21D1 ISOamsa"; codepoint = 8657
class rArr(xsc.CharRef): "rightwards double arrow, U+21D2 ISOtech"; codepoint = 8658
class dArr(xsc.CharRef): "downwards double arrow, U+21D3 ISOamsa"; codepoint = 8659
class hArr(xsc.CharRef): "left right double arrow, U+21D4 ISOamsa"; codepoint = 8660

# Mathematical Operators
class forall(xsc.CharRef): "for all, U+2200 ISOtech"; codepoint = 8704
class part(xsc.CharRef): "partial differential, U+2202 ISOtech"; codepoint = 8706
class exist(xsc.CharRef): "there exists, U+2203 ISOtech"; codepoint = 8707
class empty(xsc.CharRef): "empty set = null set = diameter, U+2205 ISOamso"; codepoint = 8709
class nabla(xsc.CharRef): "nabla = backward difference, U+2207 ISOtech"; codepoint = 8711
class isin(xsc.CharRef): "element of, U+2208 ISOtech"; codepoint = 8712
class notin(xsc.CharRef): "not an element of, U+2209 ISOtech"; codepoint = 8713
class ni(xsc.CharRef): "contains as member, U+220B ISOtech"; codepoint = 8715
class prod(xsc.CharRef): "n-ary product = product sign, U+220F ISOamsb"; codepoint = 8719
class sum(xsc.CharRef): "n-ary sumation, U+2211 ISOamsb"; codepoint = 8721
class minus(xsc.CharRef): "minus sign, U+2212 ISOtech"; codepoint = 8722
class lowast(xsc.CharRef): "asterisk operator, U+2217 ISOtech"; codepoint = 8727
class radic(xsc.CharRef): "square root = radical sign, U+221A ISOtech"; codepoint = 8730
class prop(xsc.CharRef): "proportional to, U+221D ISOtech"; codepoint = 8733
class infin(xsc.CharRef): "infinity, U+221E ISOtech"; codepoint = 8734
class ang(xsc.CharRef): "angle, U+2220 ISOamso"; codepoint = 8736
class and_(xsc.CharRef): "logical and = wedge, U+2227 ISOtech"; codepoint = 8743
class or_(xsc.CharRef): "logical or = vee, U+2228 ISOtech"; codepoint = 8744
class cap(xsc.CharRef): "intersection = cap, U+2229 ISOtech"; codepoint = 8745
class cup(xsc.CharRef): "union = cup, U+222A ISOtech"; codepoint = 8746
class int(xsc.CharRef): "integral, U+222B ISOtech"; codepoint = 8747
class there4(xsc.CharRef): "therefore, U+2234 ISOtech"; codepoint = 8756
class sim(xsc.CharRef): "tilde operator = varies with = similar to, U+223C ISOtech"; codepoint = 8764
class cong(xsc.CharRef): "approximately equal to, U+2245 ISOtech"; codepoint = 8773
class asymp(xsc.CharRef): "almost equal to = asymptotic to, U+2248 ISOamsr"; codepoint = 8776
class ne(xsc.CharRef): "not equal to, U+2260 ISOtech"; codepoint = 8800
class equiv(xsc.CharRef): "identical to, U+2261 ISOtech"; codepoint = 8801
class le(xsc.CharRef): "less-than or equal to, U+2264 ISOtech"; codepoint = 8804
class ge(xsc.CharRef): "greater-than or equal to, U+2265 ISOtech"; codepoint = 8805
class Sub(xsc.CharRef): "subset of, U+2282 ISOtech"; codepoint = 8834; xmlname = "sub"
class Sup(xsc.CharRef): "superset of, U+2283 ISOtech"; codepoint = 8835; xmlname = "sup"
class nsub(xsc.CharRef): "not a subset of, U+2284 ISOamsn"; codepoint = 8836
class sube(xsc.CharRef): "subset of or equal to, U+2286 ISOtech"; codepoint = 8838
class supe(xsc.CharRef): "superset of or equal to, U+2287 ISOtech"; codepoint = 8839
class oplus(xsc.CharRef): "circled plus = direct sum, U+2295 ISOamsb"; codepoint = 8853
class otimes(xsc.CharRef): "circled times = vector product, U+2297 ISOamsb"; codepoint = 8855
class perp(xsc.CharRef): "up tack = orthogonal to = perpendicular, U+22A5 ISOtech"; codepoint = 8869
class sdot(xsc.CharRef): "dot operator, U+22C5 ISOamsb"; codepoint = 8901

# Miscellaneous Technical
class lceil(xsc.CharRef): "left ceiling = apl upstile, U+2308 ISOamsc"; codepoint = 8968
class rceil(xsc.CharRef): "right ceiling, U+2309 ISOamsc"; codepoint = 8969
class lfloor(xsc.CharRef): "left floor = apl downstile, U+230A ISOamsc"; codepoint = 8970
class rfloor(xsc.CharRef): "right floor, U+230B ISOamsc"; codepoint = 8971
class lang(xsc.CharRef): "left-pointing angle bracket = bra, U+2329 ISOtech"; codepoint = 9001
class rang(xsc.CharRef): "right-pointing angle bracket = ket, U+232A ISOtech"; codepoint = 9002

# Geometric Shapes
class loz(xsc.CharRef): "lozenge, U+25CA ISOpub"; codepoint = 9674

# Miscellaneous Symbols
class spades(xsc.CharRef): "black spade suit, U+2660 ISOpub"; codepoint = 9824
class clubs(xsc.CharRef): "black club suit = shamrock, U+2663 ISOpub"; codepoint = 9827
class hearts(xsc.CharRef): "black heart suit = valentine, U+2665 ISOpub"; codepoint = 9829
class diams(xsc.CharRef): "black diamond suit, U+2666 ISOpub"; codepoint = 9830
