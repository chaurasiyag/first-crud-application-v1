
from django.http import Http404
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo
#object of fastapi
app=FastAPI()
from database import (
    fetch_all_todo,fetch_one_todo,update_todo,remove_todo,create_todo
)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/',tags=["Root Page"])
def root():
    return {"PIng":"Pong"}

@app.get("/api/todo",tags=["Get todo"])
async def get_todo():
    response=await fetch_all_todo()
    return response


@app.get("/api/todo/{title}",response_model=Todo,tags=["Get todo"])
async def get_todo_by_title(title):
    response=await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404,"There is no todo item with ",title)

@app.post("/api/todo/",response_model=Todo,tags=["Create Todo"])
async def post_todo(todo:Todo):
    if len(todo.title)>0:
        response=await create_todo(todo.dict())
        if response:
            return response
        raise HTTPException(400,"Something went wrong with ")
    return {"Data Error":"Wrong Title"}

@app.put("/api/todo{title}",response_model=Todo,tags=["update todo"])
async def put_todo(title:str,desc:str):
    if len(title)>0:
        response=await update_todo(title,desc)
        if response:
            return response
        raise HTTPException(404,"There is no todo item with ",title)
    return {"Data Error":"Wrong Title"}


@app.delete("/api/todo/{title}",tags=["delete todo"])
async def delete_todo(title):
    if len(title)>0:
        response=await remove_todo(title)
        if response:
            return "Succesfullt deleted"
        raise HTTPException(404,"There is no todo item with ",title)
    return {"Data Error":"Wrong Title"}
