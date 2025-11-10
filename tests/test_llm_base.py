import pytest
import asyncio
from src.ai_framework.llms.fake import FakeLLM


class TestFakeLLM:
    def test_initialization(self):
        llm = FakeLLM()
        assert llm.model_name == "fake"
        assert llm.call_count == 0
    
    def test_sync_call(self):
        llm = FakeLLM()
        result = llm("Hello")
        assert "Hello" in result
        assert llm.call_count == 1
    
    @pytest.mark.asyncio
    async def test_async_call(self):
        llm = FakeLLM(responses={"test": "response"})
        result = await llm.call("test")
        assert result == "response"
        assert llm.call_count == 1