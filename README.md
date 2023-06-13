# Оффлайн-библиотека


## Запуск сервиса

1) Создать файлы с переменными окружения:
    

    1) Для разработки:
    .env
    SECRET_KEY=django-insecure-1=gwsqy1_c!lg2notjoas8&-r(^-1+*$sj9xbfe*mlt^52kfhc
    DEBUG=True
    ALLOWED_HOSTS=
    
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=12345
    POSTGRES_DB=library
    
    DB_HOST=127.0.0.1
    DB_PORT=5432

    2) Для контейнеризации:
    .env.prod
    SECRET_KEY=django-insecure-1=gwsqy1_c!lg2notjoas8&-r(^-1+*$sj9xbfe*mlt^52kfhc
    DEBUG=True
    ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0
    DB_HOST=db
    DB_PORT=5432
    REDIS_HOST=redis
    REDIS_PORT=6379

    .env.db
    POSTGRES_USER=library_user
    POSTGRES_PASSWORD=library
    POSTGRES_DB=library
    

2) Запустить docker-compose
    

    docker-compose up


# REST API

## Get list of Books

### Request

`GET /api/library/books/`


### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 3,
            "title": "Скотный двор",
            "author": "Джордж О́руэлл",
            "amount": 10,
            "in_stock_count": 8,
            "next_return": null
        },
        {
            "id": 4,
            "title": "Война и мир",
            "author": "Лев Толстой",
            "amount": 5,
            "in_stock_count": 1,
            "next_return": null
        }
    ]

## Get list of Readers

### Request

`GET /api/library/readers/`


### Response

    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 1,
            "first_name": "Ivan",
            "last_name": "Petrov",
            "middle_name": "",
            "passport_number": "12345678"
        },
        {
            "id": 2,
            "first_name": "Matia",
            "last_name": "Zaicev",
            "middle_name": "",
            "passport_number": "12345679"
        },
        {
            "id": 3,
            "first_name": "Foo",
            "last_name": "Foo",
            "middle_name": "Foo",
            "passport_number": "11004422"
        }
    ]

## Get list of Items

Список записей с читателями и зарезервированными книгами

### Request

`GET /api/library/items/`


### Response

    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 2,
            "book": 4,
            "current_reader": 2,
            "status": 1
        },
        {
            "id": 9,
            "book": 3,
            "current_reader": 1,
            "status": 1
        }
    ]





## Create a new Reader

### Request

`POST /api/library/readers/`

    Accept: application/json
    
    {
        "first_name": "Foo",
        "last_name": "Foo",
        "middle_name": "Foo",
        "passport_number": "11004422"
    }

### Response

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "id": 3,
        "first_name": "Foo",
        "last_name": "Foo",
        "middle_name": "Foo",
        "passport_number": "11004422"
    }

## Create a new Item

Создание записи о взятии книги пользователем на прочтение

### Request

`POST /api/library/items/`
    
    Accept: application/json
    
    {
        "book": 3,
        "current_reader": 1
    }

### Response

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "id": 9,
        "book": 3,
        "current_reader": 1,
        "status": 1
    }

## Import books from csv file

Импортирует данные о книгах из csv файла в директории ```data``` в корне проекта
    
    Структура строк в csv файле:
        название_книги;имя_автора;жанр;количество_книг
    Например:
        Скотный двор;Джордж О́руэлл;сатира;10
        Война и мир;Лев Толстой;роман;5

### Request

`POST /api/library/import_books/`
    
    Accept: application/json
    
    {
        "filename": "books.csv"
    }

### Response

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {}


## Export statistic about readers

Экспортирует статистику самых активных читателей за последние 30 дней в csv файл

### Request

`GET /api/library/export_reader_report/`

### Response

    HTTP 200 Ok
    Allow: GET, HEAD, OPTIONS
    Content-Disposition: attachment; filename="reader_report.csv"
    Content-Length: 62
    Content-Type: text/csv



## Delete an Item

### Request

`DELETE /thing/id`


### Response

    HTTP 204 No Content
    Allow: DELETE, OPTIONS
    Content-Type: application/json
    Vary: Accept
