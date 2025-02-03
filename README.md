## Описание проекта

Account change — это Backend-часть программы электронного кошелька. 

Он разработан с использованием Django и Django REST Framework. 

## Требования

- Python 3.11
- PostgreSQL
- Redis

## Установка
1. Клонируйте репозиторий: https://github.com/RamilNigamatulin/account_change.git
2. Создайте виртуальное окружение и активируйте его:
    ```
    python -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
3. Переименуйте файл ".env.sample" в ".env" и заполните его.
Для генерации SECRET_KEY введите в консоль команду: 
    ```
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```
4. Установите зависимости командой: 
    ```
    pip install -r requirements.txt
    ```
5. Запустите проект:
    ```
    python manage.py runserver
    ```
6. Для тестирования проекта возможно использование подготовленных фикстур, для их загрузки введите команду:
    ```
    python manage.py loaddata fixtures/general.json
    ```
    или по отдельности: 
    ```
    python manage.py loaddata fixtures/users.json
    ```
    ```
    python manage.py loaddata fixtures/wallets.json
    ```
- Пароль для всех пользователей 123qwe.
7. Для использования чистой базы и настройки администратора, внесите соответствующие изменения в файл "csu.py" (логин и пароль администратора, по умолчанию "email=admin@example.com, password=123qwe") и введите команду: 
    ```
    python manage.py csu
    ```
   
## Проект подготовлен для упаковки в Docker

Для упаковки и пользования проектом в Docker внесите изменения в настройки файла ".env", после чего введите команду:
```
docker-compose up -d --build
```

Для загрузки подготовленных фикстур в проект введите команду:
```
docker-compose exec app python manage.py loaddata fixtures/general.json
```
либо по отдельности каждую фикстуру: 
```
docker-compose exec app python manage.py loaddata fixtures/users.json
```
```
docker-compose exec app python manage.py loaddata fixtures/wallets.json
```

## Эндпоинты

- **Авторизация и аутентификация**:
  - Регистрация пользователя
    ```
    POST /users/register/
    ``` 
    ```
    {
      "email": "user@example.ru",
      "password": "example"
    }
    ```
  - Получение токена
    ```
    POST /users/token/
    ``` 
    ```
    {
      "email": "user@example.ru",
      "password": "example"
    }
    ```
  - Обновление токена
    ```
    POST /users/token/refresh/
    ```
    ```
    {
      "email": "user@example.ru",
      "password": "example"
    }
    ```
  
- **Сотрудники**:
    CRUD для кошелька
  - Список кошельков
    ```
    GET /wallets/
    ``` 
  - Создание кошелька
    ```
    POST /wallets/create/
    ```
  - Детальная информация о кошельке (баланс)
    ```
    GET /wallets/<uuid:uuid>/
    ```
  - Удаление кошелька
    ```
    DELETE /wallets/<uuid:uuid>//delete/
    ```

- **Операции**:
    CRUD для операции
  - Список операций по кошельку пользователя
    ```
    GET /wallets/operations/<uuid:uuid>/
    ``` 
    - Создание операции (пополнение или перевод)
    ```
    POST /wallets/<uuid:uuid>/operations/
    ``` 
    ```
    {
        "operation_type": "DEPOSIT" or "WITHDRAWAL",
        "amount": 1000.00
    }
    ```
    
- **Тестирование**:
    
  ```
  coverage run --source='.' manage.py test
  ```
  ```
  coverage report -m
  ```
    Тестами покрыто 90% кода