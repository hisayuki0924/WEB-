from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uuid

app = FastAPI()

users = {}
sessions = {}
notes = []
note_id = 1


class Auth(BaseModel):
    username: str
    password: str


class Note(BaseModel):
    content: str


def get_user(token: str):
    if token not in sessions:
        raise HTTPException(401, "not logged in")
    return sessions[token]


@app.post("/register")
def register(data: Auth):
    if data.username in users:
        raise HTTPException(400, "exists")
    users[data.username] = data.password
    return {"ok": True}


@app.post("/login")
def login(data: Auth):
    if users.get(data.username) != data.password:
        raise HTTPException(401, "bad credentials")
    token = str(uuid.uuid4())
    sessions[token] = data.username
    return {"token": token}


@app.get("/me")
def me(authorization: str = Header(None)):
    return {"user": get_user(authorization)}


@app.post("/notes")
def create(note: Note, authorization: str = Header(None)):
    global note_id
    user = get_user(authorization)

    n = {"id": note_id, "user": user, "content": note.content}
    notes.append(n)
    note_id += 1
    return n


@app.get("/notes")
def get_my_notes(authorization: str = Header(None)):
    user = get_user(authorization)
    return [n for n in notes if n["user"] == user]


@app.put("/notes/{note_id}")
def update(note_id: int, data: Note, authorization: str = Header(None)):
    user = get_user(authorization)

    for n in notes:
        if n["id"] == note_id:
            if n["user"] != user:
                raise HTTPException(403, "not yours")
            n["content"] = data.content
            return n

    raise HTTPException(404, "not found")


@app.delete("/notes/{note_id}")
def delete(note_id: int, authorization: str = Header(None)):
    user = get_user(authorization)

    for n in notes:
        if n["id"] == note_id:
            if n["user"] != user:
                raise HTTPException(403, "not yours")
            notes.remove(n)
            return {"ok": True}

    raise HTTPException(404, "not found")
