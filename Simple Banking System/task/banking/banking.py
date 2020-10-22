import random
import sqlite3


class Card:
    def __init__(self):
        self.number = "400000"
        self.pin = str(random.randint(0, 9))
        self.balance = 0
        Luhn = [4, 0, 0, 0, 0, 0]
        sum = 0
        index = 0
        for _ in range(9):
            num = random.randint(0, 9)
            Luhn.append(num)
            self.number = self.number + str(num)

        for _ in range(3):
            num = random.randint(0, 9)
            self.pin = self.pin + str(num)

        for l in Luhn:
            if index % 2 == 0:
                l = l * 2
            if l > 9:
                l = l - 9
            index += 1
            sum = sum + l
        num = sum % 10
        if num != 0:
            num = 10 - num
        self.number = self.number + str(num)


def algLuhn(cardNum):
    index = 0
    sum = 0
    for j in cardNum:
        i = int(j)
        if index == 15:
            sum += int(i)
            break
        if index % 2 == 0:
            i = i * 2
        if i > 9:
            i = i - 9
        index += 1
        sum = sum + i
    if sum % 10 == 0:
        return True
    return False


#cards = []
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()
id = 1

while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = input()
    if choice == "1":
        newCard = Card()
        cur.execute('INSERT INTO card(id, number, pin) VALUES({}, {}, {});'.format(id, newCard.number, newCard.pin))
        conn.commit()
        id += 1
        print("Your card has been created")
        print("Your card number:\n" + newCard.number)
        print("Your card PIN:\n" + newCard.pin)
    elif choice == "2":
        found = False
        print("Enter your card number:")
        logNum = input()
        print("Enter your PIN:")
        logPin = input()
        cur.execute('SELECT balance FROM card WHERE number = {} AND pin = {}'.format(logNum, logPin))
        result = cur.fetchone()
        if result:
            result = str(result)
            balance = 0
            for word in result.split():
                if word.isdigit():
                    if balance == 0:
                        balance = int(word)
                    else:
                        balance = balance * 10 + int(word)
            print("You have successfully logged in!")
            while True:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                choice = input()
                if choice == "1":
                    print("Balance: " + str(balance))
                elif choice == "2":
                    print("Enter how much do you want to add:")
                    balance += int(input())
                    cur.execute('UPDATE card SET balance = {} WHERE number = {} AND pin = {};'.format(balance, logNum, logPin))
                    conn.commit()
                elif choice == "3":
                    print("Enter card number of receiver:")
                    transNum = input()
                    if transNum == logNum:
                        print("You can't transfer money to the same account!")
                    elif algLuhn(transNum) == False:
                        print("Probably you made a mistake in the card number. Please try again!")
                    else:
                        cur.execute('SELECT balance FROM card WHERE number = {}'.format(transNum))
                        result = cur.fetchone()
                        if result:
                            print("Enter how much do you want to transfer:")
                            transSum = int(input())
                            if transSum > balance:
                                print("Not enough money!")
                            else:
                                result = str(result)
                                transBalance = 0
                                for word in result.split():
                                    if word.isdigit():
                                        if transBalance == 0:
                                            transBalance = int(word)
                                        else:
                                            transBalance = transBalance * 10 + int(word)
                                transBalance += transSum
                                balance -= transSum
                                cur.execute(
                                    'UPDATE card SET balance = {} WHERE number = {};'.format(transBalance,
                                                                                                         transNum))
                                cur.execute(
                                    'UPDATE card SET balance = {} WHERE number = {} AND pin = {};'.format(balance,
                                                                                                          logNum,
                                                                                                          logPin))
                                conn.commit()
                        else:
                            print("Such a card does not exist.")
                elif choice == "4":
                    cur.execute('DELETE FROM card WHERE number = {}'.format(logNum))
                    conn.commit()
                elif choice == "5":
                    print("You have successfully logged out!")
                    break
                elif choice == "0":
                    break
        else:
            print("Wrong card number or PIN!")
    if choice == "0":
        print("Bye!")
        #cur.execute('DELETE FROM card')
        #conn.commit()
        break
