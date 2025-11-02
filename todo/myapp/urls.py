from django.contrib import admin
from django.urls import path
import myapp.views as app_views

urlpatterns = [
    path("", app_views.TaskListView.as_view(), name="home"),
    path("task/create/", app_views.TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", app_views.TaskDetailView.as_view(), name="task-view"),
    path("task/<int:pk>/update", app_views.TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete", app_views.TaskDeleteView.as_view(), name="task-delete"),
    path("task/search", app_views.task_search, name="task-search"),
    path("tasks/expired", app_views.ExpiredTaskListView.as_view(), name="tasks-expired")
]
