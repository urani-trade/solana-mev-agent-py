# -*- encoding: utf-8 -*-
#!/usr/bin/env python3
# protocol_server/_server.py

import os
import json

from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.protocol_server.utils.file_operations import load_data, save_data


app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Load and save data paths
BATCHES_FILE_PATH = os.path.join(os.path.dirname(__file__), "orderbook/batches/batch.json")
SOLUTIONS_FILE_PATH = os.path.join(os.path.dirname(__file__), "orderbook/solutions/solution.json")

# Mount the static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/")
def say_hi(request: Request):
    """Return the home page with a background image."""
    return templates.TemplateResponse("index.html", {"request": request})


# API for the batches endpoint
@app.get("/batches")
def get_orderbook(request: Request):
    """Get all items."""
    try:
        data = load_data(BATCHES_FILE_PATH)
        pretty_data = json.dumps(data, indent=4)
        return templates.TemplateResponse("batches.html", {"request": request, "data": pretty_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batches", status_code=201)
async def post_solutions(request: Request):
    """Post User batches."""
    try:
        # Parse JSON body
        body = await request.json()
        # Save data to the file
        save_data(BATCHES_FILE_PATH,body)
        # Build the full URL of the endpoint
        full_url = str(request.url)
        return JSONResponse(content={"message": f"Data successfully posted at {full_url}"}, status_code=201) 

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error decoding JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# API for the solutions endpoint
@app.get("/solutions")
def get_solutions(request: Request):
    """Get all solutions."""
    try:
        data = load_data(SOLUTIONS_FILE_PATH)
        pretty_data = json.dumps(data, indent=4)
        return templates.TemplateResponse("solutions.html", {"request": request, "data": pretty_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/solutions", status_code=201)
async def post_solutions(request: Request):
    """Post solutions."""
    try:
        # Parse JSON body
        body = await request.json()
        # Save data to the file
        save_data(SOLUTIONS_FILE_PATH,body)
        return 
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error decoding JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
