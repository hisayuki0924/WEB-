from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uuid

app = FastAPI()

users = {}       
sessions = {} 

class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(data: RegisterRequest):
    if data.username in users:
        raise HTTPException(status_code=400, detail="user already exists")

    users[data.username] = data.password
    return {"message": "user created", "user": data.username}


@app.post("/login")
def login(data: LoginRequest):
    if data.username in users and users[data.username] == data.password:
        token = str(uuid.uuid4())
        sessions[token] = data.username
        return {"message": "login success", "token": token}

    raise HTTPException(status_code=401, detail="invalid credentials")

@app.get("/me")
def me(authorization: str = Header(None)):
    if authorization in sessions:
        return {"user": sessions[authorization]}

    raise HTTPException(status_code=401, detail="not logged in")


@app.post("/logout")
def logout(authorization: str = Header(None)):
    if authorization in sessions:
        del sessions[authorization]
        return {"message": "logged out"}

    raise HTTPException(status_code=401, detail="not logged in")


# ----------------------
# テスト用トップ
# ----------------------
@app.get("/")
def root():
    return {"message": "auth system running"}
