from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton')
jane = User(first_name='Jane', last_name='Smith')

post1 = Post(title="How to catch fish",
             content="Here is how to catch a fish in 3 days", user_id=1)
post2 = Post(title="My first post!", content="Wow it's working", user_id=2)
post3 = Post(title="Nature's Great Events", content="A book at the library", user_id=3)
post4 = Post(title="Math Makers", content="Learning to do math", user_id=1)

tag1 = Tag(name="#selfie")
tag2 = Tag(name="#wow")
tag3 = Tag(name="#tgif")

post_tag1 = PostTag(post_id=1, tag_id=2)
post_tag2 = PostTag(post_id=1, tag_id=3)
post_tag3 = PostTag(post_id=2, tag_id=1)

db.session.add_all([alan,joel,jane])
db.session.add_all([post1,post2,post3,post4])
db.session.add_all([tag1,tag2,tag3])


db.session.commit()

db.session.add_all([post_tag1,post_tag2,post_tag3])
db.session.commit()
