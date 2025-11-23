from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Expanding the dictionary with more dummy posts
text_posts = {
    1: {
        "title": "New Post",
        "content": "Cool test post"
    },
    2: {
        "title": "Second Post",
        "content": "This is the content for the second post. It's just an example!"
    },
    3: {
        "title": "Learning FastAPI",
        "content": "FastAPI is a modern web framework for building APIs with Python. It's fast and easy to use."
    },
    4: {
        "title": "Tech News",
        "content": "Tech News: Python continues to evolve and improve every year with new features and better performance."
    },
    5: {
        "title": "Exploring ASGI",
        "content": "ASGI is a specification for asynchronous Python web servers and applications. It's gaining popularity!"
    },
    6: {
        "title": "FastAPI Tips",
        "content": "FastAPI provides great developer experience with automatic documentation generation. Don't miss the docs!"
    }
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    
    if limit is not None:

        if limit > len(text_posts):
            raise HTTPException(status_code=400, detail=f"Limit exceeds number of posts available. Max is {len(text_posts)}.")

        limited_posts = dict(list(text_posts.items())[:limit])
        return limited_posts
    
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    """Fetch a single post by ID"""
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return text_posts[id]

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    
    return text_posts

@app.delete("/posts")
def delete_post():
    pass
    