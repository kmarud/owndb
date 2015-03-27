from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Adres e-mail',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(render_value=False, attrs={
            'placeholder': 'Hasło',
            'class': 'form-control'
        })
    )


class RegistrationForm(UserCreationForm):
    username = forms.RegexField(label="", max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")},
                                # Every form field uses a widget.
                                # 'attrs' are attributes normally placed in <input xx=""> in templates.
                                widget=forms.TextInput(attrs={
                                    'placeholder': _("Username"),
                                    'class': 'form-control'})
                                )

    email = forms.EmailField(label="", required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Adres e-mail',
                                 'class': 'form-control'})
                             )

    password1 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': _("Password"),
                                    'class': 'form-control'})
                                )

    password2 = forms.CharField(label="",
                                help_text=_("Enter the same password as above, for verification."),
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': _("Password confirmation"),
                                    'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = ["username", "email"]

    # Method used in ModelForm to automaticly save new objects in model stated above
