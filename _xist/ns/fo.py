#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains definitions for the
<link href="http://www.w3.org/TR/SVG/">&xsl;</link> 1.0 definition.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc


###
### Attributes
###

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


class size(xsc.Element.Attrs):
	class size(xsc.TextAttr):
		pass


class page_height(size):
	class page_height(xsc.TextAttr):
		xmlname = "page-height"


class page_width(size):
	class page_width(xsc.TextAttr):
		xmlname = "page-width"


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


class page_break_after(xsc.Element.Attrs):
	class page_break_after(xsc.TextAttr):
		xmlname = "page-break-after"
		values = ("auto", "always", "avoid", "left", "right", "inherit")


class break_after(page_break_after):
	class break_after(xsc.TextAttr):
		xmlname = "break-after"
		values = (" auto", "column", "page", "even-page", "odd-page", "inherit")


class page_break_before(xsc.Element.Attrs):
	class page_break_before(xsc.TextAttr):
		xmlname = "page-break-before"
		values = ("auto", "always", "avoid", "left", "right", "inherit")


class break_before(page_break_before):
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


class page_break_inside(xsc.Element.Attrs):
	class page_break_inside(xsc.TextAttr):
		xmlname = "page-break-inside"
		values = ("avoid", "auto", "inherit")


class keep_together(page_break_inside):
	class keep_together(xsc.TextAttr):
		xmlname = "keep-together"
	class keep_together_within_line(xsc.TextAttr):
		xmlname = "keep-together.within-line"
	class keep_together_within_column(xsc.TextAttr):
		xmlname = "keep-together.within-column"
	class keep_together_within_page(xsc.TextAttr):
		xmlname = "keep-together.within-page"


class keep_with_next(page_break_after):
	class keep_with_next(xsc.TextAttr):
		xmlname = "keep-with-next"
	class keep_with_next_within_line(xsc.TextAttr):
		xmlname = "keep-with-next.within-line"
	class keep_with_next_within_column(xsc.TextAttr):
		xmlname = "keep-with-next.within-column"
	class keep_with_next_within_page(xsc.TextAttr):
		xmlname = "keep-with-next.within-page"


class keep_with_previous(page_break_before):
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


class white_space(xsc.Element.Attrs):
	class white_space(xsc.TextAttr):
		xmlname = "white-space"
		values = ("normal", "pre", "nowrap", "inherit")


class linefeed_treatment(white_space):
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


class white_space_treatment(white_space):
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


class white_space_collapse(white_space):
	class white_space_collapse(xsc.TextAttr):
		xmlname = "white-space-collapse"
		values = ("false", "true", "inherit")


class widows(xsc.Element.Attrs):
	class widows(xsc.TextAttr):
		pass


class wrap_option(white_space):
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


class content_height(xsc.Element.Attrs):
	class content_height(xsc.TextAttr):
		xmlname = "content-height"


class content_width(xsc.Element.Attrs):
	class content_width(xsc.TextAttr):
		xmlname = "content-width"


class content_type(xsc.Element.Attrs):
	class content_type(xsc.TextAttr):
		xmlname = "content-type"


class scaling(xsc.Element.Attrs):
	class scaling(xsc.TextAttr):
		values = ("uniform", "non-uniform", "inherit")


class scaling_method(xsc.Element.Attrs):
	class scaling_method(xsc.TextAttr):
		xmlname = "scaling-method"
		values = ("auto", "integer-pixels", "resample-any-method", "inherit")


class id(xsc.Element.Attrs):
	class id(xsc.IDAttr):
		pass


class leader_alignment(xsc.Element.Attrs):
	class leader_alignment(xsc.TextAttr):
		xmlname = "leader-alignment"
		values = ("none", "reference-area", "page", "inherit")


class leader_pattern(xsc.Element.Attrs):
	class leader_pattern(xsc.TextAttr):
		xmlname = "leader-pattern"
		values = ("space", "rule", "dots", "use-content", "inherit")


class leader_pattern_width(xsc.Element.Attrs):
	class leader_pattern_width(xsc.TextAttr):
		xmlname = "leader-pattern-width"


class leader_length(xsc.Element.Attrs):
	class leader_length(xsc.TextAttr):
		xmlname = "leader-length"
	class leader_length_minimum(xsc.TextAttr):
		xmlname = "leader-length.minimum"
	class leader_length_optimum(xsc.TextAttr):
		xmlname = "leader-length.optimum"
	class leader_length_maximum(xsc.TextAttr):
		xmlname = "leader-length.maximum"


class rule_style(xsc.Element.Attrs):
	class rule_style(xsc.TextAttr):
		xmlname = "rule-style"
		values = ("none", "dotted", "dashed", "solid", "double", "groove", "ridge", "inherit")


class rule_thickness(xsc.Element.Attrs):
	class rule_thickness(xsc.TextAttr):
		xmlname = "rule-thickness"


class ref_id(xsc.Element.Attrs):
	class ref_id(xsc.TextAttr):
		xmlname = "ref-id"


class caption_side(xsc.Element.Attrs):
	class caption_side(xsc.TextAttr):
		xmlname = "caption-side"
		values = ("before", "after", "start", "end", "top", "bottom", "left", "right", "inherit")


class border_after_precedence(xsc.Element.Attrs):
	class border_after_precedence(xsc.TextAttr):
		xmlname = "border-after-precedence"


class border_before_precedence(xsc.Element.Attrs):
	class border_before_precedence(xsc.TextAttr):
		xmlname = "border-before-precedence"


class border_start_precedence(xsc.Element.Attrs):
	class border_start_precedence(xsc.TextAttr):
		xmlname = "border-start-precedence"


class border_end_precedence(xsc.Element.Attrs):
	class border_end_precedence(xsc.TextAttr):
		xmlname = "border-end-precedence"


class border_collapse(xsc.Element.Attrs):
	class border_collapse(xsc.TextAttr):
		xmlname = "border-collapse"
		values = ("collapse", "collapse-with-precedence", "separate", "inherit")


class border_separation(xsc.Element.Attrs):
	class border_separation(xsc.TextAttr):
		xmlname = "border-separation"
	class border_separation_block_progression_direction(xsc.TextAttr):
		xmlname = "border-separation.block-progression-direction"
	class border_separation_inline_progression_direction(xsc.TextAttr):
		xmlname = "border-separation.inline-progression-direction"
	class border_spacing(xsc.TextAttr):
		xmlname = "border-spacing"


class table_layout(xsc.Element.Attrs):
	class table_layout(xsc.TextAttr):
		xmlname = "table-layout"
		values = ("auto", "fixed", "inherit")


class table_omit_footer_at_break(xsc.Element.Attrs):
	class table_omit_footer_at_break(xsc.TextAttr):
		xmlname = "table-omit-footer-at-break"
		values = ("true", "false")


class table_omit_header_at_break(xsc.Element.Attrs):
	class table_omit_header_at_break(xsc.TextAttr):
		xmlname = "table-omit-header-at-break"
		values = ("true", "false")


class column_number(xsc.Element.Attrs):
	class column_number(xsc.TextAttr):
		xmlname = "column-number"


class column_width(xsc.Element.Attrs):
	class column_width(xsc.TextAttr):
		xmlname = "column-width"


class number_columns_repeated(xsc.Element.Attrs):
	class number_columns_repeated(xsc.TextAttr):
		xmlname = "number-columns-repeated"


class number_columns_spanned(xsc.Element.Attrs):
	class number_columns_spanned(xsc.TextAttr):
		xmlname = "number-columns-spanned"


class relative_align(xsc.Element.Attrs):
	class relative_align(xsc.TextAttr):
		xmlname = "relative-align"
		values = ("before", "baseline", "inherit")


class empty_cells(xsc.Element.Attrs):
	class empty_cells(xsc.TextAttr):
		xmlname = "empty-cells"
		values = ("show", "hide", "inherit")


class ends_row(xsc.Element.Attrs):
	class ends_row(xsc.TextAttr):
		xmlname = "ends-row"
		values = ("true", "false")


class starts_row(xsc.Element.Attrs):
	class starts_row(xsc.TextAttr):
		xmlname = "starts-row"
		values = ("true", "false")


class number_rows_spanned(xsc.Element.Attrs):
	class number_rows_spanned(xsc.TextAttr):
		xmlname = "number-rows-spanned"


class provisional_distance_between_starts(xsc.Element.Attrs):
	class provisional_distance_between_starts(xsc.TextAttr):
		xmlname = "provisional-distance-between-starts"


class provisional_label_separation(xsc.Element.Attrs):
	class provisional_label_separation(xsc.TextAttr):
		xmlname = "provisional-label-separation"


class destination_placement_offset(xsc.Element.Attrs):
	class destination_placement_offset(xsc.TextAttr):
		xmlname = "destination-placement-offset"


class external_destination(xsc.Element.Attrs):
	class external_destination(xsc.URLAttr):
		xmlname = "external-destination"


class indicate_destination(xsc.Element.Attrs):
	class indicate_destination(xsc.TextAttr):
		xmlname = "indicate-destination"
		values = ("true", "false")


class internal_destination(xsc.Element.Attrs):
	class internal_destination(xsc.TextAttr):
		xmlname = "internal-destination"


class show_destination(xsc.Element.Attrs):
	class show_destination(xsc.TextAttr):
		xmlname = "show-destination"
		values = ("replace", "new")


class auto_restore(xsc.Element.Attrs):
	class auto_restore(xsc.TextAttr):
		xmlname = "auto-restore"
		values = ("true", "false")


class starting_state(xsc.Element.Attrs):
	class starting_state(xsc.TextAttr):
		xmlname = "starting-state"
		values = ("show", "hide")


class switch_to(xsc.Element.Attrs):
	class switch_to(xsc.TextAttr):
		xmlname = "switch-to"


class target_presentation_context(xsc.Element.Attrs):
	class target_presentation_context(xsc.TextAttr):
		xmlname = "target-presentation-context"


class target_processing_context(xsc.Element.Attrs):
	class target_processing_context(xsc.TextAttr):
		xmlname = "target-processing-context"


class target_stylesheet(xsc.Element.Attrs):
	class target_stylesheet(xsc.TextAttr):
		xmlname = "target-stylesheet"


class case_name(xsc.Element.Attrs):
	class case_name(xsc.TextAttr):
		xmlname = "case-name"


class case_title(xsc.Element.Attrs):
	class case_title(xsc.TextAttr):
		xmlname = "case-title"


class active_state(xsc.Element.Attrs):
	class active_state(xsc.TextAttr):
		xmlname = "active-state"
		values = ("link", "visited", "active", "hover", "focus")


class float(xsc.Element.Attrs):
	class float(xsc.TextAttr):
		values = ("start", "end", "left", "right", "both", "none", "inherit")


class clear(xsc.Element.Attrs):
	class clear(xsc.TextAttr):
		values = ("start", "end", "left", "right", "both", "none", "inherit")


class marker_class_name(xsc.Element.Attrs):
	class marker_class_name(xsc.TextAttr):
		xmlname = "marker-class-name"


class common_margin_properties_block(xsc.Element.Attrs):
	class margin(xsc.TextAttr): pass
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
	class space_after(xsc.TextAttr): xmlname = "space-after"
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
	class space_start(xsc.TextAttr): xmlname = "space-start"
	class space_start_minimum(xsc.TextAttr): xmlname = "space-start.minimum"
	class space_start_optimum(xsc.TextAttr): xmlname = "space-start.optimum"
	class space_start_maximum(xsc.TextAttr): xmlname = "space-start.maximum"
	class space_start_conditionality(xsc.TextAttr): xmlname = "space-start.conditionality"
	class space_start_precedence(xsc.TextAttr): xmlname = "space-start.precedence"


class common_border_padding_background_properties(xsc.Element.Attrs):
	class background(xsc.TextAttr):
		pass
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
	class background_position(xsc.TextAttr):
		xmlname = "background-position"
	class background_position_horizontal(xsc.TextAttr):
		xmlname = "background-position-horizontal"
	class background_position_vertical(xsc.TextAttr):
		xmlname = "background-position-vertical"
	class border(xsc.TextAttr):
		pass
	class border_color(xsc.ColorAttr):
		xmlname = "border-color"
	class border_style(xsc.ColorAttr):
		xmlname = "border-style"
	class border_width(xsc.ColorAttr):
		xmlname = "border-width"
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
	class border_top(xsc.TextAttr):
		xmlname = "border-top"
	class border_top_color(xsc.ColorAttr):
		xmlname = "border-top-color"
	class border_top_style(xsc.TextAttr):
		xmlname = "border-top-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_top_width(xsc.TextAttr):
		xmlname = "border-top-width"
	class border_bottom(xsc.TextAttr):
		xmlname = "border-bottom"
	class border_bottom_color(xsc.ColorAttr):
		xmlname = "border-bottom-color"
	class border_bottom_style(xsc.TextAttr):
		xmlname = "border-bottom-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_bottom_width(xsc.TextAttr):
		xmlname = "border-bottom-width"
	class border_left(xsc.TextAttr):
		xmlname = "border-left"
	class border_left_color(xsc.ColorAttr):
		xmlname = "border-left-color"
	class border_left_style(xsc.TextAttr):
		xmlname = "border-left-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_left_width(xsc.TextAttr):
		xmlname = "border-left-width"
	class border_right(xsc.TextAttr):
		xmlname = "border-right"
	class border_right_color(xsc.ColorAttr):
		xmlname = "border-right-color"
	class border_right_style(xsc.TextAttr):
		xmlname = "border-right-style"
		values = ("none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "inherit")
	class border_right_width(xsc.TextAttr):
		xmlname = "border-right-width"
	class padding(xsc.TextAttr):
		xmlname = "padding"
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
	class cue(xsc.TextAttr): pass
	class cue_after(xsc.TextAttr): xmlname = "cue-after"
	class cue_before(xsc.TextAttr): xmlname = "cue-before"
	class elevation(xsc.TextAttr): pass
	class pause(xsc.TextAttr): pass
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
	class font(xsc.TextAttr):
		pass
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


class position(xsc.Element.Attrs):
	class position(xsc.TextAttr):
		values = ("static", "relative", "absolute", "fixed")


class common_relative_position_properties(position):
	class relative_position(xsc.TextAttr):
		xmlname = "relative-position"
		values = ("static", "relative", "inherit")


class common_absolute_position_properties(position):
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


class vertical_align(xsc.Element.Attrs):
	class vertical_align(xsc.TextAttr):
		xmlname = "vertical-align"


class alignment_adjust(vertical_align):
	class alignment_adjust(xsc.TextAttr):
		xmlname = "alignment-adjust"


class treat_as_word_space(xsc.Element.Attrs):
	class treat_as_word_space(xsc.TextAttr):
		xmlname = "treat-as-word-space"
		values = ("auto", "true", "false", "inherit")


class alignment_baseline(vertical_align):
	class alignment_baseline(xsc.TextAttr):
		xmlname = "alignment-baseline"
		values = ("auto", "baseline", "before-edge", "text-before-edge", "middle", "central", "after-edge", "text-after-edge", "ideographic", "alphabetic", "hanging", "mathematical", "inherit")


class baseline_shift(vertical_align):
	class baseline_shift(xsc.TextAttr):
		xmlname = "baseline-shift"


class character(xsc.Element.Attrs):
	class character(xsc.TextAttr):
		pass


class dominant_baseline(vertical_align):
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


class retrieve_class_name(xsc.Element.Attrs):
	class retrieve_class_name(xsc.TextAttr):
		xmlname = "retrieve-class-name"


class retrieve_position(xsc.Element.Attrs):
	class retrieve_position(xsc.TextAttr):
		xmlname = "retrieve-position"
		values = ("first-starting-within-page", "first-including-carryover", "last-starting-within-page", "last-ending-within-page")


class retrieve_boundary(xsc.Element.Attrs):
	class retrieve_boundary(xsc.TextAttr):
		xmlname = "retrieve-boundary"
		values = ("page", "page-sequence", "document")


class usage_context_of_suppress_at_line_break(xsc.Element.Attrs):
	class usage_context_of_suppress_at_line_break(xsc.TextAttr):
		xmlname = "usage-context-of-suppress-at-line-break"
		values = ("auto", "observe", "ignore", "inherit")


###
### Elements
### Attributes are only the applicable ones. Inheritable ones will be added afterwards
###

class color_profile(xsc.Element):
	xmlname = "color-profile"
	empty = True
	class Attrs(src, color_profile_name, rendering_intent):
		pass


class declarations(xsc.Element):
	empty = False
	class Attrs(
		# inheritable attributes
		color_profile.Attrs
		):
		pass


class root(xsc.Element):
	empty = False
	class Attrs(media_usage):
		pass


class page_sequence(xsc.Element):
	xmlname = "page-sequence"
	empty = False
	class Attrs(
		country,
		format,
		id,
		language,
		letter_value,
		grouping_separator,
		grouping_size,
		initial_page_number,
		force_page_count,
		master_reference):
		pass


class layout_master_set(xsc.Element):
	xmlname = "layout-master-set"
	empty = False
	class Attrs(xsc.Element.Attrs): # this is required, otherwise adding inherited attributes would modify xsc.Element.Attrs
		pass


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
		id,
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
		usage_context_of_suppress_at_line_break,
		visibility,
		white_space_collapse,
		widows,
		wrap_option):
		pass


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
		id,
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
		pass


class bidi_override(xsc.Element):
	xmlname = "bidi-override"
	empty = False
	class Attrs(
		common_aural_properties,
		common_font_properties,
		common_relative_position_properties,
		color,
		direction,
		id,
		letter_spacing,
		line_height,
		score_spaces,
		unicode_bidi,
		word_spacing):
		pass


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
		id,
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
		pass


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
		id,
		letter_spacing,
		line_height,
		score_spaces,
		text_decoration,
		text_shadow,
		text_transform,
		word_spacing):
		pass


class external_graphic(xsc.Element):
	xmlname = "external-graphic"
	empty = True
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		block_progression_dimension,
		clip,
		content_height,
		content_type,
		content_width,
		display_align,
		dominant_baseline,
		height,
		id,
		inline_progression_dimension,
		keep_with_next,
		keep_with_previous,
		line_height,
		overflow,
		scaling,
		scaling_method,
		src,
		text_align,
		width):
		pass


class instream_foreign_object(xsc.Element):
	xmlname = "instream-foreign-object"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		block_progression_dimension,
		clip,
		content_height,
		content_type,
		content_width,
		display_align,
		dominant_baseline,
		height,
		id,
		inline_progression_dimension,
		keep_with_next,
		keep_with_previous,
		line_height,
		overflow,
		scaling,
		scaling_method,
		text_align,
		width):
		pass


class inline(xsc.Element):
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		block_progression_dimension,
		color,
		dominant_baseline,
		height,
		id,
		inline_progression_dimension,
		keep_together,
		keep_with_next,
		keep_with_previous,
		line_height,
		text_decoration,
		usage_context_of_suppress_at_line_break,
		visibility,
		width,
		wrap_option):
		pass


class inline_container(xsc.Element):
	xmlname = "inline-container"
	empty = False
	class Attrs(
		common_border_padding_background_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		block_progression_dimension,
		clip,
		display_align,
		dominant_baseline,
		height,
		id,
		inline_progression_dimension,
		keep_together,
		keep_with_next,
		keep_with_previous,
		line_height,
		overflow,
		reference_orientation,
		width,
		writing_mode):
		pass


class leader(xsc.Element):
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		color,
		dominant_baseline,
		text_depth,
		text_altitude,
		id,
		keep_with_next,
		keep_with_previous,
		leader_alignment,
		leader_length,
		leader_pattern,
		leader_pattern_width,
		rule_style,
		rule_thickness,
		letter_spacing,
		line_height,
		text_shadow,
		visibility,
		word_spacing):
		pass


class page_number(xsc.Element):
	xmlname = "page-number"
	empty = True
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		dominant_baseline,
		id,
		keep_with_next,
		keep_with_previous,
		letter_spacing,
		line_height,
		score_spaces,
		text_altitude,
		text_decoration,
		text_depth,
		text_shadow,
		text_transform,
		usage_context_of_suppress_at_line_break,
		visibility,
		word_spacing,
		wrap_option):
		pass


class page_number_citation(xsc.Element):
	xmlname = "page-number-citation"
	empty = True
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_font_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		dominant_baseline,
		id,
		keep_with_next,
		keep_with_previous,
		letter_spacing,
		line_height,
		ref_id,
		score_spaces,
		text_altitude,
		text_decoration,
		text_depth,
		text_shadow,
		text_transform,
		usage_context_of_suppress_at_line_break,
		visibility,
		word_spacing,
		wrap_option):
		pass


class table_and_caption(xsc.Element):
	xmlname = "table-and-caption"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_margin_properties_block,
		common_relative_position_properties,
		break_after,
		break_before,
		caption_side,
		id,
		intrusion_displace,
		keep_together,
		keep_with_next,
		keep_with_previous,
		text_align):
		pass


class table(xsc.Element):
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_margin_properties_block,
		common_relative_position_properties,
		block_progression_dimension,
		border_after_precedence,
		border_before_precedence,
		border_collapse,
		border_end_precedence,
		border_separation,
		border_start_precedence,
		break_after,
		break_before,
		id,
		inline_progression_dimension,
		intrusion_displace,
		height,
		keep_together,
		keep_with_next,
		keep_with_previous,
		table_layout,
		table_omit_footer_at_break,
		table_omit_header_at_break,
		width,
		writing_mode):
		pass


class table_column(xsc.Element):
	xmlname = "table-column"
	empty = True
	class Attrs(
		common_border_padding_background_properties,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		column_number,
		column_width,
		number_columns_repeated,
		number_columns_spanned,
		visibility):
		pass


class table_caption(xsc.Element):
	xmlname = "table-caption"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		block_progression_dimension,
		height,
		id,
		inline_progression_dimension,
		intrusion_displace,
		keep_together,
		width):
		pass


class table_header(xsc.Element):
	xmlname = "table-header"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		id,
		visibility):
		pass


class table_footer(xsc.Element):
	xmlname = "table-footer"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		id,
		visibility):
		pass


class table_body(xsc.Element):
	xmlname = "table-body"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		id,
		visibility):
		pass


class table_row(xsc.Element):
	xmlname = "table-row"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		block_progression_dimension,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		break_after,
		break_before,
		id,
		height,
		keep_together,
		keep_with_next,
		keep_with_previous,
		visibility):
		pass


class table_cell(xsc.Element):
	xmlname = "table-cell"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_relative_position_properties,
		border_after_precedence,
		border_before_precedence,
		border_end_precedence,
		border_start_precedence,
		block_progression_dimension,
		column_number,
		display_align,
		relative_align,
		empty_cells,
		ends_row,
		height,
		id,
		inline_progression_dimension,
		number_columns_spanned,
		number_rows_spanned,
		starts_row,
		width):
		pass


class list_block(xsc.Element):
	xmlname = "list-block"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_margin_properties_block,
		common_relative_position_properties,
		break_after,
		break_before,
		id,
		intrusion_displace,
		keep_together,
		keep_with_next,
		keep_with_previous,
		provisional_distance_between_starts,
		provisional_label_separation):
		pass


class list_item(xsc.Element):
	xmlname = "list-item"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_margin_properties_block,
		common_relative_position_properties,
		break_after,
		break_before,
		id,
		intrusion_displace,
		keep_together,
		keep_with_next,
		keep_with_previous,
		relative_align):
		pass


class list_item_body(xsc.Element):
	xmlname = "list-item-body"
	empty = False
	class Attrs(
		common_accessibility_properties,
		id,
		keep_together):
		pass


class list_item_label(xsc.Element):
	xmlname = "list-item-label"
	empty = False
	class Attrs(
		common_accessibility_properties,
		id,
		keep_together):
		pass


class basic_link(xsc.Element):
	xmlname = "basic-link"
	empty = False
	class Attrs(
		common_accessibility_properties,
		common_aural_properties,
		common_border_padding_background_properties,
		common_margin_properties_inline,
		common_relative_position_properties,
		alignment_adjust,
		alignment_baseline,
		baseline_shift,
		destination_placement_offset,
		dominant_baseline,
		external_destination,
		id,
		indicate_destination,
		internal_destination,
		keep_together,
		keep_with_next,
		keep_with_previous,
		line_height,
		show_destination,
		target_processing_context,
		target_presentation_context,
		target_stylesheet):
		pass


class multi_switch(xsc.Element):
	xmlname = "multi-switch"
	empty = False
	class Attrs(
		common_accessibility_properties,
		auto_restore,
		id):
		pass


class multi_case(xsc.Element):
	xmlname = "multi-case"
	empty = False
	class Attrs(
		common_accessibility_properties,
		id,
		starting_state,
		case_name,
		case_title):
		pass


class multi_toggle(xsc.Element):
	xmlname = "multi-toggle"
	empty = False
	class Attrs(
		common_accessibility_properties,
		id,
		switch_to):
		pass


class multi_properties(xsc.Element):
	xmlname = "multi-properties"
	empty = False
	class Attrs(
		common_accessibility_properties,
		id):
		pass


class multi_property_set(xsc.Element):
	xmlname = "multi-property-set"
	empty = False
	class Attrs(
		id,
		active_state):
		pass


class float(xsc.Element):
	empty = False
	class Attrs(
		float,
		clear):
		pass


class footnote(xsc.Element):
	empty = False
	class Attrs(
		common_accessibility_properties
		):
		pass


class footnote_body(xsc.Element):
	xmlname = "footnote-body"
	empty = False
	class Attrs(
		common_accessibility_properties
		):
		pass


class wrapper(xsc.Element):
	empty = False
	class Attrs(
		id
		):
		pass


class marker(xsc.Element):
	empty = False
	class Attrs(
		marker_class_name
		):
		pass


class retrieve_marker(xsc.Element):
	xmlname = "retrieve-marker"
	empty = True
	class Attrs(
		retrieve_class_name,
		retrieve_position,
		retrieve_boundary
		):
		pass

# Parameter entities defined in the XSL specification
pe_block = (block, block_container, table_and_caption, table, list_block)
pe_inline = (bidi_override, character, external_graphic, instream_foreign_object, inline, inline_container, leader, page_number, page_number_citation, basic_link, multi_toggle)
pe_neutral = (multi_switch, multi_properties, wrapper, retrieve_marker)

# DTD information
dtd = {
	root: (layout_master_set, declarations, page_sequence),
	declarations: (color_profile,),
	page_sequence: (title, static_content, flow),
	layout_master_set: (simple_page_master, page_sequence_master),
	page_sequence_master: (single_page_master_reference, repeatable_page_master_reference, repeatable_page_master_alternatives),
	repeatable_page_master_alternatives: (conditional_page_master_reference,),
	simple_page_master: (region_body, region_before, region_after, region_start, region_end),
	flow: pe_block + (marker,),
	static_content: pe_block,
	title: pe_inline,
	block: pe_inline + pe_block,
	block_container: pe_block,
	bidi_override: pe_inline + pe_block,
	inline: pe_inline + pe_block,
	inline_container: pe_block,
	leader: pe_inline,
	table_and_caption: (table_caption, table),
	table: (table_column, table_header, table_footer, table_body),
	table_caption: pe_block + (marker,),
	table_header: (table_row, table_cell, marker),
	table_footer: (table_row, table_cell, marker),
	table_body: (table_row, table_cell, marker),
	table_row: (table_cell,),
	table_cell: pe_block + (marker,),
	list_block: (list_item, marker),
	list_item: (list_item_label, list_item_body, marker),
	list_item_body: pe_block + (marker,),
	list_item_label: pe_block + (marker,),
	basic_link: pe_inline + pe_block + (marker,),
	multi_switch: (multi_case,),
	multi_case: pe_inline + pe_block + (multi_toggle,), ### More attributes are allowed
	multi_toggle: pe_inline + pe_block,
	multi_properties: (multi_property_set, wrapper),
	float: pe_block,
	footnote: pe_inline + (footnote_body,),
	wrapper: pe_inline + pe_block + (marker,),
	marker: pe_inline + pe_block
}


class xmlns(xsc.Namespace):
	xmlname = "fo"
	xmlurl = "http://www.w3.org/1999/XSL/Format"
xmlns.makemod(vars())


# This function uses the DTD information from above to add inheritable attributes to the elements
def addinheritableattributes(element):
	if element in dtd: # if element hasn't been prcessed yet
		content = dtd[element] # fetch and delete content model from the DTD info
		del dtd[element]
		for child in content:
			if child is not element: # avoid endless recursion
				addinheritableattributes(child) # make sure the child element already have their inheritable attributes added
				for attr in child.Attrs.iterallowedvalues():
					if not element.Attrs.isallowed(attr.xmlname[0]):
						setattr(element.Attrs, attr.xmlname[0], attr) # add child attribute to element

for element in dtd.keys(): # use a copy of the keys, because we mutate the dict
	addinheritableattributes(element)

del dtd
