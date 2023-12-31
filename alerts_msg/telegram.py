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

    @property
    def RECIPIENT_SELF(self) -> str:
        return RecipientTgID().MyTgID


# =====================================================================================================================
