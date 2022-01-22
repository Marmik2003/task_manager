from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views import generic

from .models import Task
from .forms import TaskForm


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'all_tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_completed'] = Task.objects.filter(completed=True, user=self.request.user, deleted=False).count()
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False).order_by('priority')


@method_decorator(login_required, name='dispatch')
class PendingTaskView(generic.ListView):
    template_name = 'tasks/pending_tasks.html'
    context_object_name = 'pending_tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_all'] = Task.objects.filter(deleted=False, user=self.request.user).count()
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=False, deleted=False).order_by('priority')


@method_decorator(login_required, name='dispatch')
class CompletedTaskView(generic.ListView):
    template_name = 'tasks/completed_tasks.html'
    context_object_name = 'completed_tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_all'] = Task.objects.filter(deleted=False, user=self.request.user).count()
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=True, deleted=False).order_by('priority')


@method_decorator(login_required, name='dispatch')
class AddTaskView(generic.CreateView):
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditTaskView(generic.UpdateView):
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)


@method_decorator(login_required, name='dispatch')
class DeleteTaskView(View):
    def get(self, request, id):
        Task.objects.filter(id=id).update(deleted=True)
        return redirect('/')
