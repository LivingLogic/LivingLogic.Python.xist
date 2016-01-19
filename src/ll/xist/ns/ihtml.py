# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains the elements and entities for i-mode compatible HTML.
"""


import cgi # for parse_header

from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.nttdocomo.co.jp/imode"


class a(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr):
			"Designates a marker name within an HTML file (1.0)"
		class accesskey(xsc.TextAttr):
			"Directkey function (1.0)"
		class href(xsc.URLAttr):
			"Designates a link to a Web site (http), e-mail address (mailto) or phone number (tel) (1.0)"
		class cti(xsc.TextAttr):
			"Dial function + tone input function (2.0)"
		class ijam(xsc.TextAttr):
			"Designates the ID of the downloaded i appli that the OBJECT tag specifies. (3.0)"
		class utn(xsc.BoolAttr):
			"Verifies individual identification information (3.0)"
		class subject(xsc.TextAttr):
			"Designates the subject with mailto: (3.0)"
		class body(xsc.TextAttr):
			"Designates the body with mailto: (3.0)"
		class telbook(xsc.TextAttr):
			"Records in telphone book (3.0)"
		class kana(xsc.TextAttr):
			"Records in telphone book (3.0)"
		class email(xsc.TextAttr):
			"Records in telphone book (3.0)"
			xmlname = "e-mail"


class base(xsc.Element):
	"""
	Designates the base URL for the relative paths used in an HTML file. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass


class blink(xsc.Element):
	"""
	Blinks the designated text. (2.0)
	"""
	xmlns = xmlns


class blockquote(xsc.Element):
	"""
	Creates a text block and displays a quote mark. (1.0)
	"""
	xmlns = xmlns


class body(xsc.Element):
	"""
	Designates content to be displayed as a page.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class bgcolor(xsc.TextAttr):
			"Designates background color (2.0)"
		class text(xsc.TextAttr):
			"Designates text color (2.0)"
		class link(xsc.TextAttr):
			"Designates link color (2.0)"


class br(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class clear(xsc.TextAttr):
			"""
			Designates the way a character string wraps around an inline image by
			deciding where line feeding takes place. Depending on the attribute,
			it also cancels the wraparound function. (1.0)
			"""


class center(xsc.Element):
	"""
	Centers character strings, images and tables. (1.0)
	"""
	xmlns = xmlns


class dd(xsc.Element):
	"""
	Creates a definition list. (See :class:`dl`) (1.0)
	"""
	xmlns = xmlns


class dir(xsc.Element):
	"""
	Creates a list of menus or directories. Each list item must be a
	:class:`li`. (1.0)
	"""
	xmlns = xmlns


class div(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Aligns the content left or right or centers it (1.0)"


class dl(xsc.Element):
	"""
	Creates a definition list. The content consists of :class:`dd` and
	:class:`dt` elements. (1.0)
	"""
	xmlns = xmlns


class dt(xsc.Element):
	"""
	Designates the list heading and aligns the character string at left. (1.0)
	"""
	xmlns = xmlns


class font(xsc.Element):
	"""
	Designates the color of a certain portion of text. (2.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class color(xsc.TextAttr): pass


class form(xsc.Element):
	"""
	Encloses an area to be shown as a data input form. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class action(xsc.URLAttr):
			"URL or e-mail address (mailto) the input form will be sent to. (1.0)"
		class method(xsc.TextAttr):
			"Designates the method by which data is sent to the server, to either post or get. (1.0)"
		class utn(xsc.BoolAttr):
			"Verifies individual identification information. (3.0)"


class head(xsc.Element):
	"""
	Designates the information that is used as the page title and/or by the
	server. The :class:`head` tag follows the :class:`html` tag. (1.0)
	"""
	xmlns = xmlns


class h1(xsc.Element):
	"""
	Designates level 1 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class h2(xsc.Element):
	"""
	Designates level 2 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class h3(xsc.Element):
	"""
	Designates level 3 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class h4(xsc.Element):
	"""
	Designates level 4 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class h5(xsc.Element):
	"""
	Designates level 5 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class h6(xsc.Element):
	"""
	Designates level 6 header. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the header. (1.0)"


class hr(xsc.Element):
	"""
	Designates the settings of the horizontal dividing line. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Designates the alignment of the horizontal line. (1.0)"
		class size(xsc.TextAttr):
			"Sets the thickness of the horizontal line.(1.0)"
		class width(xsc.TextAttr):
			"Determines the length of the horizontal line. (1.0)"
		class noshade(xsc.BoolAttr):
			"Gives the horizontal line a two-dimensional appearance. (1.0)"


class html(xsc.Element):
	"""
	The root element
	"""
	xmlns = xmlns


class img(xsc.Element):
	"""
	Designates an image file (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr):
			"the image URL (1.0)"
		class align(xsc.TextAttr):
			"""
			Defines the way the image and character string are laid out, and how
			the character string wraps around the image. ``top``, ``middle`` or
			``bottom``. (1.0)
			"""
		class width(xsc.TextAttr):
			"Sets the image width (1.0)"
		class height(xsc.TextAttr):
			"Sets the image height (1.0)"
		class hspace(xsc.IntAttr):
			"Sets the blank space to the left of the image on the screen. (1.0)"
		class vspace(xsc.IntAttr):
			"Sets the blank space between the image and the preceding line. (1.0)"
		class alt(xsc.TextAttr):
			"Designates a text string that can be shown as an alternative to the image. (1.0)"


class input(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr):
			"""
			Displays a textbox (``text``), a password input textbox (``password``),
			checkbox (``checkbox``), radio button (``radio``), hidden field
			(``hidden``), submit (``submit``) or reset (``reset``) (1.0)
			"""
		class name(xsc.TextAttr):
			"""
			Designates the name of the field employed to pass the data, obtained
			using the :class:`input` tag, to an CGI script and others. (1.0)
			"""
		class size(xsc.IntAttr):
			"Designates the width of the textbox by number of characters. (1.0)"
		class maxlength(xsc.IntAttr):
			"Limits the number of characters that can be input to the textbox. (1.0)"
		class accesskey(xsc.TextAttr):
			"Directkey function. (1.0)"
		class value(xsc.TextAttr):
			"Designates the initial value of the data. (1.0)"
		class istyle(xsc.TextAttr):
			"(2.0)"
		class checked(xsc.BoolAttr):
			"Makes a selected checkbox the default. (1.0)"


class li(xsc.Element):
	"""
	A list item (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr):
			"""
			Designates number format of a list. ``1`` is numeric, ``A`` is capital
			Roman letters, and ``a`` is lower-case Roman letters. (2.0)
			"""
		class value(xsc.IntAttr):
			"Designates the starting number of a list. (2.0)"


class marquee(xsc.Element):
	"""
	Scrolls text horizontally (2.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class behaviour(xsc.TextAttr):
			"""
			Designates whether text will scroll off screen, stop at the edge of
			the screen, etc. (``scroll``, ``slide`` or ``alternate``) (2.0)
			"""
		class direction(xsc.TextAttr):
			"""
			Designates which direction text will scroll. (``left`` or ``right``) (2.0)
			"""
		class loop(xsc.IntAttr):
			"Designates how many times the text will scroll. (2.0)"
		class height(xsc.TextAttr):
			"Designates height. (Fixed at one line (Cannot be changed by user.).) (2.0)"
		class width(xsc.TextAttr):
			"Designates width. (Fixed to screen width (Cannot be changed by user.).) (2.0)"
		class scrollamount(xsc.TextAttr):
			"Designates the distance the text will scroll. (Cannot be changed by user.) (2.0)"
		class scrolldelay(xsc.TextAttr):
			"Designates the time it takes for text to scroll. (Cannot be changed by user.) (2.0)"


class menu(xsc.Element):
	"""
	Creates a menu list (1.0)
	"""
	xmlns = xmlns


class meta(xsc.Element):
	"""
	Page meta information (2.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr):
			"Designates the name of the meta field"
		class http_equiv(xsc.TextAttr):
			"Designates the HTTP header fields you want to emulate. (Fixed to ``Content-Type``) (2.0)"
			xmlname = "http-equiv"
		class content(xsc.TextAttr):
			"Designates content type (Fixed ``to text/html; charset=SHIFT_JIS``) (2.0)"

	def publish(self, publisher):
		if "http_equiv" in self.attrs:
			ctype = str(self["http_equiv"]).lower()
			if ctype == "content-type" and "content" in self.attrs:
				(contenttype, options) = cgi.parse_header(str(self["content"]))
				if "charset" not in options or options["charset"] != publisher.encoding:
					options["charset"] = publisher.encoding
					node = self.__class__(
						self.attrs,
						http_equiv="Content-Type",
						content=(contenttype, "; ", "; ".join("{}={}".format(*option) for option in options.items()))
					)
					return node.publish(publisher) # return a generator-iterator
		return super().publish(publisher) # return a generator-iterator


class object(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class declare(xsc.BoolAttr):
			"Identifier that that declares and OBJECT ??? (3.0)"
		class id(xsc.TextAttr):
			"The ID of this OBJECT tag (unique within HTML). (3.0)"
		class data(xsc.URLAttr):
			"The URL of the i appli ADF that corresponds to the OBJECT tag. (3.0)"
		class type(xsc.TextAttr):
			"""Content type of the ADF designated in the data attribute ("application/x-jam" fixed). (2.0)"""


class ol(xsc.Element):
	"""
	Creates a numbered list. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr):
			"""
			Designates number format of a list. ``1`` is numeric, ``A`` is capital Roman letters,
			and ``a`` is lower-case Roman letters. (2.0)
			"""
		class start(xsc.IntAttr):
			"Designates the starting number of a list. (2.0)"


class option(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class selected(xsc.BoolAttr):
			"Designates the selected (initial value). (2.0)"
		class value(xsc.TextAttr):
			"Designates selected menu items. (1.0)"


class p(xsc.Element):
	"""
	Creates a text block. (1.0)
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class align(xsc.TextAttr):
			"Aligns the content left or right or centers it (1.0)"


class plaintext(xsc.Element):
	"""
	Displays a text file exactly as entered.
	"""
	xmlns = xmlns


class pre(xsc.Element):
	"""
	Displays a source file exactly as entered, including line feeds and blank
	spaces.
	"""
	xmlns = xmlns


class select(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr):
			"Designates the name of the list for passing selected items. (1.0)"
		class size(xsc.IntAttr):
			"Designates the number of lines for the list. (1.0)"
		class multiple(xsc.BoolAttr):
			"Enables multiple selections. (2.0)"


class textarea(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr):
			"""
			Designates the name of the field employed to pass the data, obtained
			using the TEXTAREA tag, to a CGI script and others. (1.0)
			"""
		class accesschar(xsc.TextAttr):
			"(1.0)"
		class rows(xsc.IntAttr):
			"Designates the height of the input box field. (1.0)"
		class cols(xsc.IntAttr):
			"Designates the width of the input box field. (1.0)"
		class istyle(xsc.TextAttr):
			"Designates full-size Kana, half-size Kana, Roman letters, and numerals. (2.0)"


class title(xsc.Element):
	"""
	Designates the page title.
	"""
	xmlns = xmlns


class ul(xsc.Element):
	"""
	Creates a bullet point list (o).
	"""
	xmlns = xmlns


###
### "picture symbols"
###

# Weather
class fine(xsc.CharRef): codepoint = 0xe63e; xmlns = xmlns
class cloudy(xsc.CharRef): codepoint = 0xe63f; xmlns = xmlns
class rain(xsc.CharRef): codepoint = 0xe640; xmlns = xmlns
class snow(xsc.CharRef): codepoint = 0xe641; xmlns = xmlns
class thunder(xsc.CharRef): codepoint = 0xe642; xmlns = xmlns
class typhoon(xsc.CharRef): codepoint = 0xe643; xmlns = xmlns
class fog(xsc.CharRef): codepoint = 0xe644; xmlns = xmlns
class drizzle(xsc.CharRef): codepoint = 0xe645; xmlns = xmlns

# Horoscope
class aries(xsc.CharRef): codepoint = 0xe646; xmlns = xmlns
class taurus(xsc.CharRef): codepoint = 0xe647; xmlns = xmlns
class gemini(xsc.CharRef): codepoint = 0xe648; xmlns = xmlns
class cancer(xsc.CharRef): codepoint = 0xe649; xmlns = xmlns
class leo(xsc.CharRef): codepoint = 0xe64a; xmlns = xmlns
class virgo(xsc.CharRef): codepoint = 0xe64b; xmlns = xmlns
class libra(xsc.CharRef): codepoint = 0xe64c; xmlns = xmlns
class scorpio(xsc.CharRef): codepoint = 0xe64d; xmlns = xmlns
class sagittarius(xsc.CharRef): codepoint = 0xe64e; xmlns = xmlns
class capricorn(xsc.CharRef): codepoint = 0xe64f; xmlns = xmlns
class aquarius(xsc.CharRef): codepoint = 0xe650; xmlns = xmlns
class pisces(xsc.CharRef): codepoint = 0xe651; xmlns = xmlns

# Sports
class sports(xsc.CharRef): codepoint = 0xe652; xmlns = xmlns
class baseball(xsc.CharRef): codepoint = 0xe653; xmlns = xmlns
class golf(xsc.CharRef): codepoint = 0xe654; xmlns = xmlns
class tennis(xsc.CharRef): codepoint = 0xe655; xmlns = xmlns
class soccer(xsc.CharRef): codepoint = 0xe656; xmlns = xmlns
class ski(xsc.CharRef): codepoint = 0xe657; xmlns = xmlns
class basketball(xsc.CharRef): codepoint = 0xe658; xmlns = xmlns
class motorsports(xsc.CharRef): codepoint = 0xe659; xmlns = xmlns

# General
class pager(xsc.CharRef): codepoint = 0xe65a; xmlns = xmlns

# Transport
class train(xsc.CharRef): codepoint = 0xe65b; xmlns = xmlns
class subway(xsc.CharRef): codepoint = 0xe65c; xmlns = xmlns
class bullettrain(xsc.CharRef): codepoint = 0xe65d; xmlns = xmlns
class carsedan(xsc.CharRef): codepoint = 0xe65e; xmlns = xmlns
class carrv(xsc.CharRef): codepoint = 0xe65f; xmlns = xmlns
class bus(xsc.CharRef): codepoint = 0xe660; xmlns = xmlns
class ship(xsc.CharRef): codepoint = 0xe661; xmlns = xmlns
class airplane(xsc.CharRef): codepoint = 0xe662; xmlns = xmlns

# Town map
class house(xsc.CharRef): codepoint = 0xe663; xmlns = xmlns
class building(xsc.CharRef): codepoint = 0xe664; xmlns = xmlns
class postoffice(xsc.CharRef): codepoint = 0xe665; xmlns = xmlns
class hospital(xsc.CharRef): codepoint = 0xe666; xmlns = xmlns
class bank(xsc.CharRef): codepoint = 0xe667; xmlns = xmlns
class atm(xsc.CharRef): codepoint = 0xe668; xmlns = xmlns
class hotel(xsc.CharRef): codepoint = 0xe669; xmlns = xmlns
class conveniencestore(xsc.CharRef): codepoint = 0xe66a; xmlns = xmlns
class gasstation(xsc.CharRef): codepoint = 0xe66b; xmlns = xmlns
class parking(xsc.CharRef): codepoint = 0xe66c; xmlns = xmlns
class trafficsignal(xsc.CharRef): codepoint = 0xe66d; xmlns = xmlns
class toilet(xsc.CharRef): codepoint = 0xe66e; xmlns = xmlns
class restaurant(xsc.CharRef): codepoint = 0xe66f; xmlns = xmlns
class cafe(xsc.CharRef): codepoint = 0xe670; xmlns = xmlns
class bar(xsc.CharRef): codepoint = 0xe671; xmlns = xmlns
class beer(xsc.CharRef): codepoint = 0xe672; xmlns = xmlns
class fastfood(xsc.CharRef): codepoint = 0xe673; xmlns = xmlns
class boutique(xsc.CharRef): codepoint = 0xe674; xmlns = xmlns
class hairdresser(xsc.CharRef): codepoint = 0xe675; xmlns = xmlns
class karaoke(xsc.CharRef): codepoint = 0xe676; xmlns = xmlns
class movie(xsc.CharRef): codepoint = 0xe677; xmlns = xmlns

# Others
class diagonallyupwardtowardright(xsc.CharRef): codepoint = 0xe678; xmlns = xmlns

# Town map
class amusementpark(xsc.CharRef): codepoint = 0xe679; xmlns = xmlns
class music(xsc.CharRef): codepoint = 0xe67a; xmlns = xmlns
class art(xsc.CharRef): codepoint = 0xe67b; xmlns = xmlns
class drama(xsc.CharRef): codepoint = 0xe67c; xmlns = xmlns
class event(xsc.CharRef): codepoint = 0xe67d; xmlns = xmlns
class ticket(xsc.CharRef): codepoint = 0xe67e; xmlns = xmlns
class smoking(xsc.CharRef): codepoint = 0xe67f; xmlns = xmlns
class nonsmoking(xsc.CharRef): codepoint = 0xe680; xmlns = xmlns

# Gazette
class camera(xsc.CharRef): codepoint = 0xe681; xmlns = xmlns
class bag(xsc.CharRef): codepoint = 0xe682; xmlns = xmlns
class book(xsc.CharRef): codepoint = 0xe683; xmlns = xmlns
class ribbon(xsc.CharRef): codepoint = 0xe684; xmlns = xmlns
class present(xsc.CharRef): codepoint = 0xe685; xmlns = xmlns
class birthday(xsc.CharRef): codepoint = 0xe686; xmlns = xmlns
class phone(xsc.CharRef): codepoint = 0xe687; xmlns = xmlns
class mobilephone(xsc.CharRef): codepoint = 0xe688; xmlns = xmlns
class memo(xsc.CharRef): codepoint = 0xe689; xmlns = xmlns
class tv(xsc.CharRef): codepoint = 0xe68a; xmlns = xmlns
class game(xsc.CharRef): codepoint = 0xe68b; xmlns = xmlns
class cd(xsc.CharRef): codepoint = 0xe68c; xmlns = xmlns

# Playing
class cardsheart(xsc.CharRef): codepoint = 0xe68d; xmlns = xmlns
class cardsspade(xsc.CharRef): codepoint = 0xe68e; xmlns = xmlns
class cardsdiamond(xsc.CharRef): codepoint = 0xe68f; xmlns = xmlns
class cardsclub(xsc.CharRef): codepoint = 0xe690; xmlns = xmlns

# Body
class eyes(xsc.CharRef): codepoint = 0xe691; xmlns = xmlns
class ear(xsc.CharRef): codepoint = 0xe692; xmlns = xmlns
class handrock(xsc.CharRef): codepoint = 0xe693; xmlns = xmlns
class handscissors(xsc.CharRef): codepoint = 0xe694; xmlns = xmlns
class handpaper(xsc.CharRef): codepoint = 0xe695; xmlns = xmlns

# Others
class diagonallydownwardtowardright(xsc.CharRef): codepoint = 0xe696; xmlns = xmlns
class diagonallyupwardtowardleft(xsc.CharRef): codepoint = 0xe697; xmlns = xmlns

# Body
class foot(xsc.CharRef): codepoint = 0xe698; xmlns = xmlns
class shoe(xsc.CharRef): codepoint = 0xe699; xmlns = xmlns
class eyeclasses(xsc.CharRef): codepoint = 0xe69a; xmlns = xmlns
class wheelchair(xsc.CharRef): codepoint = 0xe69b; xmlns = xmlns

# Moon
class newmoon(xsc.CharRef): codepoint = 0xe69c; xmlns = xmlns
class waningmoon(xsc.CharRef): codepoint = 0xe69d; xmlns = xmlns
class halfmoon(xsc.CharRef): codepoint = 0xe69e; xmlns = xmlns
class crescentmoon(xsc.CharRef): codepoint = 0xe69f; xmlns = xmlns
class fullmoon(xsc.CharRef): codepoint = 0xe6a0; xmlns = xmlns

# Others
class dog(xsc.CharRef): codepoint = 0xe6a1; xmlns = xmlns
class cat(xsc.CharRef): codepoint = 0xe6a2; xmlns = xmlns
class resort(xsc.CharRef): codepoint = 0xe6a3; xmlns = xmlns
class christmas(xsc.CharRef): codepoint = 0xe6a4; xmlns = xmlns

class diagonallydownwardtowardleft(xsc.CharRef): codepoint = 0xe6a5; xmlns = xmlns

# Service
class phoneto(xsc.CharRef): codepoint = 0xe6ce; xmlns = xmlns
class mailto(xsc.CharRef): codepoint = 0xe6cf; xmlns = xmlns
class faxto(xsc.CharRef): codepoint = 0xe6d0; xmlns = xmlns
class email(xsc.CharRef): codepoint = 0xe6d3; xmlns = xmlns
class providedbydocomo(xsc.CharRef): codepoint = 0xe6d4; xmlns = xmlns
class docomopoint(xsc.CharRef): codepoint = 0xe6d5; xmlns = xmlns
class feecharging(xsc.CharRef): codepoint = 0xe6d6; xmlns = xmlns
class freeofcharge(xsc.CharRef): codepoint = 0xe6d7; xmlns = xmlns
class id(xsc.CharRef): codepoint = 0xe6d8; xmlns = xmlns
class password(xsc.CharRef): codepoint = 0xe6d9; xmlns = xmlns
class continuing(xsc.CharRef): codepoint = 0xe6da; xmlns = xmlns
class clear(xsc.CharRef): codepoint = 0xe6db; xmlns = xmlns
class search(xsc.CharRef): codepoint = 0xe6dc; xmlns = xmlns
class new(xsc.CharRef): codepoint = 0xe6dd; xmlns = xmlns
class locationinformation(xsc.CharRef): codepoint = 0xe6de; xmlns = xmlns
class freedial(xsc.CharRef): codepoint = 0xe6df; xmlns = xmlns
class sharpdial(xsc.CharRef): codepoint = 0xe6e0; xmlns = xmlns
class mopaq(xsc.CharRef): codepoint = 0xe6e1; xmlns = xmlns
class key1(xsc.CharRef): codepoint = 0xe6e2; xmlns = xmlns
class key2(xsc.CharRef): codepoint = 0xe6e3; xmlns = xmlns
class key3(xsc.CharRef): codepoint = 0xe6e4; xmlns = xmlns
class key4(xsc.CharRef): codepoint = 0xe6e5; xmlns = xmlns
class key5(xsc.CharRef): codepoint = 0xe6e6; xmlns = xmlns
class key6(xsc.CharRef): codepoint = 0xe6e7; xmlns = xmlns
class key7(xsc.CharRef): codepoint = 0xe6e8; xmlns = xmlns
class key8(xsc.CharRef): codepoint = 0xe6e9; xmlns = xmlns
class key9(xsc.CharRef): codepoint = 0xe6ea; xmlns = xmlns
class key0(xsc.CharRef): codepoint = 0xe6eb; xmlns = xmlns

# Mail
class blackheart(xsc.CharRef): codepoint = 0xe6ec; xmlns = xmlns
class flutteringheart(xsc.CharRef): codepoint = 0xe6ed; xmlns = xmlns
class heartbreak(xsc.CharRef): codepoint = 0xe6ee; xmlns = xmlns
class hearts(xsc.CharRef): codepoint = 0xe6ef; xmlns = xmlns
class happyface(xsc.CharRef): codepoint = 0xe6f0; xmlns = xmlns
class angryface(xsc.CharRef): codepoint = 0xe6f1; xmlns = xmlns
class disappointedface(xsc.CharRef): codepoint = 0xe6f2; xmlns = xmlns
class sadface(xsc.CharRef): codepoint = 0xe6f3; xmlns = xmlns
class dizzy(xsc.CharRef): codepoint = 0xe6f4; xmlns = xmlns
class good(xsc.CharRef): codepoint = 0xe6f5; xmlns = xmlns
class cheerful(xsc.CharRef): codepoint = 0xe6f6; xmlns = xmlns
class comfort(xsc.CharRef): codepoint = 0xe6f7; xmlns = xmlns
class cute(xsc.CharRef): codepoint = 0xe6f8; xmlns = xmlns
class kiss(xsc.CharRef): codepoint = 0xe6f9; xmlns = xmlns
class shining(xsc.CharRef): codepoint = 0xe6fa; xmlns = xmlns
class goodidea(xsc.CharRef): codepoint = 0xe6fb; xmlns = xmlns
class angry(xsc.CharRef): codepoint = 0xe6fc; xmlns = xmlns
class punch(xsc.CharRef): codepoint = 0xe6fd; xmlns = xmlns
class bomb(xsc.CharRef): codepoint = 0xe6fe; xmlns = xmlns
class mood(xsc.CharRef): codepoint = 0xe6ff; xmlns = xmlns
class bad(xsc.CharRef): codepoint = 0xe700; xmlns = xmlns
class sleepy(xsc.CharRef): codepoint = 0xe701; xmlns = xmlns
class exclamation(xsc.CharRef): codepoint = 0xe702; xmlns = xmlns
class exclamationquestion(xsc.CharRef): codepoint = 0xe703; xmlns = xmlns
class exclamation2(xsc.CharRef): codepoint = 0xe704; xmlns = xmlns
class bump(xsc.CharRef): codepoint = 0xe705; xmlns = xmlns
class sweat(xsc.CharRef): codepoint = 0xe706; xmlns = xmlns
class coldsweat(xsc.CharRef): codepoint = 0xe707; xmlns = xmlns
class dash(xsc.CharRef): codepoint = 0xe708; xmlns = xmlns
class macron1(xsc.CharRef): codepoint = 0xe709; xmlns = xmlns
class macron2(xsc.CharRef): codepoint = 0xe70a; xmlns = xmlns
class fixed(xsc.CharRef): codepoint = 0xe70b; xmlns = xmlns


# Boiled down version of the same stuff in the html namespace
pe_special_extra = (object, img)
pe_special_basic = (br, )
pe_special = pe_special_basic + pe_special_extra
pe_fontstyle = (font, )
pe_inline_forms = (input, select, textarea)
pe_inline = (a,) + pe_special + pe_fontstyle + pe_inline_forms
pe_Inline = pe_inline
pe_heading = (h1, h2, h3, h4, h5, h6)
pe_lists = (ul, ol, dl, menu, dir)
pe_blocktext = (pre, hr, blockquote, center)
pe_block = (p,) + pe_heading + (div,) + pe_lists + pe_blocktext
pe_Flow = pe_block + (form,) + pe_inline


base.model = \
meta.model = \
hr.model = \
br.model = \
img.model = \
input.model = sims.Empty()
# Just a guess for blink, plaintext and marquee
body.model = \
div.model = \
li.model = \
dd.model = \
blockquote.model = \
blink.model = \
plaintext.model = \
marquee.model = \
center.model = sims.ElementsOrText(*pe_Flow)
p.model = \
h1.model = \
h2.model = \
h3.model = \
h4.model = \
h5.model = \
h6.model = \
dt.model = \
font.model = sims.ElementsOrText(*pe_Inline)
ul.model = \
ol.model = \
menu.model = \
dir.model = sims.Elements(li)
title.model = \
option.model = \
textarea.model = sims.NoElements()
object.model = sims.ElementsOrText(*(pe_block + (form,) + pe_inline))
dl.model = sims.Elements(dt, dd)
html.model = sims.Elements(head, body)
select.model = sims.Elements(option)
head.model = sims.Elements(title, base, meta, object)
pre.model = sims.ElementsOrText(*((a,) + pe_special_basic + pe_inline_forms))
form.model = sims.ElementsOrText(*(pe_block + pe_inline))
a.model = sims.ElementsOrText(*(pe_special + pe_fontstyle + pe_inline_forms))
