from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import hmac
import hashlib
from urllib.parse import parse_qsl

from fastapi import FastAPI, Request, HTTPException


import asyncio, os

from aiogram import Router, Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from dotenv import load_dotenv

load_dotenv()
# Load the bot token from the .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN_SECRET = hashlib.sha256(BOT_TOKEN.encode()).digest()
# Initialize FastAPI app


def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Click", web_app=WebAppInfo(
        url="https://inflyser.github.io/CaseBattle/index.html"), # Replace with your web app URL
        )  
    
    return builder.as_markup()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
        await message.reply(
        "Привет! 👇",
        reply_markup=webapp_builder()
    )
        


bot = Bot(
    BOT_TOKEN,
    # session=AiohttpSession(proxy="socks5://user:pass@host:port"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(router)
    


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше указать точный адрес сайта на проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Запуск бота при старте
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    yield  # Здесь запускается сервер
    # Тут можно добавить код при завершении

app = FastAPI(lifespan=lifespan)
    
@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})


def verify_telegram_init_data(init_data: str) -> dict:
    """
    Проверка подписи данных, полученных из Telegram WebApp (initData).
    Возвращает словарь данных пользователя, если всё валидно.
    """
    parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    hash_from_telegram = parsed_data.pop("hash", None)
    if not hash_from_telegram:
        raise ValueError("Missing hash in init data")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
    hmac_hash = hmac.new(BOT_TOKEN_SECRET, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hmac_hash != hash_from_telegram:
        raise ValueError("Invalid data: hash mismatch")

    return parsed_data

@app.post("/auth/telegram")
async def telegram_auth(request: Request):
    data = await request.json()
    init_data = data.get("init_data")
    if not init_data:
        raise HTTPException(status_code=400, detail="No init_data")

    try:
        user_data = verify_telegram_init_data(init_data)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Auth failed: {str(e)}")

    # Здесь можно сохранять user_data в БД и возвращать токен
    return {"status": "ok", "user": user_data}

