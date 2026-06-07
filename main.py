const express = require("express");
const app = express();

let count = 0;

app.get("/", (req, res) => {
  res.send(`
    <html>
      <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
        <h1>Simple Site</h1>
        <p>Count: ${count}</p>
        <form method="POST" action="/add">
          <button style="font-size:20px;">+1</button>
        </form>
      </body>
    </html>
  `);
});

app.post("/add", (req, res) => {
  count++;
  res.redirect("/");
});

app.listen(3000);
