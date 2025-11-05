from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import ToDo

class ToDoTests(TestCase):
    def setUp(self):
        """Create and login a test user"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_new_todo(self):
        """User can create a new todo item"""
        data = {
            "name": "Write unit tests",
            "description": "Add tests for new features",
            "due_date": "2025-12-31",
            "completed": False
        }
        response = self.client.post(reverse("todo_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("todo_list"))

        todo = ToDo.objects.get(name="Write unit tests")
        self.assertEqual(todo.description, "Add tests for new features")
        self.assertFalse(todo.completed)
        self.assertEqual(str(todo.due_date), "2025-12-31")

    def test_edit_existing_todo(self):
        """User can edit an existing task"""
        todo = ToDo.objects.create(
            user=self.user,
            name="Old Name",
            description="Old desc",
            due_date="2025-11-30"
        )
        edit_data = {
            "name": "Updated Name",
            "description": "New desc",
            "due_date": "2025-12-15",
            "completed": False
        }
        response = self.client.post(
            reverse("todo_edit", args=[todo.pk]),
            edit_data
        )
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.name, "Updated Name")
        self.assertEqual(str(todo.due_date), "2025-12-15")

    def test_delete_todo(self):
        """User can delete an existing task"""
        todo = ToDo.objects.create(user=self.user, name="To Delete")
        response = self.client.post(reverse("todo_delete", args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDo.objects.count(), 0)

    def test_mark_complete_and_incomplete(self):
        """Check mark_complete and mark_incomplete methods"""
        todo = ToDo.objects.create(user=self.user, name="Toggle Test")
        todo.mark_complete()
        self.assertTrue(todo.completed)

        todo.mark_incomplete()
        self.assertFalse(todo.completed)

    def test_overdue_property(self):
        """Verify overdue logic for past due tasks"""
        past_date = timezone.now().date() - timedelta(days=3)
        todo = ToDo.objects.create(
            user=self.user,
            name="Overdue Task",
            due_date=past_date,
            completed=False
        )
        self.assertTrue(todo.is_overdue)

    def test_due_date_not_overdue_if_completed(self):
        """Completed tasks should never be flagged overdue"""
        past_date = timezone.now().date() - timedelta(days=5)
        todo = ToDo.objects.create(
            user=self.user,
            name="Done Task",
            due_date=past_date,
            completed=True
        )
        self.assertFalse(todo.is_overdue)

    def test_due_date_validation_in_form(self):
        """Ensure form rejects invalid date format"""
        invalid_data = {
            "name": "Invalid Date",
            "due_date": "31-12-2025",  # wrong format
        }
        response = self.client.post(reverse("todo_create"), invalid_data)
        self.assertEqual(response.status_code, 200)  # stays on same page
        self.assertContains(response, "Enter a valid date")