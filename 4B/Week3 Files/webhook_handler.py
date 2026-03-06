"""
Webhook Handler for Twilio WhatsApp Integration
Processes incoming WhatsApp messages and returns TwiML responses
"""

from fastapi import Request
from sqlalchemy.orm import Session
from typing import Dict, Optional

from bot.response_builder import build_response
from authentication.phone_verification import authenticate_phone_user
from database.state_tracking import log_message


async def parse_twilio_payload(request: Request) -> Dict:
    """
    Parse incoming Twilio webhook payload.
    
    Args:
        request: FastAPI Request object
    
    Returns:
        Dictionary with parsed data:
        - from_number: User's phone number
        - message_body: Message text
        - profile_name: User's WhatsApp profile name (if available)
        - message_sid: Twilio message ID
    """
    try:
        # Twilio sends form data, not JSON
        form_data = await request.form()
        
        return {
            "from_number": form_data.get("From", "").replace("whatsapp:", ""),
            "to_number": form_data.get("To", "").replace("whatsapp:", ""),
            "message_body": form_data.get("Body", ""),
            "profile_name": form_data.get("ProfileName", ""),
            "message_sid": form_data.get("MessageSid", ""),
            "num_media": int(form_data.get("NumMedia", 0)),
        }
    except Exception as e:
        print(f"Error parsing Twilio payload: {e}")
        return {
            "from_number": "",
            "to_number": "",
            "message_body": "",
            "profile_name": "",
            "message_sid": "",
            "num_media": 0,
        }


def create_twiml_response(message: str) -> str:
    """
    Create TwiML response for Twilio.
    
    Args:
        message: Response message to send
    
    Returns:
        TwiML XML string
    """
    # Escape XML special characters
    message = (
        message
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>'''
    
    return twiml


async def handle_twilio_webhook(request: Request, db: Session) -> str:
    """
    Main webhook handler for Twilio WhatsApp messages.
    
    Pipeline:
    1. Parse Twilio webhook payload
    2. Authenticate user via phone number
    3. Get/create conversation context
    4. Process message through bot pipeline
    5. Log message to database
    6. Return TwiML response
    
    Args:
        request: FastAPI Request object
        db: Database session
    
    Returns:
        TwiML XML string for Twilio
    """
    try:
        # Step 1: Parse webhook payload
        payload = await parse_twilio_payload(request)
        
        from_number = payload["from_number"]
        message_body = payload["message_body"]
        profile_name = payload["profile_name"]
        
        print(f"📱 Received message from {from_number}: {message_body}")
        
        # Handle empty messages or media-only messages
        if not message_body or not message_body.strip():
            if payload["num_media"] > 0:
                response_text = "I received your media! However, I can only process text messages at this time. Please send me a text message, and I'll be happy to help! 😊"
            else:
                response_text = "I didn't receive any message. Please try again! 🙏"
            return create_twiml_response(response_text)
        
        # Step 2: Authenticate user and get/create conversation
        user_context = None
        try:
            user, conversation = authenticate_phone_user(
                db=db,
                phone_number=from_number,
                name=profile_name
            )
            
            user_context = {
                "user_id": str(user.id),
                "conversation_id": str(conversation.id),
                "phone_number": from_number,
                "name": profile_name or "Unknown"
            }
            
            print(f"✅ Authenticated user: {user.id}")
        except Exception as e:
            print(f"⚠️ Authentication failed: {e}")
            print("   Continuing without user context...")
        
        # Step 3: Log incoming message (if database available)
        if user_context:
            try:
                log_message(
                    db=db,
                    conversation_id=user_context["conversation_id"],
                    direction="inbound",
                    text=message_body,
                    intent=None  # Will be determined by bot
                )
            except Exception as e:
                print(f"⚠️ Failed to log incoming message: {e}")
        
        # Step 4: Process through bot pipeline
        try:
            bot_response = build_response(message_body, user_context)
            print(f"🤖 Bot response: {bot_response[:100]}...")
        except Exception as e:
            print(f"❌ Bot pipeline error: {e}")
            bot_response = "I'm having trouble processing your request. Please try again or contact the temple at (469) 606-3119."
        
        # Step 5: Log outgoing message (if database available)
        if user_context:
            try:
                log_message(
                    db=db,
                    conversation_id=user_context["conversation_id"],
                    direction="outbound",
                    text=bot_response,
                    intent=None
                )
            except Exception as e:
                print(f"⚠️ Failed to log outgoing message: {e}")
        
        # Step 6: Return TwiML response
        return create_twiml_response(bot_response)
    
    except Exception as e:
        print(f"❌ Webhook handler error: {e}")
        error_message = "I'm experiencing technical difficulties. Please try again later or contact the temple at (469) 606-3119."
        return create_twiml_response(error_message)


def verify_twilio_signature(request: Request, auth_token: str) -> bool:
    """
    Verify that the request is actually from Twilio.
    
    This is an optional security measure. Currently not implemented
    to simplify initial deployment.
    
    Args:
        request: FastAPI Request object
        auth_token: Twilio auth token
    
    Returns:
        True if signature is valid, False otherwise
    """
    # TODO: Implement Twilio signature verification
    # from twilio.request_validator import RequestValidator
    # validator = RequestValidator(auth_token)
    # return validator.validate(url, post_data, signature)
    return True


if __name__ == "__main__":
    # Test the webhook handler with mock data
    print("Webhook handler module loaded successfully!")
    print("This module should be imported by app.py")
