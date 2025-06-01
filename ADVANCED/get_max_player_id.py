import requests

# фукнция получения максимального id игрока(отправляем запрос на получение команд и ишем в них самый максимальный id игрока)
def get_max_player_id(AUTH_TOKEN:dict,URL:str) -> int:
    answer = requests.get(f"{URL}/teams", headers=AUTH_TOKEN).json()

    maximum = 0 
    for i in answer:
        if max(list(i.get("players"))) > maximum:
            maximum = max(list(i.get("players")))


    return maximum


        
