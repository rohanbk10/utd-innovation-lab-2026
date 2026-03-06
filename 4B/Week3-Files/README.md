# JKYog WhatsApp Bot

AI-powered WhatsApp bot for JKYog Radha Krishna Temple, built with FastAPI, OpenAI, and Twilio.

## Features

- **Intent Classification**: Uses OpenAI's text-embedding-3-small for semantic understanding
- **Entity Extraction**: Extracts dates, times, locations, and event types from natural language
- **Knowledge Base Integration**: Searches temple FAQs and events
- **External Integrations**:
  - Google Maps for directions
  - Stripe for donations
  - Google Calendar for events
- **Database Logging**: Tracks conversations and messages in Supabase PostgreSQL
- **Twilio WhatsApp**: Handles incoming/outgoing WhatsApp messages

## Team Structure

This project combines work from multiple team members:

- **Rohan Kothapalli**: Bot logic core (intent classifier, entity extractor, response builder)
- **Leena Hussein**: Knowledge base (FAQs, events, search functionality)
- **Chakradhar**: Database schema and state tracking
- **Sysha**: Authentication and session management
- **Subodh Krishna Nikumbh**: External API integrations (Maps, Calendar, Stripe)

## Project Structure

```
Week3 Files/
├── bot/                        # Rohan's bot logic
│   ├── intent_classifier.py
│   ├── entity_extractor.py
│   └── response_builder.py
├── knowledge_base/             # Leena's knowledge base
│   ├── faqs.json
│   ├── events.json
│   └── ingestion.py
├── database/                   # Chakradhar's database
│   ├── models.py
│   ├── schema.py
│   └── state_tracking.py
├── authentication/             # Sysha's auth
│   ├── auth.py
│   ├── phone_verification.py
│   └── session_manager.py
├── integrations/               # Subodh's integrations
│   ├── google_maps.py
│   ├── stripe.py
│   └── calendar.py
├── app.py                      # FastAPI application
├── webhook_handler.py          # Twilio webhook processing
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md
```

## Local Development Setup

### Prerequisites

- Python 3.11+
- Supabase account (for database)
- OpenAI API key
- Twilio account (for WhatsApp)
- Google Cloud account (for Maps & Calendar APIs)
- Stripe account (for payment links)

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd "Week3 Files"
```

2. **Create virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys and credentials (see Configuration section below).

5. **Run the application**

```bash
# Development mode with auto-reload
uvicorn app:app --reload --port 8000

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

The app will be available at `http://localhost:8000`

## Configuration

### 1. Supabase Database Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Project Settings** > **Database**
3. Copy the **Connection string** (URI format)
4. Run the database migrations (create tables):

```python
# The app will automatically create tables on startup
# Or manually run:
python -c "from database.models import init_db; init_db()"
```

5. Add `DATABASE_URL` to `.env`:

```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 2. OpenAI API Setup

1. Get API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add to `.env`:

```
OPENAI_API_KEY=sk-...
```

### 3. Twilio WhatsApp Sandbox Setup

1. Create account at [twilio.com](https://www.twilio.com)
2. Go to **Messaging** > **Try it out** > **Send a WhatsApp message**
3. Follow instructions to join sandbox (send "join [code]" to sandbox number)
4. Configure webhook:
   - Webhook URL: `https://your-render-url.onrender.com/webhook`
   - Method: `POST`
5. Add credentials to `.env`:

```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+14155238886
```

### 4. Google Maps API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Maps Directions API**
3. Create credentials (API Key)
4. Add to `.env`:

```
GOOGLE_MAPS_API_KEY=AIza...
```

### 5. Google Calendar API Setup

1. Enable **Google Calendar API** in Cloud Console
2. Create **Service Account**
3. Download JSON key file
4. Add to `.env` (either JSON string or file path):

```
GOOGLE_CALENDAR_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
GOOGLE_CALENDAR_ID=primary
```

### 6. Stripe Payment Links Setup

1. Create payment links at [dashboard.stripe.com/payment-links](https://dashboard.stripe.com/payment-links)
2. Add to `.env`:

```
STRIPE_DEFAULT_LINK=https://buy.stripe.com/...
STRIPE_DALLAS_LINK=https://buy.stripe.com/...
```

## Deployment to Render

### Quick Deploy

1. **Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Connect to Render**

- Go to [render.com](https://render.com)
- Click **New** > **Blueprint**
- Connect your GitHub repository
- Render will automatically detect `render.yaml`
- Click **Apply**

3. **Configure Environment Variables**

In Render dashboard, go to your service and add all environment variables from `.env.example`:

- `OPENAI_API_KEY`
- `DATABASE_URL`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `GOOGLE_MAPS_API_KEY`
- `GOOGLE_CALENDAR_SERVICE_ACCOUNT_JSON`
- `GOOGLE_CALENDAR_ID`
- `STRIPE_DEFAULT_LINK`
- `STRIPE_DALLAS_LINK`

4. **Update Twilio Webhook**

Once deployed, copy your Render URL (e.g., `https://jkyog-whatsapp-bot.onrender.com`) and update the Twilio webhook:

- Webhook URL: `https://your-app.onrender.com/webhook`
- Method: `POST`

5. **Test the Bot**

Send a WhatsApp message to your Twilio sandbox number!

## Testing

### Test Endpoints

1. **Health Check**

```bash
curl https://your-app.onrender.com/health
```

2. **Test Bot Pipeline** (without Twilio)

```bash
curl https://your-app.onrender.com/test
```

### Test Messages

Try these messages with your WhatsApp bot:

1. **Greeting**: "Hello"
2. **FAQ**: "Where is the temple?"
3. **Event**: "When is Friday satsang?"
4. **Donation**: "How do I donate?"
5. **Directions**: "Directions from Dallas"

### Local Testing with Twilio

Use [ngrok](https://ngrok.com/) to test Twilio webhooks locally:

```bash
# Install ngrok
# Download from ngrok.com

# Start your local server
uvicorn app:app --reload --port 8000

# In another terminal, start ngrok
ngrok http 8000

# Copy the ngrok URL (e.g., https://abc123.ngrok.io)
# Update Twilio webhook to: https://abc123.ngrok.io/webhook
```

## Monitoring & Logs

### Render Logs

View logs in Render dashboard:
- Go to your service
- Click **Logs** tab
- See real-time application logs

### Database Logs

Check conversation history in Supabase:
- Go to **Table Editor**
- View `users`, `conversations`, `messages` tables

## Troubleshooting

### Bot not responding

1. Check Render logs for errors
2. Verify all environment variables are set
3. Test `/health` endpoint
4. Check Twilio webhook configuration

### Database connection errors

1. Verify `DATABASE_URL` is correct
2. Check Supabase project is active
3. Ensure IP is not blocked (Supabase allows all IPs by default)

### OpenAI API errors

1. Verify API key is valid
2. Check API usage/billing at platform.openai.com
3. Bot will fall back to keyword matching if API fails

### Twilio webhook failures

1. Check webhook URL is correct
2. Verify it's POST method
3. Test with `/test` endpoint first
4. Check Twilio debugger for request details

## API Reference

### Endpoints

#### `GET /`
Root endpoint with API information

#### `GET /health`
Health check for Render

**Response:**
```json
{
  "status": "healthy",
  "service": "jkyog-whatsapp-bot"
}
```

#### `POST /webhook`
Twilio WhatsApp webhook endpoint

**Request:** Twilio webhook form data

**Response:** TwiML XML

#### `GET /test`
Test bot pipeline without Twilio

**Response:**
```json
{
  "test_message": "Hello, where is the temple?",
  "bot_response": "..."
}
```

## Bot Architecture

```
WhatsApp User
    ↓
Twilio API
    ↓
Render (FastAPI)
    ↓
webhook_handler.py
    ↓
┌─────────────────────────────┐
│  Bot Pipeline               │
│  1. classify_intent()       │
│  2. extract_entities()      │
│  3. build_response()        │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Integrations               │
│  • Knowledge Base (FAQs)    │
│  • Google Maps              │
│  • Google Calendar          │
│  • Stripe Payments          │
│  • Supabase Database        │
└─────────────────────────────┘
    ↓
Twilio API
    ↓
WhatsApp User
```

## Contributing

This project was built as a team assignment. Each module is owned by a specific team member:

- To modify bot logic: Contact Rohan
- To update FAQs/events: Contact Leena
- To change database schema: Contact Chakradhar
- To modify auth: Contact Sysha
- To update integrations: Contact Subodh

## License

This project is for educational purposes as part of the JKYog WhatsApp Bot assignment.

## Support

For issues or questions:
- Check Render logs
- Review Twilio debugger
- Contact temple: (469) 606-3119
- Visit: jkyog.org

---

**Built with ❤️ by the JKYog Bot Team**
