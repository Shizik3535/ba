# Первое разворачиенвание
Нужно, сделать только в первый раз
## Устаноква зависимостей
```bash
pip install -r t.txt
```

## Работа с бд
Как развернёшь бд надо настроить `.env`
```bash
alembic upgrade head
```


## Запуск локального сервера
```bash
uvicorn app.main:app
```


# Когда будешь делать очередной pull
```bash
pip install -r t.txt
```
```bash
alembic upgrade head
```
```bash
uvicorn app.main:app
```