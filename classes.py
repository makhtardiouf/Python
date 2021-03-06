'''
Demo for Classes, simulating pseudo stock market operations

'''
# import math
import random
import datetime

class Stock:
    availDate = datetime.date.today()

    # Conctructor of the object
    def __init__(self):
        self.shares = []

    def add(self, x):
        self.shares.append(x)

    def size(self):
        return len(self.shares)

    def show(self):
        width = 15
        print(str('\t' + '-'*width).center(10), str('\t' + '-'*width).center(20))

        for i, s in enumerate(self.shares):
            print("\t{0:10}".format("\tItem " + str(i)), " | \t{0:20}".format(str(s)))
        #    i += 1
        print("Available since: ", self.availDate)

class Stockbis(Stock):
    def __init__(self):
        print("OOP magic inherited class from Stock")
        Stock.__init__(self)

    def listStock(self):
        Stock.show(self)


print("Creating your stock")
myStock = Stock()
i = random.randint(3, 15)

while i > 0:
    myStock.add(random.random())
    i -= 1

print(myStock.size(), " shares added to your portfolio:")
myStock.show()

stockB = Stockbis()
#stockB.shares =
print( myStock.shares.reverse())
stockB.listStock()

print(isinstance(myStock, Stock))
print(isinstance(stockB, Stock))
print(issubclass(stockB, Stock))
