import uvicorn

from fastapi import FastAPI, status

from pydantic import BaseModel

app = FastAPI()
#app
#method=get
@app.get(/test)
async def get_item("/items/", response_model=Item, status_code=status.HTTP_201_CREATED):
return {ok}
if __name__ == "__main__":
uvicorn.run('app:app2', host="127.0.0.2", port=800, reload=True, access_log=False)
