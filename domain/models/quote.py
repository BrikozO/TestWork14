from dataclasses import dataclass


@dataclass
class Quote:
    author: str
    text: str
    tags: list[str]
