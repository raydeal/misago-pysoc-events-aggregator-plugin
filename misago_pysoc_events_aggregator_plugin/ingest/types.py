from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NormalizedEvent:
    external_id: str
    title: str
    canonical_url: str
    description: str = ""
    starts_at: datetime | None = None
    location: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        data = asdict(self)
        if self.starts_at is not None:
            data["starts_at"] = self.starts_at.isoformat()
        data.update(self.payload)
        return data
