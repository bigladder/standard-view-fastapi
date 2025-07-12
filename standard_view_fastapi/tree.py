from __future__ import annotations

import builtins
import json
from enum import StrEnum
from typing import Any, Optional

from cache import StandardViewCacheFile
from pydantic import BaseModel


class StandardViewMessageType(StrEnum):
    INFO = ("INFO",)
    WARNING = ("WARNING",)
    ERROR = ("ERROR",)


class StandardViewMessage(BaseModel):
    type: StandardViewMessageType = StandardViewMessageType.INFO
    value: str = ""

    def __init__(self, type: StandardViewMessageType, value: str) -> None:
        super().__init__()
        self.type = type
        self.value = value


class StandardViewNodeType(StrEnum):
    DEFAULT = ("DEFAULT",)
    HEADER = ("HEADER",)
    GROUP = ("GROUP",)
    METADATA = ("METADATA",)
    ARRAY = ("ARRAY",)


class StandardViewNode(BaseModel):
    type: StandardViewNodeType = StandardViewNodeType.DEFAULT
    key: str = ""
    key_title: str = ""
    value: Optional[Any] = None
    message: Optional[StandardViewMessage] = None
    nodes: Optional[list[StandardViewNode]] = None

    def __init__(self, key: str, json_node: Any) -> None:
        super().__init__()
        self.key = key
        self.key_title = self.key.title().replace("_", " ")

        match type(json_node):
            case builtins.dict:
                self.type = StandardViewNodeType.HEADER
                self.nodes = []
                for json_key, json_value in json_node.items():
                    node = StandardViewNode(json_key, json_value)
                    if key == "metadata":
                        node.type = StandardViewNodeType.METADATA
                    self.nodes.append(node)
            case builtins.list:
                self.type = StandardViewNodeType.ARRAY
                self.value = json_node
            case _:
                self.type = StandardViewNodeType.DEFAULT
                self.value = json_node


class StandardViewTree(BaseModel):
    filename: str = ""
    nodes: list[StandardViewNode] = []

    def __init__(self, cache_file: StandardViewCacheFile) -> None:
        super().__init__()
        self.filename = cache_file.filename
        json_node = json.loads(cache_file.content)
        self.nodes = StandardViewNode("", json_node).nodes or []
