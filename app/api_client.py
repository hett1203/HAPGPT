# app/api_client.py

import os
from groq import Groq
from logger import CustomLogger  # Import your custom logger


def get_groq_api_key():
    """Return the Groq key from either API_KEY or GROQ_API_KEY and normalize it."""
    api_key = os.getenv('GROQ_API_KEY') or os.getenv('API_KEY')
    if not api_key:
        raise RuntimeError(
            "Missing Groq API key. Set GROQ_API_KEY or API_KEY in your environment or .env file."
        )
    os.environ['GROQ_API_KEY'] = api_key
    return api_key


class GroqClient:
    """Class to interact with the Groq API."""

    def __init__(self):
        self.api_key = get_groq_api_key()
        self.model = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')
        self.client = Groq(api_key=self.api_key)
        self.logger = CustomLogger().get_logger()  # Initialize your custom logger

    def get_response(self, messages):
        """
        Send messages to the Groq API and return the response.

        :param messages: List of messages for the conversation.
        :return: AI response as a string.
        """
        try:
            self.logger.info("Sending messages to Groq API...")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            response = chat_completion.choices[0].message.content
            self.logger.info("Received response from Groq API.")
            return response
        except Exception as e:
            self.logger.error(f"Error communicating with Groq API: {e}")
            return "Sorry, I couldn't get a response at this time."