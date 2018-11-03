from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from dash.decorators import admin_required
from dash.forms import RegisterAdminForm
from django.shortcuts import render
from dash.models import Admin


@method_decorator(admin_required, name='dispatch')
class RegisterAdminView(PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'dash/register_admin.html'
    permission_required = 'dash.add_admin'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': RegisterAdminForm()})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = RegisterAdminForm(request.POST)

        if form.is_valid():
            # Create user
            user = form.save(commit=False)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            user.save()

            # Set permissions and redirect
            group = Group.objects.get(name='admin')
            group.user_set.add(user)

            admin = Admin()
            admin.user = user
            admin.save()

            return HttpResponseRedirect('/dash')
        else:
            return render(request, self.template_name, {'form': form})
