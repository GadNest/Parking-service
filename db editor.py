from tinydb import TinyDB, Query
import Main

db = TinyDB('db.json')
def ClearDB():
    #Funkcja do czyszczenia bazy danych
    db.remove(Query())
    print(db.all())
