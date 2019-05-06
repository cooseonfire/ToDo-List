from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse
import datetime

from .models import TodoList, Task
from .forms import TodolistForm, TodoForm

from .predictive_model.log_regression_model import *


def overview_view(request, todolist_id):
    todolist = request.user.todolists.get(id=todolist_id)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'todolist/list_overview.html', {"todolist": todolist})

def new_list_view(request):
    # if not request.user.is_authenticated():
    #     redirect('404')
    if request.method == 'POST':
        user = request.user
        todolist = TodoList(title=request.POST['title'], creator=user)
        todolist.save()
        return redirect('todolist:overview', todolist_id=todolist.id)

    else:
        return render(request, 'todolist/new_list.html', {"form": TodolistForm()})


def edit_list_view(request, todolist_id):
    try:
        todolist = request.user.todolists.get(id=todolist_id)
        if request.method == 'POST':
            todolist.title = request.POST["title"]
            todolist.save()
            return redirect('todolist:overview', todolist_id=todolist.id)
        else:
            form = TodolistForm()
            form.fields["title"].initial = todolist.title
            return render(request, 'todolist/edit_list.html',
                          {"form": form})
    except TodoList.DoesNotExist:
        return HttpResponseNotFound("<h2>List not found</h2>")


def delete_list_view(request, todolist_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todolist.delete()
    return redirect('home')


def new_task_view(request, todolist_id):
    if request.method == 'POST':
        todo = Task(
            name=request.POST['name'],
            description=request.POST['description'],
            priority=request.POST['priority'],
            deadline=request.POST.get('deadline') or None,
            todo_list=request.user.todolists.get(id=todolist_id)
        )
        todo.save()
        return redirect('todolist:overview', todolist_id=todolist_id)

    else:
        return render(request, 'todolist/new_task.html', {"form": TodoForm()})


def edit_task_view(request, todolist_id, todo_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todo = todolist.todos.get(id=todo_id)
    if request.method == 'POST':
        todo.name = request.POST["name"]
        todo.description = request.POST["description"]
        todo.priority = request.POST["priority"]
        todo.deadline = request.POST.get('deadline') or None
        todo.save()
        return redirect('todolist:overview', todolist_id=todolist.id)
    else:
        form = TodoForm()
        form.fields["name"].initial = todo.name
        form.fields["description"].initial = todo.description
        form.fields["priority"].initial = todo.priority
        form.fields["deadline"].initial = todo.deadline
        return render(request, 'todolist/edit_list.html',
                      {"form": form})


def delete_task_view(request, todolist_id, todo_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todo = todolist.todos.get(id=todo_id)
    todo.delete()
    return redirect('todolist:overview', todolist_id=todolist_id)


def done_task_view(request, todolist_id, todo_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todo = todolist.todos.get(id=todo_id)
    todo.is_finished = True
    todo.finished_date = datetime.date.today()
    todo.save()
    return redirect('todolist:overview', todolist_id=todolist_id)


def prediction_view(request):
    task_success = list(filter(lambda x: x == 1, predict(request.user)))
    return render(request, 'todolist/prediction.html',
                  {"count": len(task_success)})


def train_view(request):
    acc = train(request.user)[0]
    return render(request, 'todolist/train.html', {"accuracy": acc})

