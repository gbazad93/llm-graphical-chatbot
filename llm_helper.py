"""
LLM API helper module for the AI-Powered Data Chatbot application.

This module handles all interactions with the OpenAI API and provides
text formatting utilities for processing AI responses.
"""

import os
import re
from typing import List, Tuple, Optional
import openai
from pathlib import Path


# Environment & API Key
ROOT = Path(__file__).parent
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

MODEL = "gpt-4o-mini"


class LLMHelper:
    """
    Helper class for LLM operations and text formatting.
    
    This class provides methods for interacting with OpenAI's API
    and formatting markdown text to HTML for display purposes.
    """
    
    def __init__(self, model: str = MODEL) -> None:
        """
        Initialize the LLM helper.
        
        Args:
            model (str): The OpenAI model to use for API calls.
        """
        self.model = model
        self._setup_api()
    
    def _setup_api(self) -> None:
        """
        Set up the OpenAI API configuration.
        
        Raises:
            ValueError: If OPENAI_API_KEY environment variable is not set.
        """
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it before using the application."
            )
        openai.api_key = OPENAI_API_KEY
    
    def format_markdown_to_html(self, text: str) -> str:
        """
        Convert basic markdown formatting to HTML.
        
        This method converts markdown elements like headers, bold text,
        and bullet points to properly formatted HTML for display in Qt widgets.
        
        Args:
            text (str): The markdown text to convert.
            
        Returns:
            str: The converted HTML text.
        """
        # Replace **bold** with <b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Replace ### headers with styled headers
        text = re.sub(
            r'^### (.*?)$',
            r'<h3 style="color: #2c5aa0; margin: 16px 0 8px 0; font-size: 14pt; font-weight: bold;">\1</h3>',
            text,
            flags=re.MULTILINE
        )
        
        # Replace ## headers
        text = re.sub(
            r'^## (.*?)$',
            r'<h2 style="color: #1e4176; margin: 18px 0 10px 0; font-size: 16pt; font-weight: bold;">\1</h2>',
            text,
            flags=re.MULTILINE
        )
        
        # Replace # headers
        text = re.sub(
            r'^# (.*?)$',
            r'<h1 style="color: #1a365d; margin: 20px 0 12px 0; font-size: 18pt; font-weight: bold;">\1</h1>',
            text,
            flags=re.MULTILINE
        )
        
        # Replace bullet points with proper HTML lists
        lines = text.split('\n')
        formatted_lines = []
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- '):
                if not in_list:
                    formatted_lines.append('<ul style="margin: 8px 0; padding-left: 20px;">')
                    in_list = True
                formatted_lines.append(f'<li style="margin: 4px 0; line-height: 1.4;">{stripped[2:]}</li>')
            else:
                if in_list:
                    formatted_lines.append('</ul>')
                    in_list = False
                if stripped:
                    formatted_lines.append(f'<p style="margin: 8px 0; line-height: 1.5;">{line}</p>')
        
        if in_list:
            formatted_lines.append('</ul>')
            
        return '\n'.join(formatted_lines)
    
    def ask_llm(self, data: str, question: str) -> str:
        """
        Send a question about data to the LLM and get a response.
        
        This method creates a prompt combining the provided data and question,
        sends it to the OpenAI API, and returns the formatted response.
        
        Args:
            data (str): The data to analyze.
            question (str): The question to ask about the data.
            
        Returns:
            str: The LLM's response to the question.
            
        Raises:
            Exception: If there's an error communicating with the OpenAI API.
        """
        prompt = (
            "You are an expert data analyst assistant. The user has provided data below "
            "and wants you to analyze it. Please provide clear, well-formatted responses using "
            "markdown formatting (headers with ###, bullet points with -, **bold** text) "
            "to make your analysis easy to read and understand.\n\n"
            f"Data:\n{data}\n\nQuestion: {question}\n\n"
            "Please provide a comprehensive analysis with proper formatting."
        )

        messages = [
            {
                "role": "system", 
                "content": (
                    "You are a helpful data analyst. Always format your responses with "
                    "markdown for better readability. Use headers (###), bullet points (-), "
                    "and **bold** text appropriately."
                )
            },
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=3000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error communicating with OpenAI API: {str(e)}")
    
    def format_chat_message(self, sender: str, message: str, is_user: bool = False) -> str:
        """
        Format a chat message for display in the chat area.
        
        Args:
            sender (str): The sender of the message ("You" or "AI").
            message (str): The message content.
            is_user (bool): Whether this is a user message or AI response.
            
        Returns:
            str: The formatted HTML message.
        """
        if is_user:
            return f"""
            <div style="margin: 16px 0; padding: 12px 16px; background: #e6fffa; border-left: 4px solid #38b2ac; border-radius: 8px;">
                <div style="font-weight: bold; color: #2c7a7b; margin-bottom: 6px;">👤 {sender}:</div>
                <div style="color: #234e52; line-height: 1.5;">{message}</div>
            </div>
            """
        else:
            # Format AI response with markdown conversion
            formatted_msg = self.format_markdown_to_html(message)
            return f"""
            <div style="margin: 16px 0; padding: 16px; background: #f0f9ff; border-left: 4px solid #3b82f6; border-radius: 8px;">
                <div style="font-weight: bold; color: #1e40af; margin-bottom: 8px;">🤖 AI Assistant:</div>
                <div style="color: #1e3a8a; line-height: 1.6;">{formatted_msg}</div>
            </div>
            """
    
    def build_chat_history_html(self, chat_history: List[Tuple[str, str]]) -> str:
        """
        Build the complete chat history HTML from a list of messages.
        
        Args:
            chat_history (List[Tuple[str, str]]): List of (sender, message) tuples.
            
        Returns:
            str: The complete formatted HTML for all chat messages.
        """
        formatted_html = ""
        for sender, message in chat_history:
            is_user = sender == "You"
            formatted_html += self.format_chat_message(sender, message, is_user)
        
        return formatted_html
    
    @staticmethod
    def validate_api_key() -> bool:
        """
        Validate that the OpenAI API key is available.
        
        Returns:
            bool: True if API key is available, False otherwise.
        """
        return bool(OPENAI_API_KEY)
    
    @staticmethod
    def get_available_models() -> List[str]:
        """
        Get a list of available OpenAI models.
        
        Returns:
            List[str]: List of available model names.
        """
        return ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    
    def set_model(self, model: str) -> None:
        """
        Set the model to use for API calls.
        
        Args:
            model (str): The model name to use.
            
        Raises:
            ValueError: If the model is not in the list of available models.
        """
        available_models = self.get_available_models()
        if model not in available_models:
            raise ValueError(f"Model {model} not in available models: {available_models}")
        
        self.model = model