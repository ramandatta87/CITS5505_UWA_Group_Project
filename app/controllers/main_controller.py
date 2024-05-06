from flask import Blueprint, render_template

# Define a Blueprint named 'main' for organizing routes and views
main = Blueprint('main', __name__)

# Route decorator to map the URL "/" to the index function
# Also maps URLs "/index" and "/home" to the same function
@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    # Render the index.html template with login set to False
    return render_template("index.html", login=False)

# Route decorator to map the URL "/forum" to the forum function
@main.route("/forum")
def forum():
    return render_template("forum.html")
