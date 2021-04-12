from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton')
jane = User(first_name='Jane', last_name='Smith')

post1 = Post(title="How to catch fish",
             content="here is how to catch a fish in 3 days", user_id=1)
post2 = Post(title="My first post!", content="Wow it's working", user_id=2)
post3 = Post(title="Nature's Great Events", content="A book at the library", user_id=3)
post4 = Post(title="Math Makers", content="Learning to do math", user_id=1)

db.session.add(alan)
db.session.add(joel)
db.session.add(jane)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

db.session.commit()
