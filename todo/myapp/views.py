from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(expiration_date__gte=timezone.now().date())  # gte -> django greater than or equal stuff


class ExpiredTaskListView(ListView):
    model = TODOList
    ordering = ["expiration_date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter_type = self.request.GET.get("filter", "active")
        # if filter_type == "expired":
        #     return queryset.filter(expiration_date__lt=timezone.now().date())
        return queryset.filter(expiration_date__lt=timezone.now().date())  # gte -> django less or equal stuff




class TaskCreateView(CreateView):
    model = TODOList
    form_class = TaskCreateForm

    def form_valid(self, form):
        self.object = form.save()

        if self.request.htmx:
            return render(self.request, "myapp/task_partial.html", context={"obj": self.object})
        else:
            return redirect(self.object.get_absolute_url())


class TaskUpdateView(UpdateView):
    model = TODOList
    form_class = TaskUpdateForm
    template_name = "myapp/todolist_update_custom.html"


class TaskDeleteView(DeleteView):
    model = TODOList
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('')


def task_search(request):
    search_query = request.POST.get("search")  # get value from html's name=search input
    results = TODOList.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    if not search_query:
        return HttpResponse("")
    return render(request, "myapp/search_results.html", {"object_list": results})

