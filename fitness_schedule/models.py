from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ClassStatus(str, Enum):
    PLANNED = "planned"
    CANCELLED = "cancelled"

@dataclass
class FitnessClass:
    class_id: int
    name: str
    starts_at: datetime
    capacity: int
    participants: list[str] = field(default_factory=list)
    status: ClassStatus = ClassStatus.PLANNED