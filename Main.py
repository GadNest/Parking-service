from tinydb import TinyDB, Query

db = TinyDB('db.json')
pricePerHour = 10


def enter():
    #Funkcja tworzy nowy rekord w bazie danych po wprowadzeniu numeru rejestracyjnego.
    import time
    enterTime = time.time()
    plates = input('Wprowadź numer tablic rejestracyjnych: ')
    q = Query()
    existing = db.search(q.plates == plates)
    if not existing:
        db.insert({'plates': plates, 'enterTime': enterTime, 'isPaid': False})
        print('Zapraszamy.')
    else:
        print(f'Error: Rejestracja {plates} już istnieje w bazie.')
#enter()


def paymentcalCulationTerminal(registrationPlates):
    #Funkcja wylicza należną płatność na podstawie czasu wjazdu na parking oraz czasu realizowanej płatności.
    import time
    get = Query()
    car = db.get(get.plates == registrationPlates)
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
            print('Czas postoju:', '\n', str(parkingHours)+'h', str(parkingMinutes)+'min')
            paymentRequired = None
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
            print('Do zapłaty: ', str(paymentRequired) + 'zł')
            return paymentRequired
        else:
            print('Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.')

#Ta część kodu odpowiada za realizację płatności. Funkcja paymentcalCulationTerminal() wylicza kwotę, następnie obsługuje płatność. Po wykonaniu płatności ustawia flagę isPaid na True
registration = input('Wprowadź numer rejestracyjny: ')
paymentRequired = paymentcalCulationTerminal(registration)
paymentMade = int(input('Podaj wpłaconą kwotę w zł:'))
while paymentMade < paymentRequired:
    missingPayment = paymentRequired - paymentMade
    print(f'Pozostała kwota do zapłaty to: {missingPayment}zł')
    paymentMade += int(input('Podaj dodaną kwotę w zł: '))
if paymentMade > paymentRequired:
    overPayment = paymentMade - paymentRequired
    print(f'Reszta: {overPayment}zł. Parking opłacony, dziękujemy.')
    payment = Query()
    db.update({'isPaid': True}, payment.plates == registration)
    get = Query()
    print(db.get(get.plates == registration))
else:
    print('Parking opłacony, dziękujemy.')
    payment = Query()
    db.update({'isPaid': True}, payment.plates == registration)
    get = Query()
    print(db.get(get.plates == registration))
rejestracja = None





