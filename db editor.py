from tinydb import TinyDB, Query

db = TinyDB('db.json')
def ClearDB():
    #Funkcja do czyszczenia bazy danych
    db.remove(Query())
    print(db.all())
