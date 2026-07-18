from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    provider: str = "none"
    model: str = ""
    api_base: Optional[str] = None


class LLMRouter:
    """Provider-agnostic LLM config holder for future orchestration prompts.

    Supported provider labels are intentionally flexible to enable OpenAI,
    Anthropic, local models, and LangChain-backed adapters.
    """

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def summary(self) -> str:
        if self.config.provider == "none":
            return "LLM disabled (rule-based scaffold mode)."
        model = self.config.model or "default-model"
        return f"LLM provider: {self.config.provider}, model: {model}"
