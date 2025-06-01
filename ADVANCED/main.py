from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from pathlib import Path
import requests
import asyncio



# функции из других файлов 
# функция получения максимального id игрока
from get_max_player_id import get_max_player_id
# функция получения информации о командах и матчах
from get_commands_and_matches_info import get_commands_and_matches_info, commands_matches
# OpenAPI схема
from open_api_scheme import OPEN_API



# корневая дерриктория, куда отправлять запросы 
URL = "https://lksh-enter.ru"


#заголовок для авторизации, его передаем в каждом запросе
AUTH_TOKEN = {
    "Authorization": "30942b654d7081e119892445cfd2c1ec440fd430b62c15001bf35af42c9f0af8"
}


# логинимся в системе, для получения дополнительного эндпоинта
requests.post(f"{URL}/login",json = {"reason": 'I strive for perfection and "LKSH" is one of the roads to it.'}, headers=AUTH_TOKEN)



# максимальный id игрока для будущих провервок
max_player_id = get_max_player_id(AUTH_TOKEN,URL)

#словарь с информацией о команде по id, словарь для получения названия команды по id 
dict_of_commands__id_to_info,\
dict_of_commands__name_to_id = get_commands_and_matches_info(AUTH_TOKEN,URL)



app = FastAPI()



# ТОЛЬКО ДЛЯ ТОГО, ЧТОБЫ РАБОТАЛО НА ЛОКАЛЬНОМ ПОДКЛЮЧЕНИИ, ИНАЧЕ БУДЕТ ОШИБКА В js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# обрабатываем запрос на статистику команды 
@app.get(f"/stats")
def stats(team_name:str):
    # проверяем, существует ли команда
    if team_name in dict_of_commands__name_to_id.keys():
        command_id = dict_of_commands__name_to_id[team_name]


        # разность между забитыми мячами и пропушенными
        difference = dict_of_commands__id_to_info[command_id]["score"] - dict_of_commands__id_to_info[command_id]["miss"]


        # формируем результат
        result = {
            "wins": dict_of_commands__id_to_info[command_id]["wins"],
            "losses" : dict_of_commands__id_to_info[command_id]["losses"],
            "difference" : difference
        }


        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"message": "Command Not Found"}, status_code=404)
    
    

# обрабатываем запрос о кол-ве мачей с игроками 
@app.get(f"/versus")
def versus(player1_id:int,player2_id:int):
    # проверяем, существуют ли игроки и коректны ли данные
    if player1_id == player2_id:
        return JSONResponse(content={"message": "Incorect data, the player IDs must be different"}, status_code=400)

    elif  0<player1_id<=max_player_id and 0<player2_id<=max_player_id:
        # узнаем id команд игроков
        for i in dict_of_commands__id_to_info:
            if player1_id in dict_of_commands__id_to_info[i]["players"]:
                command_player_1 = i 
            

            elif  player2_id in dict_of_commands__id_to_info[i]["players"]:
                command_player_2 = i


        # проходимся по всем соперникам в матчах, когда играла команда первого игрока
        result = 0 

        for i in dict_of_commands__id_to_info[command_player_1]["rivals"]:
            if i == command_player_2:
                result += 1


        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"message": "Players Not Found"}, status_code=404)


# ифнормация о голах конкретного игрока 
@app.get(f"/goals")
def goals(player_id:int):
    # проверяем, существуют ли игроки
    if  0<player_id<=max_player_id:
        # определяем команду игрока
        for i in dict_of_commands__id_to_info:

            if player_id in dict_of_commands__id_to_info[i]["players"]:
                player_command = i


        # список информации о матчах, в которых играла команда игрока
        list_of_Matches = asyncio.run(commands_matches(AUTH_TOKEN,player_command,dict_of_commands__id_to_info, URL))


        # проходимся по list_of_Matches и ищем матч, в котором игрок забил гол
        result = []

        for i in list_of_Matches:
            for j in list_of_Matches[i]:

                if j["player"] == player_id:
                    result.append(
                        {
                            "match": i,
                            "time": j["minute"],
                        }
                    )


        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"message": "Player Not Found"}, status_code=404)



# получение статистики команды ввиде html страницы
@app.get(f"/front/stats")
def stat_html():
    # путь до файла 
    file_path = Path(__file__).parent / "htmls" / "stats.html"
    return FileResponse(file_path)



# сравнение игроков ввиде html страницы
@app.get(f"/front/versus")
def stat_html():
    # путь до файла 
    file_path = Path(__file__).parent / "htmls" / "versus.html"
    return FileResponse(file_path)



# получение OpenAPI схемы
@app.get(f"/openapi")
def openapi():
    return JSONResponse(content=OPEN_API, status_code=200)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)