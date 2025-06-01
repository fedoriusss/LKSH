OPEN_API= {
    "openapi": "3.0.3",
    "info": {
        "title": "LKSH Football Statistics API",
        "version": "1.0.0",
        "description": "API для получения футбольной статистики, создал Фёдор Краснов для поступления в ЛКШ"
    },
    "components": {
        "securitySchemes": {
            "AuthToken": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Токен авторизации для доступа к API. Должен передаваться в заголовке Authorization."
            }
        }
    },
    "security": [{"AuthToken": []}],
    "paths": {
        "/stats": {
            "get": {
                "summary": "Получить статистику команды",
                "description": "Возвращает базовую статистику команды по её названию",
                "security": [{"AuthToken": []}],
                "parameters": [
                    {
                        "name": "team_name",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "Название команды (регистрозависимое)"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешный ответ со статистикой команды",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "wins": {
                                            "type": "integer",
                                            "description": "Количество побед команды"
                                        },
                                        "losses": {
                                            "type": "integer",
                                            "description": "Количество поражений команды"
                                        },
                                        "difference": {
                                            "type": "integer",
                                            "description": "Разница между забитыми и пропущенными мячами"
                                        }
                                    },
                                    "required": ["wins", "losses", "difference"]
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Команда не найдена"
                    }
                }
            }
        },
        "/versus": {
            "get": {
                "summary": "Получить количество матчей между игроками",
                "description": "Возвращает количество матчей, в которых участвовали два указанных игрока",
                "security": [{"AuthToken": []}],
                "parameters": [
                    {
                        "name": "player1_id",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "format": "int32",
                            "minimum": 1
                        },
                        "description": "ID первого игрока"
                    },
                    {
                        "name": "player2_id",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "format": "int32",
                            "minimum": 1
                        },
                        "description": "ID второго игрока"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Количество матчей между игроками",
                        "content": {
                            "application/json": {
                                "schema": {"type": "integer"}
                            }
                        }
                    },
                    "400": {
                        "description": "Некорректные данные"
                    },
                    "404": {
                        "description": "Один из игроков не найден"
                    }
                }
            }
        },
        "/goals": {
            "get": {
                "summary": "Получить информацию о голах игрока",
                "description": "Возвращает список голов, забитых указанным игроком",
                "security": [{"AuthToken": []}],
                "parameters": [
                    {
                        "name": "player_id",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "format": "int32",
                            "minimum": 1
                        },
                        "description": "ID игрока"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Список голов игрока",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "match": {
                                                "type": "integer",
                                                "description": "ID матча, в котором был забит гол"
                                            },
                                            "time": {
                                                "type": "integer",
                                                "description": "Минута матча, на которой был забит гол"
                                            }
                                        },
                                        "required": ["match", "time"]
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Игрок не найден"
                    }
                }
            }
        },
        "/front/stats": {
            "get": {
                "summary": "HTML страница статистики команды",
                "description": "Возвращает HTML страницу для просмотра статистики команды",
                "responses": {
                    "200": {
                        "description": "HTML страница",
                        "content": {
                            "text/html": {
                                "schema": {"type": "string"}
                            }
                        }
                    }
                }
            }
        },
        "/front/versus": {
            "get": {
                "summary": "HTML страница сравнения игроков",
                "description": "Возвращает HTML страницу для просмотра матчей между игроками",
                "responses": {
                    "200": {
                        "description": "HTML страница",
                        "content": {
                            "text/html": {
                                "schema": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
}