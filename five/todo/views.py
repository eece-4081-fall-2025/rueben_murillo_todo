# views.py - UPDATE function names
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, ToDo
from .forms import ToDoForm, ProjectForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('todo_list')
        else:
            context['error'] = 'Invalid username or password.'
    
    return render(request, 'todo/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            context['error'] = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            context['error'] = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password)
            auth_login(request, user)
            return redirect('todo_list')
    
    return render(request, 'todo/register.html', context)

@login_required
def todo_list(request):  
    todos = ToDo.objects.filter(user=request.user).order_by('priority', 'due_date')
    projects = Project.objects.filter(user=request.user)
    
    query = request.GET.get('q')
    project_filter = request.GET.get('project')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    
    if query:
        todos= todos.filter(name__icontains=query)
    if project_filter:
        todos = todos.filter(project__id=project_filter)
    if priority: 
        todos = todos.filter(priority=priority)
    if status == 'completed':
        todos = todos.filter(completed = True)
    elif status == 'incomplete':
        todos = todos.filter(completed = False)
    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'projects': projects,
        'query': query,
        'project_filter': project_filter,
        'priority': priority,
        'status': status,
    })

@login_required
def reorder_todos(request):
    if request.method == 'POST':
        order = request.POST.getlist('order[]')
        for idx, todo_id in enumerate(order):
            ToDo.objects.filter(id=todo_id, user=request.user).update(priority=idx)
        return JsonResponse({'success': True})
    return JsonResponse({'error' : 'Invalid request'}, status=400)
    
@login_required
def todo_create(request): 
    project_id = request.GET.get('project')  
    project= None
    if project_id:
        project=get_object_or_404(Project, id=project_id, user=request.user)
        
    if request.method == 'POST':
        form = ToDoForm(request.POST, user= request.user)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task created successfully!')
            return redirect('todo_list')
        else:
            print(form.errors)
    else:
        form = ToDoForm(user= request.user, initial={'project': project})
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def todo_edit(request, pk):  # Renamed from todo_edit
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo_list')
    else:
        form = ToDoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'todo': todo,
        'action': 'Edit'
    })

@login_required
def todo_delete(request, pk):  # Renamed from todo_delete
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@login_required
def todo_toggle_complete(request, pk):  # Renamed from todo_toggle_complete
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if todo.completed:
        todo.mark_incomplete()
        status = 'incomplete'
    else:
        todo.mark_complete()
        status = 'complete'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': status,
            'completed': todo.completed
        })

    messages.success(request, f'Todo marked as {status}!')
    return redirect('todo_list')

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'todo/project_list.html', {
        'projects': projects,})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'todo/project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, f"Project '{project.name}' deleted successfully!")
        return redirect('project_list')
    
    return render(request, 'todo/project_confirm_delete.html', {'project': project})