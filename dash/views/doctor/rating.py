from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from dash.decorators import doctor_required
from django.urls import reverse_lazy
from django.shortcuts import render
from dash.models import Rating

@method_decorator(doctor_required, name='dispatch')
class RatingListView(PermissionRequiredMixin, TemplateView):
    model = Rating
    context_object_name = 'ratings'
    template_name = 'dash/ratings.html'

    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[self.context_object_name] = self.model.objects\
            .filter(status=self.model.WAITING)\
            .order_by('appointment__datetime')

        context['is_doctor'] = True

        return context

