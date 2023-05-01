from typing import List, Union
from dataclasses import dataclass


@dataclass
class Message:
    to: Union[List[str], str]
    text: str
