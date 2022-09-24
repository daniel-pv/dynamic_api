from dataclasses import dataclass


@dataclass
class Content:
    name = str
    body = str


@dataclass
class API:
    port = int
    route = str
    content = Content
