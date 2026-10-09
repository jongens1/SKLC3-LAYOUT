import json
from pathlib import Path
import unittest

from excel_renderer import build_floor_figure, floor_content, sheet_names
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class ExcelLayoutTests(unittest.TestCase):
    def test_four_floors_switch_without_exceptions(self):
        app = AppTest.from_file(str(ROOT / 'sklc3.py')).run(timeout=60)
        self.assertEqual(len(sheet_names()), 4)
        for name in sheet_names():
            app.radio[0].set_value(name).run(timeout=60)
            self.assertEqual(len(app.exception), 0, [e.message for e in app.exception])
            charts = app.get('plotly_chart')
            self.assertEqual(len(charts), 1)
            figure = json.loads(charts[0].proto.spec)
            self.assertGreater(len(figure['layout']['shapes']), 500)
            self.assertEqual(figure['layout']['yaxis']['scaleanchor'], 'x')
            self.assertFalse(figure['layout']['xaxis']['visible'])

    def test_bpo_numbering_and_vertical_pairs(self):
        floor, texts, lines = floor_content('2NP (3. BPO)')
        by_cell = {t['cell']: t['text'] for t in texts if not t.get('manual')}
        self.assertEqual([by_cell[c] for c in ['FC89','GD89','HK89','II89','JN89','KE89','LK89','LY89','NK89']],
                         [f'BPO{n}' for n in range(20, 29)])
        self.assertEqual([by_cell[c] for c in ['FE140','GC140','HH140','IG140','JK140','KJ140','LM140','ML140','NM140']],
                         [f'BPO{n}' for n in range(30, 39)])
        manual = [t for t in texts if t.get('manual')]
        self.assertEqual([t['text'] for t in manual], [f'BPO{n:02}' for n in range(1,19)])
        self.assertEqual(len(lines), 9)
        for left, right in zip(manual[::2], manual[1::2]):
            self.assertEqual(left['box'][2], right['box'][0])
            self.assertEqual(left['box'][1::2], right['box'][1::2])

    def test_xpo_missing_locations_remain_missing(self):
        _, texts, _ = floor_content('3NP (4. XPO)')
        labels = {t['text'] for t in texts}
        self.assertTrue({'4C-13','4C-16','4H-07','4H-09'} <= labels)
        self.assertFalse({'4C-14','4C-15','4H-08'} & labels)

    def test_source_labels_are_retained_and_helpers_are_optional(self):
        for name in sheet_names():
            floor, texts, _ = floor_content(name, True)
            self.assertGreaterEqual(len(texts), len(floor['texts']))
            self.assertIn('SHUTTLE', {t['text'] for t in texts})
            self.assertIn('AUTOSTORE', {t['text'] for t in texts})
        floor, regular, _ = floor_content('1NP (2. SPO)')
        self.assertLess(len(regular), 100)
        self.assertGreater(len(floor['texts']), 9000)


if __name__ == '__main__':
    unittest.main()
