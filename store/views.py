from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from allauth.account.decorators import verified_email_required
from datetime import datetime
from store import models
import re


# Check if guest is a logged user
class LoggedInMixin(object):
    # Transform function decorator into method decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

        
# Check if guest is a logged user
class VerifiedMixin(object):
    # Transform function decorator into method decorator
    @method_decorator(verified_email_required)
    def dispatch(self, *args, **kwargs):
        return super(VerifiedMixin, self).dispatch(*args, **kwargs)
        
        
class FormAdd(VerifiedMixin,TemplateView):
    template_name = 'store/form_add.html'
    
    def get_context_data(self, **kwargs):
        context = super(FormAdd, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if (request.POST.get('connection') == "false"):
        
            title_pattern = re.compile("^([a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9])$")
            if not title_pattern.match(request.POST.get('title')):
                return HttpResponse("Form name is invalid (letters, digits and spaces between allowed)!")

            p = models.Project.objects.get(pk=self.kwargs['project'])
            f = models.Form(
                    title=request.POST.get('title'),
                    project=p, 
                    slug = slugify(request.POST.get('title'))
                )
            f.save()

            i = 0
            for name in request.POST.getlist("names[]"):
                
                t = models.Type.objects.get(name=request.POST.getlist("types[]")[i])
                s = request.POST.getlist("settings[]")[i]
                
                ff = models.FormField(
                    form=f, 
                    type=t,
                    caption=name, 
                    settings=s,
                    position=i
                )
                ff.save()

                if (t.name == "Connection"):
                    ffepk = s.split(';')
                    ffe = models.FormField.objects.get(pk=ffepk[1])
                    c = models.Connection(
                            formfield_begin = ff,
                            formfield_end = ffe
                        )
                    c.save()
                
                i = i + 1

            return HttpResponse("OK")
            
        elif (request.POST.get('connection') == "field"):
            fields = ""
            for field in models.FormField.objects.filter(form=request.POST.get('form')):
                fields += '<option value="' + str(field.pk) + '">' + field.caption + '</option>'
            return HttpResponse(fields)
            
        else:
            forms = ""
            for form in models.Form.objects.filter(project=self.kwargs['project']):
                forms += '<option value="' + str(form.pk) + '">' + form.title + '</option>'
            return HttpResponse(forms)
        
        
class FormEdit(VerifiedMixin,TemplateView):
    template_name = 'store/form_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super(FormEdit, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        context['fields'] = models.FormField.objects.filter(form=self.kwargs['form']).order_by('position')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        
        if (request.POST.get('connection') == "false"):
        
            title_pattern = re.compile("^([a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9])$")
            if not title_pattern.match(request.POST.get('title')):
                return HttpResponse("Form name is invalid (letters, digits and spaces between allowed)!")

            f = models.Form.objects.get(pk=self.kwargs['form'])
            f.title = request.POST.get('title')
            f.slug = slugify(request.POST.get('title'))
            f.save()

            models.FormField.objects.filter(form=f).delete()
            #the simplest but in the future will be easily added more intelligent solution here

            i = 0
            for name in request.POST.getlist("names[]"):
                ff = models.FormField(
                    form=f, 
                    type=models.Type.objects.get(name=request.POST.getlist("types[]")[i]),
                    caption=name, 
                    settings=request.POST.getlist("settings[]")[i],
                    position=i
                )
                ff.save()
                i = i + 1

            return HttpResponse("OK")
            
        elif (request.POST.get('connection') == "field"):
            #fields of form (active choice should be at first option)
            fields = ""
            for field in models.FormField.objects.filter(form=request.POST.get('form')):
                fields += '<option value="' + str(field.pk) + '">' + field.caption + '</option>'
            return HttpResponse(fields)
            
        else:
            #list of forms in project for connection field (active choice should be at first option)
            forms = ""
            for form in models.Form.objects.filter(project=self.kwargs['project']):
                forms += '<option value="' + str(form.pk) + '">' + form.title + '</option>'
            return HttpResponse(forms)

        
class FormInstanceAdd(VerifiedMixin, TemplateView):
    template_name = 'store/forminstance_add.html'
    
    def get_context_data(self, **kwargs):
        context = super(FormInstanceAdd, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        context['fields'] = models.FormField.objects.filter(form=self.kwargs['form']).order_by('position')

        try:
            temp = models.FormField.objects.filter(form=self.kwargs['form'], type=models.Type.objects.get(name="Connection"))[0]
            context['temp_data_list'] = models.DataText.objects.filter(formfield=models.Connection.objects.get(formfield_begin=temp).formfield_end)
        except:
            print("That's only temporary...")
            
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
                    
        f = models.Form.objects.get(pk=self.kwargs['form'])
        fi = models.FormInstance(
                form=f,
                user = self.request.user
            )
        fi.save()
        
        i = 0
        for field in models.FormField.objects.filter(form=self.kwargs['form']).order_by('position'):
            data = models.DataText(
                    formfield = field,
                    forminstance = fi,
                    data = request.POST.getlist("contents[]")[i]
                )
            data.save()
            i = i + 1
        
        return HttpResponse("OK")
        

class FormInstanceAddConnectionAutocomplete(View):

    def get(self, request, *args, **kwargs):
        if 'connection' in kwargs:
            json_response = ['value1','value2','value3','value4']
            return HttpResponse(json_response,content_type='application/json')
    
    
class ProjectList(VerifiedMixin, ListView):
    model = models.Project
    paginate_by = 2
    context_object_name = 'project_list'

    def get_queryset(self):
        return self.model.objects.filter(owner__pk=self.request.user.pk)


class FormList(VerifiedMixin, ListView):
    model = models.Form
    paginate_by = 4
    context_object_name = 'form_list'

    def get_queryset(self):
        return self.model.objects.filter(project__pk=self.kwargs['project'])

    def get_context_data(self, **kwargs):
        context = super(FormList, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        return context


class FormInstanceList(VerifiedMixin, ListView):
    model = models.FormInstance
    paginate_by = 10
    context_object_name = 'forminstance_list'

    def get_queryset(self):
        return self.model.objects.filter(form__pk=self.kwargs['form'])

    def get_context_data(self, **kwargs):
        context = super(FormInstanceList, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        return context


class FormInstanceDetail(VerifiedMixin, DetailView):
    model = models.FormInstance
    context_object_name = 'forminstance'
    slug_field = 'id'
    slug_url_kwarg = 'forminstance'

    def get_context_data(self, **kwargs):
        context = super(FormInstanceDetail, self).get_context_data(**kwargs)
        context['formfield_list'] = models.FormField.objects.filter(form__pk=self.kwargs['form']).order_by('position')
        context['text_list'] = models.DataText.objects.filter(
            # Get text labels
            Q(forminstance__pk__isnull=True, formfield__form__pk=self.kwargs['form']) |
            # Get text data
            Q(forminstance__pk=self.kwargs['forminstance'])).order_by('formfield__position')
        context['image_list'] = models.Image.objects.filter(
            # Get image labels
            Q(forminstance__pk__isnull=True, formfield__form__pk=self.kwargs['form']) |
            # Get image data
            Q(forminstance__pk=self.kwargs['forminstance'])).order_by('formfield__position')
        return context


class ProjectAdd(VerifiedMixin, SuccessMessageMixin, TemplateView):
    template_name = 'store/project_add.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectAdd, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        p = models.Project(
            title=self.request.POST.get('project_name'),
            owner=self.request.user,
            slug=slugify(self.request.POST.get('project_name'))

        )
        if ( p.title.isspace() or p.title=='' ):
            messages.error(request, "Bad project name!")
            return HttpResponseRedirect('/store/')

        p.save()
        messages.success(request, "Your project succesfully added!")
        return HttpResponseRedirect('/store/')


class ProjectEdit(VerifiedMixin, TemplateView):
    template_name = 'store/project_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectEdit, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        p = models.Project.objects.get(pk=self.kwargs['project'])
        p.title = self.request.POST.get('project_name')
        p.slug = slugify(self.request.POST.get('project_name'))
        if ( p.title.isspace() or p.title=='' ):
            messages.error(request, "Bad project name!")
            return HttpResponseRedirect('/store/')

        p.save()
        messages.success(request, "Your project succesfully edited!")
        return HttpResponseRedirect('/store/')


class FormDelete(VerifiedMixin, TemplateView):
    template_name = 'store/form_delete.html'

    def get_context_data(self, **kwargs):
        context = super(FormDelete, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        context['fields'] = models.FormField.objects.filter(form=self.kwargs['form']).order_by('position')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        num = self.kwargs['project']
        f = models.Form.objects.get(pk=self.kwargs['form'])
        models.FormField.objects.filter(form=f).delete()
        f.delete()
        messages.success(request, "Successfully deleted !")
        return HttpResponseRedirect('/store/' + str(num))
