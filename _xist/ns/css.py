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
<doc:par>An &xist; module that contains elements that can be used to generate
&css;2 files.</doc:par>
<doc:par>For further info about &css;2 see 
<a href="http://www.w3.org/TR/REC-CSS2">http://www.w3.org/TR/REC-CSS2</a>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc, helpers

class css(xsc.Element):
	"""
	The root element
	"""
	empty = 0

	def publish(self, publisher):
		publisher.pushTextFilter(helpers.escapeCSS)
		# publish the imports first
		imports = self.find(type=atimport)
		for i in imports:
			publisher.publish(u"\n")
			i.publish(publisher)
		content = self.find(type=(rule, atmedia), subtype=1)
		for child in content:
			publisher.publish(u"\n")
			child.publish(publisher)
		publisher.popTextFilter()

class atimport(xsc.Element):
	"""
	<doc:par>The <class>atimport</class> rule allows users to import style rules from other style sheets.
	The content is the URI of the style sheet to include.</doc:par>
	<doc:par>So that user agents can avoid retrieving resources for unsupported media types,
	authors may specify media-dependent <class>atimport</class> rules. These conditional imports
	specify comma-separated media types as the attribute <lit>media</lit>. In the absence of
	any media types, the import is unconditional. Specifying <lit>all</lit> for <lit>media</lit>
	has the same effect.</doc:par>
	"""
	empty = 0
	attrHandlers = {"media": xsc.TextAttr}

	def publish(self, publisher):
		publisher.publish(u'@import url("')
		self.content.publish(publisher)
		publisher.publish(u'")')
		if self.hasAttr("media"):
			publisher.publish(u" " + unicode(self["media"]))
		publisher.publish(u";")

class atmedia(xsc.Element):
	"""
	<doc:par>An <class>atmedia</class> rule specifies the target media types
	(separated by commas in the attribute <lit>media</lit>) of a set of rules (in the content).
	The <class>atmedia</class> element allows style sheet rules for various media in the same 
	style sheet.</doc:par>
	<doc:par>Possible media types are:</doc:par>
	<doc:ulist>
	<doc:item><lit>all</lit>: Suitable for all devices.</doc:item>
	<doc:item><lit>aural</lit>: Intended for speech synthesizers.</doc:item>
	<doc:item><lit>braille</lit>: Intended for braille tactile feedback devices.</doc:item>
	<doc:item><lit>embossed</lit>: Intended for paged braille printers.</doc:item>
	<doc:item><lit>handheld</lit>: Intended for handheld devices (typically small screen, monochrome, limited bandwidth).</doc:item>
	<doc:item><lit>print</lit>: Intended for paged, opaque material and for documents viewed on screen
	in print preview mode.</doc:item>
	<doc:item><lit>projection</lit>: Intended for projected presentations, for example projectors
	or print to transparencies.</doc:item>
	<doc:item><lit>screen</lit>: Intended primarily for color computer screens.</doc:item>
	<doc:item><lit>tty</lit>: Intended for media using a fixed-pitch character grid, such as teletypes,
	terminals, or portable devices with limited display capabilities. Authors should not use pixel units
	with the <lit>tty</lit> media type.</doc:item>
	<doc:item><lit>tv</lit>: Intended for television-type devices (low resolution, color, limited-scrollability screens, sound available).</doc:item>
	</doc:ulist>
	<doc:par>Media type names are case-insensitive.</doc:par>
	"""
	empty = 0
	attrHandlers = {"media": xsc.TextAttr}

	def publish(self, publisher):
		publisher.publish(u"@media ")
		publisher.publish(unicode(self["media"]))
		publisher.publish(u"\n{\n")
		self.content.publish(publisher)
		publisher.publish(u"\n}")

class atcharset(xsc.Element):
	"""
	<doc:par>The character set of the stylesheet. Will be set automatically
	on publishing, so this element is empty. Simply include it at the start
	of the style sheet.</doc:par>
	"""
	empty = 1
	
	def publish(self, publisher):
		publisher.publish(u'@charset "')
		publisher.publish(unicode(publisher.encoding))
		publisher.publish(u'";')

class rule(xsc.Element):
	"""
	<doc:par>One CSS rule (with potentially multiple <pyref class="sel">selectors</pyref>).</doc:par>
	"""
	empty = 0

	def publish(self, publisher):
		sels = self.find(type=sel)
		props = self.find(type=prop, subtype=1)

		for i in xrange(len(sels)):
			if i != 0:
				publisher.publish(u", ")
			sels[i].publish(publisher)
		publisher.publish(u" { ")
		for i in xrange(len(props)):
			if i != 0:
				publisher.publish(u" ")
			props[i].publish(publisher)
		publisher.publish(u" }")

class sel(xsc.Element):
	"""
	<doc:par>A CSS selector.</doc:par>
	"""
	empty = 0

	def publish(self, publisher):
		self.content.publish(publisher)

class prop(xsc.Element):
	"""
	<doc:par>A &css; property. This is the base class for all
	the properties defined in &css;2.</doc:par>
	"""
	empty = 0
	attrHandlers = {"important": xsc.BoolAttr}

	def publish(self, publisher):
		publisher.publish(u"%s: " % self.name())
		self.content.publish(publisher)
		if self.hasAttr("important"):
			publisher.publish(u" !important")
		publisher.publish(u";")

class margin_top(prop):
	"""
	<doc:par>Set the top margin of a box. Allowed values are a length or the value <lit>inherit</lit>.</doc:par>
	"""
	name = "margin-top"

class margin_right(prop):
	"""
	<doc:par>Set the right margin of a box. Allowed values are a length or the value <lit>inherit</lit>.</doc:par>
	"""
	name = "margin-right"

class margin_bottom(prop):
	"""
	<doc:par>Set the bottom margin of a box. Allowed values are a length or the value <lit>inherit</lit>.</doc:par>
	"""
	name = "margin-bottom"

class margin_left(prop):
	"""
	<doc:par>Set the left margin of a box. Allowed values are a length or the value <lit>inherit</lit>.</doc:par>
	"""
	name = "margin-left"

class margin(prop):
	"""
	<doc:par>The <class>margin</class> property is a shorthand property for setting
	<pyref class="margin_top"><class>margin_top</class></pyref>,
	<pyref class="margin_right"><class>margin_right</class></pyref>,
	<pyref class="margin_bottom"><class>margin_bottom</class></pyref>
	and <pyref class="margin_left"><class>margin_left</class></pyref>
	at the same place in the style sheet.</doc:par>

	<doc:par>If there is only one value, it applies to all sides. If there are two values,
	the top and bottom margins are set to the first value and the right and left margins
	are set to the second. If there are three values, the top is set to the first value,
	the left and right are set to the second, and the bottom is set to the third.
	If there are four values, they apply to the top, right, bottom, and left, respectively.</doc:par> 
	"""

class padding_top(prop):
	"""
	<doc:par>Set the top padding of a box. Allowed values are a length or the value <lit>inherit</lit>.
	A percentage value is calculated with respect to the width of the generated box.</doc:par>"""
	name = "padding-top"

class padding_right(prop):
	"""
	<doc:par>Set the right padding of a box. Allowed values are a length or the value <lit>inherit</lit>.
	A percentage value is calculated with respect to the width of the generated box.</doc:par>
	"""
	name = "padding-right"

class padding_bottom(prop):
	"""
	<doc:par>Set the bottom padding of a box. Allowed values are a length or the value <lit>inherit</lit>.
	A percentage value is calculated with respect to the width of the generated box.</doc:par>
	"""
	name = "padding-bottom"

class padding_left(prop):
	"""
	<doc:par>Set the left padding of a box. Allowed values are a length or the value <lit>inherit</lit>.
	A percentage value is calculated with respect to the width of the generated box.</doc:par>
	"""
	name = "padding-left"

class padding(prop):
	"""
	<doc:par>The <class>padding</class> property is a shorthand property for setting
	<pyref class="padding_top"><class>padding_top</class></pyref>,
	<pyref class="padding_right"><class>padding_right</class></pyref>,
	<pyref class="padding_bottom"><class>padding_bottom</class></pyref>
	and <pyref class="padding_left"><class>padding_left</class></pyref>
	at the same place in the style sheet.</doc:par>

	<doc:par>If there is only one value, it applies to all sides. If there are two values,
	the top and bottom paddings are set to the first value and the right and left paddings
	are set to the second. If there are three values, the top is set to the first value,
	the left and right are set to the second, and the bottom is set to the third.
	If there are four values, they apply to the top, right, bottom, and left, respectively.</doc:par>
	"""

class border_top_width(prop):
	"""
	<doc:par>Set the top border width of a box. Allowed values are a length, <lit>thin</lit>,
	<lit>medium</lit>, <lit>thick</lit> and <lit>inherit</lit>.</doc:par>
	"""
	name = "border-top-width"

class border_right_width(prop):
	"""
	<doc:par>Set the right border width of a box. Allowed values are a length, <lit>thin</lit>,
	<lit>medium</lit>, <lit>thick</lit> and <lit>inherit</lit>.</doc:par>
	"""
	name = "border-right-width"

class border_bottom_width(prop):
	"""
	<doc:par>Set the bottom border width of a box. Allowed values are a length, <lit>thin</lit>,
	<lit>medium</lit>, <lit>thick</lit> and <lit>inherit</lit>.</doc:par>
	"""
	name = "border-bottom-width"

class border_left_width(prop):
	"""
	<doc:par>Set the left border width of a box. Allowed values are a length, <lit>thin</lit>,
	<lit>medium</lit>, <lit>thick</lit> and <lit>inherit</lit>.</doc:par>
	"""
	name = "border-left-width"

class border_width(prop):
	"""
	<doc:par>The <class>border_width</class> property is a shorthand property for setting
	<pyref class="border_top_width"><class>border_top_width</class></pyref>,
	<pyref class="border_right_width"><class>border_right_width</class></pyref>,
	<pyref class="border_bottom_width"><class>border_bottom_width</class></pyref>,
	and <pyref class="border_left_width"><class>border_left_width</class></pyref> at the same place
	in the style sheet.</doc:par>

	<doc:par>If there is only one value, it applies to all sides. If there are two values,
	the top and bottom borders are set to the first value and the right and left are set to the second.
	If there are three values, the top is set to the first value, the left and right are set to the second,
	and the bottom is set to the third. If there are four values, they apply to the top, right,
	bottom, and left, respectively.</doc:par> 
	"""
	name = "border-width"

class border_top_color(prop):
	"""
	<doc:par>Set the top border color of a box. Allowed values are a color or <lit>transparent</lit>.</doc:par>
	"""
	name = "border-top-color"

class border_right_color(prop):
	"""
	<doc:par>Set the right border color of a box. Allowed values are a color or <lit>transparent</lit>.</doc:par>
	"""
	name = "border-right-color"

class border_bottom_color(prop):
	"""
	<doc:par>Set the bottom border color of a box. Allowed values are a color or <lit>transparent</lit>.</doc:par>
	"""
	name = "border-bottom-color"

class border_left_color(prop):
	"""
	<doc:par>Set the left border color of a box. Allowed values are a color or <lit>transparent</lit>.</doc:par>
	"""
	name = "border-left-color"

class border_color(prop):
	"""
	<doc:par>The <class>border_color</class> property is a shorthand property for setting
	<pyref class="border_top_color"><class>border_top_color</class></pyref>,
	<pyref class="border_right_color"><class>border_right_color</class></pyref>,
	<pyref class="border_bottom_color"><class>border_bottom_color</class></pyref>,
	and <pyref class="border_left_color"><class>border_left_color</class></pyref> at the same place
	in the style sheet.</doc:par>

	<doc:par>The <class>border_color</class> property can have from one to four values,
	and the values are set on the different sides as for
	<pyref class="border_width"><class>border_width</class></pyref>.</doc:par> 

	<doc:par>If an element's border color is not specified with a border property, 
	user agents must use the value of the element's <pyref class="color"><class>color</class></pyref>
	property as the computed value for the border color.</doc:par>
	"""
	name = "border-color"

class border_top_style(prop):
	"""
	<doc:par>The <class>border_top_style</class> properties specify the line style of a 
	box's top border. Allow values are:</doc:par>

	<doc:ulist>
	<doc:item><lit>none</lit>: No border. This value forces the computed value of 
	<pyref class="border_top_width"><class>border_top_width</class></pyref> to be <lit>0</lit>.</doc:item> 
	<doc:item><lit>hidden</lit>: Same as <lit>none</lit>, except in terms of border conflict resolution 
	for table elements.</doc:item>
	<doc:item><lit>dotted</lit>: The border is a series of dots.</doc:item> 
	<doc:item><lit>dashed</lit>: The border is a series of short line segments.</doc:item>
	<doc:item><lit>solid</lit>: The border is a single line segment.</doc:item> 
	<doc:item><lit>double</lit>: The border is two solid lines. The sum of the two lines and the 
	space between them equals the value of <pyref class="border_top_width"><class>border_top_width</class></pyref>.</doc:item> 
	<doc:item><lit>groove</lit>: The border looks as though it were carved into the canvas.</doc:item>
	<doc:item><lit>ridge</lit>: The opposite of <lit>groove</lit>: the border looks as though it were 
	coming out of the canvas.</doc:item>
	<doc:item><lit>inset</lit>: The border makes the entire box look as though it were embedded 
	in the canvas.</doc:item>
	<doc:item><lit>outset</lit>: The opposite of <lit>inset</lit>: the border makes the entire box 
	look as though it were coming out of the canvas.</doc:item>
	</doc:ulist>

	<doc:par>All borders are drawn on top of the box's background. The color of borders drawn for values 
	of <lit>groove</lit>, <lit>ridge</lit>, <lit>inset</lit>, and <lit>outset</lit> depends on the 
	element's <pyref class="color"><class>color</class></pyref> property. 
	"""
	name = "border-top-style"

class border_right_style(prop):
	"""
	<doc:par>The <class>border_right_style</class> properties specify the line style of a 
	box's right border. For allowed values refer to
	<pyref class="border_top_style"><class>border_top_style</class></pyref>.</doc:par>
	"""
	name = "border-right-style"

class border_bottom_style(prop):
	"""
	<doc:par>The <class>border_bottom_style</class> properties specify the line style of a 
	box's bottom border. For allowed values refer to
	<pyref class="border_bottom_style"><class>border_bottom_style</class></pyref>.</doc:par>
	"""
	name = "border-bottom-style"

class border_left_style(prop):
	"""
	<doc:par>The <class>border_left_style</class> properties specify the line style of a 
	box's left border. For allowed values refer to
	<pyref class="border_left_style"><class>border_left_style</class></pyref>.</doc:par>
	"""
	name = "border-left-style"

class border_style(prop):
	"""
	<doc:par>The <class>border_style</class> property sets the style of the four borders.
	It can have from one to four values, and the values are set on the different sides as for
	<pyref class="border_width"><class>border-width</class></pyref>.</doc:par>
	"""
	name = "border-style"

class border_top(prop):
	"""
	<doc:par>This is a shorthand property for setting the width, style, and color
	of the top border of a box.</doc:par>
	"""
	name = "border-top"

class border_right(prop):
	"""
	<doc:par>This is a shorthand property for setting the width, style, and color
	of the right border of a box.</doc:par>
	"""
	name = "border-right"

class border_bottom(prop):
	"""
	<doc:par>This is a shorthand property for setting the width, style, and color
	of the bottom border of a box.</doc:par>
	"""
	name = "border-bottom"

class border_left(prop):
	"""
	<doc:par>This is a shorthand property for setting the width, style, and color
	of the left border of a box.</doc:par>
	"""
	name = "border-left"

class border(prop):
	"""
	<doc:par>The <class>border</class> property is a shorthand property for setting the same width,
	color, and style for all four borders of a box. Unlike the shorthand
	<pyref class="margin"><class>margin</class></pyref> and <pyref class="padding"><class>padding</class></pyref>
	properties, the <class>border</class> property cannot set different values on the four borders.
	To do so, one or more of the other border properties must be used.</doc:par>
	"""

class display(prop):
	"""
	<doc:par>Sets the display type of a box. The values of this property
	have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>block</lit>: This value causes an element to generate a principal block box.</doc:item>
	<doc:item><lit>inline</lit>: This value causes an element to generate one or more inline boxes.</doc:item>
	<doc:item><lit>list-item</lit>: This value causes an element (e.g., <pyref module="xist.ns.html" class="li"><class>li</class></pyref>
	in <pyref module="xist.ns.html">&html;</pyref>) to generate a principal block box and a
	list-item inline box.</doc:item>
	<doc:item><lit>marker</lit>: This value declares generated content before or after a box
	to be a marker. This value should only be used with <lit>:before</lit> and
	<lit>:after</lit> pseudo-elements attached to block-level elements. In other cases,
	this value is interpreted as <lit>inline</lit>.</doc:item>
	<doc:item><lit>none</lit>: This value causes an element to generate no boxes
	in the formatting structure (i.e., the element has no effect on layout). Descendant elements
	do not generate any boxes either; this behavior cannot be overridden by setting the
	<class>display</class> property on the descendants. Please note that a display of
	<lit>none</lit> does not create an invisible box; it creates no box at all. &css; includes
	mechanisms that enable an element to generate boxes in the formatting structure that
	affect formatting but are not visible themselves.</doc:item>
	<doc:item><lit>run-in</lit> and <lit>compact</lit>: These values create either block
	or inline boxes, depending on context. Properties apply to run-in and compact boxes based
	on their final status (inline-level or block-level). For example, the
	<pyref class="white_space"><class>white_space</class></pyref> property only applies if the box
	becomes a block box.</doc:item>
	<doc:item><lit>table</lit>, <lit>inline-table</lit>, <lit>table-row-group</lit>,
	<lit>table-column</lit>, <lit>table-column-group</lit>, <lit>table-header-group</lit>,
	<lit>table-footer-group</lit>, <lit>table-row</lit>, <lit>table-cell</lit>, and <lit>table-caption</lit>:
	These values cause an element to behave like a table element.</doc:item>
	</doc:ulist>
	"""

class position(prop):
	"""
	<doc:par>The <class>position</class> and <pyref class="float"><class>float</class></pyref> properties
	determine which of the &css;2 positioning algorithms is used to calculate the
	position of a box. The values of this property have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>static</lit>: The box is a normal box, laid out according to the normal flow.
	The <pyref class="left"><class>left</class></pyref> and <pyref class="top"><class>top</class></pyref>
	properties do not apply.</doc:item>
	<doc:item><lit>relative</lit>: The box's position is calculated according to the normal flow
	(this is called the position in normal flow). Then the box is offset relative to its normal
	position. When a box <lit><rep>B</rep></lit> is relatively positioned,
	the position of the following box is calculated as though <lit><rep>B</rep></lit>
	were not offset.</doc:item>
	<doc:item><lit>absolute</lit>: The box's position (and possibly size) is specified with the
	<pyref class="left"><class>left</class></pyref>, <pyref class="right"><class>right</class></pyref>,
	<pyref class="top"><class>top</class></pyref>, and <pyref class="bottom"><class>bottom</class></pyref>
	properties. These properties specify offsets with respect to the box's containing block.
	Absolutely positioned boxes are taken out of the normal flow. This means they have no impact
	on the layout of later siblings. Also, though absolutely positioned boxes have margins,
	they do not collapse with any other margins.</doc:item>
	<doc:item><lit>fixed</lit>: The box's position is calculated according to the
	<lit>absolute</lit> model, but in addition, the box is fixed with respect to some reference.
	In the case of continuous media, the box is fixed with respect to the viewport
	(and doesn't move when scrolled). In the case of paged media, the box is fixed with respect
	to the page, even if that page is seen through a viewport (in the case of a print-preview,
	for example).</doc:item>
	</doc:ulist>
	"""

class top(prop):
	"""
	<doc:par>This property specifies how far a box's top content edge
	is offset below the top edge of the box's containing block.</doc:par>
	"""

class right(prop):
	"""
	<doc:par>This property specifies how far a box's right content edge
	is offset to the left of the right edge of the box's containing block.</doc:par>
	"""

class bottom(prop):
	"""
	<doc:par>This property specifies how far a box's bottom content edge
	is offset above the bottom of the box's containing block.</doc:par>
	"""

class left(prop):
	"""
	<doc:par>This property specifies how far a box's left content edge
	is offset to the right of the left edge of the box's
	containing block.</doc:par>
	"""

class float(prop):
	"""
	<doc:par>This property specifies whether a box should float to the
	left, right, or not at all. It may be set for elements that
	generate boxes that are not absolutely positioned. The values
	of this property have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>left</lit>: The element generates a block box that is
	floated to the left. Content flows on the right side of the box,
	starting at the top (subject to the <pyref class="clear"><class>clear</class></pyref>
	property). The <pyref class="display"><class>display</class></pyref> is ignored,
	unless it has the value <lit>none</lit>.</doc:item>
	<doc:item><lit>right</lit>: Same as <lit>left</lit>, but content flows on the
	left side of the box, starting at the top.</doc:item>
	<doc:item><lit>none</lit>: The box is not floated.</doc:item>
	</doc:ulist>
	"""

class clear(prop):
	"""
	<doc:par>This property indicates which sides of an element's box(es) may <em>not</em>
	be adjacent to an earlier floating box. (It may be that the element itself has floating
	descendants; the <class>clear</class> property has no effect on those.)</doc:par>
	
	<doc:par>This property may only be specified for block-level elements (including floats).
	For compact and run-in boxes, this property applies to the final block box to which the
	compact or run-in box belongs.</doc:par>
	
	<doc:par>Values have the following meanings when applied to non-floating block boxes:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>left</lit>: The top margin of the generated box is increased enough
	that the top border edge is below the bottom outer edge of any left-floating boxes
	that resulted from elements earlier in the source document.</doc:item>
	<doc:item><lit>right</lit> The top margin of the generated box is increased enough
	that the top border edge is below the bottom outer edge of any right-floating boxes
	that resulted from elements earlier in the source document.</doc:item>
	<doc:item><lit>both</lit>: The generated box is moved below all floating boxes of
	earlier elements in the source document.</doc:item>
	<doc:item><lit>none</lit>: No constraint on the box's position with respect to floats.</doc:item>
	</doc:ulist>

	<doc:par>When the property is set on floating elements, it results in a modification
	of the rules for positioning the float. An extra constraint is added:
	The top outer edge of the float must be below the bottom outer edge of all earlier
	left-floating boxes (in the case of <markup>&lt;clear&gt;left&lt;clear&gt;</markup>),
	or all earlier right-floating boxes (in the case of <markup>&lt;clear&gt;right&lt;clear&gt;</markup>),
	or both (<markup>&lt;clear&gt;both&lt;clear&gt;</markup>).</doc:par>
	"""

class z_index(prop):
	"""
	<doc:par>For a positioned box, the <class>z_index</class>
	property specifies:</doc:par>
	
	<doc:olist>
	<doc:item>The stack level of the box in the current stacking context.</doc:item>
	<doc:item>Whether the box establishes a local stacking context.</doc:item>
	</doc:olist>
	
	<doc:par>Values have the following meanings:</doc:par>
	
	<doc:ulist>
	<doc:item><lit><rep>integer</rep></lit>: This integer is the stack level
	of the generated box in the current stacking context. The box also establishes a
	local stacking context in which its stack level is <lit>0</lit>.</doc:item>
	<doc:item><lit>auto</lit>: The stack level of the generated box in the current stacking context
	is the same as its parent's box. The box does not establish a new local stacking context.</doc:item>
	</doc:ulist>
	"""
	name = "z-index"

class direction(prop):
	"""
	<doc:par>This property specifies the base writing direction of blocks
	and the direction of embeddings and overrides
	(see <pyref class="unicode_bidi"><class>unicode_bidi</class></pyref>)
	for the Unicode bidirectional algorithm. In addition, it specifies the direction
	of table column layout, the direction of horizontal overflow, and the position
	of an incomplete last line in a block in case of <markup>&lt;text_align&gt;justify&lt;/text_align&gt;</markup>.</doc:par>
	
	<doc:par>Values for this property have the following meanings:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>ltr</lit>: Left-to-right direction.</doc:item>
	<doc:item><lit>rtl</lit>: Right-to-left direction.</doc:item>
	</doc:ulist>
	
	<doc:par>For the <class>direction</class> property to have any
	effect on inline-level elements, the <pyref class="unicode_bidi"><class>unicode_bidi</class></pyref>
	property's value must be <lit>embed</lit> or <lit>override</lit>.</doc:par>
	"""

class unicode_bidi(prop):
	"""
	<doc:par>Values for this property have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: The element does not open an additional level
	of embedding with respect to the bidirectional algorithm. For inline-level elements,
	implicit reordering works across element boundaries.</doc:item>
	<doc:item><lit>embed</lit>: If the element is inline-level, this value opens
	an additional level of embedding with respect to the bidirectional algorithm.
	The direction of this embedding level is given by the
	<pyref class="direction"><class>direction</class></pyref> property. Inside the element,
	reordering is done implicitly. This corresponds to adding a LRE (U+202A; for
	<markup>&lt;direction&gt;ltr&lt;/direction&gt;</markup>) or RLE
	(U+202B; for <markup>&lt;direction&lt;/gt;rtl&lt;/direction&lt;/gt;</markup>)
	at the start of the element and a PDF (U+202C) at the end of the element.</doc:item>
	<doc:item><lit>bidi-override</lit>: If the element is inline-level or a block-level
	element that contains only inline-level elements, this creates an override.
	This means that inside the element, reordering is strictly in sequence according
	to the <pyref class="direction"><class>direction</class></pyref> property; the implicit part
	of the bidirectional algorithm is ignored. This corresponds to adding a LRO (U+202D; for
	<markup>&lt;direction&/gt;ltr&lt;/direction&gt;</markup>) or RLO
	(U+202E; for <markup>&lt;direction&gt;rtl&lt;/direction&/gt;</markup>) at the start
	of the element and a PDF (U+202C) at the end of the element.</doc:item>
	</doc:ulist>

	<doc:par>The final order of characters in each block-level element is the same
	as if the bidi control codes had been added as described above, markup had been
	stripped, and the resulting character sequence had been passed to an implementation
	of the Unicode bidirectional algorithm for plain text that produced the same line-breaks
	as the styled text. In this process, non-textual entities such as images are treated as
	neutral characters, unless their <class>unicode_bidi</class> property has a value other
	than <lit>normal</lit>, in which case they are treated as strong characters in the
	<pyref class="direction"><class>direction</class></pyref> specified for the element.</doc:par>

	<doc:par>Please note that in order to be able to flow inline boxes in a uniform direction
	(either entirely left-to-right or entirely right-to-left), more inline boxes
	(including anonymous inline boxes) may have to be created, and some inline boxes may
	have to be split up and reordered before flowing.</doc:par>

	<doc:par>Because the Unicode algorithm has a limit of 15 levels of embedding,
	care should be taken not to use <class>unicode_bidi</class> with a value other
	than <lit>normal</lit> unless appropriate. In particular, a value of <lit>inherit</lit>
	should be used with extreme caution. However, for elements that are, in general,
	intended to be displayed as blocks, a setting of
	<markup>&lt;unicode_bidi&lt;/gt;embed&lt;/unicode_bidi&lt;/gt;</markup> is preferred
	to keep the element together in case display is changed to inline.</doc:par>
	"""
	name = "unicode-bidi"

class width(prop):
	"""
	<doc:par>This property specifies the content width of boxes generated by block-level
	and replaced elements.</doc:par>

	<doc:par>This property does not apply to non-replaced inline-level elements.
	The width of a non-replaced inline element's boxes is that of the rendered content
	within them (before any relative offset of children). Recall that inline boxes flow
	into line boxes. The width of line boxes is given by the their containing block,
	but may be shorted by the presence of floats.</doc:par>
	
	<doc:par>The width of a replaced element's box is intrinsic and may be scaled by the user agent
	if the value of this property is different than <lit>auto</lit>.</doc:par>
	"""

class min_width(prop):
	"""
	<doc:par>This property allow the authors to constrain box widths to a certain range.</doc:par>
	"""
	name = "min-width"

class max_width(prop):
	"""
	<doc:par>This property allow the authors to constrain box widths to a certain range.</doc:par>
	"""
	name = "max-width"

class height(prop):
	"""
	<doc:par>This property specifies the content height of boxes generated by block-level
	and replaced elements.</doc:par>

	<doc:par>This property does not apply to non-replaced inline-level elements.
	The height of a non-replaced inline element's boxes is given by the element's
	(possibly inherited) <pyref class="line_height"><class>line_height</class></pyref> value.</doc:par>
	"""

class min_height(prop):
	"""
	<doc:par>This property allow the authors to constrain box heights to a certain range.</doc:par>
	"""
	name = "min-height"

class max_height(prop):
	"""
	<doc:par>This property allow the authors to constrain box heights to a certain range.</doc:par>
	"""
	name = "max-height"

class line_height(prop):
	"""
	<doc:par>If the property is set on a block-level element whose content
	is composed of inline-level elements, it specifies the minimal height
	of each generated inline box.</doc:par>

	<doc:par>If the property is set on an inline-level element, it specifies
	the exact height of each box generated by the element. (Except for inline
	replaced elements, where the height of the box is given by the
	<pyref class="height"><class>height</class></pyref> property.)</doc:par>
	"""
	name = "line-height"

class vertical_align(prop):
	"""
	<doc:par>This property affects the vertical positioning inside a line box of the boxes
	generated by an inline-level element. The following values only have meaning with
	respect to a parent inline-level element, or to a parent block-level element,
	if that element generates anonymous inline boxes; they have no effect if no
	such parent exists.</doc:par>

	<doc:ulist>
	<doc:item><lit>baseline</lit>: Align the baseline of the box with the baseline of the parent box.
	If the box doesn't have a baseline, align the bottom of the box with the parent's baseline.</doc:item>
	<doc:item><lit>middle</lit>: Align the vertical midpoint of the box with the baseline
	of the parent box plus half the x-height of the parent.</doc:item>
	<doc:item><lit>sub</lit>: Lower the baseline of the box to the proper position
	for subscripts of the parent's box. (This value has no effect on the font size
	of the element's text.)</doc:item>
	<doc:item><lit>super</lit>: Raise the baseline of the box to the proper position
	for superscripts of the parent's box. (This value has no effect on the font size
	of the element's text.)</doc:item>
	<doc:item><lit>text-top</lit>: Align the top of the box with the top of the parent
	element's font.</doc:item>
	<doc:item><lit>text-bottom</lit>: Align the bottom of the box with the bottom of the
	parent element's font.</doc:item>
	<doc:item><lit><rep>percentage</rep></lit>: Raise (positive value)
	or lower (negative value) the box by this distance (a percentage of the
	<pyref class="line_height"><class>line_height</class></pyref> value). The value <lit>0%</lit>
	means the same as <lit>baseline</lit>.</doc:item>
	<doc:item><lit><rep>length</rep></lit>: Raise (positive value)
	or lower (negative value) the box by this distance. The value <lit>0cm</lit>
	means the same as <lit>baseline</lit>.</doc:item>
	</doc:ulist>

	<doc:par>The remaining values refer to the line box in which the generated box appears:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>top</lit>: Align the top of the box with the top of the line box.</doc:item>
	<doc:item><lit>bottom</lit>: Align the bottom of the box with the bottom of the line box.</doc:item>
	</doc:ulist>
	"""
	name = "vertical-align"

class overflow(prop):
	"""
	<doc:par>This property specifies whether the content of a block-level element is clipped
	when it overflows the element's box (which is acting as a containing block for the content).
	Values have the following meanings:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>visible</lit>: This value indicates that content is not clipped, i.e.,
	it may be rendered outside the block box.</doc:item>
	<doc:item><lit>hidden</lit>: This value indicates that the content is clipped
	and that no scrolling mechanism should be provided to view the content outside
	the clipping region; users will not have access to clipped content. The size and shape
	of the clipping region is specified by the <pyref class="clip"><class>clip</class></pyref> property.</doc:item>
	<doc:item><lit>scroll</lit>: This value indicates that the content is clipped and
	that if the user agent uses scrolling mechanism that is visible on the screen
	(such as a scroll bar or a panner), that mechanism should be displayed for a box
	whether or not any of its content is clipped. This avoids any problem with scrollbars
	appearing and disappearing in a dynamic environment. When this value is specified
	and the target medium is <lit>print</lit> or <lit>projection</lit>, overflowing
	content should be printed. </doc:item>
	<doc:item><lit>auto</lit>: The behavior of the <lit>auto</lit> value is user
	agent-dependent, but should cause a scrolling mechanism to be provided
	for overflowing boxes.</doc:item>
	</doc:ulist>
	<doc:par>Even if <class>overflow</class> is set to <lit>visible</lit>, content may be clipped
	to a UA's document window by the native operating environment.</doc:par>
	"""

class clip(prop):
	"""
	<doc:par>The <class>clip</class> property applies to elements that have a
	<pyref class="overflow"><class>overflow</class></pyref> property with a value
	other than <lit>visible</lit>. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>auto</lit>: The clipping region has the same size and
	location as the element's box(es).</doc:item>
	<doc:item><doc:par><lit><rep>shape</rep></lit>: In &css;2, the only valid
	<lit><rep>shape</rep></lit> value is: rect
	(<lit><rep>top</rep> <rep>right</rep> <rep>bottom</rep> <rep>left</rep></lit>)
	where <lit><rep>top</rep></lit>, <lit><rep>bottom</rep></lit>,
	<lit><rep>right</rep></lit>, and <lit><rep>left</rep></lit>
	specify offsets from the respective sides of the box.</doc:par>

	<doc:par><lit><rep>top</rep></lit>, <lit><rep>right</rep></lit>,
	<lit><rep>bottom</rep></lit>, and <lit><rep>left</rep></lit>
	may either have a <lit><rep>length</rep></lit> value or <lit>auto</lit>.
	Negative lengths are permitted. The value <lit>auto</lit> means that a given edge of
	the clipping region will be the same as the edge of the element's generated box
	(i.e., <lit>auto</lit> means the same as <lit>0</lit>.)</doc:par>

	<doc:par>When coordinates are rounded to pixel coordinates, care should be taken that
	no pixels remain visible when <lit><rep>left</rep> + <rep>right</rep></lit>
	is equal to the element's width (or <lit><rep>top</rep> + <rep>bottom</rep></lit>
	equals the element's height), and conversely that no pixels remain hidden when these values are 0.</doc:par>
	</doc:item>
	</doc:ulist>

	<doc:par>The element's ancestors may also have clipping regions (in case their
	<pyref class="overflow"><class>overflow</class></pyref> property is not <lit>visible</lit>);
	what is rendered is the intersection of the various clipping regions.</doc:par>

	<doc:par>If the clipping region exceeds the bounds of the UA's document window,
	content may be clipped to that window by the native operating environment.</doc:par>
	"""

class visibility(prop):
	"""
	<doc:par>The <class>visibility</class> property specifies whether the boxes generated
	by an element are rendered. Invisible boxes still affect layout (set the
	<pyref class="display"><class>display</class></pyref> property to <lit>none</lit> to
	suppress box generation altogether). Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>visible</lit>: The generated box is visible.</doc:item>
	<doc:item><lit>hidden</lit>: The generated box is invisible (fully transparent),
	but still affects layout.</doc:item>
	<doc:item><lit>collapse</lit>: Used for dynamic row and column effects in tables.
	If used on elements other than rows or columns, <lit>collapse</lit> has the same
	meaning as <lit>hidden</lit>.</doc:item>
	</doc:ulist>

	<doc:par>This property may be used in conjunction with scripts to create dynamic effects.</doc:par>
	"""

class content(prop):
	"""
	<doc:par>This property is used with the <lit>:before</lit> and <lit>:after</lit>
	pseudo-elements to generate content in a document.</doc:par>
	"""

class quotes(prop):
	"""
	<doc:par>This property specifies quotation marks for any number of embedded quotations.
	Values have the following meanings:</doc:par>
	<doc:ulist>
	<doc:item><lit>none</lit>: The <lit>open-quote</lit> and <lit>close-quote</lit>
	values of the <pyref class="content"><class>content</class></pyref>
	property produce no quotations marks.</doc:item>
	<doc:item>an even number of strings: Values for the <lit>open-quote</lit> and <lit>close-quote</lit>
	values of the <pyref class="content"><class>content</class></pyref> property are taken from this list
	of pairs of quotation marks (opening and closing). The first (leftmost) pair represents the
	outermost level of quotation, the second pair the first level of embedding, etc.
	The user agent must apply the appropriate pair of quotation marks according to the
	level of embedding.</doc:item>
	</doc:ulist>
	"""

class counter_reset(prop):
	"""
	<doc:par>The <class>counter_reset</class> property contains a list of one or more names of counters,
	each one optionally followed by an integer. The integer gives the value that the counter is set to
	on each occurrence of the element. The default is 0.</doc:par> 
	"""
	name = "counter-reset"

class counter_increment(prop):
	"""
	<doc:par>The <class>counter_increment</class> property accepts one or more names of counters 
	(identifiers), each one optionally followed by an integer. The integer indicates by how much 
	the counter is incremented for every occurrence of the element. The default increment is 1.
	Zero and negative integers are allowed.</doc:par>
	"""
	name = "counter-increment"

class marker_offset(prop):
	"""
	<doc:par>This property specifies the distance between the nearest border edges of a marker box
	and its associated principal box. The offset may either be a user-specified length or
	chosen by the UA (<lit>auto</lit>). Lengths may be negative, but there may be 
	implementation-specific limits.</doc:par>
	"""
	name = "marker-offset"

class list_style_type(prop):
	"""
	<doc:par>This property specifies appearance of the list item marker if
	<pyref class="list_style_image"><class>list_style_image</class></pyref> has the value <lit>none</lit>
	or if the image pointed to by the URI cannot be displayed. The value <lit>none</lit> specifies no marker,
	otherwise there are three types of marker: glyphs, numbering systems, and alphabetic systems.</doc:par>
	
	<doc:par>Glyphs are specified with <lit>disc</lit>, <lit>circle</lit>, and <lit>square</lit>.
	Their exact rendering depends on the user agent.</doc:par> 
	
	<doc:par>Numbering systems are specified with:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>decimal</lit>: Decimal numbers, beginning with 1.</doc:item> 
	<doc:item><lit>decimal-leading-zero</lit>: Decimal numbers padded by initial zeros
	(e.g., 01, 02, 03, ..., 98, 99).</doc:item> 
	<doc:item><lit>lower-roman</lit>: Lowercase roman numerals (i, ii, iii, iv, v, etc.).</doc:item> 
	<doc:item><lit>upper-roman</lit>: Uppercase roman numerals (I, II, III, IV, V, etc.).</doc:item>
	<doc:item><lit>hebrew</lit>: Traditional Hebrew numbering.</doc:item>
	<doc:item><lit>georgian</lit>: Traditional Georgian numbering
	(an, ban, gan, ..., he, tan, in, in-an, ...).</doc:item>
	<doc:item><lit>armenian</lit>: Traditional Armenian numbering.</doc:item>
	<doc:item><lit>cjk-ideographic</lit>: Plain ideographic numbers.</doc:item>
	<doc:item><lit>hiragana</lit>: a, i, u, e, o, ka, ki, ...</doc:item>
	<doc:item><lit>katakana</lit>: A, I, U, E, O, KA, KI, ...</doc:item>
	<doc:item><lit>hiragana-iroha</lit>: i, ro, ha, ni, ho, he, to, ...</doc:item>
	<doc:item><lit>katakana-iroha</lit>: I, RO, HA, NI, HO, HE, TO, ...</doc:item>
	</doc:ulist>

	<doc:par>Alphabetic systems are specified with:</doc:par>
	
	<doc:ulist>
	<doc:item><lit>lower-latin</lit> or <lit>lower-alpha</lit>: Lowercase ascii letters
	(a, b, c, ... z).</doc:item>
	<doc:item><lit>upper-latin</lit> or <lit>upper-alpha</lit>: Uppercase ascii letters
	(A, B, C, ... Z).</doc:item>
	<doc:item><lit>lower-greek</lit>: Lowercase classical Greek alpha, beta, gamma, ...
	(&#941;, &#942;, &#943;, ...)</doc:item>
	</doc:ulist>
	"""
	name = "list-style-type"

class list_style_image(prop):
	"""
	<doc:par>This property sets the image that will be used as the list item marker. When the image is available,
	it will replace the marker set with the <pyref class="list_style_type"><class>list_style_type</class></pyref> marker.</doc:par>
	"""
	name = "list-style-image"

class list_style_position(prop):
	"""
	<doc:par>This property specifies the position of the marker box in the principal block box. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>outside</lit>: The marker box is outside the principal block box. Note. &css;1 did not specify the precise location
	of the marker box and for reasons of compatibility, &css;2 remains equally ambiguous. For more precise control of marker boxes,
	please use markers.</doc:item>
	<doc:item><lit>inside</lit>: The marker box is the first inline box in the principal block box, after which the element's content flows.</doc:item>
	</doc:ulist>
	"""
	name = "list-style-position"

class list_style(prop):
	"""
	<doc:par>The <class>list_style</class> property is a shorthand notation for setting the three properties
	<pyref class="list_style_type"><class>list_style_type</class></pyref>,
	<pyref class="list_style_image"><class>list_style_image</class></pyref>, and
	<pyref class="list_style_position"><class>list_style_position</class></pyref> at the same place in the style sheet.</doc:par>
	"""
	name = "list-style"

class size(prop):
	"""
	<doc:par>This property specifies the size and orientation of a page box.</doc:par>

	<doc:par>The size of a page box may either be <z>absolute</z> (fixed size) or <z>relative</z>
	(scalable, i.e., fitting available sheet sizes). Relative page boxes allow user agents to scale a document
	and make optimal use of the target size.</doc:par>

	<doc:par>Three values for the <class>size</class> property create a relative page box:</doc:par>

	<doc:ulist>
	<doc:item><lit>auto</lit>: The page box will be set to the size and orientation of the target sheet.</doc:item>
	<doc:item><lit>landscape</lit>: Overrides the target's orientation. The page box is the same size as the target,
	and the longer sides are horizontal.</doc:item>
	<doc:item><lit>portrait</lit>: Overrides the target's orientation. The page box is the same size as the target,
	and the shorter sides are horizontal.</doc:item>
	</doc:ulist>

	<doc:par>One or two length values for the <class>size</class> property create an absolute page box.
	If only one length value is specified, it sets both the width and height of the page box (i.e., the box is a square).
	Since the page box is the initial containing block, percentage values are not allowed for the <class>size</class> property.</doc:par>

	"""

class marks(prop):
	"""
	<doc:par>In high-quality printing, marks are often added outside the page box. This property specifies whether cross marks
	or crop marks or both should be rendered just outside the page box edge.</doc:par>

	<doc:par>Allowed values are <lit>crop</lit>, <lit>cross</lit> (or both), <lit>none</lit> and <lit>inherit</lit>.</doc:par>

	<doc:par>Crop marks indicate where the page should be cut. Cross marks (also known as register marks or registration marks)
	are used to align sheets.</doc:par>

	<doc:par>Marks are visible only on absolute page boxes (see the <pyref class="size"><class>size</class></pyref> property).
	In relative page boxes, the page box will be aligned with the target and the marks will be outside the printable area.</doc:par>

	<doc:par>The size, style, and position of cross marks depend on the user agent.</doc:par>
	"""

class page_break_before(prop):
	"""
	<doc:par>Controls whether a page break should occur before the generated box.
	Values for this property have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>auto</lit>: Neither force nor forbid a page break before the generated box.</doc:item>
	<doc:item><lit>always</lit>: Always force a page break before the generated box.</doc:item>
	<doc:item><lit>avoid</lit>: Avoid a page break before the generated box.</doc:item>
	<doc:item><lit>left</lit>: Force one or two page breaks before the generated box
	so that the next page is formatted as a left page.</doc:item>
	<doc:item><lit>right</lit>: Force one or two page breaks before the generated box
	so that the next page is formatted as a right page.</doc:item>
	</doc:ulist>

	<doc:par>A potential page break location is typically under the influence of the parent element's
	<pyref class="page_break_inside"><class>page_break_inside</class></pyref> property, the
	<pyref class="page_break_after"><class>page_break_after</class></pyref> property of the preceding element,
	and the <class>page_break_before</class> property of the following element.
	When these properties have values other than <lit>auto</lit>, the values <lit>always</lit>, <lit>left</lit>,
	and <lit>right</lit> take precedence over <lit>avoid</lit>.</doc:par>
	"""
	name = "page-break-before"

class page_break_after(prop):
	"""
	<doc:par>Controls whether a page break should occur after the generated box.
	For allowed values see <pyref class="page_break_before"><class>page_break_before</class></pyref>.</doc:par>
	"""
	name = "page-break-after"

class page_break_inside(prop):
	"""
	<doc:par>Controls whether a page break should occur inside the generated box.
	For allowed values see <pyref class="page_break_before"><class>page_break_before</class></pyref>.</doc:par>
	"""
	name = "page-break-inside"

class atpage(prop):
	"""
	"""

class orphans(prop):
	"""
	<doc:par>The <class>orphans</class> property specifies the minimum number of lines of a paragraph
	that must be left at the bottom of a page.</doc:par>
	"""

class widows(prop):
	"""
	<doc:par>The <class>widows</class> property specifies the minimum number of lines of a paragraph
	that must be left at the top of a page.</doc:par>
	"""

class color(prop):
	"""
	<doc:par>This property describes the foreground color of an element's text content.</doc:par>
	"""

class background_color(prop):
	"""
	<doc:par>This property sets the background color of an element,
	either a color value or the keyword <lit>transparent</lit>,
	to make the underlying colors shine through.</doc:par>
	"""
	name = "background-color"

class background_image(prop):
	"""
	<doc:par>This property sets the background image of an element. When setting a background image,
	authors should also specify a background color that will be used when the image is unavailable.
	When the image is available, it is rendered on top of the background color. (Thus, the color
	is visible in the transparent parts of the image).</doc:par>

	<doc:par>Values for this property are either an URL, to specify the image, or <lit>none</lit>,
	when no image is used.</doc:par>
	"""
	name = "background-image"

class background_repeat(prop):
	"""
	<doc:par>If a background image is specified, this property specifies
	whether the image is repeated (tiled), and how. All tiling covers the content
	and padding areas of a box. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>repeat</lit>: The image is repeated both horizontally and vertically.</doc:item>
	<doc:item><lit>repeat-x</lit>: The image is repeated horizontally only.</doc:item>
	<doc:item><lit>repeat-y</lit>: The image is repeated vertically only.</doc:item>
	<doc:item><lit>no-repeat</lit>: The image is not repeated: only one copy of the image is drawn.</doc:item>
	</doc:ulist>
	"""
	name = "background-repeat"

class background_attachment(prop):
	"""
	<doc:par>If a background image is specified, this property specifies
	whether it is fixed with regard to the viewport (<lit>fixed</lit>)
	or scrolls along with the document (<lit>scroll</lit>).</doc:par>

	<doc:par>Even if the image is fixed, it is still only visible
	when it is in the background or padding area of the element.
	Thus, unless the image is tiled (with
	<markup>&lt;background-repeat&gt;repeat&lt;/background-repeat&gt;</markup>), it may be invisible.</doc:par>
	"""
	name = "background-attachment"

class background_position(prop):
	"""
	<doc:par>If a background image has been specified, this property specifies its initial position.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>percentage</rep> <rep>percentage</rep></lit>:
	With a value pair of <lit>0% 0%</lit>, the upper left corner of the image is aligned
	with the upper left corner of the box's padding edge. A value pair of <lit>100% 100%</lit>
	places the lower right corner of the image in the lower right corner of padding area.
	With a value pair of <lit>14% 84%</lit>, the point 14% across and 84% down the image
	is to be placed at the point 14% across and 84% down the padding area.</doc:item>
	<doc:item><lit><rep>length</rep> <rep>length</rep></lit>:
	With a value pair of <lit>2cm 2cm</lit>, the upper left corner of the image is placed
	2cm to the right and 2cm below the upper left corner of the padding area.</doc:item>
	<doc:item><lit>top left</lit> and <lit>left top</lit>: Same as <lit>0% 0%</lit>.</doc:item>
	<doc:item><lit>top</lit>, <lit>top center</lit>, and <lit>center top</lit>: Same as <lit>50% 0%</lit>.</doc:item>
	<doc:item><lit>right top</lit> and <lit>top right</lit>: Same as <lit>100% 0%</lit>.</doc:item>
	<doc:item><lit>left</lit>, <lit>left center</lit>, and <lit>center left</lit>: Same as <lit>0% 50%</lit>.</doc:item>
	<doc:item><lit>center</lit> and <lit>center center</lit>: Same as <lit>50% 50%</lit>.</doc:item>
	<doc:item><lit>right</lit>, <lit>right center</lit>, and <lit>center right</lit>: Same as <lit>100% 50%</lit>.</doc:item>
	<doc:item><lit>bottom left</lit> and <lit>left bottom</lit>: Same as <lit>0% 100%</lit>.</doc:item>
	<doc:item><lit>bottom</lit>, <lit>bottom center</lit>, and <lit>center bottom</lit>: Same as <lit>50% 100%</lit>.</doc:item>
	<doc:item><lit>bottom right</lit> and <lit>right bottom</lit>: Same as <lit>100% 100%</lit>.</doc:item>
	</doc:ulist>
	
	<doc:par>If only one percentage or length value is given, it sets the horizontal position only,
	the vertical position will be <lit>50%</lit>. If two values are given, the horizontal position comes first.
	Combinations of length and percentage values are allowed, (e.g., <lit>50% 2cm</lit>). Negative positions are allowed.
	Keywords cannot be combined with percentage values or length values (all possible combinations are given above).</doc:par>

	<doc:par>If the background image is fixed within the viewport (see the
	<pyref class="background_attachment"><class>background_attachment</class></pyref> property), the image is placed
	relative to the viewport instead of the element's padding area.</doc:par>
	"""
	name = "background-position"

class background(prop):
	"""
	<doc:par>The <class>background</class> property is a shorthand property for setting the individual background properties
	(i.e.,
	<pyref class="background_color"><class>background_color</class></pyref>,
	<pyref class="background_image"><class>background_image</class></pyref>,
	<pyref class="background_repeat"><class>background_repeat</class></pyref>,
	<pyref class="background_attachment"><class>background_attachment</class></pyref> and
	<pyref class="background_position"><class>background_position</class></pyref>
	(in this order)) at the same place in the style sheet.</doc:par>

	<doc:par>The <class>background</class> property first sets all the individual background properties
	to their initial values, then assigns explicit values given in the declaration.</doc:par>
	"""

class font_family(prop):
	"""
	<doc:par>This property specifies a prioritized list of font family names and/or generic family names.
	To deal with the problem that a single font may not contain glyphs to display all the characters in a document,
	or that not all fonts are available on all systems, this property allows authors to specify a list of fonts,
	all of the same style and size, that are tried in sequence to see if they contain a glyph for a certain character.
	This list is called a font set.</doc:par>

	<doc:par>The generic font family will be used if one or more of the other fonts in a font set is unavailable.
	Although many fonts provide the <z>missing character</z> glyph, typically an open box, as its name implies
	this should not be considered a match except for the last font in a font set.</doc:par>

	<doc:par>There are two types of font family names:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>family-name</rep></lit>: The name of a font family of choice.
	For example <lit>Baskerville</lit>, <lit>Heisi Mincho W3</lit> and <lit>Symbol</lit> are font families.
	Font family names containing whitespace should be quoted. If quoting is omitted, any whitespace characters
	before and after the font name are ignored and any sequence of whitespace characters inside the font name
	is converted to a single space.</doc:item>
	<doc:item><lit><rep>generic-family</rep></lit>: The following generic families are defined:
	<lit>serif</lit>, <lit>sans-serif</lit>, <lit>cursive</lit>, <lit>fantasy</lit>, and <lit>monospace</lit>.
	Generic font family names are keywords, and therefore must not be quoted.</doc:item>
	</doc:ulist>
	
	<doc:par>Authors are encouraged to offer a generic font family as a last alternative, for improved robustness.</doc:par>
	"""
	name = "font-family"

class font_style(prop):
	"""
	<doc:par>The <class>font_style</class> property requests normal (sometimes referred to as <z>roman</z> or <z>upright</z>),
	italic, and oblique faces within a font family. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: Specifies a font that is classified as <z>normal</z> in the UA's font database.</doc:item>
	<doc:item><lit>oblique</lit>: Specifies a font that is classified as <z>oblique</z> in the UA's font database.
	Fonts with Oblique, Slanted, or Incline in their names will typically be labeled <z>oblique</z> in the font database.
	A font that is labeled <z>oblique</z> in the UA's font database may actually have been generated
	by electronically slanting a normal font.</doc:item>
	<doc:item><lit>italic</lit>: Specifies a font that is classified as <z>italic</z> in the UA's font database, or,
	if that is not available, one labeled <z>oblique</z>. Fonts with Italic, Cursive, or Kursiv
	in their names will typically be labeled <z>italic</z>.</doc:item>
	</doc:ulist>
	"""
	name = "font-style"

class font_variant(prop):
	"""
	<doc:par>In a small-caps font, the glyphs for lowercase letters look similar to the uppercase ones,
	but in a smaller size and with slightly different proportions. The <class>font_variant</class> property
	requests such a font for bicameral (having two cases, as with Latin script). This property has no visible effect
	for scripts that are unicameral (having only one case, as with most of the world's writing systems).
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: Specifies a font that is not labeled as a small-caps font.</doc:item>
	<doc:item><lit>small-caps</lit>: Specifies a font that is labeled as a small-caps font.
	If a genuine small-caps font is not available, user agents should simulate a small-caps font,
	for example by taking a normal font and replacing the lowercase letters by scaled uppercase characters.
	As a last resort, unscaled uppercase letter glyphs in a normal font may replace glyphs in a small-caps font
	so that the text appears in all uppercase letters.</doc:item>
	</doc:ulist>
	"""
	name = "font-variant"

class font_weight(prop):
	"""
	<doc:par>The <class>font_weight</class> property specifies the weight of the font.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>100</lit> to <lit>900</lit>: These values form an ordered sequence,
	where each number indicates a weight that is at least as dark as its predecessor.</doc:item>
	<doc:item><lit>normal</lit>: Same as <lit>400</lit>.</doc:item>
	<doc:item><lit>bold</lit>: Same as <lit>700</lit>.</doc:item>
	<doc:item><lit>bolder</lit>: Specifies the next weight that is assigned to a font that is darker than the inherited one.
	If there is no such weight, it simply results in the next darker numerical value (and the font remains unchanged),
	unless the inherited value was <lit>900</lit>, in which case the resulting weight is also <lit>900</lit>.</doc:item>
	<doc:item><lit>lighter</lit>: Specifies the next weight that is assigned to a font that is lighter
	than the inherited one. If there is no such weight, it simply results in the next lighter numerical value
	(and the font remains unchanged), unless the inherited value was <lit>100</lit>,
	in which case the resulting weight is also <lit>100</lit>.</doc:item>
	</doc:ulist>

	<doc:par>Child elements inherit the computed value of the weight.</doc:par>
	"""
	name = "font-weight"

class font_stretch(prop):
	"""
	<doc:par>The <class>font_stretch</class> property selects a normal, condensed, or extended face from a font family.
	Absolute keyword values have the following ordering, from narrowest to widest:</doc:par>

	<doc:olist>
	<doc:item><lit>ultra-condensed</lit></doc:item>
	<doc:item><lit>extra-condensed</lit></doc:item>
	<doc:item><lit>condensed</lit></doc:item>
	<doc:item><lit>semi-condensed</lit></doc:item>
	<doc:item><lit>normal</lit></doc:item>
	<doc:item><lit>semi-expanded</lit></doc:item>
	<doc:item><lit>expanded</lit></doc:item>
	<doc:item><lit>extra-expanded</lit></doc:item>
	<doc:item><lit>ultra-expanded</lit></doc:item>
	</doc:olist>
	
	<doc:par>The relative keyword <lit>wider</lit> sets the value to the next expanded value
	above the inherited value (while not increasing it above <lit>ultra-expanded</lit>); the relative keyword
	<lit>narrower</lit> sets the value to the next condensed value below the inherited value
	(while not decreasing it below <lit>ultra-condensed</lit>).</doc:par>
	"""
	name = "font-stretch"

class font_size(prop):
	"""
	<doc:par>This property describes the size of the font when set solid. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><doc:par><lit><rep>absolute-size</rep></lit>: An <lit><rep>absolute-size</rep></lit> keyword refers to an entry
	in a table of font sizes computed and kept by the user agent. Possible values are:
	<lit>xx-small</lit>, <lit>x-small</lit>, <lit>small</lit>, <lit>medium</lit>,
	<lit>large</lit>, <lit>x-large</lit> and <lit>xx-large</lit>.</doc:par>

	<doc:par>On a computer screen a scaling factor of 1.2 is suggested between adjacent indexes;
	if the <lit>medium</lit> font is 12pt, the <lit>large</lit> font could be 14.4pt. Different media may need different scaling factors.
	Also, the user agent should take the quality and availability of fonts into account when computing the table.
	The table may be different from one font family to another.</doc:par></doc:item>

	<doc:item><doc:par><lit><rep>relative-size</rep></lit>: A <lit><rep>relative-size</rep></lit> keyword
	is interpreted relative to the table of font sizes and the font size of the parent element. Possible values are
	<lit>larger</lit> and <lit>smaller</lit>.</doc:par>

	<doc:par>For example, if the parent element has a font size of <lit>medium</lit>, a value of <lit>larger</lit>
	will make the font size of the current element be <lit>large</lit>. If the parent element's size is not close
	to a table entry, the user agent is free to interpolate between table entries or round off to the closest one.
	The user agent may have to extrapolate table values if the numerical value goes beyond the keywords.</doc:par></doc:item>

	<doc:item><lit><rep>length</rep></lit>: A length value specifies an absolute font size
	(that is independent of the user agent's font table). Negative lengths are illegal.</doc:item>

	<doc:item><lit><rep>percentage</rep></lit>: A percentage value specifies an absolute font size relative
	to the parent element's font size. Use of percentage values, or values in <lit>em</lit>s,
	leads to more robust and cascadable style sheets.</doc:item>
	</doc:ulist>
	"""
	name = "font-size"

class font_size_adjust(prop):
	"""
	<doc:par>In bicameral scripts, the subjective apparent size and legibility of a font
	are less dependent on their <pyref class="font_size"><class>font_size</class></pyref> value
	than on the value of their <z>x-height</z>, or, more usefully, on the ratio of these two values,
	called the <z>aspect value</z> (font size divided by x-height). The higher the aspect value,
	the more likely it is that a font at smaller sizes will be legible. Inversely, faces with a lower aspect value
	will become illegible more rapidly below a given threshold size than faces with a higher aspect value.
	Straightforward font substitution that relies on font size alone may lead to illegible characters.</doc:par>

	<doc:par>For example, the popular font Verdana has an aspect value of 0.58; when Verdana's font size 100 units,
	its x-height is 58 units. For comparison, Times New Roman has an aspect value of 0.46. Verdana will therefore
	tend to remain legible at smaller sizes than Times New Roman. Conversely, Verdana will often look <z>too big</z> if substituted
	for Times New Roman at a chosen size.</doc:par>

	<doc:par>This property allows authors to specify an aspect value for an element that will preserve the x-height of the first choice font
	in the substitute font. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>none</lit>: Do not preserve the font's x-height.</doc:item>
	<doc:item><lit><rep>number</rep></lit>: Specifies the aspect value.
	The number refers to the aspect value of the first choice font.</doc:item>
	</doc:ulist>
	"""
	name = "font-size-adjust"

class font(prop):
	"""
	<doc:par>The <class>font</class> property is <z>almost</z> a shorthand property for setting
	<pyref class="font_style"><class>font_style</class></pyref>,
	<pyref class="font_variant"><class>font_variant</class></pyref>,
	<pyref class="font_weight"><class>font_weight</class></pyref>,
	<pyref class="font_size"><class>font_size</class></pyref>,
	<pyref class="line_height"><class>line_height</class></pyref>,
	and <pyref class="font_family"><class>font_family</class></pyref>,
	at the same place in the style sheet. The syntax of this property is based on a traditional typographical shorthand notation
	to set multiple properties related to fonts.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/fonts.html#font-shorthand">relevant part of the &css;2 spec</a>.</doc:par>
	"""

class atfontface(xsc.Element):
	"""
	<doc:par>A &css;2 font descriptor.</doc:par>
	"""
	empty = 0

	def publish(self, publisher):
		publisher.publish(u"@font-face\n{\n")
		self.content.publish(publisher)
		publisher.publish(u"\n}")

class text_indent(prop):
	"""
	<doc:par>This property specifies the indentation of the first line of text in a block.
	More precisely, it specifies the indentation of the first box that flows into the block's first line box.
	The box is indented with respect to the left (or right, for right-to-left layout) edge of the line box.
	User agents should render this indentation as blank space.</doc:par>

	<doc:par>Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>length</rep></lit>: The indentation is a fixed length.</doc:item>
	<doc:item><lit><rep>percentage</rep></lit>: The indentation is a percentage of the containing block width.</doc:item>
	</doc:ulist>
	
	<doc:par>The value of <class>text_indent</class> may be negative,
	but there may be implementation-specific limits.</doc:par>
	"""
	name = "text-indent"

class text_align(prop):
	"""
	<doc:par>This property describes how inline content of a block is aligned. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>left</lit>, <lit>right</lit>, <lit>center</lit>, and <lit>justify</lit>:
	Left, right, center, and double justify text, respectively.</doc:item>
	<doc:item><lit><rep>string</rep></lit>: Specifies a string on which cells in a table column will align.
	This value applies only to table cells. If set on other elements, it will be treated as <lit>left</lit> or <lit>right</lit>,
	depending on whether <pyref class="direction"><class>direction</class></pyref> is <lit>ltr</lit>, or <lit>rtl</lit>, respectively.</doc:item>
	</doc:ulist>
	"""
	name = "text-align"

class text_decoration(prop):
	"""
	<doc:par>This property describes decorations that are added to the text of an element.
	If the property is specified for a block-level element, it affects all inline-level descendants of the element.
	If it is specified for (or affects) an inline-level element, it affects all boxes generated by the element.
	If the element has no content or no text content (e.g., the <pyref module="xist.ns.html" class="img"><class>img</class></pyref>
	element in <pyref module="xist.ns.html">&html;</pyref>), user agents must ignore this property.</doc:par>

	<doc:par>Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>none</lit>: Produces no text decoration.</doc:item>
	<doc:item><lit>underline</lit>: Each line of text is underlined.</doc:item>
	<doc:item><lit>overline</lit>: Each line of text has a line above it.</doc:item>
	<doc:item><lit>line-through</lit>: Each line of text has a line through the middle.</doc:item>
	<doc:item><lit>blink</lit>: Text blinks (alternates between visible and invisible).
	Conforming user agents are not required to support this value.</doc:item>
	</doc:ulist>
	"""
	name = "text-decoration"

class text_shadow(prop):
	"""
	<doc:par>This property accepts a comma-separated list of shadow effects to be applied to the text of the element.
	The shadow effects are applied in the order specified and may thus overlay each other, but they will never overlay
	the text itself. Shadow effects do not alter the size of a box, but may extend beyond its boundaries.
	The stack level of the shadow effects is the same as for the element itself.</doc:par>

	<doc:par>Each shadow effect must specify a shadow offset and may optionally specify a blur radius and a shadow color.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/text.html#text-shadow-props">relevant part of the &css;2 spec</a>.</doc:par>
	"""
	name = "text-shadow"

class letter_spacing(prop):
	"""
	<doc:par>This property specifies spacing behavior between text characters. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: The spacing is the normal spacing for the current font. This value allows the user agent
	to alter the space between characters in order to justify text.</doc:item>
	<doc:item><lit><rep>length</rep></lit>: This value indicates inter-character space in addition
	to the default space between characters. Values may be negative, but there may be implementation-specific limits.
	User agents may not further increase or decrease the inter-character space in order to justify text.</doc:item>
	</doc:ulist>
	"""
	name = "letter-spacing"

class word_spacing(prop):
	"""
	<doc:par>This property specifies spacing behavior between words. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: The normal inter-word space, as defined by the current font and/or the UA.</doc:item>
	<doc:item><lit><rep>length</rep></lit>: This value indicates inter-word space in addition to the default space between words.
	Values may be negative, but there may be implementation-specific limits.</doc:item>
	</doc:ulist>
	"""
	name = "word-spacing"

class text_transform(prop):
	"""
	<doc:par>This property controls capitalization effects of an element's text. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>capitalize</lit>: Puts the first character of each word in uppercase.</doc:item>
	<doc:item><lit>uppercase</lit>: Puts all characters of each word in uppercase.</doc:item>
	<doc:item><lit>lowercase</lit>: Puts all characters of each word in lowercase.</doc:item>
	<doc:item><lit>none</lit>: No capitalization effects.</doc:item>
	</doc:ulist>
	"""
	name = "text-transform"

class white_space(prop):
	"""
	<doc:par>This property declares how whitespace inside the element is handled. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>normal</lit>: This value directs user agents to collapse sequences of whitespace,
	and break lines as necessary to fill line boxes. Additional line breaks may be created by occurrences of
	<z>\A</z> in generated content (e.g., for the <pyref module="xist.ns.html" class="br"><class>br</class></pyref> element
	in <pyref module="xist.ns.html">&html;</pyref>).</doc:item>

	<doc:item><lit>pre</lit>: This value prevents user agents from collapsing sequences of whitespace.
	Lines are only broken at newlines in the source, or at occurrences of <z>\A</z> in generated content.</doc:item>
	<doc:item><lit>nowrap</lit>: This value collapses whitespace as for <lit>normal</lit>, but suppresses line breaks within text
	except for those created by <z>\A</z> in generated content (e.g., for the <pyref module="xist.ns.html" class="br"><class>br</class></pyref> element
	in <pyref module="xist.ns.html">&html;</pyref>).</doc:item>
	</doc:ulist>
	"""
	name = "white-space"

class caption_side(prop):
	"""
	<doc:par>This property specifies the position of the caption box with respect to the table box.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>top</lit>: Positions the caption box above the table box.</doc:item>
	<doc:item><lit>bottom</lit>: Positions the caption box below the table box.</doc:item>
	<doc:item><lit>left</lit>: Positions the caption box to the left of the table box.</doc:item>
	<doc:item><lit>right</lit>: Positions the caption box to the right of the table box.</doc:item>
	</doc:ulist>
	"""
	name = "caption-side"

class table_layout(prop):
	"""
	<doc:par>The <class>table_layout</class> property controls the algorithm used to lay out
	the table cells, rows, and columns. Values have the following meaning:</doc:par>

	<doc:ulist>
	<doc:item><lit>fixed</lit>: Use the fixed table layout algorithm</doc:item>
	<doc:item><lit>auto</lit>: Use any automatic table layout algorithm</doc:item>
	</doc:ulist>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/tables.html#width-layout">relevant part of the &css;2 spec</a>.</doc:par>
	"""
	name = "table-layout"

class border_collapse(prop):
	"""
	<doc:par>This property selects a table's border model.
	The value <lit>separate</lit> selects the separated borders border model.
	The value <lit>collapse</lit> selects the collapsing borders model.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/tables.html#borders">relevant part of the &css;2 spec</a>.</doc:par>
	"""
	name = "border-collapse"

class border_spacing(prop):
	"""
	<doc:par>The lengths specify the distance that separates adjacent cell borders in a table.
	If one length is specified, it gives both the horizontal and vertical spacing. If two are specified,
	the first gives the horizontal spacing and the second the vertical spacing. Lengths may not be negative.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/tables.html#separated-borders">relevant part of the &css;2 spec</a>.</doc:par>
	"""
	name = "border-spacing"

class empty_cells(prop):
	"""
	<doc:par>In the separated borders model, this property controls the rendering of borders around cells in a table that have no visible content.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/tables.html#separated-borders">relevant part of the &css;2 spec</a>.</doc:par>
	"""
	name = "empty-cells"

class speak_header(prop):
	"""
	<doc:par>This property specifies whether table headers are spoken before every cell,
	or only before a cell when that cell is associated with a different header than the previous cell.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>once</lit>: The header is spoken one time, before a series of cells.</doc:item>
	<doc:item><lit>always</lit>: The header is spoken before every pertinent cell.</doc:item>
	</doc:ulist>
	"""
	name = "speak-header"

class cursor(prop):
	"""
	<doc:par>This property specifies the type of cursor to be displayed for the pointing device. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>auto</lit>: The UA determines the cursor to display based on the current context.</doc:item>
	<doc:item><lit>crosshair</lit>: A simple crosshair (e.g., short line segments resembling a <z>+</z> sign).</doc:item>
	<doc:item><lit>default</lit>: The platform-dependent default cursor. Often rendered as an arrow.</doc:item>
	<doc:item><lit>pointer</lit>: The cursor is a pointer that indicates a link.</doc:item>
	<doc:item><lit>move</lit>: Indicates something is to be moved.</doc:item>
	<doc:item><lit>e-resize</lit>, <lit>ne-resize</lit>, <lit>nw-resize</lit>,
	<lit>n-resize</lit>, <lit>se-resize</lit>, <lit>sw-resize</lit>, <lit>s-resize</lit>, <lit>w-resize</lit>:
	Indicate that some edge is to be moved. For example, the <lit>se-resize</lit> cursor is used when the movement
	starts from the south-east corner of the box.</doc:item>
	<doc:item><lit>text</lit>: Indicates text that may be selected. Often rendered as an I-bar.</doc:item>
	<doc:item><lit>wait</lit>: Indicates that the program is busy and the user should wait. Often rendered as a watch or hourglass.</doc:item>
	<doc:item><lit>help</lit>: Help is available for the object under the cursor. Often rendered as a question mark or a balloon.</doc:item>
	<doc:item><lit><rep>uri</rep></lit>: The user agent retrieves the cursor from the resource designated by the URI.
	If the user agent cannot handle the first cursor of a list of cursors, it should attempt to handle the second, etc.
	If the user agent cannot handle any user-defined cursor, it must use the generic cursor at the end of the list.</doc:item>
	</doc:ulist>
	"""

class outline(prop):
	"""
	<doc:par>At times, style sheet authors may want to create outlines around visual objects
	such as buttons, active form fields, image maps, etc., to make them stand out.
	&css;2 outlines differ from borders in the following ways:</doc:par>

	<doc:olist>
	<doc:item>Outlines do not take up space.</doc:item>
	<doc:item>Outlines may be non-rectangular.</doc:item>
	</doc:olist>

	<doc:par>The <class>outline</class> property is a shorthand property, and sets all three of
	<pyref class="outline_style"><class>outline_style</class></pyref>,
	<pyref class="outline_width"><class>outline_width</class></pyref>,
	and <pyref class="outline_colro"><class>outline_color</class></pyref>.</doc:par>

	<doc:par>For more info see the <a href="http://www.w3.org/TR/REC-CSS2/ui.html#dynamic-outlines">relevant part of the &css;2 spec</a>.</doc:par>
	"""

class outline_width(prop):
	"""
	<doc:par>Specifies the width of the outline. Allowed values
	are the same as for <pyref class="border_width"><class>border_width</class></pyref>.</doc:par>
	"""
	name = "outline-width"

class outline_style(prop):
	"""
	<doc:par>Specifies the style of the outline. Allowed values
	are the same as for <pyref class="border_style"><class>border_style</class></pyref> except that
	<lit>hidden</lit> is not allowed.</doc:par>
	"""
	name = "outline-style"

class outline_color(prop):
	"""
	<doc:par>Specifies the color of the outline. Allowed values
	are the same as for <pyref class="border_color"><class>border_color</class></pyref> and the
	special keyword <lit>invert</lit>.</doc:par>
	"""
	name = "outline-color"

class volume(prop):
	"""
	<doc:par>Volume refers to the median volume of the waveform. In other words, a highly inflected voice
	at a volume of 50 might peak well above that. The overall values are likely to be human adjustable for comfort,
	for example with a physical volume control (which would increase both the 0 and 100 values proportionately);
	what this property does is adjust the dynamic range.</doc:par>

	<doc:par>Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>number</rep></lit>: Any number between <lit>0</lit> and <lit>100</lit>.
	<lit>0</lit> represents the minimum audible volume level and <lit>100</lit> corresponds to the maximum comfortable level.</doc:item>
	<doc:item><lit><rep>percentage</rep></lit>: Percentage values are calculated relative to the inherited value,
	and are then clipped to the range <lit>0</lit> to <lit>100</lit>.</doc:item>
	<doc:item><lit>silent</lit>: No sound at all. The value <lit>0</lit> does not mean the same as <lit>silent</lit>.</doc:item>
	<doc:item><lit>x-soft</lit>: Same as <lit>0</lit>.</doc:item>
	<doc:item><lit>soft</lit>: Same as <lit>25</lit>.</doc:item>
	<doc:item><lit>medium</lit>: Same as <lit>50</lit>.</doc:item>
	<doc:item><lit>loud</lit>: Same as <lit>75</lit>.</doc:item>
	<doc:item><lit>x-loud</lit>: Same as <lit>100</lit>.</doc:item>
	</doc:ulist>
	"""

class speak(prop):
	"""
	<doc:par>This property specifies whether text will be rendered aurally and if so,
	in what manner (somewhat analogous to the <pyref class="display"><class>display</class></pyref> property).
	The possible values are:</doc:par>

	<doc:ulist>
	<doc:item><lit>none</lit>: Suppresses aural rendering so that the element requires no time to render.
	Note, however, that descendants may override this value and will be spoken.
	(To be sure to suppress rendering of an element and its descendants,
	use the <pyref class="display"><class>display</class></pyref> property).</doc:item>
	<doc:item><lit>normal</lit>: Uses language-dependent pronunciation rules for rendering an element and its children.</doc:item>
	<doc:item><lit>spell-out</lit>: Spells the text one letter at a time (useful for acronyms and abbreviations).</doc:item>
	</doc:ulist>

	<doc:par>Note the difference between an element whose <pyref class="volume"><class>volume</class></pyref> property
	has a value of <lit>silent</lit> and an element whose <class>speak</class> property has the value <lit>none</lit>.
	The former takes up the same time as if it had been spoken, including any pause before and after the element,
	but no sound is generated. The latter requires no time and is not rendered (though its descendants may be).</doc:par>
	"""

class pause_before(prop):
	"""
	<doc:par>These property specify a pause to be observed before speaking an element's content.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>time</rep></lit>: Expresses the pause in absolute time units (seconds and milliseconds).</doc:item>
	<doc:item><lit><rep>percentage</rep></lit>: Refers to the inverse of the value
	of the <pyref class="speech_rate"><class>speech_rate</class></pyref> property. For example,
	if the speech-rate is 120 words per minute (i.e., a word takes half a second, or 500ms) then a
	<class>pause-before</class> of <lit>100%</lit> means a pause of 500 ms and a
	<class>pause_before</class> of <lit>20%</lit> means 100ms.</doc:item>
	</doc:ulist>

	<doc:par>The pause is inserted between the element's content and any
	<pyref class="cue_before"><class>cue_before</class></pyref> content.</doc:par>

	<doc:par>Authors should use relative units to create more robust style sheets in the face of large changes in speech-rate.</doc:par>
	"""
	name = "pause-before"

class pause_after(prop):
	"""
	<doc:par>These property specify a pause to be observed after speaking an element's content.
	For allowed values see <pyref class="pause_before"><class>pause_before</class></pyref>.</doc:par>
	"""
	name = "pause-after"

class pause(prop):
	"""
	<doc:par>The <class>pause</class> property is a shorthand for setting
	<pyref class="pause_before"><class>pause_before</class></pyref> and
	<pyref class="pause_after"><class>pause_after</class></pyref>.
	If two values are given, the first value is <pyref class="pause_before"><class>pause_before</class></pyref>
	and the second is <pyref class="pause_after"><class>pause_after</class></pyref>.
	If only one value is given, it applies to both properties.</doc:par>
	"""

class cue_before(prop):
	"""
	<doc:par>Auditory icons are another way to distinguish semantic elements.
	Sounds may be played before the element to delimit it with <class>cue_before</class>.
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>uri</rep></lit>: The URI must designate an auditory icon resource.
	If the URI resolves to something other than an audio file, such as an image, the resource
	should be ignored and the property treated as if it had the value <lit>none</lit>.</doc:item>
	<doc:item><lit>none</lit>: No auditory icon is specified.</doc:item>
	</doc:ulist>
	"""
	name = "cue-before"

class cue_after(prop):
	"""
	<doc:par>A sound may be played after the element to delimit it with <class>cue_after</class>.
	For allowed values see <pyref class="cue_before"><class>cue_before</class></pyref></doc:par>
	"""
	name = "cue-after"

class cue(prop):
	"""
	<doc:par>The <class>cue</class> property is a shorthand for setting
	<pyref class="cue_before"><class>cue_before</class></pyref> and
	<pyref class="cue_after"><class>cue_after</class></pyref>.
	If two values are given, the first value is <pyref class="cue_before"><class>cue_before</class></pyref>
	and the second is <pyref class="cue_after"><class>cue_after</class></pyref>.
	If only one value is given, it applies to both properties.</doc:par>
	"""
	name = "cue"

class play_during(prop):
	"""
	<doc:par>Similar to the <pyref class="cue_before"><class>cue_before</class></pyref> and
	<pyref class="cue_after"><class>cue_after</class></pyref> properties, this property specifies a sound
	to be played as a background while an element's content is spoken. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>uri</rep></lit>: The sound designated by this <rep>uri</rep> is played as a background
	while the element's content is spoken.</doc:item>
	<doc:item><lit>mix</lit>: When present, this keyword means that the sound inherited from the parent element's
	<class>play_during</class> property continues to play and the sound designated by the <rep>uri</rep> is mixed with it.
	If <lit>mix</lit> is not specified, the element's background sound replaces the parent's.</doc:item>
	<doc:item><lit>repeat</lit>: When present, this keyword means that the sound will repeat if it is too short
	to fill the entire duration of the element. Otherwise, the sound plays once and then stops. This is similar to the
	<pyref class="background_repeat"><class>background-repeat</class></pyref> property. If the sound is too long for the element,
	it is clipped once the element has been spoken.</doc:item>
	<doc:item><lit>auto</lit>: The sound of the parent element continues to play (it is not restarted,
	which would have been the case if this property had been inherited).</doc:item>
	<doc:item><lit>none</lit>: This keyword means that there is silence. The sound of the parent element (if any)
	is silent during the current element and continues after the current element.</doc:item>
	</doc:ulist>
	"""
	name = "play-during"

class azimuth(prop):
	"""
	<doc:par>This property is used for spatial audio. Values have the following meaning:</doc:par>
	<doc:ulist>
	<doc:item><lit><rep>angle</rep></lit>: Position is described in terms of an angle within the range <lit>-360deg</lit>
	to <lit>360deg</lit>. The value <lit>0deg</lit> means directly ahead in the center of the sound stage.
	<lit>90deg</lit> is to the right, <lit>180deg</lit> behind, and <lit>270deg</lit> (or, equivalently and more conveniently,
	<lit>-90deg</lit>) to the left.</doc:item>
	<doc:item><lit>left-side</lit>: Same as <lit>270deg</lit>. With <lit>behind</lit>, <lit>270deg</lit> (i.e. <lit>behind left-side</lit>).</doc:item>
	<doc:item><lit>far-left</lit>: Same as <lit>300deg</lit>. With <lit>behind</lit>, <lit>240deg</lit>.</doc:item>
	<doc:item><lit>left</lit>: Same as <lit>320deg</lit>. With <lit>behind</lit>, <lit>220deg</lit>.</doc:item>
	<doc:item><lit>center-left</lit>: Same as <lit>340deg</lit>. With <lit>behind</lit>, <lit>200deg</lit>.</doc:item>
	<doc:item><lit>center</lit>: Same as <lit>0deg</lit>. With <lit>behind</lit>, <lit>180deg</lit>.</doc:item>
	<doc:item><lit>center-right</lit>: Same as <lit>20deg</lit>. With <lit>behind</lit>, <lit>160deg</lit>.</doc:item>
	<doc:item><lit>right</lit>: Same as <lit>40deg</lit>. With <lit>behind</lit>, <lit>140deg</lit>.</doc:item>
	<doc:item><lit>far-right</lit>: Same as <lit>60deg</lit>. With <lit>behind</lit>, <lit>120deg</lit>.</doc:item>
	<doc:item><lit>right-side</lit>: Same as <lit>90deg</lit>. With <lit>behind</lit>, <lit>90deg</lit>.</doc:item>
	<doc:item><lit>leftwards</lit>: Moves the sound to the left, relative to the current angle. More precisely,
	subtracts 20 degrees. Arithmetic is carried out modulo 360 degrees. Note that <lit>leftwards</lit> is more
	accurately described as <z>turned counter-clockwise</z>, since it always subtracts 20 degrees, even if the
	inherited azimuth is already behind the listener (in which case the sound actually appears to move to the right).</doc:item>
	<doc:item><lit>rightwards</lit>: Moves the sound to the right, relative to the current angle. More precisely, adds 20 degrees.
	See <lit>leftwards</lit> for arithmetic.</doc:item>
	</doc:ulist>
	"""

class elevation(prop):
	"""
	<doc:par>This property is used for spatial audio. Values have the following meaning:</doc:par>
	<doc:ulist>
	<doc:item><lit><rep>angle</rep></lit>: Specifies the elevation as an angle,
	between <lit>-90deg</lit> and <lit>90deg</lit>. <lit>0deg</lit> means on the forward horizon, which loosely
	means level with the listener. <lit>90deg</lit> means directly overhead and <lit>-90deg</lit> means directly below.</doc:item>
	<doc:item><lit>below</lit>: Same as <lit>-90deg</lit>.</doc:item>
	<doc:item><lit>level</lit>: Same as <lit>0deg</lit>.</doc:item>
	<doc:item><lit>above</lit>: Same as <lit>90deg</lit>.</doc:item>
	<doc:item><lit>higher</lit>: Adds 10 degrees to the current elevation.</doc:item>
	<doc:item><lit>lower</lit>: Subtracts 10 degrees from the current elevation.</doc:item>
	</doc:ulist>
	"""

class speech_rate(prop):
	"""
	<doc:par>This property specifies the speaking rate. Note that both absolute and relative
	keyword values are allowed (compare with <pyref class="font_size"><class>font_size</class></pyref>).
	Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>number</rep></lit>: Specifies the speaking rate in words per minute,
	a quantity that varies somewhat by language but is nevertheless widely supported by speech synthesizers.</doc:item>
	<doc:item><lit>x-slow</lit>: Same as 80 words per minute.</doc:item>
	<doc:item><lit>slow</lit>: Same as 120 words per minute.</doc:item>
	<doc:item><lit>medium</lit>: Same as 180&ndash;200 words per minute.</doc:item>
	<doc:item><lit>fast</lit>: Same as 300 words per minute.</doc:item>
	<doc:item><lit>x-fast</lit>: Same as 500 words per minute.</doc:item>
	<doc:item><lit>faster</lit>: Adds 40 words per minute to the current speech rate.</doc:item>
	<doc:item><lit>slower</lit>: Subtracts 40 words per minutes from the current speech rate.</doc:item>
	</doc:ulist>
	"""
	name = "speech-rate"

class voice_family(prop):
	"""
	<doc:par>The value is a comma-separated, prioritized list of voice family names
	(compare with <pyref class="font_family"><class>font-family</class></pyref>).
	Values have the following meanings:</doc:par>
	
	<doc:ulist>
	<doc:item><lit><rep>generic-voice</rep></lit>: Values are voice families.
	Possible values are <lit>male</lit>, <lit>female</lit>, and <lit>child</lit>.</doc:item>
	<doc:item><lit><rep>specific-voice</rep></lit>: Values are specific instances
	(e.g., <lit>comedian</lit>, <lit>trinoids</lit>, <lit>carlos</lit>, <lit>lani</lit>).</doc:item>
	</doc:ulist>
	"""
	name = "voice-family"

class pitch(prop):
	"""
	<doc:par>Specifies the average pitch (a frequency) of the speaking voice. The average pitch
	of a voice depends on the voice family. For example, the average pitch for a standard male voice
	is around 120Hz, but for a female voice, it's around 210Hz.</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>frequency</rep></lit>: Specifies the average pitch of the speaking voice in hertz (Hz).</doc:item>
	<doc:item><lit>x-low</lit>, <lit>low</lit>, <lit>medium</lit>, <lit>high</lit>, <lit>x-high</lit>: These values do not map
	to absolute frequencies since these values depend on the voice family. User agents should map these values to appropriate
	frequencies based on the voice family and user environment. However, user agents must map these values in order (i.e.,
	<lit>x-low</lit> is a lower frequency than <lit>low</lit>, etc.).</doc:item>
	</doc:ulist>
	"""

class pitch_range(prop):
	"""
	<doc:par>Specifies variation in average pitch. The perceived pitch of a human voice is determined by the fundamental frequency
	and typically has a value of 120Hz for a male voice and 210Hz for a female voice. Human languages are spoken with varying
	inflection and pitch; these variations convey additional meaning and emphasis. Thus, a highly animated voice, i.e., one
	that is heavily inflected, displays a high pitch range. This property specifies the range over which these variations
	occur, i.e., how much the fundamental frequency may deviate from the average pitch.</doc:par>

	<doc:par>Values have the following meanings:</doc:par>
	<doc:ulist>
	<doc:item><lit><rep>number</rep></lit>: A value between <lit>0</lit> and <lit>100</lit>. A pitch range of
	<lit>0</lit> produces a flat, monotonic voice. A pitch range of <lit>50</lit> produces normal inflection.
	Pitch ranges greater than <lit>50</lit> produce animated voices.</doc:item>
	</doc:ulist>
	"""
	name = "pitch-range"

class stress(prop):
	"""
	<doc:par>Specifies the height of <z>local peaks</z> in the intonation contour of a voice.
	For example, English is a stressed language, and different parts of a sentence are assigned primary, secondary,
	or tertiary stress. The value of <class>stress</class> controls the amount of inflection that results from these
	stress markers. This property is a companion to the <pyref class="pitch_range"><class>pitch-range</class></pyref>
	property and is provided to allow developers to exploit higher-end auditory displays.</doc:par>

	<doc:par>Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>number</rep></lit>: A value, between <lit>0</lit> and <lit>100</lit>. The meaning of values
	depends on the language being spoken. For example, a level of <lit>50</lit> for a standard, English-speaking
	male voice (average pitch = 122Hz), speaking with normal intonation and emphasis would have a different meaning
	than <lit>50</lit> for an Italian voice.</doc:item>
	</doc:ulist>
	"""

class richness(prop):
	"""
	<doc:par>Specifies the richness, or brightness, of the speaking voice. A rich voice will <z>carry</z> in a large room,
	a smooth voice will not. (The term <z>smooth</z> refers to how the wave form looks when drawn.)</doc:par>

	<doc:par>Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit><rep>number</rep></lit>: A value between <lit>0</lit> and <lit>100</lit>. The higher the value,
	the more the voice will carry. A lower value will produce a soft, mellifluous voice.</doc:item>
	</doc:ulist>
	"""

class speak_punctuation(prop):
	"""
	<doc:par>This property specifies how punctuation is spoken. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>code</lit>: Punctuation such as semicolons, braces, and so on are to be spoken literally.</doc:item>
	<doc:item><lit>none</lit>: Punctuation is not to be spoken, but instead rendered naturally as various pauses.</doc:item>
	</doc:ulist>
	"""
	name = "speak-punctuation"

class speak_numeral(prop):
	"""
	<doc:par>This property controls how numerals are spoken. Values have the following meanings:</doc:par>

	<doc:ulist>
	<doc:item><lit>digits</lit>: Speak the numeral as individual digits. Thus, <lit>237</lit> is spoken <z>Two Three Seven</z>.</doc:item>
	<doc:item><lit>continuous</lit>: Speak the numeral as a full number. Thus,
	<lit>237</lit> is spoken <z>Two hundred thirty seven</z>. Word representations are language-dependent.</doc:item>
	</doc:ulist>
	"""
	name = "speak-numeral"

class filter(prop):
	"""
	<doc:par>This property is an <app>Internet Explorer</app> extensions for image processing filters.</doc:par>
	"""

class _moz_opacity(prop):
	"""
	<doc:par>This property is an <app>Mozilla</app> extension and specifies the opacity of the element.</doc:par>
	"""
	name = "-moz-opacity"

# register all the classes we've defined so far
namespace = xsc.Namespace("css", "http://www.w3.org/TR/REC-CSS2", vars())
