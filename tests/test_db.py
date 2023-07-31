# file will be used to test the database connection and any interactions with a database thorugh the peewee library
import unittest
from peewee import *

from app import TimelinePost

# creating a table?
MODELS = [TimelinePost]

# use an in-memory SQLite (portable database) for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)


        test_db.connect()
        test_db.create_tables(MODELS)
    
    def tearDown(self):
        test_db.drop_tables(MODELS)
        # close connection to database
        test_db.close()

    def test_timeline_post(self):
        # create two timeline posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Testing 1')
        # ensure it's the first post (id 1)
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Testing 2')
        assert second_post.id == 2

        # issue a GET request for the first two posts and confirm they're correct 
        get_first_post = TimelinePost.get_by_id(1).id
        assert get_first_post == 1

        get_second_post = TimelinePost.get_by_id(2).id
        assert get_second_post == 2


        

