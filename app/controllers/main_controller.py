from flask import Blueprint, render_template, session,flash, redirect, url_for, request, Response, json
from flask_mail import  Message
from app import mail, db
import datetime         #Importing for mail date & time
from flask_login import current_user, login_required
from app.forms import PostForm
from app.models.model import Posts, Tag 

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


@main.route("/add_post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Check if the tag exists
        tag_text = form.tag.data.strip()
        tag = Tag.query.filter_by(tag=tag_text).first()

        # If the tag doesn't exist, create a new one
        if not tag:
            tag = Tag(tag=tag_text)
            db.session.add(tag)
            db.session.commit()

        # Create the new post
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            tag_id=tag.id,  # Use the tag's ID
            career_preparation=form.career_preparation.data,
            author_id=current_user.id,
            deleted=False,
            answered=False
        )
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully")
        return redirect(url_for('main.add_post'))
    
    return render_template("/main/add_post.html", form=form)

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    results = db.session.query(Tag.tag).filter(Tag.tag.like(f'%{search}%')).all()
    results = [result[0] for result in results]  # Extract names from tuples
    #app.logger.debug(results)
    return Response(json.dumps(results), mimetype='application/json')