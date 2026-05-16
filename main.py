import asyncio
from aiogram import Bot, Dispatcher
from bot.config.config import BOT_TOKEN
from bot.handlers.handlers import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print("✅ Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
