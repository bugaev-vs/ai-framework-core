import asyncio
import pytest
from src.ai_framework.llms.fake import FakeLLM


class TestFakeLLM:
    def test_initialization(self):
        llm = FakeLLM()
        assert llm.response_prefix == "Echo: "

    def test_initialization_custom_prefix(self):
        llm = FakeLLM(response_prefix="Test: ")
        assert llm.response_prefix == "Test: "

    def test_sync_call(self):
        llm = FakeLLM()
        # FakeLLM не callable, используем call() метод
        result = asyncio.run(llm.call("Hello"))
        assert result == "Echo: Hello"

    @pytest.mark.asyncio
    async def test_async_call(self):
        llm = FakeLLM(response_prefix="Test: ")
        result = await llm.call("test")
        assert result == "Test: test"

    @pytest.mark.asyncio
    async def test_call_with_metadata(self):
        llm = FakeLLM()
        result = await llm.call_with_metadata("hello")
        assert result["content"] == "Echo: hello"
        assert result["model"] == "fake-llm"
        assert "usage" in result