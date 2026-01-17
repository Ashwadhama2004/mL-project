"""
Tools for Math Mentor AI

This module provides utility tools for the agents, including a safe Python calculator
for mathematical computations.
"""

import math
import re
from typing import Dict, Any, Union, Optional


class PythonCalculator:
    """
    A safe Python calculator for mathematical computations.
    
    This tool evaluates mathematical expressions in a sandboxed environment,
    providing access to common math functions while preventing code execution.
    """
    
    # Allowed functions and constants
    ALLOWED_NAMES = {
        # Basic math
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'pow': pow,
        
        # Math module functions
        'sqrt': math.sqrt,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        
        # Trigonometry
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'atan2': math.atan2,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        
        # Degrees/Radians
        'degrees': math.degrees,
        'radians': math.radians,
        
        # Other useful functions
        'factorial': math.factorial,
        'gcd': math.gcd,
        'ceil': math.ceil,
        'floor': math.floor,
        
        # Constants
        'pi': math.pi,
        'e': math.e,
        'inf': math.inf,
        
        # Boolean
        'True': True,
        'False': False,
    }
    
    # Dangerous patterns to block
    BLOCKED_PATTERNS = [
        r'__\w+__',        # Dunder methods
        r'\bimport\b',     # Import statements
        r'\bexec\b',       # exec function
        r'\beval\b',       # eval function
        r'\bopen\b',       # file operations
        r'\bos\b',         # os module
        r'\bsys\b',        # sys module
        r'\bsubprocess\b', # subprocess
        r'\bcompile\b',    # compile function
        r'\bglobals\b',    # globals access
        r'\blocals\b',     # locals access
        r'\bgetattr\b',    # getattr function
        r'\bsetattr\b',    # setattr function
        r'\bdelattr\b',    # delattr function
        r'\bdir\b',        # dir function
        r'\bvars\b',       # vars function
    ]
    
    def __init__(self):
        """Initialize the calculator."""
        self.last_result = None
        self.history = []
    
    def _is_safe(self, expression: str) -> bool:
        """
        Check if an expression is safe to evaluate.
        
        Args:
            expression: The expression to check
            
        Returns:
            True if safe, False otherwise
        """
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, expression, re.IGNORECASE):
                return False
        return True
    
    def _preprocess(self, expression: str) -> str:
        """
        Preprocess the expression for evaluation.
        
        Args:
            expression: Raw expression
            
        Returns:
            Preprocessed expression
        """
        # Replace common math notation
        expr = expression.strip()
        
        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')
        
        # Replace × with *
        expr = expr.replace('×', '*')
        
        # Replace ÷ with /
        expr = expr.replace('÷', '/')
        
        # Replace √ with sqrt
        expr = re.sub(r'√(\d+)', r'sqrt(\1)', expr)
        expr = re.sub(r'√\(', r'sqrt(', expr)
        
        return expr
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: The mathematical expression to evaluate
            
        Returns:
            Dictionary with result, success status, and any errors
        """
        result = {
            "expression": expression,
            "success": False,
            "result": None,
            "error": None,
            "formatted_result": None
        }
        
        # Check for safety
        if not self._is_safe(expression):
            result["error"] = "Expression contains blocked operations"
            return result
        
        # Preprocess
        processed_expr = self._preprocess(expression)
        result["processed_expression"] = processed_expr
        
        try:
            # Evaluate in restricted namespace
            computed = eval(
                processed_expr,
                {"__builtins__": {}},
                self.ALLOWED_NAMES.copy()
            )
            
            result["success"] = True
            result["result"] = computed
            
            # Format result
            if isinstance(computed, float):
                if computed.is_integer():
                    result["formatted_result"] = str(int(computed))
                elif abs(computed) < 0.0001 or abs(computed) > 1000000:
                    result["formatted_result"] = f"{computed:.6e}"
                else:
                    result["formatted_result"] = f"{computed:.6f}".rstrip('0').rstrip('.')
            else:
                result["formatted_result"] = str(computed)
            
            # Save to history
            self.last_result = computed
            self.history.append({
                "expression": expression,
                "result": computed
            })
            
        except ZeroDivisionError:
            result["error"] = "Division by zero"
        except ValueError as e:
            result["error"] = f"Math domain error: {str(e)}"
        except OverflowError:
            result["error"] = "Result too large to compute"
        except SyntaxError as e:
            result["error"] = f"Invalid expression syntax: {str(e)}"
        except NameError as e:
            result["error"] = f"Unknown function or variable: {str(e)}"
        except Exception as e:
            result["error"] = f"Calculation error: {str(e)}"
        
        return result
    
    def verify_equation(
        self,
        left_side: str,
        right_side: str,
        tolerance: float = 1e-9
    ) -> Dict[str, Any]:
        """
        Verify if two expressions are equal.
        
        Args:
            left_side: Left side of equation
            right_side: Right side of equation
            tolerance: Numerical tolerance for comparison
            
        Returns:
            Dictionary with verification result
        """
        left_result = self.calculate(left_side)
        right_result = self.calculate(right_side)
        
        result = {
            "left_side": left_side,
            "right_side": right_side,
            "left_value": left_result.get("result"),
            "right_value": right_result.get("result"),
            "are_equal": False,
            "error": None
        }
        
        if not left_result["success"]:
            result["error"] = f"Left side error: {left_result['error']}"
            return result
        
        if not right_result["success"]:
            result["error"] = f"Right side error: {right_result['error']}"
            return result
        
        try:
            left_val = float(left_result["result"])
            right_val = float(right_result["result"])
            result["are_equal"] = abs(left_val - right_val) < tolerance
            result["difference"] = abs(left_val - right_val)
        except (TypeError, ValueError):
            result["are_equal"] = left_result["result"] == right_result["result"]
        
        return result
    
    def substitute_and_evaluate(
        self,
        expression: str,
        variables: Dict[str, Union[int, float]]
    ) -> Dict[str, Any]:
        """
        Substitute variables and evaluate an expression.
        
        Args:
            expression: Expression with variables
            variables: Dictionary of variable values
            
        Returns:
            Dictionary with result
        """
        # Create substituted expression
        substituted = expression
        for var, value in variables.items():
            # Use word boundaries to avoid partial replacements
            substituted = re.sub(rf'\b{var}\b', str(value), substituted)
        
        result = self.calculate(substituted)
        result["original_expression"] = expression
        result["variables"] = variables
        
        return result


# Singleton instance
_calculator_instance = None

def get_calculator() -> PythonCalculator:
    """Get or create the singleton calculator instance."""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = PythonCalculator()
    return _calculator_instance


def main():
    """Test the calculator."""
    print("=" * 60)
    print("Math Mentor AI - Python Calculator Test")
    print("=" * 60)
    
    calc = PythonCalculator()
    
    # Test expressions
    test_cases = [
        "2 + 2",
        "sqrt(16)",
        "sin(pi/2)",
        "log(e)",
        "5^2 + 3^2",
        "factorial(5)",
        "(3 + 4) * 2",
        "1/0",  # Should handle error
        "import os",  # Should block
    ]
    
    for expr in test_cases:
        print(f"\nExpression: {expr}")
        result = calc.calculate(expr)
        if result["success"]:
            print(f"  Result: {result['formatted_result']}")
        else:
            print(f"  Error: {result['error']}")
    
    # Test substitution
    print("\n\nSubstitution test:")
    result = calc.substitute_and_evaluate("x^2 + 2*x + 1", {"x": 3})
    print(f"  x^2 + 2*x + 1 where x=3 => {result.get('formatted_result')}")
    
    # Test equation verification
    print("\n\nVerification test:")
    result = calc.verify_equation("2^10", "1024")
    print(f"  2^10 = 1024? {result['are_equal']}")


if __name__ == "__main__":
    main()
