from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Đây là trang chủ!!!"

@app.route("/news")
def news():
    return "<h1>Đây là trang tin tức!!!</h1>"

@app.route("/news/<page>", default={"page": 1})
def news(page):
    return f"<h1>Đây là trang tin tức!!! {page}</h1>"

app.run()