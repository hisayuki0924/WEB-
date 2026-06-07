from fastapi import FastAPI

app = FastAPI()

count = 0

@app.get("/")
def home():
    return {
        "message": "Python FastAPI running",
        "count": count
    }

@app.post("/add")
def add():
    global count
    count += 1
    return {"count": count}
