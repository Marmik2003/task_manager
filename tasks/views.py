from django.shortcuts import render, redirect

tasks_arr = []
completed_tasks_arr = []

def index(request):
    return redirect('tasks:all_tasks')

def tasks(request):
    ctx = {'tasks': tasks_arr}
    return render(request, 'tasks/tasks.html', context=ctx)

def add_task(request):
    if request.method == 'GET':
        tasks_arr.append(request.GET.get('task'))
        return redirect('tasks:tasks')
    return render(request, 'tasks/add_task.html')

def all_tasks(request):
    ctx = {'tasks': tasks_arr.extend(completed_tasks_arr),}
    return render(request, 'tasks/all_tasks.html', context=ctx)

def complete_task(request, pk):
    completed_tasks_arr.append(tasks_arr[pk])
    tasks_arr.pop(pk)
    return redirect('tasks:tasks')

def completed_tasks(request):
    ctx = {
        'completed_tasks': completed_tasks_arr,
    }
    return render(request, 'tasks/completed_tasks.html', context=ctx)

def delete_task(request, pk):
    tasks_arr.pop(pk)
    return redirect('tasks:tasks')
