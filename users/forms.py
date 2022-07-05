from datetime import datetime

from allauth.account.forms import SignupForm
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class CustomSignupForm(SignupForm):
    """
    Adapt default signup form from All-AUTH to add custom fields
    """
    field_order = [
        "email",
        "password1",
        "password2",
        "name",
        "date_of_birth",
        "gender",
        "phone_number",
    ]
    name = forms.CharField(
        label=_("Name"),
        min_length=1,
        widget=forms.TextInput(
            attrs={"placeholder": _("Name"), "autocomplete": "name"}
        ),
    )

    BIRTH_YEAR_CHOICES = range(timezone.now().year - 4, 1914, -1)
    date_of_birth = forms.DateField(
        label=_("Date of birth"),
        widget=forms.SelectDateWidget(
            years=BIRTH_YEAR_CHOICES,
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),

    )

    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=(("f", "Female"), ("m", "Male"), ("o", "Other"))
    )

    phone_number = forms.CharField(
        label=_("Phone Number"),
        min_length=9,
        widget=forms.TextInput(
            attrs={"placeholder": _("Phone number")}
        ),
    )

    def save(self, request):
        """ Override save to save new fields added"""
        user = super(CustomSignupForm, self).save(request)

        # Handle saving of profile to model UserProfile
        if request.method == "POST":
            post = request.POST

            profile = UserProfile()
            profile.user = user
            profile.name = post.get("name")
            profile.date_of_birth = datetime(
                int(post.get("date_of_birth_year")),
                int(post.get("date_of_birth_month")),
                int(post.get("date_of_birth_day")),
            )
            profile.gender = post.get("gender")
            profile.phone_number = int(post.get("phone_number"))
            profile.save()

        return user
