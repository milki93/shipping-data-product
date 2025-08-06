from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from . import crud, schemas

app = FastAPI(title="Shipping Data Analytical API")

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = Query(10, ge=1, le=100)):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str):
    result = crud.get_channel_activity(channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResult])
def search_messages(query: str = Query(..., min_length=1)):
    return crud.search_messages(query)
