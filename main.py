from fastapi import FastAPI

app = FastAPI()

count = 0

@app.get("/")
def home():
    return """
    <html>
        <body style="text-align:center;margin-top:100px;">
            <h1>My Site</h1>
            <p>Count: """ + str(count) + """</p>

            <form action="/add" method="post">
                <button>+1</button>
            </form>
        </body>
    </html>
    """

@app.post("/add")
def add():
    global count
    count += 1
    return {"count": count}
