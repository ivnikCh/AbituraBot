# AbituraBot

## Описание
Телеграмм бот для подачи заявлений на поступление в вуз.

## Технологии
- [X] Python
- [X] python-telegram
- [X] Pymongo

## Запуск

Перейдите в директорию ```src```

```cd src```

Зайдите в @BotFather в телеграмме, получите токен. Создайте файл:

```echo 'MY_TOKEN = "<токен который вы получили у бота>"' > gen_token.py```

Запустите базу данных:
```
docker pull mongodb/mongodb-community-server:latest

docker run -p 27017:27017 --name mongodb1 -d mongodb/mongodb-community-server:latest
```
Введите:
```python3 -m main```

## Запуск тестов:
```pip3 install poetry```


```poetry init```

```poetry run pytest —cov```

### Покрытие тестов:

application_test.py ...                                                  [ 20%]

process_test.py .......                                                  [ 66%]

router_test.py ..                                                        [ 80%]

user_test.py ...                                                         [100%]

## Управление

```/help``` - список команд

```/start``` - запустит интерфейс регистрации

```/cancel``` - отменит текущую операцию

```/add``` - подать документы на программу

```/show_apps``` - покажет список всех поданных заявок и их статусы (каждое из заявлений можно будет отозвать ```\delete```)

## Архитектура
### Классы
  * ``` Application ``` - класс для хранения каждого заявления
  * ``` User ``` - класс для хранения информации о каждом пользователе
  * ```Router``` -  операции с БД
  * ```Process``` - обработка команд
### Наполнение классов

### Application
  ##### Поля
    pass_id: str - паспорт
    snils_id: str - снилс
    id_app: str - уникальный номер заявления
    url_docs: str - ссылка на гугл диск с документами
    name_program: str - название программы на котрую было подано заявление
    is_bvi: bool - конкурсная группа
    count_ege: int - сумма балов егэ
    state: str - статус заявления
    comment: str - комментарий проверяющего
  ##### Методы
    to_str() -> str - преобразует к строке все поля класса и выведет читабельным текстом
    
    static
    to_json(ob: Application) -> dict - вернёт словарь из полей класса

    static
    from_json(data: dict) -> Application - преобразует словарь из полей класса в класс с этими полями

    
### User
  ##### Поля
    user_id: str - тег пользователя
    apps: List[Application] - поданные заявки
  ##### Методы
    to_str() -> str - вернет список всех заявок
    
    static
    to_json(ob: Application) -> dict - вернёт словарь из полей класса

    static
    from_json(data: dict) -> Application - преобразует словарь из полей класса в класс с этими полями

### Router(telegram.ext.BasePersistence)
  ##### Поля
    mongo_db: pymongo.database.Database
  #### Методы
    get_users() -> {int : user} - возвращает User всех пользователей.
    update_users(user_id: int, data: User) -> None - обновляет в бд данные для user_id.
    update_conversations() -> None - обновляет бд telegram.ext.ConversationHandler.

### Process
  #### Методы
    help  - обрабатывает команду /help.
    start - обрабатывает команду /start
    cancel - обрабатывает команду /cancel
    application - обрабатывает команду /add
    show_app - обрабатывает команду /show_apps
