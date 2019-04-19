from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    title = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def count_finished(self):
        return self.todos.filter(is_finished=True).count()


class Task(models.Model):
    description = models.CharField(max_length=500)
    todo_date = models.DateTimeField(default=timezone.now().strftime("%d-%m-%Y"))
    priority = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default='General',
                                 on_delete=models.CASCADE)
    todo_list = models.ForeignKey(ToDoList, related_name='todos',
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority', '-todo_date']
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.description




