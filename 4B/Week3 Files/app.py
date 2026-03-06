"""
FastAPI Application for JKYog WhatsApp Bot
Main application entry point for Render deployment
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database.models import get_db, init_db
from webhook_handler import handle_twilio_webhook

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI startup and shutdown events.
    """
    # Startup
    print("🚀 Starting JKYog WhatsApp Bot...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        print("   Continuing without database support...")
    
    yield
    
    # Shutdown
    print("👋 Shutting down JKYog WhatsApp Bot...")


# Initialize FastAPI app
app = FastAPI(
    title="JKYog WhatsApp Bot",
    description="AI-powered WhatsApp bot for JKYog Radha Krishna Temple",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """
    Root endpoint - provides basic information about the bot.
    """
    return {
        "name": "JKYog WhatsApp Bot",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Render.
    
    Render uses this to verify the service is running.
    """
    return {
        "status": "healthy",
        "service": "jkyog-whatsapp-bot"
    }


@app.post("/webhook")
async def twilio_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Twilio WhatsApp webhook endpoint.
    
    Receives incoming WhatsApp messages from Twilio and processes them
    through the bot pipeline.
    """
    try:
        twiml_response = await handle_twilio_webhook(request, db)
        return Response(
            content=twiml_response,
            media_type="application/xml"
        )
    except Exception as e:
        print(f"Error processing webhook: {e}")
        # Return a generic error message in TwiML format
        error_twiml = '<?xml version="1.0" encoding="UTF-8"?><Response><Message>Sorry, I\'m experiencing technical difficulties. Please try again later.</Message></Response>'
        return Response(
            content=error_twiml,
            media_type="application/xml",
            status_code=500
        )


@app.get("/test")
async def test_endpoint():
    """
    Test endpoint for verifying the bot pipeline works.
    
    This endpoint can be used to test the bot without Twilio.
    """
    from bot.response_builder import build_response
    
    test_message = "Hello, where is the temple?"
    response = build_response(test_message)
    
    return {
        "test_message": test_message,
        "bot_response": response
    }


if __name__ == "__main__":
    import uvicorn
    
    # For local development
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
