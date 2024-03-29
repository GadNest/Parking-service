from tinydb import TinyDB, Query

db = TinyDB('db.json')
pricePerHour = 15

plates = input('Wprowadź numer rejestracyjny pojazdu: ')
def PaymentCalculationExit():
    import time
    get = Query()
    car = db.get(get.plates == f'{plates}')
    while car == None:
        print('Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.')
        Car = db.get(get.plates == input('Wprowadź numer rejestracyjny: '))
    else:
        print(car)

        if 'enterTime' in car:
            enterTime = (car['enterTime'])
            exitTime = time.time()
            parkingTime = exitTime - enterTime
            parkingHours = int(parkingTime / 3600)
            parkingMinutes = int((parkingTime % 3600) / 60)
            print('Parking time:', '\nH:', parkingHours, 'M:', parkingMinutes)
            paymentRequired = None
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = (parkingHours + 1) * pricePerHour
            print('Do zapłaty: ', str(paymentRequired) + 'zł')
            return paymentRequired
        else:
            print('Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.')
paymentRequired = PaymentCalculationExit()
print(paymentRequired)


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