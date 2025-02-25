import random
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import CustomUser, Client, Form, Level, Topping, Berry, Decor, Cake, Invoice, Order


class Command(BaseCommand):
    help = "Заполнить базу данных тестовыми данными"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Создание клиентов
            user1 = CustomUser.objects.create_user(
                email="user1@example.com", password="password123", username="user1"
            )
            user2 = CustomUser.objects.create_user(
                email="user2@example.com", password="password123", username="user2"
            )
            user3 = CustomUser.objects.create_user(
                email="user3@example.com", password="password123", username="VALERA"
            )

            clients = []
            clients.append(Client.objects.create(
                full_name="Иван Иванов",
                user=user1,
                phone_number="+79161112233"
            ))
            clients.append(Client.objects.create(
                full_name="Петр Петров",
                user=user2,
                phone_number="+79162223344"
            ))
            clients.append(Client.objects.create(
                full_name="Валерий",
                user=user3,
                phone_number="+79162223324"
            ))
            # Создание уровней
            Level.objects.create(title="1 уровень", price=400)
            Level.objects.create(title="2 уровня", price=750)
            Level.objects.create(title="3 уровня", price=1100)

            # Создание форм
            Form.objects.create(title="Круг", price=600)
            Form.objects.create(title="Квадрат", price=400)
            Form.objects.create(title="Прямоугольник", price=1000)

            # Создание топпингов
            Topping.objects.create(title="Без топпинга", price=0)
            Topping.objects.create(title="Белый соус", price=200)
            Topping.objects.create(title="Карамельный", price=180)
            Topping.objects.create(title="Кленовый", price=200)
            Topping.objects.create(title="Черничный", price=300)
            Topping.objects.create(title="Молочный шоколад", price=350)
            Topping.objects.create(title="Клубничный", price=200)

            # Создание ягод
            Berry.objects.create(title="Ежевика", price=400)
            Berry.objects.create(title="Малина", price=300)
            Berry.objects.create(title="Голубика", price=450)
            Berry.objects.create(title="Клубника", price=500)

            # Создание декора
            Decor.objects.create(title="Фисташки", price=300)
            Decor.objects.create(title="Безе", price=400)
            Decor.objects.create(title="Фундук", price=350)
            Decor.objects.create(title="Пекан", price=300)
            Decor.objects.create(title="Маршмеллоу", price=200)
            Decor.objects.create(title="Марципан", price=280)

            cake_captions = [
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "С Днём Рождения!",
                "Люблю тебя!",
                "Сладкая жизнь",
                "Счастья и радости!",
                "Всегда вместе",
                "Лучший день!",
                "С юбилеем!",
                "Дорогой маме",
                "Вечная любовь",
                "На долгую память",
            ]

            levels = list(Level.objects.all())
            forms = list(Form.objects.all())
            toppings = list(Topping.objects.all())
            berries = list(Berry.objects.all())
            decors = list(Decor.objects.all())

            for i in range(10):
                level = random.choice(levels)
                form = random.choice(forms)
                topping = random.choice(toppings)
                berry = random.choice(berries)
                decor = random.choice(decors)
                caption = random.choice(cake_captions)
                Cake.objects.create(
                    price=level.price
                    + form.price
                    + topping.price
                    + berry.price
                    + decor.price,
                    level=level,
                    form=form,
                    topping=topping,
                    berry=berry,
                    decor=decor,
                    caption=caption,
                )

            addresses = [
                "Москва, Тверская, 21, кв. 23",
                "Москва, Краснопресненская, 46, кв. 355",
                "Люберцы, Октябрьский проспект, 101, кв. 123",
                "Химки, Калинина, 4А, кв. 145",
                "Одинцово, Маршала Жукова, 46, кв. 299"
            ]
            comments = [
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "Не забудьте позвонить!",
                "Ещё надо будет сигареты купить. Позвоните перед доставкой пж.",
                "Набрать за час до приезда. В дверь постучать 3 раза"
            ]
            # Создание заказов
            cakes = Cake.objects.all()
            clients = list(Client.objects.all())
            
            invoice_statuses = [1, 2, 3, 4]
            order_statuses = [1, 2, 3]
            for cake in cakes:
                client = random.choice(clients)
                address = random.choice(addresses)
                receipt_id = random.randint(100, 999)
                receipt = f"https://receipt.com/id={receipt_id}"
                day = random.randint(1, 24)
                date = f"2025-02-{day:02d}"
                hour = random.randint(9, 17)
                minute = random.randint(1, 59)
                time = f"{hour:02d}:{minute:02d}"
                delivery_date = f"2025-03-{day+1:02d}"
                delivery_time = f"{hour:02d}:00"

                invoice_status = random.choice(invoice_statuses)
                invoice = Invoice.objects.create(
                    status=invoice_status,
                    receipt=receipt,
                    amount=cake.price
                )
                order_status = random.choice(order_statuses)
                if invoice_status == 3:
                    order_status = 4    
                Order.objects.create(
                    status=order_status,
                    date=date,
                    time=time,
                    client=client,
                    cake=cake,
                    delivery_date=delivery_date,
                    delivery_time=delivery_time,
                    delivery_address=address,
                    invoice=invoice,
                    comment=random.choice(comments)
                )
            self.stdout.write(
                self.style.SUCCESS("Тестовые данные успешно загружены в бд")
            )
