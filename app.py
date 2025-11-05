from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import openai, os

app = FastAPI()

@app.post("/voice")
async def voice(request: Request):
    """Handle a voice call from Twilio"""
    data = await request.form()
    user_text = data.get("SpeechResult", "")
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""You are Mark, a friendly AI receptionist for Throttle Pulse MX Limited.
Caller says: "{user_text}"
Respond naturally, conversationally, and keep replies short.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content.strip()

    # Return TwiML for Twilio to speak
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="Polly.Matthew">{reply}</Say>
</Response>"""
    return PlainTextResponse(twiml, media_type="application/xml")

@app.get("/")
async def root():
    return {"status": "AI Receptionist ready!"}
