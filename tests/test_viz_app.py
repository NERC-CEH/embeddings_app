from streamlit.testing.v1 import AppTest
import requests
from unittest import TestCase, mock
import json
from visualisation.visualisation_app import create_figure
import pandas as pd

class TestRagApp(TestCase):

    def setUp(self):
        self.data = data = pd.DataFrame({
            'x': [1,2],
            'y': [10,11],
            'topic_number': [1,2],
            'doc_id': ['id1', 'id2'],
            'short_title': ['stitle1', 'stitle2']
        })

    def test_app_starts(self):
        with mock.patch("visualisation.visualisation_app.get_embeddings", return_value=self.data):
            at = AppTest.from_file("visualisation/visualisation_app.py").run(timeout=30)
        

    def test_create_figure(self):
        fig = create_figure(self.data)
        
        scatter_data = fig.data[0]
        assert scatter_data.type == 'scatter', "The plot type should be scatter"
        assert all(scatter_data.x == self.data['x']), "X data should match"
        assert all(scatter_data.y == self.data['y']), "Y data should match"
