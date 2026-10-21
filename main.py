from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
from typing import List, Optional

app = FastAPI(title="WE SELL TIME")
templates = Jinja2Templates(directory=".")

# Data Model
class SessionState(BaseModel):
    seen_ids: List[int] = []

# Mock Library with sample elements representing the 4 categories
CARDS_DATABASE = [
    # 01. Riddles & Discoveries
    {
        "id": 1,
        "category": "Riddles & Discoveries",
        "prompt": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "options": ["A shadow", "An echo", "A cloud", "A reflection"],
        "correct_answer": "An echo",
        "explanation": "An echo is sound reflecting off surfaces, created by soundwaves moving through air.",
        "takeaway": "Perspective reveals that some presence exists only through reaction."
    },
    {
        "id": 2,
        "category": "Riddles & Discoveries",
        "prompt": "The more of this you take, the more you leave behind. What are they?",
        "options": ["Footsteps", "Memories", "Seconds", "Breath"],
        "correct_answer": "Footsteps",
        "explanation": "Every step you make creates a mark behind you as you move forward.",
        "takeaway": "Progress inherently leaves a trail of past actions."
    },
    # 02. Real-Life Situations
    {
        "id": 3,
        "category": "Real-Life Situations",
        "prompt": "A colleague repeatedly interrupts you during team presentations. What is the most effective immediate response?",
        "options": [
            "Interrupt them back loudly",
            "Pause calmly, say 'Let me finish this point', then continue",
            "Remain silent and file a complaint later",
            "Stop presenting completely"
        ],
        "correct_answer": "Pause calmly, say 'Let me finish this point', then continue",
        "explanation": "Setting direct, calm boundaries preserves your authority without escalating tension.",
        "takeaway": "Calm composure maintains control in professional boundaries."
    },
    # 03. Everyday Math & Problem Solving
    {
        "id": 4,
        "category": "Everyday Math & Problem Solving",
        "prompt": "You have $20. You spend $7.50 on lunch and $3.25 on a drink. How much money remains?",
        "options": ["$8.25", "$9.25", "$10.75", "$11.25"],
        "correct_answer": "$9.25",
        "explanation": "$7.50 + $3.25 = $10.75 total spent. $20.00 − $10.75 = $9.25 remaining.",
        "takeaway": "Calculate total expenditure first before subtracting from your total budget."
    },
    # 04. Human Needs & Positive Perspectives
    {
        "id": 5,
        "category": "Human Needs & Positive Perspectives",
        "prompt": "When feeling overwhelmed by a long list of obligations, which psychological strategy best restores focus?",
        "options": [
            "Multitask all items at once",
            "Complete one tiny 2-minute task immediately",
            "Wait until energy returns naturally",
            "Re-organize the list repeatedly"
        ],
        "correct_answer": "Complete one tiny 2-minute task immediately",
        "explanation": "Completing a minor task triggers a sense of agency and reduces friction.",
        "takeaway": "Action precedes motivation; small wins reduce cognitive overload."
    }
]

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/next-card")
async def get_next_card(state: SessionState):
    # Filter unseen items
    available = [card for card in CARDS_DATABASE if card["id"] not in state.seen_ids]
    
    if not available:
        # Fallback if all items have been seen in this session
        available = CARDS_DATABASE

    # Pick a random card from available ones
    selected_card = random.choice(available)
    return selected_card

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
