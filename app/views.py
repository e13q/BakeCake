import json

import phonenumbers as ph
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from phonenumbers import NumberParseException
from yookassa import Configuration, Payment

from .models import (
    Berry,
    Cake,
    ClientUser,
    Decor,
    Form,
    Invoice,
    Level,
    Order,
    Topping,
)

from .forms import OrderForm

Configuration.configure(
    settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY
)


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
        "Words": 500,
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
    levels_titles.insert(0, "не выбрано")
    forms_titles.insert(0, "не выбрано")
    toppings_titles.insert(0, "не выбрано")
    berries_titles.insert(0, "нет")
    decors_titles.insert(0, "нет")
    data = {
        "Levels": levels_titles,
        "Forms": forms_titles,
        "Toppings": toppings_titles,
        "Berries": berries_titles,
        "Decors": decors_titles,
    }
    context.update({"data_json": json.dumps(data)})

    if request.method == "POST":
        payment = Payment.create(
            {
                "amount": {"value": "200", "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri("/"),
                },
                "capture": True,
                "description": "Заказ прошел",
                "test": True,
            }
        )
        return redirect(payment.confirmation.confirmation_url)

    return render(request, "index.html", context)


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Заказ успешно создан! Проверьте почту.",
                }
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse(
        {"success": False, "message": "Неверный метод запроса"}
    )


class ClientLoginView(View):
    def get(self, request):
        return redirect("/")

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        try:
            phone_number_normalised = normalise_phone_number(phone_number)
        except (ValidationError, NumberParseException):
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "⚠ Формат телефона нарушен",
                }
            )

        username = f"user{str(phone_number_normalised).replace('+', '_')}"
        user, _ = ClientUser.objects.get_or_create(
            phone_number=phone_number_normalised,
            defaults={"username": username},
        )
        login(request, user)

        return JsonResponse({"success": True})


class ClientLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class ClientProfileView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(client=user).select_related(
            "cake",
            "cake__level",
            "cake__form",
            "cake__topping",
            "cake__berry",
            "cake__decor",
        )
        client_orders = []

        for order in orders:
            client_orders.append(
                {
                    "order_id": order.id,
                    "cake_id": order.cake.id,
                    "level": order.cake.level.title,
                    "form": order.cake.form.title,
                    "topping": order.cake.topping.title,
                    "berry": order.cake.berry.title
                    if order.cake.berry
                    else "нет",
                    "decor": order.cake.decor.title
                    if order.cake.decor
                    else "нет",
                    "caption": order.cake.caption
                    if order.cake.caption
                    else "Без надписи",
                    "price": order.cake.price,
                    "status": order.get_status_display(),
                    "delivery_date": order.delivery_date,
                    "delivery_time": order.delivery_time,
                }
            )

        context = {
            "client_orders": client_orders,
        }

        return render(request, "lk.html", context)

    def post(self, request):
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        user = request.user

        try:
            phone_number_normalised = normalise_phone_number(phone_number)
        except (ValidationError, NumberParseException):
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "⚠ Формат телефона нарушен",
                }
            )

        if user.full_name != full_name:
            user.full_name = full_name
            user.save()

        if user.phone_number != phone_number_normalised:
            username = f"user{str(phone_number_normalised).replace('+', '_')}"
            user.username = username
            user.phone_number = phone_number_normalised
            user.save()

        if user.email != email:
            user.email = email
            user.save()

        return JsonResponse({"success": True})
