import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        # retrieve hompepage to ("/") perform tests on it 
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellows</title>" in html
      
        # Tests I added: check that Chizaram and Jiya's profile pictures are present
        assert '<img src="./static/img/jiya/headshot.jpg" alt="A picture of Jiya\'s face">' in html
        assert '<img id="chizy-profile-picture" src="./static/img/chizy/chizy.jpg" alt="A picture of Chizy\'s face">' in html


    def test_timeline(self):
        # retrieve timeline page to perform tests on it
        response = self.client.get("/api/timeline_post")
        # 200 represents success
        assert response.status_code == 200
        assert response.is_json
        # convert timeline page into JSON format
        json = response.get_json()
        assert "timeline_posts" in json

        # Tests I added: create a new POST request and check if it can be retrieved via a GET request
        # Create a JSON POST request 
        response_post = self.client.post("/api/timeline_post", data={'name': 'Jane Doe', 'email': 'jane@example.com', 'content':'Testing 2'})
        assert response_post.status_code == 200
        # GET request
        response_get = self.client.get("/api/timeline_post")
        assert response_get.status_code == 200
        # convert response to JSON
        json = response_get.get_json()
        # verify the content the GET request yielded (Note b: byte like object)
        assert b"Testing 2" in response_get.data

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Testing 1"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content" :""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "invalid-email", "content": "Testing 1"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

