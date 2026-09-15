# Hotel AI Assistant

Prototyp tekstowego asystenta AI dla hotelu, wykorzystującego architekturę RAG.

## Opis projektu

Aplikacja pełni rolę wirtualnego hotelowego konsjerża. Odpowiada na pytania gości na podstawie przygotowanej bazy wiedzy hotelu, pamięta kontekst rozmowy oraz obsługuje wybrane scenariusze hotelowe.

Projekt wykorzystuje architekturę RAG, dzięki czemu odpowiedzi są generowane na podstawie danych zapisanych w bazie wiedzy hotelu.

## Funkcje

- odpowiadanie na pytania dotyczące hotelu,
- wyszukiwanie semantyczne w bazie wiedzy,
- pamięć kontekstu rozmowy,
- proaktywne pytania i sugestie,
- rozpoznawanie intencji użytkownika,
- obsługa wybranych scenariuszy:
  - room service,
  - dodatkowe ręczniki,
  - budzenie,
  - rezerwacja masażu,
  - rezerwacja stolika,
- podsumowanie akcji przed potwierdzeniem,
- interfejs czatu w Streamlit,
- możliwość konfiguracji rozwiązania dla różnych hoteli.

## Technologie

- Python 3.11
- OpenAI API
- Sentence Transformers
- NumPy
- Streamlit

## Jak działa RAG

Dokumenty zawierające informacje o hotelu są wczytywane przez aplikację i dzielone na mniejsze fragmenty.

Każdy fragment jest zamieniany na embedding. Pytanie użytkownika również jest zamieniane na embedding, a następnie system wyszukuje najbardziej podobne fragmenty bazy wiedzy.

Wybrane informacje są przekazywane do modelu językowego jako kontekst do wygenerowania odpowiedzi.

## Struktura projektu

```text
hotel-ai-assistant/
│
├── app/
│   ├── actions/
│   ├── config/
│   ├── conversation/
│   ├── llm/
│   └── rag/
│
├── hotels/
│   └── aurora_poznan/
│       ├── config.json
│       └── knowledge/
│
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Uruchomienie

### 1. Instalacja zależności

Po pobraniu projektu zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

### 2. Konfiguracja klucza OpenAI API

Aplikacja wymaga klucza OpenAI API.

W systemie Windows można ustawić go w PowerShellu:

```powershell
setx OPENAI_API_KEY "TWÓJ_KLUCZ_API"
```

Po ustawieniu zmiennej należy ponownie uruchomić terminal lub środowisko programistyczne.

### 3. Uruchomienie aplikacji webowej

```bash
streamlit run streamlit_app.py
```

Aplikacja zostanie uruchomiona w przeglądarce.

### 4. Uruchomienie wersji terminalowej

Alternatywnie można uruchomić aplikację bez interfejsu webowego:

```bash
python main.py
```