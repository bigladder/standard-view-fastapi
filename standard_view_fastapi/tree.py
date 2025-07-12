from __future__ import annotations

import builtins
import json
from typing import Any, Optional

from cache import StandardViewCacheFile
from pydantic import BaseModel


def add_nodes(nodes: list[StandardViewNode], json_node: Any) -> None:
    for key, value in json_node.items():
        node = StandardViewNode(key)
        nodes.append(node)

        match type(value):
            case builtins.dict:
                if value.items():
                    node.nodes = []
                    add_nodes(node.nodes, value)
            case _:
                node.value = value


class StandardViewNode(BaseModel):
    key: str = ""
    display_key: str = ""
    value: Any = None
    nodes: Optional[list[StandardViewNode]] = None

    def __init__(self, key: str) -> None:
        super().__init__(key=key)

        self.display_key = self.key.title().replace("_", " ")


class StandardViewTree(BaseModel):
    filename: str = ""
    nodes: list[StandardViewNode] = []

    def __init__(self, cache_file: StandardViewCacheFile) -> None:
        super().__init__(filename=cache_file.filename)

        json_node = json.loads(cache_file.content)
        add_nodes(self.nodes, json_node)
