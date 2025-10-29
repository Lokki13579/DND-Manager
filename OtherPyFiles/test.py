from requests_html import HTMLSession, AsyncHTMLSession

session = HTMLSession()
s2 = HTMLSession()
asyncSession = AsyncHTMLSession()
link = "https://dnd.su/"


def searchinPage(page):
    print(link + page)
    return session.get(link + page)


spellData = {}


def Find(req, string):
    return req.html.find(string, first=True)


def syncSearch(sLink):
    reqs = []
    for ln in sLink:
        reqs.append(s2.get(ln))
    for req in reqs:
        req.html.render(sleep=2)
        name = Find(req, "div.card__header > h2 > span:nth-child(1)").text
        level, school = Find(req, ".size-type-alignment").text.split(", ")
        castingTime = Find(req, ".params > li:nth-child(2)").text.replace(
            "Время накладывания: ", ""
        )
        distance = Find(req, ".params > li:nth-child(3)").text.replace(
            "Дистанция: ", ""
        )
        components = (
            Find(req, ".params > li:nth-child(4)")
            .text.replace("Компоненты: ", "")
            .split(", ")
        )
        duration = Find(req, ".params > li:nth-child(5)").text.replace(
            "Длительность: ", ""
        )
        classes = (
            Find(req, ".params > li:nth-child(6)")
            .text.replace("Классы: ", "")
            .split(", ")
        )
        subclasses = Find(req, ".params > li:nth-child(7)").text
        if "Подклассы" in subclasses:
            subclasses = subclasses.replace("Подклассы: ", "").split(", ")
        else:
            subclasses = []
        description = Find(req, ".params > .subsection").text
        level = level.strip(" уровень")
        if level not in list(spellData.keys()):
            spellData[level] = {}
        spellData[level][name] = {
            "school": school,
            "castingTime": castingTime,
            "distance": distance,
            "components": components,
            "duration": duration,
            "classes": classes,
            "subclasses": subclasses,
            "description": description,
        }


#
# div.card__header > h2 > span:nth-child(1)
# div.active > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > span:nth-child(1)
# .size-type-alignment
#

r = searchinPage("/spells/")
r.html.render(scrolldown=420)
spellList = r.html.find("#list", first=True)
spellBlocks = spellList.find(".cards_list__block")

for block in spellBlocks:
    aLinks = list(block.absolute_links)
    syncSearch(aLinks)
    break

print(spellData["4"])
