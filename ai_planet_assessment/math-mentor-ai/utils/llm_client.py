"""
LLM Client for Math Mentor AI

This module provides a unified interface for interacting with Google's Gemini API.
It handles API calls, error handling, and response parsing.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("Please install google-generativeai: pip install google-generativeai")
    raise


class LLMClient:
    """Unified LLM client for Gemini API."""
    
    def __init__(
        self,
        api_key: str = None,
        model_name: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        Initialize the LLM client.
        
        Args:
            api_key: Google API key (defaults to env var or streamlit secrets)
            model_name: Model to use (defaults to env var or gemini-2.0-flash)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        # Try multiple sources for API key:
        # 1. Direct parameter
        # 2. Environment variable
        # 3. Streamlit secrets (for cloud deployment)
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            try:
                import streamlit as st
                if hasattr(st, 'secrets') and 'api_keys' in st.secrets:
                    self.api_key = st.secrets.api_keys.get("GOOGLE_API_KEY")
            except Exception:
                pass
        
        self.model_name = model_name or os.getenv("MODEL_NAME", "gemini-2.0-flash")
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Set GOOGLE_API_KEY environment variable, "
                "pass api_key parameter, or configure Streamlit secrets."
            )
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
        )
        
        print(f"LLM Client initialized with model: {self.model_name}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system instructions
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated text response
        """
        try:
            # Combine system prompt with user prompt if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature or self.temperature,
                    max_output_tokens=max_tokens or self.max_tokens,
                )
            )
            
            return response.text
            
        except Exception as e:
            error_msg = f"LLM generation error: {str(e)}"
            print(error_msg)
            raise RuntimeError(error_msg) from e
    
    def generate_json(
        self,
        prompt: str,
        system_prompt: str = None,
        schema_hint: str = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system instructions
            schema_hint: Description of expected JSON structure
            
        Returns:
            Parsed JSON response as dictionary
        """
        # Add JSON formatting instructions
        json_instruction = """
You must respond with valid JSON only. No markdown, no explanation, just the JSON object.
"""
        if schema_hint:
            json_instruction += f"\nExpected structure: {schema_hint}"
        
        full_system = (system_prompt or "") + "\n" + json_instruction
        
        response = self.generate(prompt, system_prompt=full_system)
        
        # Clean the response (remove markdown code blocks if present)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', cleaned)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {cleaned[:500]}")
    
    def generate_with_context(
        self,
        prompt: str,
        context: str,
        system_prompt: str = None
    ) -> str:
        """
        Generate a response with RAG context.
        
        Args:
            prompt: The user prompt
            context: Retrieved context from RAG
            system_prompt: Optional system instructions
            
        Returns:
            Generated text response
        """
        context_prompt = f"""
Use the following context from the knowledge base to answer the question.
Only use information from the provided context. If the context doesn't contain
relevant information, say so clearly.

CONTEXT:
{context}

QUESTION:
{prompt}
"""
        return self.generate(context_prompt, system_prompt=system_prompt)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None
    ) -> str:
        """
        Have a multi-turn conversation.
        
        Args:
            messages: List of {"role": "user"|"assistant", "content": str}
            system_prompt: Optional system instructions
            
        Returns:
            Generated response
        """
        # Build conversation history
        history = []
        for msg in messages[:-1]:  # All but last
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})
        
        # Start chat
        chat = self.model.start_chat(history=history)
        
        # Send last message
        last_message = messages[-1]["content"]
        if system_prompt:
            last_message = f"{system_prompt}\n\n{last_message}"
        
        response = chat.send_message(last_message)
        return response.text


# Singleton instance
_client_instance = None

def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = LLMClient()
    return _client_instance


def main():
    """Test the LLM client."""
    print("=" * 60)
    print("Math Mentor AI - LLM Client Test")
    print("=" * 60)
    
    client = LLMClient()
    
    # Test basic generation
    print("\nTest 1: Basic generation")
    response = client.generate("What is 2 + 2? Answer briefly.")
    print(f"Response: {response}")
    
    # Test JSON generation
    print("\nTest 2: JSON generation")
    json_response = client.generate_json(
        "Identify the topic and variables in this math problem: 'Solve x^2 - 5x + 6 = 0'",
        schema_hint='{"topic": string, "variables": [string], "problem_type": string}'
    )
    print(f"JSON Response: {json.dumps(json_response, indent=2)}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    main()
