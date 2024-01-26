a = {'a': 1, 'b': 2, 'e': 4} 
b = {'b': 3, 'c': 4, 'e': 6}
c = {}

for i in a.keys():
    if i in b:
        c[i] = a[i] + b[i]
    else:
        c[i] = a[i]
for i in b.keys():
    if i not in c:
        c[i] = b[i]
print(c)

