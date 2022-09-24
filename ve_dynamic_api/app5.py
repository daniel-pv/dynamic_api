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
@app.get("/")
async def get_root():
    return {'Hello': 'World'}
#method=GET
@app.get("/items/{item_id}")
async def get_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}
#method=PUT
@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}


subapp = FastAPI()
app.mount("/subapp", subapp)


#method=GET
@subapp.get("/sub")
async def get_sub():
    return {'browsers':{'firefox':{'name':'Firefox','pref_url':'about:config','releases':{'1':{'release_date':'2004-11-09','status':'retired','engine':'Gecko','engine_version':'1.7'}}}}}


if __name__ == "__main__":
    uvicorn.run('app5:app', host="127.0.0.2", port=800, reload=True, access_log=False)
