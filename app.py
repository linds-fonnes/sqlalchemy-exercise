"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import update

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'SecretSecretSecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home_page():
    """redirects to /users"""
    return redirect("/users")

#### USER ROUTES ####

@app.route("/users")
def list_users():
    """List current users and show add user button"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def show_form():
    """Shows form to add a new user"""
    return render_template("user_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds user information to db and to home page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("show_user.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    """Displays page to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edits user info"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user from db and home page"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#### POST ROUTES ####

@app.route("/users/<int:user_id>/posts/new")
def post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("add_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds user's post and redirects to user detail page"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=request.form['title'], content=request.form['content'],user=user,tags=tags)

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    """Show a post, show buttons to edit & delete post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)    

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show form to edit a post and to cancel(back to user page)"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)   

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post, redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    user = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user}")

#### Tag Routes ####

@app.route("/tags")
def show_all_tags():
    """Lists all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about a tag. Have links to edit form and to delete"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)

@app.route("/tags/new")
def new_tag_form():
    """Show a form to add a new tag"""
    return render_template("tag_form.html")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Process form, adds tag, and redirect to tag list"""
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show edit  form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)  

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")