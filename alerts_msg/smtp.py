from .main import *

import time
from typing import *

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from private_values import *


# =====================================================================================================================
# TODO: cant solve not to use always connecting - tried many variants!
# make decition - use only one ability to send - only by instantiating!
# always will connecting! but always in threads! so dont mind!

# =====================================================================================================================
class SmtpAddress(NamedTuple):
    ADDR: str
    PORT: int


class SmtpServers:
    MAIL_RU: SmtpAddress = SmtpAddress("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp(AlertsBase):
    AUTH_USER: str = PrivateEnv.get("SMTP_USER")    # example@mail.ru
    AUTH_PWD: str = PrivateEnv.get("SMTP_PWD")     # use thirdPartyPwd!
    SMTP_SERVER: SmtpAddress = SmtpServers.MAIL_RU
    RECIPIENT: str = None

    # CONNECT =========================================================================================================
    def _connect_unsafe(self) -> Any:
        return smtplib.SMTP_SSL(self.SMTP_SERVER.ADDR, self.SMTP_SERVER.PORT, timeout=5)

    def _login_unsafe(self) -> Any:
        return self._conn.login(self.AUTH_USER, self.AUTH_PWD)

    # MSG =============================================================================================================
    def _send_unsafe(self) -> Any:
        body: Optional[str] = str(self._body or "")
        subj_suffix: Optional[str] = self._subj_suffix or ""
        _subtype: Optional[str] = self._subtype or "plain"

        msg = MIMEMultipart()
        msg["From"] = self.AUTH_USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = f"{self.SUBJECT_PREFIX}{subj_suffix}"
        msg.attach(MIMEText(body, _subtype=_subtype))

        self.MSG = msg

        print("Try", "-" * 80)
        print(self.MSG)
        print("Try", "-" * 80)

        return self._conn.send_message(msg)


# =====================================================================================================================
