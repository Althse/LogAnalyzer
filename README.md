# Analizator Logów (Log Analyzer)

## Opis Projektu
To narzędzie do analizy logów w języku Python, stworzone jako projekt końcowy kursu CS50. Skrypt parsuje logi serwerów (np. SSH), zlicza nieudane próby logowania i identyfikuje najczęściej atakujące adresy IP.

## Funkcjonalności
* Parsuje pliki logów i wyodrębnia kluczowe dane.
* Zlicza całkowitą liczbę nieudanych prób logowania.
* Zlicza całkowitą liczbę udanych połączeń.
* Generuje listę top 5 najczęściej atakujących adresów IP.

## Jak Uruchomić
1.  **Sklonuj repozytorium:**
    ```bash
    git clone [https://github.com/Althse/LogAnalyzer]
    ```
2.  **Przejdź do folderu projektu:**
    ```bash
    cd LogAnalyzer
    ```
3.  **Utwórz i aktywuj wirtualne środowisko:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # lub: venv\Scripts\activate  # Windows
    ```
4.  **Uruchom skrypt, podając plik logów jako argument:**
    ```bash
    python3 analyzer.py example_logs.txt
    ```


## Przykład Użycia

Poniżej znajduje się przykład outputu po uruchomieniu skryptu z plikiem `example_logs.txt`:

======================================== 
         LOG ANALYSIS SUMMARY
======================================== 


Total failed login attempts: 3
Total accepted connections: 2

Top attacking IP addresses:

    203.0.113.1: 3 attempts

    198.51.100.2: 2 attempts
========================================

## Autor
* [Sławomir Cieślik]
* **LinkedIn:** [https://www.linkedin.com/in/s%C5%82awomir-cie%C5%9Blik-646bb6bb/]
* **GitHub:** [https://github.com/Althse]


