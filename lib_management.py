from abc import ABC, abstractmethod

class LibraryItem(ABC):
    def __init__(self, title, id, available = True):
        self.title = title
        self.id = id
        self.__available = available
        self.borrowed_by = None
        
    @abstractmethod
    def get_details(self):
        pass

    def display_id(self):
        print(f"ID:{self.id}")

    def borrow(self, user):
        if self.__available:
            self.__available = False
            self.borrowed_by = user
            print(f"{self.title} successfully borrowed by {user.name}")

    
    def return_item(self):
        self.__available = True
        self.borrowed_by = None
    def is_available(self):
        return self.__available

#======Book======#
class Book(LibraryItem):
    def __init__(self, title, id):
        super().__init__(title, id)
      

    def get_details(self):
        status= "Available" if self.is_available() else "Not Available"
        print(f"Book's title: {self.title}.ID:{self.id}.Availability:{status}")



    
#======Magazine======#    
class Magazine(LibraryItem):
    def __init__(self, title, id):
        super().__init__(title, id)
        

    def get_details(self):
        status= "Available" if self.is_available() else "Not Available"
        print(f"Magazine's title: {self.title}.ID:{self.id}.Availability:{status}")

   
#======User======#
class User():
    def __init__(self, name):
        self.name = name
        self.borrowed_items = []

    def borrow_item(self, item):
        self.borrowed_items.append(item)

    def return_item(self, item):
        self.borrowed_items.remove(item)

    def show_item(self):
        if not self.borrowed_items:
            print(f"{self.name} has not borrowed any book/magazine ")

        else:
            print(f"{self.name} has borrowed: ")
            for item in self.borrowed_items:
                print(f"-{item.title}")

#======Library======#
class Library():
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)

    def show_available_items(self):
        print("Available items: ")
        for item in self.items:
            if item.is_available():
                item.get_details()

    def lend_item(self, user, item):       
        if item.is_available():              # is the item free?
            item.borrow(user)                    # mark item as "not available"
            user.borrow_item(item)           # add item to user's borrowed list

        else:
            print(f"Already taken by {item.borrowed_by.name}")

    def accept_return(self, user, item):
        if item in user.borrowed_items:      # did this user actually borrow it?
            item.return_item()               # mark item as "available" again
            user.return_item(item)           # remove from user's borrowed list

        else: 
            print(f"{user.name} did not borrow {item.title}")

book1=Book("python", 101)
book2=Book("Java", 102)
magazine1=Magazine("Spider Man: Brand New Day", 201)
magazine2=Magazine("Moon Knight", 202)
user1=User("Gaurav")
user2=User("Bani")
user3=User("Suraj")
lib=Library()

lib.add_item(book1)
lib.add_item(book2)
lib.add_item(magazine1)
lib.add_item(magazine2)


lib.show_available_items()
lib.lend_item(user1, book1)
lib.lend_item(user2, book2)
lib.accept_return(user2, book2)
lib.lend_item(user2, book1)
lib.accept_return(user1, book2)
lib.show_available_items()
user1.show_item()
user2.show_item()
book2.get_details()