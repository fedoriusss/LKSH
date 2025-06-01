## Инструкция 

1. Запустите main.py.
2. после вывода в консоль приведенного ниже лога можете отправлять запросы на следующие эндпоинты:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

- /stats?team_name=<name> - статистика команды

- /versus?player1_id=<id>&player2_id=<id> - информация о противостоянии игроков

- /goals?player_id=<id> - возвращает список всех голов игрока, указывая матч и минуту

- /front/stats - html представление /stas

- /front/versus - html представление /versus

- /openapi - cхема проекта

- /redoc - документация проекта