<<<<<<< HEAD
﻿import unittest
=======
import unittest
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
from unittest.mock import patch, MagicMock
import requests
from starlette.testclient import TestClient

from main import app, load_knowledge_base, build_system_prompt, SupportResponse


class TestCustomerSupportAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Verify if Ollama is accessible
        cls.ollama_online = False
        try:
            r = requests.get("http://localhost:11434", timeout=2)
            if r.status_code == 200:
                cls.ollama_online = True
        except Exception:
            cls.ollama_online = False

    def test_root_endpoint(self):
        """Root endpoint should return application name."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
<<<<<<< HEAD
        self.assertEqual(response.text, "KnowledgeAssist AI")
=======
        self.assertEqual(response.text, "AI Customer Support")
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

    def test_knowledge_base_loading(self):
        """Knowledge base should load items from knowledge.json."""
        kb = load_knowledge_base()
        self.assertIsInstance(kb, list)
        self.assertGreater(len(kb), 0)
        self.assertIn("question", kb[0])
        self.assertIn("answer", kb[0])

    def test_empty_and_whitespace_message_rejected(self):
        """Empty or whitespace-only messages must be rejected with HTTP 400."""
        # Empty string
        res_empty = self.client.post("/chat", json={"message": ""})
        self.assertEqual(res_empty.status_code, 400)
        self.assertIn("Please enter a question", res_empty.json()["detail"])

        # Whitespace only
        res_whitespace = self.client.post("/chat", json={"message": "    "})
        self.assertEqual(res_whitespace.status_code, 400)
        self.assertIn("Please enter a question", res_whitespace.json()["detail"])

    def test_ollama_unavailable_returns_503(self):
        """When Ollama is unreachable, endpoint should return 503 with a clear message."""
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Connection refused")):
            response = self.client.post("/chat", json={"message": "How do I reset my password?"})
            self.assertEqual(response.status_code, 503)
            self.assertIn("The AI service is unavailable", response.json()["detail"])

    def test_ollama_model_not_found_returns_clear_message(self):
        """When Ollama returns 404 (model not found), error detail guides the user to pull model."""
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        http_error = requests.exceptions.HTTPError(response=mock_resp)
        with patch("requests.post", side_effect=http_error):
            response = self.client.post("/chat", json={"message": "How do I reset my password?"})
            self.assertEqual(response.status_code, 503)
            self.assertIn("Model 'gemma4:e4b' not found in Ollama", response.json()["detail"])

    def test_invalid_llm_json_fallback(self):
        """When the LLM returns invalid JSON, the assistant should safely return a fallback."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"response": "This is not valid JSON at all."}
            response = self.client.post("/chat", json={"message": "How do I reset my password?"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["needs_human"])
            self.assertEqual(data["category"], "error")
            self.assertIn("couldn't process", data["answer"].lower())

    def test_incomplete_llm_schema_fallback(self):
        """When the LLM returns JSON missing required fields, it should return fallback."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            # Missing category and needs_human
            mock_post.return_value.json.return_value = {"response": '{"answer": "Some answer"}'}
            response = self.client.post("/chat", json={"message": "How do I reset my password?"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["needs_human"])
            self.assertEqual(data["category"], "error")

    def test_markdown_code_fenced_json_parsed(self):
        """Model output enclosed in markdown code fences should be parsed correctly."""
        markdown_output = "```json\n{\"answer\": \"Test answer\", \"category\": \"account\", \"needs_human\": false}\n```"
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"response": markdown_output}
            response = self.client.post("/chat", json={"message": "How do I reset my password?"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["answer"], "Test answer")
            self.assertEqual(data["category"], "account")
            self.assertFalse(data["needs_human"])

    def test_unknown_category_enforces_needs_human(self):
        """If model returns category='unknown' but needs_human=False, it should enforce needs_human=True."""
        output = '{"answer": "I do not know", "category": "unknown", "needs_human": false}'
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"response": output}
            response = self.client.post("/chat", json={"message": "Unknown question?"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["needs_human"])
            self.assertEqual(data["category"], "unknown")

    def test_live_password_reset(self):
        """Scenario 1: Reset password should return correct answer from knowledge base."""
        if not self.ollama_online:
            self.skipTest("Ollama is not running locally")
        response = self.client.post("/chat", json={"message": "How do I reset my password?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Forgot Password", data["answer"])
        self.assertFalse(data["needs_human"])

    def test_live_paraphrased_password_reset(self):
        """Scenario 2: Paraphrased password query should recognize the same topic."""
        if not self.ollama_online:
            self.skipTest("Ollama is not running locally")
        response = self.client.post("/chat", json={"message": "I forgot my password. How can I access my account?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Forgot Password", data["answer"])
        self.assertFalse(data["needs_human"])

    def test_live_cancel_subscription(self):
        """Scenario 3: Subscription cancellation should return documented instructions."""
        if not self.ollama_online:
            self.skipTest("Ollama is not running locally")
        response = self.client.post("/chat", json={"message": "How do I cancel my subscription?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Cancel Subscription", data["answer"])
        self.assertFalse(data["needs_human"])

    def test_live_unknown_integration_question(self):
        """Scenario 4: Question not in knowledge base triggers unknown fallback."""
        if not self.ollama_online:
            self.skipTest("Ollama is not running locally")
<<<<<<< HEAD
        response = self.client.post("/chat", json={"message": "Does KnowledgeAssist AI integrate with Salesforce?"})
=======
        response = self.client.post("/chat", json={"message": "Does CloudDesk integrate with Salesforce?"})
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["needs_human"])
        self.assertEqual(data["category"].lower(), "unknown")

    def test_live_out_of_scope_weather(self):
        """Scenario 5: Unrelated query is marked as out of scope/unknown."""
        if not self.ollama_online:
            self.skipTest("Ollama is not running locally")
        response = self.client.post("/chat", json={"message": "What is the weather today?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["needs_human"])
        self.assertEqual(data["category"].lower(), "unknown")


if __name__ == "__main__":
    unittest.main()
