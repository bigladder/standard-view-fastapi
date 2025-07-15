from __future__ import annotations

import json
import numbers
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
    METADATA = ("METADATA",)
    ARRAY = ("ARRAY",)
    ARRAY_ELEMENT = ("ARRAY_ELEMENT",)


class StandardViewNode(BaseModel):
    type: StandardViewNodeType = StandardViewNodeType.DEFAULT
    key: Optional[str] = None
    key_title: Optional[str] = None
    value: Optional[Any] = None
    message: Optional[StandardViewMessage] = None
    nodes: Optional[list[StandardViewNode]] = None

    def __init__(self, json_node: Any, key: Optional[str] = None) -> None:
        super().__init__()
        self.key = key
        if self.key is not None:
            self.key_title = self.key.title().replace("_", " ")

            if "performance" in self.key:
                self.message = StandardViewMessage(StandardViewMessageType.ERROR, "This error is for testing.")
            else:
                self.message = StandardViewMessage(StandardViewMessageType.INFO, "This note is for testing.")

        if isinstance(json_node, dict):
            self.type = StandardViewNodeType.HEADER
            self.nodes = []
            for json_key, json_value in json_node.items():
                node = StandardViewNode(json_value, json_key)
                if self.key == "metadata":
                    node.type = StandardViewNodeType.METADATA
                self.nodes.append(node)
        elif isinstance(json_node, list):
            self.type = StandardViewNodeType.ARRAY
            if all(isinstance(json_item, numbers.Number) or isinstance(json_item, str) for json_item in json_node):
                self.value = json_node
            else:
                self.nodes = []
                for json_item in json_node:
                    node = StandardViewNode(json_item)
                    node.type = StandardViewNodeType.ARRAY_ELEMENT
                    self.nodes.append(node)
        else:
            self.type = StandardViewNodeType.DEFAULT
            self.value = json_node


class StandardViewTree(BaseModel):
    filename: str = ""
    nodes: list[StandardViewNode] = []

    def __init__(self, cache_file: StandardViewCacheFile) -> None:
        super().__init__()
        self.filename = cache_file.filename
        json_node = json.loads(cache_file.content)
        self.nodes = StandardViewNode(json_node).nodes or []
