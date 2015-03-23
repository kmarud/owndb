from django import forms


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