from tinydb import TinyDB, Query

db = TinyDB('db.json')

#Cena za godzinę parkowania [zł]
pricePerHour = 10

#Czas na wyjazd z parkingu po dokonaniu płatności [s]
timeToLeave = 600

def enter():
    #Funkcja tworzy nowy rekord w bazie danych po wprowadzeniu numeru rejestracyjnego.
    import time
    enterTime = time.time()
    plates = input('[ENTER] Wprowadź numer tablic rejestracyjnych: ')
    q = Query()
    existing = db.search(q.plates == plates)
    if not existing:
        db.insert({'plates': plates, 'enterTime': enterTime, 'moneyPaid': 0})
        print('Zapraszamy.')
    else:
        print(f'ERROR: Rejestracja {plates} już istnieje w bazie.')
    return



def paymentCalculation(registration):
    #Funkcja wylicza należną płatność na podstawie czasu wjazdu na parking oraz czasu realizowanej płatności.
    import time
    get = Query()
    car = db.get(get.plates == registration)
    while car == None:
        print('Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.')
        car = db.get(get.plates == input('Wprowadź numer rejestracyjny: '))
    else:
        if 'enterTime' in car:
            enterTime = (car['enterTime'])
            exitTime = time.time()
            parkingTime = exitTime - enterTime
            parkingHours = int(parkingTime / 3600)
            parkingMinutes = int((parkingTime % 3600) / 60)
            #print('Czas postoju:', '\n'+str(parkingHours)+'h', str(parkingMinutes)+'min')
            paymentRequired = None
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
            return paymentRequired
        else:
            print('Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.')


def paymentValidation(registration):
    #Funkcja sprawdza czy płatność została uiszczona. Do sprawdzania przy wyjeździe
    import time
    get = Query()
    car = db.get(get.plates == registration)
    while car == None:
        print('Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.')
        car = db.get(get.plates == input('Wprowadź numer rejestracyjny: '))
    else:
        if 'enterTime' in car:
            enterTime = (car['enterTime'])
            exitTime = time.time() - timeToLeave
            parkingTime = exitTime - enterTime
            parkingHours = int(parkingTime / 3600)
            parkingMinutes = int((parkingTime % 3600) / 60)
            paymentRequired = None
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
            return paymentRequired
        else:
            print('Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.')


def canLeave(registration):
    #Ta funkcja sprawdza czy pojazd o podanym numerze rejestracyjnym ma opłacony parking i może wyjechać.
    get = Query()
    car = db.get(get.plates == registration)
    moneyPaid = car['moneyPaid']
    balance = moneyPaid - paymentValidation(registration)
    if balance < 0:
        return False
    elif balance >= 0:
        return True



def Payment():
    #Ta część kodu odpowiada za realizację płatności. Funkcja paymentCalculation() wylicza kwotę, następnie obsługuje płatność. Po wykonaniu płatności ustawia flagę isPaid na True
    import time
    registration = input('[PŁATNOŚĆ] Wprowadź numer rejestracyjny: ')
    query = Query()
    car = db.get(query.plates == registration)

    enterTime = (car['enterTime'])
    exitTime = time.time()
    parkingTime = exitTime - enterTime
    parkingHours = int(parkingTime / 3600)
    parkingMinutes = int((parkingTime % 3600) / 60)
    print('Czas postoju:', '\n'+str(parkingHours)+'h', str(parkingMinutes)+'min')

    paymentRequired = paymentCalculation(registration)
    missingPayment = paymentRequired - car['moneyPaid']
    if missingPayment > 0:
        print('Do zapłaty:', missingPayment)
        paymentMade = int(input('Podaj wpłaconą kwotę w zł:'))
        currentBalance = car['moneyPaid']
        newBalance = currentBalance + paymentMade
        db.update({'moneyPaid': newBalance}, Query().plates == registration)
        car = db.get(query.plates == registration)
        while newBalance < paymentRequired:
            missingPayment = paymentRequired - newBalance
            print(f'Pozostała kwota do zapłaty to: {missingPayment}zł')
            newBalance += int(input('Podaj dodaną kwotę w zł: '))
            db.update({'moneyPaid': newBalance}, Query().plates == registration)
            car = db.get(query.plates == registration)
        if newBalance > paymentRequired:
            overPayment = newBalance - paymentRequired
            print(f'Reszta: {overPayment}zł. Parking opłacony, dziękujemy.')
        else:
            db.update({'moneyPaid': newBalance}, Query().plates == registration)
            print('Parking opłacony, dziękujemy.')
    else:
        print("Parking opłacony. Dziękujemy.")


def Exit():
    registration = input('[EXIT] Wprowadź numer rejestracyjny pojazdu: ')
    get = Query()
    car = db.get(get.plates == registration)
    while car == None:
        print('Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.')
        car = db.get(get.plates == input('Wprowadź numer rejestracyjny: '))
    else:
        if canLeave(registration):
            print('Dziękujemy za pobyt, zapraszamy ponownie.')
            db.remove(get.plates == registration)
        else:
            print('Brak pełnej opłaty za pobyt. Proszę uregulować należność.')
