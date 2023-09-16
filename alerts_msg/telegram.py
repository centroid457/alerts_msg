from .main import *

import time
from typing import *

import telebot

from private_values import *


# =====================================================================================================================
class AlertTelegram(AlertBase):
    SERVER_TG: PrivateJsonTgBotAddress = PrivateJsonTgBotAddress().get_section("TGBOT1")
    RECIPIENT: int = PrivateJson().get("MyTgID")

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
        body: str = str(self._body or "")
        subj_suffix: str = self._subj_suffix or ""
        subj = f"{self.SUBJECT_PREFIX}{subj_suffix}"
        msg = subj + body
        return msg


# =====================================================================================================================
