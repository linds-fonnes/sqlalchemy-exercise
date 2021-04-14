"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    "User"
    __tablename__ = "users"

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default="http://www.advancedsec.com/wp-content/uploads/2018/11/profile-blank.png")

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    def __repr__(self):
        """Show info about the post"""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Tag(db.Model):
    """Tag"""
    __tablename__ = "tags"

    def __repr__(self):
        """Show info about the tag"""
        t = self
        return f"<Tag {t.id} {t.name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25),nullable=False, unique=True)

    posts = db.relationship("Post", secondary="post_tags", cascade="all, delete", backref="tags")

class PostTag(db.Model):
    """Joins Post togrther with a Tag"""
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    