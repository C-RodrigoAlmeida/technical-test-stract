from dataclasses import dataclass

@dataclass
class Insight:
    account_name: str
    platform: str
    data: dict