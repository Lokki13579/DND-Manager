from requests_html import HTMLSession


url = "https://dnd.su/spells/"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"
}
spellData = {}


def main(links):
    for link in links:
        session = HTMLSession()
        print(link)
        response = session.get(link)
        response.html.render(sleep=1)
        print(response.html.find("body", first=True).html)

        spellInfo = response.html.find(".cards-wrapper", first=True)
        print(spellInfo.text)


def openFile():
    with open("OtherPyFiles/spells.txt", "r") as file:
        return file.readlines()


if __name__ == "__main__":
    links = openFile()
    main(links)

    # thread2.start()
    # thread3.start()
