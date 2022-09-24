import uvicorn
from fastapi import FastAPI, status
from typing import Union
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


app = FastAPI()


#method=GET
@app.get("/root")
async def root():
    return {"Hello world!"}


if __name__ == "__main__":
    uvicorn.run('app1:app', host="127.0.0.1", port=800, reload=True, access_log=False)
