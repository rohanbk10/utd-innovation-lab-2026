from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import get_db
from .phone_verification import authenticate_phone_user
from .session_manager import generate_session, validate_session


async def verify_whatsapp_request(request: Request, db: Session = Depends(get_db)):
    """
    FastAPI dependency to authenticate incoming webhook requests.
    Combines phone verification and session management.
    """

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Extract phone number and profile name from the WhatsApp payload
    try:
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        # Ignore non-message events (like read receipts)
        if not messages:
            return {"status": "ignored"}

        message = messages[0]
        phone_number = message.get("from")

        # Extract the user's WhatsApp profile name if available
        contacts = value.get("contacts", [])
        profile_name = contacts[0].get("profile", {}).get("name", "") if contacts else ""

        if not phone_number:
            raise HTTPException(status_code=400, detail="Missing phone number")

        # Authenticate user and create/get session
        user, conversation = authenticate_phone_user(
            db=db,
            phone_number=phone_number,
            name=profile_name
        )

        # Generate session token for the user
        session = generate_session(db=db, user_id=user.id)

        return {
            "user": user,
            "conversation": conversation,
            "session": session,
            "message": message.get("text", {}).get("body", ""),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
