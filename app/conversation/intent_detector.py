def detect_intent(message):
    message_lower = message.lower().strip()

    # -------------------------
    # RĘCZNIKI
    # -------------------------

    if (
        "ręcznik" in message_lower
        or "recznik" in message_lower
    ):
        return "order_towels"

    # -------------------------
    # BUDZENIE
    # -------------------------

    if (
        "budzenie" in message_lower
        or "pobudk" in message_lower
        or "obudź" in message_lower
        or "obudz" in message_lower
    ):
        return "set_wakeup"

    # -------------------------
    # MASAŻ / SPA - REZERWACJA
    # -------------------------

    if (
        ("masaż" in message_lower or "masaz" in message_lower)
        and (
            "chcę" in message_lower
            or "chce" in message_lower
            or "zarezerw" in message_lower
            or "umów" in message_lower
            or "umow" in message_lower
        )
    ):
        return "book_spa"

    # -------------------------
    # RESTAURACJA - REZERWACJA
    # -------------------------

    if (
        "stolik" in message_lower
        and (
            "chcę" in message_lower
            or "chce" in message_lower
            or "zarezerw" in message_lower
            or "rezerwac" in message_lower
        )
    ):
        return "book_restaurant"

    # -------------------------
    # WODA / ROOM SERVICE
    # -------------------------

    if (
        "woda" in message_lower
        or "wodę" in message_lower
        or "wode" in message_lower
        or "butelkę wody" in message_lower
        or "butelke wody" in message_lower
    ):
        return "order_water"

    # Brak konkretnej akcji = zwykła rozmowa RAG + LLM
    return None