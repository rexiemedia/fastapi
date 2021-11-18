from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body 

# importing basemodel to create a schema for incoming data
from pydantic import BaseModel
from random import randrange

from starlette.responses import Response

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
},{
    "title": "fastapi 2",
    "content": "checking it up",
     "id": 2
}]

def find_post(id):
    for p in all_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(all_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!!"}

# Get all Posts
@app.get("/posts")
def get_posts():
    return {"data": all_posts}

# Get one post with id
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return {"post_details": post}

# Create a post
@app.post("/posts")
# def create_posts(payload: dict = Body(...)):    
# # return {"post":f"title {payload['title']} content: {payload['content']}"}

def create_posts(post: Createpostschema ):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    all_posts.append(post_dict)
    return{"data": post_dict}

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
   index = find_post_index(id)
   if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")
   all_posts.pop(index)
   return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, post: Createpostschema):
   index = find_post_index(id)
   if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")
   post_dict = post.dict()
   post_dict['id'] = id
   all_posts[index] = post_dict

   return {"data": post_dict}