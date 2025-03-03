from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from phonenumber_field.formfields import PhoneNumberField
from django.shortcuts import get_object_or_404
from yookassa import Payment

from .models import Cake, ClientUser, Order, Level, Form, Topping, Berry, Decor, Invoice


def create_payment(request, price):
    payment = Payment.create(
        {
            "amount": {"value": price, "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri("/"),
            },
            "capture": True,
            "description": "Заказ прошел",
            "test": True,
        }
    )
    return payment.id, payment.confirmation.confirmation_url


class OrderForm(forms.Form):
    level = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "required": "Нужно выбрать уровни.",
        },
    )
    form = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "required": "Нужно выбрать форму.",
        },
    )
    topping = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "required": "Нужно выбрать топпинг.",
        },
    )
    berry = forms.CharField(max_length=200, required=False)
    decor = forms.CharField(max_length=200, required=False)
    words = forms.CharField(max_length=200, required=False)
    order_comment = forms.CharField(max_length=200, required=False)
    # NAME
    full_name = forms.CharField(
        label="",
        max_length=200,
        required=True,
        error_messages={
            "required": "Поле 'ФИО' обязательно для заполнения.",
            "invalid": "Ну и что ты тут умудрился написать?",
        },
    )
    # EMAIL
    email = forms.EmailField(
        label="",
        max_length=255,
        required=True,
        error_messages={
            "required": "Поле 'Email' обязательно для заполнения.",
            "invalid": "Введите корректный email-адрес.",
        },
    )
    # PHONE
    phone_number = PhoneNumberField(
        label="",
        region="RU",
        required=True,
        error_messages={
            "invalid": "Введите правильный номер телефона в формате +7 (___) ___-__-__.",
            "required": "Поле 'Номер телефона' обязательно для заполнения.",
        },
    )
    # ADDRESS
    address = forms.CharField(
        label="",
        max_length=200,
        required=True,
        error_messages={
            "required": "Укажите откуда забирать вещи.",
        },
    )
    # DATE
    order_date = forms.DateField(
        label="Дата начала аренды",
        required=True,
        error_messages={
            "required": "Укажите дату заказа",
        },
    )
    order_time = forms.TimeField(
        label="Время начала аренды",
        required=True,
        error_messages={
            "required": "Укажите время заказа",
        },
    )
    delivery_comment = forms.CharField(max_length=200, required=False)

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get("order_date")
        email = cleaned_data.get("email")
        now = timezone.now().date()
        if order_date and order_date < now:
            self.add_error("order_date", "Дата заказа должна быть актуальной.")

        user = ClientUser.objects.filter(email=email).first()
        if user and (self.user is None or self.user.is_anonymous):
            self.add_error(
                "email",
                "Для указанного email существует учётная запись. Авторизуйтесь.",
            )
        if (
            user
            and self.user
            and self.user.is_authenticated
            and self.user.email != user.email
        ):
            self.add_error(
                "email",
                "Вы уже авторизованы под другой УЗ. Авторизуйтесь под иной учётной записью.",
            )
        phone_number = cleaned_data.get("phone_number")
        user = ClientUser.objects.filter(phone_number=phone_number).first()
        if user and (self.user is None or self.user.is_anonymous):
            self.add_error(
                "phone_number",
                "Для указанного phone_number существует учётная запись. Авторизуйтесь.",
            )
        if (
            user
            and self.user
            and self.user.is_authenticated
            and self.user.phone_number != user.phone_number
        ):
            self.add_error(
                "phone_number",
                "Вы уже авторизованы под другой УЗ. Авторизуйтесь под иной учётной записью.",
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.request = kwargs.pop("request", None)  # Извлекаем request из kwargs
        super().__init__(*args, **kwargs)

    def save(self):
        with transaction.atomic():
            data = self.cleaned_data

            # Торт
            price = 0 if data["words"] == "" else 500

            level = get_object_or_404(Level, title=data["level"])
            form = get_object_or_404(Form, title=data["form"])
            topping = get_object_or_404(Topping, title=data["topping"])
            price += level.price + form.price + topping.price
            if data["berry"] != "":
                berry = get_object_or_404(Berry, title=data["berry"])
                price += berry.price
            else:
                berry = None
            if data["decor"] != "":
                decor = get_object_or_404(Decor, title=data["decor"])
                price += decor.price
            else:
                decor = None
            cake = Cake.objects.create(
                level=level,
                form=form,
                topping=topping,
                berry=berry,
                decor=decor,
                price=price,
                caption=data["words"],
            )
            amount = cake.price
            yoomoney_id, url = create_payment(self.request, amount)
            # Чек
            invoice = Invoice.objects.create(
                amount=amount, yoomoney_id=yoomoney_id, receipt=url
            )
            # Клиент
            from django.db.models import Q

            client = ClientUser.objects.filter(
                Q(email=data["email"]) | Q(phone_number=data["phone_number"])
            ).first()

            if not client:
                client, client_created = ClientUser.objects.create(
                    email=data["email"],
                    phone_number=data["phone_number"],
                    full_name=data["full_name"],
                )
                client_created = True
            else:
                client_created = False

            # Заказ
            order, order_created = Order.objects.get_or_create(
                client=client,
                cake=cake,
                invoice=invoice,
                delivery_date=data["order_date"],
                delivery_time=data["order_time"],
                delivery_address=data["address"],
                comment=data["delivery_comment"],
            )
            if client_created:
                username = get_random_string(length=8)
                while not ClientUser.objects.filter(username=username).first() is None:
                    username = get_random_string(length=8)
                client.username = username
                password = get_random_string(length=12)
                client.password = make_password(password)
                client.set_password(password)
                client.save()
                subject = "BakeCake| Пароль от учётной записи"
                message = f"Здарова, {client.full_name}!\n\nУ тебя создана учётная запись в рамках формирования заказа {order.id}.\nИспользуй для входа:\nE-mail: {client.phone_number}\nПароль: {password}\n\nВсего хорошего :)\n\nBakeCake service"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [client.email]
                send_mail(subject, message, from_email, recipient_list)

            if order_created:
                subject = "BakeCake| Сформирован заказ"
                message = f"Приветствую, {client.full_name}!\n\nСформирован заказ №{order.id}:\nАдрес доставки: {order.delivery_address}\nСостав торта\nУровни: {order.cake.level}\nФорма: {order.cake.form}\nТоппинг: {order.cake.topping}\nЯгоды: {order.cake.berry or 'отсутствуют'}\nДекор: {order.cake.decor or 'отсутствует'}\nНадпись: {order.cake.caption or 'отсутствует'}\n\nПланируемая дата доставки: {order.delivery_date} {order.delivery_time}\n\nВсего хорошего :)\n\nBakeCake service"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [client.email]
                send_mail(subject, message, from_email, recipient_list)
            return url
