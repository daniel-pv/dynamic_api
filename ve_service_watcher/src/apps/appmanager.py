from fastapi import FastAPI
from starlette.responses import RedirectResponse
from model import *
import importlib

appmanager = FastAPI()
# for endpoint in ["user", "item"]:
#    plugin_module = importlib.import_module(endpoint, "app")
#    app.include_router(plugin_module.router)
# if __name__ == "__main__": uvicorn.run('app1:app', host="127.0.0.1", port=800, reload=True, access_log=False)


@appmanager.get("/")
async def create_item():
    response = RedirectResponse(url='/docs')
    return response

subapp = importlib.import_module('users', "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("apptwo", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("apptwo", "appmanager")
appmanager.include_router(subapp.router)


subapp = importlib.import_module("appone", "appmanager")
appmanager.include_router(subapp.router)
