"""Offline regression checks. No real API calls or original user databases."""
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from src.agent.orchestrator import TravelAgent
from src.llm.llm_service import LLMService
from src.memory.user_memory import UserMemory

class ConfigurationTests(unittest.TestCase):
    def test_missing_key_is_rejected_before_creating_client(self):
        with patch.dict(os.environ, {}, clear=True), patch("src.llm.llm_service.OpenAI") as sdk:
            with self.assertRaisesRegex(ValueError, "LLM_API_KEY"):
                LLMService()
            sdk.assert_not_called()

    def test_configurable_endpoint_and_model(self):
        env = {"LLM_API_KEY": "local-test-placeholder", "LLM_BASE_URL": "https://example.invalid", "LLM_MODEL": "mock-model"}
        with patch.dict(os.environ, env, clear=True), patch("src.llm.llm_service.OpenAI") as sdk:
            service = LLMService()
            sdk.assert_called_once_with(api_key="local-test-placeholder", base_url="https://example.invalid")
            self.assertEqual(service.model, "mock-model")

    def test_explicit_arguments_override_environment(self):
        with patch.dict(os.environ, {"LLM_API_KEY": "environment-placeholder"}, clear=True), patch("src.llm.llm_service.OpenAI") as sdk:
            service = LLMService(api_key="argument-placeholder", base_url="https://override.invalid", model="override")
            sdk.assert_called_once_with(api_key="argument-placeholder", base_url="https://override.invalid")
            self.assertEqual(service.model, "override")

    def test_chat_uses_configured_model_without_network(self):
        with patch("src.llm.llm_service.OpenAI") as sdk:
            sdk.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="mock response"))]
            )
            service = LLMService(api_key="local-placeholder", model="mock-model")
            self.assertEqual(service.chat([{"role": "user", "content": "test"}]), "mock response")
            self.assertEqual(sdk.return_value.chat.completions.create.call_args.kwargs["model"], "mock-model")

class MemoryAndFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.temp.name) / "memory.db")
        self.memory = UserMemory(self.path)
        self.memory.user_id = "user-a"

    def tearDown(self):
        self.temp.cleanup()

    def test_preferences_persist_without_leaking_to_other_user(self):
        self.memory.save_preferences({"taste": "不吃辣"})
        reopened = UserMemory(self.path)
        reopened.user_id = "user-a"
        self.assertEqual(reopened.get_preferences()["taste"], "不吃辣")
        reopened.user_id = "user-b"
        self.assertEqual(reopened.get_preferences(), {})

    def test_conversation_history_is_scoped_and_can_be_resumed(self):
        first = self.memory.new_conversation()
        self.memory.add_message("user", "first")
        second = self.memory.new_conversation()
        self.memory.add_message("user", "second")
        self.assertNotEqual(first, second)
        self.assertEqual(self.memory.get_history()[0]["content"], "second")
        self.memory.conversation_id = first
        self.assertEqual(self.memory.get_history()[0]["content"], "first")
        self.memory.user_id = "user-b"
        self.assertEqual(self.memory.get_history(), [])

    def test_mocked_request_includes_local_reference_and_saves_reply(self):
        data_path = Path(__file__).resolve().parents[1] / "src/data/scenic_spots.json"
        first_spot = json.loads(data_path.read_text(encoding="utf-8"))[0]
        captured = {}

        class FakeLLM:
            def classify_intent(self, text):
                return {"intent": "trip_planning", "info": {"destination": first_spot["city"]}}

            def quick_chat(self, text, **kwargs):
                captured.update(kwargs)
                return "This is an offline test response."

        agent = TravelAgent(memory=self.memory, llm=FakeLLM())
        result = agent.process("请帮我安排旅行")
        self.assertEqual(result["response"], "This is an offline test response.")
        self.assertIn(first_spot["name"], captured["system_extra"])
        history = self.memory.get_history()
        self.assertEqual([m["role"] for m in history], ["user", "assistant"])

if __name__ == "__main__":
    unittest.main()
