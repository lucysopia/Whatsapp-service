from utils.rag_helper import query_rag

# simple in-memory session store
user_sessions = {}

async def handle_message(incoming_msg: str, sender: str) -> str:
    """
    Handle an incoming WhatsApp message.
    """

    # Normalize input
    msg = incoming_msg.strip()

    # If sender has not chosen a bus model yet
    if sender not in user_sessions or user_sessions[sender].get("bus_model") is None:
        # Check if the user is trying to set a bus model
        available_models = ["BLK-E9", "BYD-K6", "Higer", "Joylong", "Kinglong", "Zhongtong"]

        if msg in available_models:
            # Store chosen bus model
            user_sessions[sender] = {"bus_model": msg}
            return f" Bus model set to {msg}. Now ask me a question about it."

        else:
            # Ask them to specify bus model
            return "Please specify the bus model (BLK-E9, BYD-K6, Higer, Joylong, Kinglong, Zhongtong)."

    # Otherwise, user already has a bus model selected
    bus_model = user_sessions[sender]["bus_model"]

    # If user wants to change model
    if msg.lower().startswith("change model"):
        user_sessions[sender]["bus_model"] = None
        return "Okay, please specify the new bus model."

    # Run RAG query
    answer = query_rag(bus_model, msg)
    return answer
