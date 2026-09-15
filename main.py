from app.rag.loader import load_documents
from app.rag.chunker import split_documents
from app.rag.embedder import create_embeddings
from app.rag.search import search_chunks
from app.llm.client import generate_answer

from app.config.hotel_config import load_hotel_config

from app.conversation.memory import ConversationMemory
from app.conversation.intent_detector import detect_intent

from app.actions.room_service import RoomServiceOrder
from app.actions.towels import TowelsOrder
from app.actions.wakeup import WakeupOrder
from app.actions.spa_booking import SpaBooking
from app.actions.restaurant_booking import RestaurantBooking


# -------------------------
# KONFIGURACJA HOTELU
# -------------------------

HOTEL_ID = "aurora_poznan"

hotel_config = load_hotel_config(HOTEL_ID)

hotel_name = hotel_config["name"]
knowledge_base = hotel_config["knowledge_base"]


# -------------------------
# BAZA WIEDZY
# -------------------------

documents = load_documents(knowledge_base)
chunks = split_documents(documents)
chunks = create_embeddings(chunks)


# -------------------------
# PAMIĘĆ
# -------------------------

memory = ConversationMemory()


# -------------------------
# AKCJE HOTELOWE
# -------------------------

room_service = RoomServiceOrder()
towels = TowelsOrder()
wakeup = WakeupOrder()
spa_booking = SpaBooking()
restaurant_booking = RestaurantBooking()


print(hotel_name)
print("Hotel AI Assistant")
print("Wpisz 'exit', aby zakończyć rozmowę.\n")


while True:
    query = input("Ty: ")

    if query.lower() == "exit":
        print("Bot: Do zobaczenia!")
        break

    # -------------------------
    # AKTYWNE AKCJE
    # -------------------------

    if room_service.active:
        answer = room_service.handle_message(query)

    elif towels.active:
        answer = towels.handle_message(query)

    elif wakeup.active:
        answer = wakeup.handle_message(query)

    elif spa_booking.active:
        answer = spa_booking.handle_message(query)

    elif restaurant_booking.active:
        answer = restaurant_booking.handle_message(query)

    else:
        answer = None

    if answer is not None:
        print(f"Bot: {answer}\n")

        memory.add_user_message(query)
        memory.add_assistant_message(answer)

        continue

    # -------------------------
    # INTENCJE
    # -------------------------

    intent = detect_intent(query)

    if intent == "order_water":
        answer = room_service.start()

    elif intent == "order_towels":
        answer = towels.start()

    elif intent == "set_wakeup":
        answer = wakeup.start()

    elif intent == "book_spa":
        answer = spa_booking.start()

    elif intent == "book_restaurant":
        answer = restaurant_booking.start()

    else:
        answer = None

    if answer is not None:
        print(f"Bot: {answer}\n")

        memory.add_user_message(query)
        memory.add_assistant_message(answer)

        continue

    # -------------------------
    # RAG + LLM
    # -------------------------

    results = search_chunks(query, chunks)

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    history = memory.get_history()

    answer = generate_answer(
        query=query,
        context=context,
        history=history,
        hotel_name=hotel_name
    )

    print(f"Bot: {answer}\n")

    memory.add_user_message(query)
    memory.add_assistant_message(answer)