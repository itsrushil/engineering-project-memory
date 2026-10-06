from dataclasses import dataclass, asdict
@dataclass
class Chunk:
    text: str
    source: str
    kind: str = "document"
    metadata: dict | None = None
    def to_dict(self):
        return asdict(self)
