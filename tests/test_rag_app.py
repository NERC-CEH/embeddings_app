from streamlit.testing.v1 import AppTest
import requests
from unittest import TestCase, mock


class TestRagApp(TestCase):

    def setUp(self):
        self.response = requests.Response()

    def test_input_and_query(self):
        at = AppTest.from_file("rag/rag_app.py").run(timeout=30)
        test_query = "Test question?"
        test_response = "This is a test answer."
        self.response.status_code = 200
        self.response._content = (
            '{"results": {"llm": {"replies": ["This is a test answer."]}}}'.encode()
        )
        with mock.patch("requests.get", return_value=self.response):
            at.chat_input[0].set_value(test_query).run()
            assert at.chat_message[1].markdown[0].value == test_query
            assert at.chat_message[2].markdown[0].value == test_response
