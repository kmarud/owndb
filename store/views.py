from django.views.generic import ListView
from django.views.generic import DetailView
from store import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Check if guest is a logged user
class LoggedInMixin(object):
    # Transform function decorator into method decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class ProjectList(LoggedInMixin, ListView):
    model = models.Project
    paginate_by = 1
    context_object_name = 'project_list'

    def get_queryset(self):
        return self.model.objects.filter(owner__pk=self.request.user.pk)


class FormList(LoggedInMixin, ListView):
    model = models.Form
    paginate_by = 10
    context_object_name = 'form_list'

    def get_queryset(self):
        return self.model.objects.filter(project__pk=self.kwargs['project'])

    def get_context_data(self, **kwargs):
        context = super(FormList, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        return context


class FormInstanceList(LoggedInMixin, ListView):
    model = models.FormInstance
    paginate_by = 10
    context_object_name = 'forminstance_list'

    def get_queryset(self):
        return self.model.objects.filter(form__pk=self.kwargs['form'])

    def get_context_data(self, **kwargs):
        context = super(FormInstanceList, self).get_context_data(**kwargs)
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        return context


class FormInstanceDetail(DetailView):
    model = models.FormInstance
    context_object_name = 'forminstance'
    slug_field = 'id'
    slug_url_kwarg = 'forminstance'

    def get_context_data(self, **kwargs):
        context = super(FormInstanceDetail, self).get_context_data(**kwargs)
        context['formfield_list'] = models.FormField.objects.filter(form__pk=self.kwargs['form']).order_by('position')
        context['text_list'] = models.Text.objects.filter(
            Q(forminstance__pk__isnull=True, formfield__form__pk=self.kwargs['form'])
            | Q(forminstance__pk=self.kwargs['forminstance'])).order_by('formfield__position')
        return context
