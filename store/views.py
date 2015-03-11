from django.views.generic import ListView
from django.views.generic import DetailView
from store import models


class CategoryList(ListView):
    model = models.Category
    paginate_by = 6
    context_object_name = 'category_list'


class FormList(ListView):
    model = models.Form
    paginate_by = 10
    context_object_name = 'form_list'

    def get_queryset(self):
        return self.model.objects.filter(category__pk=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super(FormList, self).get_context_data(**kwargs)
        context['category'] = models.Category.objects.get(pk=self.kwargs['category'])
        return context


class FormInstanceList(ListView):
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
        context['formfield_list'] = models.FormField.objects.filter(form__pk=self.kwargs['form'])
        context['text_list'] = models.Text.objects.filter(forminstance__pk=self.kwargs['forminstance'])
        return context
