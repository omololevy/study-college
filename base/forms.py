from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Cohort, Module, Discussion



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'cohort')


class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        exclude = ('admin',)


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ('user', 'cohort')


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = ('user', 'cohort')
