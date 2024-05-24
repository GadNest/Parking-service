from tinydb import TinyDB, Query
import main

db = TinyDB('db.json')
def ClearDB():
    #Funkcja do czyszczenia bazy danych
    db.remove(Query())
    print(db.all())

def deleteCar(registration):
    #Funkcja do usuwania wybranego samochodu z bazy
    query = Query()
    db.remove(query.plates == registration)


registration = input('Auto do usunięcia: ')
deleteCar(registration)
