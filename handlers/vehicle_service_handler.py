# from utils.search_vehicle_manual_utils import search_manual


# class VehicleServiceHandler:
#     vehicle_options: dict = {
#         "1": "Zhongtong",
#         "2": "Kinglong",
#         "3": "Joylong",
#         "4": "Higer",
#         "5": "BYD-K6",
#         "6": "BLK-E9",
#     }

#     def __init__(self, session):
#         self.session = session
#         self.vehicle = session.get("state", {}).get("model")
#         self.status = session.get("state", {}).get("status")

#     def search_vehicle_manual(self, message) -> str:
#         self.session["state"]["action"] = 3

#         if self.session["state"]["status"] == "awaiting_model":
#             if message in self.vehicle_options:
#                 self.session["state"]["model"] = self.vehicle_options[message]
#                 self.session["state"]["status"] = "awaiting_issue"
#                 return f"Got it. You're working on *{self.session['state']['model']}*. What's the issue?"
#             else:
#                 msg = (
#                     "Which vehicle are you working on?\nPlease reply with the number:\n"
#                 )
#                 for k, v in self.vehicle_options.items():
#                     msg += f"{k}. {v}\n"

#             return str(msg)

#         elif self.session["state"]["status"] == "awaiting_issue":
#             query = message
#             results = search_manual(query, self.session["state"]["model"])
#             self.session["state"]["status"] = "done"
#             self.session["state"]["action"] = None

#             if results:
#                 msg = results
#             else:
#                 msg = " Sorry, I couldn't find anything relevant for that issue."
#             return msg

#         else:
#             self.session["state"]["status"] = "awaiting_model"
#             self.session["state"]["model"] = None
#             msg = "Welcome! Which vehicle are you working on?\nPlease reply with the number:\n"
#             for k, v in self.vehicle_options.items():
#                 msg += f"{k}. {v}\n"
#             return str(msg)

from utils.search_vehicle_manual_utils import search_manual


class VehicleServiceHandler:
    vehicle_options: dict = {
        "1": "Zhongtong",
        "2": "Kinglong",
        "3": "Joylong",
        "4": "Higer",
        "5": "BYD-K6",
        "6": "BLK-E9",
    }

    def __init__(self, session):
        self.session = session
        self.vehicle = session.get("state", {}).get("model")
        self.status = session.get("state", {}).get("status")

    def search_vehicle_manual(self, message: str):
        message = message.strip()

        if self.status == "awaiting_model":
            if message in self.vehicle_options:
                selected_vehicle = self.vehicle_options[message]
                self.session["state"]["model"] = selected_vehicle
                self.session["state"]["status"] = "awaiting_issue"
                return (
                    f"✅ Got it. You're working on *{selected_vehicle}*.\n\n"
                    "🔍 What issue are you experiencing?"
                )
            else:
                return self._vehicle_prompt()

        elif self.status == "awaiting_issue":
            query = message
            model = self.session["state"].get("model")
            results = search_manual(query, model)

            # Reset state after search
            self.session["state"]["action"] = None
            self.session["state"]["status"] = None
            self.session["state"]["model"] = None

            if results:
                return results
            else:
                return "❌ Sorry, I couldn't find anything relevant for that issue."

        else:
            # No known state; start over
            self.session["state"]["status"] = "awaiting_model"
            self.session["state"]["model"] = None
            return self._vehicle_prompt()

    def _vehicle_prompt(self) -> str:
        msg = "🚌 *Which vehicle are you working on?*\nReply with the number:\n"
        for k, v in self.vehicle_options.items():
            msg += f"{k}. {v}\n"
        return msg
