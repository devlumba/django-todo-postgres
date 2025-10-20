from django.shortcuts import render
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy, reverse


from .models import TODOList
from .forms import TaskCreateForm, TaskUpdateForm


# def home(request):  # no longer used
#     return render(request, "myapp/home.html")
#

class TaskDetailView(DetailView):
    model = TODOList


class TaskListView(ListView):
    model = TODOList
    ordering = ["expiration_date"]


class TaskCreateView(CreateView):
    model = TODOList
    form_class = TaskCreateForm


class TaskUpdateView(UpdateView):
    model = TODOList
    form_class = TaskUpdateForm


class TaskDeleteView(DeleteView):
    model = TODOList
    success_url = reverse_lazy("home")


