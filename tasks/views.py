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
            # Get the solution file path
            solution_path = solution.code_file.path
            print(f"Solution path: {solution_path}")  # Debug info
            
            # Get test cases from the task
            test_cases = task.test_cases
            print(f"Test cases: {test_cases}")  # Debug info
            
            # Prepare inputs and expected outputs for run_tests
            inputs = []
            expected_outputs = []
            
            # Process test cases
            for test_case in test_cases:
                # Convert input to string format
                input_str = convert_to_string(test_case['input'])
                # Convert expected output to string format
                expected_str = convert_to_string(test_case['expected_output'])
                
                inputs.append(input_str)
                expected_outputs.append(expected_str)
            
            print(f"Processed inputs: {inputs}")  # Debug info
            print(f"Expected outputs: {expected_outputs}")  # Debug info
            
            # Run the tests using run_tests.py
            test_results = []
            all_passed = True
            
            try:
                # Execute tests
                results = run_tests(inputs, expected_outputs, [solution_path], timeout=5, strip=True)
                print(f"Raw test results: {results}")  # Debug info
                
                # Process results for each test case
                for i, result in enumerate(results[0]):
                    test_case = test_cases[i]
                    
                    if isinstance(result, dict):
                        # Get the actual output from the test result
                        actual_output = result.get('actual', '')
                        expected_output = test_case['expected_output']
                        
                        # Compare actual and expected outputs
                        is_passed = actual_output == convert_to_string(expected_output)
                        
                        test_result = {
                            'test_case': i + 1,
                            'input': test_case['input'],
                            'expected': expected_output,
                            'actual': actual_output,
                            'status': 'passed' if is_passed else 'failed'
                        }
                        
                        if not is_passed:
                            all_passed = False
                            
                        if 'error' in result:
                            test_result['error'] = result['error']
                            test_result['status'] = 'error'
                            all_passed = False
                            
                    else:
                        # Test failed with exception
                        all_passed = False
                        test_result = {
                            'test_case': i + 1,
                            'input': test_case['input'],
                            'expected': test_case['expected_output'],
                            'actual': str(result),
                            'status': 'error',
                            'error': str(result)
                        }
                    
                    test_results.append(test_result)
                    print(f"Test result {i+1}: {test_result}")  # Debug info
                
            except Exception as e:
                # Handle test execution errors
                error_message = f"Test execution error: {str(e)}"
                print(f"Test execution error: {error_message}")  # Debug info
                test_results = [{
                    'status': 'error',
                    'error': error_message
                }]
                all_passed = False
            
            # Update solution with results
            solution.status = 'passed' if all_passed else 'failed'
            solution.test_results = test_results
            solution.save()
            
        except Exception as e:
            # Handle file processing errors
            error_message = f"File processing error: {str(e)}"
            print(f"File processing error: {error_message}")  # Debug info
            solution.status = 'failed'
            solution.test_results = [{
                'status': 'error',
                'error': error_message
            }]
            solution.save()
        
        return redirect('task_detail', task_id=task_id)
    
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'solutions': solutions
    })

