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
<link href="http://www.w3.org/TR/SVG/">&xsl;</link> 1.0 definition.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc

class media_usage(xsc.Element.Attrs):
	class media_usage(xsc.TextAttr):
		xmlname = "media-usage"
		values = ("auto", "paginate", "bounded-in-one-dimension", "unbounded")

class src(xsc.Element.Attrs):
	class src(xsc.URLAttr):
		pass

class color_profile_name(xsc.Element.Attrs):
	class color_profile_name(xsc.TextAttr):
		xmlname = "color-profile-name"

class rendering_intent(xsc.Element.Attrs):
	class rendering_intent(xsc.TextAttr):
		xmlname = "rendering-intent"
		values = ("auto", "perceptual", "relative-colorimetric", "saturation", "absolute-colorimetric", "inherit")

class country(xsc.Element.Attrs):
	class country(xsc.TextAttr):
		pass

class format(xsc.Element.Attrs):
	class format(xsc.TextAttr):
		pass

class language(xsc.Element.Attrs):
	class language(xsc.TextAttr):
		pass

class letter_value(xsc.Element.Attrs):
	class letter_value(xsc.TextAttr):
		xmlname = "letter-value"
		values = ("auto", "alphabetic", "traditional")

class grouping_separator(xsc.Element.Attrs):
	class grouping_separator(xsc.TextAttr):
		xmlname = "grouping-separator"

class grouping_size(xsc.Element.Attrs):
	class grouping_size(xsc.TextAttr):
		xmlname = "grouping-size"

class initial_page_number(xsc.Element.Attrs):
	class initial_page_number(xsc.TextAttr):
		xmlname = "initial-page-number"

class force_page_count(xsc.Element.Attrs):
	class force_page_count(xsc.TextAttr):
		xmlname = "force-page-count"
		values = ("auto", "even", "odd", "end-on-even", "end-on-odd", "no-force", "inherit")

class master_reference(xsc.Element.Attrs):
	class master_reference(xsc.TextAttr):
		xmlname = "master-reference"

class master_name(xsc.Element.Attrs):
	class master_name(xsc.TextAttr):
		xmlname = "master-name"

class maximum_repeats(xsc.Element.Attrs):
	class maximum_repeats(xsc.TextAttr):
		xmlname = "maximum-repeats"

class page_position(xsc.Element.Attrs):
	class page_position(xsc.TextAttr):
		xmlname = "page-position"
		values = ("first", "last", "rest", "any", "inherit")

class odd_or_even(xsc.Element.Attrs):
	class odd_or_even(xsc.TextAttr):
		xmlname = "odd-or-even"
		values = ("odd", "even", "any", "inherit")

class blank_or_not_blank(xsc.Element.Attrs):
	class blank_or_not_blank(xsc.TextAttr):
		xmlname = "blank-or-not-blank"
		values = ("blank", "not-blank", "any", "inherit")

class page_height(xsc.Element.Attrs):
	class page_height(xsc.TextAttr):
		xmlname = "page_height"

class page_width(xsc.Element.Attrs):
	class page_width(xsc.TextAttr):
		xmlname = "page_width"

class reference_orientation(xsc.Element.Attrs):
	class reference_orientation(xsc.TextAttr):
		xmlname = "reference-orientation"
		values = (0, 90, 180, 270, -90, -180, -270, "inherit")

class writing_mode(xsc.Element.Attrs):
	class writing_mode(xsc.TextAttr):
		xmlname = "writing-mode"
		values = ("lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb", "inherit")

class clip(xsc.Element.Attrs):
	class clip(xsc.TextAttr):
		pass

class column_count(xsc.Element.Attrs):
	class column_count(xsc.TextAttr):
		xmlname = "column-count"

class column_gap(xsc.Element.Attrs):
	class column_gap(xsc.TextAttr):
		xmlname = "column-gap"

class display_align(xsc.Element.Attrs):
	class display_align(xsc.TextAttr):
		xmlname = "display-align"
		values = ("auto", "before", "center", "after", "inherit")

class overflow(xsc.Element.Attrs):
	class overflow(xsc.TextAttr):
		values = ("visible", "hidden", "scroll", "error-if-overflow", "auto", "inherit")

class region_name(xsc.Element.Attrs):
	class region_name(xsc.TextAttr):
		xmlname = "region-name"

class extent(xsc.Element.Attrs):
	class extent(xsc.TextAttr):
		pass

class precedence(xsc.Element.Attrs):
	class precedence(xsc.TextAttr):
		values = ("true", "false", "inherit")

class flow_name(xsc.Element.Attrs):
	class flow_name(xsc.TextAttr):
		xmlname = "flow-name"

class color(xsc.Element.Attrs):
	class color(xsc.ColorAttr):
		pass

class line_height(xsc.Element.Attrs):
	class line_height(xsc.TextAttr):
		xmlname = "line-height"

class visibility(xsc.Element.Attrs):
	class visibility(xsc.TextAttr):
		values = ("visible", "hidden", "collapse", "inherit")

class break_after(xsc.Element.Attrs):
	class break_after(xsc.TextAttr):
		xmlname = "break-after"
		values = (" auto", "column", "page", "even-page", "odd-page", "inherit")

class break_before(xsc.Element.Attrs):
	class break_before(xsc.TextAttr):
		xmlname = "break-before"
		values = (" auto", "column", "page", "even-page", "odd-page", "inherit")

class text_depth(xsc.Element.Attrs):
	class text_depth(xsc.TextAttr):
		xmlname = "text-depth"

class text_altitude(xsc.Element.Attrs):
	class text_altitude(xsc.TextAttr):
		xmlname = "text-altitude"

class hyphenation_keep(xsc.Element.Attrs):
	class hyphenation_keep(xsc.Element.Attrs):
		xmlname = "hyphenation-keep"
		values = ("auto", "column", "page", "inherit")

class hyphenation_ladder_count(xsc.Element.Attrs):
	class hyphenation_ladder_count(xsc.TextAttr):
		xmlname = "hyphenation-ladder-count"

class intrusion_displace(xsc.Element.Attrs):
	class intrusion_displace(xsc.TextAttr):
		xmlname = "intrusion-displace"
		values = ("auto", "none", "line", "indent", "block", "inherit")

class keep_together(xsc.Element.Attrs):
	class keep_together(xsc.TextAttr):
		xmlname = "keep-together"

class keep_with_next(xsc.Element.Attrs):
	class keep_with_next(xsc.TextAttr):
		xmlname = "keep-with-next"
	class keep_with_next_within_line(xsc.TextAttr):
		xmlname = "keep-with-next.within-line"
	class keep_with_next_within_column(xsc.TextAttr):
		xmlname = "keep-with-next.within-column"
	class keep_with_next_within_page(xsc.TextAttr):
		xmlname = "keep-with-next.within-page"

class keep_with_previous(xsc.Element.Attrs):
	class keep_with_previous(xsc.TextAttr):
		xmlname = "keep-with-previous"
	class keep_with_previous_within_line(xsc.TextAttr):
		xmlname = "keep-with-previous.within-line"
	class keep_with_previous_within_column(xsc.TextAttr):
		xmlname = "keep-with-previous.within-column"
	class keep_with_previous_within_page(xsc.TextAttr):
		xmlname = "keep-with-previous.within-page"

class last_line_end_indent(xsc.Element.Attrs):
	class last_line_end_indent(xsc.TextAttr):
		xmlname = "last-line-end-indent"

class linefeed_treatment(xsc.Element.Attrs):
	class linefeed_treatment(xsc.TextAttr):
		xmlname = "linefeed-treatment"
		values = ("ignore", "preserve", "treat-as-space", "treat-as-zero-width-space", "inherit")

class line_height_shift_adjustment(xsc.Element.Attrs):
	class line_height_shift_adjustment(xsc.TextAttr):
		xmlname = "line-height-shift-adjustment"
		values = ("consider-shifts", "disregard-shifts", "inherit")

class line_stacking_strategy(xsc.Element.Attrs):
	class line_stacking_strategy(xsc.TextAttr):
		xmlname = "line-stacking-strategy"
		values = ("line-height", "font-height", "max-height", "inherit")

class orphans(xsc.Element.Attrs):
	class orphans(xsc.TextAttr):
		pass

class white_space_treatment(xsc.Element.Attrs):
	class white_space_treatment(xsc.TextAttr):
		xmlname = "white-space-treatment"
		values = ("ignore", "preserve", "ignore-if-before-linefeed", "ignore-if-after-linefeed", "ignore-if-surrounding-linefeed", "inherit")

class span(xsc.Element.Attrs):
	class span(xsc.TextAttr):
		values = ("none", "all", "inherit")

class text_align(xsc.Element.Attrs):
	class text_align(xsc.TextAttr):
		xmlname = "text-align"

class text_align_last(xsc.Element.Attrs):
	class text_align_last(xsc.TextAttr):
		xmlname = "text-align-last"
		values = ("relative", "start", "center", "end", "justify", "inside", "outside", "left", "right", "inherit")

class text_indent(xsc.Element.Attrs):
	class text_indent(xsc.TextAttr):
		xmlname = "text-indent"

class white_space_collapse(xsc.Element.Attrs):
	class white_space_collapse(xsc.TextAttr):
		xmlname = "white-space-collapse"
		values = ("false", "true", "inherit")

class widows(xsc.Element.Attrs):
	class widows(xsc.TextAttr):
		pass

class wrap_option(xsc.Element.Attrs):
	class wrap_option(xsc.TextAttr):
		xmlname = "wrap-option"
		values = ("no-wrap", "wrap", "inherit")

class score_spaces(xsc.Element.Attrs):
	class score_spaces(xsc.TextAttr):
		xmlname = "score-spaces"
		values = ("true", "false", "inherit")

class text_decoration(xsc.Element.Attrs):
	class text_decoration(xsc.TextAttr):
		xmlname = "text-decoration"

class common_margin_properties_block(xsc.Element.Attrs):
	class margin_top(xsc.TextAttr): xmlname = "margin-top"
	class margin_bottom(xsc.TextAttr): xmlname = "margin-bottom"
	class margin_left(xsc.TextAttr): xmlname = "margin-left"
	class margin_right(xsc.TextAttr): xmlname = "margin-right"
	class space_before(xsc.TextAttr): xmlname = "space-before"
	class space_before_minimum(xsc.TextAttr): xmlname = "space-before.minimum"
	class space_before_optimum(xsc.TextAttr): xmlname = "space-before.optimum"
	class space_before_maximum(xsc.TextAttr): xmlname = "space-before.maximum"
	class space_before_conditionality(xsc.TextAttr): xmlname = "space-before.conditionality"
	class space_before_precedence(xsc.TextAttr): xmlname = "space-before.precedence"
	class space_after_minimum(xsc.TextAttr): xmlname = "space-after.minimum"
	class space_after_optimum(xsc.TextAttr): xmlname = "space-after.optimum"
	class space_after_maximum(xsc.TextAttr): xmlname = "space-after.maximum"
	class space_after_conditionality(xsc.TextAttr): xmlname = "space-after.conditionality"
	class space_after_precedence(xsc.TextAttr): xmlname = "space-after.precedence"
	class start_indent(xsc.TextAttr): xmlname = "start-indent"
	class end_indent(xsc.TextAttr): xmlname = "end-indent"

class common_margin_properties_inline(xsc.Element.Attrs):
	class space_end(xsc.TextAttr): xmlname = "space-end"
	class space_end_minimum(xsc.TextAttr): xmlname = "space-end.minimum"
	class space_end_optimum(xsc.TextAttr): xmlname = "space-end.optimum"
	class space_end_maximum(xsc.TextAttr): xmlname = "space-end.maximum"
	class space_end_conditionality(xsc.TextAttr): xmlname = "space-end.conditionality"
	class space_end_precedence(xsc.TextAttr): xmlname = "space-end.precedence"
	class space_start_minimum(xsc.TextAttr): xmlname = "space-start.minimum"
	class space_start_optimum(xsc.TextAttr): xmlname = "space-start.optimum"
	class space_start_maximum(xsc.TextAttr): xmlname = "space-start.maximum"
	class space_start_conditionality(xsc.TextAttr): xmlname = "space-start.conditionality"
	class space_start_precedence(xsc.TextAttr): xmlname = "space-start.precedence"

class common_border_padding_background_properties(xsc.Element.Attrs):
	class background_attachment(xsc.TextAttr):
		xmlname = "background-attachment"
		values = ("scroll", "fixed", "inherit")
	class background_color(xsc.ColorAttr):
		xmlname = "background-color"
	class background_image(xsc.URLAttr):
		xmlname = "background-image"
	class background_repeat(xsc.TextAttr):
		xmlname = "background-repeat"
		values = ("repeat", "repeat-x", "repeat-y", "no-repeat", "inherit")
	class background_position_horizontal(xsc.TextAttr):
		xmlname = "background-position-horizontal"
	class background_position_vertical(xsc.TextAttr):
		xmlname = "background-position-vertical"
	class border_before_color(xsc.ColorAttr):
		xmlname = "border-before-color"
	class border_before_style(xsc.TextAttr):
		xmlname = "border-before-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_before_width(xsc.TextAttr):
		xmlname = "border-before-width"
	class border_before_width_length(xsc.TextAttr):
		xmlname = "border-before-width.length"
	class border_before_width_conditionality(xsc.TextAttr):
		xmlname = "border-before-width.conditionality"
	class border_after_color(xsc.ColorAttr):
		xmlname = "border-after-color"
	class border_after_style(xsc.TextAttr):
		xmlname = "border-after-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_after_width(xsc.TextAttr):
		xmlname = "border-after-width"
	class border_after_width_length(xsc.TextAttr):
		xmlname = "border-after-width.length"
	class border_after_width_conditionality(xsc.TextAttr):
		xmlname = "border-after-width.conditionality"
	class border_start_color(xsc.ColorAttr):
		xmlname = "border-start-color"
	class border_start_style(xsc.TextAttr):
		xmlname = "border-start-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_start_width(xsc.TextAttr):
		xmlname = "border-start-width"
	class border_start_width_length(xsc.TextAttr):
		xmlname = "border-start-width.length"
	class border_start_width_conditionality(xsc.TextAttr):
		xmlname = "border-start-width.conditionality"
	class border_end_color(xsc.ColorAttr):
		xmlname = "border-end-color"
	class border_end_style(xsc.TextAttr):
		xmlname = "border-end-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_end_width(xsc.TextAttr):
		xmlname = "border-end-width"
	class border_end_width_length(xsc.TextAttr):
		xmlname = "border-end-width.length"
	class border_end_width_conditionality(xsc.TextAttr):
		xmlname = "border-end-width.conditionality"
	class border_top_color(xsc.ColorAttr):
		xmlname = "border-top-color"
	class border_top_style(xsc.TextAttr):
		xmlname = "border-top-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_top_width(xsc.TextAttr):
		xmlname = "border-top-width"
	class border_bottom_color(xsc.ColorAttr):
		xmlname = "border-bottom-color"
	class border_bottom_style(xsc.TextAttr):
		xmlname = "border-bottom-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_bottom_width(xsc.TextAttr):
		xmlname = "border-bottom-width"
	class border_left_color(xsc.ColorAttr):
		xmlname = "border-left-color"
	class border_left_style(xsc.TextAttr):
		xmlname = "border-left-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_left_width(xsc.TextAttr):
		xmlname = "border-left-width"
	class border_right_color(xsc.ColorAttr):
		xmlname = "border-right-color"
	class border_right_style(xsc.TextAttr):
		xmlname = "border-right-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_right_width(xsc.TextAttr):
		xmlname = "border-right-width"
	class padding_before(xsc.TextAttr):
		xmlname = "padding-before"
	class padding_before_length(xsc.TextAttr):
		xmlname = "padding-before.length"
	class padding_before_conditionality(xsc.TextAttr):
		xmlname = "padding-before.conditionality"
	class padding_after(xsc.TextAttr):
		xmlname = "padding-after"
	class padding_after_length(xsc.TextAttr):
		xmlname = "padding-after.length"
	class padding_after_conditionality(xsc.TextAttr):
		xmlname = "padding-after.conditionality"
	class padding_start(xsc.TextAttr):
		xmlname = "padding-start"
	class padding_start_length(xsc.TextAttr):
		xmlname = "padding-start.length"
	class padding_start_conditionality(xsc.TextAttr):
		xmlname = "padding-start.conditionality"
	class padding_end(xsc.TextAttr):
		xmlname = "padding-end"
	class padding_end_length(xsc.TextAttr):
		xmlname = "padding-end.length"
	class padding_end_conditionality(xsc.TextAttr):
		xmlname = "padding-end.conditionality"
	class padding_top(xsc.TextAttr):
		xmlname = "padding-top"
	class padding_bottom(xsc.TextAttr):
		xmlname = "padding-bottom"
	class padding_left(xsc.TextAttr):
		xmlname = "padding-left"
	class padding_right(xsc.TextAttr):
		xmlname = "padding-right"

class common_accessibility_properties(xsc.Element.Attrs):
	class source_document(xsc.TextAttr): xmlname = "source-document"
	class role(xsc.TextAttr): pass

class common_aural_properties(xsc.Element.Attrs):
	class azimuth(xsc.TextAttr): pass
	class cue_after(xsc.TextAttr): xmlname = "cue-after"
	class cue_before(xsc.TextAttr): xmlname = "cue-before"
	class elevation(xsc.TextAttr): pass
	class pause_after(xsc.TextAttr): xmlname = "pause-after"
	class pause_before(xsc.TextAttr): xmlname = "pause-before"
	class pitch(xsc.TextAttr): pass
	class pitch_range(xsc.TextAttr): xmlname = "pitch-range"
	class play_during(xsc.TextAttr): xmlname = "play-during"
	class richness(xsc.TextAttr): pass
	class speak(xsc.TextAttr): values = ("normal", "none", "spell-out", "inherit")
	class speak_header(xsc.TextAttr): xmlname = "speak-header"; values = ("once", "always", "inherit")
	class speak_numeral(xsc.TextAttr): xmlname = "speak-numeral"; values = ("digits", "continuous", "inherit")
	class speak_punctuation(xsc.TextAttr): xmlname = "speak-punctuation"; values = ("code", "none", "inherit")
	class speech_rate(xsc.TextAttr): xmlname = "speech-rate"
	class stress(xsc.TextAttr): pass
	class voice_family(xsc.TextAttr): xmlname = "voice-family"
	class volume(xsc.TextAttr): pass

class common_font_properties(xsc.Element.Attrs):
	class font_family(xsc.TextAttr):
		xmlname = "font-family"
	class font_selection_strategy(xsc.TextAttr):
		xmlname = "font-selection-strategy"
		values = ("auto", "character-by-character", "inherit")
	class font_size(xsc.TextAttr):
		xmlname = "font-size"
	class font_stretch(xsc.TextAttr):
		xmlname = "font-stretch"
		values = ("normal", "wider", "narrower", "ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded", "inherit")
	class font_size_adjust(xsc.TextAttr):
		xmlname = "font-size-adjust"
	class font_style(xsc.TextAttr):
		xmlname = "font-style"
		values = ("normal", "italic", "oblique", "backslant", "inherit")
	class font_variant(xsc.TextAttr):
		xmlname = "font-variant"
		values = ("normal", "small-caps", "inherit")
	class font_weight(xsc.TextAttr):
		xmlname = "font-weight"
		values = ("normal", "bold", "bolder", "lighter", 100, 200, 300, 400, 500, 600, 700, 800, 900, "inherit")

class common_hyphenation_properties(country, language):
	class script(xsc.TextAttr): pass
	class hyphenate(xsc.TextAttr): values = ("false", "true", "inherit")
	class hyphenation_character(xsc.TextAttr): xmlname = "hyphenation-character"
	class hyphenation_push_character_count(xsc.TextAttr): xmlname = "hyphenation-push-character-count"
	class hyphenation_remain_character_count(xsc.TextAttr): xmlname = "hyphenation-remain-character-count"

class common_relative_position_properties(xsc.Element.Attrs):
	class relative_position(xsc.TextAttr):
		xmlname = "relative-position"
		values = ("static", "relative", "inherit")

class common_absolute_position_properties(xsc.Element.Attrs):
	class absolute_position(xsc.TextAttr):
		xmlname = "absolute-position"
		values = ("auto", "absolute", "fixed", "inherit")
	class top(xsc.TextAttr):
		pass
	class right(xsc.TextAttr):
		pass
	class bottom(xsc.TextAttr):
		pass
	class left(xsc.TextAttr):
		pass

class block_progression_dimension(xsc.Element.Attrs):
	class block_progression_dimension(xsc.TextAttr):
		xmlname = "block-progression-dimension"
	class block_progression_dimension_minimum(xsc.TextAttr):
		xmlname = "block-progression-dimension.minimum"
	class block_progression_dimension_optimum(xsc.TextAttr):
		xmlname = "block-progression-dimension.optimum"
	class block_progression_dimension_maximum(xsc.TextAttr):
		xmlname = "block-progression-dimension.maximum"

class inline_progression_dimension(xsc.Element.Attrs):
	class inline_progression_dimension(xsc.TextAttr):
		xmlname = "inline-progression-dimension"
	class inline_progression_dimension_minimum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.minimum"
	class inline_progression_dimension_optimum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.optimum"
	class inline_progression_dimension_maximum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.maximum"

class height(xsc.Element.Attrs):
	class height(xsc.TextAttr):
		pass

class width(xsc.Element.Attrs):
	class width(xsc.TextAttr):
		pass

class z_index(xsc.Element.Attrs):
	class z_index(xsc.TextAttr):
		xmlname = "z-index"

class direction(xsc.Element.Attrs):
	class direction(xsc.TextAttr):
		values = ("ltr", "rtl", "inherit")

class letter_spacing(xsc.Element.Attrs):
	class letter_spacing(xsc.TextAttr):
		xmlname = "letter-spacing"

class unicode_bidi(xsc.Element.Attrs):
	class unicode_bidi(xsc.TextAttr):
		xmlname = "unicode-bidi"
		values = ("normal", "embed", "bidi-override", "inherit")

class word_spacing(xsc.Element.Attrs):
	class word_spacing(xsc.TextAttr):
		xmlname = "word-spacing"

class alignment_adjust(xsc.Element.Attrs):
	class alignment_adjust(xsc.TextAttr):
		xmlname = "alignment-adjust"

class treat_as_word_space(xsc.Element.Attrs):
	class treat_as_word_space(xsc.TextAttr):
		xmlname = "treat-as-word-space"
		values = ("auto", "true", "false", "inherit")

class alignment_baseline(xsc.Element.Attrs):
	class alignment_baseline(xsc.TextAttr):
		xmlname = "alignment-baseline"
		values = ("auto", "baseline", "before-edge", "text-before-edge", "middle", "central", "after-edge", "text-after-edge", "ideographic", "alphabetic", "hanging", "mathematical", "inherit")

class baseline_shift(xsc.Element.Attrs):
	class baseline_shift(xsc.TextAttr):
		xmlname = "baseline-shift"

class character(xsc.Element.Attrs):
	class character(xsc.TextAttr):
		pass

class dominant_baseline(xsc.Element.Attrs):
	class dominant_baseline(xsc.TextAttr):
		xmlname = "dominant-baseline"
		values = ("auto", "use-script", "no-change", "reset-size", "ideographic", "alphabetic", "hanging", "mathematical", "central", "middle", "text-after-edge", "text-before-edge", "inherit")

class glyph_orientation_horizontal(xsc.Element.Attrs):
	class glyph_orientation_horizontal(xsc.TextAttr):
		xmlname = "glyph-orientation-horizontal"

class glyph_orientation_vertical(xsc.Element.Attrs):
	class glyph_orientation_vertical(xsc.TextAttr):
		xmlname = "glyph-orientation-vertical"

class suppress_at_line_break(xsc.Element.Attrs):
	class suppress_at_line_break(xsc.TextAttr):
		xmlname = "suppress-at-line-break"
		values = ("auto", "suppress", "retain", "inherit")

class text_decoration(xsc.Element.Attrs):
	class text_decoration(xsc.TextAttr):
		xmlname = "text-decoration"

class text_shadow(xsc.Element.Attrs):
	class text_shadow(xsc.TextAttr):
		xmlname = "text-shadow"

class text_transform(xsc.Element.Attrs):
	class text_transform(xsc.TextAttr):
		xmlname = "text-transform"
		values = ("capitalize", "uppercase", "lowercase", "none", "inherit")

class fo(xsc.Namespace):
	xmlurl = "http://www.w3.org/1999/XSL/Format"

	class DocType10(xsc.DocType):
		"""
		document type for XSL (FO) 1.0
		"""
		def __init__(self):
			xsc.DocType.__init__(self, '???svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"')

	class root(xsc.Element):
		empty = False
		class Attrs(media_usage):
			pass

	class declarations(xsc.Element):
		empty = False

	class color_profile(xsc.Element):
		xmlname = "color-profile"
		empty = True
		class Attrs(src, color_profile_name, rendering_intent):
			pass

	class page_sequence(xsc.Element):
		xmlname = "page-sequence"
		empty = False
		class Attrs(
			country,
			format,
			language,
			letter_value,
			grouping_separator,
			grouping_size,
			initial_page_number,
			force_page_count,
			master_reference):
			class id(xsc.IDAttr): pass

	class layout_master_set(xsc.Element):
		xmlname = "layout-master-set"
		empty = False

	class page_sequence_master(xsc.Element):
		xmlname = "page-sequence-master"
		empty = False
		class Attrs(master_name):
			pass

	class single_page_master_reference(xsc.Element):
		xmlname = "single-page-master-reference"
		empty = True
		class Attrs(master_reference):
			pass

	class repeatable_page_master_reference(xsc.Element):
		xmlname = "repeatable-page-master-reference"
		empty = True
		class Attrs(master_reference, maximum_repeats):
			pass

	class repeatable_page_master_alternatives(xsc.Element):
		xmlname = "repeatable-page-master-alternatives"
		empty = False
		class Attrs(maximum_repeats):
			pass

	class conditional_page_master_reference(xsc.Element):
		xmlname = "conditional-page-master-reference"
		empty = True
		class Attrs(master_reference, page_position, odd_or_even, blank_or_not_blank):
			pass

	class simple_page_master(xsc.Element):
		xmlname = "simple-page-master"
		empty = False
		class Attrs(
			common_margin_properties_block,
			master_name,
			page_height,
			page_width,
			reference_orientation,
			writing_mode):
			pass

	class region_body(xsc.Element):
		xmlname = "region-body"
		empty = True
		class Attrs(
			common_border_padding_background_properties,
			common_margin_properties_block,
			clip,
			column_count,
			column_gap,
			display_align,
			overflow,
			reference_orientation,
			region_name,
			writing_mode):
			pass

	class region_before(xsc.Element):
		xmlname = "region-before"
		empty = True
		class Attrs(
			common_border_padding_background_properties,
			clip,
			display_align,
			extent,
			overflow,
			reference_orientation,
			region_name,
			precedence,
			writing_mode):
			pass

	class region_after(xsc.Element):
		xmlname = "region-after"
		empty = True
		class Attrs(
			common_border_padding_background_properties,
			clip,
			display_align,
			extent,
			overflow,
			reference_orientation,
			region_name,
			precedence,
			writing_mode):
			pass

	class region_start(xsc.Element):
		xmlname = "region-start"
		empty = True
		class Attrs(
			common_border_padding_background_properties,
			clip,
			display_align,
			extent,
			overflow,
			reference_orientation,
			region_name,
			writing_mode):
			pass

	class region_end(xsc.Element):
		xmlname = "region-end"
		empty = True
		class Attrs(
			common_border_padding_background_properties,
			clip,
			display_align,
			extent,
			overflow,
			reference_orientation,
			region_name,
			writing_mode):
			pass

	class flow(xsc.Element):
		empty = False
		class Attrs(flow_name):
			pass

	class static_content(xsc.Element):
		xmlname = "static-content"
		empty = False
		class Attrs(flow_name):
			pass

	class title(xsc.Element):
		empty = False
		class Attrs(
			common_accessibility_properties,
			common_aural_properties,
			common_border_padding_background_properties,
			common_font_properties,
			common_margin_properties_inline,
			color,
			line_height,
			visibility):
			pass

	class block(xsc.Element):
		empty = False
		class Attrs(
			common_accessibility_properties,
			common_aural_properties,
			common_border_padding_background_properties,
			common_font_properties,
			common_hyphenation_properties,
			common_margin_properties_block,
			common_relative_position_properties,
			break_after,
			break_before,
			color,
			text_depth,
			text_altitude,
			hyphenation_keep,
			hyphenation_ladder_count,
			intrusion_displace,
			keep_together,
			keep_with_next,
			keep_with_previous,
			last_line_end_indent,
			linefeed_treatment,
			line_height,
			line_height_shift_adjustment,
			line_stacking_strategy,
			orphans,
			white_space_treatment,
			span,
			text_align,
			text_align_last,
			text_indent,
			visibility,
			white_space_collapse,
			widows,
			wrap_option):
			class id(xsc.IDAttr): pass

	class block_container(xsc.Element):
		xmlname = "block-container"
		empty = False
		class Attrs(
			common_absolute_position_properties,
			common_border_padding_background_properties,
			common_margin_properties_block,
			block_progression_dimension,
			break_after,
			break_before,
			clip,
			display_align,
			height,
			inline_progression_dimension,
			intrusion_displace,
			keep_together,
			keep_with_next,
			keep_with_previous,
			overflow,
			reference_orientation,
			span,
			width,
			writing_mode,
			z_index):
			class id(xsc.IDAttr): pass

	class bidi_override(xsc.Element):
		xmlname = "bidi-override"
		empty = False
		class Attrs(
			common_aural_properties,
			common_font_properties,
			common_relative_position_properties,
			color,
			direction,
			letter_spacing,
			line_height,
			score_spaces,
			unicode_bidi,
			word_spacing):
			class id(xsc.IDAttr): pass

	class character(xsc.Element):
		empty = True
		class Attrs(
			common_aural_properties,
			common_border_padding_background_properties,
			common_font_properties,
			common_hyphenation_properties,
			common_margin_properties_inline,
			common_relative_position_properties,
			alignment_adjust,
			treat_as_word_space,
			alignment_baseline,
			baseline_shift,
			character,
			color,
			dominant_baseline,
			text_depth,
			text_altitude,
			glyph_orientation_horizontal,
			glyph_orientation_vertical,
			keep_with_next,
			keep_with_previous,
			letter_spacing,
			line_height,
			score_spaces,
			suppress_at_line_break,
			text_decoration,
			text_shadow,
			text_transform,
			visibility,
			word_spacing):
			class id(xsc.IDAttr): pass

	class initial_property_set(xsc.Element):
		xmlname = "initial-property-set"
		empty = True
		class Attrs(
			common_accessibility_properties,
			common_aural_properties,
			common_border_padding_background_properties,
			common_font_properties,
			common_relative_position_properties,
			color,
			letter_spacing,
			line_height,
			score_spaces,
			text_decoration,
			text_shadow,
			text_transform,
			word_spacing):
			class id(xsc.IDAttr): pass
