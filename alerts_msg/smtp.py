from .main import *

import time
from typing import *

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from private_values import *


# =====================================================================================================================
# TODO: cant solve not to use always connecting - tried many variants!
# make decision - use only one ability to send - only by instantiating!
# always will connecting! but always in threads! so dont mind!


# =====================================================================================================================
class SmtpAddress(NamedTuple):
    """class for keeping connection parameters/settings for exact smtp server

    :ivar ADDR: smtp server address like "smtp.mail.ru"
    :ivar PORT: smtp server port like 465
    """
    ADDR: str
    PORT: int


class SmtpServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    MAIL_RU: SmtpAddress = SmtpAddress("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp(AlertBase):
    """SMTP realisation for sending email msg.

    :ivar AUTH: object with USER/PWD attributes for authorisation (see PrivateAuth/PrivateAuto for details)
    :ivar SERVER_SMTP: SmtpAddress object
    """
    AUTH: PrivateAuth = PrivateAuto(_section="AUTH_EMAIL_DEF")
    SERVER_SMTP: SmtpAddress = SmtpServers.MAIL_RU

    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        self._conn = smtplib.SMTP_SSL(self.SERVER_SMTP.ADDR, self.SERVER_SMTP.PORT, timeout=5)
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        response = self._conn.login(self.AUTH.USER, self.AUTH.PWD)
        print(response)
        print("=" * 100)
        return response and response[0] in [235, 503]

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        self._conn.send_message(self._msg_compose())
        return True

    def _msg_compose(self) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.AUTH.USER
        msg["To"] = self.RECIPIENT_SPECIAL or self.AUTH.USER
        msg['Subject'] = self.SUBJECT
        msg.attach(MIMEText(self.body, _subtype=self._subtype))
        return msg

    def _recipient_self_get(self) -> str:
        return self.AUTH.USER


# =====================================================================================================================
