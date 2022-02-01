from django import forms
from django.db import transaction

from .models import Task, STATUS_CHOICES

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    priority = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'
            },
        ),
        choices=STATUS_CHOICES
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'user']

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
