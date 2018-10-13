from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def patient_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged in user is a patient,
    redirects to the log-in page if necessary.
    """
    def is_patient(user):
        try:
            return user.patient
        except:
            raise PermissionDenied

    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_patient(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def doctor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged in user is a patient,
    redirects to the log-in page if necessary.
    """
    def is_doctor(user):
        try:
            return user.doctor
        except:
            raise PermissionDenied

    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_doctor(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged in user is a patient,
    redirects to the log-in page if necessary.
    """
    def is_admin(user):
        try:
            return user.admin
        except:
            raise PermissionDenied

    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_admin(u),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)

    return actual_decorator