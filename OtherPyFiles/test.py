a = ["apple", "banana", "cherry", "date"]
b = "ban"
print(any([b.lower() in i.lower() for i in a]))
