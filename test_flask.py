from unittest import TestCase
from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserRoutesTestCase(TestCase):
    """Tests routes for User"""

    def setUp(self):
        """Add a sample user"""
        db.drop_all()
        db.create_all()
        User.query.delete()
        
        user = User(first_name="Testy", last_name="Jones", image_url="https://mymodernmet.com/wp/wp-content/uploads/2017/10/highland-cattle-calves-6.jpg")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Test", content="Testing", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        self.post_id = post.id
        self.post = post
    
    def tearDown(self):
        """clean up any fouled transacations"""
        db.session.rollback()

    def test_show_users(self):
        """/users route - tests that user is added to page"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<a href="/users/1">Testy Jones</a>',html)

    def test_show_form(self):
        """GET /users/new route - tests form page displays"""
        with app.test_client() as client:
            resp = client.get("/users/new")

            self.assertEqual(resp.status_code,200)

    def test_user_form(self):
        """POST /users/new route - tests that adding a new user adds to db & /users page """
        with app.test_client() as client:
            d = {"first_name": "TestGuy", "last_name":"Jones III", "image_url": "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg?v=3"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<a href="/users/2">TestGuy Jones III</a>', html)

    def test_delete_user(self):
        """ /users/<int:user_id>/delete route - tests that deleting a user removes them from db & /users page"""
        with app.test_client() as client:
            
            resp = client.post("/users/1/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<a href="/users/1">Testy Jones</a>',html)
        
    def test_show_post(self):
        """ /posts/<int:post_id> route - test that post info page loads"""
        with app.test_client() as client:
            resp = client.get("/posts/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test</h1>', html)

    def test_edit_post_form(self):
        """ GET /posts/<int:post_id>/edit route- tests form page to edit post"""
        with app.test_client() as client:
            resp = client.get("/posts/1/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="title">Title: </label>', html)

    def test_edit_post(self):
        """ POST /posts/<int:post_id>/edit route- tests editing a post"""
        with app.test_client() as client:
            d = {"title":"Test2","content":"Testing2","user_id":1}
            resp = client.post("/posts/1/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Test2</h1>', html)

    def test_delete_post(self):
        """POST /posts/<int:post_id>/delete route - tests deleting a post"""
        with app.test_client() as client:
            resp = client.post("/posts/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('<h1>Test</h1>',html)                

    
