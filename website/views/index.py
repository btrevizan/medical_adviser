from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from dash.models import Doctor
from website.forms import *


class IndexView(generic.TemplateView):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'search_form': SearchDoctorForm()})


class SearchDoctorView(generic.ListView):
    model = Doctor
    template_name = 'website/search_doctor_results.html'
    context_object_name = 'doctors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchDoctorForm(self.request.GET)

        if form.is_valid():
            obj_name = self.context_object_name
            context[obj_name] = context[obj_name].filter(speciality__icontains=form.cleaned_data['speciality'],
                                                         address__city__icontains=form.cleaned_data['city'],
                                                         address__neighborhood__icontains=form.cleaned_data[
                                                             'neighborhood'])

            context[obj_name] = context[obj_name].order_by('user__username')
            context[obj_name] = [doctor for doctor in context[obj_name]
                                 if doctor.has_free_schedule(form.cleaned_data['startdt'], form.cleaned_data['enddt'])]

            return context
        else:
            return HttpResponseRedirect('/')
