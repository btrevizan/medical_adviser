from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/main.html'
