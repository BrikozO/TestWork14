from dataclasses import dataclass


@dataclass
class Quote:
    """Quote object

    Attributes:
        author (str): The author of the quote
        text (str): The text of the quote
        tags (list[str]): The tags of the quote
    """
    author: str
    text: str
    tags: list[str]
