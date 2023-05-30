from dataclasses import dataclass, field
from typing import Optional

from core.settings import ID_GENERATOR


@dataclass
class PeopleCounter:
    name: str
    ts: str
    in_: int
    out: int
    id_: Optional[str] = None

    def __post_init__(self):
        if self.id_ is None:
            self.id_ = str(ID_GENERATOR())

    @property
    def flow(self):
        return self.in_ - self.out
