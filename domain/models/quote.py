from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Quote:
    """Quote object

    Attributes:
        author (str): The author of the quote
        text (str): The text of the quote
        tags (list[str]): The tags of the quote
        parsed_at (datetime): The date and time the quote was parsed
    """

    author: str
    text: str
    tags: list[str]
    parsed_at: datetime = field(default_factory=datetime.now)
