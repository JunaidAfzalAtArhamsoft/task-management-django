from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Person(User):
    gender_choice = [('M', 'Male'),
                     ('F', 'Female'),
                     ]
    gender = models.CharField(verbose_name='Gender', max_length=6, choices=gender_choice, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password1', 'password2']

    def __str__(self):
        """
        Message: Show person name as default
        Parameters:
            self:
        Returns:
            name (str): Return person name
                """
        return '{} {}'.format(self.first_name.title(), self.last_name.title())


class TaskList(models.Model):
    task_list_title = models.CharField(max_length=50, blank=False)
    task_list_description = models.TextField()
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        """
        Message: Show task_list title as default
        Parameters:
            self:
        Returns:
            task__list_title (str): Return task_list title
        """
        return self.task_list_title


class Task(models.Model):
    task_title = models.CharField(max_length=100, blank=False)
    task_description = models.TextField()
    start_date = models.DateTimeField(default=datetime.now())
    completed_date = models.DateTimeField(blank=True, null=True, default=None)
    is_complete = models.BooleanField(default=False)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)

    def __str__(self):
        """
        Message: Show task title as default
        Parameters:
            self:
        Returns:
            task_title (str): Return task title
        """
        return self.task_title
