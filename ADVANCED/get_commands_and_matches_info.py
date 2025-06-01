import requests
import aiohttp
import asyncio


# функция получения трех словарей - с информацией о команде по id(участники, победы, поражения, забитые мячи, пропущенные, противники, матчи в которых играла комнада), 
# с id команды по имени
def get_commands_and_matches_info(AUTH_TOKEN:dict, URL:str) -> tuple:
    dict_of_commands__id_to_info = {}
    dict_of_commands__name_to_id = {}


    # перебераем все команды, добавляем в удобный словарь, указываем параметры
    for i in requests.get(f"{URL}/teams", headers=AUTH_TOKEN).json():
        dict_of_commands__id_to_info[i.get("id")] = {
            "players" : i.get("players"), # id игроков, играющих за команду
            "wins": 0, #победы в матчах 
            "losses": 0, #проигрыши в матчах
            "score": 0, #забитые мячи 
            "miss": 0,#пропущенные мячи 
            "rivals": [], #соперники в разных матчах 
            "matches" : [] #id матчей, в которых играла команда
        }
        
        dict_of_commands__name_to_id[i.get("name")] = i.get("id")


    # заполняем поля командам, проходясь по матчам
    for i in requests.get(f"{URL}/matches", headers=AUTH_TOKEN).json():

        # заполняем забитые и пропущенные мячи 
        dict_of_commands__id_to_info[i.get("team1")]["score"] += i.get("team1_score")
        dict_of_commands__id_to_info[i.get("team1")]["miss"] += i.get("team2_score")

        dict_of_commands__id_to_info[i.get("team2")]["score"] += i.get("team2_score")
        dict_of_commands__id_to_info[i.get("team2")]["miss"] += i.get("team1_score")


        # заполняем победы и поражения
        if i.get("team1_score") > i.get("team2_score"):
            dict_of_commands__id_to_info[i.get("team1")]["wins"] += 1
            dict_of_commands__id_to_info[i.get("team2")]["losses"] += 1

        elif  i.get("team1_score") < i.get("team2_score"):
            # заполняем победы и поражения
            dict_of_commands__id_to_info[i.get("team2")]["wins"] += 1
            dict_of_commands__id_to_info[i.get("team1")]["losses"] += 1


        # заплняем противников 
        dict_of_commands__id_to_info[i.get("team1")]["rivals"].append(i.get("team2"))
        dict_of_commands__id_to_info[i.get("team2")]["rivals"].append(i.get("team1"))


        # заполняем матчи в которых играла команда 
        dict_of_commands__id_to_info[i.get("team1")]["matches"].append(i.get("id"))
        dict_of_commands__id_to_info[i.get("team2")]["matches"].append(i.get("id"))


    return dict_of_commands__id_to_info, dict_of_commands__name_to_id


# функция плучения всех матчей, в которых играла определенная команда
# используем асинхронную функцию для того, чтобы все было красиво и быстро т.к нужно будет отправить относительно много запросов
async def commands_matches(AUTH_TOKEN:dict,COMAND_ID:int,DICT_OF_COMMANDS__ID_TO_INFO:dict,URL:str) -> dict:

    # функция получения информации о матче по id матча
    async def get_match_info(session,index,sem):
        while True:
           async with sem:
               async with session.get(url = f"{URL}/goals?match_id={index}", headers = AUTH_TOKEN) as response:
                   if response.status == 200:
                        answer = await response.json()
                        return {index: answer}
                   else:
                       continue

    # открываем ссэссию и формируем задачи
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(10)

        tasks = []
        for i in DICT_OF_COMMANDS__ID_TO_INFO[COMAND_ID]["matches"]:
            tasks.append(get_match_info(session,i,sem))

        # асинхронно выполняем все задачи
        answers = await asyncio.gather(*tasks)


        # конвертируем результат в удобный словарь 
        result = {}

        for i in answers:
            result.update(i)


        return result