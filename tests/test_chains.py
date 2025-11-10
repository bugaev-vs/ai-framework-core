import pytest
from src.ai_framework.chains.simple import SimpleLLMChain
from src.ai_framework.llms.fake import FakeLLM


class TestSimpleLLMChain:
    @pytest.fixture
    def fake_llm(self):
        return FakeLLM()
    
    @pytest.fixture
    def simple_chain(self, fake_llm):
        return SimpleLLMChain(
            llm=fake_llm,
            prompt_template="Translate this to French: {text}"
        )
    
    def test_initialization(self, simple_chain, fake_llm):
        assert simple_chain.llm == fake_llm
        assert "text" in simple_chain.prompt_template
        assert simple_chain.verbose == False
    
    def test_format_prompt(self, simple_chain):
        input_data = {"text": "Hello world"}
        formatted = simple_chain.format_prompt(input_data)
        assert formatted == "Translate this to French: Hello world"
    
    @pytest.mark.asyncio
    async def test_async_run(self, simple_chain):
        input_data = {"text": "Hello world"}
        result = await simple_chain.run(input_data)
        
        assert "input" in result
        assert "prompt" in result
        assert "output" in result
        assert result["input"] == input_data
        assert "Hello world" in result["prompt"]
        assert "Echo:" in result["output"]
    
    def test_sync_call(self, simple_chain):
        input_data = {"text": "Test sync"}
        result = simple_chain(input_data)
        assert result["output"] == "Echo: Translate this to French: Test sync"