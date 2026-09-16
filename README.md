# Hotel AI Assistant

Prototyp tekstowego asystenta AI dla hotelu, pełniącego rolę wirtualnego konsjerża.

## Opis projektu

Aplikacja umożliwia gościowi prowadzenie rozmowy z asystentem hotelowym, zadawanie pytań dotyczących obiektu oraz korzystanie z wybranych usług hotelowych.

System rozpoznaje, czy wiadomość użytkownika dotyczy jednej z obsługiwanych akcji, takich jak room service, zamówienie ręczników, ustawienie budzenia czy rezerwacja stolika lub masażu.

W przypadku pytań informacyjnych aplikacja wyszukuje odpowiednie dane w bazie wiedzy hotelu, a następnie przekazuje je wraz z kontekstem rozmowy do modelu językowego, który generuje odpowiedź.

Projekt ma modułową strukturę i umożliwia zmianę konfiguracji oraz bazy wiedzy dla różnych hoteli.

## Funkcje

- odpowiadanie na pytania dotyczące hotelu,
- wyszukiwanie informacji w bazie wiedzy,
- pamięć kontekstu rozmowy,
- rozpoznawanie intencji użytkownika,
- proaktywne pytania i sugestie,
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

1. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

2. Ustaw klucz OpenAI API.

W systemie Windows:

```powershell
setx OPENAI_API_KEY "TWÓJ_KLUCZ_API"
```

Po ustawieniu zmiennej należy ponownie uruchomić terminal lub środowisko programistyczne.

3. Uruchom wersję webową:

```bash
streamlit run streamlit_app.py
```

4. Alternatywnie można uruchomić wersję terminalową:

```bash
python main.py
```