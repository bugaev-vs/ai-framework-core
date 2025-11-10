#!/usr/bin/env python3
"""
Demo script showing the complete framework in action
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_framework.llms.fake import FakeLLM
from ai_framework.tools.calculator import CalculatorTool
from ai_framework.tools.search import SearchTool
from ai_framework.agents.base import SimpleAgent  # ⬅️ ПРОВЕРЬТЕ ЭТУ СТРОКУ


async def main():
    """Demo the complete agent system"""
    print("🤖 AI Framework Demo - Day 2")
    print("=" * 50)
    
    # Initialize components
    llm = FakeLLM()
    calculator = CalculatorTool()
    search_tool = SearchTool()
    
    # Create agent
    agent = SimpleAgent(  # ⬅️ И ЭТУ СТРОКУ
        llm=llm,
        tools=[calculator, search_tool],
        verbose=True
    )
    
    # Test cases
    test_cases = [
        "Calculate 25 * 4 + 10",
        "Search for information about artificial intelligence",
        "What is the capital of France?",
        "Tell me a joke"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {question}")
        print("-" * 40)
        
        result = await agent.run({"input": question})
        
        print(f"🛠️  Tool used: {result['tool_used']}")
        if result.get('tool_result'):
            print(f"🔧 Tool result: {result['tool_result']}")
        print(f"🤖 Final answer: {result['final_answer']}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())