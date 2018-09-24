from django import forms
from .models import Doctor, Patient


class AppointmentForm(forms.Form):
    doctor = forms.IntegerField()       # doctor_id
    patient = forms.IntegerField()      # patient_id
    datetime = forms.DateTimeField()

    def clean(self):
        cleaned_data = super().clean()
        doctor_id = cleaned_data.get('doctor')
        patient_id = cleaned_data.get('patient')

        if not Doctor.objects.filter(pk=doctor_id).exists():
            self.add_error['doctor'] = 'Médico não existe.'

        if not Patient.objects.filter(pk=patient_id).exists():
            self.add_error['patient'] = 'Paciente não existe.'
