from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class StandardViewNode(BaseModel):
    name: str
    value: str


class StandardViewTree(BaseModel):
    name: str
    nodes: Optional[list[StandardViewNode]] = None
    branches: Optional[list[StandardViewTree]] = None

    def __init__(self, name: str) -> None:
        super().__init__(name=name)
