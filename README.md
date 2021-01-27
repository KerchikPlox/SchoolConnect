# Лекционный пример

## Запуск
### Запуск через командную строку:
Находясь в директории проекта:

`uvicorn main:app --reload --port 8083 --host "0.0.0.0"`

### Запуск из редактора
Запустить `main.py`

### Запуск с помощью `Docker` / `docker-compose`

`docker-compose up -d postgres`

ждать секунд 15-20

`docker-compose up -d main_app`

 