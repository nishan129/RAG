from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

class SkippedIntent(Exception):
    pass

class Invoker(ABC):
    """Abstract base class for invokers."""

    @abstractmethod
    def invoke(self, question:str, flags:dict, intent: str) -> tuple[Any, list]:
        ...

    
class ServiceInvoker(Invoker):
    SUPPORTED_INTENTS = {"rag", "web_fallback"}

    def invoke(
            self, question: str, flags:dict, intent: str
    )-> tuple[Any, list]:
        raise NotImplementedError(
            "RAG service is not implemented in Lesson 0."
            "Switch to the lesson-1-naive branch to enable retrieval-based eval"
        )