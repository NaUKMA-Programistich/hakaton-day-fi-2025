from django.db import models
import json

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    test_cases = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_test_cases(self):
        return json.loads(self.test_cases) if isinstance(self.test_cases, str) else self.test_cases

class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solutions')
    code_file = models.FileField(upload_to='solutions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', 
                            choices=[('pending', 'Pending'), 
                                   ('running', 'Running'),
                                   ('passed', 'Passed'),
                                   ('failed', 'Failed')])
    test_results = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"Solution for {self.task.title} - {self.submitted_at}"
