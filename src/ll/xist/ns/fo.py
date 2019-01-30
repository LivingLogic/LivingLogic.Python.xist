# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains definitions for the XSL__ 1.0 definition.

__ http://www.w3.org/TR/xsl11/
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.w3.org/1999/XSL/Format"


###
### Attributes
###

class media_usage(xsc.Attrs):
	class media_usage(xsc.TextAttr):
		xmlname = "media-usage"
		values = ("auto", "paginate", "bounded-in-one-dimension", "unbounded")


class src(xsc.Attrs):
	class src(xsc.URLAttr):
		pass


class color_profile_name(xsc.Attrs):
	class color_profile_name(xsc.TextAttr):
		xmlname = "color-profile-name"


class rendering_intent(xsc.Attrs):
	class rendering_intent(xsc.TextAttr):
		xmlname = "rendering-intent"
		values = ("auto", "perceptual", "relative-colorimetric", "saturation", "absolute-colorimetric", "inherit")


class country(xsc.Attrs):
	class country(xsc.TextAttr):
		pass


class format(xsc.Attrs):
	class format(xsc.TextAttr):
		pass


class language(xsc.Attrs):
	class language(xsc.TextAttr):
		pass


class letter_value(xsc.Attrs):
	class letter_value(xsc.TextAttr):
		xmlname = "letter-value"
		values = ("auto", "alphabetic", "traditional")


class grouping_separator(xsc.Attrs):
	class grouping_separator(xsc.TextAttr):
		xmlname = "grouping-separator"


class grouping_size(xsc.Attrs):
	class grouping_size(xsc.TextAttr):
		xmlname = "grouping-size"


class initial_page_number(xsc.Attrs):
	class initial_page_number(xsc.TextAttr):
		xmlname = "initial-page-number"


class force_page_count(xsc.Attrs):
	class force_page_count(xsc.TextAttr):
		xmlname = "force-page-count"
		values = ("auto", "even", "odd", "end-on-even", "end-on-odd", "no-force", "inherit")


class master_reference(xsc.Attrs):
	class master_reference(xsc.TextAttr):
		xmlname = "master-reference"


class master_name(xsc.Attrs):
	class master_name(xsc.TextAttr):
		xmlname = "master-name"


class maximum_repeats(xsc.Attrs):
	class maximum_repeats(xsc.TextAttr):
		xmlname = "maximum-repeats"


class page_position(xsc.Attrs):
	class page_position(xsc.TextAttr):
		xmlname = "page-position"
		values = ("first", "last", "rest", "any", "inherit")


class odd_or_even(xsc.Attrs):
	class odd_or_even(xsc.TextAttr):
		xmlname = "odd-or-even"
		values = ("odd", "even", "any", "inherit")


class blank_or_not_blank(xsc.Attrs):
	class blank_or_not_blank(xsc.TextAttr):
		xmlname = "blank-or-not-blank"
		values = ("blank", "not-blank", "any", "inherit")


class size(xsc.Attrs):
	class size(xsc.TextAttr):
		pass


class page_height(size):
	class page_height(xsc.TextAttr):
		xmlname = "page-height"


class page_width(size):
	class page_width(xsc.TextAttr):
		xmlname = "page-width"


class reference_orientation(xsc.Attrs):
	class reference_orientation(xsc.TextAttr):
		xmlname = "reference-orientation"
		values = (0, 90, 180, 270, -90, -180, -270, "inherit")


class writing_mode(xsc.Attrs):
	class writing_mode(xsc.TextAttr):
		xmlname = "writing-mode"
		values = ("lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb", "inherit")


class clip(xsc.Attrs):
	class clip(xsc.TextAttr):
		pass


class column_count(xsc.Attrs):
	class column_count(xsc.TextAttr):
		xmlname = "column-count"


class column_gap(xsc.Attrs):
	class column_gap(xsc.TextAttr):
		xmlname = "column-gap"


class display_align(xsc.Attrs):
	class display_align(xsc.TextAttr):
		xmlname = "display-align"
		values = ("auto", "before", "center", "after", "inherit")


class overflow(xsc.Attrs):
	class overflow(xsc.TextAttr):
		values = ("visible", "hidden", "scroll", "error-if-overflow", "auto", "inherit")


class region_name(xsc.Attrs):
	class region_name(xsc.TextAttr):
		xmlname = "region-name"


class extent(xsc.Attrs):
	class extent(xsc.TextAttr):
		pass


class precedence(xsc.Attrs):
	class precedence(xsc.TextAttr):
		values = ("true", "false", "inherit")


class flow_name(xsc.Attrs):
	class flow_name(xsc.TextAttr):
		xmlname = "flow-name"


class color(xsc.Attrs):
	class color(xsc.ColorAttr):
		pass


class line_height(xsc.Attrs):
	class line_height(xsc.TextAttr):
		xmlname = "line-height"


class visibility(xsc.Attrs):
	class visibility(xsc.TextAttr):
		values = ("visible", "hidden", "collapse", "inherit")


class page_break_after(xsc.Attrs):
	class page_break_after(xsc.TextAttr):
		xmlname = "page-break-after"
		values = ("auto", "always", "avoid", "left", "right", "inherit")


class break_after(page_break_after):
	class break_after(xsc.TextAttr):
		xmlname = "break-after"
		values = ("auto", "column", "page", "even-page", "odd-page", "inherit")


class page_break_before(xsc.Attrs):
	class page_break_before(xsc.TextAttr):
		xmlname = "page-break-before"
		values = ("auto", "always", "avoid", "left", "right", "inherit")


class break_before(page_break_before):
	class break_before(xsc.TextAttr):
		xmlname = "break-before"
		values = ("auto", "column", "page", "even-page", "odd-page", "inherit")


class text_depth(xsc.Attrs):
	class text_depth(xsc.TextAttr):
		xmlname = "text-depth"


class text_altitude(xsc.Attrs):
	class text_altitude(xsc.TextAttr):
		xmlname = "text-altitude"


class hyphenation_keep(xsc.Attrs):
	class hyphenation_keep(xsc.Attrs):
		xmlname = "hyphenation-keep"
		values = ("auto", "column", "page", "inherit")


class hyphenation_ladder_count(xsc.Attrs):
	class hyphenation_ladder_count(xsc.TextAttr):
		xmlname = "hyphenation-ladder-count"


class intrusion_displace(xsc.Attrs):
	class intrusion_displace(xsc.TextAttr):
		xmlname = "intrusion-displace"
		values = ("auto", "none", "line", "indent", "block", "inherit")


class page_break_inside(xsc.Attrs):
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


class last_line_end_indent(xsc.Attrs):
	class last_line_end_indent(xsc.TextAttr):
		xmlname = "last-line-end-indent"


class white_space(xsc.Attrs):
	class white_space(xsc.TextAttr):
		xmlname = "white-space"
		values = ("normal", "pre", "nowrap", "inherit")


class linefeed_treatment(white_space):
	class linefeed_treatment(xsc.TextAttr):
		xmlname = "linefeed-treatment"
		values = ("ignore", "preserve", "treat-as-space", "treat-as-zero-width-space", "inherit")


class line_height_shift_adjustment(xsc.Attrs):
	class line_height_shift_adjustment(xsc.TextAttr):
		xmlname = "line-height-shift-adjustment"
		values = ("consider-shifts", "disregard-shifts", "inherit")


class line_stacking_strategy(xsc.Attrs):
	class line_stacking_strategy(xsc.TextAttr):
		xmlname = "line-stacking-strategy"
		values = ("line-height", "font-height", "max-height", "inherit")


class orphans(xsc.Attrs):
	class orphans(xsc.TextAttr):
		pass


class white_space_treatment(white_space):
	class white_space_treatment(xsc.TextAttr):
		xmlname = "white-space-treatment"
		values = ("ignore", "preserve", "ignore-if-before-linefeed", "ignore-if-after-linefeed", "ignore-if-surrounding-linefeed", "inherit")


class span(xsc.Attrs):
	class span(xsc.TextAttr):
		values = ("none", "all", "inherit")


class text_align(xsc.Attrs):
	class text_align(xsc.TextAttr):
		xmlname = "text-align"


class text_align_last(xsc.Attrs):
	class text_align_last(xsc.TextAttr):
		xmlname = "text-align-last"
		values = ("relative", "start", "center", "end", "justify", "inside", "outside", "left", "right", "inherit")


class text_indent(xsc.Attrs):
	class text_indent(xsc.TextAttr):
		xmlname = "text-indent"


class white_space_collapse(white_space):
	class white_space_collapse(xsc.TextAttr):
		xmlname = "white-space-collapse"
		values = ("false", "true", "inherit")


class widows(xsc.Attrs):
	class widows(xsc.TextAttr):
		pass


class wrap_option(white_space):
	class wrap_option(xsc.TextAttr):
		xmlname = "wrap-option"
		values = ("no-wrap", "wrap", "inherit")


class score_spaces(xsc.Attrs):
	class score_spaces(xsc.TextAttr):
		xmlname = "score-spaces"
		values = ("true", "false", "inherit")


class text_decoration(xsc.Attrs):
	class text_decoration(xsc.TextAttr):
		xmlname = "text-decoration"


class content_height(xsc.Attrs):
	class content_height(xsc.TextAttr):
		xmlname = "content-height"


class content_width(xsc.Attrs):
	class content_width(xsc.TextAttr):
		xmlname = "content-width"


class content_type(xsc.Attrs):
	class content_type(xsc.TextAttr):
		xmlname = "content-type"


class scaling(xsc.Attrs):
	class scaling(xsc.TextAttr):
		values = ("uniform", "non-uniform", "inherit")


class scaling_method(xsc.Attrs):
	class scaling_method(xsc.TextAttr):
		xmlname = "scaling-method"
		values = ("auto", "integer-pixels", "resample-any-method", "inherit")


class id(xsc.Attrs):
	class id(xsc.IDAttr):
		pass


class leader_alignment(xsc.Attrs):
	class leader_alignment(xsc.TextAttr):
		xmlname = "leader-alignment"
		values = ("none", "reference-area", "page", "inherit")


class leader_pattern(xsc.Attrs):
	class leader_pattern(xsc.TextAttr):
		xmlname = "leader-pattern"
		values = ("space", "rule", "dots", "use-content", "inherit")


class leader_pattern_width(xsc.Attrs):
	class leader_pattern_width(xsc.TextAttr):
		xmlname = "leader-pattern-width"


class leader_length(xsc.Attrs):
	class leader_length(xsc.TextAttr):
		xmlname = "leader-length"
	class leader_length_minimum(xsc.TextAttr):
		xmlname = "leader-length.minimum"
	class leader_length_optimum(xsc.TextAttr):
		xmlname = "leader-length.optimum"
	class leader_length_maximum(xsc.TextAttr):
		xmlname = "leader-length.maximum"


class rule_style(xsc.Attrs):
	class rule_style(xsc.TextAttr):
		xmlname = "rule-style"
		values = ("none", "dotted", "dashed", "solid", "double", "groove", "ridge", "inherit")


class rule_thickness(xsc.Attrs):
	class rule_thickness(xsc.TextAttr):
		xmlname = "rule-thickness"


class ref_id(xsc.Attrs):
	class ref_id(xsc.TextAttr):
		xmlname = "ref-id"


class caption_side(xsc.Attrs):
	class caption_side(xsc.TextAttr):
		xmlname = "caption-side"
		values = ("before", "after", "start", "end", "top", "bottom", "left", "right", "inherit")


class border_after_precedence(xsc.Attrs):
	class border_after_precedence(xsc.TextAttr):
		xmlname = "border-after-precedence"


class border_before_precedence(xsc.Attrs):
	class border_before_precedence(xsc.TextAttr):
		xmlname = "border-before-precedence"


class border_start_precedence(xsc.Attrs):
	class border_start_precedence(xsc.TextAttr):
		xmlname = "border-start-precedence"


class border_end_precedence(xsc.Attrs):
	class border_end_precedence(xsc.TextAttr):
		xmlname = "border-end-precedence"


class border_collapse(xsc.Attrs):
	class border_collapse(xsc.TextAttr):
		xmlname = "border-collapse"
		values = ("collapse", "collapse-with-precedence", "separate", "inherit")


class border_separation(xsc.Attrs):
	class border_separation(xsc.TextAttr):
		xmlname = "border-separation"
	class border_separation_block_progression_direction(xsc.TextAttr):
		xmlname = "border-separation.block-progression-direction"
	class border_separation_inline_progression_direction(xsc.TextAttr):
		xmlname = "border-separation.inline-progression-direction"
	class border_spacing(xsc.TextAttr):
		xmlname = "border-spacing"


class table_layout(xsc.Attrs):
	class table_layout(xsc.TextAttr):
		xmlname = "table-layout"
		values = ("auto", "fixed", "inherit")


class table_omit_footer_at_break(xsc.Attrs):
	class table_omit_footer_at_break(xsc.TextAttr):
		xmlname = "table-omit-footer-at-break"
		values = ("true", "false")


class table_omit_header_at_break(xsc.Attrs):
	class table_omit_header_at_break(xsc.TextAttr):
		xmlname = "table-omit-header-at-break"
		values = ("true", "false")


class column_number(xsc.Attrs):
	class column_number(xsc.TextAttr):
		xmlname = "column-number"


class column_width(xsc.Attrs):
	class column_width(xsc.TextAttr):
		xmlname = "column-width"


class number_columns_repeated(xsc.Attrs):
	class number_columns_repeated(xsc.TextAttr):
		xmlname = "number-columns-repeated"


class number_columns_spanned(xsc.Attrs):
	class number_columns_spanned(xsc.TextAttr):
		xmlname = "number-columns-spanned"


class relative_align(xsc.Attrs):
	class relative_align(xsc.TextAttr):
		xmlname = "relative-align"
		values = ("before", "baseline", "inherit")


class empty_cells(xsc.Attrs):
	class empty_cells(xsc.TextAttr):
		xmlname = "empty-cells"
		values = ("show", "hide", "inherit")


class ends_row(xsc.Attrs):
	class ends_row(xsc.TextAttr):
		xmlname = "ends-row"
		values = ("true", "false")


class starts_row(xsc.Attrs):
	class starts_row(xsc.TextAttr):
		xmlname = "starts-row"
		values = ("true", "false")


class number_rows_spanned(xsc.Attrs):
	class number_rows_spanned(xsc.TextAttr):
		xmlname = "number-rows-spanned"


class provisional_distance_between_starts(xsc.Attrs):
	class provisional_distance_between_starts(xsc.TextAttr):
		xmlname = "provisional-distance-between-starts"


class provisional_label_separation(xsc.Attrs):
	class provisional_label_separation(xsc.TextAttr):
		xmlname = "provisional-label-separation"


class destination_placement_offset(xsc.Attrs):
	class destination_placement_offset(xsc.TextAttr):
		xmlname = "destination-placement-offset"


class external_destination(xsc.Attrs):
	class external_destination(xsc.URLAttr):
		xmlname = "external-destination"


class indicate_destination(xsc.Attrs):
	class indicate_destination(xsc.TextAttr):
		xmlname = "indicate-destination"
		values = ("true", "false")


class internal_destination(xsc.Attrs):
	class internal_destination(xsc.TextAttr):
		xmlname = "internal-destination"


class show_destination(xsc.Attrs):
	class show_destination(xsc.TextAttr):
		xmlname = "show-destination"
		values = ("replace", "new")


class auto_restore(xsc.Attrs):
	class auto_restore(xsc.TextAttr):
		xmlname = "auto-restore"
		values = ("true", "false")


class starting_state(xsc.Attrs):
	class starting_state(xsc.TextAttr):
		xmlname = "starting-state"
		values = ("show", "hide")


class switch_to(xsc.Attrs):
	class switch_to(xsc.TextAttr):
		xmlname = "switch-to"


class target_presentation_context(xsc.Attrs):
	class target_presentation_context(xsc.TextAttr):
		xmlname = "target-presentation-context"


class target_processing_context(xsc.Attrs):
	class target_processing_context(xsc.TextAttr):
		xmlname = "target-processing-context"


class target_stylesheet(xsc.Attrs):
	class target_stylesheet(xsc.TextAttr):
		xmlname = "target-stylesheet"


class case_name(xsc.Attrs):
	class case_name(xsc.TextAttr):
		xmlname = "case-name"


class case_title(xsc.Attrs):
	class case_title(xsc.TextAttr):
		xmlname = "case-title"


class active_state(xsc.Attrs):
	class active_state(xsc.TextAttr):
		xmlname = "active-state"
		values = ("link", "visited", "active", "hover", "focus")


class float(xsc.Attrs):
	class float(xsc.TextAttr):
		values = ("start", "end", "left", "right", "both", "none", "inherit")


class clear(xsc.Attrs):
	class clear(xsc.TextAttr):
		values = ("start", "end", "left", "right", "both", "none", "inherit")


class marker_class_name(xsc.Attrs):
	class marker_class_name(xsc.TextAttr):
		xmlname = "marker-class-name"


class common_margin_properties_block(xsc.Attrs):
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


class common_margin_properties_inline(xsc.Attrs):
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


class common_border_padding_background_properties(xsc.Attrs):
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


class common_accessibility_properties(xsc.Attrs):
	class source_document(xsc.TextAttr): xmlname = "source-document"
	class role(xsc.TextAttr): pass


class common_aural_properties(xsc.Attrs):
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


class common_font_properties(xsc.Attrs):
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


class position(xsc.Attrs):
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


class block_progression_dimension(xsc.Attrs):
	class block_progression_dimension(xsc.TextAttr):
		xmlname = "block-progression-dimension"
	class block_progression_dimension_minimum(xsc.TextAttr):
		xmlname = "block-progression-dimension.minimum"
	class block_progression_dimension_optimum(xsc.TextAttr):
		xmlname = "block-progression-dimension.optimum"
	class block_progression_dimension_maximum(xsc.TextAttr):
		xmlname = "block-progression-dimension.maximum"


class inline_progression_dimension(xsc.Attrs):
	class inline_progression_dimension(xsc.TextAttr):
		xmlname = "inline-progression-dimension"
	class inline_progression_dimension_minimum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.minimum"
	class inline_progression_dimension_optimum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.optimum"
	class inline_progression_dimension_maximum(xsc.TextAttr):
		xmlname = "inline-progression-dimension.maximum"


class height(xsc.Attrs):
	class height(xsc.TextAttr):
		pass


class width(xsc.Attrs):
	class width(xsc.TextAttr):
		pass


class z_index(xsc.Attrs):
	class z_index(xsc.TextAttr):
		xmlname = "z-index"


class direction(xsc.Attrs):
	class direction(xsc.TextAttr):
		values = ("ltr", "rtl", "inherit")


class letter_spacing(xsc.Attrs):
	class letter_spacing(xsc.TextAttr):
		xmlname = "letter-spacing"


class unicode_bidi(xsc.Attrs):
	class unicode_bidi(xsc.TextAttr):
		xmlname = "unicode-bidi"
		values = ("normal", "embed", "bidi-override", "inherit")


class word_spacing(xsc.Attrs):
	class word_spacing(xsc.TextAttr):
		xmlname = "word-spacing"


class vertical_align(xsc.Attrs):
	class vertical_align(xsc.TextAttr):
		xmlname = "vertical-align"


class alignment_adjust(vertical_align):
	class alignment_adjust(xsc.TextAttr):
		xmlname = "alignment-adjust"


class treat_as_word_space(xsc.Attrs):
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


class character(xsc.Attrs):
	class character(xsc.TextAttr):
		pass


class dominant_baseline(vertical_align):
	class dominant_baseline(xsc.TextAttr):
		xmlname = "dominant-baseline"
		values = ("auto", "use-script", "no-change", "reset-size", "ideographic", "alphabetic", "hanging", "mathematical", "central", "middle", "text-after-edge", "text-before-edge", "inherit")


class glyph_orientation_horizontal(xsc.Attrs):
	class glyph_orientation_horizontal(xsc.TextAttr):
		xmlname = "glyph-orientation-horizontal"


class glyph_orientation_vertical(xsc.Attrs):
	class glyph_orientation_vertical(xsc.TextAttr):
		xmlname = "glyph-orientation-vertical"


class suppress_at_line_break(xsc.Attrs):
	class suppress_at_line_break(xsc.TextAttr):
		xmlname = "suppress-at-line-break"
		values = ("auto", "suppress", "retain", "inherit")


class text_decoration(xsc.Attrs):
	class text_decoration(xsc.TextAttr):
		xmlname = "text-decoration"


class text_shadow(xsc.Attrs):
	class text_shadow(xsc.TextAttr):
		xmlname = "text-shadow"


class text_transform(xsc.Attrs):
	class text_transform(xsc.TextAttr):
		xmlname = "text-transform"
		values = ("capitalize", "uppercase", "lowercase", "none", "inherit")


class retrieve_class_name(xsc.Attrs):
	class retrieve_class_name(xsc.TextAttr):
		xmlname = "retrieve-class-name"


class retrieve_position(xsc.Attrs):
	class retrieve_position(xsc.TextAttr):
		xmlname = "retrieve-position"
		values = ("first-starting-within-page", "first-including-carryover", "last-starting-within-page", "last-ending-within-page")


class retrieve_boundary(xsc.Attrs):
	class retrieve_boundary(xsc.TextAttr):
		xmlname = "retrieve-boundary"
		values = ("page", "page-sequence", "document")


class usage_context_of_suppress_at_line_break(xsc.Attrs):
	class usage_context_of_suppress_at_line_break(xsc.TextAttr):
		xmlname = "usage-context-of-suppress-at-line-break"
		values = ("auto", "observe", "ignore", "inherit")


###
### Elements
### Only applicable attributes are specified at class creation time.
### Inheritable attributes will be added afterwards.
### The schema information will be added in the same step.
###

class color_profile(xsc.Element):
	xmlns = xmlns
	xmlname = "color-profile"
	class Attrs(src, color_profile_name, rendering_intent):
		pass


class declarations(xsc.Element):
	xmlns = xmlns
	class Attrs(
		# inheritable attributes
		color_profile.Attrs
		):
		pass


class root(xsc.Element):
	xmlns = xmlns
	class Attrs(media_usage):
		pass


class page_sequence(xsc.Element):
	xmlns = xmlns
	xmlname = "page-sequence"
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
	xmlns = xmlns
	xmlname = "layout-master-set"
	class Attrs(xsc.Element.Attrs): # this is required, otherwise adding inherited attributes would modify xsc.Element.Attrs
		pass


class page_sequence_master(xsc.Element):
	xmlns = xmlns
	xmlname = "page-sequence-master"
	class Attrs(master_name):
		pass


class single_page_master_reference(xsc.Element):
	xmlns = xmlns
	xmlname = "single-page-master-reference"
	class Attrs(master_reference):
		pass


class repeatable_page_master_reference(xsc.Element):
	xmlns = xmlns
	xmlname = "repeatable-page-master-reference"
	class Attrs(master_reference, maximum_repeats):
		pass


class repeatable_page_master_alternatives(xsc.Element):
	xmlns = xmlns
	xmlname = "repeatable-page-master-alternatives"
	class Attrs(maximum_repeats):
		pass


class conditional_page_master_reference(xsc.Element):
	xmlns = xmlns
	xmlname = "conditional-page-master-reference"
	class Attrs(master_reference, page_position, odd_or_even, blank_or_not_blank):
		pass


class simple_page_master(xsc.Element):
	xmlns = xmlns
	xmlname = "simple-page-master"
	class Attrs(
		common_margin_properties_block,
		master_name,
		page_height,
		page_width,
		reference_orientation,
		writing_mode):
		pass


class region_body(xsc.Element):
	xmlns = xmlns
	xmlname = "region-body"
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
	xmlns = xmlns
	xmlname = "region-before"
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
	xmlns = xmlns
	xmlname = "region-after"
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
	xmlns = xmlns
	xmlname = "region-start"
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
	xmlns = xmlns
	xmlname = "region-end"
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
	xmlns = xmlns
	class Attrs(flow_name):
		pass


class static_content(xsc.Element):
	xmlns = xmlns
	xmlname = "static-content"
	class Attrs(flow_name):
		pass


class title(xsc.Element):
	xmlns = xmlns
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
	xmlns = xmlns
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
	xmlns = xmlns
	xmlname = "block-container"
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
	xmlns = xmlns
	xmlname = "bidi-override"
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
	xmlns = xmlns
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
	xmlns = xmlns
	xmlname = "initial-property-set"
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
	xmlns = xmlns
	xmlname = "external-graphic"
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
	xmlns = xmlns
	xmlname = "instream-foreign-object"
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
	xmlns = xmlns
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
	xmlns = xmlns
	xmlname = "inline-container"
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
	xmlns = xmlns
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
	xmlns = xmlns
	xmlname = "page-number"
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
	xmlns = xmlns
	xmlname = "page-number-citation"
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
	xmlns = xmlns
	xmlname = "table-and-caption"
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
	xmlns = xmlns
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
	xmlns = xmlns
	xmlname = "table-column"
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
	xmlns = xmlns
	xmlname = "table-caption"
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
	xmlns = xmlns
	xmlname = "table-header"
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
	xmlns = xmlns
	xmlname = "table-footer"
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
	xmlns = xmlns
	xmlname = "table-body"
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
	xmlns = xmlns
	xmlname = "table-row"
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
	xmlns = xmlns
	xmlname = "table-cell"
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
	xmlns = xmlns
	xmlname = "list-block"
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
	xmlns = xmlns
	xmlname = "list-item"
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
	xmlns = xmlns
	xmlname = "list-item-body"
	class Attrs(
		common_accessibility_properties,
		id,
		keep_together):
		pass


class list_item_label(xsc.Element):
	xmlns = xmlns
	xmlname = "list-item-label"
	class Attrs(
		common_accessibility_properties,
		id,
		keep_together):
		pass


class basic_link(xsc.Element):
	xmlns = xmlns
	xmlname = "basic-link"
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
	xmlns = xmlns
	xmlname = "multi-switch"
	class Attrs(
		common_accessibility_properties,
		auto_restore,
		id):
		pass


class multi_case(xsc.Element):
	xmlns = xmlns
	xmlname = "multi-case"
	class Attrs(
		common_accessibility_properties,
		id,
		starting_state,
		case_name,
		case_title):
		pass


class multi_toggle(xsc.Element):
	xmlns = xmlns
	xmlname = "multi-toggle"
	class Attrs(
		common_accessibility_properties,
		id,
		switch_to):
		pass


class multi_properties(xsc.Element):
	xmlns = xmlns
	xmlname = "multi-properties"
	class Attrs(
		common_accessibility_properties,
		id):
		pass


class multi_property_set(xsc.Element):
	xmlns = xmlns
	xmlname = "multi-property-set"
	class Attrs(
		id,
		active_state):
		pass


class float(xsc.Element):
	xmlns = xmlns
	class Attrs(
		float,
		clear):
		pass


class footnote(xsc.Element):
	xmlns = xmlns
	class Attrs(
		common_accessibility_properties
		):
		pass


class footnote_body(xsc.Element):
	xmlns = xmlns
	xmlname = "footnote-body"
	class Attrs(
		common_accessibility_properties
		):
		pass


class wrapper(xsc.Element):
	xmlns = xmlns
	class Attrs(
		id
		):
		pass


class marker(xsc.Element):
	xmlns = xmlns
	class Attrs(
		marker_class_name
		):
		pass


class retrieve_marker(xsc.Element):
	xmlns = xmlns
	xmlname = "retrieve-marker"
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
	root: sims.Elements(layout_master_set, declarations, page_sequence),
	declarations: sims.Elements(color_profile),
	page_sequence: sims.Elements(title, static_content, flow),
	layout_master_set: sims.Elements(simple_page_master, page_sequence_master),
	page_sequence_master: sims.Elements(single_page_master_reference, repeatable_page_master_reference, repeatable_page_master_alternatives),
	repeatable_page_master_alternatives: sims.Elements(conditional_page_master_reference),
	simple_page_master: sims.Elements(region_body, region_before, region_after, region_start, region_end),
	flow: sims.Elements(*(pe_block + (marker,))),
	static_content: sims.Elements(*pe_block),
	title: sims.ElementsOrText(*pe_inline),
	block: sims.ElementsOrText(*(pe_inline + pe_block)),
	block_container: sims.Elements(*pe_block),
	bidi_override: sims.ElementsOrText(*(pe_inline + pe_block)),
	inline: sims.ElementsOrText(*(pe_inline + pe_block)),
	inline_container: sims.Elements(*pe_block),
	leader: sims.ElementsOrText(*pe_inline),
	table_and_caption: sims.Elements(table_caption, table),
	table: sims.Elements(table_column, table_header, table_footer, table_body),
	table_caption: sims.Elements(*(pe_block + (marker,))),
	table_header: sims.Elements(table_row, table_cell, marker),
	table_footer: sims.Elements(table_row, table_cell, marker),
	table_body: sims.Elements(table_row, table_cell, marker),
	table_row: sims.Elements(table_cell),
	table_cell: sims.Elements(*(pe_block + (marker,))),
	list_block: sims.Elements(list_item, marker),
	list_item: sims.Elements(list_item_label, list_item_body, marker),
	list_item_body: sims.Elements(*(pe_block + (marker,))),
	list_item_label: sims.Elements(*(pe_block + (marker,))),
	basic_link: sims.ElementsOrText(*(pe_inline + pe_block + (marker,))),
	multi_switch: sims.Elements(multi_case),
	multi_case: sims.ElementsOrText(*(pe_inline + pe_block + (multi_toggle,))), ### FIXME: More attributes are allowed
	multi_toggle: sims.ElementsOrText(*(pe_inline + pe_block)),
	multi_properties: sims.Elements(multi_property_set, wrapper),
	float: sims.Elements(*pe_block),
	footnote: sims.Elements(*(pe_inline + (footnote_body,))),
	footnote_body: sims.Elements(*pe_block),
	wrapper: sims.ElementsOrText(*(pe_inline + pe_block + (marker,))),
	marker: sims.ElementsOrText(*(pe_inline + pe_block)),
	region_before: sims.Empty(),
	single_page_master_reference: sims.Empty(),
	region_after: sims.Empty(),
	external_graphic: sims.Empty(),
	repeatable_page_master_reference: sims.Empty(),
	initial_property_set: sims.Empty(),
	instream_foreign_object: sims.NoElementsOrText(), # content is from a different namespace
	character: sims.Empty(),
	page_number: sims.Empty(),
	table_column: sims.Empty(),
	conditional_page_master_reference: sims.Empty(),
	color_profile: sims.Empty(),
	page_number_citation: sims.Empty(),
	region_start: sims.Empty(),
	retrieve_marker: sims.Empty(),
	region_body: sims.Empty(),
	multi_property_set: sims.Empty(),
	region_end: sims.Empty(),
}


# This function uses the DTD information from above to add inheritable attributes and schema information to the elements
def fixattributesandmodel(element):
	if element in dtd: # if element hasn't been processed yet
		model = dtd.pop(element) # fetch and delete content model from the DTD info

		# Add schema information
		element.model = model
		if isinstance(model, (sims.Elements, sims.ElementsOrText)):
			for child in model.elements:
				if child is not element: # avoid endless recursion
					fixattributesandmodel(child) # make sure the child element already have their inheritable attributes added
					for attr in child.Attrs.declaredattrs():
						if not element.Attrs.isdeclared(attr):
							element.Attrs.add(attr) # add child attribute to element

varitems = list(vars().items())

for (key, value) in varitems:
	if isinstance(value, xsc._Element_Meta):
		fixattributesandmodel(value)

# make sure, we assigned a model to every element
for (key, value) in varitems:
	if isinstance(value, xsc._Element_Meta):
		assert value.model is not None

# don't pollute the namespace
del dtd
del fixattributesandmodel
del varitems
