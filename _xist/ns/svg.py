#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 2002 by Walter Dörwald
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
<par>An &xist; module that contains definitions for the
<link href="http://www.w3.org/TR/SVG/">&svg;</link> 1.0 definition.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, utils
from ll.xist.ns import xml

class DocTypeSVG10(xsc.DocType):
	"""
	document type for SVG 1.0
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"')

# common attributes types
class BaselineShiftValueAttr(xsc.TextAttr): pass
class BooleanAttr(xsc.TextAttr): values = ("false", "true")
class ClassListAttr(xsc.TextAttr): pass
class ClipValueAttr(xsc.TextAttr): pass
class ClipPathValueAttr(xsc.TextAttr): pass
class ClipFillRuleAttr(xsc.TextAttr): values = ("nonzero", "evenodd", "inherit")
class ContentTypeAttr(xsc.TextAttr): pass
class CoordinateAttr(xsc.TextAttr): pass
class CoordinatesAttr(xsc.TextAttr): pass
class CursorValueAttr(xsc.TextAttr): pass
class EnableBackgroundValueAttr(xsc.TextAttr): pass
class ExtensionListAttr(xsc.TextAttr): pass
class FeatureListAttr(xsc.TextAttr): pass
class FilterValueAttr(xsc.TextAttr): pass
class FontFamilyValueAttr(xsc.TextAttr): pass
class FontSizeValueAttr(xsc.TextAttr): pass
class FontSizeAdjustValueAttr(xsc.TextAttr): pass
class GlyphOrientationHorizontalValueAttr(xsc.TextAttr): pass
class GlyphOrientationVerticalValueAttr(xsc.TextAttr): pass
class IntegerAttr(xsc.IntAttr): pass
class KerningValueAttr(xsc.TextAttr): pass
class LanguageCodeAttr(xsc.TextAttr): pass
class LanguageCodesAttr(xsc.TextAttr): pass
class LengthAttr(xsc.TextAttr): pass
class LengthsAttr(xsc.TextAttr): pass
class LinkTargetAttr(xsc.TextAttr): pass
class MarkerValueAttr(xsc.TextAttr): pass
class MaskValueAttr(xsc.TextAttr): pass
class MediaDescAttr(xsc.TextAttr): pass
class NumberAttr(xsc.TextAttr): pass
class NumberOptionalNumberAttr(xsc.TextAttr): pass
class NumberOrPercentageAttr(xsc.TextAttr): pass
class NumbersAttr(xsc.TextAttr): pass
class OpacityValueAttr(xsc.TextAttr): pass
class PaintAttr(xsc.TextAttr): pass
class PathDataAttr(xsc.TextAttr): pass
class PointsAttr(xsc.TextAttr): pass
class PreserveAspectRatioSpecAttr(xsc.TextAttr): pass
class ScriptAttr(xsc.TextAttr): pass
class SpacingValueAttr(xsc.TextAttr): pass
class StrokeDashArrayValueAttr(xsc.TextAttr): pass
class StrokeDashOffsetValueAttr(xsc.TextAttr): pass
class StrokeMiterLimitValueAttr(xsc.TextAttr): pass
class StrokeWidthValueAttr(xsc.TextAttr): pass
class SVGColorAttr(xsc.TextAttr): pass
class TextDecorationValueAttr(xsc.TextAttr): pass
class TransformListAttr(xsc.TextAttr): pass
class ViewBoxSpecAttr(xsc.TextAttr): pass
class StructuredTextAttr(xsc.TextAttr): pass

# common attributes sets
class stdattrs(xsc.Element.Attrs):
	"All elements have an ID."
	class id(xsc.IDAttr): "document-wide unique id"

class testattrs(xsc.Element.Attrs):
	"Common attributes to check for system capabilities"
	class requiredFeatures(FeatureListAttr): pass
	class requiredExtensions(ExtensionListAttr): pass
	class systemLanguage(LanguageCodesAttr): pass

class graphicelementevents(xsc.Element.Attrs):
	class onfocusin(ScriptAttr): pass
	class onfocusout(ScriptAttr): pass
	class onactivate(ScriptAttr): pass
	class onclick(ScriptAttr): pass
	class onmousedown(ScriptAttr): pass
	class onmouseup(ScriptAttr): pass
	class onmouseover(ScriptAttr): pass
	class onmousemove(ScriptAttr): pass
	class onmouseout(ScriptAttr): pass
	class onload(ScriptAttr): pass

class documentevents(xsc.Element.Attrs):
	class onunload(ScriptAttr): pass
	class onabort(ScriptAttr): pass
	class onerror(ScriptAttr): pass
	class onresize(ScriptAttr): pass
	class onscroll(ScriptAttr): pass
	class onzoom(ScriptAttr): pass

class animationevents(xsc.Element.Attrs):
	class onbegin(ScriptAttr): pass
	class onend(ScriptAttr): pass
	class onrepeat(ScriptAttr): pass

class presentationattributescolor(xsc.Element.Attrs):
	"These presentation attributes have to do with specifying color."
	class color(xsc.ColorAttr): pass
	class color_interpolation(xsc.TextAttr):
		xmlname = "color-interpolation"
		values = ("auto", "sRGB", "linearRGB", "inherit")
	class color_rendering(xsc.TextAttr):
		xmlname = "color-rendering"
		values = ("auto", "optimizeSpeed", "optimizeQuality", "inherit")

class presentationattributescontainers(xsc.Element.Attrs):
	"These presentation attributes apply to container elements."
	class enable_background(EnableBackgroundValueAttr):
		xmlname = "enable-background"

class presentationattributesfeflood(xsc.Element.Attrs):
	"""These presentation attributes apply to <pyref class="feFlood"><class>feFlood</class></pyref> elements."""
	class flood_color(SVGColorAttr): xmlname = "flood-color"
	class flood_opacity(OpacityValueAttr): xmlname = "flood-opacity"

class presentationattributesfillstroke(xsc.Element.Attrs):
	"These presentation attributes apply to filling and stroking operations."
	class fill(PaintAttr): pass
	class fill_opacity(OpacityValueAttr): xmlname = "fill-opacity"
	class fill_rule(ClipFillRuleAttr): xmlname = "fill-rule"
	class stroke(PaintAttr): pass
	class stroke_dasharray(StrokeDashArrayValueAttr): xmlname = "stroke-dasharray"
	class stroke_dashoffset(StrokeDashOffsetValueAttr): xmlname = "stroke-dashoffset"
	class stroke_linecap(xsc.TextAttr):
		xmlname = "stroke-linecap"
		values = ("butt", "round", "square", "inherit")
	class stroke_linejoin(xsc.TextAttr):
		xmlname = "stroke-linejoin"
		values = ("miter", "round", "bevel", "inherit")
	class stroke_miterlimit(StrokeMiterLimitValueAttr): xmlname = "stroke-miterlimit"
	class stroke_opacity(OpacityValueAttr): xmlname = "stroke-opacity"
	class stroke_width(StrokeWidthValueAttr): xmlname = "stroke-width"

class presentationattributesfilterprimitives(xsc.Element.Attrs):
	"These presentation attributes apply to filter primitives."
	class color_interpolation_filters(xsc.TextAttr):
		xmlname = "color-interpolation-filters"
		values = ("auto", "sRGB", "linearRGB", "inherit")

class presentationattributesfontspecification(xsc.Element.Attrs):
	"These presentation attributes have to do with selecting a font to use."
	class font_family(FontFamilyValueAttr): xmlname = "font-family"
	class font_size(FontSizeValueAttr): xmlname = "font-size"
	class font_size_adjust(FontSizeAdjustValueAttr): xmlname = "font-size-adjust"
	class font_stretch(xsc.TextAttr):
		xmlname = "font-stretch"
		values = ("normal", "wider", "narrower", "ultra-condensed", "extra-condensed", "condensed",
		          "semi-condensed", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded",
		          "inherit")
	class font_style(xsc.TextAttr):
		xmlname = "font-style"
		values = ("normal", "italic", "oblique", "inherit")
	class font_variant(xsc.TextAttr):
		xmlname = "font-variant"
		values = ("normal", "small-caps", "inherit")
	class font_weight(xsc.TextAttr):
		xmlname = "font-weight"
		values = ("normal", "bold", "bolder", "lighter", 100, 200, 300, 400, 500, 600, 700, 800, 900, "inherit")

class presentationattributesgradients(xsc.Element.Attrs):
	"""These presentation attributes apply to gradient <pyref class="stop"><class>stop</class></pyref>."""
	class stop_color(SVGColorAttr): xmlname = "stop-color"
	class stop_opacity(OpacityValueAttr): xmlname = "stop-opacity"

class presentationattributesgraphics(xsc.Element.Attrs):
	"""These presentation attributes apply to graphic elements."""
	class clip_path(ClipPathValueAttr): xmlname = "clip-path"
	class clip_rule(ClipFillRuleAttr): xmlname = "clip-rule"
	class cursor(CursorValueAttr): pass
	class display(xsc.TextAttr):
		values = ("inline", "block", "list-item", "run-in", "compact", "marker", "table", "inline-table",
		          "table-row-group", "table-header-group", "table-footer-group", "table-row", "table-column-group",
		          "table-column", "table-cell", "table-caption", "none", "inherit")
	class filter(FilterValueAttr): pass
	class image_rendering(xsc.TextAttr):
		xmlname = "image-rendering"
		values = ("auto", "optimizeSpeed", "optimizeQuality", "inherit")
	class mask(MaskValueAttr): pass
	class opacity(OpacityValueAttr): pass
	class pointer_events(xsc.TextAttr):
		xmlname = "pointer-events"
		values = ("visiblePainted", "visibleFill", "visibleStroke", "visible", "painted", "fill", "stroke",
		          "all", "none", "inherit")
	class shape_rendering(xsc.TextAttr):
		xmlname = "shape-rendering"
		values = ("auto", "optimizeSpeed", "crispEdges", "geometricPrecision", "inherit")
	class text_rendering(xsc.TextAttr):
		xmlname = "text-rendering"
		values = ("auto", "optimizeSpeed", "optimizeLegibility", "geometricPrecision", "inherit")
	class visibility(xsc.TextAttr):
		values = ("visible", "hidden", "inherit")

class presentationattributesimages(xsc.Element.Attrs):
	"""These presentation attributes apply to <pyref class="image"><class>image</class></pyref> elements."""
	class color_profile(xsc.TextAttr): xmlname = "color-profile"

class presentationattributeslightingeffects(xsc.Element.Attrs):
	"""These presentation attributes apply to <pyref class="feDiffuseLighting"><class>feDiffuseLighting</class></pyref>
	and <pyref class="feSpecularLighting"><class>feSpecularLighting</class></pyref> elements."""
	class lighting_color(SVGColorAttr): xmlname = "lighting-color"

class presentationattributesmarkers(xsc.Element.Attrs):
	"""These presentation attributes apply to marker operations."""
	class marker_start(MarkerValueAttr): xmlname = "marker-start"
	class marker_mid(MarkerValueAttr): xmlname = "marker-mid"
	class marker_end(MarkerValueAttr): xmlname = "marker-end"

class presentationattributestextcontentelements(xsc.Element.Attrs):
	"""These presentation attributes apply to text content elements."""
	class alignment_baseline(xsc.TextAttr):
		xmlname = "alignment-baseline"
		values = ("baseline", "top", "before-edge", "text-top", "text-before-edge", "middle", "bottom", "after-edge",
		          "text-bottom", "text-after-edge", "ideographic", "lower", "hanging", "mathematical", "inherit")
	class baseline_shift(BaselineShiftValueAttr): xmlname = "baseline-shift"
	class direction(xsc.TextAttr): values = ("ltr", "rtl", "inherit")
	class dominant_baseline(xsc.TextAttr):
		xmlname = "dominant-baseline"
		values = ("auto", "autosense-script", "no-change", "reset", "ideographic", "lower", "hanging", "mathematical", "inherit")
	class glyph_orientation_horizontal(GlyphOrientationHorizontalValueAttr): xmlname = "glyph-orientation-horizontal"
	class glyph_orientation_vertical(GlyphOrientationVerticalValueAttr): xmlname = "glyph-orientation-vertical"
	class kerning(KerningValueAttr): pass
	class letter_spacing(SpacingValueAttr): xmlname = "letter-spacing"
	class text_anchor(xsc.TextAttr):
		xmlname = "text-anchor"
		values = ("start", "middle", "end", "inherit")
	class text_decoration(TextDecorationValueAttr): xmlname = "text-decoration"
	class unicode_bidi(xsc.TextAttr):
		xmlname = "unicode-bidi"
		values = ("normal", "embed", "bidi-override", "inherit")
	class word_spacing(SpacingValueAttr): xmlname = "word-spacing"

class presentationattributestextelements(xsc.Element.Attrs):
	"""These presentation attributes apply to <pyref class="text"><class>text</class></pyref> elements."""
	class writing_mode(xsc.TextAttr):
		xmlname = "writing-mode"
		values = ("lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb", "inherit")

class presentationattributesviewports(xsc.Element.Attrs):
	"""These presentation attributes apply to elements that establish viewports."""
	class clip(ClipValueAttr): pass
	class overflow(xsc.TextAttr): values = ("visible", "hidden", "scroll", "auto", "inherit")

class presentationattributesall(
	presentationattributescolor,
	presentationattributescontainers,
	presentationattributesfeflood,
	presentationattributesfillstroke,
	presentationattributesfilterprimitives,
	presentationattributesfontspecification,
	presentationattributesgradients,
	presentationattributesgraphics,
	presentationattributesimages,
	presentationattributeslightingeffects,
	presentationattributesmarkers,
	presentationattributestextcontentelements,
	presentationattributestextelements,
	presentationattributesviewports):
	"""This represents the complete list of presentation attributes."""

class filterprimitiveattributes(xsc.Element.Attrs):
	class x(CoordinateAttr): pass
	class y(CoordinateAttr): pass
	class width(LengthAttr): pass
	class height(LengthAttr): pass
	class result(xsc.TextAttr): pass

class filterprimitiveattributeswithin(filterprimitiveattributes):
	class in_(xsc.TextAttr): xmlname = "in"

class componenttransferfunctionattributes(xsc.Element.Attrs):
	class type(xsc.TextAttr):
		values = ("identity", "table", "discrete", "linear", "gamma")
		required = True
	class tableValues(xsc.TextAttr): pass
	class slope(NumberAttr): pass
	class intercept(NumberAttr): pass
	class amplitude(NumberAttr): pass
	class exponent(NumberAttr): pass
	class offset(NumberAttr): pass

class animattributeattrs(xsc.Element.Attrs):
	class attributeName(xsc.TextAttr): required = True
	class attributeType(xsc.TextAttr): pass

class animtimingattrs(xsc.Element.Attrs):
	class begin(xsc.TextAttr): pass
	class dur(xsc.TextAttr): pass
	class end(xsc.TextAttr): pass
	class min(xsc.TextAttr): pass
	class max(xsc.TextAttr): pass
	class restart(xsc.TextAttr): values = ("always", "never", "whenNotActive")
	class repeatCount(xsc.TextAttr): pass
	class repeatDur(xsc.TextAttr): pass
	class fill(xsc.TextAttr): values = ("remove", "freeze")

class animvalueattrs(xsc.Element.Attrs):
	class calcMode(xsc.TextAttr): values = ("discrete", "linear", "paced", "spline")
	class values(xsc.TextAttr): pass
	class keyTimes(xsc.TextAttr): pass
	class keySplines(xsc.TextAttr): pass
	class from_(xsc.TextAttr): xmlname = "from"
	class to(xsc.TextAttr): pass
	class by(xsc.TextAttr): pass

class animadditionattrs(xsc.Element.Attrs):
	class additive(xsc.TextAttr): values = ("replace", "sum")
	class accumulate(xsc.TextAttr): values = ("none", "sum")

# And now for something completely different: the elements
class svg(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents, documentevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class viewBox(ViewBoxSpecAttr): pass
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass
		class zoomAndPan(xsc.TextAttr): values = ("disable", "magnify")
		class version(NumberAttr): default = "1.0"
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class contentScriptType(ContentTypeAttr): pass
		class contentStyleType(ContentTypeAttr): pass

class g(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass

class defs(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass

class desc(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class content(StructuredTextAttr): pass

class title(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class content(StructuredTextAttr): pass

class symbol(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class viewBox(ViewBoxSpecAttr): pass
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass

class use(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass

class image(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesgraphics,
		presentationattributesimages, presentationattributesviewports, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): required = True
		class height(LengthAttr): required = True
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass

class switch(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass

class style(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class type(ContentTypeAttr): required = True
		class media(MediaDescAttr): pass
		class title(xsc.TextAttr): pass

class path(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, presentationattributesmarkers, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class d(PathDataAttr): required = True
		class pathLength(NumberAttr): pass

class rect(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): required = True
		class height(LengthAttr): required = True
		class rx(LengthAttr): pass
		class ry(LengthAttr): pass

class circle(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class cx(CoordinateAttr): pass
		class cy(CoordinateAttr): pass
		class r(LengthAttr): required = True

class ellipse(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class cx(CoordinateAttr): pass
		class cy(CoordinateAttr): pass
		class rx(LengthAttr): required = True
		class ry(LengthAttr): required = True

class line(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, presentationattributesmarkers, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x1(CoordinateAttr): pass
		class y1(CoordinateAttr): pass
		class x2(CoordinateAttr): pass
		class y2(CoordinateAttr): pass

class polyline(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, presentationattributesmarkers, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class points(PointsAttr): required = True

class polygon(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesgraphics, presentationattributesmarkers, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class points(PointsAttr): required = True

class text(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, presentationattributestextelements, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x(CoordinatesAttr): pass
		class y(CoordinatesAttr): pass
		class dx(LengthAttr): pass
		class dy(LengthAttr): pass
		class rotate(NumbersAttr): pass
		class textLength(LengthAttr): pass
		class lengthAdjust(xsc.TextAttr): values = ("spacing", "spacingAndGlyphs")

class tspan(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class x(CoordinatesAttr): pass
		class y(CoordinatesAttr): pass
		class dx(LengthAttr): pass
		class dy(LengthAttr): pass
		class rotate(NumbersAttr): pass
		class textLength(LengthAttr): pass
		class lengthAdjust(xsc.TextAttr): values = ("spacing", "spacingAndGlyphs")

class tref(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class x(CoordinatesAttr): pass
		class y(CoordinatesAttr): pass
		class dx(LengthAttr): pass
		class dy(LengthAttr): pass
		class rotate(NumbersAttr): pass
		class textLength(LengthAttr): pass
		class lengthAdjust(xsc.TextAttr): values = ("spacing", "spacingAndGlyphs")

class textPath(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class startOffset(LengthAttr): pass
		class textLength(LengthAttr): pass
		class lengthAdjust(xsc.TextAttr): values = ("spacing", "spacingAndGlyphs")
		class method(xsc.TextAttr): values = ("align", "stretch")
		class spacing(xsc.TextAttr): values = ("auto", "exact")

class altGlyph(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, graphicelementevents):
		class glyphRef(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class x(CoordinatesAttr): pass
		class y(CoordinatesAttr): pass
		class dx(LengthAttr): pass
		class dy(LengthAttr): pass
		class rotate(NumbersAttr): pass

class altGlyphDef(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		pass

class altGlyphItem(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		pass

class glyphRef(xsc.Element):
	empty = True
	class Attrs(stdattrs, presentationattributesfontspecification):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class glyphRef(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class x(NumberAttr): pass
		class y(NumberAttr): pass
		class dx(NumberAttr): pass
		class dy(NumberAttr): pass

class marker(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class viewBox(ViewBoxSpecAttr): pass
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass
		class refX(CoordinateAttr): pass
		class refY(CoordinateAttr): pass
		class markerUnits(xsc.TextAttr): values = ("strokeWidth", "userSpaceOnUse")
		class markerWidth(LengthAttr): pass
		class markerHeight(LengthAttr): pass
		class orient(xsc.TextAttr): pass

class color_profile(xsc.Element):
	xmlname = "color-profile"
	empty = False
	class Attrs(stdattrs):
		class local(xsc.TextAttr): pass
		class name(xsc.TextAttr): required = True
		class rendering_intent(xsc.TextAttr):
			xmlname = "rendering-intent"
			values = ("auto", "perceptual", "relative-colorimetric", "saturation", "absolute-colorimetric")

class linearGradient(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesgradients):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class gradientUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class gradientTransform(TransformListAttr): pass
		class x1(CoordinateAttr): pass
		class y1(CoordinateAttr): pass
		class x2(CoordinateAttr): pass
		class y2(CoordinateAttr): pass
		class spreadMethod(xsc.TextAttr): values = ("pad", "reflect", "repeat")

class radialGradient(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesgradients):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class gradientUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class gradientTransform(TransformListAttr): pass
		class cx(CoordinateAttr): pass
		class cy(CoordinateAttr): pass
		class r(LengthAttr): pass
		class fx(CoordinateAttr): pass
		class fy(CoordinateAttr): pass
		class spreadMethod(xsc.TextAttr): values = ("pad", "reflect", "repeat")

class stop(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesgradients):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class offset(NumberOrPercentageAttr): required = True

class pattern(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class viewBox(ViewBoxSpecAttr): pass
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass
		class patternUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class patternContentUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class patternTransform(TransformListAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass

class clipPath(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributescolor, presentationattributesfillstroke,
		presentationattributesfontspecification, presentationattributesgraphics,
		presentationattributestextcontentelements, presentationattributestextelements):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class clipPathUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")

class mask(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class maskUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class maskContentUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass

class filter(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class filterUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class primitiveUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class filterRes(NumberOptionalNumberAttr): pass

class filter(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class filterUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class primitiveUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class filterRes(NumberOptionalNumberAttr): pass

class feDistantLight(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class azimuth(NumberAttr): pass
		class elevation(NumberAttr): pass

class fePointLight(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class x(NumberAttr): pass
		class y(NumberAttr): pass
		class z(NumberAttr): pass

class feSpotLight(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class x(NumberAttr): pass
		class y(NumberAttr): pass
		class z(NumberAttr): pass
		class pointsAtX(NumberAttr): pass
		class pointsAtY(NumberAttr): pass
		class pointsAtZ(NumberAttr): pass
		class specularExponent(NumberAttr): pass
		class limitingConeAngle(NumberAttr): pass

class feBlend(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class in2(xsc.TextAttr): required = True
		class mode(xsc.TextAttr): values = ("normal", "multiply", "screen", "darken", "lighten")

class feColorMatrix(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class type(xsc.TextAttr): values = ("matrix", "saturate", "hueRotate", "luminanceToAlpha")
		class values(xsc.TextAttr): pass

class feComponentTransfer(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		pass

class feFuncR(xsc.Element):
	empty = False
	class Attrs(stdattrs, componenttransferfunctionattributes):
		pass

class feFuncG(xsc.Element):
	empty = False
	class Attrs(stdattrs, componenttransferfunctionattributes):
		pass

class feFuncB(xsc.Element):
	empty = False
	class Attrs(stdattrs, componenttransferfunctionattributes):
		pass

class feFuncA(xsc.Element):
	empty = False
	class Attrs(stdattrs, componenttransferfunctionattributes):
		pass

class feComposite(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class in2(xsc.TextAttr): required = True
		class operator(xsc.TextAttr): values = ("over", "in", "out", "atop", "xor", "arithmetic")
		class k1(NumberAttr): pass
		class k2(NumberAttr): pass
		class k3(NumberAttr): pass
		class k4(NumberAttr): pass

class feConvolveMatrix(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class order(NumberOptionalNumberAttr): required = True
		class kernelMatrix(xsc.TextAttr): required = True
		class divisor(NumberAttr): pass
		class bias(NumberAttr): pass
		class targetX(xsc.IntAttr): pass
		class targetY(xsc.IntAttr): pass
		class edgeMode(xsc.TextAttr): values = ("duplicate", "wrap", "none")
		class kernelUnitLength(NumberOptionalNumberAttr): pass
		class preserveAlpha(BooleanAttr): pass

class feDiffuseLighting(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesfilterprimitives, presentationattributeslightingeffects, filterprimitiveattributeswithin):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class surfaceScale(NumberAttr): pass
		class diffuseConstant(NumberAttr): pass
		class kernelUnitLength(NumberOptionalNumberAttr): pass

class feDisplacementMap(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class in2(xsc.TextAttr): required = True
		class scale(NumberAttr): pass
		class xChannelSelector(xsc.TextAttr): values = ("R", "G", "B", "A")
		class yChannelSelector(xsc.TextAttr): values = ("R", "G", "B", "A")

class feFlood(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesfeflood, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass

class feGaussianBlur(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class stdDeviation(NumberOptionalNumberAttr): pass

class feImage(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall, filterprimitiveattributes):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass

class feMerge(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributes):
		pass

class feMergeNode(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class in_(xsc.TextAttr): xmlname = "in"

class feMorphology(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class operator(xsc.TextAttr): values = ("erode", "dilate")
		class radius(NumberOptionalNumberAttr): pass

class feOffset(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		class dx(NumberAttr): pass
		class dy(NumberAttr): pass

class feSpecularLighting(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributescolor, presentationattributesfilterprimitives, presentationattributeslightingeffects, filterprimitiveattributeswithin):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class surfaceScale(NumberAttr): pass
		class specularConstant(NumberAttr): pass
		class specularExponent(NumberAttr): pass
		class kernelUnitLength(NumberOptionalNumberAttr): pass

class feTile(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributeswithin):
		pass

class feTurbulence(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesfilterprimitives, filterprimitiveattributes):
		class baseFrequency(NumberOptionalNumberAttr): pass
		class numOctaves(xsc.IntAttr): pass
		class seed(NumberAttr): pass
		class stitchTiles(xsc.TextAttr): values = ("stitch", "noStitch")
		class type(xsc.TextAttr): values = ("fractalNoise", "turbulence")

class cursor(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass

class a(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class target(LinkTargetAttr): pass

class view(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class viewBox(ViewBoxSpecAttr): pass
		class preserveAspectRatio(PreserveAspectRatioSpecAttr): pass
		class zoomAndPan(xsc.TextAttr): values = ("disable", "magnify")
		class viewTarget(xsc.TextAttr): pass

class script(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class type(ContentTypeAttr): required = True

class animate(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, animationevents, animattributeattrs, animtimingattrs, animvalueattrs, animadditionattrs):
		class externalResourcesRequired(BooleanAttr): pass

class set(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, animationevents, animattributeattrs, animtimingattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class to(xsc.TextAttr): pass

class animateMotion(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, animationevents, animtimingattrs, animadditionattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class calcMode(xsc.TextAttr): values = ("discrete", "linear", "paced", "spline")
		class values(xsc.TextAttr): pass
		class keyTimes(xsc.TextAttr): pass
		class keySplines(xsc.TextAttr): pass
		class from_(xsc.TextAttr): xmlname = "from"
		class to(xsc.TextAttr): pass
		class by(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass
		class keyPoints(xsc.TextAttr): pass
		class rotate(xsc.TextAttr): pass
		class origin(xsc.TextAttr): pass

class mpath(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		class externalResourcesRequired(BooleanAttr): pass

class animateColor(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, animationevents, animattributeattrs, animtimingattrs, animvalueattrs, animadditionattrs):
		class externalResourcesRequired(BooleanAttr): pass

class animateTransform(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, animationevents, animattributeattrs, animtimingattrs, animvalueattrs, animadditionattrs):
		class externalResourcesRequired(BooleanAttr): pass
		class type(xsc.TextAttr): values = ("translate", "scale", "rotate", "skewX", "skewY")

class font(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class horiz_origin_x(NumberAttr): xmlname = "horiz-origin-x"
		class horiz_origin_y(NumberAttr): xmlname = "horiz-origin-y"
		class horiz_adv_x(NumberAttr):
			xmlname = "horiz-adv-x"
			required = True
		class vert_origin_x(NumberAttr): xmlname = "vert-origin-x"
		class vert_origin_y(NumberAttr): xmlname = "vert-origin-y"
		class vert_adv_y(NumberAttr): xmlname = "vert-adv-y"

class glyph(xsc.Element):
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class unicode(xsc.TextAttr): pass
		class glyph_name(xsc.TextAttr): xmlname = "glyph-name"
		class d(PathDataAttr): pass
		class orientation(xsc.TextAttr): pass
		class arabic_form(xsc.TextAttr): xmlname = "arabic-form"
		class lang(LanguageCodesAttr): pass
		class horiz_adv_x(NumberAttr): xmlname = "horiz-adv-x"
		class vert_origin_x(NumberAttr): xmlname = "vert-origin-x"
		class vert_origin_y(NumberAttr): xmlname = "vert-origin-y"
		class vert_adv_y(NumberAttr): xmlname = "vert-adv-y"

class missing_glyph(xsc.Element):
	xmlname = "missing-glyph"
	empty = False
	class Attrs(stdattrs, presentationattributesall):
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class d(PathDataAttr): pass
		class horiz_adv_x(NumberAttr): xmlname = "horiz-adv-x"
		class vert_origin_x(NumberAttr): xmlname = "vert-origin-x"
		class vert_origin_y(NumberAttr): xmlname = "vert-origin-y"
		class vert_adv_y(NumberAttr): xmlname = "vert-adv-y"

class hkern(xsc.Element):
	empty = True
	class Attrs(stdattrs):
		class u1(xsc.TextAttr): pass
		class g1(xsc.TextAttr): pass
		class u2(xsc.TextAttr): pass
		class g2(xsc.TextAttr): pass
		class k(NumberAttr): required = True

class vkern(xsc.Element):
	empty = True
	class Attrs(stdattrs):
		class u1(xsc.TextAttr): pass
		class g1(xsc.TextAttr): pass
		class u2(xsc.TextAttr): pass
		class g2(xsc.TextAttr): pass
		class k(NumberAttr): required = True

class font_face(xsc.Element):
	xmlname = "font-face"
	empty = False
	class Attrs(stdattrs):
		class font_family(xsc.TextAttr): xmlname = "font-family"
		class font_style(xsc.TextAttr): xmlname = "font-style"
		class font_variant(xsc.TextAttr): xmlname = "font-variant"
		class font_weight(xsc.TextAttr): xmlname = "font-weight"
		class font_stretch(xsc.TextAttr): xmlname = "font-stretch"
		class font_size(xsc.TextAttr): xmlname = "font-size"
		class unicode_range(xsc.TextAttr): xmlname = "unicode-range"
		class units_per_em(NumberAttr): xmlname = "units-per-em"
		class panose_1(xsc.TextAttr): xmlname = "panose-1"
		class stemv(NumberAttr): pass
		class stemh(NumberAttr): pass
		class slope(NumberAttr): pass
		class cap_height(NumberAttr): xmlname = "cap-height"
		class x_height(NumberAttr): xmlname = "x-height"
		class accent_height(NumberAttr): xmlname = "accent-height"
		class ascent(NumberAttr): pass
		class descent(NumberAttr): pass
		class widths(xsc.TextAttr): pass
		class bbox(xsc.TextAttr): pass
		class ideographic(NumberAttr): pass
		class alphabetic(NumberAttr): pass
		class mathematical(NumberAttr): pass
		class hanging(NumberAttr): pass
		class v_ideographic(NumberAttr): xmlname = "v-ideographic"
		class v_alphabetic(NumberAttr): xmlname = "v-alphabetic"
		class v_mathematical(NumberAttr): xmlname = "v-mathematical"
		class v_hanging(NumberAttr): xmlname = "v-hanging"
		class underline_position(NumberAttr): xmlname = "underline-position"
		class underline_thickness(NumberAttr): xmlname = "underline-thickness"
		class strikethrough_position(NumberAttr): xmlname = "strikethrough-position"
		class strikethrough_thickness(NumberAttr): xmlname = "strikethrough-thickness"
		class overline_position(NumberAttr): xmlname = "overline-position"
		class overline_thickness(NumberAttr): xmlname = "overline-thickness"

class font_face_src(xsc.Element):
	xmlname = "font-face-src"
	empty = False
	class Attrs(stdattrs):
		pass

class font_face_uri(xsc.Element):
	xmlname = "font-face-uri"
	empty = False
	class Attrs(stdattrs):
		pass

class font_face_format(xsc.Element):
	xmlname = "font-face-format"
	empty = True
	class Attrs(stdattrs):
		class string(xsc.TextAttr): pass

class font_face_name(xsc.Element):
	xmlname = "font-face-name"
	empty = True
	class Attrs(stdattrs):
		class name(xsc.TextAttr): pass

class definition_src(xsc.Element):
	xmlname = "definition-src"
	empty = True
	class Attrs(stdattrs):
		pass

class metadata(xsc.Element):
	empty = False
	class Attrs(stdattrs):
		pass

class foreignObject(xsc.Element):
	empty = False
	class Attrs(stdattrs, testattrs, presentationattributesall, graphicelementevents):
		class externalResourcesRequired(BooleanAttr): pass
		class class_(ClassListAttr): xmlname = "class"
		class style(xsc.StyleAttr): pass
		class transform(TransformListAttr): pass
		class x(CoordinateAttr): pass
		class y(CoordinateAttr): pass
		class width(LengthAttr): required = True
		class height(LengthAttr): required = True
		class content(StructuredTextAttr): pass

# register all the classes we've defined so far
xmlns = xsc.Namespace("svg", "http://www.w3.org/2000/svg", vars())

