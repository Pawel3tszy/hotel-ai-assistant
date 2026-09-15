import re


class WakeupOrder:
    def __init__(self):
        self.active = False
        self.time = None
        self.awaiting_confirmation = False

    def start(self):
        self.active = True
        self.time = None
        self.awaiting_confirmation = False

        return "Na którą godzinę ustawić budzenie?"

    def handle_message(self, message):
        message = message.lower().strip()

        if self.time is None:
            return self._handle_time(message)

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
            return "Podaj godzinę, np. 07:00."

        self.awaiting_confirmation = True

        return (
            "Podsumowanie:\n"
            f"Budzenie: {self.time}\n\n"
            "Czy potwierdzasz?"
        )

    def _handle_confirmation(self, message):
        if message in ["tak", "potwierdzam", "ok"]:
            wakeup_time = self.time
            self.reset()

            return f"Budzenie na godzinę {wakeup_time} zostało ustawione."

        if message in ["nie", "anuluj", "anuluje", "anuluję"]:
            self.reset()
            return "Budzenie zostało anulowane."

        return "Potwierdzasz budzenie? Odpowiedz tak lub nie."

    def reset(self):
        self.active = False
        self.time = None
        self.awaiting_confirmation = False