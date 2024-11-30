from dataclasses import dataclass

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


@dataclass
class Secrets:
    token: str = '7497797045:AAHHsuWNMyahGPl2SmMVHtLV0aE9wfSVs3M'

bot = Bot(token=Secrets.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
