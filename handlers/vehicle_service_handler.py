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

    def search_vehicle_manual(self, message) -> str:
        self.session["state"]["action"] = 3

        if self.session["state"]["status"] == "awaiting_model":
            if message in self.vehicle_options:
                self.session["state"]["model"] = self.vehicle_options[message]
                self.session["state"]["status"] = "awaiting_issue"
                return f"Got it. You're working on *{self.session['state']['model']}*. What's the issue?"
            else:
                msg = (
                    "Which vehicle are you working on?\nPlease reply with the number:\n"
                )
                for k, v in self.vehicle_options.items():
                    msg += f"{k}. {v}\n"

            return str(msg)

        elif self.session["state"]["status"] == "awaiting_issue":
            query = message
            results = search_manual(query, self.session["state"]["model"])
            self.session["state"]["status"] = "done"
            self.session["state"]["action"] = None

            if results:
                msg = results
            else:
                msg = " Sorry, I couldn't find anything relevant for that issue."
            return (msg)

        else:
            self.session["state"]["status"] = "awaiting_model"
            self.session["state"]["model"] = None
            msg = "Welcome! Which vehicle are you working on?\nPlease reply with the number:\n"
            for k, v in self.vehicle_options.items():
                msg += f"{k}. {v}\n"
            return str(msg)