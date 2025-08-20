
# Bus Manual WhatsApp Assistant

A FastAPI + Twilio-based application that allows users to query electric bus manuals via WhatsApp.


##  Project Structure

- `process_manuals.py` — Extracts and embeds content from PDF manuals, saving them into `manual_chunks.json`.
- `app.py` — FastAPI server that connects to Twilio's WhatsApp Sandbox and responds to queries.
- `manual_chunks.json` — Pre-processed manual data used by the app.
- `utils/` — Utility functions (manual search, OpenAI client, session handling, etc.).
- `handlers/` — Logic for handling WhatsApp interactions.
- `.env` — Environment variable file for Twilio and OpenAI credentials.


##  Setup Instructions

 1. Clone the repository

2. Create a virtual environment

3. Install dependencies-pip install -r requirements.txt

4. Set up your environment variables
Create a .env file in the root directory

Add your Twilio credentials:
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886


## How to Run
Step 1: Preprocess the PDF manuals (run once)
python process_manuals.py

Step 2: Start the FastAPI app
uvicorn app:app --reload --port 5002

Step 3: Start Cloudflare Tunnel (for webhook exposure)
cloudflared tunnel --url http://localhost:5002


Copy the HTTPS forwarding URL shown (e.g., https://abc123.trycloudflare.com)
and paste it into the Twilio WhatsApp sandbox as your webhook URL


## WhatsApp Testing 
Use the Twilio sandbox number (+14155238886)

Join the sandbox with the code from the Twilio console

Send messages through WhatsApp, and the bot will respond with relevant manual sections


## Example Flow
You: Hi
Bot:  Which vehicle are you working on?
     1. Zhongtong
     2. Kinglong
     3. Joylong
     4. Higer
     5. BYD-K6
     6. BLK-E9

You: 1
Bot:  Got it. You're working on Zhongtong.
      What issue are you experiencing?

You: Battery overheating
Bot: Here’s what I found in the Zhongtong manual:
     ...


