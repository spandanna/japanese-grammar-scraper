"""FastAPI with /random and /all endpoints.

Run using ``uvicorn api.main:app --reload``
"""

import json
import random

from fastapi import FastAPI

with open("api/VERSION") as f:
    version = f.read()

with open("data/output.json") as f:
    grammar_data = json.loads(f.read())

app = FastAPI(version=version)


@app.get("/")
async def root():
    return {"version": app.version}


@app.get("/random")
async def get_random():
    """Get a random grammar point from the output data."""
    grammar_point = random.choice(grammar_data)
    return grammar_point


@app.get("/all")
async def get_all():
    """Get all grammar points in the output data."""
    return grammar_data
