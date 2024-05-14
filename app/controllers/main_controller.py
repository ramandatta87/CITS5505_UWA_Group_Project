from flask import Blueprint, render_template, session,flash, redirect, url_for, request, Response, json, jsonify
from flask_mail import  Message
from app import mail, db
import datetime         #Importing for mail date & time
from flask_login import current_user, login_required
from app.forms import PostForm
from app.models.model import Posts, Tag, User 

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


@main.route('/posts')
def posts():
    # Get query parameters
    order = request.args.get('order', 'asc')
    filter_by = request.args.get('filter_by', 'author')
    filter_value = request.args.get('filter_value', '')

    # Base query
    query = Posts.query.join(User, Posts.author_id == User.id).join(Tag, Posts.tag_id == Tag.id)

    # Apply filtering if filter_by and filter_value are provided
    if filter_by and filter_value:
        if filter_by == 'author':
            query = query.filter((User.first_name.ilike(f'%{filter_value}%')) | (User.last_name.ilike(f'%{filter_value}%')))
        elif filter_by == 'title':
            query = query.filter(Posts.title.ilike(f'%{filter_value}%'))
        elif filter_by == 'tag':
            query = query.filter(Tag.tag.ilike(f'%{filter_value}%'))

    # Apply sorting
    if order == 'desc':
        query = query.order_by(Posts.date_posted.desc())
    else:
        query = query.order_by(Posts.date_posted.asc())

    # Execute query
    posts = query.all()

    return render_template("main/posts.html", posts=posts)

@main.route('/api/posts')
def api_posts():
    # Get query parameters
    order = request.args.get('order', 'asc')
    filter_by = request.args.get('filter_by', 'author')
    filter_value = request.args.get('filter_value', '')

    # Base query
    query = Posts.query.join(User, Posts.author_id == User.id).join(Tag, Posts.tag_id == Tag.id)

    # Apply filtering if filter_by and filter_value are provided
    if filter_by and filter_value:
        if filter_by == 'author':
            query = query.filter((User.first_name.ilike(f'%{filter_value}%')) | (User.last_name.ilike(f'%{filter_value}%')))
        elif filter_by == 'title':
            query = query.filter(Posts.title.ilike(f'%{filter_value}%'))
        elif filter_by == 'tag':
            query = query.filter(Tag.tag.ilike(f'%{filter_value}%'))

    # Apply sorting
    if order == 'desc':
        query = query.order_by(Posts.date_posted.desc())
    else:
        query = query.order_by(Posts.date_posted.asc())

    # Execute query
    posts = query.all()

    # Serialize posts to JSON
    posts_data = []
    for post in posts:
        post_data = {
            'title': post.title,
            'content': post.content,
            'author_first_name': post.author.first_name,
            'author_last_name': post.author.last_name,
            'tag': post.tag.tag,
            'date_posted': post.date_posted.strftime('%B %d, %Y')
        }
        posts_data.append(post_data)

    return jsonify(posts_data)

@main.route('/api/autocomplete_posts', methods=['GET'])
def autocomplete_posts():
    search = request.args.get('q')
    filter_by = request.args.get('filter_by', 'author')

    if not search:
        return jsonify([])

    if filter_by == 'author':
        users = User.query.filter((User.first_name.ilike(f'%{search}%')) | (User.last_name.ilike(f'%{search}%'))).all()
        suggestions = [f'{user.first_name} {user.last_name}' for user in users]
    elif filter_by == 'title':
        posts = Posts.query.filter(Posts.title.ilike(f'%{search}%')).all()
        suggestions = [post.title for post in posts]
    elif filter_by == 'tag':
        tags = Tag.query.filter(Tag.tag.ilike(f'%{search}%')).all()
        suggestions = [tag.tag for tag in tags]
    else:
        suggestions = []

    return jsonify(suggestions)

# Route to display the logged-in user's posts
@main.route('/my_posts')
@login_required  # Ensures that only logged-in users can access this route
def my_posts():
    # Query to get posts by the current logged-in user, ordered by the date posted
    user_posts = Posts.query.filter_by(author_id=current_user.id).order_by(Posts.date_posted.desc()).all()
    # Render the my_posts.html template with the user's posts
    return render_template('main/my_posts.html', posts=user_posts)

# Route to view a single post by ID
@main.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    # Fetch the post by ID, return 404 if not found
    post = Posts.query.get_or_404(post_id)
    # Fetch the author of the post
    author = User.query.get_or_404(post.author_id)
    # Render the view_post.html template with the post and author details
    return render_template('main/view_post.html', post=post, author=author)