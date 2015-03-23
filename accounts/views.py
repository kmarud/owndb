from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import DetailView, FormView
from accounts.forms import LoginForm


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = LoginForm
    success_url = 'store'

    def form_valid(self, form):
        login(self.request, form.get_account())
        messages.success(self.request, "Logged!")
        return super(RegistrationView, self).form_valid(form)