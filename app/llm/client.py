from openai import OpenAI


client = OpenAI()


def generate_answer(query, context, history, hotel_name):
    messages = [
        {
            "role": "system",
            "content": (
                f"Jesteś naturalnie rozmawiającym asystentem hotelu {hotel_name}. "
                "Pełnisz rolę hotelowego konsjerża. "

                "Odpowiadaj na podstawie przekazanego kontekstu hotelowego. "
                "Nie wymyślaj informacji, których nie ma w kontekście. "
                "Jeżeli nie znasz odpowiedzi, powiedz wprost, że nie masz takiej informacji. "

                "Prowadź naturalną i krótką rozmowę. "
                "Uwzględniaj wcześniejsze wiadomości użytkownika. "

                "Jeżeli użytkownik poda za mało informacji do wykonania lub przygotowania akcji, "
                "zadaj jedno konkretne pytanie doprecyzowujące. "

                "Jeżeli odpowiedziałeś na pytanie i istnieje naturalnie powiązana usługa hotelowa, "
                "możesz krótko ją zaproponować. "

                "Nie proponuj usług na siłę i nie zadawaj kilku pytań naraz."
            )
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": f"""
Kontekst hotelowy:
{context}

Aktualne pytanie:
{query}
"""
        }
    )

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=messages
    )

    return response.output_text