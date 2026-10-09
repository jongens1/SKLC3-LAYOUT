import unittest
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest
from excel_renderer import sheet_names, build_floor_figure
from map_renderer import build_map_figure
from map_objects import normalize_floor, search_objects

class WarehouseMapTests(unittest.TestCase):
    def test_map_layers_and_search(self):
        for name in sheet_names():
            figure=build_map_figure(name)
            self.assertLess(len(figure.layout.shapes),500)
            self.assertLess(len(figure.layout.shapes),len(build_floor_figure(name).layout.shapes))
            self.assertEqual(figure.layout.dragmode,'pan')
            self.assertFalse(figure.layout.xaxis.fixedrange)
            self.assertEqual(figure.layout.yaxis.scaleanchor,'x')
            self.assertTrue(all(a.textangle==0 for a in figure.layout.annotations))
        bpo=normalize_floor('2NP (3. BPO)')['objects']
        match=search_objects(bpo,'bpo30')
        self.assertEqual(len(match),1)
        zoomed=build_map_figure('2NP (3. BPO)','BPO30')
        self.assertLess(zoomed.layout.xaxis.range[1]-zoomed.layout.xaxis.range[0],20000)
        self.assertTrue(any(s.line.color=='#facc15' for s in zoomed.layout.shapes))
        xpo=normalize_floor('3NP (4. XPO)')['objects']
        for missing in ['4C-14','4C-15','4H-08']:
            self.assertFalse(search_objects(xpo,missing))
        self.assertTrue(search_objects(xpo,'4F-12'))

    def test_navigation_and_reset(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'sklc3.py')).run(timeout=60)
        self.assertEqual(app.radio[0].value,'Mapa')
        for name in sheet_names():
            app.selectbox[0].set_value(name).run(timeout=60)
            self.assertFalse(app.exception)
            self.assertLess(len(json.loads(app.get('plotly_chart')[0].proto.spec)['layout']['shapes']),500)
        app.selectbox[0].set_value('2NP (3. BPO)').run(timeout=60)
        app.text_input[0].set_value('BPO30').run(timeout=60)
        self.assertFalse(app.exception)
        figure=json.loads(app.get('plotly_chart')[0].proto.spec)
        self.assertLess(figure['layout']['xaxis']['range'][1]-figure['layout']['xaxis']['range'][0],20000)
        app.button[0].click().run(timeout=60)
        self.assertFalse(app.exception)
        reset=json.loads(app.get('plotly_chart')[0].proto.spec)
        self.assertEqual(reset['layout']['xaxis']['range'], [0, normalize_floor('2NP (3. BPO)')['width']])
        app.radio[0].set_value('Excel debug').run(timeout=60)
        self.assertFalse(app.exception)
        self.assertGreater(len(json.loads(app.get('plotly_chart')[0].proto.spec)['layout']['shapes']),1000)
