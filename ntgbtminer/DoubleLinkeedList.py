

class Employee:
    def __init__(self, name, age, id):
        self.id = id
        self.name = name
        self.age = age
        self.next = None
        self.prev = None

class Node:
    def __init__(self):
        self.data = None
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self, emp):
        self.curr = emp
        # self.next = None
        # self.prev = None

    def nextObj(self, emp):
        self.next = emp
    



e1 = Employee('nam1', 12, 1)

e2 = Employee('nam2', 13, 2)
e3 = Employee('nam3', 14, 3)
e4 = Employee('nam4', 15, 4)
e5 = Employee('nam5', 16, 5)


dl = DoubleLinkedList(e1)

dl.nextObj(e2)

print(dl.curr.name)
