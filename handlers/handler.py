from twilio.twiml.messaging_response import MessagingResponse

from database.database import get_session, save_session
from handlers.vehicle_service_handler import VehicleServiceHandler
from settings import logger


class WhatsAppHandler:
    def __init__(
        self, user_id: str, message: str, media_url: str = None, media_type: str = None
    ):
        self.user_id = user_id
        self.message = message.strip()
        self.media_url = media_url
        self.media_type = media_type
        self.response = MessagingResponse()
        self.session = get_session(user_id)

    async def handle(self) -> MessagingResponse:
        self.session["history"].append(self.message)
        logger.info("session", self.session)
        action = self.session.get("state", {}).get("action")
        if self.message:
            result = self.handle_text(action)
        else:
            result = self.handle_fallback(action)
        save_session(self.user_id, self.session)
        return result

    def is_pdf(self):
        return self.media_url and "pdf" in (self.media_type or "")

    def handle_text(self, action: str) -> MessagingResponse:
        text = self.message.lower()
        commands = {
            "help": self._help,
            "hi": self._greet,
            "hello": self._greet,
            "1": VehicleServiceHandler(self.session).search_vehicle_manual,
            "2": self._help,
        }
        logger.info("action handle text", action, type(action))
        logger.info("action handle text", text)
        if not action:
            logger.info("not action", action)
            logger.info(self.session)
            logger.info("action", action)
            logger.info(text)
            handler = commands.get(text, self._unknown)
            result = self.response.message(handler(text))
            logger.info(text, result)
        else:
            handler = commands.get(str(action), self._unknown)
            results = handler(text)
            result = (
                [str(self.response.message(res)) for res in results]
                if type(results) == list
                else (self.response.message(results))
            )
            logger.info(text, result)
        return self.response

    def handle_fallback(self, message):
        message = "❓ I didn’t understand that. Please type 'help' to see what I can assist with."
        return message

    @staticmethod
    def _help(message) -> str:
        return (
            "📖 *Help Menu:*\n"
            "1️⃣ Search vehicle manual\n"
            "Reply with the number of your choice (e.g. 1)."
        )

    @staticmethod
    def _greet(message) -> str:
        return (
            "👋 Hello! Please choose an option below:\n\n"
            "1️⃣ Search vehicle manual\n"
            "2️⃣ Help\n\n"
            "Reply with the number of your choice (e.g. 1)."
        )

    @staticmethod
    def _unknown(message) -> str:
        return "❓ I didn’t understand that. Type 'help' to see what I can do."
