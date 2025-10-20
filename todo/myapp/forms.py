from django import forms

import datetime

from .models import TODOList


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = TODOList
        fields = ["title", "description", "expiration_date"]

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data["expiration_date"]
        if expiration_date < datetime.datetime.now().date():
            raise forms.ValidationError("Can't set a date that's not in the future)")
        return expiration_date


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TODOList
        fields = ["description", "expiration_date"]


