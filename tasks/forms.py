from django import forms
from django.db import transaction

from .models import Task

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    priority = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    completed = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-checkbox h-6 w-6 rounded text-red-500 border-0 bg-slate-100'}), required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'completed', 'user']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title.capitalize()

    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if priority < 0:
            raise forms.ValidationError("Priority must non-negative.")
        return priority

    @transaction.atomic
    def save(self, commit=True):
        task_obj = super().save(commit=False)
        this_priority = task_obj.priority
        tasks = []
        while Task.objects.filter(priority=this_priority, user=task_obj.user, completed=False).exclude(id=task_obj.id).exists():
            tasks.append(Task.objects.filter(priority=this_priority, user=task_obj.user, completed=False).exclude(id=task_obj.id).first())
            this_priority += 1
        tasks.reverse()
        for task in tasks:
            task.priority += 1
            task.save()
        return task_obj
