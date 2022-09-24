from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()



class User(BaseModel):
    name: str
    surname: str | None = None
    user_name: str
    email: str | None = None
    tax: float = 2.5
