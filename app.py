"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
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


@app.route("/users/<int:user_id>/posts/new")
def post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template("add_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds user's post and redirects to user detail page"""
    user = User.query.get_or_404(user_id)
    post = Post(title=request.form['title'], content=request.form['content'],user=user)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

#### POST ROUTES ####

@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    """Show a post, show buttons to edit & delete post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)    

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show form to edit a post and to cancel(back to user page)"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)   

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post, redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

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
