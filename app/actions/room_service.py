class RoomServiceOrder:
    def __init__(self):
        self.active = False
        self.water_type = None
        self.size = None
        self.price = None
        self.awaiting_confirmation = False

    def start(self):
        self.active = True
        self.water_type = None
        self.size = None
        self.price = None
        self.awaiting_confirmation = False

        return "Wolisz wodę gazowaną czy niegazowaną?"

    def handle_message(self, message):
        message = message.lower().strip()

        if self.water_type is None:
            return self._handle_water_type(message)

        if self.size is None:
            return self._handle_size(message)

        if self.awaiting_confirmation:
            return self._handle_confirmation(message)

    def _handle_water_type(self, message):
        if "niegaz" in message:
            self.water_type = "niegazowana"

        elif "gaz" in message:
            self.water_type = "gazowana"

        else:
            return "Nie zrozumiałem. Wolisz wodę gazowaną czy niegazowaną?"

        return "Jaką pojemność wybierasz: 0,33 l czy 0,5 l?"

    def _handle_size(self, message):
        if (
                "0,33" in message
                or "0.33" in message
                or "mała" in message
                or "mala" in message
        ):
            self.size = "0,33 l"
            self.price = 6

        elif (
                "0,5" in message
                or "0.5" in message
                or "duża" in message
                or "duza" in message
        ):
            self.size = "0,5 l"
            self.price = 8

        else:
            return "Wybierz proszę pojemność 0,33 l albo 0,5 l."

        self.awaiting_confirmation = True

        return (
            "Podsumowanie zamówienia:\n"
            f"Woda {self.water_type} {self.size}\n"
            f"Cena: {self.price} zł\n\n"
            "Czy potwierdzasz zamówienie?"
        )

    def _handle_confirmation(self, message):
        if message in ["tak", "potwierdzam", "zamawiam", "ok"]:
            self.reset()
            return "Zamówienie zostało przyjęte."

        if message in ["nie", "anuluj", "anuluję"]:
            self.reset()
            return "Zamówienie zostało anulowane."

        return "Potwierdzasz zamówienie? Odpowiedz tak lub nie."

    def reset(self):
        self.active = False
        self.water_type = None
        self.size = None
        self.price = None
        self.awaiting_confirmation = False