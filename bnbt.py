#! /usr/bin/env python

import xsc
import html
import specials

class page(xsc.Element):
	attr_handlers = { "title" : xsc.TextAttr , "head" : xsc.TextAttr , "align" : xsc.TextAttr , "refresh" : xsc.TextAttr , "class" : xsc.TextAttr , "keywords" : xsc.TextAttr , "description" : xsc.TextAttr , "onload" : xsc.TextAttr , "nohome" : xsc.TextAttr , "nosearch" : xsc.TextAttr , "nositemap" : xsc.TextAttr , "nofaq" : xsc.TextAttr , "notinsitemap" : xsc.TextAttr }
	empty = 0

	def asHTML(self):
		h = html.head(
			html.link(rel="stylesheet",type="text/css",href=":stylesheets/bnv.css")+
			html.link(rel="made",href="mailto:html@bnbt.de")
		)
		if self.has_attr("title"):
			h.append(html.title(self["title"]))
		if self.has_attr("refresh"):
			h.append(html.meta(http_equiv="Refresh",content=self["refresh"]))
		if self.has_attr("keywords"):
			h.append(html.meta(http_equiv="keywords",content=self["keywords"]))
		if self.has_attr("description"):
			h.append(html.meta(http_equiv="description",content=self["description"]))
		b = specials.plainbody(bgcolor="#ffffff",text="#000000",link="#cc6633",vlink="#999999",background=":images/SkylineBayreuth.jpg")
		if self.has_attr("class"):
			b["class"] = self["class"]
		if self.has_attr("onload"):
			b["onload"] = self["onload"]

		mylinks = self.elements(element = links)[0].content
		mycontent = self.elements(element = content)[0].content

		if self.has_attr("nohome"):
			myhome = xsc.Null()
		else:
			myhome = navigation(href = ":index.shtml",img = "home",text = "Startseite")
		if self.has_attr("nofaq"):
			myfaq = xsc.Null()
		else:
			myfaq = navigation(href = ":trv/faq.html",img = "faq",text = "FAQ")
		if self.has_attr("nositemap"):
			mysitemap = xsc.Null()
		else:
			mysitemap = navigation(href = ":sitemap.html",img = "sitemap",text = "Sitemap")
		if self.has_attr("nosearch"):
			mysearch = xsc.Null()
		else:
			mysearch = navigation(href = ":search.html",img = "search",text = "Suchen")

		b.append(
			specials.plaintable(
				html.tr(
					html.td(specials.pixel(height="66"),colspan="2") # eigentlich 70, aber der Netscape läßt trotz margintop="0" zuviel Platz
				)+
				html.tr(
					html.td(
						specials.plaintable(
							html.tr(html.td(specials.pixel(height = "20"),colspan = "4"))+
							html.tr(html.td(html.img(src = ":images/bnbt-logo.gif",alt = "Bürgernetz-Logo"),colspan = "4",align = "center",valign = "middle"))+
							html.tr(html.td(specials.pixel(height = "40"),colspan = "4"))+
							mylinks+
							fileinfo()+
							html.tr(html.td(html.img(src = ":images/ecke_links.gif",alt = ""),colspan = "4",align = "right")),
							Class = "links",bgcolor = "#333366"
						),
						valign = "top"
					)+
					html.td(
						specials.plaintable(
							html.tr(
								html.td(
									specials.plaintable(
										html.tr(
											myhome+myfaq+mysitemap+mysearch+
											html.td(html.img(src = ":images/ecke_biglinks.gif",alt = ""))
										)
									),
									align = "left",colspan = "3"
								)
							)+
							html.tr(
								html.td(html.img(src = ":images/ecke_content.gif",alt = ""),colspan = "3",valign = "top",align = "left",bgcolor = "#ffffff")
							)+
							html.tr(
								html.td(specials.pixel(width = "30"),bgcolor = "#ffffff")+
								html.td(mycontent,bgcolor = "#ffffff",valign = "top")+
								html.td(specials.pixel(width = "30"),bgcolor = "#ffffff")
							)+
							html.tr(html.td(specials.pixel(height = "30"),colspan = "3",bgcolor = "#ffffff"))
						),
						align = "left",valign = "top"
					)
				)
			)
		)

		e = xsc.DocType('HTML PUBLIC "-//W3C//DTD HTML 4.0 transitional//EN"')+html.html(h+b)

		return e.asHTML()
xsc.registerElement(page)

class blankpage(xsc.Element):
	empty = 0
	attr_handlers = { "title" : xsc.TextAttr , "notinsitemap" : xsc.TextAttr }

	def asHTML(self):
		e = html.html(
			html.head(
				html.title(self["title"])+
				html.script(type="text/javascript",language="Javascript",src=":javascripts/main.js")+
				html.link(rel="made",href="mailto:html@bnbt.de")
			)+
			specials.plainbody(self.content.clone(),bgcolor="#ffffff")
		)

		return e.asHTML()
xsc.registerElement(blankpage)

class links(xsc.Element):
	empty = 0
xsc.registerElement(links)

class scripts(xsc.Element):
	empty = 0
xsc.registerElement(scripts)

class indent(xsc.Element):
	empty = 1

	def asHTML(self):
		e = xsc.Frag([specials.nbsp()]*4)

		return e.asHTML()
xsc.registerElement(indent)

class _(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text(" - ")
xsc.registerElement(_)

class pfeil(html.img):
	empty = 1
	attr_handlers = xsc.appendDict(html.img.attr_handlers,{ "rel" : xsc.TextAttr })

	def asHTML(self):
		alts = { "home" : "-> Startseite" , "child" : "-> Untergeordnete Seite" , "parent" : "-> Übergeordnete Seite" , "next" : "-> Nächste Seite" , "previous" : "-> Vorherige Seite" , "info" : "-> Seiteninformation" , "download" : "-> Download" }
		e = html.img(self.content.clone(),border = "0")
		rel = None
		for attr in self.attrs.keys():
			if attr == "rel":
				rel = self["rel"]
			else:
				e[attr] = self[attr]
		if rel is not None:
			e["src"] = [":images/links/" , rel , ".gif" ]
			e["alt"] = alts[str(rel)]

		return e.asHTML()
xsc.registerElement(pfeil)

class capbnv(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Bnv").asHTML()
xsc.registerElement(capbnv)

class capxml(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Xml").asHTML()
xsc.registerElement(capxml)

class capcss(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Css").asHTML()
xsc.registerElement(capcss)

class capgeo(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Geo").asHTML()
xsc.registerElement(capgeo)

class capcisco(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Cisco").asHTML()
xsc.registerElement(capcisco)

class capsun(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Sun").asHTML()
xsc.registerElement(capsun)

class capcgi(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Cgi").asHTML()
xsc.registerElement(capcgi)

class capphp(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Php").asHTML()
xsc.registerElement(capphp)

class capbin(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Bin").asHTML()
xsc.registerElement(capbin)

class capwww(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("www").asHTML()
xsc.registerElement(capwww)

class capknf(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Knf").asHTML()
xsc.registerElement(capknf)

class caphtml(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Html").asHTML()
xsc.registerElement(caphtml)

class capowinet(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("OwiNet").asHTML()
xsc.registerElement(capowinet)

class capmcs(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Mcs").asHTML()
xsc.registerElement(capmcs)

class capcfs(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Cfs").asHTML()
xsc.registerElement(capcfs)

class capdaa(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Daa").asHTML()
xsc.registerElement(capdaa)

class capvhs(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Vhs").asHTML()
xsc.registerElement(capvhs)

class capakzent(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Akzent").asHTML()
xsc.registerElement(capakzent)

class capcvjm(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Cvjm").asHTML()
xsc.registerElement(capcvjm)

class capccb(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Ccb").asHTML()
xsc.registerElement(capccb)

class capppp(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("ppp").asHTML()
xsc.registerElement(capppp)

class capmtla(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Mtla").asHTML()
xsc.registerElement(capmtla)

class capbfs(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Bfs").asHTML()
xsc.registerElement(capbfs)

class capihk(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Ihk").asHTML()
xsc.registerElement(capihk)

class capdag(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Dag").asHTML()
xsc.registerElement(capdag)

class capvwa(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Vwa").asHTML()
xsc.registerElement(capvwa)

class capbfz(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Bfz").asHTML()
xsc.registerElement(capbfz)

class capedv(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("edv").asHTML()
xsc.registerElement(capedv)

class capbitoek(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Bitök").asHTML()
xsc.registerElement(capbitoek)

class capdfn(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Dfn").asHTML()
xsc.registerElement(capdfn)

class capizb(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Izb").asHTML()
xsc.registerElement(capizb)

class capdat(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Dat").asHTML()
xsc.registerElement(capdat)

class capdns(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Dns").asHTML()
xsc.registerElement(capdns)

class capascend(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Ascend").asHTML()
xsc.registerElement(capascend)

class capmax(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Max").asHTML()
xsc.registerElement(capmax)

class capisdn(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Isdn").asHTML()
xsc.registerElement(capisdn)

class cappdf(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Pdf").asHTML()
xsc.registerElement(cappdf)

class capiso(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Iso").asHTML()
xsc.registerElement(capiso)

class capurl(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Url").asHTML()
xsc.registerElement(capurl)

class caphttp(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Http").asHTML()
xsc.registerElement(caphttp)

class capsmtp(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Smtp").asHTML()
xsc.registerElement(capsmtp)

class capftp(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("ftp").asHTML()
xsc.registerElement(capftp)

class cappop3(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Pop3").asHTML()
xsc.registerElement(cappop3)

class capcvs(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Cvs").asHTML()
xsc.registerElement(capcvs)

class capfaq(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Faq").asHTML()
xsc.registerElement(capfaq)

class capgnu(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Gnu").asHTML()
xsc.registerElement(capgnu)

class caphsc(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Hsc").asHTML()
xsc.registerElement(caphsc)

class capunix(xsc.Element):
	empty = 1

	def asHTML(self):
		return specials.cap("Unix").asHTML()
xsc.registerElement(capunix)

class par(html.div):
	empty = 0
	attr_handlers = xsc.appendDict(html.div.attr_handlers,{ "noindent" : xsc.TextAttr })

	def asHTML(self):
		e = html.div(self.content.clone())
		indent = 1
		for attr in self.attrs.keys():
			if attr == "noindent":
				indent = None
			else:
				e[attr] = self[attr]
		if indent is not None:
			e["class"] = "indent"
		return e.asHTML()
xsc.registerElement(par)

class blob(xsc.Element):
	empty = 1

	def asHTML(self):
		return (specials.nbsp() + "- ").asHTML()
xsc.registerElement(blob)

class schulen(html.dl):
	empty = 0

	def asHTML(self):
		e = html.dl(self.content,self.attrs)
		return e.asHTML()
xsc.registerElement(schulen)

class schule(xsc.Element):
	empty = 0
	attr_handlers = { "privat" : xsc.TextAttr , "art" : xsc.TextAttr , "anschrift" : xsc.TextAttr , "telefon" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		t = xsc.Frag()
		if self.has_attr("url"):
			t = t + html.a(html.b(self.content.asHTML()),href=self["url"])
		else:
			t = t + html.b(self.content.asHTML())
		if self.has_attr("privat"):
			t = t + " (Privat)"
		d = xsc.Frag()
		if self.has_attr("art"):
			d = d + [ self["art"] , "; " ]
		if self.has_attr("anschrift"):
			d = d + [ self["anschrift"] , "; " ]
		if self.has_attr("telefon"):
			d = d + [ "Tel.: " , self["telefon"] ]
		d = html.div(Class="schule-text")
		return html.dt(t) + html.dd(html.div(d))
xsc.registerElement(schule)

class fileinfo(xsc.Element):
	empty = 1

	def asHTML(self):
		e = html.tr(
			html.td(indent(),rowspan = "3") +
			html.td(html.div(pfeil(rel = "info") + specials.nbsp(),Class = "lnk-title"),nowrap = None,Class = "links") +
			html.td(html.div("Letzte Änderung",Class = "lnk-title"),nowrap = None,Class = "links") +
			html.td(indent())
		)+html.tr(
			html.td(specials.pixel()) +
			html.td(specials.pixel(),colspan = "2",bgcolor = "#ffffff")
		)+html.tr(
			html.td(specials.pixel())+
			html.td(html.div("Now" + html.br() + html.a(href = "mailto:webmaster@bnbt.de"),Class = "info-text"),nowrap = None,Class = "links")+
			html.td(specials.pixel())
		)+html.tr(
			html.td(specials.pixel(),colspan = "4")
		)

		return e.asHTML()
xsc.registerElement(fileinfo)

class navigation(xsc.Element):
	empty = 1
	attr_handlers = { "href" : xsc.URLAttr , "img" : xsc.TextAttr , "text" : xsc.TextAttr }

	def asHTML(self):
		e = html.td(
			specials.pixel(width = "30"),
			Class="links",
			bgcolor="#333366"
		)
		e = e + html.td(
			html.span(
				specials.nbsp()+
				html.br()+
				hrf(
					html.img(src = ":images/biglinks/" + self["img"] + ".gif",border = "0",alt = "")+
					html.br()+
					self["text"],
					href = self["href"]
				),
				Class="biglink"
			),
			Class="links",
			bgcolor="#333366",
			valign="middle",
			align="center"
		)

		return e.asHTML()
xsc.registerElement(navigation)

class content(xsc.Element):
	empty = 0
xsc.registerElement(content)

class bytes(xsc.Element):
	attr_handlers = { "file" : xsc.URLAttr }
	empty = 1
xsc.registerElement(bytes)

class hrf(xsc.Element):
	attr_handlers = { "rel" : xsc.TextAttr , "href" : xsc.URLAttr , "class" : xsc.TextAttr , "target" : xsc.TextAttr }
	empty = 0

	def asHTML(self):
		e = html.a(self.content,self.attrs)

		return e.asHTML()
xsc.registerElement(hrf)

class lnk(xsc.Element):
	attr_handlers = { "rel" : xsc.TextAttr , "href" : xsc.URLAttr , "text" : xsc.TextAttr }
	empty = 0

	def asHTML(self):
		if self.has_attr("rel"):
			rel = self["rel"]
		else:
			rel = "child"

		e = html.tr(
			html.td(indent(),rowspan="3")+
			html.td(
				html.div(
					hrf(
						pfeil(rel = rel),
						href = self["href"],
						rel  = rel
					)+
					specials.nbsp(),
				),
				Class = "links"
			)+
			html.td(
				html.div(
					hrf(
						self["text"],
						href = self["href"],
						rel = rel
					)
				),
				Class = "links"
			)+
			html.td(indent(),Class = "links",nowrap = None)
		)
		e = e + html.tr(
			html.td(
				specials.pixel()
			)+
			html.td(
				specials.pixel(),
				colspan = "2",
				bgcolor = "#ffffff"
			)
		)

		if len(self):
			e.append(
				html.tr(
					html.td(
						specials.pixel()
					)+
					html.td(
						html.div(
							self.content.clone(),
							Class = "lnk-text"
						),
						Class = "links"
					)+
					html.td(
						specials.pixel()
					)
				)+
				html.tr(
					html.td(
						specials.pixel(height="20"),
						colspan = "4"
					)
				)
			)
		else:
			e.append(
				html.tr(
					html.td(
						specials.pixel(height="20"),
						colspan = "3"
					)
				)
			)

		return e.asHTML()
xsc.registerElement(lnk)

class vorstand(xsc.Element):
	attr_handlers = { "name" : xsc.TextAttr , "posten" : xsc.TextAttr , "email" : xsc.TextAttr , "homepage" : xsc.TextAttr }
	empty = 1
xsc.registerElement(vorstand)

class firmen(xsc.Element):
	empty = 0
xsc.registerElement(firmen)

class firma(xsc.Element):
	attr_handlers = { "anschrift" : xsc.TextAttr , "telefon" : xsc.TextAttr ,  "url" : xsc.URLAttr }
	empty = 0
xsc.registerElement(firma)

class kirchen(xsc.Element):
	empty = 0
xsc.registerElement(kirchen)

class kirche(xsc.Element):
	attr_handlers = { "ansprech" : xsc.TextAttr , "strasse" : xsc.TextAttr ,  "ort" : xsc.URLAttr , "telefon" : xsc.TextAttr , "url" : xsc.URLAttr , "dekanat" : xsc.TextAttr }
	empty = 0
xsc.registerElement(kirche)

class above(xsc.Element):
	atts_handlers = { "rel" : xsc.TextAttr , "href" : xsc.TextAttr , "class" : xsc.TextAttr }
	empty = 0
xsc.registerElement(above)

class shell(xsc.Element):
	empty = 0
xsc.registerElement(shell)

class faq(xsc.Element):
	attr_handlers = { "frage" : xsc.TextAttr }
	empty = 0
xsc.registerElement(faq)

class engines(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.dl(self.content.clone())
		return e.asHTML()
xsc.registerElement(engines)

class engine(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.Frag(
			html.dt(html.b(self["name"]) + " (" + hrf(self["url"],href=self["url"]) + ")")+
			html.dd(html.div(self.content.clone(),Class="engine-text"))
		)

		return e.asHTML()

xsc.registerElement(engine)

class bnvereine(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.dl(self.content.clone())
		return e.asHTML()
xsc.registerElement(bnvereine)

class bnverein(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.Frag(
			html.dt(html.b(self["name"]) + " (" + hrf(self["url"],href=self["url"]) + ")")+
			html.dd(html.div(self.content.clone(),Class="bnverein-text"))
		)

		return e.asHTML()

xsc.registerElement(bnverein)

class fahrplansite(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.Frag(
			html.dt(html.b(self["name"]) + " (" + hrf(self["url"],href=self["url"]) + ")")+
			html.dd(html.div(self.content.clone(),Class="fahrplan-text"))
		)

		return e.asHTML()
xsc.registerElement(fahrplansite)

class fahrplansites(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.dl(self.content.clone())

		return e.asHTML()
xsc.registerElement(fahrplansites)

class fahrplan(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		halts = self.elements(element = haltestelle)
		flipflop = "even"
		for halt in halts:
			halt["class"] = flipflop
			if flipflop == "even":
				flipflop = "odd"
			else:
				flipflop = "even"
		e = specials.plaintable(halts,Class="fahrplan",cellpadding="2",cellspacing="1")

		return e.asHTML()
xsc.registerElement(fahrplan)

class halt(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.td(self.content.clone(),align="right",Class="halt")

		return e.asHTML()
xsc.registerElement(halt)


class keinhalt(xsc.Element):
	empty = 1

	def asHTML(self):
		e = html.td()

		return e.asHTML()
xsc.registerElement(keinhalt)

class haltestelle(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "an" : xsc.TextAttr , "class" : xsc.TextAttr }

	def asHTML(self):
		if self.has_attr("an"):
			anab = td("an")
		else:
			anab = td("ab")
		e = html.tr(
			html.th(self["name"],Class="left")+
			anab+
			self.content.clone()+
			anab+
			html.th(self["name"],Class="right")
		)
		if self.has_attr("class"):
			e["class"] = self["class"]

		return e.asHTML()
xsc.registerElement(haltestelle)

class downloadsites(xsc.Element):
	empty = 0
xsc.registerElement(downloadsites)

class downloadsite(xsc.Element):
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }
	empty = 0
xsc.registerElement(downloadsite)

class newstickers(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.dl(self.content.clone())

		return e.asHTML()
xsc.registerElement(newstickers)

class newsticker(xsc.Element):
	empty = 0
	attr_handlers = { "name" : xsc.TextAttr , "url" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.Frag(
			html.dt(html.b(self["name"]) + " (" + hrf(self["url"],href=self["url"]) + ")")+
			html.dd(html.div(self.content.clone(),Class="newsticker-text"))
		)

		return e.asHTML()

xsc.registerElement(newsticker)

class kleinanzeige(xsc.Element):
	attr_handlers = { "bezeichnung" : xsc.TextAttr , "preis" : xsc.TextAttr , "tel" : xsc.TextAttr , "email" : xsc.TextAttr , "handy" : xsc.TextAttr , "fax" : xsc.TextAttr }
	empty = 0
xsc.registerElement(kleinanzeige)

class kleinanzeige_handy(xsc.Element):
	empty = 0
xsc.registerElement(kleinanzeige_handy)


class kleinanzeige_fax(xsc.Element):
	empty = 0
xsc.registerElement(kleinanzeige_fax)

class newsitems(xsc.Element):
	empty = 0

	def asHTML(self):
		e = specials.plaintable(self.content.clone(),Class="newsitems")

		return e.asHTML()
xsc.registerElement(newsitems)

class newsitem(xsc.Element):
	attr_handlers = { "datum" : xsc.TextAttr , "href" : xsc.TextAttr }
	empty = 0

	def asHTML(self):
		e = html.tr(
			html.td(html.b(self["datum"]+specials.nbsp()),valign="top")+
			html.td(html.a(self.content.clone(),href=":aktuelles/"+self["href"]+".html"))
		,Class="newsitem")

		return e.asHTML()
xsc.registerElement(newsitem)

class pagenewsitem(xsc.Element):
	empty = 0
	attr_handlers = { "datum" : xsc.TextAttr }

	def asHTML(self):
		e = page(links()+content(self.content.clone()),title="Bürgernetz Bayreuth - Aktuelles - "+self["datum"],keywords="Bürgernetz, Bayreuth, Aktuelles")

		return e.asHTML()
xsc.registerElement(pagenewsitem)

class zonk(xsc.Element):
	empty = 0

	def asHTML(self):
		return html.div(self.content.asHTML(),Class="zonk")
xsc.registerElement(zonk)

class buergerfestbild(xsc.Element):
	empty = 0
	attr_handlers = { "src" : xsc.TextAttr }

	def asHTML(self):
		e = specials.plaintable(
			html.tr(
				html.td(
					html.a(
						html.img(src=":trv/buergerfest1999/images/pic" + self["src"] + "-thumb.jpg",border="0"),
						href=":trv/buergerfest1999/images/pic" + self["src"] + ".jpg"
					)
				)
			),cellpadding="1",bgcolor="#000"
		)
		return e.asHTML()
xsc.registerElement(buergerfestbild)

class buskarte(xsc.Element):
	empty = 1

	def asHTML(self):
		e1 = specials.plaintable(style = "border: 1px black solid;")

		for x in range(7):
			e2 = html.tr()
			for y in range(7):
				e3 = html.td(
					html.img(
						name = "map_" + str(x) + "_" + str(y),
						src = "images/maps/map_" + str(x) + "_" + str(y) + ".png"
					)
				)
				e2.append(e3)
			e1.append(e2)

		return e1.asHTML()
xsc.registerElement(buskarte)

class busnav(xsc.Element):
	empty = 1
	attr_handlers = { "dir" : xsc.TextAttr }

	def asHTML(self):
		e = html.a(
			html.img(
				src = ":lokal/verkehr/images/navigation/" + self["dir"] + ".gif",
				border = "0"
			),
			href = "javascript:" + self["dir"] + "()"
		)
		return e.asHTML()
xsc.registerElement(busnav)

if __name__ == "__main__":
	xsc.make()

