from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self,owner, balance):
        self.owner=owner
        self.__balance=balance
        self.transaction_history=[]

    @abstractmethod
    def account_type(self):
        pass
    def show_balance(self):
        print(f"{self.owner}'s balance: {self.get_balance()}")

    def show_history(self):
        print(f"\n{self.owner}'s Transaction history : ")
        for transaction in self.transaction_history:
            print(f"{transaction['type']} | Amount: {transaction['amount']} | Balance: {transaction['balance']}")

    def deposit(self, amount):
        if amount>0:
            self.__balance += amount
            self.transaction_history.append({
                "type": "deposit",
                "amount": amount,
                "balance": self.__balance
            })
            print(f"{amount} deposited in your account. New balance:{self.__balance} ")
    
    def withdraw(self,amount):
        if amount > self.__balance:
            print("Insufficient balance")

        else:
            self.__balance -= amount
            self.transaction_history.append({
                "type": "withdrawal",
                "amount": amount,
                "balance": self.__balance
            })
            print(f"{amount} is witdrawn from your account. New balance: {self.__balance}")

    def get_balance(self):
        return self.__balance
    



class SavingsAccount(Account):
    def __init__(self, owner, balance):
        super().__init__(owner, balance)

    def account_type(self):
        print("Savings Account")

    
    

class CurrentAccount(Account):
    def __init__(self, owner, balance):
        super().__init__(owner , balance)

    def account_type(self):
        print("Current Account")

    


s1=SavingsAccount("Gaurav", 50000)
c1=CurrentAccount("Bani", 40000)

s1.deposit(200)
print(s1.owner)
c1.withdraw(500)
c1.show_balance()
s1.show_history()
c1.show_history()

#polymorphsim loop
accounts= [s1, c1]
for account in accounts:
    account.account_type()