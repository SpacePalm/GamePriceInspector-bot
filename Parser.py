import requests
import LoggerFile
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Event
from bs4 import BeautifulSoup


CSV = "games.csv"
HOST = "https://hot-game.info"
URL = "https://hot-game.info/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
}
gamelist = []
fulllist = []
event = Event()


def ConvertTitle(games):
    games = games.title()
    games = games.replace(" ", "")
    games = games.replace("-", "")
    games = games.replace(":", "")
    games = games.replace("\n", "")
    return games

def ConvertTitleList(games):
    list = []
    games = games[0].split("/")
    for i in games:
        i = i.title()
        i = i.replace(" ", "")
        i = i.replace("-", "")
        i = i.replace(":", "")
        i = i.replace("\n", "")
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
        games.append(
            {
                "title": item.find("div", class_= "game-title").get_text(strip = True),
                "product_link": HOST + item.find("div", class_="game-title").find("a").get("href")
            }
        )
    return games


def GetLastPage(html):
    soup = BeautifulSoup(html, "html.parser")
    lpage = soup.find("div", class_="pagination").find("span", class_ = "last").find("a", class_ = "arrow last").get_text()
    return int(lpage)


def GamePrice(l,f):
    LoggerFile.logger.info("GamePrice started")
    pricelist = []
    for i in l:
        for j in f:
            a = ConvertTitle(j["title"])
            if a.count(i) == 1:
                h = GetHtml(j["product_link"])
                soup = BeautifulSoup(h.text, "html.parser")
                items = soup.find_all("div", class_="price-list-item")
                g = []

                for item in items:
                    g.append( {
                            "shop_title": item.find("div", class_="price-col-1").find("img").get("title"),
                            "link": item.find("div", class_="hidden-link2").get("data-href"),
                            "price": item.find("div", class_="price-col-3").find("div",class_="game-price").get_text().replace("купить\n", "")
                        })
                pricelist.append([j["title"], g])
    return pricelist



def ParserF():
    html = GetHtml(URL)
    PAGENATION = GetLastPage(html.text)
    if html.status_code == 200:
        games=[]
        LoggerFile.logger.info(f"Parsing page {1}")
        html = GetHtml(URL)
        games.extend(GetContent(html.text))
        LoggerFile.logger.info("Done")
        for page in range(2,PAGENATION + 1):
            LoggerFile.logger.info(f"Parsing page {page}")
            html = GetHtml(URL+str(page))
            games.extend(GetContent(html.text))
            with open("Filllist.json", "w") as file:
                json.dump(games,file,indent=5)
                file.close()
        LoggerFile.logger.info("Done")
    else:
        LoggerFile.logger.error("Error")

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        LoggerFile.logger.info("File has been changed")
        with open("JsonList.json", "r") as f:
            gamelist = json.load(f)
            f.close()

        gamelist = ConvertTitleList(gamelist)
        with open("Filllist.json", "r") as file:
            fulllist = json.load(file)
            file.close()
        result = GamePrice(gamelist,fulllist)
        with open("GameInfo.json", "w") as file:
            json.dump(result, file, indent=5)
        LoggerFile.logger.info("Get a result")

observer = Observer()
observer.schedule(Handler(), path='/Users/daniilmurasov/PycharmProjects/Try/JsonList.json', recursive=True)
observer.start()

while True:
    LoggerFile.logger.info("Parser starts")
    #ParserF()
    event.wait(timeout=86400)





