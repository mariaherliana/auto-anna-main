from dataclasses import dataclass


@dataclass
class Files:
    client: str
    dashboard: str
    console: str
    output: str


Config = list[Files]
