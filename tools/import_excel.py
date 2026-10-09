"""Compile the source workbook into compact, exact cell geometry (stdlib only)."""
import colorsys
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
S = '{' + NS['s'] + '}'


def cell_position(address):
    letters, row = re.fullmatch(r'([A-Z]+)(\d+)', address).groups()
    column = 0
    for letter in letters:
        column = column * 26 + ord(letter) - 64
    return int(row), column


def bounds(address):
    first, _, last = address.partition(':')
    r0, c0 = cell_position(first)
    r1, c1 = cell_position(last or first)
    return r0, c0, r1, c1


def coalesce(intervals):
    """Union touching intervals without joining separate gaps."""
    output = []
    for first, last in sorted(set(intervals)):
        if output and first <= output[-1][1]:
            output[-1][1] = max(last, output[-1][1])
        else:
            output.append([first, last])
    return output


def compile_workbook(source):
    with zipfile.ZipFile(source) as archive:
        styles = ET.fromstring(archive.read('xl/styles.xml'))
        scheme = ET.fromstring(archive.read('xl/theme/theme1.xml')).find('.//a:clrScheme', NS)
        theme = {e.tag.split('}')[-1]: list(e)[0].get('lastClr', list(e)[0].get('val')) for e in scheme}
        theme_order = ['lt1', 'dk1', 'lt2', 'dk2', 'accent1', 'accent2', 'accent3',
                       'accent4', 'accent5', 'accent6', 'hlink', 'folHlink']

        def color(node, default='#000000'):
            if node is None:
                return default
            if 'rgb' in node.attrib:
                value = node.get('rgb')[-6:]
            elif 'theme' in node.attrib:
                value = theme[theme_order[int(node.get('theme'))]]
            elif node.get('indexed') in ('0', '8', '64') or node.get('auto') == '1':
                return '#000000'
            elif node.get('indexed') in ('1', '9', '65'):
                return '#FFFFFF'
            else:
                raise ValueError(f'Unsupported workbook color: {node.attrib}')
            tint = float(node.get('tint', 0))
            if tint:
                rgb = [int(value[i:i+2], 16) / 255 for i in (0, 2, 4)]
                h, l, s = colorsys.rgb_to_hls(*rgb)
                l = l * (1 + tint) if tint < 0 else l * (1 - tint) + tint
                value = ''.join(f'{round(v * 255):02X}' for v in colorsys.hls_to_rgb(h, l, s))
            return '#' + value

        fills = []
        for fill in styles.find('s:fills', NS):
            pattern = fill.find('s:patternFill', NS)
            fills.append(color(pattern.find('s:fgColor', NS))
                         if pattern is not None and pattern.get('patternType') == 'solid' else None)
        fonts = []
        for font in styles.find('s:fonts', NS):
            fonts.append({'size': float(font.find('s:sz', NS).get('val')),
                          'color': color(font.find('s:color', NS)),
                          'bold': font.find('s:b', NS) is not None,
                          'family': font.find('s:name', NS).get('val')})
        borders = []
        for border in styles.find('s:borders', NS):
            edges = {}
            for side in ('left', 'right', 'top', 'bottom'):
                edge = border.find('s:' + side, NS)
                if edge is not None and edge.get('style'):
                    edges[side] = [edge.get('style'), color(edge.find('s:color', NS))]
            borders.append(edges)
        formats = list(styles.find('s:cellXfs', NS))
        strings = [''.join(n.text or '' for n in e.iter(S + 't'))
                   for e in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        rels = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r.get('Target').lstrip('/') for r in rels}
        output = {'source': source.name, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                  'coordinate_units': 'Approximate Excel pixels at 96 DPI; not physical warehouse dimensions',
                  'sheets': {}}
        for sheet in workbook.find('s:sheets', NS):
            target = targets[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            root = ET.fromstring(archive.read(target if target.startswith('xl/') else 'xl/' + target))
            default = root.find('s:sheetFormatPr', NS)
            cells, texts, row_heights = {}, [], {}
            for row in root.findall('s:sheetData/s:row', NS):
                row_heights[int(row.get('r'))] = 0 if row.get('hidden') == '1' else float(row.get('ht', default.get('defaultRowHeight')))
                for cell in row.findall('s:c', NS):
                    position = cell_position(cell.get('r'))
                    style = int(cell.get('s', 0))
                    cells[position] = style
                    value = cell.find('s:v', NS)
                    inline = cell.find('s:is', NS)
                    if cell.get('t') == 's' and value is not None:
                        text = strings[int(value.text)]
                    elif inline is not None:
                        text = ''.join(n.text or '' for n in inline.iter(S + 't'))
                    else:
                        text = value.text if value is not None else None
                    if text is not None and text.strip():
                        texts.append({'cell': cell.get('r'), 'text': text, 'style': style})
            meaningful = [p for p, style in cells.items() if fills[int(formats[style].get('fillId', 0))]]
            meaningful += [cell_position(t['cell']) for t in texts]
            merges = [m.get('ref') for m in root.findall('s:mergeCells/s:mergeCell', NS)]
            # Merges can extend beyond the text anchor; retain their full bounds.
            for address in merges:
                r0, c0, r1, c1 = bounds(address)
                meaningful.extend([(r0, c0), (r1, c1)])
            max_row = max(r for r, _ in meaningful)
            max_col = max(c for _, c in meaningful)
            widths = [float(default.get('defaultColWidth', '8.43'))] * max_col
            for col in root.findall('s:cols/s:col', NS):
                for i in range(int(col.get('min')) - 1, min(int(col.get('max')), max_col)):
                    widths[i] = 0 if col.get('hidden') == '1' else float(col.get('width', widths[i]))
            x = [0]
            for width in widths:
                x.append(x[-1] + (math.floor(width * 7 + 5) if width else 0))
            y = [0]
            for r in range(1, max_row + 1):
                y.append(y[-1] + row_heights.get(r, float(default.get('defaultRowHeight'))) * 4 / 3)
            rectangles, active = [], {}
            line_groups = {}
            for r in range(1, max_row + 1):
                spans = []
                for c in range(1, max_col + 1):
                    style = formats[cells.get((r, c), 0)]
                    fill = fills[int(style.get('fillId', 0))]
                    if fill:
                        if spans and spans[-1][2] == fill and spans[-1][1] == c - 1:
                            spans[-1][1] = c
                        else:
                            spans.append([c - 1, c, fill])
                    for side, (kind, edge_color) in borders[int(style.get('borderId', 0))].items():
                        axis = 'v' if side in ('left', 'right') else 'h'
                        fixed = (x[c - 1] if side == 'left' else x[c]) if axis == 'v' else (y[r - 1] if side == 'top' else y[r])
                        interval = (y[r - 1], y[r]) if axis == 'v' else (x[c - 1], x[c])
                        line_groups.setdefault((axis, fixed, kind, edge_color), []).append(interval)
                current = {}
                for c0, c1, fill in spans:
                    key = (c0, c1, fill)
                    if key in active:
                        rect = active[key]
                        rect[3] = y[r]
                    else:
                        rect = [x[c0], y[r - 1], x[c1], y[r], fill]
                        rectangles.append(rect)
                    current[key] = rect
                active = current
            lines = []
            for (axis, fixed, kind, edge_color), intervals in sorted(line_groups.items()):
                for first, last in coalesce(intervals):
                    lines.append([fixed, first, fixed, last, kind, edge_color] if axis == 'v'
                                 else [first, fixed, last, fixed, kind, edge_color])
            merge_map = {m.split(':')[0]: m for m in merges}
            for text in texts:
                style = formats[text.pop('style')]
                text['range'] = merge_map.get(text['cell'], text['cell'])
                r0, c0, r1, c1 = bounds(text['range'])
                text['box'] = [x[c0 - 1], y[r0 - 1], x[c1], y[r1]]
                text['font'] = fonts[int(style.get('fontId', 0))]
                alignment = style.find('s:alignment', NS)
                text['alignment'] = alignment.attrib if alignment is not None else {}
                text['merged'] = text['cell'] in merge_map
            output['sheets'][sheet.get('name')] = {
                'width': x[-1], 'height': y[-1], 'rectangles': rectangles,
                'lines': lines, 'texts': texts, 'merges': merges,
                'row_heights_points': [row_heights.get(r, float(default.get('defaultRowHeight'))) for r in range(1, max_row + 1)],
                'column_widths_excel': widths,
                'source_used_range': root.find('s:dimension', NS).get('ref'),
            }
        return output


if __name__ == '__main__':
    data = compile_workbook(ROOT / 'data/layout.xlsx')
    destination = ROOT / 'data/floors.json'
    destination.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    for name, floor in data['sheets'].items():
        print(name, len(floor['rectangles']), 'rectangles;', len(floor['lines']), 'border segments;', len(floor['texts']), 'values')
