"""
Unit tests for the RAG application.
"""

from unittest import TestCase
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest


class TestRagApp(TestCase):
    """
    Test class for the RAG streamlit app.
    """

    def setUp(self):
        """
        Create mock response objects to use in tests.
        """
        self.question = "Test question?"
        self.answer = "This is a test answer."
        self.scores = pd.DataFrame(
            {"dataset": ["test_dataset_name"], "y": [0.5]}
        )

    @patch("rag.wrappers.RagPipelineWrapper.query")
    def test_input_and_query(self, mock_query):
        """
        Test input and query response, patching out the response from the
        API.
        """
        mock_query.return_value = self.question, self.scores

        at = AppTest.from_file("rag/rag_app.py").run(timeout=10)
        at.chat_input[0].set_value(self.question).run(timeout=10)
        assert at.chat_message[1].markdown[0].value == self.question
