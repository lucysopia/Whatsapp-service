# Bus Manual WhatsApp Assistant

A FastAPI + Twilio-based application that allows users to query electric bus manuals via WhatsApp.

## Features
- Query bus manuals (BYD-K6, BYD-E9, TATA, etc.)
- Uses FAISS + OpenAI for semantic search
- WhatsApp interface via Twilio
- Simple state management per user


##  Project Structure

Whatsapp-service/
├── handlers/
│ ├── init.py
│ ├── handler.py
├──Routers/
├  ├── router.py
├── utils/
│ ├── init.py
│ ├── update_pdf_index.py
│ ├── rag_helper.py
├── vectorstore/ # FAISS indexes (add here from Colab or build locally)
├── main.py
├── settings.py
├── requirements.txt
└── README.md


##  Setup Instructions

 1. Clone the repository

2. Create a virtual environment with:
 OPENAI_API_KEY=your_key
 PDF_DIR=manuals/
 INDEX_DIR=vectorstore/

3. Install dependencies-pip install -r requirements.txt

4. Build indexes (optional, in Colab or local):
  python utils/update_pdf_index.py

5. Run FastAPI server:
 uvicorn main:app --reload

6. Connect with Twilio Sandbox for WhatsApp

Add your Twilio credentials:
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
