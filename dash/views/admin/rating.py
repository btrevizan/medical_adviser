from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from dash.decorators import admin_required
from django.urls import reverse_lazy
from django.shortcuts import render
from dash.models import Rating


@method_decorator(admin_required, name='dispatch')
class RatingListView(PermissionRequiredMixin, TemplateView):
    model = Rating
    context_object_name = 'ratings'
    template_name = 'dash/ratings.html'
    permission_required = 'dash.view_rating'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[self.context_object_name] = self.model.objects\
            .filter(status=self.model.WAITING)\
            .order_by('appointment__datetime')

        context['is_admin'] = True

        return context


@method_decorator(admin_required, name='dispatch')
class RatingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Rating
    template_name = 'dash/rating_update_error.html'
    permission_required = 'dash.change_rating'
    success_url = reverse_lazy('rating-list-admin')

    def get(self, request, *args, **kwargs):
        rating = self.model.objects.get(pk=kwargs['pk'])

        if kwargs['status'] == rating.APPROVED:
            rating.status = rating.APPROVED
        elif kwargs['status'] == rating.NOT_APPROVED:
            rating.status = rating.NOT_APPROVED
        else:
            return render(request, self.template_name)

        rating.save()

        return HttpResponseRedirect(self.success_url)
