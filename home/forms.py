from django.forms.widgets import DateTimeInput


class CustomDateTimeWidget(DateTimeInput):
    template_name = 'home/datetimeWidget.html'
