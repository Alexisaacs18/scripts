from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class GenerateRequest:
    messages: list = field(default_factory=list)
    page_count: int = 3


@dataclass
class GenerateResponse:
    script: str


@dataclass
class ScriptInfo:
    name: str
    size_bytes: int
