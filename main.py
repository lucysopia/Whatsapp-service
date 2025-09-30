

from fastapi import FastAPI
from routers.router import router


app = FastAPI(
    title="BasiGo WhatsApp Service Bot",
    description="Helps engineers troubleshoot bus issues using RAG",
    version="1.0.0"
)

# Register routes
app.include_router(router)

@app.get("/")
def root():
    return {"status": "BasiGo WhatsApp Service Bot is running!"}