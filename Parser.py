import requests
import csv
import LoggerFile
from bs4 import BeautifulSoup


CSV = "games.csv"
HOST = "https://hot-game.info"
URL = "https://hot-game.info/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
}


def ConvertTitle(games):
    games = games.title()
    games = games.replace(" ", "")
    games = games.replace("-", "")
    games = games.replace(":", "")
    games = games.replace("\n", "")
      #а потом идет сравнение с такойже конвертированной строкой и в качестве заголовка оригинальный заголовок
    return games

def ConvertTitleList(games):
    list = []
    for i in games:
        i = i.title()
        i = i.replace(" ", "")
        i = i.replace("-", "")
        i = i.replace(":", "")
        i = i.replace("\n", "")
          #а потом идет сравнение с такойже конвертированной строкой и в качестве заголовка оригинальный заголовок
        list.append(i)
    return list


def GetHtml(url, params = ""):
    r = requests.get(url, headers = HEADERS, params = params)
    return r


def GetContent(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_ = "game-preview")
    games = []

    for item in items:
        if ConvertTitle(item.find("div", class_= "game-title").get_text(strip = True)) in gamelist:
            games.append(
                {
                    "title": item.find("div", class_= "game-title").get_text(strip = True),
                    "product_link": HOST + item.find("div", class_="game-title").find("a").get("href"),
                    "game_image": item.find("a").find("img").get("src")
                }
            )
    return games


def GetLastPage(html):
    soup = BeautifulSoup(html, "html.parser")
    lpage = soup.find("div", class_="pagination").find("span", class_ = "last").find("a", class_ = "arrow last").get_text()
    return int(lpage)


#def SaveContent1(items, path):
#    with open(path, "w", newline= "") as file:
#        writer = csv.writer(file, delimiter= ";")
#        for item in items:
 #           writer.writerow([item["title"], item["game_image"]])


def GetPrice(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="price-list-item")
    pricelist = []
    for item in items:
        pricelist.append(
            {
                "shop_title": item.find("div", class_ = "price-col-1").find("img").get("title"),
                "link": item.find("div", class_ = "hidden-link2").get("data-href"),
                "price": item.find("div", class_ = "price-col-3").find("div", class_ = "game-price").get_text().replace("купить\n", "")

            }
        )
    return pricelist

def GamePrice(games):
    for i in range(len(games)):
        html = GetHtml(games[i].get("product_link"))
        games[i]["Pricelist"] = GetPrice(html.text)
    return games



def ParserF():
    global gamelist
    gamelist = []
    with open("Games.txt", "r") as f:
        for g in f.readlines():
            gamelist.append(g)
    gamelist = ConvertTitleList(gamelist)

    html = GetHtml(URL)
    PAGENATION = GetLastPage(html.text)
    if html.status_code == 200:
        games=[]
        LoggerFile.logger.info(f"Parsing page {1}")
        html = GetHtml(URL)
        games.extend(GetContent(html.text))
        if (len(gamelist) == len(games)):
#           SaveContent1(games, CSV)
            return 0

        for page in range(2,PAGENATION + 1):
            LoggerFile.logger.info(f"Parsing page {page}")
            html = GetHtml(URL+str(page))
            games.extend(GetContent(html.text))
#            SaveContent1(games, CSV)
            if (len(gamelist) == len(games)): break
        games = GamePrice(games)
        LoggerFile.logger.info(games)
        return games
    else:
        LoggerFile.logger.error("Error")
