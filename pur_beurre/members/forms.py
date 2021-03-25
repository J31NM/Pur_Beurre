from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class Bs4FormMixin:
    def as_bs4(self):
        """
        Return this form rendered as HTML bootstrap 4 style.
        """
        return self._html_output(
            normal_row='<div class="form-group" %(html_class_attr)s> %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <small id="help" class="form-text text-muted">%s</small>',
            errors_on_separate_row=True
        )


class CreateUserForm(Bs4FormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        field_classes = ['form-control', 'form-control-lg']



