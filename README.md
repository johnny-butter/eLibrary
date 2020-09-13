# eLibrary

Online book store project. Visit it [eLibrary](https://elibrary-2019.herokuapp.com).

## Features

- Register / Login through `Facebook` account
- Register / Login through `Gmail` account
- Search books by keyword
- Sort books by specific column
- Add books to favorite list
- Add books to cart
- Buy books by credit card (`Braintree sandbox`)
- Send shopping record email
- Support i18n (`en` / `ja` / `zh-tw`)

## Tools

- `django`: api / frontend server
- `djangorestframework`: build api
- `mysql`: database
- `celery`: execute distributed tasks
- `redis`: distributed tasks broker
- `rollbar`: trace unexpected error
- `herku`: app server
- `braintree`: **sandbox environment** for using credit card

## Start Project

- Install Python packages

```shell
pip3 install -r requirements.txt
```

- Databse migrate

```shell
python3 manage.py migrate
```

- Collect Static files

```shell
python3 manage.py collectstatic
```

- Start server (local)

```shell
python3 manage.py runserver
```

- Start server (prod)

```shell
gunicorn --timeout=30 --workers=4 eLibrary.wsgi:application
```

## Unittest

```shell
python3 manage.py test
```

## Test Account

- Normal user
  - account: `test_guest`
  - password: `test_guest`
- `Braintree` credit card for test
  - card number: `4111 1111 1111 1111`
  - expiration date: `02/22`
