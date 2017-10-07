from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, UserManager

class UserCreationForm(forms.ModelForm):
    pass