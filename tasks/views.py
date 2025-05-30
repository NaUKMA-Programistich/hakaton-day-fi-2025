from django.shortcuts import render, redirect
from .models import Task
import json

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        test_cases = request.POST.get('test_cases')
        
        if title and description:
            try:
                # Validate JSON format
                test_cases_dict = json.loads(test_cases) if test_cases else {}
                Task.objects.create(
                    title=title,
                    description=description,
                    test_cases=test_cases_dict
                )
                return redirect('task_list')
            except json.JSONDecodeError:
                return render(request, 'tasks/add_task.html', {
                    'error': 'Invalid JSON format for test cases',
                    'title': title,
                    'description': description,
                    'test_cases': test_cases
                })
    return render(request, 'tasks/add_task.html')

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})
