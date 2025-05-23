from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Form, HTTPException, Depends

import asyncio, os
import hmac
import hashlib
import json
from typing import Dict
import urllib.parse

from urllib.parse import parse_qsl
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from aiogram import Router, Dispatcher, Bot, F, types
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

from deps import get_db
from models import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime



load_dotenv()
# Load the bot token from the .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN_SECRET = hashlib.sha256(BOT_TOKEN.encode()).digest()

def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Click", web_app=WebAppInfo(
        url="https://inflyser.github.io/CaseBattle/index.html"), # Replace with your web app URL
        )  
    
    return builder.as_markup()

router = Router()

text_start = """
🎁Открывай бесплатные и авторские кейсы с NFT-подарками!

🚀Апгрейди свои подарки до более ценных.

✅Испытай удачу с нами!
"""

@router.message(CommandStart())
async def start(message: Message):
        await message.answer(
        # "AgACAgIAAxkBAANUaCyoSECX2QaSUXFDybrTYxRfrP4AAqryMRv0RmhJL_ElFcky29kBAAMCAAN4AAM2BA",
        "Starting - Bot correct!",
        reply_markup=webapp_builder()
    )
        

bot = Bot(
    BOT_TOKEN,
    # session=AiohttpSession(proxy="socks5://user:pass@host:port"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(router)
    

# Запуск бота при старте
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook("https://giftcasebattle.onrender.com/telegram")
    yield  # Здесь запускается сервер
    # Тут можно добавить код при завершении


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # https://inflyser.github.io
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return JSONResponse(content={"status": "ok", "message": "Backend is alive!"})

def flatten_data(data):
    """
    Разворачивает вложенный JSON в ключи вида user.id=1423388201
    Telegram требует именно такой формат для подписи.
    """
    items = []
    for k, v in data.items():
        if isinstance(v, str):
            # Может быть JSON в строке? Попробуем распарсить
            try:
                parsed = json.loads(v)
                if isinstance(parsed, dict):
                    for sub_k, sub_v in parsed.items():
                        items.append((f"{k}.{sub_k}", str(sub_v)))
                    continue
            except:
                pass
            items.append((k, v))
        else:
            items.append((k, str(v)))
    return dict(items)

def validate_telegram_auth(init_data: str):
    # Преобразуем init_data в dict
    parsed_data = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    
    # Получаем signature и удаляем из словаря
    received_hash = parsed_data.pop('hash', None) or parsed_data.pop('signature', None)

    # Сортируем и формируем data_check_string
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(parsed_data.items())])

    # Вычисляем свой хеш
    computed_hash = hmac.new(BOT_TOKEN_SECRET, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(received_hash, computed_hash)


@app.post("/auth/telegram")
async def auth_telegram(
    init_data: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Шаг 1: Валидация
    if not validate_telegram_auth(init_data):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Шаг 2: Парсинг данных
    parsed = dict(urllib.parse.parse_qsl(init_data))
    try:
        user_data = json.loads(parsed.get("user", "{}"))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user data")

    user_id = int(user_data.get("id"))

    # Шаг 3: Дополнительные данные (аватарка и пр.)
    photo_url = await get_user_photo_url(bot, user_id)
    user_data["photo_url"] = photo_url or ""

    # Шаг 4: Работа с базой
    try:
        result = await db.execute(select(User).where(User.telegram_id == user_id))
        db_user = result.scalar_one_or_none()

        if db_user:
            db_user.username = user_data.get("username")
            db_user.first_name = user_data.get("first_name")
            db_user.last_name = user_data.get("last_name")
            db_user.updated_at = datetime.utcnow()
        else:
            db_user = User(
                telegram_id=user_id,
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
            )
            db.add(db_user)

        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    # Шаг 5: Ответ
    return JSONResponse(content={"status": "ok", "user": user_data})



async def get_user_photo_url(bot: Bot, user_id: int) -> str | None:
    photos = await bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        file_id = photos.photos[0][0].file_id  # первая фотка, первый размер
        file = await bot.get_file(file_id)
        # Ссылка на файл
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
        return photo_url
    return None

@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    
