from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from starlette.responses import RedirectResponse
from . import models
from .database import engine
from .routes import post, user, auth, vote

# from app import database

# commented out because alembic will be used for migration
# create the model on run if no new model
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
<<<<<<< HEAD
    # "https://youtube.com",
    # "https://www.google.com",
    # "http://localhost",
    # "http://localhost:8000",
    "*"
=======
    "https://youtube.com",
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8000",
>>>>>>> main
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")

async def root():
    response = RedirectResponse(url='/posts')
    return response



# # Using SQL to perform queries starts here
# Using SQL queries
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapis', user='postgres', password='!Alphaeagle123', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     if cursor.closed == True:
#         pass
#     else:
#         cursor = conn.cursor()
#         time.sleep(2)
#     print("connection successful")
# except Exception as error:
#     print("error connect")
#     print("Error:", error)
   

# all_posts = []

# def find_post(id):
#     for p in all_posts:
#         if p["id"] == id:
#             return p

# def find_post_index(id):
#     for i, p in enumerate(all_posts):
#         if p['id'] == id:
#             return i

# # Get all Posts
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}
    

# # Get one post with id
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     cursor.execute(""" select * from posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
#     return {"post_details": post}

# # Create a post
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: schemas.PostCreate ):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

#     new_post = cursor.fetchone()
#     conn.commit()
#     return{"data": new_post}

# # Delete a post
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
    
#     cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update a post
# @app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
# def update_post(id: int, post: schemas.PostCreate):

#     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

#     updated_post = cursor.fetchone()
#     conn.commit()

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

#     return {"data": updated_post}