Automatyczny parking

MVP

Aplikacja ma na celu automatyczną obsługę parkingu, kontrolowanie ilości dostępnych miejsc, rejestrowanie opłat bez konieczności używania biletów. 

Baza danych
Funkcje bazy danych
Baza danych ma przechowywać rejestr samochodów, które wjechały na teren parkingu oraz usuwać samochody z bazy, które wyjechały. Jednocześnie w każdym rekordzie powinny być zapisane dane dodatkowe, wymienione poniżej.
Baza danych powinna posiadać skonfigurowany limit miejsc oraz system informowania o kończących się zasobach miejsc. Treshold dla konkretnych powiadomień powinien być również konfigurowalny
Baza powinna mieć ciągły licznik zajętych i wolnych miejsc w bazie, wyliczanych na podstawie skonfigurowanego limitu.
Baza danych będzie miała zapis w formacie JSON i powinna zawierać obiekt samochodu wraz z danymi, takimi jak:
- plates - numer rejestracyjny [str]
- enterTime - Timestamp – unix [float]
- moneyPaid : kwota dotychczasowych wpłat [int]

Aplikacja
Aplikacja ma prowadzić rejestr samochodów wjeżdżających na parking, prowadzić system wyliczający opłatę za parkowanie oraz usuwać samochody z bazy, które opuszczają parking po uprzednim rozliczeniu.
Konfiguracja aplikacji
Konfiguracja powinna zawierać listę zmiennych, które będą łatwo dostępne do edycji. Lista zmiennych:
- price - stawka za każdą rozpoczętą godzinę parkowania
- timeToLeave – czas na wyjazd z parkingu liczony od dokonania opłaty do wyjazdu
- maxDbRecords – integer definiujący maksymalną liczbę zapisanych rekordów w bazie (rozmiar parkingu)
- alertRecordNumber – integer definiujący próg, po przekroczeniu którego uruchamiany jest alert o niewielkiej liczbie wolnych miejsc
Rejestrowanie samochodów
Dedykowana funkcja do wprowadzania samochodów do bazy danych. Funkcja powinna tworzyć obiekt JSON, na podstawie inputu w postaci numeru rejestracyjnego. Obiekt będzie zawierał nr rejestracyjny jako klucz, ustawiał czas wjazdu zgodnie z timestampem czasu bieżącego oraz tworzył flagę isPaid, ustawioną by default na False.
Rozliczanie należności za postój
Funkcja powinna prosić o input w postaci numeru rejestracyjnego. Po wprowadzeniu numeru zaciąga obiekt JSON z bazy po kluczu „plates”. Kolejnym krokiem będzie utworzenie zmiennej paymentTime wartości czasu bieżącego w formie timestampu (format do zdefiniowania). Wyliczenie różnicy między paymentTime a enterTime, który wyznaczy czas parkowania i zapisze w postaci nowej zmiennej parkingTime. 
Wzór na wyliczenie opłaty:
Jeśli zmienna parkingTime będzie zawierała minutnik o wartości 0:
	Stawka (price) jest mnożona przez liczbę godzin.
Jeśli zmienna parkingTime będzie zawierała minutnik o wartości > 0
	Stawka (price) jest mnożona przez (liczbę godzin +1)
Kolejnym etapem funkcji będzie wyświetlenie należności. Po wprowadzeniu kwoty (input) funkcja ustawia flagę isPaid na True.
Wyjazd z parkingu
Po wprowadzeniu nr rejestracyjnego samochodu opuszczającego parking, funkcja powinna wyciągnąć z bazy danych rekord po kluczu „plates”. 
Jeśli flaga isPaid = True 
	usunąć rekord z bazy.
Jeśli flaga isPaid = False
	wyświetl komunikat o nieopłaconym parkingu

Czas na opuszczenie parkingu
Po wprowadzeniu zmiennej paymentTime do bazy danych powinno zacząć się odliczanie czasu określonego w konfiguracji jako timeToLeave. Jeśli po upływie skonfigurowanego czasu rekord dalej istnieje w bazie, funkcja powinna zmienić flagę isPaid na False

Post MVP
Aplikacja
Licznik miejsc postojowych
Przy każdym zapisie oraz usunięciu rekordu z bazy powinna być pobierana liczba zapisanych rekordów. Zmienne powinny być zapisywane w pamięci podręcznej (do rozważenia Redis)
Alerty dostępności miejsc oparte na tresholdach 
Do zdefiniowania w konfiguracji aplikacji są progi highLoad, po przekroczeniu których  będzie się wyświetlał komunikat o poziomie zapełnienia parkingu. 
Jeśli przy zapisie rekordu licznik wolnych miejsc postojowych == 0
	Wyświetl komunikat o braku wolnych miejsc

Dodatkowe informacje
Do zrealizowania aplikacji współpracującej z urządzeniami takimi jak automaty do płatności, szlabany wjazdowe i wyjazdowe itp., potrzebna jest implementacja sygnałów uruchamiających konkretne reakcje (otwarcie/zamknięcie szlabanu itp.)
