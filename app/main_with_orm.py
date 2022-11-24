from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema
from .database import engine, get_db
from .utils import hash

# Creates the DB if it doesnt exists if it does then does nothing
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fast-api-project', user='postgres', password='Iaple312$', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(f'Database connection was succesful')
        break
    except Exception as err:
        print(f"Connection to database failed - {err}")
        time.sleep(2)

@app.get("/")
def root():
    return {"home": "Welcome to my Fast API project"}

@app.get("/posts", response_model = List[schema.Post])
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to fetch posts")
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
# def create_post(post: Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # similar to RETURNING above
    print(new_post.title)
    return new_post

@app.get('/posts/{id}', response_model = schema.Post)
# def get_post(id: int):
#     cursor.execute(""" SELECT * from posts WHERE id = %s""", (str(id)))
#     post = cursor.fetchone()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
#     return {'data': post}
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    if delete_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    delete_query.delete(synchronize_session=False)
    db.commit()
    return {'data': f'deleted post {id}'}

@app.put('/posts/{id}', response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    # return {'data': f'Updated post {id}'}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schema.UserCreateResponse)
def create_post(users: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(users.password)
    users.password = hashed_password
    new_user = models.Users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user