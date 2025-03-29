import asyncio
from aiogram import Bot, Dispatcher, Router
from config import load_config
from logger import logger
from handler import router as handler_router



router = Router()
router.include_router(handler_router)

config = load_config(".env")

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()

async def main():    
    logger.info("Starting bot...")
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())