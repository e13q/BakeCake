Создать .env:
```
VK_TOKEN = "***"
SECRET_KEY = top_secret_code
DEBUG = True
```

Последовательный запуск команд:
```
py manage.py makemigrations
```

```
py manage.py migrate
```

```
py manage.py createsuperuser
```

```
py manage.py runserver
```
