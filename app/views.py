from django.shortcuts import render

# from .forms import OrderForm
import json
from .models import ClientUser, Form, Level, Topping, Berry, Decor, Cake, Invoice, Order
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

from django.shortcuts import render


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise ValidationError("Номер не валиден")

    return pn_normalized


def index(request):
    levels_prices = list(Level.objects.values_list("price", flat=True))
    levels_prices.insert(0, 0)
    forms_prices = list(Form.objects.values_list("price", flat=True))
    forms_prices.insert(0, 0)
    toppings_prices = list(Topping.objects.values_list("price", flat=True))
    toppings_prices.insert(0, 0)
    berries_prices = list(Berry.objects.values_list("price", flat=True))
    berries_prices.insert(0, 0)
    decors_prices = list(Decor.objects.values_list("price", flat=True))
    decors_prices.insert(0, 0)
    costs = {
        "Levels": levels_prices,
        "Forms": forms_prices,
        "Toppings": toppings_prices,
        "Berries": berries_prices,
        "Decors": decors_prices,
        "Words": 500
    }
    levels_titles = list(Level.objects.values_list("title", flat=True))
    forms_titles = list(Form.objects.values_list("title", flat=True))
    toppings_titles = list(Topping.objects.values_list("title", flat=True))
    berries_titles = list(Berry.objects.values_list("title", flat=True))
    decors_titles = list(Decor.objects.values_list("title", flat=True))
    context = {
        "levels": levels_titles.copy(),
        "forms": forms_titles.copy(),
        "toppings": toppings_titles.copy(),
        "berries": berries_titles.copy(),
        "decors": decors_titles.copy(),
        "costs_json": json.dumps(costs),
    }
    levels_titles.insert(0, 'не выбрано')
    forms_titles.insert(0, 'не выбрано')
    toppings_titles.insert(0, 'не выбрано')
    berries_titles.insert(0, 'нет')
    decors_titles.insert(0, 'нет')
    data = {
        "Levels": levels_titles,
        "Forms": forms_titles,
        "Toppings": toppings_titles,
        "Berries": berries_titles,
        "Decors": decors_titles,
    }
    context.update({"data_json": json.dumps(data)})
    return render(request, "index.html", context)


class ClientLoginView(View):
    def get(self, request):
        pass

    def post(self, request):
        phone_number = request.POST.get("phone_number")

        user = authenticate(phone_number=phone_number)

        if user:
            login(request, user)
        else:
            try:
                phone_number_normalised = normalise_phone_number(phone_number)
            except (ValidationError, NumberParseException):
                return JsonResponse(
                    {
                        "success": False,
                        "error_message": "⚠ Формат телефона нарушен",
                    }
                )

        return JsonResponse({"success": True})



class ClientLogoutView(View):
    def get(self, request):
        logout(request)
        return


class ClientProfileView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
