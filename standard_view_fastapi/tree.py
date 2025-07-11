from __future__ import annotations

from pydantic import BaseModel


class StandardViewNode(BaseModel):
    name: str
    value: str


class StandardViewTree(BaseModel):
    name: str
    nodes: list[StandardViewNode] | None = None
    branches: list[StandardViewTree] | None = None

    def __init__(self, name: str) -> None:
        super().__init__(name=name)
