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


if __name__ == "__main__":
    uvicorn.run('app3:app', host="127.0.0.2", port=800, reload=True, access_log=False)
