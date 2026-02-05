from dataclasses import dataclass


@dataclass
class GenerateRequest:
    prompt: str
    page_count: int = 90


@dataclass
class GenerateResponse:
    script: str


@dataclass
class ScriptInfo:
    name: str
    size_bytes: int
