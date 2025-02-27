from datetime import date, datetime, timedelta

import phonenumbers as ph
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Count, Min, Q
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from phonenumbers import NumberParseException

from .models import ClientUser


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise ValidationError("Номер не валиден")

    return pn_normalized


def index(request):
    return render(request, "index.html")


def lk(request):
    return render(request, "lk.html")


class ClientLoginView(View):
    def get(self, request):
        return redirect("app:index")

    def post(self, request):
        name = request.POST.get("FULL_NAME_CREATE")
        email = request.POST.get("EMAIL_CREATE")
        password = request.POST.get("PASSWORD_CREATE")
        try:
            user = get_user_model().objects.create_user(
                email=email, username=email, password=password
            )
            ClientUser.objects.create(full_name=name, user=user)
        except IntegrityError:
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "Пользователь с таким email уже зарегистрирован",
                }
            )
        login(request, user)

        return JsonResponse({"success": True})


class ClientLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("app:index")


class ClientProfileView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
