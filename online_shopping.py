from abc import ABC, abstractmethod

class Products(ABC):
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    
    @abstractmethod
    def get_details(self):
       pass

class shirt(Products):
    def __init__(self, name, price, stock, size):
        super().__init__(name, price, stock)
        self.size = size
        
    def get_details(self):
        print(f"{self.name} | Price: {self.price} | Size: {self.size} | Stock: {self.stock}")

class pant(Products):
    def __init__(self, name, price, stock, length):
        super().__init__(name, price, stock)
        self.length = length
        
    def get_details(self):
        print(f"{self.name} | Price: {self.price} | Length: {self.length} | Stock: {self.stock}")

class shoe(Products):
    def __init__(self, name, price, stock, shoe_size):
        super().__init__(name, price, stock)
        self.shoe_size = shoe_size
        
    def get_details(self):
        print(f"{self.name} | Price: {self.price} | Shoe: {self.shoe_size} | Stock: {self.stock}")


class watch(Products):
    def __init__(self, name, price, stock, brand):
        super().__init__(name, price, stock)
        self.brand = brand
        
    def get_details(self):
        print(f"{self.name} | Price: {self.price} | Brand: {self.brand} | Stock: {self.stock}")



class cart():
    def __init__(self):
        self.products = []

    def add_products(self, product):
        self.products.append(product)
        print(f"{product.name} added to cart")

    def remove_products(self, product):
        self.products.remove(product)
        print(f"{product.name} removed from cart")

    def show_products(self):
        if not self.products:
            print("Cart is empty!")

        else:
            print("Products in cart:")
            for product in self.products:
                print(f"{product.name} | Price: {product.price}")


class shop():
    def __init__(self):
        self.products =[]

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        print("Available products: ")
        for product in self.products:
            if product.stock > 0:
                product.get_details()

    
    def checkout(self, cart, discount=0):
        total = 0
        for product in cart.products:
            total = total + product.price

        print(f"Subtotal: {total}")
        total = total - discount
        print(f"discount: {discount}")
        print(f"total after discount of {discount}: {total}")



s1 = shirt("Allen Solly ", 499, 6, "XL")
p1 = pant("Jack & Jeans", 799, 5, 35.5)
sh1 = shoe("Puma", 399, 0, 3)
w1 = watch("Casio", 1500, 6, "Casio")

cart1=cart()
shop1=shop()

shop1.add_product(s1)
shop1.add_product(p1)
shop1.add_product(sh1)
shop1.add_product(w1)

shop1.show_products()
cart1.add_products(s1)
cart1.add_products(p1)
cart1.show_products()
shop1.checkout(cart1, discount= 200)