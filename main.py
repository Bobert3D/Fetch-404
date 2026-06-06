import random
import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(docs_url=None, redoc_url=None)

USER_SUBMITTED_QUOTES = []
USER_FEEDBACK = []

BACKUP_DEV_QUOTES = [
    {"en": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler"},
    {"en": "First, solve the problem. Then, write the code.", "author": "John Johnson"}
]

# Validation Schemas
class DogGeneratorResponse(BaseModel):
    image_url: str
    en: str
    author: str
    theme: str

class CustomQuoteInput(BaseModel):
    quote_text: str
    author_name: str

class FeedbackInput(BaseModel):
    username: str
    stars: int = Field(..., ge=1, le=5)
    comment: str

# === 📤 ENDPOINT 1 (GET): Homepage Layout ===
@app.get("/", response_class=HTMLResponse, tags=["Interface"])
def home_page():
    return HTMLResponse(content="""
    <html>
    <head><title>Geeky Dog Engine</title></head>
    <body style="font-family:sans-serif; text-align:center; padding:50px; background:#f4f6f9;">
        <h1>🐕 Geeky Dog App Hub</h1>
        <p>Your multi-endpoint interactive engine is up and running!</p>
        <a href="/view" style="padding:10px 20px; background:#3498db; color:white; text-decoration:none; border-radius:5px; margin:5px; display:inline-block;">Open Card Viewer</a>
        <a href="/docs" style="padding:10px 20px; background:#95a5a6; color:white; text-decoration:none; border-radius:5px; margin:5px; display:inline-block;">View API Specs</a>
    </body>
    </html>
    """, status_code=200)

# === 📤 ENDPOINT 2 (GET): Core Data Engine ===
@app.get("/generate", response_model=DogGeneratorResponse, tags=["Core Services"])
async def generate_dog_card():
    # 🚀 FIX: Reliable fallback image URL that will never return a broken link
    dog_image = "https://unsplash.com"
    selected_quote = random.choice(BACKUP_DEV_QUOTES)
    theme_source = "Coding Wisdom (Backup Local DB)"

    async with httpx.AsyncClient() as client:
        # Step A: Fetch random dog image URL from Dog CEO API
        try:
            dog_req = await client.get("https://dog.ceo", timeout=5.0)
            if dog_req.status_code == 200:
                dog_image = dog_req.json().get("message", dog_image)
        except Exception as e: 
            print(f"--- IMAGE API ERROR: {e} ---") # Logs connection errors to your console

        # Step B: Fetch random coding statement from Programming Quotes API
        try:
            quote_req = await client.get("https://vercel.app", timeout=5.0)
            if quote_req.status_code == 200:
                selected_quote = quote_req.json()
                theme_source = "Programming & Tech Logic"
        except Exception as e: 
            print(f"--- QUOTE API ERROR: {e} ---") # Logs connection errors to your console

    return {
        "image_url": dog_image,
        "en": selected_quote.get("en", "Code works, but no statement returned."),
        "author": selected_quote.get("author", "Anonymous"),
        "theme": theme_source
    }

# === 📤 ENDPOINT 3 (GET): Visual Renderer Layout ===
@app.get("/view", response_class=HTMLResponse, tags=["Interface"])
async def view_dog_card_visual():
    data = await generate_dog_card()
    
    return HTMLResponse(content=f"""
    <html>
    <head>
        <title>Dog Card Viewer</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family:sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0; background:#efefef;">
        <div style="background:white; padding:30px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1); text-align:center; max-width:400px; width:90%; margin:20px;">
            <img src="{data['image_url']}" style="width:100%; max-height:300px; object-fit:cover; border-radius:8px; border-bottom:4px solid #3498db;">
            <p style="font-style:italic; font-size:1.1em; color:#2c3e50; margin-top:25px; line-height:1.4;">"{data['en']}"</p>
            <h4 style="color:#7f8c8d; margin-bottom:5px; font-weight:normal;">— {data['author']}</h4>
            <span style="display:inline-block; background:#e8f4fd; color:#3498db; font-size:0.8em; padding:6px 12px; border-radius:20px; font-weight:bold; margin-bottom:20px;">🏷️ {data['theme']}</span>
            <br>
            <a href="/view" style="padding:12px 24px; background:#3498db; color:white; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block; transition: background 0.2s;">Next Dog 🔄</a>
        </div>
    </body>
    </html>
    """, status_code=200)

# === 📤 ENDPOINT 4 (GET): Read User Quotes Database ===
@app.get("/custom-quotes", response_model=List[dict], tags=["User Data Management"])
def view_all_user_quotes():
    return USER_SUBMITTED_QUOTES

# === 📥 ENDPOINT 5 (POST): Create New Quote Item ===
@app.post("/custom-quotes", tags=["User Data Management"])
def add_custom_quote(user_input: CustomQuoteInput):
    USER_SUBMITTED_QUOTES.append({"en": user_input.quote_text, "author": user_input.author_name})
    return {"status": "Success", "message": "Custom item logged successfully!"}

# === 📥 ENDPOINT 6 (POST): Submit Application Feedback ===
@app.post("/feedback", tags=["Feedback System"])
def submit_app_feedback(review: FeedbackInput):
    USER_FEEDBACK.append(review.dict())
    return {"status": "Thank you!", "message": "Feedback submitted successfully."}

# === 📤 ENDPOINT 7 (GET): View Feedback Repository ===
@app.get("/feedback", response_model=List[dict], tags=["Feedback System"])
def view_all_feedback():
    return USER_FEEDBACK

# === 🛠️ SYSTEM ENDPOINT: Documentation Portal ===
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
def hand_written_documentation():
    return HTMLResponse(content="""
    <html>
    <body style="font-family:sans-serif; max-width:700px; margin:40px auto; padding:20px; line-height:1.6; background:#fafafa;">
        <h1>📜 Engine Blueprint & Documentation Portal</h1>
        <p>Official endpoints catalog for automated challenge review workflows.</p>
        <hr>
        <h3>📤 GET Endpoints</h3>
        <ul>
            <li><code>GET /</code> - Serves landing page</li>
            <li><code>GET /view</code> - Renders card visually</li>
            <li><code>GET /generate</code> - Emits core JSON data structures</li>
            <li><code>GET /custom-quotes</code> - Dumps recorded quotes array</li>
            <li><code>GET /feedback</code> - Dumps user review data models</li>
        </ul>
        <h3>📥 POST Endpoints</h3>
        <ul>
            <li><code>POST /custom-quotes</code> - Saves custom quote strings</li>
            <li><code>POST /feedback</code> - Saves a numeric rating and text message</li>
        </ul>
    </body>
    </html>
    """, status_code=200)
