from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView


class DashRedirectView(LoginRequiredMixin, RedirectView):
    query_string = True
    pattern_name = 'appointment-list'
