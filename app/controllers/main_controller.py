from flask import Blueprint, render_template, session,flash
from flask_mail import  Message
from app import mail,db
import datetime         #Importing for mail date & time
from flask_login import current_user, login_required
from app.forms import PostForm
from app.models.model import Posts

# Define a Blueprint named 'main' for organizing routes and views
main = Blueprint('main', __name__)

# Route decorator to map the URL "/" to the index function
# Also maps URLs "/index" and "/home" to the same function
@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    # Check if 'logged_in' is in session and is True
    login_status = session.get('logged_in', False)
    return render_template("index.html", login=login_status)

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
    msg = Message("Hello from Flask", sender="cssedevconnect@gmail.com", recipients=["ramandatta87@gmail.com"])
    msg.body = f"This is a test email sent from Flask using Gmail. Mail Generated Time : {ct}"
    mail.send(msg)


@main.route("/add_post",methods=['GET','POST'])
@login_required  # Make sure the user is logged in
def add_post():
    form=PostForm()
    if form.validate_on_submit():
        post =  Posts(title=form.title.data, content=form.content.data, author_id= current_user.id, deleted=False, answered=False )
        form.title.data=''
        form.content.data=''

        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully")

    return render_template("/main/add_post.html",form=form)