from docx import Document
from collections import defaultdict
import tempfile
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def get_color_formatting(run):
    if run.font.color and run.font.color.rgb:
        return str(run.font.color.rgb)
    return None

def get_highlight_color(run):
    if run.font.highlight_color:
        return str(run.font.highlight_color)
    return None

def extract_styles_from_paragraph(paragraph):
    alignment = paragraph.alignment

    font_names = set()
    font_sizes = set()
    font_colors = set()
    highlight_colors = set()
    small_caps = set()
    strikethroughs = set()
    shadows = set()
    bold = set()
    italic = set()
    underline = set()

    for run in paragraph.runs:
        if run.font.name:
            font_names.add(run.font.name)
        if run.font.size:
            font_sizes.add(f"{run.font.size.pt}pt")
        if run.font.color and run.font.color.rgb:
            font_colors.add(f"#{run.font.color.rgb}")
        if run.font.highlight_color:
            highlight_colors.add(run.font.highlight_color)
        if run.font.small_caps is not None:
            small_caps.add(run.font.small_caps)
        if run.font.strike is not None:
            strikethroughs.add(run.font.strike)
        if run.font.shadow is not None:
            shadows.add(run.font.shadow)
        if run.font.bold is not None:
            bold.add(run.font.bold)
        if run.font.italic is not None:
            italic.add(run.font.italic)
        if run.font.underline is not None:
            underline.add(run.font.underline)

    style_info = {
        'font-family': list(font_names) if font_names else None,
        'font-size': list(font_sizes) if font_sizes else None,
        'color': list(font_colors) if font_colors else None,
        'background-color': list(highlight_colors) if highlight_colors else None,
        'font-weight': list(bold) if bold else None,
        'font-style': list(italic) if italic else None,
        'text-decoration': list(underline) if underline else None,
        'text-align': str(alignment) if alignment else None,
        'padding-left': f"{paragraph.paragraph_format.left_indent.pt}pt" if paragraph.paragraph_format.left_indent else None,
        'padding-right': f"{paragraph.paragraph_format.right_indent.pt}pt" if paragraph.paragraph_format.right_indent else None,
        'margin-top': f"{paragraph.paragraph_format.space_before.pt}pt" if paragraph.paragraph_format.space_before else None,
        'margin-bottom': f"{paragraph.paragraph_format.space_after.pt}pt" if paragraph.paragraph_format.space_after else None,
        'line-height': str(paragraph.paragraph_format.line_spacing) if paragraph.paragraph_format.line_spacing else None,
        'font-variant': 'small-caps' if small_caps else None,
        'text-decoration-line': 'line-through' if strikethroughs else None,
        'text-shadow': '2px 2px 2px #000000' if shadows else None
    }

    return style_info

def extract_styles_from_document(doc_path):
    document = Document(doc_path)
    styles_info = defaultdict(list)

    for paragraph in document.paragraphs:
        style_info = extract_styles_from_paragraph(paragraph)
        if paragraph.style.name.startswith('Heading'):
            styles_info[paragraph.style.name].append(style_info)
        else:
            styles_info['Normal'].append(style_info)

    return styles_info

def summarize_styles(styles_info):
    summary = {}
    for style_name, styles in styles_info.items():
        font_families = set()
        font_sizes = set()
        colors = set()
        background_colors = set()
        text_aligns = set()
        paddings_left = set()
        paddings_right = set()
        margins_top = set()
        margins_bottom = set()
        line_heights = set()
        font_variants = set()
        text_decorations = set()
        text_shadows = set()
        font_weights = set()
        font_styles = set()

        for style in styles:
            font_families.update(filter(None, style['font-family'] if style['font-family'] else []))
            font_sizes.update(filter(None, style['font-size'] if style['font-size'] else []))
            colors.update(filter(None, style['color'] if style['color'] else []))
            background_colors.update(filter(None, style['background-color'] if style['background-color'] else []))
            if style['text-align']: text_aligns.add(style['text-align'])
            if style['padding-left']: paddings_left.add(style['padding-left'])
            if style['padding-right']: paddings_right.add(style['padding-right'])
            if style['margin-top']: margins_top.add(style['margin-top'])
            if style['margin-bottom']: margins_bottom.add(style['margin-bottom'])
            if style['line-height']: line_heights.add(style['line-height'])
            if style['font-variant']: font_variants.add(style['font-variant'])
            if style['text-decoration-line']: text_decorations.add(style['text-decoration-line'])
            if style['text-shadow']: text_shadows.add(style['text-shadow'])
            font_weights.update(filter(None, style['font-weight'] if style['font-weight'] else []))
            font_styles.update(filter(None, style['font-style'] if style['font-style'] else []))

        summary[style_name] = {
            'font-family': list(font_families),
            'font-size': list(font_sizes),
            'color': list(colors),
            'background-color': list(background_colors),
            'text-align': list(text_aligns),
            'padding-left': list(paddings_left),
            'padding-right': list(paddings_right),
            'margin-top': list(margins_top),
            'margin-bottom': list(margins_bottom),
            'line-height': list(line_heights),
            'font-variant': list(font_variants),
            'text-decoration-line': list(text_decorations),
            'text-shadow': list(text_shadows),
            'font-weight': list(font_weights),
            'font-style': list(font_styles),
        }

    return summary
