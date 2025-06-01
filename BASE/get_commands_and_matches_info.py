import requests


# функция получения трех словарей - с информацией о команде по id(участники, победы, поражения, забитые голы, пропущенные), 
# с id команды по имени, с командами и их соперниками в разных матчах
def get_commands_and_matches_info(AUTH_TOKEN:dict,URL:str) -> tuple:
    dict_of_commands__id_to_info = {}
    dict_of__commands__name_to_id = {}

    dict_of_matches = {}


    # перебераем все команды и паралельно напалняем словарь с матчами пустыми массивами для дальнейшего заполнения соперниками
    for i in requests.get(f"{URL}/teams", headers=AUTH_TOKEN).json():
        dict_of_commands__id_to_info[i.get("id")] = {"players" : i.get("players"), "wins": 0, "losses": 0,"score": 0, "miss": 0}
        dict_of__commands__name_to_id[i.get("name")] = i.get("id")
        dict_of_matches[i.get("id")] = []


    # заполняем поля выигрышей и поражений для каждой команды, заполняем соперников в матчах для каждой команды
    for i in requests.get(f"{URL}/matches", headers=AUTH_TOKEN).json():
        dict_of_commands__id_to_info[i.get("team1")]["score"] += i.get("team1_score")
        dict_of_commands__id_to_info[i.get("team1")]["miss"] += i.get("team2_score")

        dict_of_commands__id_to_info[i.get("team2")]["score"] += i.get("team2_score")
        dict_of_commands__id_to_info[i.get("team2")]["miss"] += i.get("team1_score")


        if i.get("team1_score") > i.get("team2_score"):
            dict_of_commands__id_to_info[i.get("team1")]["wins"] += 1
            dict_of_commands__id_to_info[i.get("team2")]["losses"] += 1

        elif  i.get("team1_score") < i.get("team2_score"):
            dict_of_commands__id_to_info[i.get("team2")]["wins"] += 1
            dict_of_commands__id_to_info[i.get("team1")]["losses"] += 1


        dict_of_matches[i.get("team1")].append(i.get("team2"))
        dict_of_matches[i.get("team2")].append(i.get("team1"))


    return dict_of_commands__id_to_info, dict_of__commands__name_to_id, dict_of_matches
