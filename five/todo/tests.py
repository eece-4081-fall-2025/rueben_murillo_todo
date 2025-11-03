# tests.py - YOUR TEST WITH AUTH ADDED
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ToDo

class ToDoCreationTest(TestCase):
    """
    Given a valid task title, description, and due date,
    When the user submits the create task form
    THEN a new Task should be saved in the database
    AND the user should be redirected to the task list
    """
    
    def setUp(self):
        """Create and login a test user"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_new_todo(self):
        data = {
            "name": "Write unit tests",
            "description": "Add tests for the create_todo view",
            "due_date": "2024-12-31",
            "completed": False
        }
       
        response = self.client.post(reverse("todo_create"), data)
       
        todo = ToDo.objects.first()
        self.assertEqual(response.status_code, 302)  # Redirect to task list
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(ToDo.objects.count(), 1)
        self.assertEqual(todo.name, "Write unit tests")
        self.assertFalse(todo.completed)
        self.assertEqual(str(todo.due_date), "2024-12-31")