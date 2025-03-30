import asyncio
from aiogram import Bot, Dispatcher, Router
from config import load_config
from logger import logger
from handler import router as handler_router


class BotApp:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.bot = Bot(token=self.config.tg_bot.token)
        self.dp = Dispatcher()
        self.router = Router()
        self._setup_routes()

    def _setup_routes(self):
        """Include all routers."""
        self.router.include_router(handler_router)
        self.dp.include_router(self.router)

    async def start(self):
        """Start the bot."""
        logger.critical("Starting bot...")
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    app = BotApp(".env")
    asyncio.run(app.start())
