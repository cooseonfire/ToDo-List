from django.urls import path

from . import views

app_name = 'todolist'
urlpatterns = [
    path('new/', views.new_list_view, name='new_list'),
    path('edit/<int:todolist_id>/', views.edit_list_view, name='edit_list'),
    path('delete/<int:todolist_id>/', views.delete_list_view, name='delete_list'),
    path('new/<int:todolist_id>/', views.new_task_view, name='new_task'),
    path('edit/<int:todolist_id>/<int:todo_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:todolist_id>/<int:todo_id>/', views.delete_task_view, name='delete_task'),
    path('done/<int:todolist_id>/<int:todo_id>/', views.done_task_view, name='done_task'),
    path('overview/<int:todolist_id>/', views.overview_view, name='overview'),
]