from django.views import generic


class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'