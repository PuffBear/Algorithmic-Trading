class Order:
    def __init__(self, price, quantity, order_id):
        self.price = price
        self.quantity = quantity
        self.order_id = order_id
        self.next = None
        self.prev = None

class OrderBook:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_order(self, price, quantity, order_id):
        new_order = Order(price, quantity, order_id)
        if self.head is None:
            self.head = self.tail = new_order
        else:
            current = self.head
            while current and current.price < price:
                current = current.next
            if current is None:
                self.tail.next = new_order
                new_order.prev = self.tail
                self.tail = new_order
            elif current.prev is None:
                new_order.next = self.head
                self.head.prev = new_order
                self.head = new_order
            else:
                previous = current.prev
                previous.next = new_order
                new_order.prev = previous
                new_order.next = current
                current.prev = new_order

    def remove_order(self, order_id):
        current = self.head
        while current and current.order_id != order_id:
            current = current.next
        if current is not None:
            if current.prev is not None:
                current.prev.next = current.next
            if current.next is not None:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next
            if current == self.tail:
                self.tail = current.prev

# Example usage
order_book = OrderBook()
order_book.insert_order(100, 10, 1)
order_book.insert_order(101, 5, 2)
order_book.insert_order(99, 20, 3)
order_book.remove_order(2)
