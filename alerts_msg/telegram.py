from .main import *

import time
from typing import *

import telebot

from private_values import *


# =====================================================================================================================
class PrivateTgID(PrivateAuto):
    SECTION = "TG_ID"
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(AlertBase):
    SERVER_TG: PrivateTgBotAddressAuto = PrivateTgBotAddressAuto(_section="TGBOT_DEF")
    RECIPIENT: int = PrivateTgID().MyTgID

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = telebot.TeleBot(token=self.SERVER_TG.TOKEN)
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(chat_id=self.RECIPIENT, text=self.MSG)
        return True

    @property
    def MSG(self) -> str:
        msg = f"{self.SUBJECT}\n{self.body}"
        return msg


# =====================================================================================================================
