from pathlib import Path
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

from django_file_form.forms import ExistingFile
from django_file_form.uploader import FileFormUploader

from . import forms
from .models import Example

def rendertest(request):
    context = {
        'title':'About Page',
        'content':'Welcome to the about page'
    }
    return render(request, "test_ecommerce/test.html", context)

class BaseFormView(generic.FormView):
    template_name = 'test_ecommerce/example_form.html'
    use_ajax = True

    def get_success_url(self):
        return reverse('example_success')

    def form_valid(self, form):
        form.save()
        return super(BaseFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['use_ajax'] = self.use_ajax

        return super(BaseFormView, self).get_context_data(**kwargs)


class ExampleView(BaseFormView):
    form_class = forms.ExampleForm


class ExampleSuccessView(generic.TemplateView):
    template_name = 'success.html'


class MultipleExampleView(BaseFormView):
    form_class = forms.MultipleFileExampleForm


class MultipleWithoutJsExampleView(MultipleExampleView):
    use_ajax = False


class ExistingFileExampleView(BaseFormView):
    form_class = forms.ExistingFileForm

    def get_form_kwargs(self):
        form_kwargs = super(ExistingFileExampleView, self).get_form_kwargs()

        example = Example.objects.get(id=self.kwargs['id'])

        if example.input_file:
            name = Path(example.input_file.name).name
            form_kwargs['initial'] = dict(
                input_file=ExistingFile(name)
            )

        return form_kwargs


handle_upload = FileFormUploader()
















# from django.shortcuts import render
# from django.views import generic
# from django.views.generic import CreateView
# from .forms import TestModelForm
# # Create your views here.


# class TestCreateView(generic.FormView):
#     template_name = 'test_ecommerce/test.html'
#     form_class = TestModelForm

#     def form_valid(self, form):
#         input_file = form.cleaned_data['input_file']
#         form.delete_temporary_files()

#         return super(TestCreateView, self).form_valid(form)


