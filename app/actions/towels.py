class TowelsOrder:
    def __init__(self):
        self.active = False
        self.quantity = None
        self.awaiting_confirmation = False

    def start(self):
        self.active = True
        self.quantity = None
        self.awaiting_confirmation = False

        return "Ile dodatkowych ręczników potrzebujesz?"

    def handle_message(self, message):
        message = message.lower().strip()

        if self.quantity is None:
            return self._handle_quantity(message)

        if self.awaiting_confirmation:
            return self._handle_confirmation(message)

    def _handle_quantity(self, message):
        numbers = {
            "jeden": 1,
            "jednego": 1,
            "dwa": 2,
            "dwie": 2,
            "trzy": 3,
            "cztery": 4,
            "pięć": 5,
            "piec": 5
        }

        if message.isdigit():
            quantity = int(message)

        else:
            quantity = None

            for word, number in numbers.items():
                if word in message:
                    quantity = number
                    break

        if quantity is None or quantity <= 0:
            return "Podaj proszę liczbę ręczników."

        self.quantity = quantity
        self.awaiting_confirmation = True

        return (
            "Podsumowanie:\n"
            f"Dodatkowe ręczniki: {self.quantity}\n"
            "Cena: 0 zł\n\n"
            "Czy potwierdzasz?"
        )

    def _handle_confirmation(self, message):
        if message in ["tak", "potwierdzam", "ok"]:
            quantity = self.quantity
            self.reset()

            return f"Zamówienie {quantity} dodatkowych ręczników zostało przyjęte."

        if message in ["nie", "anuluj", "anuluje", "anuluję"]:
            self.reset()
            return "Zamówienie ręczników zostało anulowane."

        return "Potwierdzasz zamówienie? Odpowiedz tak lub nie."

    def reset(self):
        self.active = False
        self.quantity = None
        self.awaiting_confirmation = False