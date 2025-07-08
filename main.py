from fastapi import FastAPI

from routers.router import twilio_router


app = FastAPI(
    title="WhatsApp AI Bot",
    description="Handles WhatsApp-based PDF bill processing and vehicle manual search",
    version="1.0.0",
)

# Include routers
app.include_router(twilio_router)


@app.get("/")
async def root():
    return {"message": "WhatsApp AI Bot is running!"}
