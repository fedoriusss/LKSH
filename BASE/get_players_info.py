import aiohttp
import asyncio
from aiolimiter import AsyncLimiter


# фукнция получения максимального id игрока(отправляем запрос на получения команд и ишем в них самый максимальный id игрока)
async def get_max_player_id(AUTH_TOKEN:dict, URL:str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url = f"{URL}/teams", headers = AUTH_TOKEN) as response:
            answer = await response.json()

            maximum = 0 
            for i in answer:
                if max(list(i.get("players"))) > maximum:
                    maximum = max(list(i.get("players")))
            return maximum
        

# функция получения имен игроков в порядке возрастания id 
async def get_all_players(max:int,AUTH_TOKEN:dict, URL:str) -> list:

    # устанавливаем лимит, чтобы избежать ошибки 429
    limiter = AsyncLimiter(50,1) 

    # функция получения фамилии и имени каждого игрока по id
    async def get_player(session,index,sem,URL):   
            # отправляем запрос в цикле, чтобы при ошибке повторялся запрос
            while True:
                async with limiter:
                    async with sem:
                        async with session.get(url = f"{URL}/players/{index}", headers = AUTH_TOKEN) as response:
                            if response.status == 200:
                                answer = await response.json()
                                return  f"{answer.get("name")} {answer.get("surname")}"
                            else:
                                continue
                

    # открываем ссэссию и формируем задачи
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(10)

        tasks = []
        for i in range(1,max+1):
            tasks.append(get_player(session,i,sem,URL))

        # асинхронно выполняем все задачи
        result = await asyncio.gather(*tasks)


        # выводим отсоритрованных игроков
        for i in sorted(result):
            print(i)


        # возвращаем список всех игроков в порядке возрастания id
        return result
