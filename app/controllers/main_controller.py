from flask import Blueprint, render_template, session, flash, redirect, url_for, request, Response, jsonify,json,g 
from flask_mail import Message
from app import mail, db
import datetime
from flask_login import current_user, login_required
from app.forms import PostForm, FilterSortForm, ReplyForm, FilterSortForm
from app.models.model import Posts, Tag, User, Reply, FavoritePost
from sqlalchemy import func

# Define a Blueprint named 'main' for organizing routes and views
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    # Check if the user is logged in
    if current_user.is_authenticated:
        # If logged in, redirect to the posts page
        return redirect(url_for('main.posts'))
    else:
        # If not logged in, render the index page
        login_status = session.get('logged_in', False)
        return render_template("index.html", login=login_status)


@main.route("/mailcheck")
def mailcheck():
    mail_check()
    return render_template("index.html", login=False)

def mail_check():
    ct = datetime.datetime.now()
    msg = Message("Hello from Flask", sender="cssedevconnect@gmail.com", recipients=["ramandatta87@gmail.com"])
    msg.body = f"This is a test email sent from Flask using Gmail. Mail Generated Time : {ct}"
    mail.send(msg)

@main.route("/add_post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        tag_text = form.tag.data.strip()
        tag = Tag.query.filter_by(tag=tag_text).first()
        if not tag:
            tag = Tag(tag=tag_text)
            db.session.add(tag)
            db.session.commit()

        # Map the radio button value to 0 or 1 for career_preparation
        career_preparation_value = 1 if form.question_type.data == 'career' else 0

        post = Posts(
            title=form.title.data,
            content=form.content.data,
            tag_id=tag.id,
            career_preparation=career_preparation_value,  # Use the mapped value
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
    results = [result[0] for result in results]
    return Response(json.dumps(results), mimetype='application/json')

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
            'id': post.id,  # Ensure the ID is included in the response
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

@main.route('/my_posts')
@login_required
def my_posts():
    user_posts = Posts.query.filter_by(author_id=current_user.id).order_by(Posts.date_posted.desc()).all()
    return render_template('main/my_posts.html', posts=user_posts)

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Posts.query.get_or_404(post_id)
    author = User.query.get_or_404(post.author_id)
    replies = Reply.query.filter_by(post_id=post_id).order_by(Reply.timestamp.asc()).all()
    form = ReplyForm()

    if form.validate_on_submit():
        reply = Reply(
            post_id=post_id,
            author_id=current_user.id,
            answer=form.answer.data,
            answered_accepted=False,
            deleted=False
        )
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been added.', 'success')
        return redirect(url_for('main.view_post', post_id=post_id))

    return render_template('main/view_post.html', post=post, author=author, replies=replies, form=form)

@main.route('/post/toggle_answer/<int:reply_id>', methods=['POST'])
@login_required
def toggle_answer(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    post = Posts.query.get_or_404(reply.post_id)

    if post.author_id != current_user.id:
        return jsonify({'success': False}), 403

    action = request.json.get('action')
    if action == 'accept':
        reply.answered_accepted = True
    elif action == 'reject':
        reply.answered_accepted = False

    db.session.commit()
    return jsonify({'success': True})

@main.route('/post/edit_reply/<int:reply_id>', methods=['POST'])
@login_required
def edit_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)

    if reply.author_id != current_user.id or reply.answered_accepted:
        return jsonify({'success': False}), 403

    new_answer = request.json.get('answer')
    reply.answer = new_answer
    db.session.commit()
    return jsonify({'success': True})

@main.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)

    if post.author_id != current_user.id:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('main.view_post', post_id=post_id))

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        tag = Tag.query.filter_by(tag=form.tag.data).first()
        if tag is None:
            tag = Tag(tag=form.tag.data)
            db.session.add(tag)
            db.session.commit()
        post.tag_id = tag.id
        post.career_preparation = form.career_preparation.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tag.data = post.tag.tag if post.tag else ''
        form.career_preparation.data = post.career_preparation

    return render_template('main/edit_post.html', title='Edit Post', form=form, post=post)

@main.route("/posts", methods=["GET", "POST"])
def posts():
    form = FilterSortForm()
    query = Posts.query

    search_query = request.args.get('q', '')

    if search_query:
        if search_query.startswith('[') and search_query.endswith(']'):
            tag_name = search_query[1:-1]
            tag = Tag.query.filter(Tag.tag.ilike(f'%{tag_name}%')).first()
            if tag:
                query = query.filter_by(tag_id=tag.id)
            else:
                query = query.filter_by(id=None)  # No results
        else:
            query = query.filter(
                (Posts.title.ilike(f'%{search_query}%')) |
                (Posts.content.ilike(f'%{search_query}%'))
            )
    else:
        if form.validate_on_submit():
            filter_by = form.filter_by.data
            filter_value = form.filter_value.data
            order = form.order.data

            if filter_by == 'author':
                query = query.join(User).filter(User.first_name.contains(filter_value) | User.last_name.contains(filter_value))
            elif filter_by == 'title':
                query = query.filter(Posts.title.contains(filter_value))
            elif filter_by == 'tag':
                query = query.join(Tag).filter(Tag.tag.contains(filter_value))

            if order == 'asc':
                query = query.order_by(Posts.date_posted.asc())
            else:
                query = query.order_by(Posts.date_posted.desc())

    posts = query.all()
    return render_template('main/posts.html', form=form, posts=posts, search_query=search_query)


@main.route('/post/<int:post_id>/reply', methods=['GET', 'POST'])
@login_required
def reply(post_id):
    form = ReplyForm()
    post = Posts.query.get_or_404(post_id)

    if form.validate_on_submit():
        reply = Reply(
            post_id=post_id,
            author_id=current_user.id,
            answer=form.answer.data,
            answered_accepted=False,
            deleted=False
        )
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been added.', 'success')
        return redirect(url_for('main.view_post', post_id=post_id))

    return render_template('main/reply.html', title='Reply to Post', form=form, post=post)

@main.route("/search", methods=["GET"])
def search():
    query = request.args.get('q', '')
    search_results = []

    # Check if the query includes a tag (e.g., [tag] keyword)
    tag = None
    keyword = query
    if query.startswith('[') and ']' in query:
        tag_part = query.split(']')[0] + ']'
        keyword_part = query.split(']')[1].strip()

        # Extract tag name from brackets and trim whitespace
        tag_name = tag_part[1:-1].strip()
        tag = Tag.query.filter(Tag.tag.ilike(f'%{tag_name}%')).first()
        keyword = keyword_part

    if tag:
        # Search for posts by tag and keyword
        search_results = Posts.query.filter(
            Posts.tag_id == tag.id,
            (Posts.title.ilike(f'%{keyword}%')) | 
            (Posts.content.ilike(f'%{keyword}%'))
        ).all()
    else:
        # General search for titles and content
        search_results = Posts.query.filter(
            (Posts.title.ilike(f'%{query}%')) | 
            (Posts.content.ilike(f'%{query}%'))
        ).all()

    form = FilterSortForm()
    return render_template('main/posts.html', form=form, posts=search_results, search_query=query)


# Route to mark/unmark a post as favorite
@main.route('/favorite_post/<int:post_id>', methods=['POST'])
@login_required
def favorite_post(post_id):
    post = Posts.query.get_or_404(post_id)
    favorite = FavoritePost.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if favorite:
        # If the post is already a favorite, remove it
        db.session.delete(favorite)
        db.session.commit()
        flash('Post removed from favorites', 'info')
    else:
        # Add post to favorites
        new_favorite = FavoritePost(user_id=current_user.id, post_id=post_id)
        db.session.add(new_favorite)
        db.session.commit()
        flash('Post added to favorites', 'success')

    return redirect(url_for('main.view_post', post_id=post_id))

# Route to display the logged-in user's favorite posts
@main.route('/my_favorites')
@login_required
def my_favorites():
    favorite_posts = FavoritePost.query.filter_by(user_id=current_user.id).all()
    posts = [favorite.post for favorite in favorite_posts]
    return render_template('main/my_favorites.html', posts=posts)

# Route to display About Page
@main.route('/about')
def about():
    
    return render_template('main/about.html')

# Route to display My Answered Post
@main.route('/my_answers')
@login_required
def my_answers():
    form = FilterSortForm()
    posts_with_my_replies = (
        db.session.query(Posts)
        .join(Reply, Posts.id == Reply.post_id)
        .filter(Reply.author_id == current_user.id)
        .all()
    )
    return render_template('main/my_answers.html', posts=posts_with_my_replies, form=form)

# API Endpoint for My Answers
@main.route('/api/my_answers_posts', methods=['GET'])
@login_required
def api_my_answers_posts():
    order = request.args.get('order', 'asc')

    query = (
        db.session.query(Posts)
        .join(Reply, Posts.id == Reply.post_id)
        .filter(Reply.author_id == current_user.id)
    )

    if order == 'desc':
        query = query.order_by(Posts.date_posted.desc())
    else:
        query = query.order_by(Posts.date_posted.asc())

    posts = query.all()

    posts_data = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_first_name': post.author.first_name,
            'author_last_name': post.author.last_name,
            'tag': post.tag.tag,
            'date_posted': post.date_posted.strftime('%B %d, %Y'),
            'answered': post.answered,
            'career_preparation': post.career_preparation
        }
        posts_data.append(post_data)

    return jsonify(posts_data)

# Route for Tag
@main.route("/tags")
@login_required
def tags():
    tags_with_counts = db.session.query(
        Tag.id,
        Tag.tag,
        func.count(Posts.id).label('post_count')
    ).join(Posts, Posts.tag_id == Tag.id).group_by(Tag.id).all()

    return render_template("main/tags.html", tags=tags_with_counts)

@main.route("/tag/<int:tag_id>")
@login_required
def posts_by_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Posts.query.filter_by(tag_id=tag_id).all()
    return render_template("main/posts_by_tag.html", tag=tag, posts=posts)

@main.before_app_request
def add_tags_to_sidebar():
    if current_user.is_authenticated:
        tags_with_counts = db.session.query(
            Tag.id,
            Tag.tag,
            func.count(Posts.id).label('post_count')
        ).join(Posts, Posts.tag_id == Tag.id).group_by(Tag.id).all()
        g.tags = tags_with_counts
    else:
        g.tags = []

# Route for Career Preparation
@main.route("/career")
@login_required
def career():
    career_posts = Posts.query.filter_by(career_preparation=True).all()
    return render_template("main/career.html", posts=career_posts)

# Route for Unit Preparation
@main.route("/uni_preparation")
@login_required
def uni_preparation():
    uni_preparation_posts = Posts.query.filter_by(career_preparation=False).all()
    return render_template("main/uni_preparation.html", posts=uni_preparation_posts)