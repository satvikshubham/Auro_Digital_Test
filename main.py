# Programming Exercise: Order Book processing
# We are looking for a program that reads a file with fictional orders. The program should read and process ALL the orders in the order file and maintain order books as order messages are read and processed. 
# The order file orders.xml contains the fictive order messages that can be of the type AddOrder or DeleteOrder (see “Order Message” on the next page).

# The file with the fictive orders will accompany this document. (Zipped as orders.7z)

# The program should create order books (see “Order Book”) dynamically as they are referenced in the order messages during processing of the XML file. Order books should be maintained in memory. Orders are inserted to the order books based on price and time, for examples see “Book Examples”.  After processing all order mes-sages the program should print the order books according to the “output exam-ple” below. 
# At start and end of processing, the timestamp should be outputted.
# All orderbooks should be printed at the end, along with the duration of processing in seconds.
# Please provide your code for implementing the described functionality. Reflect and comment on performance aspects. If not implemented, what could be done to im-prove performance? Reflect and comment on data consistency if a multithreaded approach is used for processing the order flow.
# Steps for adding an order to an order book:
# 1.	Look up the order book based upon the book attribute. If the book does not exist create it.
# 2.	Examine if the order can match one or more orders already in the book. Orders having their whole quantity being matched (i.e. volume == 0) are removed from the book. See matching example below.
# 3.	If the incoming order is completely matched against orders in the book i.e. volume == 0 the order is deleted. 
# 4.	If the incoming order is either partly or not matched the order is inserted into the book.
# Steps for deleting an order:
# 1.	Look up the order book based on the book attribute.
# 2.	Locate the order in the book based upon the orderId attribute. If the or-der is not found just ignore the operation and just continue.
# 3.	If found remove the order from the book.
#  
# Order Messages
# Orders are defined in a rather flat XML structure. Under the root element <Orders> there are only two types of elements and no deeper nesting.
# <AddOrder book="book-2" operation="SELL" price="101.00" volume="87" orderId="9363" />
# •	AddOrder, specifying that this element adds an order to an orderbook.
# •	book, identifies the order book to which the order should be added.
# •	operation, specifies whatever the order is a BUY or SELL order.
# •	price, specifies the price to which the order could be sold if a SELL order or bought if a BUY order.
# •	volume, specifies the amount of units to be sold or bought.
# •	orderID, unique identification of the order .
# <DeleteOrder book="book-3" orderId="9036" />
# •	DeleteOrder, operation specifying that an order is to be deleted from the order-book.
# •	book,  identifies the orderbook in which the order resides.
# •	orderId, identifies the order to be deleted.

# Order Book
# An order is an interest in buying or selling an “asset”.  All interest (i.e. orders) for a given “as-set”  is kept in an order book.  An order book have two sides (or lists). One side with the orders expressing a buy interest and another side with the orders expressing a sell interest.  When a new order is to be inserted in to the book it must be examined if there is an interest in the book matching the interest of the incoming order. If so a match takes place.  A match takes place if the a sell order price <= with the a buy price. The volume match is equal with the lowest vol-ume for the both orders. The order volume for the incoming order and the order in book is re-duced with the matched volume. If an incoming order cannot be matched or partly matched the  order must be inserted into the book. The orders are then inserted into the buy or sell list based upon price and time priority.
# A buy order with the price 101 € has a higher priority than a buy order with the price 100 €. On the other side a sell order with the price of 10 € has higher priority than a sell order with the price 11 €. 

# Order Book Examples
# An order book typically has a list of BUY and SELL orders. Orders are sorted by price-time priori-ty, i.e. orders with a better price precedes an order with a worse price, and orders with the same price are prioritized such that the order that’s been in the book for the longest time is processed first.
# Assume an empty order book to which we add a BUY order with the price of 100.00 and with the volume 50. The order book will look as follows:
# Buy	Sell
# 50 @ 100.0	

# We now add a SELL order with the price of 101.50 and with a volume of 60. The order book will then look as follows:
# Buy	Sell
# 50 @ 100.0	60 @ 101.50

# We now add two additional BUY orders one with price = 100.25 and volume = 30 and one with price = 99.50 and volume = 45. The order book will then look as follows:
# Buy	Sell
# 30 @ 100.25	60 @ 101.50
# 50 @ 100.00	
# 45 @ 99.5	
# We now add a SELL order with the price = 99.75 and volume = 50. The order book will then look as follows:
# Buy	Sell
# 30 @ 100.00	60 @ 101.50
# 45 @ 99.50	

# We now add an additional SELL order with the price = 100.00 and volume = 50. The or-der book will then look as follows:
# Buy	Sell
# 45 @ 99.50	20 @ 100.00
# 	60 @ 101.50

# We now add a BUY order with the price = 99.50 and volume = 60. The order book will then look as follows:
# Buy	Sell
# 45 @ 99.50	20 @ 100.00
# 60 @ 99.50	60 @ 101.50






import pandas

# Output example of a program implementing order book:

class OrderBook:
    def __init__(self):
        self.buy = []
        self.sell = []

    def __str__(self):
        return "Buy\tSell"

class Order:
    def __init__(self, book, operation, price, volume, orderId):
        self.book = book
        self.operation = operation
        self.price = price
        self.volume = volume
        self.orderId = orderId

    def __str__(self):
        return f"{self.volume} @ {self.price}"

class OrderBookManager:
    def __init__(self):
        self.order_books = {}

    def add_order(self, order):
        if order.book not in self.order_books:
            self.order_books[order.book] = OrderBook()
        order_book = self.order_books[order.book]

        if order.operation == "BUY":
            order_book.buy.append(order)
            order_book.buy.sort(key=lambda x: (x.price, x.orderId), reverse=True)
        else:
            order_book.sell.append(order)
            order_book.sell.sort(key=lambda x: (x.price, x.orderId))

    def delete_order(self, order):
        order_book = self.order_books[order.book]
        if order.operation == "BUY":
            order_book.buy.remove(order)
        else:
            order_book.sell.remove(order)

    def __str__(self):
        output = ""
        for order_book in self.order_books.values():
            output += str(order_book) + " "
        
        return output
    
orders = {}


if __name__ == "__main__":
    file = open("orders.xml", "r")
    content = file.read()
    orders = []
    orderbook = OrderBookManager()
    for line in content.splitlines():
        if line.startswith("<AddOrder"):
            # order is like
            # <AddOrder book="book-3" operation="BUY" price=" 99.50" volume="86" orderId="2" />
            # split line when see a string
            line = line.split('')
            line = line.split()
            print(line)
            book = line[1].split("=")[1].strip('"')
            operation = line[2].split("=")[1].strip('"')
            # remove spaces
            price = line[3].split("=")[1].strip('"')
            # remove " from price
            price = price.replace('"', '')
            
            print(price)
            # price = float(price)
            # price = float(line[3].split("=")[1].strip('"'))
            print(price)
            volume = int(line[4].split("=")[1].strip('"'))
            orderId = int(line[5].split("=")[1].strip('"'))
            # order = Order(book, operation, price, volume, orderId)

        elif line.startswith("<DeleteOrder"):
            line = line.split()
            book = line[1].split("=")[1].strip('"')
            orderId = int(line[2].split("=")[1].strip('"'))
            order = Order(book, None, None, None, orderId)
            orderbook.delete_order(order)
            