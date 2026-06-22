from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
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


@app.get("/")
def serve_form():
    return FileResponse("index.html")


@app.post("/submit")
async def submit_form(form: VisitForm):
    text = (
        f"📋 *Новый визит*\n"
        f"👤 {form.first_name} {form.last_name}\n"
        f"📞 {form.phone}\n"
        f"✂️ Мастер: {form.master}\n"
        f"💰 Оплата: {form.amount} сум"
    )

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
        )

    return {"status": "ok"}
