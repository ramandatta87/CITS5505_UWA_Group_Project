from flask import Blueprint, render_template, session, flash, redirect, url_for, request, Response, jsonify
from flask_mail import Message
from app import mail, db
import datetime
from flask_login import current_user, login_required
from app.forms import PostForm, FilterSortForm, ReplyForm
from app.models.model import Posts, Tag, User, Reply

# Define a Blueprint named 'main' for organizing routes and views
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    login_status = session.get('logged_in', False)
    return render_template("index.html", login=login_status)

@main.route("/forum")
def forum():
    return render_template("forum.html")

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

        post = Posts(
            title=form.title.data,
            content=form.content.data,
            tag_id=tag.id,
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
    results = [result[0] for result in results]
    return Response(json.dumps(results), mimetype='application/json')

@main.route('/api/posts')
def api_posts():
    order = request.args.get('order', 'asc')
    filter_by = request.args.get('filter_by', 'author')
    filter_value = request.args.get('filter_value', '')

    query = Posts.query.join(User, Posts.author_id == User.id).join(Tag, Posts.tag_id == Tag.id)

    if filter_by and filter_value:
        if filter_by == 'author':
            query = query.filter((User.first_name.ilike(f'%{filter_value}%')) | (User.last_name.ilike(f'%{filter_value}%')))
        elif filter_by == 'title':
            query = query.filter(Posts.title.ilike(f'%{filter_value}%'))
        elif filter_by == 'tag':
            query = query.filter(Tag.tag.ilike(f'%{filter_value}%'))

    if order == 'desc':
        query = query.order_by(Posts.date_posted.desc())
    else:
        query = query.order_by(Posts.date_posted.asc())

    posts = query.all()

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

@main.route('/posts', methods=['GET', 'POST'])
def posts():
    form = FilterSortForm()
    query = Posts.query

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
    return render_template('main/posts.html', form=form, posts=posts)

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
