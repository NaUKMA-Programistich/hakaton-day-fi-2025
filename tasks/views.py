from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Solution
import json
import os
import sys
import traceback
from pathlib import Path
from run_tests.run_tests import run_tests
from parser.parser import Task as ParserTask

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

def convert_to_string(value):
    """Convert any value to a string representation."""
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value)
    return str(value)

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    solutions = task.solutions.all().order_by('-submitted_at')
    
    if request.method == 'POST' and 'code_file' in request.FILES:
        solution = Solution.objects.create(
            task=task,
            code_file=request.FILES['code_file']
        )
        
        try:
            # Save the uploaded file to a temporary location
            solution_path = solution.code_file.path
            print(f"Solution path: {solution_path}")  # Debug info
            
            # Prepare test cases
            test_cases = task.test_cases
            print(f"Test cases type: {type(test_cases)}")  # Debug info
            print(f"Test cases content: {test_cases}")  # Debug info
            
            inputs = []
            outputs = []
            
            # Handle both list and dict formats of test cases
            if isinstance(test_cases, dict):
                for input_str, output_str in test_cases.items():
                    inputs.append(convert_to_string(input_str))
                    outputs.append(convert_to_string(output_str))
            elif isinstance(test_cases, list):
                for test_case in test_cases:
                    if isinstance(test_case, dict):
                        inputs.append(convert_to_string(test_case.get('input', '')))
                        outputs.append(convert_to_string(test_case.get('output', '')))
                    elif isinstance(test_case, (list, tuple)) and len(test_case) >= 2:
                        inputs.append(convert_to_string(test_case[0]))
                        outputs.append(convert_to_string(test_case[1]))
            
            print(f"Processed inputs: {inputs}")  # Debug info
            print(f"Processed outputs: {outputs}")  # Debug info
            
            # Run the tests
            results = run_tests(inputs, outputs, [solution_path], timeout=5, strip=True)
            print(f"Test results: {results}")  # Debug info
            
            # Process results
            test_results = []
            all_passed = True
            
            for i, result in enumerate(results[0]):
                if result is True:
                    test_results.append({
                        'test_case': i + 1,
                        'status': 'passed',
                        'input': inputs[i],
                        'expected': outputs[i],
                        'actual': outputs[i]
                    })
                elif isinstance(result, dict):
                    all_passed = False
                    test_results.append({
                        'test_case': i + 1,
                        'status': 'failed',
                        'input': inputs[i],
                        'expected': result.get('expected', ''),
                        'actual': result.get('actual', '')
                    })
                else:
                    all_passed = False
                    test_results.append({
                        'test_case': i + 1,
                        'status': 'failed',
                        'input': inputs[i],
                        'expected': outputs[i],
                        'actual': str(result)
                    })
            
            # Update solution status and results
            solution.status = 'passed' if all_passed else 'failed'
            solution.test_results = test_results
            solution.save()
            
        except Exception as e:
            print(f"Error type: {type(e)}")  # Debug info
            print(f"Error message: {str(e)}")  # Debug info
            print(f"Traceback: {traceback.format_exc()}")  # Debug info
            
            solution.status = 'failed'
            error_message = f"{type(e).__name__}: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            solution.test_results = [{
                'error': error_message,
                'status': 'error'
            }]
            solution.save()
        
        return redirect('task_detail', task_id=task_id)
    
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'solutions': solutions
    })
