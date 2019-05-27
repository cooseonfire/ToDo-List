from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import TodoList, Task
from .forms import TodolistForm, TodoForm

from .predictive_model.log_regression_model import *


@login_required(redirect_field_name='home')
def overview_view(request, todolist_id):
    todolist = request.user.todolists.get(id=todolist_id)
    return render(request, 'todolist/list_overview.html', {"todolist": todolist})


@login_required(redirect_field_name='home')
def new_list_view(request):
    if request.method == 'POST':
        user = request.user
        todolist = TodoList(title=request.POST['title'], creator=user)
        todolist.save()
        return redirect('todolist:overview', todolist_id=todolist.id)

    else:
        return render(request, 'todolist/new_list.html', {"form": TodolistForm()})


@login_required(redirect_field_name='home')
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
        return redirect('404')


@login_required(redirect_field_name='home')
def delete_list_view(request, todolist_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todolist.delete()
    return redirect('home')


@login_required(redirect_field_name='home')
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


@login_required(redirect_field_name='home')
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
        return render(request, 'todolist/edit_task.html',
                      {"form": form})


@login_required(redirect_field_name='home')
def delete_task_view(request, todolist_id, todo_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todo = todolist.todos.get(id=todo_id)
    todo.delete()
    return redirect('todolist:overview', todolist_id=todolist_id)


@login_required(redirect_field_name='home')
def done_task_view(request, todolist_id, todo_id):
    todolist = request.user.todolists.get(id=todolist_id)
    todo = todolist.todos.get(id=todo_id)
    todo.is_finished = True
    todo.finished_date = datetime.date.today()
    todo.save()
    return redirect('todolist:overview', todolist_id=todolist_id)


@login_required(redirect_field_name='home')
def prediction_view(request):
    try:
        task_success = list(filter(lambda x: x == 1, predict(request.user)))
    # for case when there's no enough tasks for training
    except:
        task_success = []
    # chart
    last_week = [datetime.date.today() - datetime.timedelta(days=i)
                 for i in reversed(range(7))]
    count_tasks = []
    for i, day in enumerate(last_week):
        count_tasks.append(0)
        for todolist in request.user.todolists.all():
            count_tasks[i] += todolist.todos.filter(finished_date=day).count()

    format_week = [i.strftime('%d.%m') for i in last_week]

    return render(request, 'todolist/prediction.html',
                  {"count": len(task_success), "labels": format_week,
                   "dataset": count_tasks})


@login_required(redirect_field_name='home')
def train_view(request):
    acc = train(request.user)
    return render(request, 'todolist/train.html', {"accuracy": acc})

