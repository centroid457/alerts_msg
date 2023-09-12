import time
from typing import *

import threading

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
class AlertSmtp(threading.Thread):
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"

    SMTP_USER: str = PrivateEnv.get("SMTP_USER")    # example@mail.ru
    SMTP_PWD: str = PrivateEnv.get("SMTP_PWD")     # use thirdPartyPwd!

    SERVER: SmtpAddress = SmtpServers.MAIL_RU
    TIMEOUT_RECONNECT: int = 60
    RECONNECT_LIMIT: int = 10

    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: str = None   #leave None if selfSending!

    _smtp: Optional[smtplib.SMTP_SSL] = None
    _result: Optional[bool] = None   # careful!

    def __init__(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None):
        super().__init__(daemon=True)

        self._body: Optional[str] = body
        self._subj_suffix:Optional[str] = subj_suffix
        self._subtype: Optional[str] = _subtype or "plain"

        if not self.RECIPIENT:
            self.RECIPIENT = self.SMTP_USER

        self.start()

    def result_wait(self) -> Optional[bool]:
        """
        for tests mainly! but you can use!
        :return:
        """
        self.join()
        return self._result

    # CONNECT =========================================================================================================
    def _connect(self) -> Optional[bool]:
        result = None
        response = None

        if not self._smtp_check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                self._smtp = smtplib.SMTP_SSL(self.SERVER.ADDR, self.SERVER.PORT, timeout=5)
            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._clear()

        if self._smtp_check_exists():
            try:
                response = self._smtp.login(self.SMTP_USER, self.SMTP_PWD)
            except Exception as exx:
                print(f"[CRITICAL] LOGIN [{exx!r}]")

            print(response)
            print("="*100)

        if response and response[0] in [235, 503]:
            print("[READY] connection")
            print("="*100)
            print("="*100)
            print("="*100)
            print()
            result = True

        return result

    def _smtp_check_exists(self) -> bool:
        return self._smtp is not None

    def _disconnect(self) -> None:
        if self._smtp:
            self._smtp.quit()
        self._clear()

    def _clear(self) -> None:
        self._smtp = None

    # MSG =============================================================================================================
    def run(self):
        self._result = False
        sbj = f"{self.SUBJECT_PREFIX}{self._subj_suffix}" if self._subj_suffix else self.SUBJECT_PREFIX
        body = str(self._body) if self._body else ""

        msg = MIMEMultipart()
        msg["From"] = self.SMTP_USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = sbj
        msg.attach(MIMEText(body, _subtype=self._subtype))

        counter = 0
        while not self._smtp_check_exists() and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try {counter=}")
                print("=" * 100)
                print()
                time.sleep(self.TIMEOUT_RECONNECT)

        if self._smtp_check_exists():
            try:
                print(self._smtp.send_message(msg))
            except Exception as exx:
                msg = f"[CRITICAL] unexpected [{exx!r}]"
                print(msg)
                self._clear()
                return

            print("-"*80)
            print(msg)
            print("-"*80)
            self._result = True

    def _send_thread(self) -> None:
        self.start()


# =====================================================================================================================
if __name__ == "__main__":
    thread1 = AlertSmtp("thread1")
    thread2 = AlertSmtp("thread2")

    thread1.join()
    thread2.join()

    assert thread1._result is True
    assert thread2._result is True
