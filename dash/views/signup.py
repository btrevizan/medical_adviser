from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from dash.models import Doctor, Patient, Address
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from dash.forms import *


class SignUpView(generic.CreateView):
    model = User
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': SignUpForm()})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            # Create user
            user = form.save(commit=False)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            user.save()

            # Log user in
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)

            # Set permissions and redirect
            user_type = form.cleaned_data['type']

            if user_type == form.DOCTOR:
                group = Group.objects.get(name='doctor')
                group.user_set.add(user)

                return HttpResponseRedirect('/dash/signup/doctor')
            elif user_type == form.PATIENT:
                group = Group.objects.get(name='patient')
                group.user_set.add(user)

                return HttpResponseRedirect('/dash/signup/patient')

        return render(request, self.template_name, {'form': form})


class SignUpPatientView(generic.CreateView):
    template_name = 'registration/signup_patient.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': SignUpPatientForm()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = SignUpPatientForm(request.POST)

        if form.is_valid():
            user = request.user

            # Create patient
            patient = Patient()
            patient.user = user
            patient.cpf = form.cleaned_data['cpf']
            patient.city = form.cleaned_data['city']
            patient.uf = form.cleaned_data['uf']

            patient.save()

            # Log user out
            logout(request)

            return HttpResponseRedirect('/dash/login')
        else:
            return render(request, self.template_name, {'form': form})


class SignUpDoctorView(generic.CreateView):
    template_name = 'registration/signup_doctor.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'doctor_form': SignUpDoctorForm(),
                                                    'address_form': SignUpAddressForm()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        doctor_form = SignUpDoctorForm(request.POST)
        address_form = SignUpAddressForm(request.POST)

        if doctor_form.is_valid() and address_form.is_valid():
            user = request.user

            # Create address
            address = Address()
            address.uf = address_form.cleaned_data['uf']
            address.city = address_form.cleaned_data['city']
            address.neighborhood = address_form.cleaned_data['neighborhood']
            address.street = address_form.cleaned_data['street']
            address.number = address_form.cleaned_data['number']
            address.complement = address_form.cleaned_data['complement']

            address.save()

            # Create doctor
            doctor = Doctor()
            doctor.user = user
            doctor.address = address
            doctor.crm = doctor_form.cleaned_data['crm']
            doctor.crm_uf = doctor_form.cleaned_data['crm_uf']
            doctor.speciality = doctor_form.cleaned_data['speciality']

            doctor.save()

            # Log user out
            logout(request)

            return HttpResponseRedirect('/dash/login')
        else:
            return render(request, self.template_name, {'doctor_form': doctor_form,
                                                        'address_form': address_form})

