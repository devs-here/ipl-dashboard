from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, item_name, item_weight):
        self.item_name = item_name
        self.item_weight = item_weight


    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def item_type(self):
        pass

    def get_info(self):
        print(f"Kakashi's item's name {self.item_name}, weight: {self.item_weight}")

class Weapon(Item):
    def __init__(self, item_name, item_weight, damage_value):
       super().__init__(item_name, item_weight)
       self.__damage_value=damage_value

        
    def use(self):
        print(f"{self.item_name} strikes lightning! with damage value: {self.__damage_value}\n")

    def item_type(self):
        return "CHIDORI"

    def damage(self, amount):
        self.__damage_value=amount
        print(f"damage set to: {self.__damage_value}")

class Consumable(Item):
    def __init__(self, item_name, item_weight, uses_left):
        super().__init__(item_name, item_weight)
        self.__uses_left=uses_left

    def use(self):
        if self.__uses_left > 0:
            self.__uses_left -=1
            print(f"Used {self.item_name}. charges remaining: {self.__uses_left}.")
        else:
            print(f"{self.item_name} is empty!")
    
    def item_type(self):
        return "Healing"
    
    def usesLeft(self, amount):
        self.__uses_left=amount
        print(f"Consumed {self.item_name}. {self.__uses_left} charges left.")

class Inventory():
    def __init__(self, max_weight):
        self.__items=[]
        self.__max_weight=max_weight
        self.__current_weight=0


    def add_item(self, new_item):
        if self.__current_weight+new_item.item_weight > self.__max_weight:
            print("Too heavy")

        else:
            self.__items.append(new_item)
            self.__current_weight += new_item.item_weight
            print(f"Added {new_item.item_weight}kg to the inventory.\n")

    def show_inventory(self):
        print(f"---Inventory({self.__current_weight}/{self.__max_weight}kg)---.\n")
        for item in self.__items:
            item.get_info()

        print()


my_backpack= Inventory(max_weight=200)

sword=Weapon("Chidori Blade", 50, 200)
portion=Consumable("health Portion", 50, 5)

my_backpack.add_item(sword)
my_backpack.add_item(portion)

my_backpack.show_inventory()
sword.use()
portion.use()

