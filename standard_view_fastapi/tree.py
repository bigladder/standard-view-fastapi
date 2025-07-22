from __future__ import annotations

import json
from enum import StrEnum
from typing import Any, Optional

from cache import StandardViewCacheFile
from pydantic import BaseModel


class StandardViewNodeType(StrEnum):
    OBJECT = ("OBJECT",)
    ARRAY = ("ARRAY",)
    DATA = ("DATA",)
    HEADER = ("HEADER",)
    META = ("META",)


class StandardViewNodeBase(BaseModel):
    type: StandardViewNodeType
    index_path: Optional[str] = None
    json_path: Optional[str] = None
    schema_path: Optional[str] = None
    exists: Optional[bool] = None
    key: Optional[str] = None
    key_title: Optional[str] = None
    description: Optional[str] = None
    units: Optional[str] = None
    error: Optional[str] = None

    def __init__(self, type: StandardViewNodeType, key: Optional[str] = None) -> None:
        super().__init__(type=type)

        self.key = key
        if self.key is not None and type is not StandardViewNodeType.HEADER:
            self.key_title = self.key.title().replace("_", " ")


class StandardViewObjectNode(StandardViewNodeBase):
    value: list[StandardViewNode] = []

    def __init__(self, key: Optional[str] = None) -> None:
        super().__init__(StandardViewNodeType.OBJECT, key)


class StandardViewArrayNode(StandardViewNodeBase):
    value: list[StandardViewNode] = []

    def __init__(self, key: Optional[str] = None) -> None:
        super().__init__(StandardViewNodeType.ARRAY, key)


class StandardViewDataNode(StandardViewNodeBase):
    value: Optional[str | int | float | complex] = None

    def __init__(self, key: Optional[str] = None) -> None:
        super().__init__(StandardViewNodeType.DATA, key)


class StandardViewHeaderNode(StandardViewNodeBase):
    title: str = ""
    subtitle: str = ""
    rootDataGroup: str = ""
    version: str = ""

    def __init__(self, title: str, subtitle: str, rootDataGroup: str, version: str) -> None:
        super().__init__(StandardViewNodeType.HEADER)

        self.title = title
        self.subtitle = subtitle
        self.rootDataGroup = rootDataGroup
        self.version = version


class StandardViewMetaNode(StandardViewNodeBase):
    value: list[StandardViewDataNode] = []

    def __init__(self, key: Optional[str] = None) -> None:
        super().__init__(StandardViewNodeType.META, key)


StandardViewNode = (
    StandardViewObjectNode
    | StandardViewArrayNode
    | StandardViewDataNode
    | StandardViewHeaderNode
    | StandardViewMetaNode
)


class StandardViewTree(BaseModel):
    filename: Optional[str] = None
    data: Optional[StandardViewObjectNode] = None
    error_paths: Optional[list[str]] = None

    def __init__(self, cache_file: Optional[StandardViewCacheFile]) -> None:
        super().__init__()

        if cache_file is not None:
            self.filename = cache_file.filename

            json_node = json.loads(cache_file.content)
            root_node = create_node(json_node, json_node["metadata"].get("schema_name"))
            if isinstance(root_node, StandardViewObjectNode):
                root_node.key_title = root_node.key
                self.data = root_node


class StandardViewTrees(BaseModel):
    tree0: Optional[StandardViewTree] = None
    tree1: Optional[StandardViewTree] = None
    diff_paths: Optional[list[str]] = None

    def __init__(
        self, cache_file0: Optional[StandardViewCacheFile], cache_file1: Optional[StandardViewCacheFile]
    ) -> None:
        super().__init__()

        if cache_file0 is not None:
            self.tree0 = StandardViewTree(cache_file0)
        if cache_file1 is not None:
            self.tree1 = StandardViewTree(cache_file1)
        if self.tree0 is not None and self.tree1 is not None:
            self.diff_paths = []


def create_node(json_node: Any, key: Optional[str] = None) -> StandardViewNode:
    parent_node: StandardViewNode

    if isinstance(json_node, dict):
        if key == "metadata":
            parent_node = StandardViewMetaNode(key)
        else:
            parent_node = StandardViewObjectNode(key)

        for json_key, json_value in json_node.items():
            if json_key == "metadata":
                header_node = StandardViewHeaderNode("title", "description", json_value.get("schema_name"), "version")
                if isinstance(parent_node, StandardViewObjectNode):
                    parent_node.value.append(header_node)

            child_node = create_node(json_value, json_key)
            if isinstance(parent_node, StandardViewObjectNode):
                parent_node.value.append(child_node)
            elif isinstance(parent_node, StandardViewMetaNode) and isinstance(child_node, StandardViewDataNode):
                parent_node.value.append(child_node)
    elif isinstance(json_node, list):
        parent_node = StandardViewArrayNode(key)

        for json_item in json_node:
            child_node = create_node(json_item)
            parent_node.value.append(child_node)
    else:
        parent_node = StandardViewDataNode(key)
        parent_node.value = json_node

    return parent_node
