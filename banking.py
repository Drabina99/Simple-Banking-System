import random
import sys
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Card:
    def __init__(self):
        self.ID = random.randint(0, 1000000)
        self.IIN = [4, 0, 0, 0, 0, 0]
        self.custNo = []
        self.PIN = random.randint(1000, 9999)
        self.fullNumber = 0
        self.balance = 0

    def custNoInit(self):
        r = random.randint(100000000, 999999999)
        numbers = list(map(int, str(r)))
        self.custNo = numbers

    def checksumGen(self, numbers):
        numbersCopy = numbers.copy()
        for i in range(len(numbers)):
            if i % 2 == 0:
                numbers[i] *= 2
        for i in range(len(numbers)):
            if numbers[i] > 9:
                numbers[i] -= 9
        Sum = 0
        for number in numbers:
            Sum += number
        if Sum % 10 != 0:
            Sum = abs(10 - Sum % 10)
        else:
            Sum = 0
        numbersCopy.append(Sum)
        chars = [str(x) for x in numbersCopy]
        string = "".join(chars)
        self.fullNumber = int(string)

    def generateNo(self):
        numbers = []
        self.custNoInit()
        numbers = self.IIN + self.custNo
        self.checksumGen(numbers)


cur.execute("""
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0);
        """)
conn.commit()


def LuhnCheck(testNumber):
    num = [int(x) for x in str(testNumber)]
    for i in range(len(num)-1):
        if i % 2 == 0:
            num[i] *= 2
    for i in range(len(num)-1):
        if num[i] > 9:
            num[i] -= 9
    Sum = 0
    for i in range(len(num)-1):
        Sum += num[i]
    if Sum % 10 != 0:
        Sum = abs(10 - Sum % 10)
    else:
        Sum = 0
    if Sum == num[-1]:
        return True
    return False


def getCard(number):
    card = Card()
    cur.execute(f"SELECT id FROM card WHERE number={number}")
    card.ID = cur.fetchone()
    cur.execute(f"SELECT number FROM card WHERE number={number}")
    card.fullNumber = cur.fetchone()
    cur.execute(f"SELECT pin FROM card WHERE number={number}")
    card.PIN = cur.fetchone()
    cur.execute(f"SELECT balance FROM card WHERE number={number}")
    card.balance = cur.fetchone()
    return card


def loginCheck(number, pin):
    cur.execute(f"SELECT number FROM card WHERE number={number}")
    rNum = cur.fetchone()
    if rNum is None:
        return False
    num_ = int(rNum[0])
    cur.execute(f"SELECT pin FROM card WHERE number={number}")
    rPin = cur.fetchone()
    if rPin is None:
        return False
    pin_ = int(rPin[0])
    if num_ == number and pin_ == pin:
        return True
    return False

def cardGen():
    card = Card()
    card.generateNo()
    cur.execute(f"INSERT INTO card VALUES {(card.ID, card.fullNumber, card.PIN, card.balance)}")
    conn.commit()
    print("\nYour card has been created!")
    print("Your card number:\n{}\nYour card PIN:\n{}\n".format(card.fullNumber, card.PIN))
    return card

def income():
    inc = int(input("\nEnter income:\n"))
    if inc > 0:
        cur.execute(f"UPDATE card SET balance = balance+{inc} "
                    f"WHERE number={cardNo}")
        conn.commit()
    print("\nIncome was added!\n")


def transfer():
    numberTo = int(input("\nTransfer\nEnter card number:\n"))
    cur.execute(f"SELECT number FROM card WHERE number={numberTo}")
    if numberTo == cardNo:
        print("\nYou can't transfer money to the same account!\n")
        return False
    if not LuhnCheck(numberTo):
        print("\nProbably you made a mistake in the card number.\n"
              "Please try again!\n")
        return False
    if cur.fetchone() is None:
        print("\nSuch a card does not exist.\n")
        return False
    amount = int(input("\nEnter how much money you want to transfer:\n"))
    cur.execute(f"SELECT balance FROM card WHERE number={cardNo}")
    bal = int(cur.fetchone()[0])
    if amount > bal:
        print("\nNot enough money!\n")
    else:
        cur.execute(f"UPDATE card SET balance=balance-{amount} "
                    f"WHERE number={cardNo}")
        conn.commit()
        cur.execute(f"UPDATE card SET balance=balance+{amount} "
                    f"WHERE number={numberTo}")
        conn.commit()
    return True


while 1:
    menu = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if menu == 0:
        print("Bye!")
        sys.exit(0)
    elif menu == 1:
        card = cardGen()
    elif menu == 2:
        cardNo = int(input("\nEnter your card number:\n"))
        pin = int(input("\nEnter your card PIN:\n"))
        if not loginCheck(cardNo, pin):
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            while 1:
                logMenu = int(input("\n1. Balance\n2. Add income\n3. Do transfer\n"
                                    "4. Close account\n5. Log out\n0. Exit\n"))
                if logMenu == 0:
                    sys.exit(0)
                elif logMenu == 1:
                    print("\nBalance: {}\n".format(card.balance))
                elif logMenu == 2:
                    income()
                elif logMenu == 3:
                    if not transfer():
                        continue
                elif logMenu == 4:
                    cur.execute(f"DELETE FROM card WHERE number={card.fullNumber}")
                    conn.commit()
                elif logMenu == 5:
                        print("\nYou have successfully logged out!\n")
                        break
