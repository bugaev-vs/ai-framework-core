import math
import re
from typing import Dict, Any
from .base import Tool


class CalculatorTool(Tool):
    """Simple calculator tool that evaluates mathematical expressions"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Evaluates mathematical expressions. Use for calculations."
        )
        self._safe_globals = {
            'abs': abs, 'min': min, 'max': max, 'round': round,
            'sum': sum, 'len': len, 'pow': pow, 'sqrt': math.sqrt,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'pi': math.pi, 'e': math.e
        }
    
    async def _run(self, input_text: str) -> str:
        """Evaluate mathematical expression safely"""
        try:
            # Извлекаем только математическое выражение из текста
            math_expression = self._extract_math_expression(input_text)
            
            if not math_expression:
                return "Error: No mathematical expression found. Please provide something like '2 + 2' or '15 * 8'"
            
            # Basic security - only allow math operations
            for char in math_expression:
                if char not in '0123456789+-*/()., \t\n\r':
                    return f"Error: Invalid character in expression: {char}"
            
            # Evaluate safely
            result = eval(math_expression, {"__builtins__": {}}, self._safe_globals)
            return f"Result: {result}"
        
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _extract_math_expression(self, text: str) -> str:
        """Extract mathematical expression from text"""
        import re
        
        # Удаляем общие вопросы и слова
        words_to_remove = ['calculate', 'compute', 'solve', 'what is', 'the value of', '?', 'please']
        expression = text.lower()
        
        for word in words_to_remove:
            expression = expression.replace(word, '')
        
        # Ищем математические выражения с помощью regex
        math_pattern = r'[\d\+\-\*\/\(\)\.\s]+'
        matches = re.findall(math_pattern, expression)
        
        if matches:
            # Берем самый длинный математический сегмент
            math_expr = max(matches, key=len).strip()
            return math_expr if math_expr else ""
        
        return expression.strip()