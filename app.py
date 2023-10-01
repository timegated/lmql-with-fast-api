import requests
import lmql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float


items = {}

# @lmql.query
# def tell_a_joke():
#     '''lmql
#     """A list of good dad jokes. A indicates the punchline
#     Q: How does a penguin build its house?
#     A: Igloos it together.
#     Q: Which knight invented King Arthur's Round Table?
#     A: Sir Cumference.
#     Q:[JOKE]
#     A:[PUNCHLINE]""" where STOPS_AT(JOKE, "?") and  STOPS_AT(PUNCHLINE, "\n")
#     '''

someone = "USER"


@lmql.query
async def greet(someone_else):
    '''
    argmax "Greet {someone} and {someone_else}: [WHO]" from "openai/text-davinci-003" where len(WHO) < 20
    '''
    return None

@lmql.query
async def band_info(band):
    '''
    argmax 
    """
    Write a summary of {band}:
    {{
      "name": "[STRING_VALUE]",
      "age": [INT_VALUE],
      "top_songs": [[
         "[STRING_VALUE]",
         "[STRING_VALUE]"
      ]]
    }}
    """
from
    "openai/text-davinci-003"
where
    STOPS_BEFORE(STRING_VALUE, '"') and INT(INT_VALUE) and len(TOKENS(INT_VALUE)) < 2
    '''
    return None


@app.get("/lmql/direct")
async def direct_q():
    res = await lmql.run('argmax "Hello[WHO]" from "openai/text-ada-001" where len(TOKENS(WHO)) < 10')
    return res[0].prompt


@app.get("/lmql/bands")
async def get_band_info(query):
    if query == None:
        raise HTTPException(status_code=400, detail="query must not be empty")
    res = (await band_info(query))[0]
    return res

# READ LMQL GREET


@app.get("/lmql/greet")
async def get_response(query):
    if query == None:
        raise HTTPException(status_code=400, detail="query must not be empty")
    res = (await greet(query))[0]
    return res

# CREATE


@app.post("/items/")
async def create_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.id] = item
    return item

# READ


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# UPDATE


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

# DELETE


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}

# Call JSONPlaceholder API


@app.get("/jsonplaceholder/{resource}/{id}")
async def call_jsonplaceholder_api(resource: str, id: int):
    response = requests.get(
        f"https://jsonplaceholder.typicode.com/{resource}/{id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Resource not found")
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
