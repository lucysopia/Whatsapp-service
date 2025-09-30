
from utils.openai_client import ask_openai


from twilio.twiml.messaging_response import MessagingResponse
from database.database import get_session, save_session
from handlers.vehicle_service_handler import VehicleServiceHandler
from settings import logger


class WhatsAppHandler:
    def __init__(self, user_id: str, message: str, media_url: str = None, media_type: str = None):
        self.user_id = user_id.replace("whatsapp:", "") 
        self.message = message.strip()
        self.media_url = media_url
        self.media_type = media_type
        self.response = MessagingResponse()
        self.session = get_session(self.user_id)

        # Ensure state and history keys exist in session
        if "state" not in self.session:
            self.session["state"] = {"action": None, "status": None, "model": None}
        if "history" not in self.session:
            self.session["history"] = []

    async def handle(self) -> MessagingResponse:
        self.session["history"].append(self.message)
        logger.info("session: %s", self.session)

        action = self.session.get("state", {}).get("action")
        logger.info("DEBUG: current state: %s", self.session.get("state"))


        if self.message:
            result = self.handle_text(action)
        else:
            result = self.handle_fallback()

        save_session(self.user_id, self.session)
        logger.info("💾 DEBUG: Session saved for %s: %s", self.user_id, self.session)

        logger.info("SAVED SESSION: %s", self.session)
        return result

    def is_pdf(self):
        return self.media_url and "pdf" in (self.media_type or "")

    def handle_text(self, action: str) -> MessagingResponse:
        text = self.message.lower().strip()
        logger.info("Handling text: '%s' with action: %s", text, action)

        # Define command options
        commands = {
            "help": self._help,
            "hi": self._greet,
            "hello": self._greet,
            "1": VehicleServiceHandler(self.session).search_vehicle_manual,
            "manual": VehicleServiceHandler(self.session).search_vehicle_manual,
            "2": self._help,
        }
        # Check for OpenAI prompt -If the message starts with "ask ai:"

        if text.startswith("ask ai"):
            user_prompt = self.message[len("ask ai"):].strip()
            ai_response = ask_openai(user_prompt)
            self.response.message(ai_response)
            return self.response
        

        # If no action in progress
        if not action:
            if text in ["1", "manual"]:
                self.session["state"] = {
                    "action": "search_vehicle_manual",
                    "status": "awaiting_model",
                    "model": None
                }
            handler = commands.get(text, self._unknown)
            response_text = handler(text)
            self.response.message(response_text)
        else:
            # Continue handling in an active flow
            if action == "search_vehicle_manual":
                handler = VehicleServiceHandler(self.session).search_vehicle_manual
            else:
                handler = self._unknown

            response_texts = handler(text)
            if isinstance(response_texts, list):
                for msg in response_texts:
                    self.response.message(msg)
            else:
                self.response.message(response_texts)

        return self.response

    def handle_fallback(self) -> MessagingResponse:
        return self.response.message(
            "❓ I didn’t understand that. Please type 'help' to see what I can assist with."
        )

    @staticmethod
    def _help(message: str) -> str:
        return (
            "📖 *Help Menu:*\n"
            "1️⃣ Search vehicle manual\n"
            "Reply with the number of your choice (e.g. 1)."
        )

    @staticmethod
    def _greet(message: str) -> str:
        return (
            "👋 Hello! Please choose an option below:\n\n"
            "1️⃣ Search vehicle manual\n"
            "2️⃣ Help\n\n"
            "Reply with the number of your choice (e.g. 1)."
        )

    @staticmethod
    def _unknown(message: str) -> str:
        return "❓ I didn’t understand that. Type 'help' to see what I can do."
