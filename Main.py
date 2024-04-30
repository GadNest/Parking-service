from tinydb import TinyDB, Query

db = TinyDB('db.json')

# Stawka za każdą rozpoczętą godzinę parkowania [zł]
pricePerHour = 10

# Maksymalna liczba samochodów [jednostka]
parkingCapacity = 200

# Czas na wyjazd z parkingu liczony od dokonania opłaty do wyjazdu [s]
timeToLeave = 600

# Liczba samochodów, która uruchamia alert o wysokim zapełnieniu parkingu
alertRecordNumber = 7

numberOfCars = len(db.all())
if numberOfCars >= alertRecordNumber:
    Alert = True
else:
    Alert = False

def enter():
    # Funkcja tworzy nowy rekord w bazie danych po wprowadzeniu numeru rejestracyjnego.
    # Funkcja do wykorzystania przy szlabanie wjazdowym
    import time
    enterTime = time.time()
    plates = input('[ENTER] Wprowadź numer tablic rejestracyjnych: ')
    plates = plates.upper()
    q = Query()
    existing = db.search(q.plates == plates)
    if not existing:
        db.insert({'plates': plates, 'enterTime': enterTime, 'moneyPaid': 0})
        print('Zapraszamy.')
    else:
        print(f'ERROR: Rejestracja {plates} już istnieje w bazie.')
    return



def paymentCalculation(registration):
    # Funkcja wylicza należną płatność na podstawie czasu wjazdu na parking oraz czasu realizowanej płatności.
    # Funkcja zagnieżdżona w funkcji payment()
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
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
            return paymentRequired
        else:
            print('Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.')


def paymentValidation(registration):
    # Funkcja sprawdza czy płatność została uiszczona podczas wykorzystania funkcji canLeave.
    # Funkcja zagnieżdżona w funkcji canLeave()
    # Różnica między paymentCalculation jest taka, że walidacja płatności obejmuje dodatkowy czas na opuszczenie parkingu
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
    # Ta funkcja sprawdza czy pojazd o podanym numerze rejestracyjnym ma opłacony parking i może wyjechać.
    # Funkcja zagnieżdżona w funkcji exit()
    get = Query()
    car = db.get(get.plates == registration)
    moneyPaid = car['moneyPaid']
    balance = moneyPaid - paymentValidation(registration)
    if balance < 0:
        return False
    elif balance >= 0:
        return True



def payment():
    # Ta funkcja odpowiada za realizację płatności.
    # Funkcja do wykorzystania w terminalu płatniczym.
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


def exit():
    # Fukncja odpowiada za wyjazd samochodu z parkingu, walidację płatności oraz usunięcie pojazdu z bazy danych
    # Funkcja do wykorzystania przy szlabanie wyjazdowym
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
