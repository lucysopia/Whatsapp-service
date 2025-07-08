from twilio.twiml.messaging_response import MessagingResponse

from database.database import get_session, save_session
from handlers.vehicle_service_handler import VehicleServiceHandler
from settings import logger
from utils.pdf_bill_handler import process_pdf_bill


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

    async def handle(self):
        self.session["history"].append(self.message)
        logger.info("session", self.session)
        action = self.session.get("state", {}).get("action")
        if action == 1 and self.is_pdf():
            result = await self.handle_pdf()
        elif self.message:
            result = self.handle_text(action)
        else:
            result = self.handle_fallback(action)
        save_session(self.user_id, self.session)
        return result

    def is_pdf(self):
        return self.media_url and "pdf" in (self.media_type or "")

    async def handle_pdf(self):
        content = process_pdf_bill(self.media_url)
        self.response.message(f"✅ Bill processed:\n\n{content}")
        return str(self.response)

    def handle_text(self, action: str) -> str:
        text = self.message.lower()
        commands = {
            "help": self._help,
            "summary": self._summary,
            "hi": self._greet,
            "hello": self._greet,
            "1": self._initiate_bill_processing,
            "2": self._report_vehicle_issue,
            "3": VehicleServiceHandler(self.session).search_vehicle_manual,
            "4": self._help,
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
        return result

    def handle_fallback(self, message):
        self.response.message(
            "❓ I didn’t understand that. Please type 'help' to see what I can assist with."
        )
        return str(self.response)

    @staticmethod
    def _help(message) -> str:
        return (
            "📖 *Help Menu:*\n"
            "- Send a PDF bill to get extracted data\n"
            "- Type 'help' to see this menu again"
        )

    @staticmethod
    def _summary(message) -> str:
        # Placeholder — this could come from a DB later
        return "🧾 Your last bill was Ksh 276,143.00 for July."

    @staticmethod
    def _greet(message) -> str:
        return (
            "👋 Hello! Please choose an option below:\n\n"
            "1️⃣ Report latest electricity bill\n"
            "2️⃣ Report a vehicle issue\n"
            "3️⃣ Search vehicle manual\n"
            "4️⃣ Help\n\n"
            "Reply with the number of your choice (e.g. 1 or 3)."
        )

    @staticmethod
    def _unknown(message) -> str:
        return "❓ I didn’t understand that. Type 'help' to see what I can do."

    def _initiate_bill_processing(self, message) -> str:
        if message == 1:
            self.session["state"]["action"] = 1
            self.session["state"]["status"] = "initiated"
            message = "Please upload a pdf bill to process and save the data"
            return message
        elif message == "0":
            self.session["state"]["action"] = None
            self.session["state"]["status"] = None
            return (
                "👋 Hello! Please choose an option below:\n\n"
                "1️⃣ Report latest electricity bill\n"
                "2️⃣ Report a vehicle issue\n"
                "3️⃣ Search vehicle manual\n"
                "4️⃣ Help\n\n"
                "Reply with the number of your choice (e.g. 1 or 3)."
            )
        else:
            return "I did not understand that. Please type 0 to see what actions I can perform."

    def _report_vehicle_issue(self, message) -> str:
        self.session["state"]["2"] = 2
        self.session["state"]["status"] = None
        return "Sorry this feature is not yet developed"
