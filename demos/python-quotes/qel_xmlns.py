# -*- coding: iso-8859-1 -*-


from ll.xist import xsc, sims
from ll.xist.ns import html, meta, chars


class title(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.h1(self.content)

		return e.convert(converter)


class editor(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.h2(self.content)

		return e.convert(converter)


class description(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.div(self.content, class_=u"description")

		return e.convert(converter)


class note(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.div(self.content, class_=u"note")

		return e.convert(converter)


class foreign(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.em(self.content)

		return e.convert(converter)


class author(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = self.content

		return e.convert(converter)


class source(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = self.content

		return e.convert(converter)


class quotation(xsc.Element):
	model = sims.Elements(author, source, note)

	class Attrs(xsc.Element.Attrs):
		class date(xsc.TextAttr): pass
		class id(xsc.IDAttr): pass

	def convert(self, converter):
		content = xsc.Frag()
		authors = xsc.Frag()
		sources = xsc.Frag()
		for child in self:
			if isinstance(child, author):
				authors.append(child)
			elif isinstance(child, source):
				sources.append(child)
			else:
				content.append(child)
		if authors:
			if sources:
				footer = html.div(authors, u" ", chars.mdash(), u" ", sources, class_=u"source")
			else:
				footer = html.div(authors, class_=u"source")
		else:
			if sources:
				footer = html.div(sources, class_=u"source")
			else:
				footer = None
		e = html.div(content, footer, class_=u"quotation")

		return e.convert(converter)


class quotations(xsc.Element):
	model = sims.Elements(title, editor, description, quotation)

	def convert(self, converter):
		e = xsc.Frag(
			html.DocTypeXHTML10transitional(), u"\n",
			html.html(
				html.head(
					meta.contenttype(),
					html.title(self[title][0].content),
					meta.stylesheet(href=u"root:python-quotes.css")
				),
				html.body(
					self[title],
					self[editor],
					self[description],
					self[quotation]
				)
			)
		)

		return e.convert(converter)


class p(xsc.Element):
	def convert(self, converter):
		e = html.p(self.content)

		return e.convert(converter)


class cite(xsc.Element):
	def convert(self, converter):
		e = html.cite(self.content)

		return e.convert(converter)


class em(xsc.Element):
	def convert(self, converter):
		e = html.em(self.content)

		return e.convert(converter)


class pre(xsc.Element):
	def convert(self, converter):
		e = html.pre(self.content)

		return e.convert(converter)


class code(xsc.Element):
	def convert(self, converter):
		e = html.code(self.content)

		return e.convert(converter)


class __ns__(xsc.Namespace):
	xmlname = "quotations"
	xmlurl = "http://www.amk.ca/qel/"
__ns__.makemod(vars())
