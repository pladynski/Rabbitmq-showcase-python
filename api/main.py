import json
from functools import lru_cache
from typing import Annotated

import uvicorn
from config import Settings
from fastapi import Depends, FastAPI
from fastapi.concurrency import run_in_threadpool
from graft_pypi_balance_service import GraftConfig as BalanceGraftConfig
from graft_pypi_balance_service.balance_graft import BalanceService
from graft_pypi_notify_service import GraftConfig as NotifyGraftConfig
from graft_pypi_notify_service.notify_graft import NotifyService

description = """
Microservice boilerplate 🚀

## Usage
- Pass foo data to any of API's endpoints (You can use foo data from down below)
- Look up to your terminal

{ 
"id": 50, 
"user_id": 12, 
"title": "Hello world", 
"description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", 
"category_id": 4, 
"price": "5000" 
}



"""

settings = Settings()
NotifyGraftConfig.host = settings.first_service_graft_host
BalanceGraftConfig.host = settings.second_service_graft_host
app = FastAPI(description=description)


@lru_cache
def get_settings():
    return Settings()


@app.post("/api/user/subscribe")
def subscribe_user(data: dict, settings: Annotated[Settings, Depends(get_settings)]):
    NotifyService.notify_user(json.dumps(data))
    return {"detail": "User subscribed."}


@app.post("/api/order/checkout")
async def order_checkout(data: dict, settings: Annotated[Settings, Depends(get_settings)]):
    await run_in_threadpool(BalanceService.change_balance, json.dumps(data))
    return {"detail": "Order created."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="debug", reload=True)
