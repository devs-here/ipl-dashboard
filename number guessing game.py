import random

while True:
    number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("You have 10 attempts. Guess a number from 1 to 100: "))
        attempts += 1

        if guess < number:
            print("Too Low!")

        elif guess > number:
            print("Too high!")

        else :
            print(f"Correct!🙌 You got it in {attempts} attempt(s). ")
            break


        if attempts >= 10:
            print(f" Game over!😵‍💫 The number was {number}")
            break

    choice = input("Play Again?😏 (yes/no): ")

    if choice == "no":
        break