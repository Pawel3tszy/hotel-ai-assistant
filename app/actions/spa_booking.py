import re


class SpaBooking:
    def __init__(self):
        self.active = False
        self.massage_type = None
        self.time = None
        self.price = None
        self.duration = None
        self.awaiting_confirmation = False

    def start(self):
        self.active = True
        self.massage_type = None
        self.time = None
        self.price = None
        self.duration = None
        self.awaiting_confirmation = False

        return (
            "Jaki masaż chcesz zarezerwować: "
            "klasyczny czy relaksacyjny?"
        )

    def handle_message(self, message):
        message = message.lower().strip()

        if self.massage_type is None:
            return self._handle_massage_type(message)

        if self.time is None:
            return self._handle_time(message)

        if self.awaiting_confirmation:
            return self._handle_confirmation(message)

    def _handle_massage_type(self, message):
        if "klasycz" in message:
            self.massage_type = "klasyczny"
            self.duration = 50
            self.price = 150

        elif "relaks" in message:
            self.massage_type = "relaksacyjny"
            self.duration = 60
            self.price = 180

        else:
            return "Wybierz masaż klasyczny albo relaksacyjny."

        return "Na którą godzinę chcesz zarezerwować masaż?"

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
            return "Podaj godzinę, np. 17:00."

        self.awaiting_confirmation = True

        return (
            "Podsumowanie rezerwacji:\n"
            f"Masaż: {self.massage_type}\n"
            f"Czas trwania: {self.duration} minut\n"
            f"Godzina: {self.time}\n"
            f"Cena: {self.price} zł\n\n"
            "Czy potwierdzasz?"
        )

    def _handle_confirmation(self, message):
        if message in ["tak", "potwierdzam", "ok"]:
            self.reset()

            return (
                "Prośba o rezerwację masażu została przyjęta."
            )

        if message in ["nie", "anuluj", "anuluje", "anuluję"]:
            self.reset()

            return "Rezerwacja masażu została anulowana."

        return "Potwierdzasz rezerwację? Odpowiedz tak lub nie."

    def reset(self):
        self.active = False
        self.massage_type = None
        self.time = None
        self.price = None
        self.duration = None
        self.awaiting_confirmation = False