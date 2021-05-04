from flask import jsonify
import json
from flask import request, session
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)
app.secret_key = "secretkey"
books = [
    {
        "author": "Hernando de Soto",
        "country": "Peru",
        "language": "English",
        "pages": 209,
        "title": "The Mystery of Capital",
        "year": 1970,
    },
    {
        "author": "Hans Christian Andersen",
        "country": "Denmark",
        "language": "Danish",
        "pages": 784,
        "title": "Fairy tales",
        "year": 1836,
    },
    {
        "author": "Dante Alighieri",
        "country": "Italy",
        "language": "Italian",
        "pages": 928,
        "title": "The Divine Comedy",
        "year": 1315,
    },
]

users = [
    {"username": "testuser", "password": "testuser"},
    {"username": "john", "password": "john"},
    {"username": "anne", "password": "anne"},
]
# Route for handling the login page logic


@app.route("/", methods=["GET", "POST"])
def redirect_get():
    if request.method == "GET":
        return redirect("static/register.html")
    else:
        # let them have books
        return redirect("/books")


def checkUser(username, password):
    for user in users:
        if username in user["username"] and password in user["password"]:
            return True
    return False


@app.route("/login", methods=["POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if checkUser(username, password):
            session["username"] = username
            return render_template(
                "index.html", title="books", username=session["username"], books=books
            )
        else:
            return "Please Register and Login"
    else:
        return 400


@app.route("/books", methods=["GET", "POST"])
def book():
    username = session["username"]
    if request.method == "POST":
        # expects pure json with quotes everywheree
        new_book = request.form["book"]
        myjson = json.loads(new_book)
        books.append(myjson)
        return render_template(
            "books.html", books=books, title="books", username=session["username"]
        )
    elif request.method == "GET":
        username = session["username"]
        return render_template(
            "books.html", books=books, title="books", username=session["username"]
        )
    else:
        return 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
