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
    {"en": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"en": "To err is human, but to really foul things up you need a computer.", "author": "Paul R. Ehrlich"}
]

# 🐕 Unblockable vector graphics of different dog designs written directly inside the code
DOG_ILLUSTRATIONS = [
    # Dog 1: Golden/Orange Retriever Look
    """<svg viewBox="0 0 200 200" style="width:100%; max-height:280px; background:#f4f7f6; border-radius:8px;">
      <circle cx="100" cy="100" r="80" fill="#f39c12" opacity="0.1"/>
      <path d="M65,80 Q50,40 40,85 Q30,110 50,110 Z" fill="#d35400"/>
      <path d="M135,80 Q150,40 160,85 Q170,110 150,110 Z" fill="#d35400"/>
      <path d="M50,90 Q100,60 150,90 Q160,140 100,160 Q40,140 50,90 Z" fill="#e67e22"/>
      <circle cx="85" cy="105" r="7" fill="#2c3e50"/><circle cx="115" cy="105" r="7" fill="#2c3e50"/>
      <polygon points="90,122 110,122 100,135" fill="#2c3e50"/>
    </svg>""",
    # Dog 2: French Bulldog Style Look
    """<svg viewBox="0 0 200 200" style="width:100%; max-height:280px; background:#edf2f7; border-radius:8px;">
      <circle cx="100" cy="100" r="80" fill="#718096" opacity="0.1"/>
      <path d="M55,50 Q40,30 50,70 Z" fill="#4a5568"/>
      <path d="M145,50 Q160,30 150,70 Z" fill="#4a5568"/>
      <circle cx="100" cy="115" r="55" fill="#a0aec0"/>
      <ellipse cx="100" cy="125" rx="25" ry="18" fill="#2d3748"/>
      <circle cx="80" cy="100" r="8" fill="#1a202c"/><circle cx="120" cy="100" r="8" fill="#1a202c"/>
      <circle cx="100" cy="120" r="6" fill="#1a202c"/>
    </svg>""",
    # Dog 3: Cute White Terrier Style Look
    """<svg viewBox="0 0 200 200" style="width:100%; max-height:280px; background:#fffaf0; border-radius:8px;">
      <circle cx="100" cy="100" r="80" fill="#ed8936" opacity="0.1"/>
      <path d="M60,60 L40,90 L75,85 Z" fill="#cbd5e0"/>
      <path d="M140,60 L160,90 L125,85 Z" fill="#cbd5e0"/>
      <circle cx="100" cy="110" r="50" fill="#f7fafc"/>
      <circle cx="85" cy="105" r="6" fill="#2d3748"/><circle cx="115" cy="105" r="6" fill="#2d3748"/>
      <ellipse cx="100" cy="118" rx="10" ry="7" fill="#4a5568"/>
    </svg>"""
]

class DogGeneratorResponse(BaseModel):
    image_element: str
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
        <a href="/view" style="padding:10px 20px; background:#3498db; color:white; text-decoration:none; border-radius:5px; margin:5px; display:inline-block; font-weight:bold;">Open Card Viewer</a>
        <a href="/docs" style="padding:10px 20px; background:#95a5a6; color:white; text-decoration:none; border-radius:5px; margin:5px; display:inline-block; font-weight:bold;">View API Specs</a>
    </body>
    </html>
    """, status_code=200)

# === 📤 ENDPOINT 2 (GET): Core Data Engine ===
@app.get("/generate", response_model=DogGeneratorResponse, tags=["Core Services"])
async def generate_dog_card():
    # Randomly select a built-in unblockable graphic illustration
    active_visual = random.choice(DOG_ILLUSTRATIONS)
    selected_quote = random.choice(BACKUP_DEV_QUOTES)
    theme_source = "Coding Wisdom (Local Asset)"

    async with httpx.AsyncClient() as client:
        try:
            quote_req = await client.get("https://vercel.app", timeout=3.0)
            if quote_req.status_code == 200:
                selected_quote = quote_req.json()
                theme_source = "Programming & Tech Logic"
        except Exception: 
            pass

    return {
        "image_element": active_visual,
        "en": selected_quote.get("en", "Code works, but no statement returned."),
        "author": selected_quote.get("author", "Anonymous Coder"),
        "theme": theme_source
    }

# === 📤 ENDPOINT 3 (GET): Visual Card Viewer ===
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
            
            <!-- 🖼️ Dynamic vector graphic block injections -->
            <div style="width:100%; overflow:hidden; border-bottom:4px solid #3498db; margin-bottom:15px;">
                {data['image_element']}
            </div>

            <p style="font-style:italic; font-size:1.15em; color:#2c3e50; margin-top:20px; line-height:1.4; min-height:60px;">"{data['en']}"</p>
            <h4 style="color:#7f8c8d; margin-bottom:15px; font-weight:normal;">— {data['author']}</h4>
            <span style="display:inline-block; background:#e8f4fd; color:#3498db; font-size:0.8em; padding:6px 12px; border-radius:20px; font-weight:bold; margin-bottom:20px;">🏷️ {data['theme']}</span>
            <br>
            <a href="/view" style="padding:12px 24px; background:#3498db; color:white; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block;">Next Dog 🔄</a>
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
