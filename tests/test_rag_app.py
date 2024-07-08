"""
Unit tests for the RAG application.
"""
from unittest import TestCase, mock
import json
import requests
from streamlit.testing.v1 import AppTest


class TestRagApp(TestCase):
    """
    Test class for the RAG streamlit app.
    """

    def setUp(self):
        """
        Create mock response object to us in tests.
        """
        self.response = requests.Response()

    def test_input_and_query(self):
        """
        Test input and query response, patching out the response from the 
        API.
        """
        at = AppTest.from_file("rag/rag_app.py").run(timeout=30)
        test_query = "Test question?"
        test_response = "This is a test answer."
        self.response.status_code = 200
        self.response._content = json.dumps(
            {"results": {"llm": {"replies": [test_response]}}}
        ).encode()
        with mock.patch("requests.get", return_value=self.response):
            at.chat_input[0].set_value(test_query).run()
            assert at.chat_message[1].markdown[0].value == test_query
            assert at.chat_message[2].markdown[0].value == test_response
