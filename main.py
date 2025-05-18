from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import asyncio, os

from aiogram import Router, Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv

load_dotenv()
# Load the bot token from the .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")


def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="", web_app=WebAppInfo(
        url="https://t.me/GiftsCaseBattlebot/GiftsCaseBattle"), # Replace with your web app URL
        )  
    
    return builder.as_markup()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
        await message.reply(
        reply_markup = webapp_builder()
    )
        
async def main():
    bot = Bot(BOT_TOKEN, parse_mod = ParseMode.HTML)
    
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:    
        print("Бот выключен.")



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Лучше указать точный адрес сайта на проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)