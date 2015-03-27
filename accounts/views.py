from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.views.generic import DetailView, FormView
from accounts.forms import RegistrationForm
from django.contrib.auth.models import User


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = '/store'

    def form_valid(self, form):
        # Use method from form to create new user
        form.save()
        messages.success(self.request, "Zarejestrowano!")
        return super(RegistrationView, self).form_valid(form)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

    return HttpResponseRedirect('/store')