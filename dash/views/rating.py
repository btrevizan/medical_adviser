from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from dash.models import Rating, Appointment
from django.urls import reverse_lazy
from dash.forms import RatingForm


class RatingListView(PermissionRequiredMixin, TemplateView):
    model = Rating
    context_object_name = 'ratings'
    template_name = 'dash/ratings.html'
    permission_required = 'dash.view_rating'

    def get_context_data(self, **kwargs):
        patient = self.request.user.patient
        context = {self.context_object_name: self.model.objects
                                                .filter(appointment__patient_id=patient.id)
                                                .order_by('-appointment__datetime')}
        return context


class RatingCreateView(PermissionRequiredMixin, TemplateView):
    model = Rating
    form_class = RatingForm
    template_name = 'dash/rating_create_update.html'
    permission_required = 'dash.add_rating'
    success_url = reverse_lazy('rating-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_choices'] = Rating.STARS_CHOICES
        context['appointment'] = get_object_or_404(Appointment, pk=kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            appointment = get_object_or_404(Appointment, pk=kwargs['pk'])

            rating = Rating()
            rating.appointment = appointment
            rating.description = form.cleaned_data['description']
            rating.stars = form.cleaned_data['stars']
            rating.save()

            rating.appointment.doctor.update_avg_rating()

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class RatingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    context_object_name = 'rating'
    template_name = 'dash/rating_create_update.html'
    permission_required = 'dash.change_rating'
    success_url = reverse_lazy('rating-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_choices'] = Rating.STARS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        errors = []
        form = self.form_class(request.POST)
        patient = self.request.user.patient
        rating = Rating.objects.get(pk=kwargs['pk'])

        if form.is_valid():
            if rating.appointment.patient_id == patient.id:
                rating.description = form.cleaned_data['description']
                rating.stars = form.cleaned_data['stars']
                rating.status = rating.WAITING
                rating.save()

                rating.appointment.doctor.update_avg_rating()

                return HttpResponseRedirect(self.success_url)
            else:
                errors = ['A avaliação editada não foi encontrada.']

        return render(request, self.template_name, {'errors': errors})


class RatingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Rating
    form_class = RatingForm
    template_name = 'dash/rating_delete.html'
    context_object_name = 'rating'
    success_url = reverse_lazy('rating-list')
    permission_required = 'dash.delete_rating'
