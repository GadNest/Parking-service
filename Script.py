from tinydb import TinyDB, Query
from Main import paymentcalCulation

db = TinyDB('db.json')
pricePerHour = 15

#Payment
registration = input('Wprowadź numer rejestracyjny: ')
get = Query()
car = db.get(get.plates == registration)
paymentRequired = paymentcalCulation(registration)
print('Do zapłaty:', paymentRequired)
paymentMade = int(input('Podaj wpłaconą kwotę w zł:'))
currentBalance = car['moneyPaid']
newBalance = currentBalance + paymentMade
db.update({'moneyPaid': newBalance}, Query().plates == registration)
car = db.get(get.plates == registration)
print(car)
# while paymentMade < paymentRequired:
#     missingPayment = paymentRequired - paymentMade
#     print(f'Pozostała kwota do zapłaty to: {missingPayment}zł')
#     paymentMade += int(input('Podaj dodaną kwotę w zł: '))
#     if paymentMade > paymentRequired:
#         overPayment = paymentMade - paymentRequired
#         print(f'Reszta: {overPayment}zł. Parking opłacony, dziękujemy.')
#         payment = Query()
#         db.update({'isPaid': True}, payment.plates == registration)
#         get = Query()
#         print(db.get(get.plates == registration))
#     else:
#         print('Parking opłacony, dziękujemy.')
#         payment = Query()
#         db.update({'isPaid': True}, payment.plates == registration)
#         get = Query()
#         print(db.get(get.plates == registration))
#     registration = None


#def exit():
    # import datetime
    # plates = input('Wprowadź numer tablic rejestracyjnych: ')
    # Car = Query()
    # db.search(Car.plates == f'{plates}')
    # exitTime = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    # enterTime = db.search(Car.enterTime)
    # parkingTime = exitTime - enterTime

#     if Car.isPaid == True:
#         db.remove(Car)
# exit()
# import datetime
# Car = Query()
# db.search(Car.plates == 'GD2G153')
# exitTime = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
# enterTime = db.search(Car.enterTime)
# parkingTime = exitTime - enterTime



#while True:
#    insert()
#    for item in db:
#        print(item)

#
# search = Query()
# db.update({'isPaid': True}, search.plates == 'KCV3103')