from dataclasses import dataclass
from typing import Optional


@dataclass
class EndPoint:
    method: str
    route: str
    name: str
    params: str
    payload: str
    api_name: str


@dataclass
class Api:
    api_name: str
    main_api: bool
    endpoints: Optional[list[EndPoint]]
    api_file_name: str


@dataclass
class ApiFile:
    api_file_name: str
    imports: Optional[list[str]]
    variables: Optional[list[str]]
    apis: Optional[list[Api]]
    port: str
    host: str

    def __eq__(self, __o) -> bool:
        return self.api_file_name == __o.api_file_name and \
            self.port == __o.port and \
            self.host == __o.host
