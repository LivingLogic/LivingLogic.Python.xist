#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<doc:par>An &xist; module that contains the elements and entities for
i-mode compatible &html;.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from xist import xsc

class a(xsc.Element):
	empty = 0
	attrHandlers = {
		"name": xsc.TextAttr, # Designates a marker name within an HTML file (1.0)
		"accesskey": xsc.TextAttr, # Directkey function (1.0)
		"href": xsc.URLAttr, # Designates a link to a Web site (http), e-amil address (mailto) or phone number (tel) (1.0)
		"cti": xsc.TextAttr, # Dial function + tone input function (2.0)
		"ijam": xsc.TextAttr, # Designates the ID of the downloaded i appli that the OBJECT tag specifies. (3.0)
		"utn": xsc.BoolAttr, # Verifies individual identification information (3.0)
		"subject": xsc.TextAttr, # Designates the subject with mailto: (3.0)
		"body": xsc.TextAttr, # Designates the body with mailto: (3.0)
		"telbook": xsc.TextAttr, # Records in telphone book (3.0)
		"kana": xsc.TextAttr, # Records in telphone book (3.0)
		"e-mail": xsc.TextAttr # Records in telphone book (3.0)
	}

class base(xsc.Element):
	"""
	Designates the base URL for the relative paths used in an HTML file. (1.0)
	"""
	empty = 1
	attrHandlers = {
		"href": xsc.URLAttr
	}

class blink(xsc.Element):
	"""
	Blinks the designated text. (2.0)
	"""
	empty = 0

class blockquote(xsc.Element):
	"""
	Creates a text block and displays a quote mark. (1.0)
	"""
	empty = 0

class body(xsc.Element):
	"""
	Designates content to be displayed as a page.
	"""
	empty = 0
	attrHandlers = {
		"bgcolor": xsc.TextAttr, # Designates background color (2.0)
		"text": xsc.TextAttr, # Designates text color (2.0)
		"link": xsc.TextAttr # Designates link color (2.0)
	}

class br(xsc.Element):
	empty = 1
	attrHandlers = {
		"clear": xsc.TextAttr # Designates the way a character string wraps around an inline image by deciding where line feeding takes place. Depending on the attribute, it also cancels the wraparound function. (1.0)
	}

class center(xsc.Element):
	"""
	Centers character strings, images and tables. (1.0)
	"""
	empty = 0

class dd(xsc.Element):
	"""
	Creates a definition list. (See <pyref class="dl"><class>dl</class></pyref>) (1.0)
	"""
	empty = 0

class dir(xsc.Element):
	"""
	Creates a list of menus or directories. Each list item must be a <pyref class="li"><class>li</class></pyref>. (1.0)
	"""
	empty = 0

class div(xsc.Element):
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Aligns the content left or right or centers it (1.0)
	}

class dl(xsc.Element):
	"""
	Creates a definition list. The content consists of <pyref class="dd"><class>dd</class></pyref> and
	<pyref class="dt"><class>dt</class></pyref> elements. (1.0)
	"""
	empty = 0

class dt(xsc.Element):
	"""
	Designates the list heading and aligns the character string at left. (1.0)
	"""
	empty = 0

class font(xsc.Element):
	"""
	Designates the color of a certain portion of text. (2.0)
	"""
	empty = 0
	attrHandlers = {
		"color": xsc.TextAttr
	}

class form(xsc.Element):
	"""
	Encloses an area to be shown as a data input form. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"action": xsc.URLAttr, # URL or e-mail address (mailto) the input form will be sent to. (1.0)
		"method": xsc.TextAttr, # Designates the method by which data is sent to the server, to either post or get. (1.0)
		"utn": xsc.BoolAttr # Verifies individual identification information. (3.0)
	}

class head(xsc.Element):
	"""
	Designates the information that is used as the page title and/or by the server. The <class>head</class> tag follows the <pyref class="html"><class>html</class></pyref> tag. (1.0)
	"""
	empty = 0

class h1(xsc.Element):
	"""
	Designates level 1 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class h2(xsc.Element):
	"""
	Designates level 2 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class h3(xsc.Element):
	"""
	Designates level 3 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class h4(xsc.Element):
	"""
	Designates level 4 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class h5(xsc.Element):
	"""
	Designates level 5 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class h6(xsc.Element):
	"""
	Designates level 6 header. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Designates the alignment of the header. (1.0)
	}

class hr(xsc.Element):
	"""
	Designates the settings of the horizontal dividing line. (1.0)
	"""
	empty = 1
	attrHandlers = {
		"align": xsc.TextAttr, # Designates the alignment of the horizontal line. (1.0)
		"size": xsc.TextAttr, # Sets the thickness of the horizontal line.(1.0)
		"width": xsc.TextAttr, # Determines the length of the horizontal line. (1.0)
		"noshade": xsc.BoolAttr # Gives the horizontal line a two-dimensional appearance. (1.0)
	}

class html(xsc.Element):
	"""
	The root element
	"""
	empty = 0

class img(xsc.Element):
	"""
	Designates an image file (1.0)
	"""
	empty = 1
	attrHandlers = {
		"src": xsc.URLAttr, # the image URL (1.0)
		"align": xsc.TextAttr, # Defines the way the image and character string are laid out, and how the character string wraps around the image. <lit>top</lit>, <lit>middle</lit> or <lit>bottom</lit>. (1.0)
		"width": xsc.TextAttr, # Sets the image width (1.0)
		"height": xsc.TextAttr, # Sets the image height (1.0)
		"hspace": xsc.IntAttr, # Sets the blank space to the left of the image on the screen. (1.0)
		"vspace": xsc.IntAttr, # Sets the blank space between the image and the preceding line. (1.0)
		"alt": xsc.TextAttr, # Designates a text string that can be shown as an alternative to the image. (1.0)
	}

class input(xsc.Element):
	empty = 1
	attrHandlers = {
		"type": xsc.TextAttr, # Displays a textbox (<lit>text</lit>), a password input textbox (<lit>password</lit>), checkbox (<lit>checkbox</lit>), radio button (<lit>radio</lit>), hidden field (<lit>hidden</lit>), submit (<lit>submit</lit>) or reset (<lit>reset</lit>) (1.0)
		"name": xsc.TextAttr, # Designates the name of the field employed to pass the data, obtained using the <class>input</class> tag, to an &cgi; script and others. (1.0)
		"size": xsc.IntAttr, # Designates the width of the textbox by number of characters. (1.0)
		"maxlength": xsc.IntAttr, # Limits the number of characters that can be input to the textbox. (1.0)
		"accesskey": xsc.TextAttr, # Directkey function. (1.0)
		"value": xsc.TextAttr, # Designates the initial value of the data. (1.0)
		"istyle": xsc.TextAttr, # (2.0)
		"checked": xsc.BoolAttr # Makes a selected checkbox the default.(1.0)
	}

class li(xsc.Element):
	"""
	A list item (1.0)
	"""
	empty = 0
	attrHandlers = {
		"type": xsc.TextAttr, # Designates number format of a list. <lit>1</lit> is numeric, <lit>A</lit> is capital Roman letters, and <lit>a</lit> is lower-case Roman letters. (2.0)
		"value": xsc.IntAttr, # Designates the starting number of a list. (2.0)
	}

class marquee(xsc.Element):
	"""
	Scrolls text horizontally (2.0)
	"""
	empty = 1
	attrHandlers = {
		"behaviour": xsc.TextAttr, # Designates whether text will scroll off screen, stop at the edge of the screen, etc. (<lit>scroll</lit>, <lit>slide</lit> or <lit>alternate</lit>) (2.0)
		"direction": xsc.TextAttr, # Designates which direction text will scroll. (<lit>left</lit> or <lit>right</lit>) (2.0)
		"loop": xsc.IntAttr, # Designates how many times the text will scroll. (2.0)
		"height": xsc.TextAttr, # Designates height. (Fixed at one line (Cannot be changed by user.).) (2.0)
		"width": xsc.TextAttr, # Designates width. (Fixed to screen width (Cannot be changed by user.).) (2.0)
		"scrollamount": xsc.TextAttr, # Designates the distance the text will scroll. (Cannot be changed by user.) (2.0)
		"scrolldelay": xsc.TextAttr, # Designates the time it takes for text to scroll. (Cannot be changed by user.) (2.0)
	}

class menu(xsc.Element):
	"""
	Creates a menu list (1.0)
	"""
	empty = 0

class meta(xsc.Element):
	"""
	Page meta information (2.0)
	"""
	empty = 1
	attrHandlers = {
		"http-equiv": xsc.TextAttr, # Designates the HTTP header fields you want to emulate. (Fixed to <lit>Content-Type</lit>) (2.0)
		"http_equiv": xsc.TextAttr, # copy of the above
		"content": xsc.TextAttr # Designates content type (Fixed <lit>to text/html; charset=SHIFT_JIS</lit>) (2.0)
	}

	def __init__(self, *_content, **_attrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		xsc.Element.__init__(self, *_content, **_attrs)
		if self.hasAttr("http_equiv"):
			if not self.hasAttr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]

	def publish(self, publisher):
		if self.hasAttr("http-equiv"):
			ctype = unicode(self["http-equiv"]).lower()
			if ctype == u"content-type" and self.hasAttr("content"):
				(contenttype, options) = cgi.parse_header(unicode(self["content"]))
				if not options.has_key(u"charset") or options[u"charset"] != publisher.encoding:
					options[u"charset"] = publisher.encoding
					node = meta(
						self.attrs,
						http_equiv="Content-Type",
						content=(contenttype, u"; ", u"; ".join([ "%s=%s" % option for option in options.items()]))
					)
					node.publish(publisher)
					return
		super(meta, self).publish(publisher)

class object(xsc.Element):
	empty = 1
	attrHandlers = {
		"declare": xsc.BoolAttr, # Identifier that that declares and OBJECT ??? (3.0)
		"id": xsc.TextAttr, # The ID of this OBJECT tag (unique within HTML). (3.0)
		"data": xsc.URLAttr, # The URL of the i appli ADF that correspondes to the OBJECT tag. (3.0)
		"type": xsc.TextAttr, # Content type of the ADF designated in the data attribute ("application/x-jam" fixed). (2.0)
	}

class ol(xsc.Element):
	"""
	Creates a numbered list. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"type": xsc.TextAttr, # Designates number format of a list. <lit>1</lit> is numeric, <lit>A</lit> is capital Roman letters, and <lit>a</lit> is lower-case Roman letters. (2.0)
		"start": xsc.IntAttr, # Designates the starting number of a list. (2.0)
	}


class option(xsc.Element):
	empty = 0
	attrHandlers = {
		"selected": xsc.BoolAttr, # Designates the selected (initial value). (2.0)
		"value": xsc.TextAttr, # Designates selected menu items. (1.0)
	}

class p(xsc.Element):
	"""
	Creates a text block. (1.0)
	"""
	empty = 0
	attrHandlers = {
		"align": xsc.TextAttr # Aligns the content left or right or centers it (1.0)
	}

class plaintext(xsc.Element):
	"""
	Displays a text file exactly as entered.
	"""
	empty = 0

class pre(xsc.Element):
	"""
	Displays a source file exactly as entered, including line feeds and blank spaces.
	"""
	empty = 0

class select(xsc.Element):
	empty = 0
	attrHandlers = {
		"name": xsc.TextAttr, # Designates the name of the list for passing selected items. (1.0)
		"size": xsc.IntAttr, # Designates the number of lines for the list. (1.0)
		"multiple": xsc.BoolAttr # Enables multiple selections. (2.0)
	}

class textarea(xsc.Element):
	empty = 1
	attrHandlers = {
		"name": xsc.TextAttr, # Designates the name of the field employed to pass the data, obtained using the TEXTAREA tag, to a CGI script and others. (1.0)
		"accesschar": xsc.IntAttr, # (1.0)
		"rows": xsc.IntAttr, # Designates the height of the input box field. (1.0)
		"cols": xsc.IntAttr, # Designates the width of the input box field. (1.0)
		"istyle": xsc.TextAttr # Designates full-size Kana, half-size Kana, Roman letters, and numerals. (2.0)
	}


class title(xsc.Element):
	"""
	Designates the page title.
	"""
	empty = 0

class ul(xsc.Element):
	"""
	Creates a bullet point list (o).
	"""
	empty = 0

###
### "picture symbols"
###

# Weather
class fine(xsc.CharRef): codepoint = 0xe63e
class cloudy(xsc.CharRef): codepoint = 0xe63f
class rain(xsc.CharRef): codepoint = 0xe640
class snow(xsc.CharRef): codepoint = 0xe641
class thunder(xsc.CharRef): codepoint = 0xe642
class typhoon(xsc.CharRef): codepoint = 0xe643
class fog(xsc.CharRef): codepoint = 0xe644
class drizzle(xsc.CharRef): codepoint = 0xe645

# Horoscope
class aries(xsc.CharRef): codepoint = 0xe646
class taurus(xsc.CharRef): codepoint = 0xe647
class gemini(xsc.CharRef): codepoint = 0xe648
class cancer(xsc.CharRef): codepoint = 0xe649
class leo(xsc.CharRef): codepoint = 0xe64a
class virgo(xsc.CharRef): codepoint = 0xe64b
class libra(xsc.CharRef): codepoint = 0xe64c
class scorpio(xsc.CharRef): codepoint = 0xe64d
class sagittarius(xsc.CharRef): codepoint = 0xe64e
class capricorn(xsc.CharRef): codepoint = 0xe64f
class aquarius(xsc.CharRef): codepoint = 0xe650
class pisces(xsc.CharRef): codepoint = 0xe651

# Sports
class sports(xsc.CharRef): codepoint = 0xe652
class baseball(xsc.CharRef): codepoint = 0xe653
class golf(xsc.CharRef): codepoint = 0xe654
class tennis(xsc.CharRef): codepoint = 0xe655
class soccer(xsc.CharRef): codepoint = 0xe656
class ski(xsc.CharRef): codepoint = 0xe657
class basketball(xsc.CharRef): codepoint = 0xe658
class motorsports(xsc.CharRef): codepoint = 0xe659

# General
class pager(xsc.CharRef): codepoint = 0xe65a

# Transport
class train(xsc.CharRef): codepoint = 0xe65b
class subway(xsc.CharRef): codepoint = 0xe65c
class bullettrain(xsc.CharRef): codepoint = 0xe65d
class carsedan(xsc.CharRef): codepoint = 0xe65e
class carrv(xsc.CharRef): codepoint = 0xe65f
class bus(xsc.CharRef): codepoint = 0xe660
class ship(xsc.CharRef): codepoint = 0xe661
class airplane(xsc.CharRef): codepoint = 0xe662

# Town map
class house(xsc.CharRef): codepoint = 0xe663
class building(xsc.CharRef): codepoint = 0xe664
class postoffice(xsc.CharRef): codepoint = 0xe665
class hospital(xsc.CharRef): codepoint = 0xe666
class bank(xsc.CharRef): codepoint = 0xe667
class atm(xsc.CharRef): codepoint = 0xe668
class hotel(xsc.CharRef): codepoint = 0xe669
class conveniencestore(xsc.CharRef): codepoint = 0xe66a
class gasstation(xsc.CharRef): codepoint = 0xe66b
class parking(xsc.CharRef): codepoint = 0xe66c
class trafficsignal(xsc.CharRef): codepoint = 0xe66d
class toilet(xsc.CharRef): codepoint = 0xe66e
class restaurant(xsc.CharRef): codepoint = 0xe66f
class cafe(xsc.CharRef): codepoint = 0xe670
class bar(xsc.CharRef): codepoint = 0xe671
class beer(xsc.CharRef): codepoint = 0xe672
class fastfood(xsc.CharRef): codepoint = 0xe673
class boutique(xsc.CharRef): codepoint = 0xe674
class hairdresser(xsc.CharRef): codepoint = 0xe675
class karaoke(xsc.CharRef): codepoint = 0xe676
class movie(xsc.CharRef): codepoint = 0xe677

# Others
class diagonallyupwardtowardright(xsc.CharRef): codepoint = 0xe678

# Town map
class amusementpark(xsc.CharRef): codepoint = 0xe679
class music(xsc.CharRef): codepoint = 0xe67a
class art(xsc.CharRef): codepoint = 0xe67b
class drama(xsc.CharRef): codepoint = 0xe67c
class event(xsc.CharRef): codepoint = 0xe67d
class ticket(xsc.CharRef): codepoint = 0xe67e
class smoking(xsc.CharRef): codepoint = 0xe67f
class nonsmoking(xsc.CharRef): codepoint = 0xe680

# Gazette
class camera(xsc.CharRef): codepoint = 0xe681
class bag(xsc.CharRef): codepoint = 0xe682
class book(xsc.CharRef): codepoint = 0xe683
class ribbon(xsc.CharRef): codepoint = 0xe684
class present(xsc.CharRef): codepoint = 0xe685
class birthday(xsc.CharRef): codepoint = 0xe686
class phone(xsc.CharRef): codepoint = 0xe687
class mobilephone(xsc.CharRef): codepoint = 0xe688
class memo(xsc.CharRef): codepoint = 0xe689
class tv(xsc.CharRef): codepoint = 0xe68a
class game(xsc.CharRef): codepoint = 0xe68b
class cd(xsc.CharRef): codepoint = 0xe68c

# Playing
class cardsheart(xsc.CharRef): codepoint = 0xe68d
class cardsspade(xsc.CharRef): codepoint = 0xe68e
class cardsdiamond(xsc.CharRef): codepoint = 0xe68f
class cardsclub(xsc.CharRef): codepoint = 0xe690

# Body
class eyes(xsc.CharRef): codepoint = 0xe691
class ear(xsc.CharRef): codepoint = 0xe692
class handrock(xsc.CharRef): codepoint = 0xe693
class handscissors(xsc.CharRef): codepoint = 0xe694
class handpaper(xsc.CharRef): codepoint = 0xe695

# Others
class diagonallydownwardtowardright(xsc.CharRef): codepoint = 0xe696
class diagonallyupwardtowardleft(xsc.CharRef): codepoint = 0xe697

# Body
class foot(xsc.CharRef): codepoint = 0xe698
class shoe(xsc.CharRef): codepoint = 0xe699
class eyeclasses(xsc.CharRef): codepoint = 0xe69a
class wheelchair(xsc.CharRef): codepoint = 0xe69b

# Moon
class newmoon(xsc.CharRef): codepoint = 0xe69c
class waningmoon(xsc.CharRef): codepoint = 0xe69d
class halfmoon(xsc.CharRef): codepoint = 0xe69e
class crescentmoon(xsc.CharRef): codepoint = 0xe69f
class fullmoon(xsc.CharRef): codepoint = 0xe6a0

# Others
class dog(xsc.CharRef): codepoint = 0xe6a1
class cat(xsc.CharRef): codepoint = 0xe6a2
class resort(xsc.CharRef): codepoint = 0xe6a3
class christmas(xsc.CharRef): codepoint = 0xe6a4

class diagonallydownwardtowardleft(xsc.CharRef): codepoint = 0xe6a5

# Service
class phoneto(xsc.CharRef): codepoint = 0xe6ce
class mailto(xsc.CharRef): codepoint = 0xe6cf
class faxto(xsc.CharRef): codepoint = 0xe6d0
class email(xsc.CharRef): codepoint = 0xe6d3
class providedbydocomo(xsc.CharRef): codepoint = 0xe6d4
class docomopoint(xsc.CharRef): codepoint = 0xe6d5
class feecharging(xsc.CharRef): codepoint = 0xe6d6
class freeofcharge(xsc.CharRef): codepoint = 0xe6d7
class id(xsc.CharRef): codepoint = 0xe6d8
class password(xsc.CharRef): codepoint = 0xe6d9
class continuing(xsc.CharRef): codepoint = 0xe6da
class clear(xsc.CharRef): codepoint = 0xe6db
class search(xsc.CharRef): codepoint = 0xe6dc
class new(xsc.CharRef): codepoint = 0xe6dd
class locationinformation(xsc.CharRef): codepoint = 0xe6de
class freedial(xsc.CharRef): codepoint = 0xe6df
class sharpdial(xsc.CharRef): codepoint = 0xe6e0
class mopaq(xsc.CharRef): codepoint = 0xe6e1
class key1(xsc.CharRef): codepoint = 0xe6e2
class key2(xsc.CharRef): codepoint = 0xe6e3
class key3(xsc.CharRef): codepoint = 0xe6e4
class key4(xsc.CharRef): codepoint = 0xe6e5
class key5(xsc.CharRef): codepoint = 0xe6e6
class key6(xsc.CharRef): codepoint = 0xe6e7
class key7(xsc.CharRef): codepoint = 0xe6e8
class key8(xsc.CharRef): codepoint = 0xe6e9
class key9(xsc.CharRef): codepoint = 0xe6ea
class key0(xsc.CharRef): codepoint = 0xe6eb

# Mail
class blackheart(xsc.CharRef): codepoint = 0xe6ec
class flutteringheart(xsc.CharRef): codepoint = 0xe6ed
class heartbreak(xsc.CharRef): codepoint = 0xe6ee
class hearts(xsc.CharRef): codepoint = 0xe6ef
class happyface(xsc.CharRef): codepoint = 0xe6f0
class angryface(xsc.CharRef): codepoint = 0xe6f1
class disappointedface(xsc.CharRef): codepoint = 0xe6f2
class sadface(xsc.CharRef): codepoint = 0xe6f3
class dizzy(xsc.CharRef): codepoint = 0xe6f4
class good(xsc.CharRef): codepoint = 0xe6f5
class cheerful(xsc.CharRef): codepoint = 0xe6f6
class comfort(xsc.CharRef): codepoint = 0xe6f7
class cute(xsc.CharRef): codepoint = 0xe6f8
class kiss(xsc.CharRef): codepoint = 0xe6f9
class shining(xsc.CharRef): codepoint = 0xe6fa
class goodidea(xsc.CharRef): codepoint = 0xe6fb
class angry(xsc.CharRef): codepoint = 0xe6fc
class punch(xsc.CharRef): codepoint = 0xe6fd
class bomb(xsc.CharRef): codepoint = 0xe6fe
class mood(xsc.CharRef): codepoint = 0xe6ff
class bad(xsc.CharRef): codepoint = 0xe700
class sleepy(xsc.CharRef): codepoint = 0xe701
class exclamation(xsc.CharRef): codepoint = 0xe702
class exclamationquestion(xsc.CharRef): codepoint = 0xe703
class exclamation2(xsc.CharRef): codepoint = 0xe704
class bump(xsc.CharRef): codepoint = 0xe705
class sweat(xsc.CharRef): codepoint = 0xe706
class coldsweat(xsc.CharRef): codepoint = 0xe707
class dash(xsc.CharRef): codepoint = 0xe708
class macron1(xsc.CharRef): codepoint = 0xe709
class macron2(xsc.CharRef): codepoint = 0xe70a
class fixed(xsc.CharRef): codepoint = 0xe70b

namespace = xsc.Namespace("ihtml", "http://www.nttdocomo.co.jp/imode", vars())
