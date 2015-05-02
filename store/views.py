from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.core.urlresolvers import reverse
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
import re, json


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
        
        print(request.POST)
        print(request.FILES)

        if request.POST.get('connection') == "forms":
            forms = ""
            for form in models.Form.objects.filter(project=self.kwargs['project']):
                forms += '<option value="' + str(form.pk) + '">' + form.title + '</option>'
            return HttpResponse(forms)        

        else:
            
            form_title = request.POST.get('title')
            
            names = json.loads(request.POST.get('names'))
            types = json.loads(request.POST.get('types'))
            settings = json.loads(request.POST.get('settings'))
            
            c = 0
            for type in types:
                if type == "LabelImage":
                    c = c + 1
            
            if c > 0:
                if request.FILES:
                    if len(request.FILES) < c:
                        return HttpResponse("You should provide all images for labels.")
                else:
                    return HttpResponse("You should provide image for label.")
            
            title_pattern = re.compile("^([a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9])$")
            
            if not title_pattern.match(form_title):
                return HttpResponse("Form name is invalid (letters, digits and spaces between allowed)!")

            p = models.Project.objects.get(pk=self.kwargs['project'])
            
            f = models.Form(
                    title=form_title,
                    project=p, 
                    slug = slugify(form_title)
                )
            f.save()

            i = 0

            for name in names:
                
                t = models.Type.objects.get(name=types[i])
                s = settings[i]

                ff = models.FormField(
                    form=f,
                    type=t,
                    caption=name, 
                    settings=s,
                    position=i
                )
                ff.save()
                
                if (t.name == "LabelText"):
                    data = models.DataText(
                            formfield = ff,
                            data = s
                        )
                    data.save()
                    
                if (t.name == "LabelImage"):
                    imgname = "labelimage" + str(i)
                    img = models.Image(
                        formfield=ff, 
                        image=request.FILES[imgname]
                    )
                    img.save()

                if (t.name == "Connection"):
                    cf = models.Form.objects.get(pk=s)
                    c = models.Connection(
                            formfield = ff,
                            form = cf
                        )
                    c.save()
                
                i = i + 1
                
            messages.success(request, "Form successfully added!")
            return HttpResponse("OK")

            
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
        
        if request.POST.get('connection') == "forms":
            forms = ""
            for form in models.Form.objects.filter(project=self.kwargs['project']):
                forms += '<option value="' + str(form.pk) + '">' + form.title + '</option>'
            return HttpResponse(forms)

        else:

            
            form_title = request.POST.get('title')
            
            names = json.loads(request.POST.get('names'))
            types = json.loads(request.POST.get('types'))
            settings = json.loads(request.POST.get('settings'))
            
            c = 0
            for type in types:
                if type == "LabelImage":
                    c = c + 1
            
            if c > 0:
                if request.FILES:
                    if len(request.FILES) < c:
                        return HttpResponse("You should provide all images for labels.")
                else:
                    return HttpResponse("You should provide image for label.")
            
            title_pattern = re.compile("^([a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9])$")
            
            if not title_pattern.match(form_title):
                return HttpResponse("Form name is invalid (letters, digits and spaces between allowed)!")
            
                
            f = models.Form.objects.get(pk=self.kwargs['form'])
            f.title = form_title
            f.slug = slugify(form_title)
            f.save()
            
            #remove instances inserted via this form
            models.FormInstance.objects.filter(form=f).delete()
            
            #remove datatext, image and connection objects 
            #related to formfields in modifying form
            models.DataText.objects.filter(formfield=models.FormField.objects.filter(form=f)).delete()
            
            models.Image.objects.filter(formfield=models.FormField.objects.filter(form=f)).delete() #unable to delete images !!!bug so we cant edit forms with images now
            
            models.ConnectionInstance.objects.filter(connection=models.Connection.objects.filter(formfield=models.FormField.objects.filter(form=f))).delete()
            
            models.Connection.objects.filter(formfield=models.FormField.objects.filter(form=f)).delete()

            #remove all formfields, better we should check to not delete 
            #unchanged fields but correct their position and add new ones only
            models.FormField.objects.filter(form=f).delete() 
            
            i = 0

            for name in names:
                
                t = models.Type.objects.get(name=types[i])
                s = settings[i]

                ff = models.FormField(
                    form=f,
                    type=t,
                    caption=name, 
                    settings=s,
                    position=i
                )
                ff.save()
                
                if (t.name == "LabelText"):
                    data = models.DataText(
                            formfield = ff,
                            data = s
                        )
                    data.save()
                    
                if (t.name == "LabelImage"):
                    imgname = "labelimage" + str(i)
                    img = models.Image(
                        formfield=ff, 
                        image=request.FILES[imgname]
                    )
                    img.save()
                    
                if (t.name == "Connection"):
                    cf = models.Form.objects.get(pk=s)
                    c = models.Connection(
                            formfield = ff,
                            form = cf
                        )
                    c.save()

                i = i + 1

            messages.success(request, "Form changes saved successfully!")
            return HttpResponse("OK")

        
class FormInstanceAdd(VerifiedMixin, TemplateView):
    template_name = 'store/forminstance_add.html'
    
    def get_context_data(self, **kwargs):
        context = super(FormInstanceAdd, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        context['fields'] = models.FormField.objects.filter(form=self.kwargs['form']).order_by('position')

        
        try:
            context['labelimages'] = models.Image.objects.filter(formfield=models.FormField.objects.filter(form=self.kwargs['form']).order_by('position'), forminstance__isnull=True)
        except:
            print("That's only temporary...")
        
            
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if request.POST.get('connection') == "instances":

            fpk = request.POST.get('form')
            forms = "<thead><tr><td></td>"
            for field in models.FormField.objects.filter(form=fpk).order_by('position'):
                if (field.type.pk != 8 and field.type.pk != 9 and field.type.pk != 10):
                    forms += '<td>'+ field.caption +'</td>'
            forms += "</tr></thead><tbody>"

            i = 0
            for instance in models.FormInstance.objects.filter(form=models.Form.objects.get(pk=fpk)):
                forms += '<tr><td><a class="modal-select" name="'+str(instance.pk)+'">#</a></td>'
                for field in models.FormField.objects.filter(form=fpk).order_by('position'):
                    if (field.type.pk != 8 and field.type.pk != 9 and field.type.pk != 10 and field.type.pk != 5):
                        insd = models.DataText.objects.get(formfield = field, forminstance = instance)
                        forms += '<td>' + str(insd.data) + '</td>'
                forms += '</tr>'
                i = i + 1
            forms += '</tbody>'
            
            if i==0:
                forms = '<tr><td>Connected form is empty!</td></tr>'
            
            return HttpResponse(forms)

        else:

            f = models.Form.objects.get(pk=self.kwargs['form'])
            fi = models.FormInstance(
                    form = f,
                    user = self.request.user
                )
            fi.save()
            
            contents = json.loads(request.POST.get('contents'))
            
            i = 0
            for field in models.FormField.objects.filter(form=self.kwargs['form']).order_by('position'):
                if (field.type.pk != 8 and field.type.pk != 9 and field.type.pk != 10):
                    if (field.type.pk == 5):
                        imgname = "image" + str(i)
                        img = models.Image(
                            formfield=field,
                            forminstance = fi,
                            image=request.FILES[imgname]
                        )
                        img.save()
                    else:
                        data = models.DataText(
                            formfield = field,
                            forminstance = fi,
                            data = contents[i]
                        )
                        data.save()
                i = i + 1

            messages.success(request, "Form instance added successfully!")
            return HttpResponse("OK")
        
            
    
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
    paginate_by = 5
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
            return HttpResponseRedirect(reverse('project-list'))

        p.save()
        messages.success(request, "Project \"" + p.title + "\" succesfully added!")
        return HttpResponseRedirect(reverse('project-list'))


class ProjectEdit(VerifiedMixin, TemplateView):
    template_name = 'store/project_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectEdit, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        p = models.Project.objects.get(pk=self.kwargs['project'])
        p.title = self.request.POST.get('project_name')
        p.slug = slugify(self.request.POST.get('project_name'))
        if ( p.title.isspace() or p.title=='' ):
            messages.error(request, "Bad project name!")
            return HttpResponseRedirect(reverse('project-list'))

        p.save()
        messages.success(request, "Project \"" + p.title + "\" succesfully edited!")
        return HttpResponseRedirect(reverse('form-list', kwargs={'project': self.kwargs['project'] } ))


class FormDelete(VerifiedMixin, TemplateView):
    template_name = 'store/form_delete.html'

    def get_context_data(self, **kwargs):
        context = super(FormDelete, self).get_context_data(**kwargs)
        context['project'] = models.Project.objects.get(pk=self.kwargs['project'])
        context['form'] = models.Form.objects.get(pk=self.kwargs['form'])
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        f = models.Form.objects.get(pk=self.kwargs['form'])
        titleBackup = f.title
        models.FormField.objects.filter(form=f).delete()
        f.delete()
        messages.success(request, "Form \"" + titleBackup + "\" successfully deleted!")
        return HttpResponseRedirect(reverse('form-list', kwargs={'project': self.kwargs['project'] } ))
