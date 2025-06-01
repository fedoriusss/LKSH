import asyncio

# функции из других файлов 
# функции для получения информации об игроках 
from get_players_info import get_max_player_id
from get_players_info import get_all_players
# функция для получения информации о командах и матчах
from get_commands_and_matches_info import get_commands_and_matches_info



# корневая дерриктория, куда отправлять запросы 
URL = "https://lksh-enter.ru"


#заголовок для авторизации, его передаем в каждом запросе
AUTH_TOKEN = {
    "Authorization": "30942b654d7081e119892445cfd2c1ec440fd430b62c15001bf35af42c9f0af8"
}



# список всех игроков в порядке возрастания id                                          
LIST_OF_PLAYERS = asyncio.run(get_all_players(asyncio.run(get_max_player_id(AUTH_TOKEN,URL)),AUTH_TOKEN,URL))

#словарь с информацией о команде по id, словарь с получением id по имени, словарь с командами и их соперниками в разных матчах
DICT_OF_COMMANDS__ID_TO_INFO,\
DICT_OF__COMMANDS__NAME_TO_ID,\
DICT_OF_MATCHES = get_commands_and_matches_info(AUTH_TOKEN,URL)



# функция, позволяющая бесконечно спрашивать и обрабатывать запросы у пользователя
def query_cycle():
    # строка ввода для пользователя
    USER_REQUEST = input()



    # обрабатываем запрос на статистику команды 
    if  USER_REQUEST[0:6]== "stats?":

        try:
            name_of_command = USER_REQUEST[7:].split('"')[1]

            # проверяем, существует ли команда
            if name_of_command not in DICT_OF__COMMANDS__NAME_TO_ID.keys():
                print("0 0 0")

            else:
                command_id = DICT_OF__COMMANDS__NAME_TO_ID[name_of_command] # id команды

                # разность между забитыми голами и пропушенными
                difference = DICT_OF_COMMANDS__ID_TO_INFO[command_id]["score"] - DICT_OF_COMMANDS__ID_TO_INFO[command_id]["miss"]

                # ставим знак перед разницей
                if difference>0:
                    difference = f"+{difference}"

                print(f"{DICT_OF_COMMANDS__ID_TO_INFO[command_id]["wins"]} {DICT_OF_COMMANDS__ID_TO_INFO[command_id]["losses"]} {difference}")
        except:
            print("0 0 0")




    # обрабатываем запрос о кол-ве мачей с игроками 
    elif USER_REQUEST[0:7] == "versus?":
        try:
            player_id_1, player_id_2 = map(int, USER_REQUEST[8:].split())

            # проверяем, существуют ли игроки
            if  0<player_id_1<=len(LIST_OF_PLAYERS) and 0<player_id_2<=len(LIST_OF_PLAYERS):

                command_player_1 = 0
                command_player_2 = 0

                # узнаем id команд игроков
                for i in DICT_OF_COMMANDS__ID_TO_INFO:
                    if player_id_1 in DICT_OF_COMMANDS__ID_TO_INFO[i]["players"]:
                        command_player_1 = i 
                    elif  player_id_2 in DICT_OF_COMMANDS__ID_TO_INFO[i]["players"]:
                        command_player_2 = i


                # проходимся по всем соперникам в матчах, когда играла команда первого игрока
                colvo = 0 

                for i in DICT_OF_MATCHES[command_player_1]:
                    if i == command_player_2:
                        colvo += 1

                print(colvo)

            else:
                print(0)
        except:
            print(0)


    query_cycle()


query_cycle()