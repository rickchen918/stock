class account:
    def __init__(self,name,number,balance):
         self.__name = name 
         self.__number = number
         self.__balance = balance
         
    def deposit(self,amount):
        if amount <= 0:
            print ("deposit can't be 0")
        else:
            self.__balance += amount
            print (self.__balance)
