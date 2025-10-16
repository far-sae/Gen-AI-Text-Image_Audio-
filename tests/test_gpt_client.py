
import os
import unittest
from unittest.mock import patch, MagicMock
from src.lm.gpt_client import GPTClient

class TestGPTClient(unittest.TestCase):
    @patch('src.lm.gpt_client.OpenAI')
    def test_generate_returns_text(self, mock_openai):
        mock_client = MagicMock()
        # mock the response structure
        msg = MagicMock()
        msg.content = "Hello world"
        choice = MagicMock()
        choice.message = msg
        response = MagicMock()
        response.choices = [choice]
        response.model_dump.return_value = {'mock': True}
        mock_client().chat.completions.create.return_value = response
        mock_openai.return_value = mock_client

        os.environ['OPENAI_API_KEY'] = 'test'
        client = GPTClient(api_key_env='OPENAI_API_KEY', model='gpt-4o-mini')
        out = client.generate('hi')
        self.assertIn('text', out)
        self.assertEqual(out['text'], 'Hello world')

if __name__ == '__main__':
    unittest.main()
