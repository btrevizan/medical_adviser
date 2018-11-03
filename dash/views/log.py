from django.contrib.auth import logout
from django.views import generic


class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)