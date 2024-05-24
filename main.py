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

#Bezpłatny czas parkowania [s]
freeTime = 3600
def alert():
    numberOfCars = len(db.all())
    if numberOfCars >= alertRecordNumber:
        return True
    else:
        return False

def emptySlots():
    numberOfCars = len(db.all())
    return parkingCapacity - numberOfCars

def ifExists(plates):
    q = Query()
    existing = db.search(q.plates == plates)
    if existing:
        return True
    else:
        return False
def enter(plates):
    # Funkcja tworzy nowy rekord w bazie danych po wprowadzeniu numeru rejestracyjnego.
    # Funkcja do wykorzystania przy szlabanie wjazdowym
    import time, datetime
    enterTime = time.time()
    enterTimeHuman = datetime.datetime.now().strftime("%H:%M")
    ifExists(plates)
    if not ifExists(plates):
        db.insert({'plates': plates, 'enterTime': enterTime, 'moneyPaid': 0})
        return f'Samochód o tablicach rejestracyjnych {plates} wjechał na parking o godzinie {enterTimeHuman}'
    else:
        return (f'ERROR: Rejestracja {plates} już istnieje w bazie.')




def paymentCalculation(plates):
    # Funkcja wylicza należną płatność na podstawie czasu wjazdu na parking oraz czasu realizowanej płatności.
    # Funkcja zagnieżdżona w funkcji payment()
    import time
    get = Query()
    car = db.get(get.plates == plates)
    while not ifExists(plates):
        return 'Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.'
        car = db.get(get.plates == input('Wprowadź numer rejestracyjny: '))
    else:
        if 'enterTime' in car:
            enterTime = (car['enterTime'])
            exitTime = time.time()
            parkingTime = exitTime - enterTime - freeTime
            parkingHours = int(parkingTime / 3600)
            parkingMinutes = int((parkingTime % 3600) / 60)
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
            return paymentRequired
        else:
            return'Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.'


def paymentValidation(plates):
    # Funkcja sprawdza czy płatność została uiszczona podczas wykorzystania funkcji canLeave.
    # Funkcja zagnieżdżona w funkcji canLeave()
    # Różnica między paymentCalculation jest taka, że walidacja płatności obejmuje dodatkowy czas na opuszczenie parkingu
    import time
    get = Query()
    car = db.get(get.plates == plates)
    if not ifExists(plates):
        return'Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.'
        car = db.get(get.plates == plates)
    else:
        if 'enterTime' in car:
            enterTime = (car['enterTime'])
            exitTime = time.time() - timeToLeave
            parkingTime = exitTime - enterTime - freeTime
            parkingHours = int(parkingTime / 3600)
            parkingMinutes = int((parkingTime % 3600) / 60)
            paymentRequired = None
            if parkingMinutes == 0:
                paymentRequired = parkingHours * pricePerHour
                return paymentRequired
            else:
                paymentRequired = int((parkingHours + 1) * pricePerHour)
                return paymentRequired
        else:
            return'Brak danych dotyczących czasu wjazdu. Skontaktuj się z administratorem.'







def paymentRequired(plates):
    q = Query()
    existing = db.search(q.plates == plates)
    if existing:
        import time
        plates = plates.upper()
        query = Query()
        car = db.get(query.plates == plates)
        enterTime = (car['enterTime'])
        exitTime = time.time()
        parkingTime = exitTime - enterTime - freeTime
        parkingHours = int(parkingTime / 3600)
        parkingMinutes = int((parkingTime % 3600) / 60)
        paymentRequired = paymentCalculation(plates)
        missingPayment = paymentRequired - car['moneyPaid']
        return missingPayment
    else:
        return 'Samochód nie znajduje się w bazie danych. Wprowadź poprawny numer rejestracyjny'

def payment(plates, money):
    if ifExists(plates):
        if money == "":
            return 'Wprowadź kwotę płatności'
        else:
            paymentMade = int(money)
            plates = plates.upper()
            query = Query()
            car = db.get(query.plates == plates)
            currentBalance = car['moneyPaid']
            newBalance = currentBalance + paymentMade
            db.update({'moneyPaid': newBalance}, Query().plates == plates)
            paymentNeeded = int(paymentRequired(plates))
            if paymentNeeded > 0:
                return f'Pozostała kwota do zapłaty to: {paymentNeeded}zł.'
            elif paymentNeeded < 0:
                refund = paymentNeeded*(-1)
                balanceAfterRefund = newBalance - refund
                db.update({'moneyPaid': balanceAfterRefund}, Query().plates == plates)
                return f'Reszta: {refund}zł.'
            else:
                db.update({'moneyPaid': newBalance}, Query().plates == plates)
                return 'Parking opłacony, dziękujemy.'
    else:
        return 'ERROR: Błędny numer rejestracyjny.'


def canLeave(plates):
    # Ta funkcja sprawdza czy pojazd o podanym numerze rejestracyjnym ma opłacony parking i może wyjechać.
    # Funkcja zagnieżdżona w funkcji exit()
    import time
    get = Query()
    car = db.get(get.plates == plates)
    enterTime = (car['enterTime'])
    exitTime = time.time() - timeToLeave
    parkingTime = exitTime - enterTime - freeTime
    parkingHours = int(parkingTime / 3600)
    parkingMinutes = int((parkingTime % 3600) / 60)
    moneyPaid = car['moneyPaid']
    balance = moneyPaid - paymentValidation(plates)
    if parkingHours <= 0 and parkingMinutes <= 0:
        return True
    elif balance >= 0:
        return True
    elif balance < 0:
        return False


def exit(plates):
    # Fukncja odpowiada za wyjazd samochodu z parkingu, walidację płatności oraz usunięcie pojazdu z bazy danych
    # Funkcja do wykorzystania przy szlabanie wyjazdowym
    plates = plates.upper()
    get = Query()
    car = db.get(get.plates == plates)
    if not ifExists(plates):
        return 'Błędny numer rejestracyjny. Brak samochodu w bazie. Spróbuj ponownie.'
    else:
        if canLeave(plates):
            db.remove(get.plates == plates)
            return f'Dziękujemy za pobyt, samochód o numerach {plates} został opłacony. Zapraszamy ponownie.'
        else:
            return 'Brak pełnej opłaty za pobyt. Proszę uregulować należność.'
