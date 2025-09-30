from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from handlers.handler import handle_message

router = APIRouter()

@router.post("/whatsapp/incoming")
async def whatsapp_webhook(request: Request):
    """
    Endpoint Twilio will call when a new WhatsApp message arrives.
    """
    form = await request.form()
    incoming_msg = form.get("Body", "").strip()
    sender = form.get("From", "")

    response_text = await handle_message(incoming_msg, sender)

    return PlainTextResponse(content=response_text)
