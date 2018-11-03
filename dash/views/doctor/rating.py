from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from dash.decorators import doctor_required
from dash.models import Rating


@method_decorator(doctor_required, name='dispatch')
class RatingListView(PermissionRequiredMixin, TemplateView):
    model = Rating
    context_object_name = 'ratings'
    template_name = 'dash/ratings.html'
    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        doctor = self.request.user.doctor
        context[self.context_object_name] = self.model.objects.filter(appointment__doctor_id=doctor.id,
                                                                      status=Rating.APPROVED)\
            .order_by('-appointment__datetime')

        context['is_doctor'] = True
        return context


