from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uuid

app = FastAPI()

# 仮データ
users = {}
sessions = {}
notes = []
note_id_counter = 1


# ------------------
# リクエストモデル
# ------------------

class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class NoteRequest(BaseModel):
    content: str


# ------------------
# ユーザー登録
# ------------------
@app.post("/register")
def register(data: RegisterRequest):
    if data.username in users:
        raise HTTPException(status_code=400, detail="user already exists")

    users[data.username] = data.password
    return {"message": "user created", "user": data.username}


# ------------------
# ログイン
# ------------------
@app.post("/login")
def login(data: LoginRequest):
    if data.username in users and users[data.username] == data.password:
        token = str(uuid.uuid4())
        sessions[token] = data.username
        return {"message": "login success", "token": token}

    raise HTTPException(status_code=401, detail="invalid credentials")


# ------------------
# 自分の情報
# ------------------
@app.get("/me")
def me(authorization: str = Header(None)):
    if authorization in sessions:
        return {"user": sessions[authorization]}

    raise HTTPException(status_code=401, detail="not logged in")


# ------------------
# ログアウト
# ------------------
@app.post("/logout")
def logout(authorization: str = Header(None)):
    if authorization in sessions:
        del sessions[authorization]
        return {"message": "logged out"}

    raise HTTPException(status_code=401, detail="not logged in")


# ------------------
# メモ作成
# ------------------
@app.post("/notes")
def create_note(data: NoteRequest, authorization: str = Header(None)):
    global note_id_counter

    if authorization not in sessions:
        raise HTTPException(status_code=401, detail="not logged in")

    note = {
        "id": note_id_counter,
        "user": sessions[authorization],
        "content": data.content
    }

    notes.append(note)
    note_id_counter += 1

    return {"message": "note created", "note": note}


# ------------------
# メモ一覧
# ------------------
@app.get("/notes")
def get_notes():
    return notes


# ------------------
# メモ更新
# ------------------
@app.put("/notes/{note_id}")
def update_note(note_id: int, data: NoteRequest, authorization: str = Header(None)):
    if authorization not in sessions:
        raise HTTPException(status_code=401, detail="not logged in")

    for note in notes:
        if note["id"] == note_id:
            if note["user"] != sessions[authorization]:
                raise HTTPException(status_code=403, detail="not your note")

            note["content"] = data.content
            return {"message": "updated", "note": note}

    raise HTTPException(status_code=404, detail="note not found")


# ------------------
# メモ削除
# ------------------
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, authorization: str = Header(None)):
    if authorization not in sessions:
        raise HTTPException(status_code=401, detail="not logged in")

    for note in notes:
        if note["id"] == note_id:
            if note["user"] != sessions[authorization]:
                raise HTTPException(status_code=403, detail="not your note")

            notes.remove(note)
            return {"message": "deleted"}

    raise HTTPException(status_code=404, detail="note not found")


# ------------------
# ルート
# ------------------
@app.get("/")
def root():
    return {"message": "auth + notes system running"}
