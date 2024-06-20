import unittest
from datetime import datetime, timedelta
from flask import Flask, url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Schedule, UpcomingCollection
from app.forms import ScheduleForm, GenerateCollectionsForm


class TestUserRoutes(TestCase):

    def create_app(self):
        app = create_app("config.TestConfig")
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        # Create a test user
        user = User(
            names="John Doe",
            email="john.doe@example.com",
            password="password123",
            role="user",
            address="123 Main St",
        )
        db.session.add(user)
        db.session.commit()

        # Create a test schedule for the user
        schedule = Schedule(
            user_id=user.id, day_of_week="Monday"  # Choose a day for testing
        )
        db.session.add(schedule)
        db.session.commit()

    def login(self, email, password):
        return self.client.post(
            "/login", data=dict(email=email, password=password), follow_redirects=True
        )

    def test_schedule_route_get(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Access the schedule route
        response = self.client.get("/schedule")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Schedule Day", response.data)  # Check for expected content

    def test_schedule_route_post(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Prepare form data for POST request
        form_data = {"day_of_week": "Tuesday"}  # Choose a different day for testing

        # Send POST request to add a new schedule day
        response = self.client.post("/schedule", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Schedule day added successfully.", response.data
        )  # Check for success message

    def test_generate_collections_route_post(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Send POST request to generate collections
        response = self.client.post("/schedule/generate", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Upcoming collections generated successfully.", response.data
        )  # Check for success message

    def test_edit_schedule_route_get(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Access the edit schedule route for the existing schedule
        schedule_id = (
            Schedule.query.filter_by(user_id=1).first().id
        )  # Adjust the user_id as needed
        response = self.client.get(f"/schedule/{schedule_id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Schedule Day", response.data)  # Check for expected content

    def test_edit_schedule_route_post(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Access the schedule ID to edit
        schedule_id = (
            Schedule.query.filter_by(user_id=1).first().id
        )  # Adjust the user_id as needed

        # Prepare form data for POST request
        form_data = {"day_of_week": "Wednesday"}  # Choose a different day for testing

        # Send POST request to edit the schedule day
        response = self.client.post(
            f"/schedule/{schedule_id}/edit", data=form_data, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Schedule updated successfully.", response.data
        )  # Check for success message

    def test_delete_schedule_route_get(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Access the delete schedule route for the existing schedule
        schedule_id = (
            Schedule.query.filter_by(user_id=1).first().id
        )  # Adjust the user_id as needed
        response = self.client.get(f"/schedule/{schedule_id}/delete")
        self.assertEqual(response.status_code, 302)  # Expecting redirect after deletion

    def test_delete_collection_route_get(self):
        # Log in the user first
        self.login("john.doe@example.com", "password123")

        # Access the delete collection route for the existing collection
        collection_id = (
            UpcomingCollection.query.filter_by(user_id=1).first().id
        )  # Adjust the user_id as needed
        response = self.client.get(f"/collection/{collection_id}/delete")
        self.assertEqual(response.status_code, 302)  # Expecting redirect after deletion


if __name__ == "__main__":
    unittest.main()
