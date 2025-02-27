# Generated by Django 5.1.6 on 2025-02-27 18:44

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('short_url', models.URLField(blank=True, verbose_name='Сокращенная ссылка')),
                ('visits_number', models.IntegerField(default=0, verbose_name='Количество визитов')),
            ],
            options={
                'verbose_name': 'Рекламная ссылка',
                'verbose_name_plural': 'Рекламные ссылки',
            },
        ),
        migrations.CreateModel(
            name='Berry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название ягоды')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Ягода для торта',
                'verbose_name_plural': 'Ягоды для торта',
            },
        ),
        migrations.CreateModel(
            name='Decor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название декора')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Декор для торта',
                'verbose_name_plural': 'Декоры для торта',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название формы')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Форма для торта',
                'verbose_name_plural': 'Формы для торта',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(1, 'Ожидает оплаты'), (2, 'Оплачено'), (3, 'Отменено')], default='waiting', max_length=14, verbose_name='Статус счета')),
                ('receipt', models.URLField(blank=True, null=True, verbose_name='Чек')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Счёт выставлен')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('amount', models.FloatField(verbose_name='Сумма чека')),
            ],
            options={
                'verbose_name': 'Счет на оплату',
                'verbose_name_plural': 'Счета на оплату',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название уровня')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Размер/уровень для торта',
                'verbose_name_plural': 'Размеры/уровни для торта',
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название топпинга')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Топпинг для торта',
                'verbose_name_plural': 'Топпинги для торта',
            },
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', unique=True, verbose_name='Номер телефона')),
                ('full_name', models.CharField(blank=True, max_length=200, verbose_name='ФИО')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Цена торта')),
                ('caption', models.CharField(blank=True, max_length=200, null=True, verbose_name='Надпись на торте')),
                ('berry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.berry', verbose_name='Ягода')),
                ('decor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.decor', verbose_name='Декор')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.form', verbose_name='Форма торта')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.level', verbose_name='Количество уровней торта')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.topping', verbose_name='Топпинг')),
            ],
            options={
                'verbose_name': 'Торт',
                'verbose_name_plural': 'Торты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(1, 'Принят'), (2, 'В доставке'), (3, 'Выполнен'), (4, 'Отменен')], default=1, max_length=9, verbose_name='Статус заказа')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата заказа')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='Время заказа')),
                ('delivery_date', models.DateField(verbose_name='Дата доставки')),
                ('delivery_time', models.TimeField(verbose_name='Время доставки')),
                ('delivery_address', models.TextField(blank=True, max_length=200, null=True, verbose_name='Адрес доставки')),
                ('comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='Комментарий для курьера')),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.cake', verbose_name='Торт')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='app.invoice', verbose_name='Счет на оплату')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
