from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from store import models
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _


class ProfileDetail(UpdateView):
    model = User
    context_object_name = 'user'
    fields = ['first_name', 'last_name']
    template_name = 'accounts/profile-detail.html'
    success_url = 'profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['projects_count'] = len(models.Project.objects.filter(owner=self.request.user))
        context['forms_count'] = len(models.Form.objects.filter(project__owner=self.request.user))
        return context

    def get_success_url(self):
        messages.success(self.request, _("Profile successfully updated"))
        return super(ProfileDetail, self).get_success_url()


