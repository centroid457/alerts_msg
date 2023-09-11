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

    # CONNECT =========================================================================================================
    @classmethod
    def _connect(cls) -> Optional[bool]:
        result = None

        if not cls._smtp:
            print(f"TRY _connect {cls.__class__.__name__}")
            try:
                cls._smtp = smtplib.SMTP_SSL(cls.SERVER.ADDR, cls.SERVER.PORT, timeout=5)
            except Exception as exx:
                print(f"[CRITICAL] CONNECT {exx!r}")
                cls._clear()

        if cls._smtp:
            try:
                result = cls._smtp.login(cls.SMTP_USER, cls.SMTP_PWD)
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

    @classmethod
    def _disconnect(cls) -> None:
        if cls._smtp:
            cls._smtp.quit()
        cls._clear()

    @classmethod
    def _clear(cls) -> None:
        cls._smtp = None

    # MSG =============================================================================================================
    @classmethod
    def send(cls, subject: str, body: Any, _subtype="plain") -> Optional[bool]:
        FROM = cls.SMTP_USER
        TO = cls.RECIPIENT
        SUBJECT = subject
        BODY = str(body)

        msg = MIMEMultipart()
        msg['Subject'] = SUBJECT
        msg["From"] = FROM
        msg["To"] = TO
        msg.attach(MIMEText(BODY, _subtype=_subtype))

        counter = 0
        while not cls._smtp and counter <= cls.RECONNECT_LIMIT:
            counter += 1
            if not cls._connect():
                print(f"[WARNING]try {counter=}")
                print("=" * 100)
                print()
                time.sleep(cls.TIMEOUT_RECONNECT)

        if cls._smtp:
            try:
                print(cls._smtp.send_message(msg))
            except Exception as exx:
                msg = f"[CRITICAL] unexpected {exx!r}"
                print(msg)
                cls._clear()
                return

            print("-"*80)
            print(msg)
            print("-"*80)
            return True


# =====================================================================================================================
if __name__ == "__main__":
    for subj, body, _subtype in [("[ALERT]plain123", "plain123", "plain123"), ("[ALERT]plain", "plain", "plain"), ("[ALERT]html", "<p><font color='red'>html(red)</font></p>", "html")]:
        AlertSmtp.send(subj, body, _subtype)
