from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8067709324:AAEXgbjhiaeExYr9gbxrclYRgqW69rSnhrk")
CHAT_ID = os.getenv("CHAT_ID", "16268161")


class VisitForm(BaseModel):
    first_name: str
    last_name: str
    phone: str
    master: str
    amount: str
    service: str
    visit_type: str
    source: str
    rating: str
    satisfied: str
    comment: Optional[str] = ""
    lang: Optional[str] = "RU"


@app.get("/")
def serve_form():
    return FileResponse("index.html")


@app.post("/submit")
async def submit_form(form: VisitForm):
    stars = "⭐" * int(form.rating)
    comment_line = f"\n💬 Комментарий: {form.comment}" if form.comment else ""

    text = (
        f"📋 *Новый визит* [{form.lang}]\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 {form.first_name} {form.last_name}\n"
        f"📞 {form.phone}\n"
        f"✂️ Мастер: {form.master}\n"
        f"💰 Оплата: {form.amount} сум\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💅 Услуга: {form.service}\n"
        f"🔄 Визит: {form.visit_type}\n"
        f"📣 Источник: {form.source}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{stars} Оценка: {form.rating}/5\n"
        f"😊 Доволен(а): {form.satisfied}"
        f"{comment_line}"
    )

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
        )

    return {"status": "ok"}
