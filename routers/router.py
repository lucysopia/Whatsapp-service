from fastapi import APIRouter, Form
from starlette.responses import Response

from handlers.handler import WhatsAppHandler

twilio_router = APIRouter()


@twilio_router.post("/whatsapp")
async def whatsapp_router(
    Body: str = Form(""),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None),
    From: str = Form(None),
):
    print(Body,From)
    handler = WhatsAppHandler(
        user_id=From, message=Body, media_url=MediaUrl0, media_type=MediaContentType0
    )
    # Get TwiML string from handler
    twiml_response = await handler.handle()
    print(twiml_response)
    # Ensure the response is a stringified XML (TwiML)
    return Response(content=twiml_response.to_xml(), media_type="application/xml")