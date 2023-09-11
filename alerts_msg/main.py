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
    """
    main class to work with smtp.
    """
    SMTP_USER: str = EnvValues.get("SMTP_USER")    # example@mail.ru
    SMTP_PWD: str = EnvValues.get("SMTP_PWD")     # use thirdPartyPwd!

    SERVER: SmtpAddress = SmtpServers.MAIL_RU
    TIMEOUT_RECONNECT: int = 60
    RECONNECT_LIMIT: int = 10

    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: str = SMTP_USER

    _smtp: Optional[smtplib.SMTP_SSL] = None

    def __init__(self):
        super().__init__()
        self._connect()

    # CONNECT =========================================================================================================
    def _connect(self) -> Optional[bool]:
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
    def send(self, subject: str, body: Any, _subtype="plain") -> Optional[bool]:
        FROM = self.SMTP_USER
        TO = self.RECIPIENT
        SUBJECT = subject
        BODY = str(body)

        msg = MIMEMultipart()
        msg['Subject'] = SUBJECT
        msg["From"] = FROM
        msg["To"] = TO
        msg.attach(MIMEText(BODY, _subtype=_subtype))

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
            return True


# =====================================================================================================================
if __name__ == "__main__":
    sender = AlertSmtp()
    for subj, body, _subtype in [("[ALERT]plain123", "plain123", "plain123"), ("[ALERT]plain", "plain", "plain"), ("[ALERT]html", "<p><font color='red'>html(red)</font></p>", "html")]:
        sender.send(subj, body, _subtype)
