from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    id: str
    company: str
    title: str
    location: str
    url: str
    description: str = ""
    posted_at: Optional[str] = None
    source: str = ""

    def searchable_text(self) -> str:
        return " ".join([
            self.title or "",
            self.location or "",
            self.description or "",
        ]).lower()
