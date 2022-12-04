from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schema
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model = List[schema.Post])
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int = 2, skip: int = 0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to fetch posts")
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
# def create_post(post: Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # similar to RETURNING above
    print(new_post.title)
    return new_post

@router.get('/{id}', response_model = schema.Post)
# def get_post(id: int):
#     cursor.execute(""" SELECT * from posts WHERE id = %s""", (str(id)))
#     post = cursor.fetchone()
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
#     return {'data': post}
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_query.first()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not found')
    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    delete_query.delete(synchronize_session=False)
    db.commit()
    return {'data': f'deleted post {id}'}

@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()