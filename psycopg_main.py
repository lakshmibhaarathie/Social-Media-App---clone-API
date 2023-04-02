from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from fastapi.responses import Response
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(database="fastapi",user="postgres"
                            ,password="sql123",cursor_factory=RealDictCursor)
    cur = conn.cursor()
except Exception as e:
    raise e


class Post(BaseModel):
    title: str
    content: str
    published:bool=True
    user_id: int


app = FastAPI()

@app.get("/")
def home():
    return {"home":"Welcome to the API..."}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"msg":posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"msg":"This return latest post."}


@app.get("/posts/{id}")
def get_one_post(id:int):
    print(type(str(id)))
    cur.execute("""SELECT * FROM posts WHERE id=%s;""",(str(id),))
    post = cur.fetchone()
    if not post:
        return Response( status_code=status.HTTP_404_NOT_FOUND, content=f"The post with id {id} does not exists")
    return {"msg":post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(schema:Post):
    try:
        cur.execute("""INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *""", (
            schema.title, schema.content, schema.published, schema.user_id
        ))
        post = cur.fetchone()
        return {"msg":post}
    except Exception as e:
        return Response(content=e, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.put("/posts/{id}")
def update_post(id:int, schema:Post):
    cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s, user_id=%s WHERE id = %s RETURNING *;""",
                (schema.title, schema.content, schema.published, schema.user_id, str(id)))
    post = cur.fetchone()
    if not post:
        return Response(content=f"Post with id {id} doesnot exists", status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return {"msg":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("""DELETE FROM posts WHERE id = %s""",(str(id),))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, content=f"Post with {id} deleted.")



