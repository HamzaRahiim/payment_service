from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    content: str


app: FastAPI = FastAPI(
    title="TODO Service App",
    description="A simple Todo CRUD application",
    version="1.0.0",
    root_path="/todo-service",
    root_path_in_servers=True,
)


@app.get("/", tags=["Main"])
def root():
    return {"Message": "Todo App running :-}"}


@app.post("/create-todo")
def create_todo(todo: Todo):
    return todo
