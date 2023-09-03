from typing import List, Union
from dataclasses import dataclass
from enum import Enum
from furl import furl


@dataclass
class Message:
    to: Union[List[str], str]
    text: str


class Unraid_Severity(Enum):
    NORMAL = 'normal'
    WARN = 'warning'
    ERR = 'alert'


@dataclass
class Unraid_Notification:
    severity: Unraid_Severity   # -i
    event: str                  # -e
    subject: str                # -s
    description: str            # -d
    link: furl                  # -l
