from dataclasses import dataclass

@dataclass
class Pagination:
    current: int
    total: int
