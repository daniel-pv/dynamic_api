import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


#method=GET
@app.get("/test")
async def get_item():
    return {'ok'}


#method=GET
@app.get("/books")
async def get_book():
    return {'ok':'go'}


subapp = FastAPI()
app.mount("/subapp", subapp)


#method=GET
@subapp.get("/sub")
async def get_sub():
    return {'browsers':{'firefox':{'name':'Firefox','pref_url':'about:config','releases':{'1':{'release_date':'2004-11-09','status':'retired','engine':'Gecko','engine_version':'1.7'}}}}}


if __name__ == "__main__":
    uvicorn.run('app4:app', host="127.0.0.2", port=800, reload=True, access_log=False)
