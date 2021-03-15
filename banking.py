import random
import sys

class Card:
    def __init__(self):
        self.IIN = 400000
        self.custNo = 0
        self.PIN = random.randint(1000, 9999)
        self.fullNumber = 0
        self.balance = 0

    def custNoInit(self):
        numbers = []
        for i in range(9):
            r = random.randint(1, 9)
            #print(r)
            numbers.append(r)
        chars = [str(x) for x in numbers]
        string = "".join(chars)
        self.custNo = int(string)

    def generateNo(self):
        numbers = []
        numbers.append(self.IIN)
        numbers.append(self.custNo)
        numbers.append(random.randint(1, 9))
        #print(numbers)
        chars = [str(x) for x in numbers]
        string = "".join(chars)
        self.fullNumber = int(string)


while (1):
    menu = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if menu == 0:
        print("Bye!")
        sys.exit(0)
    elif menu == 1:
        card = Card()
        card.custNoInit()
        card.generateNo()
        print("\nYour card has been created!")
        print("Your card number:\n{}\nYour card PIN:\n{}\n".format(card.fullNumber, card.PIN))
    elif menu == 2:
        cardNo = int(input("\nEnter your card number:\n"))
        pin = int(input("\nEnter your card PIN:\n"))
        if cardNo != card.fullNumber or pin != card.PIN:
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            logMenu = int(input("1. Balance\n2. Log out\n0. Exit\n"))
            if logMenu == 0:
                sys.exit(0)
            elif logMenu == 1:
                print("\nBalance: {}\n".format(card.balance))
            elif logMenu == 2:
                print("\nYou have successfully logged out!\n")
