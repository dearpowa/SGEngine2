test = [(3.23, "rosso"), (2, "verde"), (1.2, "blu"), (1.1, "verde")]

test.sort(key=lambda l: l[0])

print(test[0][1])