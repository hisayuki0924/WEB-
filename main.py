from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

notes = []
note_id = 1


class Note(BaseModel):
    content: str


@app.get("/")
def home():
    html = "<h1>My Notes</h1><ul>"
    for n in notes:
        html += f"<li>{n['id']}: {n['content']}</li>"
    html += """
    </ul>
    <form action="/add" method="post">
        <input name="content" />
        <button type="submit">Add</button>
    </form>
    """
    return html


@app.post("/add")
def add(note: Note):
    global note_id
    n = {"id": note_id, "content": note.content}
    notes.append(n)
    note_id += 1
    return {"ok": True, "note": n}


@app.delete("/delete/{id}")
def delete(id: int):
    global notes
    notes = [n for n in notes if n["id"] != id]
    return {"ok": True}
