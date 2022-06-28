from django import forms
from .models import Activity
from home.forms import CustomDateTimeWidget

class ActivityForm(forms.ModelForm):
    time_of_event = forms.DateTimeField(widget=CustomDateTimeWidget, label='')

    class Meta:
        model = Activity
        fields = [
            'time_of_event', 'title', 'description', 'location', 'category', 'waiting_list_enabled'
        ]
