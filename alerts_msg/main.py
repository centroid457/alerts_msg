import time
from typing import *

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from private_values import *


# =====================================================================================================================
class SmtpAddress(NamedTuple):
    ADDR: str
    PORT: int


class SmtpServers:
    MAIL_RU: SmtpAddress = SmtpAddress("smtp.mail.ru", 465)


# =====================================================================================================================
class AlertSmtp:
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"

    SMTP_USER: str = PrivateEnv.get("SMTP_USER")    # example@mail.ru
    SMTP_PWD: str = PrivateEnv.get("SMTP_PWD")     # use thirdPartyPwd!

    SERVER: SmtpAddress = SmtpServers.MAIL_RU
    TIMEOUT_RECONNECT: int = 60
    RECONNECT_LIMIT: int = 10

    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: str = None

    result: Optional[bool] = None   # for thread

    def __init__(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None):
        super().__init__()

        self._smtp: Optional[smtplib.SMTP_SSL] = None
        if not self.RECIPIENT:
            self.RECIPIENT = self.SMTP_USER

        if body:
            self._send(subj_suffix=subj_suffix, body=body, _subtype=_subtype)

    # CONNECT =========================================================================================================
    def _connect(self) -> Optional[bool]:
        self.result = None

        result = None

        if not self._smtp:
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                self._smtp = smtplib.SMTP_SSL(self.SERVER.ADDR, self.SERVER.PORT, timeout=5)
            except Exception as exx:
                print(f"[CRITICAL] CONNECT {exx!r}")
                self._clear()

        if self._smtp:
            try:
                result = self._smtp.login(self.SMTP_USER, self.SMTP_PWD)
            except Exception as exx:
                print(f"[CRITICAL] LOGIN {exx!r}")

            print(result)
            print("="*100)

        if result and result[0] in [235, 503]:
            print("[READY] connection")
            print("="*100)
            print("="*100)
            print("="*100)
            print()
            return True

    def _disconnect(self) -> None:
        if self._smtp:
            self._smtp.quit()
        self._clear()

    def _clear(self) -> None:
        self._smtp = None

    # MSG =============================================================================================================
    def _send(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None) -> Optional[bool]:
        self.result = False
        _subtype = _subtype or "plain"

        sbj = f"{self.SUBJECT_PREFIX}{subj_suffix}" if subj_suffix else self.SUBJECT_PREFIX
        body = str(body) if body else ""

        msg = MIMEMultipart()
        msg["From"] = self.SMTP_USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = sbj
        msg.attach(MIMEText(body, _subtype=_subtype))

        counter = 0
        while not self._smtp and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try {counter=}")
                print("=" * 100)
                print()
                time.sleep(self.TIMEOUT_RECONNECT)

        if self._smtp:
            try:
                print(self._smtp.send_message(msg))
            except Exception as exx:
                msg = f"[CRITICAL] unexpected {exx!r}"
                print(msg)
                self._clear()
                return

            print("-"*80)
            print(msg)
            print("-"*80)
            self.result = True
            return True


# =====================================================================================================================
if __name__ == "__main__":
    pass
