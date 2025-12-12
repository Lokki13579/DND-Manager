stats = {
    "1": [4, 3, 5],
    "2": [6, 5],
}
print([j for i in stats.values() for j in i])
