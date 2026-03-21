import requests
import os
from typing import List, Dict

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def chat_completion(self, messages: List[Dict[str, str]], model: str = "openrouter/free"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/openviking",
            "X-Title": "OpenViking Agent"
        }
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenRouter API Error: {response.text}")
