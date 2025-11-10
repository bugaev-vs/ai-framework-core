import pytest
import asyncio
from src.ai_framework.llms.fake import FakeLLM
from src.ai_framework.tools.calculator import CalculatorTool
from src.ai_framework.tools.search import SearchTool
from src.ai_framework.agents.base import SimpleAgent


class TestIntegration:
    @pytest.fixture
    def setup_agent(self):
        llm = FakeLLM()
        calculator = CalculatorTool()
        search_tool = SearchTool()
        return SimpleAgent(llm=llm, tools=[calculator, search_tool])

    @pytest.mark.asyncio
    async def test_agent_with_calculator(self, setup_agent):
        result = await setup_agent.run({"input": "10 + 15"})
        assert result["tool_used"] == "calculator"
        assert "Result: 25" in result["tool_result"]
        assert "input" in result

    @pytest.mark.asyncio
    async def test_agent_with_search(self, setup_agent):
        result = await setup_agent.run({"input": "Search for AI news"})
        assert result["tool_used"] == "search"
        assert "Search results" in result["tool_result"]

    @pytest.mark.asyncio
    async def test_agent_without_tools(self, setup_agent):
        result = await setup_agent.run({"input": "Hello how are you?"})
        assert result["tool_used"] is None
        assert "Echo:" in result["final_answer"]