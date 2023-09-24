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
    ADDR: str
    PORT: int


class SmtpServers:
    MAIL_RU: SmtpAddress = SmtpAddress("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp(AlertBase):
    AUTH: PrivateAuto = PrivateAuto(_section="AUTH_EMAIL_DEF")
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
        self._conn.send_message(self.MSG)
        return True

    @property
    def MSG(self) -> MIMEMultipart:
        body: str = self._body
        subj_suffix: str = self._subj_suffix
        _subtype: str = self._subtype

        msg = MIMEMultipart()
        msg["From"] = self.AUTH.USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = f"{self.SUBJECT_PREFIX}{subj_suffix}"
        msg.attach(MIMEText(body, _subtype=_subtype))
        return msg


# =====================================================================================================================
