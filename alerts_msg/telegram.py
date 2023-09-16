from .main import *

import time
from typing import *

import telebot
import random

from private_values import *
from singleton_meta import *


# =====================================================================================================================
class AlertTelegram(AlertsBase):
    TG_BOTADDRESS: PrivateJsonTgBotAddress = PrivateJsonTgBotAddress().get_section("TGBOT1")
    RECIPIENT: int = PrivateJson().get("MyTgID")

    # CONNECT =========================================================================================================
    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = telebot.TeleBot(token=self.TG_BOTADDRESS.TOKEN)
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        return True

    # MSG ========================================================================================================
    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(chat_id=self.RECIPIENT, text=self._body)
        return True


# =====================================================================================================================
