from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {
    "admin": "1234",
    "test": "pass"
}

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: LoginRequest):
    if data.username in users and users[data.username] == data.password:
        return {"message": "login success", "user": data.username}
    
    raise HTTPException(status_code=401, detail="invalid credentials")
