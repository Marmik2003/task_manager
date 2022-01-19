from django.shortcuts import render, redirect
from .models import Task

def index(request):
    return redirect('tasks:all_tasks')

def tasks(request):
    ctx = {'tasks': Task.objects.filter(deleted=False, completed=False),}
    return render(request, 'tasks/tasks.html', context=ctx)

def add_task(request):
    if 'task' in request.GET:
        task = request.GET['task']
        Task.objects.create(title=task)
        return redirect('tasks:tasks')
    return render(request, 'tasks/add_task.html')

def all_tasks(request):
    ctx = {'tasks': Task.objects.all(),}
    return render(request, 'tasks/all_tasks.html', context=ctx)

def complete_task(request, pk):
    Task.objects.filter(pk=pk).update(completed=True)
    return redirect('tasks:tasks')

def completed_tasks(request):
    ctx = {
        'completed_tasks': Task.objects.filter(completed=True),
    }
    return render(request, 'tasks/completed_tasks.html', context=ctx)

def delete_task(request, pk):
    Task.objects.filter(pk=pk).filter(deleted=True)
    return redirect('tasks:tasks')
