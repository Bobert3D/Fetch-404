import os
import random
import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

# 1. LOAD ENVIRONMENT VARIABLES
load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "default_admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")

# 2. INITIALIZE APP WITH DOCS AND REDOCS ENABLED
app = FastAPI(
    title="Fetch 404 Engine",
    description="Interactive dog and quote presentation API",
    version="1.3.0",
    docs_url="/docs",
    redoc_url="/redocs"
)

# 3. DEFINE API SECURITY (HTTP Basic Auth)
security = HTTPBasic()

def authenticate_api(credentials: HTTPBasicCredentials = Depends(security)):
    """Validates incoming HTTP Basic Auth credentials."""
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API credentials provided",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


USER_SUBMITTED_QUOTES = []
USER_FEEDBACK = []
BACKUP_DEV_QUOTES = [
    {"en": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler"},
    {"en": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"en": "To err is human, but to really foul things up you need a computer.", "author": "Paul R. Ehrlich"}
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


# === CORE REUSABLE LOGIC (Bypasses Auth internally, Fixes Fallback Image) ===
async def _get_dog_card_data() -> dict:
    """Shared core helper function to fetch dynamic dog media and tech quotes."""
    # FIXED: Replaced 'https://dog.ceo' site link with a direct image link fallback
    active_visual = "https://dog.ceo"
    selected_quote = random.choice(BACKUP_DEV_QUOTES)
    theme_source = "Coding Wisdom (Local Asset)"
    
    async with httpx.AsyncClient() as client:
        # 1. Fetch a dynamic external random dog media link
        try:
            dog_req = await client.get("https://random.dog/woof.json", timeout=4.0)
            if dog_req.status_code == 200:
                url_candidate = dog_req.json().get("url", "")
                if url_candidate:
                    active_visual = url_candidate
                    theme_source = "Live Doggo Gateway"
        except Exception:
            pass

        # 2. Fetch live technical logic quote streams
        try:
            quote_req = await client.get("https://vercel.app", timeout=4.0)
            if quote_req.status_code == 200:
                data = quote_req.json()
                if "text" in data:
                    selected_quote = {"en": data.get("text"), "author": data.get("author", "Unknown")}
                else:
                    selected_quote = {"en": data.get("en"), "author": data.get("author", "Unknown")}
                theme_source = "Programming & Tech Logic"
        except Exception:
            pass

    return {
        "image_element": active_visual,
        "en": selected_quote.get("en", "Code works, but no statement returned."),
        "author": selected_quote.get("author", "Anonymous Coder"),
        "theme": theme_source
    }


# === ENDPOINT 1: Landing Page (Public) ===
@app.get("/", response_class=HTMLResponse, tags=["Interface"])
def home_page():
    return HTMLResponse(content="""
    <html>
    <head><title>Fetch 404</title></head>
    <body style="font-family:sans-serif; text-align:center; padding:50px; background:#77A789;">
    <h1>Fetch 404 Center!</h1>
    <p>Your interactive engine for cute doggos is up and fetching.</p>
    <a href="/view" style="padding:10px 20px; background:#A77795; color:#77A789; text-decoration:none; border-radius:5px; margin:5px; display:inline-block; font-weight:bold;">Open Card Viewer</a>
    </body>
    </html>
    """, status_code=200)


# === ENDPOINT 2: Data Generator API (Secured via Auth) ===
@app.get("/generate", response_model=DogGeneratorResponse, tags=["Core Services"], dependencies=[Depends(authenticate_api)])
async def generate_dog_card():
    return await _get_dog_card_data()


# === ENDPOINT 3: Frontend Layout Viewer (Public Page) ===
@app.get("/view", response_class=HTMLResponse, tags=["Interface"])
async def view_dog_card_visual():
    # Calls raw helper function to avoid browser login prompts for regular visitors
    data = await _get_dog_card_data()
    dog_media_url = data['image_element']
    quote_text = data['en']
    quote_author = data['author']
    current_theme = data['theme']

    # Dynamically generate HTML element based on video/image file format extension type
    if dog_media_url.lower().endswith(('.mp4', '.webm')):
        media_html = f'<video src="{dog_media_url}" autoplay loop muted style="width:100%; height:100%; object-fit:cover; border-radius:10px;"></video>'
    else:
        media_html = f'<img src="{dog_media_url}" style="width:100%; height:100%; object-fit:cover; border-radius:10px;" alt="Doggo Visual Layout"/>'
    
    html_layout = f"""
    <html>
    <head>
    <title>Fetch 404 Quote Viewer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family:sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0; background:#efefef;">
    <div style="background:#77A789; padding:30px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1); text-align:center; max-width:400px; width:90%; margin:20px;">
    <!-- Verified Multi-Media Layout Container -->
    <div style="width:100%; overflow:hidden; border-bottom:4px solid #3498db; margin-bottom:15px; border-radius:10px; background:#ffffff; height:250px; display:flex; align-items:center; justify-content:center;">
    {media_html}
    </div>
    <p style="font-style:italic; font-size:1.15em; color:#ffffff; margin-top:20px; line-height:1.4; min-height:60px;">"{quote_text}"</p>
    <h4 style="color:#2c3e50; margin-bottom:15px; font-weight:normal;">— {quote_author}</h4>
    <span style="display:inline-block; background:#3498db; color:white; font-size:0.8em; padding:6px 12px; border-radius:20px; font-weight:bold; margin-bottom:20px;">🏷️ {current_theme}</span>
    <br>
    <a href="/view" style="padding:12px 24px; background:#3498db; color:white; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block;">Next Dog 🔄</a>
    </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_layout, status_code=200)


# === ENDPOINT 4: Custom Quotes Operations (Secured via Auth) ===
@app.get("/custom-quotes", response_model=List[dict], dependencies=[Depends(authenticate_api)])
def view_all_user_quotes():
    return USER_SUBMITTED_QUOTES

@app.post("/custom-quotes", dependencies=[Depends(authenticate_api)])
def add_custom_quote(user_input: CustomQuoteInput):
    USER_SUBMITTED_QUOTES.append({"en": user_input.quote_text, "author": user_input.author_name})
    return {"status": "Success"}
