import os
class Panel:
    def __init__(self, name = "<P> Панелька <P>"):
        self.name = name
    def show(self,data):
        showable = data.split("&")
        print(showable)
        os.system("clear")
        print(self.name)
        for l in showable:
            print(l,end="")

