from utils.rag_helper import query_rag

# simple in-memory session store
user_sessions = {}

# Define available bus models globally
available_models = ["BLK-E9", "BYD-K6", "Higer", "Joylong", "Kinglong", "Zhongtong"]

async def handle_message(incoming_msg: str, sender: str) -> str:
    """
    Handle an incoming WhatsApp message.
    """

    # Normalize input
    msg = incoming_msg.strip()

    # If sender has not chosen a bus model yet
    if sender not in user_sessions or user_sessions[sender].get("bus_model") is None:

        # If user entered a number (e.g., 1, 2, 3)
        if msg.isdigit():
            index = int(msg) - 1
            if 0 <= index < len(available_models):
                selected_model = available_models[index]
                user_sessions[sender] = {"bus_model": selected_model}
                return f" Bus model set to *{selected_model}*. Now ask me a question about it."
            else:
                return " Invalid option. Please reply with a number from the list."

        # If user typed the model name directly
        elif msg in available_models:
            user_sessions[sender] = {"bus_model": msg}
            return f" Bus model set to *{msg}*. Now ask me a question about it."

        # Otherwise, show the list of models
        else:
            model_list = "\n".join([f"{i+1}. {model}" for i, model in enumerate(available_models)])
            return f"Please select your bus model by typing the number or name:\n\n{model_list}"

    # If user wants to change model
    if msg.lower().startswith("change model"):
        user_sessions[sender]["bus_model"] = None
        model_list = "\n".join([f"{i+1}. {model}" for i, model in enumerate(available_models)])
        return f"Okay, please choose the new bus model:\n\n{model_list}"

    # Otherwise, user already has a bus model selected
    bus_model = user_sessions[sender]["bus_model"]

    # Run RAG query
    answer = query_rag(bus_model, msg)
    return answer
