from operator import sub
import re
from requests_html import HTMLSession
import json


url = "https://dnd.su/spells/"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"
}


spellData = {}


# .card__group-0 > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > span:nth-child(1)
def main(links):
    global spellData
    del spellData

    spellData = {}

    for i in range(1, 10):
        spellData[str(i)] = {}
    spellData["Заговор"] = {}
    for link in links:
        link = link.strip()
        session = HTMLSession()
        response = session.get(link)
        response.html.render(sleep=1 / 100)
        # print(f"|{str(link).center(80)}|", end="")
        name = (
            response.html.find(".cards-wrapper", first=True)
            .find(".card-title > span:nth-child(1)", first=True)
            .text
        )
        spellInfo = response.html.find(".cards-wrapper", first=True).find(
            ".params", first=True
        )
        level, school = spellInfo.find("li.size-type-alignment", first=True).text.split(
            ", ", 1
        )
        level = level.replace(" уровень", "")
        description = spellInfo.find("li.subsection", first=True).text

        spellInfo = spellInfo.find("li")[1:-1]
        classes = []
        subclasses = []
        for el in spellInfo:
            el = el.text
            sep = el.find(":")
            match el[:sep]:
                case "Время накладывания":
                    casting_time = el[sep + 2 :]
                case "Дистанция":
                    distance = el[sep + 2 :]
                case "Компоненты":
                    components = re.findall(r"[ВСМ] ?(?:\(.*\))?", el[sep + 2 :])
                case "Длительность":
                    duration = el[sep + 2 :]
                case "Классы":
                    classes = el[sep + 2 :].split(", ")
                case "Подклассы":
                    subclasses = el[sep + 2 :].split(", ")

        spellData[level][name] = {
            "name": name,
            "level": level,
            "school": school,
            "casting_time": casting_time,
            "distance": distance,
            "components": components,
            "duration": duration,
            "classes": classes,
            "subclasses": subclasses,
            "description": description,
        }
        # print("<success>".center(20))
    del name
    del spellInfo
    del level
    del school
    del description
    del classes
    del subclasses
    del casting_time
    del distance
    del components
    del duration
    return spellData


def openFile():
    with open("OtherPyFiles/spells.txt", "r") as file:
        return file.readlines()


def jsonOpen():
    with open("OtherPyFiles/spells.json", "r+", encoding="utf-8") as file:
        return json.load(file)


def saveFile(data):
    oldData = jsonOpen()
    for _level in data:
        for _spell in data[_level]:
            # print(_level, _spell)
            oldData[_level][_spell] = data[_level][_spell]
    with open("OtherPyFiles/spells.json", "w", encoding="utf-8") as file:
        json.dump(oldData, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # last been 220-warding-bond = 140 line
    sl = 131
    links = openFile()
    for i in range(81, sl):
        spD = main(links[i * len(links) // sl : len(links) // sl * (i + 1)])
        saveFile(spD)

    # thread2.start()
    # thread3.start()
