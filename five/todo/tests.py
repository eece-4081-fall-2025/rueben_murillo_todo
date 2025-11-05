# tests.py - YOUR TEST WITH AUTH ADDED
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ToDo

class ToDoCreationTest(TestCase):
    def setUp(self):
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
        self.assertEqual(todo.due_date.isoformat(), "2024-12-31")
        
    

# Additional CRUD tests
class ToDoEditTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edituser', password='testpass123')
        self.client.login(username='edituser', password='testpass123')
        self.todo = ToDo.objects.create(user=self.user, name='Old name', description='Old desc', completed=False)

    def test_edit_todo(self):
        data = {
            'name': 'Updated name',
            'description': 'Updated description',
            'due_date': '2024-12-31',
            'completed': True
        }
        response = self.client.post(reverse('todo_edit', args=[self.todo.id]), data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, 'Updated name')
        self.assertTrue(self.todo.completed)


class ToDoDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='deleteuser', password='testpass123')
        self.client.login(username='deleteuser', password='testpass123')
        self.todo = ToDo.objects.create(user=self.user, name='Delete me', description='Test delete')

    def test_delete_todo(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDo.objects.count(), 0)


class ToDoToggleCompleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='toggleuser', password='testpass123')
        self.client.login(username='toggleuser', password='testpass123')
        self.todo = ToDo.objects.create(user=self.user, name='Toggle test', completed=False)

    def test_toggle_complete(self):
        response = self.client.get(reverse('todo_toggle_complete', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)