# eLibrary

Online book store project. Visit it [eLibrary](https://elibrary-2019.herokuapp.com/login/).

## Features

- Register / Login through `Facebook` account
- Register / Login through `Gmail` account
- Search books by keyword
- Sort books by specific column
- Add books to favorite list
- Add books to cart
- Buy books by credit card
- Send shopping record email

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

## Test Account

- Normal user
  - username: `test_guest`
  - password: `test_guest`
- Braintree test credit card
  - card number: `4111 1111 1111 1111`
  - date: `02/22`
