# UNIX - skrypty
1. Napisz skrypt liczący, ile plików, katalogów i symlinków jest w katalogu podanym jako pierwszy parametr skryptu. Jeżeli nie podano parametru, sprawdź katalog bieżący; jeżeli podano więcej niż 1 parametr, sprawdź pierwszy z nich, a pozostałe wypisz z komunikatem "Parametr nadliczbowy".

2. Argument - nazwa użytkownika. Jeśli nie podany, kończy działanie z wypisaniem składni uruchomienia. Jeśli więcej argumentów, to tylko pierwszy nas interesuje.
	W pętli nieskończonej przerywanej przez CTRL-C co ok. 2 s wypisuje łączny rozmiar pamięci rezydentnej zajmowanej przez procesy użytkownika o podanej nazwie

3. 1 argument - sciezka dostepu do katalogu. Sprawdza, czy istnieje, jesli nie - wypisuje komunikat i konczy prace. Jesli bez argumentu, to pracuje w kat. biezacym. Jesli wiecej arg to tylko dla pierwszego.
	Obliczyc sumaryczny rozmiar plikow regularnych w bajtach znajdujacych sie w sprecyzowanym katalogu, do ktorych uzytkownik, ktory uruchomil skrypt, ma prawo odczytu. wypisac na stdout.

4. Wylistować użytkowników, którzy nie są zalogowani w systemie, a których procesy są wykonywane.

5. Zsumować i podać RSS procesów dla każdego z użytkowników (podanych jako argument lub z wejścia)

6. Obliczyć średni rozmiar pliku regularnego w katalogu podanym jako arg. (lub w kat. bieżącym, gdy bez arg.). Jeśli ścieżka nie wskazuje katalogu, to błąd.

7. Napisz skrypt, który sprawdzi ilość procesów działających dłużej niż czas podany w sekundach do pierwszego parametru. Przy braku parametrów ma się upomnieć, ma też pominąć dalsze niż pierwszy.

8. Jeden argument (w razie czego dopytać): nazwa usera, w pętli nieskończonej co parę sekund sprawdzać, czy jest zalogowany - jeśli jest, to krzyczy, że jest - i kończy działanie.
