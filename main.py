from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body 
# importing basemodel to create a schema for incoming data
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Createpostschema(BaseModel):
    title: str
    content: str
    # optional field if not provided by client
    published: bool = True
    rating: Optional[int] = None

all_posts = [{
    "title": "fastapi 1",
    "content": "checking it up",
    "id": 1
}, {
    "title": "fastapi 2",
    "content": "checking it up",
     "id": 2
}]

def find_post(id):
    for p in all_posts:
        if p["id"] == id:
            return p
        else:
            return {"msg": "Not found"}

@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/posts")
def get_posts():
    return {"data": all_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"post_details": post}

@app.post("/posts")
# def create_posts(payload: dict = Body(...)):    
# # return {"post":f"title {payload['title']} content: {payload['content']}"}

def create_posts(post: Createpostschema ):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    all_posts.append(post_dict)
    return{"data": post_dict}