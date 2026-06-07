from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

count = 0

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
        <body style="text-align:center;font-family:sans-serif;margin-top:100px;">
            <h1>My Website</h1>
            <h2>Count: {count}</h2>

            <form action="/add" method="post">
                <button style="font-size:20px;">+1</button>
            </form>
        </body>
    </html>
    """

@app.post("/add")
def add():
    global count
    count += 1
    return {"count": count}
