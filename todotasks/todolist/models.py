from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TodoList(models.Model):
    title = models.CharField(max_length=150)
    creator = models.ForeignKey(User, related_name='todolists', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def count_finished(self):
        return self.todos.filter(is_finished=True).count()


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True)
    priority = models.IntegerField(null=True)
    created_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    finished_date = models.DateField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, related_name='todos',
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority', '-deadline']

    def __str__(self):
        return self.name

    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()




