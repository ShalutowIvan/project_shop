a = "11331"
q = any(i.isdigit() for i in a) and not all(i.isdigit() for i in a)
print(q)

