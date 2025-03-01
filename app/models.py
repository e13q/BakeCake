from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ClientUser(AbstractUser):
    phone_number = PhoneNumberField("Номер телефона", region="RU", unique=True)
    full_name = models.CharField("ФИО", max_length=200, blank=True)
    email = models.EmailField("Email", max_length=255, blank=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Level(models.Model):
    title = models.CharField("Название уровня", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Размер/уровень для торта"
        verbose_name_plural = "Размеры/уровни для торта"


class Form(models.Model):
    title = models.CharField("Название формы", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Форма для торта"
        verbose_name_plural = "Формы для торта"


class Topping(models.Model):
    title = models.CharField("Название топпинга", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Топпинг для торта"
        verbose_name_plural = "Топпинги для торта"


class Berry(models.Model):
    title = models.CharField("Название ягоды", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Ягода для торта"
        verbose_name_plural = "Ягоды для торта"


class Decor(models.Model):
    title = models.CharField("Название декора", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Декор для торта"
        verbose_name_plural = "Декоры для торта"


class Cake(models.Model):
    price = models.FloatField("Цена торта")
    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        verbose_name="Количество уровней торта",
    )
    form = models.ForeignKey(
        Form, on_delete=models.PROTECT, verbose_name="Форма торта"
    )
    topping = models.ForeignKey(
        Topping, on_delete=models.PROTECT, verbose_name="Топпинг"
    )
    berry = models.ForeignKey(
        Berry,
        on_delete=models.PROTECT,
        verbose_name="Ягода",
        null=True,
        blank=True,
    )
    decor = models.ForeignKey(
        Decor,
        on_delete=models.PROTECT,
        verbose_name="Декор",
        null=True,
        blank=True,
    )
    caption = models.CharField(
        "Надпись на торте", max_length=200, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.id) or "Кастом"

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"


class Invoice(models.Model):
    STATUSES = [
        ("1", "Ожидает оплаты"),
        ("2", "Оплачено"),
        ("3", "Отменено"),
    ]
    status = models.CharField(
        "Статус счета", max_length=14, choices=STATUSES, default="1"
    )
    receipt = models.URLField("Чек", blank=True, null=True)
    created_at = models.DateTimeField("Счёт выставлен", auto_now_add=True)
    updated_at = models.DateTimeField("Последнее обновление", auto_now=True)
    amount = models.FloatField("Сумма чека")

    def __str__(self) -> str:
        return f"{self.updated_at} {self.orders.first().client.full_name} {self.status}"

    class Meta:
        verbose_name = "Счет на оплату"
        verbose_name_plural = "Счета на оплату"


class Order(models.Model):
    STATUSES = [
        ("1", "Принят"),
        ("2", "В доставке"),
        ("3", "Выполнен"),
        ("4", "Отменен"),
    ]
    status = models.CharField(
        "Статус заказа", max_length=9, choices=STATUSES, default="1"
    )
    date = models.DateField("Дата заказа", auto_now_add=True)
    time = models.TimeField("Время заказа", auto_now_add=True)
    client = models.ForeignKey(
        ClientUser,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Клиент",
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Торт",
    )
    delivery_date = models.DateField("Дата доставки")
    delivery_time = models.TimeField("Время доставки")
    delivery_address = models.TextField(
        verbose_name="Адрес доставки", max_length=200, null=True, blank=True
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        verbose_name="Счет на оплату",
        related_name="orders",
    )
    comment = models.CharField(
        "Комментарий для курьера",
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(f"{self.id} {self.client.phone_number}")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class AdvertisingLink(models.Model):
    url = models.URLField("Ссылка")
    short_url = models.URLField("Сокращенная ссылка", blank=True)
    visits_number = models.IntegerField("Количество визитов", default=0)

    class Meta:
        verbose_name = "Рекламная ссылка"
        verbose_name_plural = "Рекламные ссылки"
