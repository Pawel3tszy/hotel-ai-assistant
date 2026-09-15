import re


class RestaurantBooking:
    def __init__(self):
        self.active = False
        self.time = None
        self.people = None
        self.awaiting_confirmation = False

    def start(self):
        self.active = True
        self.time = None
        self.people = None
        self.awaiting_confirmation = False

        return "Na którą godzinę chcesz zarezerwować stolik?"

    def handle_message(self, message):
        message = message.lower().strip()

        if self.time is None:
            return self._handle_time(message)

        if self.people is None:
            return self._handle_people(message)

        if self.awaiting_confirmation:
            return self._handle_confirmation(message)

    def _handle_time(self, message):
        match = re.search(
            r"\b([01]?\d|2[0-3])[:.]([0-5]\d)\b",
            message
        )

        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))

            self.time = f"{hour:02d}:{minute:02d}"

        elif message.isdigit() and 0 <= int(message) <= 23:
            self.time = f"{int(message):02d}:00"

        else:
            return "Podaj godzinę, np. 19:00."

        return "Dla ilu osób zarezerwować stolik?"

    def _handle_people(self, message):
        numbers = {
            "jedna": 1,
            "jednej": 1,
            "dwie": 2,
            "dwóch": 2,
            "dwoch": 2,
            "trzy": 3,
            "cztery": 4,
            "pięć": 5,
            "piec": 5,
            "sześć": 6,
            "szesc": 6
        }

        if message.isdigit():
            people = int(message)

        else:
            people = None

            for word, number in numbers.items():
                if word in message:
                    people = number
                    break

        if people is None or people <= 0:
            return "Podaj liczbę osób."

        self.people = people
        self.awaiting_confirmation = True

        return (
            "Podsumowanie rezerwacji:\n"
            f"Godzina: {self.time}\n"
            f"Liczba osób: {self.people}\n\n"
            "Czy potwierdzasz?"
        )

    def _handle_confirmation(self, message):
        if message in ["tak", "potwierdzam", "ok"]:
            self.reset()

            return "Prośba o rezerwację stolika została przyjęta."

        if message in ["nie", "anuluj", "anuluje", "anuluję"]:
            self.reset()

            return "Rezerwacja stolika została anulowana."

        return "Potwierdzasz rezerwację? Odpowiedz tak lub nie."

    def reset(self):
        self.active = False
        self.time = None
        self.people = None
        self.awaiting_confirmation = False