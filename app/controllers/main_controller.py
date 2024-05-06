from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    return render_template("index.html", login=False)

@main.route("/forum")
def forum():
    return render_template("forum.html")
