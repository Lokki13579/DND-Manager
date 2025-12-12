stats = {"1": 4, "2": 0}
print(max(list(map(int, dict(filter(lambda x: x[1] > 0, stats.items())).keys()))) + 1)
