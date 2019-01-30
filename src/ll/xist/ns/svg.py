# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This is a namespace module implementing `SVG 1.1`__.

__ http://www.w3.org/TR/SVG11/
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.w3.org/2000/svg"


class DocTypeSVG11(xsc.DocType):
	"""
	document type for SVG 1.1
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"')


class alignment_baseline(xsc.Attrs):
	class alignment_baseline(xsc.TextAttr):
		xmlname = "alignment-baseline"
		values = ("auto", "baseline", "before-edge", "text-before-edge", "middle", "central", "after-edge", "text-after-edge", "ideographic", "alphabetic", "hanging", "mathematical", "inherit")


class baseline_shift(xsc.Attrs):
	class baseline_shift(xsc.TextAttr): xmlname = "baseline-shift"


class class_(xsc.Attrs):
	class class_(xsc.TextAttr): xmlname = "class"


class clip(xsc.Attrs):
	class clip(xsc.TextAttr): pass


class clip_path(xsc.Attrs):
	class clip_path(xsc.TextAttr): xmlname = "clip-path"


class clip_rule(xsc.Attrs):
	class clip_rule(xsc.TextAttr):
		xmlname = "clip-rule"
		values = ("nonzero", "evenodd", "inherit")


class color(xsc.Attrs):
	class color(xsc.ColorAttr): pass


class color_interpolation(xsc.Attrs):
	class color_interpolation(xsc.TextAttr):
		xmlname = "color-interpolation"
		values = ("auto", "sRGB", "linearRGB", "inherit")


class color_interpolation_filters(xsc.Attrs):
	class color_interpolation_filters(xsc.TextAttr):
		xmlname = "color-interpolation-filters"
		values = ("auto", "sRGB", "linearRGB", "inherit")


class color_profile2(xsc.Attrs):
	class color_profile(xsc.TextAttr): xmlname = "color-profile"


class color_rendering(xsc.Attrs):
	class color_rendering(xsc.TextAttr):
		xmlname = "color-rendering"
		values = ("auto", "optimizeSpeed", "optimizeQuality", "inherit")


class cursor2(xsc.Attrs):
	class cursor(xsc.TextAttr): pass


class direction(xsc.Attrs):
	class direction(xsc.TextAttr): values = ("ltr", "rtl", "inherit")


class display(xsc.Attrs):
	class display(xsc.TextAttr): values = ("inline", "block", "list-item", "run-in", "compact", "marker", "table", "inline-table", "table-row-group", "table-header-group", "table-footer-group", "table-row", "table-column-group", "table-column", "table-cell", "table-caption", "none", "inherit")


class dominant_baseline(xsc.Attrs):
	class dominant_baseline(xsc.TextAttr):
		xmlname = "dominant-baseline"
		values = ("auto", "use-script", "no-change", "reset-size", "ideographic", "alphabetic", "hanging", "mathematical", "central", "middle", "text-after-edge", "text-before-edge", "inherit")


class enable_background(xsc.Attrs):
	class enable_background(xsc.TextAttr): xmlname = "enable-background"


class externalResourcesRequired(xsc.Attrs):
	class externalResourcesRequired(xsc.TextAttr): values = ("false", "true")


class fill(xsc.Attrs):
	class fill(xsc.ColorAttr): pass


class fill_opacity(xsc.Attrs):
	class fill_opacity(xsc.TextAttr): xmlname = "fill-opacity"


class fill_rule(xsc.Attrs):
	class fill_rule(xsc.TextAttr):
		xmlname = "fill-rule"
		values = ("nonzero", "evenodd", "inherit")


class filter2(xsc.Attrs):
	class filter(xsc.TextAttr): pass


class flood_color(xsc.Attrs):
	class flood_color(xsc.ColorAttr): xmlname = "flood-color"


class flood_opacity(xsc.Attrs):
	class flood_opacity(xsc.TextAttr): xmlname = "flood-opacity"


class font_family(xsc.Attrs):
	class font_family(xsc.TextAttr): xmlname = "font-family"


class font_size(xsc.Attrs):
	class font_size(xsc.TextAttr): xmlname = "font-size"


class font_size_adjust(xsc.Attrs):
	class font_size_adjust(xsc.TextAttr): xmlname = "font-size-adjust"


class font_stretch(xsc.Attrs):
	class font_stretch(xsc.TextAttr):
		xmlname = "font-stretch"
		values = ("normal", "wider", "narrower", "ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded", "inherit")


class font_style(xsc.Attrs):
	class font_style(xsc.TextAttr):
		xmlname = "font-style"
		values = ("normal", "italic", "oblique", "inherit")


class font_variant(xsc.Attrs):
	class font_variant(xsc.TextAttr):
		xmlname = "font-variant"
		values = ("normal", "small-caps", "inherit")


class font_weight(xsc.Attrs):
	class font_weight(xsc.TextAttr):
		xmlname = "font-weight"
		values = ("normal", "bold", "bolder", "lighter", 100, 200, 300, 400, 500, 600, 700, 800, 900, "inherit")


class glyph_orientation_horizontal(xsc.Attrs):
	class glyph_orientation_horizontal(xsc.TextAttr): xmlname = "glyph-orientation-horizontal"


class glyph_orientation_vertical(xsc.Attrs):
	class glyph_orientation_vertical(xsc.TextAttr): xmlname = "glyph-orientation-vertical"


class id(xsc.Attrs):
	class id(xsc.IDAttr): pass


class image_rendering(xsc.Attrs):
	class image_rendering(xsc.TextAttr):
		xmlname = "image-rendering"
		values = ("auto", "optimizeSpeed", "optimizeQuality", "inherit")


class kerning(xsc.Attrs):
	class kerning(xsc.TextAttr): pass


class letter_spacing(xsc.Attrs):
	class letter_spacing(xsc.TextAttr): xmlname = "letter-spacing"


class lighting_color(xsc.Attrs):
	class lighting_color(xsc.ColorAttr): xmlname = "lighting-color"


class marker_end(xsc.Attrs):
	class marker_end(xsc.TextAttr): xmlname = "marker-end"


class marker_mid(xsc.Attrs):
	class marker_mid(xsc.TextAttr): xmlname = "marker-mid"


class marker_start(xsc.Attrs):
	class marker_start(xsc.TextAttr): xmlname = "marker-start"


class mask2(xsc.Attrs):
	class mask(xsc.TextAttr): pass


class onactivate(xsc.Attrs):
	class onactivate(xsc.TextAttr): pass


class onclick(xsc.Attrs):
	class onclick(xsc.TextAttr): pass


class onfocusin(xsc.Attrs):
	class onfocusin(xsc.TextAttr): pass


class onfocusout(xsc.Attrs):
	class onfocusout(xsc.TextAttr): pass


class onload(xsc.Attrs):
	class onload(xsc.TextAttr): pass


class onmousedown(xsc.Attrs):
	class onmousedown(xsc.TextAttr): pass


class onmousemove(xsc.Attrs):
	class onmousemove(xsc.TextAttr): pass


class onmouseout(xsc.Attrs):
	class onmouseout(xsc.TextAttr): pass


class onmouseover(xsc.Attrs):
	class onmouseover(xsc.TextAttr): pass


class onmouseup(xsc.Attrs):
	class onmouseup(xsc.TextAttr): pass


class opacity(xsc.Attrs):
	class opacity(xsc.TextAttr): pass


class overflow(xsc.Attrs):
	class overflow(xsc.TextAttr): values = ("visible", "hidden", "scroll", "auto", "inherit")


class pointer_events(xsc.Attrs):
	class pointer_events(xsc.TextAttr):
		xmlname = "pointer-events"
		values = ("visiblePainted", "visibleFill", "visibleStroke", "visible", "painted", "fill", "stroke", "all", "none", "inherit")


class requiredExtensions(xsc.Attrs):
	class requiredExtensions(xsc.TextAttr): pass


class requiredFeatures(xsc.Attrs):
	class requiredFeatures(xsc.TextAttr): pass


class shape_rendering(xsc.Attrs):
	class shape_rendering(xsc.TextAttr):
		xmlname = "shape-rendering"
		values = ("auto", "optimizeSpeed", "crispEdges", "geometricPrecision", "inherit")


class stop_color(xsc.Attrs):
	class stop_color(xsc.ColorAttr): xmlname = "stop-color"


class stop_opacity(xsc.Attrs):
	class stop_opacity(xsc.TextAttr): xmlname = "stop-opacity"


class stroke(xsc.Attrs):
	class stroke(xsc.ColorAttr): pass


class stroke_dasharray(xsc.Attrs):
	class stroke_dasharray(xsc.TextAttr): xmlname = "stroke-dasharray"


class stroke_dashoffset(xsc.Attrs):
	class stroke_dashoffset(xsc.TextAttr): xmlname = "stroke-dashoffset"


class stroke_linecap(xsc.Attrs):
	class stroke_linecap(xsc.TextAttr):
		xmlname = "stroke-linecap"
		values = ("butt", "round", "square", "inherit")


class stroke_linejoin(xsc.Attrs):
	class stroke_linejoin(xsc.TextAttr):
		xmlname = "stroke-linejoin"
		values = ("miter", "round", "bevel", "inherit")


class stroke_miterlimit(xsc.Attrs):
	class stroke_miterlimit(xsc.TextAttr): xmlname = "stroke-miterlimit"


class stroke_opacity(xsc.Attrs):
	class stroke_opacity(xsc.TextAttr): xmlname = "stroke-opacity"


class stroke_width(xsc.Attrs):
	class stroke_width(xsc.TextAttr): xmlname = "stroke-width"


class style2(xsc.Attrs):
	class style(xsc.StyleAttr): pass


class systemLanguage(xsc.Attrs):
	class systemLanguage(xsc.TextAttr): pass


class text_anchor(xsc.Attrs):
	class text_anchor(xsc.TextAttr):
		xmlname = "text-anchor"
		values = ("start", "middle", "end", "inherit")


class text_decoration(xsc.Attrs):
	class text_decoration(xsc.TextAttr): xmlname = "text-decoration"


class text_rendering(xsc.Attrs):
	class text_rendering(xsc.TextAttr):
		xmlname = "text-rendering"
		values = ("auto", "optimizeSpeed", "optimizeLegibility", "geometricPrecision", "inherit")


class transform(xsc.Attrs):
	class transform(xsc.TextAttr): pass


class unicode_bidi(xsc.Attrs):
	class unicode_bidi(xsc.TextAttr):
		xmlname = "unicode-bidi"
		values = ("normal", "embed", "bidi-override", "inherit")


class visibility(xsc.Attrs):
	class visibility(xsc.TextAttr): values = ("visible", "hidden", "inherit")


class word_spacing(xsc.Attrs):
	class word_spacing(xsc.TextAttr): xmlname = "word-spacing"


class writing_mode(xsc.Attrs):
	class writing_mode(xsc.TextAttr):
		xmlname = "writing-mode"
		values = ("lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb", "inherit")


class dx(xsc.Attrs):
	class dx(xsc.TextAttr): pass


class dy(xsc.Attrs):
	class dy(xsc.TextAttr): pass


class format(xsc.Attrs):
	class format(xsc.TextAttr): pass


class glyphRef2(xsc.Attrs):
	class glyphRef(xsc.TextAttr): pass


class rotate(xsc.Attrs):
	class rotate(xsc.TextAttr): pass


class x(xsc.Attrs):
	class x(xsc.TextAttr): pass


class y(xsc.Attrs):
	class y(xsc.TextAttr): pass


class accumulate(xsc.Attrs):
	class accumulate(xsc.TextAttr): values = ("none", "sum")


class additive(xsc.Attrs):
	class additive(xsc.TextAttr): values = ("replace", "sum")


class attributeName(xsc.Attrs):
	class attributeName(xsc.TextAttr): required = True


class attributeType(xsc.Attrs):
	class attributeType(xsc.TextAttr): pass


class begin(xsc.Attrs):
	class begin(xsc.TextAttr): pass


class by(xsc.Attrs):
	class by(xsc.TextAttr): pass


class calcMode(xsc.Attrs):
	class calcMode(xsc.TextAttr): values = ("discrete", "linear", "paced", "spline")


class dur(xsc.Attrs):
	class dur(xsc.TextAttr): pass


class end(xsc.Attrs):
	class end(xsc.TextAttr): pass


class fill2(xsc.Attrs):
	class fill(xsc.TextAttr): values = ("remove", "freeze")


class from_(xsc.Attrs):
	class from_(xsc.TextAttr): xmlname = "from"


class keySplines(xsc.Attrs):
	class keySplines(xsc.TextAttr): pass


class keyTimes(xsc.Attrs):
	class keyTimes(xsc.TextAttr): pass


class max(xsc.Attrs):
	class max(xsc.TextAttr): pass


class min(xsc.Attrs):
	class min(xsc.TextAttr): pass


class onbegin(xsc.Attrs):
	class onbegin(xsc.TextAttr): pass


class onend(xsc.Attrs):
	class onend(xsc.TextAttr): pass


class onrepeat(xsc.Attrs):
	class onrepeat(xsc.TextAttr): pass


class repeatCount(xsc.Attrs):
	class repeatCount(xsc.TextAttr): pass


class repeatDur(xsc.Attrs):
	class repeatDur(xsc.TextAttr): pass


class restart(xsc.Attrs):
	class restart(xsc.TextAttr): values = ("always", "never", "whenNotActive")


class to(xsc.Attrs):
	class to(xsc.TextAttr): pass


class values(xsc.Attrs):
	class values_(xsc.TextAttr): xmlname = "values"


class cx(xsc.Attrs):
	class cx(xsc.TextAttr): pass


class cy(xsc.Attrs):
	class cy(xsc.TextAttr): pass


class height(xsc.Attrs):
	class height(xsc.TextAttr): pass


class in_(xsc.Attrs):
	class in_(xsc.TextAttr): xmlname = "in"


class in2(xsc.Attrs):
	class in2(xsc.TextAttr): required = True


class result(xsc.Attrs):
	class result(xsc.TextAttr): pass


class width(xsc.Attrs):
	class width(xsc.TextAttr): pass


class kernelUnitLength(xsc.Attrs):
	class kernelUnitLength(xsc.TextAttr): pass


class surfaceScale(xsc.Attrs):
	class surfaceScale(xsc.TextAttr): pass


class amplitude(xsc.Attrs):
	class amplitude(xsc.TextAttr): pass


class exponent(xsc.Attrs):
	class exponent(xsc.TextAttr): pass


class intercept(xsc.Attrs):
	class intercept(xsc.TextAttr): pass


class offset(xsc.Attrs):
	class offset(xsc.TextAttr): pass


class slope(xsc.Attrs):
	class slope(xsc.TextAttr): pass


class tableValues(xsc.Attrs):
	class tableValues(xsc.TextAttr): pass


class type(xsc.Attrs):
	class type(xsc.TextAttr):
		values = ("identity", "table", "discrete", "linear", "gamma")
		required = True


class preserveAspectRatio(xsc.Attrs):
	class preserveAspectRatio(xsc.TextAttr): pass


class z(xsc.Attrs):
	class z(xsc.TextAttr): pass


class specularExponent(xsc.Attrs):
	class specularExponent(xsc.TextAttr): pass


class vert_adv_y(xsc.Attrs):
	class vert_adv_y(xsc.TextAttr): xmlname = "vert-adv-y"


class vert_origin_x(xsc.Attrs):
	class vert_origin_x(xsc.TextAttr): xmlname = "vert-origin-x"


class vert_origin_y(xsc.Attrs):
	class vert_origin_y(xsc.TextAttr): xmlname = "vert-origin-y"


class height2(xsc.Attrs):
	class height(xsc.TextAttr): required = True


class width2(xsc.Attrs):
	class width(xsc.TextAttr): required = True


class d(xsc.Attrs):
	class d(xsc.TextAttr): pass


class horiz_adv_x(xsc.Attrs):
	class horiz_adv_x(xsc.TextAttr): xmlname = "horiz-adv-x"


class g1(xsc.Attrs):
	class g1(xsc.TextAttr): pass


class g2(xsc.Attrs):
	class g2(xsc.TextAttr): pass


class k(xsc.Attrs):
	class k(xsc.TextAttr): required = True


class u1(xsc.Attrs):
	class u1(xsc.TextAttr): pass


class u2(xsc.Attrs):
	class u2(xsc.TextAttr): pass


class x1(xsc.Attrs):
	class x1(xsc.TextAttr): pass


class x2(xsc.Attrs):
	class x2(xsc.TextAttr): pass


class y1(xsc.Attrs):
	class y1(xsc.TextAttr): pass


class y2(xsc.Attrs):
	class y2(xsc.TextAttr): pass


class gradientTransform(xsc.Attrs):
	class gradientTransform(xsc.TextAttr): pass


class gradientUnits(xsc.Attrs):
	class gradientUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")


class spreadMethod(xsc.Attrs):
	class spreadMethod(xsc.TextAttr): values = ("pad", "reflect", "repeat")


class viewBox(xsc.Attrs):
	class viewBox(xsc.TextAttr): pass


class points(xsc.Attrs):
	class points(xsc.TextAttr): required = True


class type2(xsc.Attrs):
	class type(xsc.TextAttr): required = True


class zoomAndPan(xsc.Attrs):
	class zoomAndPan(xsc.TextAttr): values = ("disable", "magnify")


class lengthAdjust(xsc.Attrs):
	class lengthAdjust(xsc.TextAttr): values = ("spacing", "spacingAndGlyphs")


class textLength(xsc.Attrs):
	class textLength(xsc.TextAttr): pass


class a(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, word_spacing, writing_mode):
		class target(xsc.TextAttr): pass


class altGlyph(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, dx, dy, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, format, glyph_orientation_horizontal, glyph_orientation_vertical, glyphRef2, id, image_rendering, kerning, letter_spacing, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, rotate, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, unicode_bidi, visibility, word_spacing, x, y):
		pass


class altGlyphDef(xsc.Element):
	xmlns = xmlns
	class Attrs(id):
		pass


class altGlyphItem(xsc.Element):
	xmlns = xmlns
	class Attrs(id):
		pass


class animate(xsc.Element):
	xmlns = xmlns
	class Attrs(accumulate, additive, attributeName, attributeType, begin, by, calcMode, dur, end, externalResourcesRequired, fill2, from_, id, keySplines, keyTimes, max, min, onbegin, onend, onload, onrepeat, repeatCount, repeatDur, requiredExtensions, requiredFeatures, restart, systemLanguage, to, values):
		pass


class animateColor(xsc.Element):
	xmlns = xmlns
	class Attrs(accumulate, additive, attributeName, attributeType, begin, by, calcMode, dur, end, externalResourcesRequired, fill2, from_, id, keySplines, keyTimes, max, min, onbegin, onend, onload, onrepeat, repeatCount, repeatDur, requiredExtensions, requiredFeatures, restart, systemLanguage, to, values):
		pass


class animateMotion(xsc.Element):
	xmlns = xmlns
	class Attrs(accumulate, additive, begin, by, dur, end, externalResourcesRequired, fill2, from_, id, keySplines, keyTimes, max, min, onbegin, onend, onload, onrepeat, repeatCount, repeatDur, requiredExtensions, requiredFeatures, restart, rotate, systemLanguage, to, values):
		class calcMode(xsc.TextAttr): values = ("discrete", "linear", "paced", "spline")
		class keyPoints(xsc.TextAttr): pass
		class origin(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass


class animateTransform(xsc.Element):
	xmlns = xmlns
	class Attrs(accumulate, additive, attributeName, attributeType, begin, by, calcMode, dur, end, externalResourcesRequired, fill2, from_, id, keySplines, keyTimes, max, min, onbegin, onend, onload, onrepeat, repeatCount, repeatDur, requiredExtensions, requiredFeatures, restart, systemLanguage, to, values):
		class type(xsc.TextAttr): values = ("translate", "scale", "rotate", "skewX", "skewY")


class circle(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, cx, cy, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility):
		class r(xsc.TextAttr): required = True


class clipPath(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, mask2, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, word_spacing, writing_mode):
		class clipPathUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")


class color_profile(xsc.Element):
	xmlns = xmlns
	xmlname = "color-profile"
	class Attrs(id):
		class local(xsc.TextAttr): pass
		class name(xsc.TextAttr): required = True
		class rendering_intent(xsc.TextAttr):
			xmlname = "rendering-intent"
			values = ("auto", "perceptual", "relative-colorimetric", "saturation", "absolute-colorimetric")


class cursor(xsc.Element):
	xmlns = xmlns
	class Attrs(externalResourcesRequired, id, requiredExtensions, requiredFeatures, systemLanguage, x, y):
		pass


class definition_src(xsc.Element):
	xmlns = xmlns
	xmlname = "definition-src"
	class Attrs(id):
		pass


class defs(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, word_spacing, writing_mode):
		pass


class desc(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, id, style2):
		pass


class ellipse(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, cx, cy, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility):
		class rx(xsc.TextAttr): required = True
		class ry(xsc.TextAttr): required = True


class feBlend(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, in2, result, width, x, y):
		class mode(xsc.TextAttr): values = ("normal", "multiply", "screen", "darken", "lighten")


class feColorMatrix(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, result, values, width, x, y):
		class type(xsc.TextAttr): values = ("matrix", "saturate", "hueRotate", "luminanceToAlpha")


class feComponentTransfer(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, result, width, x, y):
		pass


class feComposite(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, in2, result, width, x, y):
		class k1(xsc.TextAttr): pass
		class k2(xsc.TextAttr): pass
		class k3(xsc.TextAttr): pass
		class k4(xsc.TextAttr): pass
		class operator(xsc.TextAttr): values = ("over", "in", "out", "atop", "xor", "arithmetic")


class feConvolveMatrix(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, kernelUnitLength, result, width, x, y):
		class bias(xsc.TextAttr): pass
		class divisor(xsc.TextAttr): pass
		class edgeMode(xsc.TextAttr): values = ("duplicate", "wrap", "none")
		class kernelMatrix(xsc.TextAttr): required = True
		class order(xsc.TextAttr): required = True
		class preserveAlpha(xsc.TextAttr): values = ("false", "true")
		class targetX(xsc.IntAttr): pass
		class targetY(xsc.IntAttr): pass


class feDiffuseLighting(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_interpolation_filters, color_rendering, height, id, in_, kernelUnitLength, lighting_color, result, style2, surfaceScale, width, x, y):
		class diffuseConstant(xsc.TextAttr): pass


class feDisplacementMap(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, in2, result, width, x, y):
		class scale(xsc.TextAttr): pass
		class xChannelSelector(xsc.TextAttr): values = ("R", "G", "B", "A")
		class yChannelSelector(xsc.TextAttr): values = ("R", "G", "B", "A")


class feDistantLight(xsc.Element):
	xmlns = xmlns
	class Attrs(id):
		class azimuth(xsc.TextAttr): pass
		class elevation(xsc.TextAttr): pass


class feFlood(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_interpolation_filters, color_rendering, flood_color, flood_opacity, height, id, in_, result, style2, width, x, y):
		pass


class feFuncA(xsc.Element):
	xmlns = xmlns
	class Attrs(amplitude, exponent, id, intercept, offset, slope, tableValues, type):
		pass


class feFuncB(xsc.Element):
	xmlns = xmlns
	class Attrs(amplitude, exponent, id, intercept, offset, slope, tableValues, type):
		pass


class feFuncG(xsc.Element):
	xmlns = xmlns
	class Attrs(amplitude, exponent, id, intercept, offset, slope, tableValues, type):
		pass


class feFuncR(xsc.Element):
	xmlns = xmlns
	class Attrs(amplitude, exponent, id, intercept, offset, slope, tableValues, type):
		pass


class feGaussianBlur(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, result, width, x, y):
		class stdDeviation(xsc.TextAttr): pass


class feImage(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, preserveAspectRatio, result, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, visibility, width, word_spacing, writing_mode, x, y):
		pass


class feMerge(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, result, width, x, y):
		pass


class feMergeNode(xsc.Element):
	xmlns = xmlns
	class Attrs(id, in_):
		pass


class feMorphology(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, result, width, x, y):
		class operator(xsc.TextAttr): values = ("erode", "dilate")
		class radius(xsc.TextAttr): pass


class feOffset(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, dx, dy, height, id, in_, result, width, x, y):
		pass


class fePointLight(xsc.Element):
	xmlns = xmlns
	class Attrs(id, x, y, z):
		pass


class feSpecularLighting(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_interpolation_filters, color_rendering, height, id, in_, kernelUnitLength, lighting_color, result, specularExponent, style2, surfaceScale, width, x, y):
		class specularConstant(xsc.TextAttr): pass


class feSpotLight(xsc.Element):
	xmlns = xmlns
	class Attrs(id, specularExponent, x, y, z):
		class limitingConeAngle(xsc.TextAttr): pass
		class pointsAtX(xsc.TextAttr): pass
		class pointsAtY(xsc.TextAttr): pass
		class pointsAtZ(xsc.TextAttr): pass


class feTile(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, in_, result, width, x, y):
		pass


class feTurbulence(xsc.Element):
	xmlns = xmlns
	class Attrs(color_interpolation_filters, height, id, result, width, x, y):
		class baseFrequency(xsc.TextAttr): pass
		class numOctaves(xsc.IntAttr): pass
		class seed(xsc.TextAttr): pass
		class stitchTiles(xsc.TextAttr): values = ("stitch", "noStitch")
		class type(xsc.TextAttr): values = ("fractalNoise", "turbulence")


class filter(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, visibility, width, word_spacing, writing_mode, x, y):
		class filterRes(xsc.TextAttr): pass
		class filterUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class primitiveUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")


class font(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, vert_adv_y, vert_origin_x, vert_origin_y, visibility, word_spacing, writing_mode):
		class horiz_adv_x(xsc.TextAttr):
			xmlname = "horiz-adv-x"
			required = True
		class horiz_origin_x(xsc.TextAttr): xmlname = "horiz-origin-x"
		class horiz_origin_y(xsc.TextAttr): xmlname = "horiz-origin-y"


class font_face(xsc.Element):
	xmlns = xmlns
	xmlname = "font-face"
	class Attrs(font_family, font_size, id, slope):
		class accent_height(xsc.TextAttr): xmlname = "accent-height"
		class alphabetic(xsc.TextAttr): pass
		class ascent(xsc.TextAttr): pass
		class bbox(xsc.TextAttr): pass
		class cap_height(xsc.TextAttr): xmlname = "cap-height"
		class descent(xsc.TextAttr): pass
		class font_stretch(xsc.TextAttr): xmlname = "font-stretch"
		class font_style(xsc.TextAttr): xmlname = "font-style"
		class font_variant(xsc.TextAttr): xmlname = "font-variant"
		class font_weight(xsc.TextAttr): xmlname = "font-weight"
		class hanging(xsc.TextAttr): pass
		class ideographic(xsc.TextAttr): pass
		class mathematical(xsc.TextAttr): pass
		class overline_position(xsc.TextAttr): xmlname = "overline-position"
		class overline_thickness(xsc.TextAttr): xmlname = "overline-thickness"
		class panose_1(xsc.TextAttr): xmlname = "panose-1"
		class stemh(xsc.TextAttr): pass
		class stemv(xsc.TextAttr): pass
		class strikethrough_position(xsc.TextAttr): xmlname = "strikethrough-position"
		class strikethrough_thickness(xsc.TextAttr): xmlname = "strikethrough-thickness"
		class underline_position(xsc.TextAttr): xmlname = "underline-position"
		class underline_thickness(xsc.TextAttr): xmlname = "underline-thickness"
		class unicode_range(xsc.TextAttr): xmlname = "unicode-range"
		class units_per_em(xsc.TextAttr): xmlname = "units-per-em"
		class v_alphabetic(xsc.TextAttr): xmlname = "v-alphabetic"
		class v_hanging(xsc.TextAttr): xmlname = "v-hanging"
		class v_ideographic(xsc.TextAttr): xmlname = "v-ideographic"
		class v_mathematical(xsc.TextAttr): xmlname = "v-mathematical"
		class widths(xsc.TextAttr): pass
		class x_height(xsc.TextAttr): xmlname = "x-height"


class font_face_format(xsc.Element):
	xmlns = xmlns
	xmlname = "font-face-format"
	class Attrs(id):
		class string(xsc.TextAttr): pass


class font_face_name(xsc.Element):
	xmlns = xmlns
	xmlname = "font-face-name"
	class Attrs(id):
		class name(xsc.TextAttr): pass


class font_face_src(xsc.Element):
	xmlns = xmlns
	xmlname = "font-face-src"
	class Attrs(id):
		pass


class font_face_uri(xsc.Element):
	xmlns = xmlns
	xmlname = "font-face-uri"
	class Attrs(id):
		pass


class foreignObject(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height2, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, width2, word_spacing, writing_mode, x, y):
		pass


class g(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, word_spacing, writing_mode):
		pass


class glyph(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, d, direction, display, dominant_baseline, enable_background, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, horiz_adv_x, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, vert_adv_y, vert_origin_x, vert_origin_y, visibility, word_spacing, writing_mode):
		class arabic_form(xsc.TextAttr): xmlname = "arabic-form"
		class glyph_name(xsc.TextAttr): xmlname = "glyph-name"
		class lang(xsc.TextAttr): pass
		class orientation(xsc.TextAttr): pass
		class str(xsc.TextAttr): pass


class glyphRef(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, dx, dy, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, format, glyphRef2, id, style2, x, y):
		pass


class hkern(xsc.Element):
	xmlns = xmlns
	class Attrs(g1, g2, id, k, u1, u2):
		pass


class image(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip, clip_path, clip_rule, color, color_interpolation, color_profile2, color_rendering, cursor2, display, externalResourcesRequired, fill_opacity, filter2, height2, id, image_rendering, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, preserveAspectRatio, requiredExtensions, requiredFeatures, shape_rendering, stroke_opacity, style2, systemLanguage, text_rendering, transform, visibility, width2, x, y):
		pass


class line(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility, x1, x2, y1, y2):
		pass


class linearGradient(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_rendering, externalResourcesRequired, gradientTransform, gradientUnits, id, spreadMethod, stop_color, stop_opacity, style2, x1, x2, y1, y2):
		pass


class marker(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, preserveAspectRatio, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, viewBox, visibility, word_spacing, writing_mode):
		class markerHeight(xsc.TextAttr): pass
		class markerUnits(xsc.TextAttr): values = ("strokeWidth", "userSpaceOnUse")
		class markerWidth(xsc.TextAttr): pass
		class orient(xsc.TextAttr): pass
		class refX(xsc.TextAttr): pass
		class refY(xsc.TextAttr): pass


class mask(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, unicode_bidi, visibility, width, word_spacing, writing_mode, x, y):
		class maskContentUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class maskUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")


class metadata(xsc.Element):
	xmlns = xmlns
	class Attrs(id):
		pass


class missing_glyph(xsc.Element):
	xmlns = xmlns
	xmlname = "missing-glyph"
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, d, direction, display, dominant_baseline, enable_background, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, horiz_adv_x, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, vert_adv_y, vert_origin_x, vert_origin_y, visibility, word_spacing, writing_mode):
		pass


class mpath(xsc.Element):
	xmlns = xmlns
	class Attrs(externalResourcesRequired, id):
		pass


class path(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility):
		class d(xsc.TextAttr): required = True
		class pathLength(xsc.TextAttr): pass


class pattern(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, opacity, overflow, pointer_events, preserveAspectRatio, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, unicode_bidi, viewBox, visibility, width, word_spacing, writing_mode, x, y):
		class patternContentUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")
		class patternTransform(xsc.TextAttr): pass
		class patternUnits(xsc.TextAttr): values = ("userSpaceOnUse", "objectBoundingBox")


class polygon(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, points, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility):
		pass


class polyline(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, id, image_rendering, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, points, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility):
		pass


class radialGradient(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_rendering, cx, cy, externalResourcesRequired, gradientTransform, gradientUnits, id, spreadMethod, stop_color, stop_opacity, style2):
		class fx(xsc.TextAttr): pass
		class fy(xsc.TextAttr): pass
		class r(xsc.TextAttr): pass


class rect(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, display, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, height2, id, image_rendering, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_rendering, transform, visibility, width2, x, y):
		class rx(xsc.TextAttr): pass
		class ry(xsc.TextAttr): pass


class script(xsc.Element):
	xmlns = xmlns
	class Attrs(externalResourcesRequired, id, type2):
		pass


class set(xsc.Element):
	xmlns = xmlns
	class Attrs(attributeName, attributeType, begin, dur, end, externalResourcesRequired, fill2, id, max, min, onbegin, onend, onload, onrepeat, repeatCount, repeatDur, requiredExtensions, requiredFeatures, restart, systemLanguage, to):
		pass


class stop(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, color, color_interpolation, color_rendering, id, stop_color, stop_opacity, style2):
		class offset(xsc.TextAttr): required = True


class style(xsc.Element):
	xmlns = xmlns
	class Attrs(id, type2):
		class media(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass


class svg(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, preserveAspectRatio, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, unicode_bidi, viewBox, visibility, width, word_spacing, writing_mode, x, y, zoomAndPan):
		class baseProfile(xsc.TextAttr): pass
		class contentScriptType(xsc.TextAttr): pass
		class contentStyleType(xsc.TextAttr): pass
		class onabort(xsc.TextAttr): pass
		class onerror(xsc.TextAttr): pass
		class onresize(xsc.TextAttr): pass
		class onscroll(xsc.TextAttr): pass
		class onunload(xsc.TextAttr): pass
		class onzoom(xsc.TextAttr): pass
		class version(xsc.TextAttr): pass


class switch(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, word_spacing, writing_mode):
		pass


class symbol(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, preserveAspectRatio, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, text_anchor, text_decoration, text_rendering, unicode_bidi, viewBox, visibility, word_spacing, writing_mode):
		pass


class text(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, dx, dy, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, lengthAdjust, letter_spacing, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, rotate, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, textLength, transform, unicode_bidi, visibility, word_spacing, writing_mode, x, y):
		pass


class textPath(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, lengthAdjust, letter_spacing, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, textLength, unicode_bidi, visibility, word_spacing):
		class method(xsc.TextAttr): values = ("align", "stretch")
		class spacing(xsc.TextAttr): values = ("auto", "exact")
		class startOffset(xsc.TextAttr): pass


class title(xsc.Element):
	xmlns = xmlns
	class Attrs(class_, id, style2):
		pass


class tref(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, dx, dy, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, lengthAdjust, letter_spacing, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, rotate, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, textLength, unicode_bidi, visibility, word_spacing, x, y):
		pass


class tspan(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip_path, clip_rule, color, color_interpolation, color_rendering, cursor2, direction, display, dominant_baseline, dx, dy, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, id, image_rendering, kerning, lengthAdjust, letter_spacing, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, pointer_events, requiredExtensions, requiredFeatures, rotate, shape_rendering, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, textLength, unicode_bidi, visibility, word_spacing, x, y):
		pass


class use(xsc.Element):
	xmlns = xmlns
	class Attrs(alignment_baseline, baseline_shift, class_, clip, clip_path, clip_rule, color, color_interpolation, color_interpolation_filters, color_profile2, color_rendering, cursor2, direction, display, dominant_baseline, enable_background, externalResourcesRequired, fill, fill_opacity, fill_rule, filter2, flood_color, flood_opacity, font_family, font_size, font_size_adjust, font_stretch, font_style, font_variant, font_weight, glyph_orientation_horizontal, glyph_orientation_vertical, height, id, image_rendering, kerning, letter_spacing, lighting_color, marker_end, marker_mid, marker_start, mask2, onactivate, onclick, onfocusin, onfocusout, onload, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, opacity, overflow, pointer_events, requiredExtensions, requiredFeatures, shape_rendering, stop_color, stop_opacity, stroke, stroke_dasharray, stroke_dashoffset, stroke_linecap, stroke_linejoin, stroke_miterlimit, stroke_opacity, stroke_width, style2, systemLanguage, text_anchor, text_decoration, text_rendering, transform, unicode_bidi, visibility, width, word_spacing, writing_mode, x, y):
		pass


class view(xsc.Element):
	xmlns = xmlns
	class Attrs(externalResourcesRequired, id, preserveAspectRatio, viewBox, zoomAndPan):
		class viewTarget(xsc.TextAttr): pass


class vkern(xsc.Element):
	xmlns = xmlns
	class Attrs(g1, g2, id, k, u1, u2):
		pass


altGlyphDef.model = sims.Elements(altGlyphItem, glyphRef)
feBlend.model = \
feColorMatrix.model = \
feComposite.model = \
feConvolveMatrix.model = \
feDisplacementMap.model = \
feDistantLight.model = \
feFuncA.model = \
feFuncB.model = \
feFuncG.model = \
feFuncR.model = \
feGaussianBlur.model = \
feMergeNode.model = \
feMorphology.model = \
feOffset.model = \
fePointLight.model = \
feSpotLight.model = \
feTile.model = \
feTurbulence.model = sims.Elements(animate, set)
feFlood.model = \
stop.model = sims.Elements(animate, set, animateColor)
feImage.model = sims.Elements(animate, set, animateTransform)
circle.model = \
ellipse.model = \
image.model = \
line.model = \
path.model = \
polygon.model = \
polyline.model = \
rect.model = \
use.model = sims.Elements(animateMotion, set, title, animateColor, animateTransform, animate, metadata, desc)
font_face.model = sims.Elements(definition_src, desc, metadata, font_face_src, title)
defs.model = sims.Elements(defs, set, animate, text, symbol, clipPath, use, animateColor, font_face, style, polyline, view, marker, path, line, font, color_profile, ellipse, rect, desc, a, cursor, animateMotion, polygon, g, title, svg, script, mask, altGlyphDef, filter, switch, animateTransform, linearGradient, pattern, circle, radialGradient, image, metadata)
g.model = \
glyph.model = \
marker.model = \
mask.model = \
missing_glyph.model = \
pattern.model = \
svg.model = \
symbol.model = sims.Elements(defs, set, animate, text, symbol, clipPath, use, animateColor, font_face, style, polyline, view, marker, path, line, font, color_profile, ellipse, rect, desc, a, cursor, animateMotion, polygon, g, title, svg, script, mask, altGlyphDef, filter, switch, animateTransform, linearGradient, pattern, circle, radialGradient, image, metadata)
animateMotion.model = sims.Elements(desc, metadata, mpath, title)
feComponentTransfer.model = sims.Elements(feFuncA, feFuncR, feFuncB, feFuncG)
feMerge.model = sims.Elements(feMergeNode)
filter.model = sims.Elements(feTurbulence, set, feTile, feColorMatrix, feConvolveMatrix, feMorphology, feGaussianBlur, feDisplacementMap, feComposite, animate, feMerge, feSpecularLighting, desc, feComponentTransfer, title, feDiffuseLighting, feFlood, feBlend, feOffset, feImage, metadata)
font_face_uri.model = sims.Elements(font_face_format)
font_face_src.model = sims.Elements(font_face_name, font_face_uri)
altGlyphItem.model = sims.Elements(glyphRef)
switch.model = sims.Elements(set, animate, text, image, animateMotion, animateColor, polyline, path, line, ellipse, rect, desc, a, use, polygon, g, title, svg, switch, animateTransform, foreignObject, circle, metadata)
clipPath.model = sims.Elements(set, animate, text, use, animateColor, polyline, path, line, ellipse, rect, desc, animateMotion, polygon, title, altGlyphDef, animateTransform, circle, metadata)
feDiffuseLighting.model = \
feSpecularLighting.model = sims.Elements(set, fePointLight, feSpotLight, animate, feDistantLight, animateColor)
tref.model = sims.Elements(set, title, animate, metadata, animateColor, desc)
linearGradient.model = \
radialGradient.model = sims.Elements(set, title, animate, metadata, stop, animateTransform, desc)
animate.model = \
animateColor.model = \
animateTransform.model = \
color_profile.model = \
cursor.model = \
mpath.model = \
set.model = \
view.model = sims.Elements(title, metadata, desc)
font.model = sims.Elements(title, missing_glyph, font_face, vkern, hkern, metadata, glyph, desc)
text.model = sims.ElementsOrText(a, animateMotion, set, textPath, tspan, title, animateColor, tref, animateTransform, altGlyph, animate, desc, metadata)
textPath.model = \
tspan.model = sims.ElementsOrText(a, set, title, tspan, animateColor, tref, altGlyph, animate, metadata, desc)
a.model = sims.ElementsOrText(defs, set, text, symbol, clipPath, use, animateColor, font_face, style, polyline, view, marker, path, line, font, color_profile, animate, rect, desc, a, cursor, animateMotion, polygon, g, svg, title, mask, altGlyphDef, ellipse, filter, script, switch, animateTransform, linearGradient, pattern, circle, radialGradient, image, metadata)
definition_src.model = \
font_face_format.model = \
font_face_name.model = \
glyphRef.model = \
hkern.model = \
vkern.model = sims.Empty()
altGlyph.model = \
desc.model = \
foreignObject.model = \
metadata.model = \
script.model = \
style.model = \
title.model = sims.NoElements()
