"""
Utility functions for the Daytona-Goose integration.
"""
import os
import sys
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

def load_environment() -> bool:
    """
    Load environment variables from .env file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        load_dotenv()
        required_vars = ['OPENAI_API_KEY', 'DAYTONA_API_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            print(f"⚠️ Missing required environment variables: {', '.join(missing)}")
            return False
            
        return True
    except Exception as e:
        print(f"⚠️ Error loading environment: {e}")
        return False

def generate_code(prompt: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
    """
    Generate code using OpenAI
    
    Args:
        prompt: The prompt asking for code
        model: The OpenAI model to use
        
    Returns:
        Generated code or None if generation failed
    """
    try:
        # Load API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ OpenAI API key not found in environment")
            return None
            
        client = OpenAI(api_key=api_key)
        
        # Create a prompt that emphasizes code output
        full_prompt = f"""
        Generate Python code for the following request. Return ONLY the code, no explanations or comments unless they're part of the code.
        
        Request: {prompt}
        """
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Python code generator. Generate clean, efficient, and correct code."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )
        
        # Extract generated code
        code = response.choices[0].message.content.strip()
        
        # Remove markdown code block markers if present
        if code.startswith("```python"):
            code = code[len("```python"):].strip()
        if code.startswith("```"):
            code = code[3:].strip()
        if code.endswith("```"):
            code = code[:-3].strip()
            
        return code
    except Exception as e:
        print(f"⚠️ Error generating code: {e}")
        return None

def parse_goose_input(input_text: str) -> Dict[str, Any]:
    """
    Parse input from Goose to extract code and language
    
    Args:
        input_text: Text input from Goose
        
    Returns:
        Dictionary with extracted code and language
    """
    try:
        # Check for code block format
        if "```" in input_text:
            # Extract language and code from markdown code blocks
            parts = input_text.split("```", 2)
            if len(parts) >= 3:
                lang_line = parts[1].strip().split("\n")[0]
                language = lang_line if lang_line else "python"
                code = "\n".join(parts[1].strip().split("\n")[1:]) if "\n" in parts[1] else ""
            else:
                language = "python"
                code = input_text
        else:
            # Default to python if no code block markers
            language = "python"
            code = input_text
            
        return {
            "code": code.strip(),
            "language": language.strip()
        }
    except Exception as e:
        print(f"⚠️ Error parsing input: {e}")
        return {
            "code": input_text,
            "language": "python"
        }