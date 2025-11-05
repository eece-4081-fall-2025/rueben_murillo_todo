from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('<int:pk>/toggle/', views.todo_toggle_complete, name='todo_toggle_complete'),
]