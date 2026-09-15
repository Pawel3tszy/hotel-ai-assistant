import streamlit as st

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


HOTEL_ID = "aurora_poznan"

hotel_config = load_hotel_config(HOTEL_ID)

hotel_name = hotel_config["name"]
knowledge_base = hotel_config["knowledge_base"]


st.set_page_config(
    page_title=hotel_name,
    page_icon="🏨",
    layout="centered"
)


@st.cache_resource
def prepare_knowledge_base():
    documents = load_documents(knowledge_base)
    chunks = split_documents(documents)
    chunks = create_embeddings(chunks)

    return chunks


chunks = prepare_knowledge_base()


def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()

    if "room_service" not in st.session_state:
        st.session_state.room_service = RoomServiceOrder()

    if "towels" not in st.session_state:
        st.session_state.towels = TowelsOrder()

    if "wakeup" not in st.session_state:
        st.session_state.wakeup = WakeupOrder()

    if "spa_booking" not in st.session_state:
        st.session_state.spa_booking = SpaBooking()

    if "restaurant_booking" not in st.session_state:
        st.session_state.restaurant_booking = RestaurantBooking()


initialize_session()


def process_message(query):
    room_service = st.session_state.room_service
    towels = st.session_state.towels
    wakeup = st.session_state.wakeup
    spa_booking = st.session_state.spa_booking
    restaurant_booking = st.session_state.restaurant_booking
    memory = st.session_state.memory

    query_lower = query.lower().strip()

    # -------------------------
    # ANULOWANIE AKCJI
    # -------------------------

    cancel_phrases = [
        "anuluj",
        "rezygnuję",
        "rezygnuje",
        "nie chcę",
        "nie chce",
        "nieważne",
        "niewazne"
    ]

    if any(phrase in query_lower for phrase in cancel_phrases):
        room_service.reset()
        towels.reset()
        wakeup.reset()
        spa_booking.reset()
        restaurant_booking.reset()

        answer = "Jasne, anuluję bieżącą akcję. W czym mogę pomóc?"

        memory.add_user_message(query)
        memory.add_assistant_message(answer)

        return answer

    # -------------------------
    # AKTYWNE PROCESY
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
        memory.add_user_message(query)
        memory.add_assistant_message(answer)

        return answer

    # -------------------------
    # WYKRYWANIE INTENCJI
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
        memory.add_user_message(query)
        memory.add_assistant_message(answer)

        return answer

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

    memory.add_user_message(query)
    memory.add_assistant_message(answer)

    return answer


st.title("🏨 Hotel AI Assistant")

st.caption(
    f"Wirtualny konsjerż — {hotel_name}"
)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


query = st.chat_input("Napisz wiadomość...")


if query:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Chwila..."):
            answer = process_message(query)

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )