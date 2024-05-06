from flask import Blueprint, render_template
from flask_mail import  Message
from app import mail
import datetime         #Importing for mail date & time

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

@main.route("/mailcheck")
def mailcheck():            #Sample route for sending email from flask
    mail_check()
    return render_template("index.html",login=False)

def mail_check(): # Sample function to test email

    # ct stores current time
    ct = datetime.datetime.now() 
    msg = Message("Hello from Flask", sender="cssedevconnect@gmail.com", recipients=["ramandatta87@gmail.com"," loujinsen@hotmail.com"])
    msg.body = f"This is a test email sent from Flask using Gmail. Mail Generated Time : {ct}"
    mail.send(msg)