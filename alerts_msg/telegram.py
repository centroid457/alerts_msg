from .main import *

import time
from typing import *

import telebot

from private_values import *


# =====================================================================================================================
class RecipientTgID(PrivateAuto):
    """Object to get telegram RecipientId
    """
    SECTION = "TG_ID"
    MyTgID: str


# =====================================================================================================================
class AlertTelegram(AlertBase):
    """realisation for sending Telegeam msg.

    :ivar AUTH: object with USER/PWD attributes for authorisation
    :ivar SERVER_SMTP: SmtpAddress object
    """
    SERVER_TG: PrivateTgBotAddressAuto = PrivateTgBotAddressAuto(_section="TGBOT_DEF")
    _conn: telebot.TeleBot

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = telebot.TeleBot(token=self.SERVER_TG.TOKEN)
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(chat_id=self.RECIPIENT, text=self._msg_compose())
        return True

    def _msg_compose(self) -> str:
        msg = f"{self.SUBJECT}\n{self.body}"
        return msg

    def _recipient_self_get(self) -> str:
        return RecipientTgID().MyTgID


# =====================================================================================================================
