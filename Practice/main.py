class Employee():
    def __init__(self, name , id , desc):
        self.__name = name
        self.id = id
        self.desc = {"desc": desc }

    def roll(func):
        def wrap(self):
            print("hey\n")
            func(self)
            print("end\n")
        return wrap

    @roll
    def display(self):
        print(self.__name)
    
    @roll
    def display1(self):
        print(self.id)
    


i = Employee("samir",5,"Professional")

i.display()
i.display1()

print( i._Employee__name)