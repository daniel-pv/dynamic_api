import uvicorn
from fastapi import FastAPI, status
app = FastAPI()


#method=GET
@app.get("/")
async def root():
    return {'Hello': 'World'}


if __name__ == "__main__":
    uvicorn.run('app2test:app', host="127.0.0.2", port=8000, reload=True, access_log=False)
