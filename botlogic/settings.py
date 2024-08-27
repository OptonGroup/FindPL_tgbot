from dataclasses import dataclass

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


@dataclass
class Secrets:
    token: str = '7524225732:AAG-7O-riqPfQ4uQGUa47GxJc28KSH4r5nM'

bot = Bot(token=Secrets.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
