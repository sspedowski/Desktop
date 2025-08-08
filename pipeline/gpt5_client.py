"""Lightweight GPT-5 client wrapper.

Uncomment OpenAI code and set environment variable OPENAI_API_KEY to enable live calls.
Falls back to stub responses when API key not set.
"""
from __future__ import annotations
import os
from typing import List, Optional

STUB = "[STUB COMPLETION – Replace with real GPT-5 output after enabling OpenAI API key]"

class GPT5Client:
    def __init__(self, model: str = "gpt-5", temperature: float = 0.2):
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.live = bool(self.api_key)
        # To enable live mode install openai>=1.0 and uncomment below
        # from openai import OpenAI
        # self.client = OpenAI(api_key=self.api_key)

    def complete(self, system: str, prompt: str, max_tokens: int = 3000) -> str:
        if not self.live:
            return f"SYSTEM:\n{system}\nPROMPT:\n{prompt[:500]}...\n{STUB}"
        # Uncomment for real calls
        # resp = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
        #     temperature=self.temperature,
        #     max_tokens=max_tokens
        # )
        # return resp.choices[0].message.content.strip()
        return STUB

_client_singleton: Optional[GPT5Client] = None

def get_client() -> GPT5Client:
    global _client_singleton
    if _client_singleton is None:
        _client_singleton = GPT5Client()
    return _client_singleton
