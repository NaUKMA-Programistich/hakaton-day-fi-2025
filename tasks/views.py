from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Solution
import json

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        test_cases = request.POST.get('test_cases')
        
        # Handle file upload
        if 'test_cases_file' in request.FILES:
            try:
                file_content = request.FILES['test_cases_file'].read().decode('utf-8')
                test_cases = file_content
            except Exception as e:
                return render(request, 'tasks/add_task.html', {
                    'error': f'Error reading file: {str(e)}',
                    'title': title,
                    'description': description,
                    'test_cases': test_cases
                })
        
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
    task = get_object_or_404(Task, id=task_id)
    solutions = task.solutions.all().order_by('-submitted_at')
    
    if request.method == 'POST' and 'code_file' in request.FILES:
        solution = Solution.objects.create(
            task=task,
            code_file=request.FILES['code_file']
        )
        # Here you would integrate with your existing code checking system
        # For now, we'll just set it as pending
        solution.status = 'pending'
        solution.save()
        return redirect('task_detail', task_id=task_id)
    
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'solutions': solutions
    })
