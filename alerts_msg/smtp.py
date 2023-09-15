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
    SERVER: SmtpAddress = SmtpServers.MAIL_RU

    # CONNECT =========================================================================================================
    def _connect(self) -> Optional[bool]:
        # self._mutex.acquire()

        result = None
        response = None

        if not self._conn_check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                self._conn = smtplib.SMTP_SSL(self.SERVER.ADDR, self.SERVER.PORT, timeout=5)
            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._clear()

        if self._conn_check_exists():
            try:
                response = self._conn.login(self.AUTH_USER, self.AUTH_PWD)
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

        # self._mutex.release()
        return result

    # MSG =============================================================================================================
    def _send(self):
        self._result = False
        sbj = f"{self.SUBJECT_PREFIX}{self._subj_suffix}" if self._subj_suffix else self.SUBJECT_PREFIX
        body = str(self._body) if self._body else ""

        msg = MIMEMultipart()
        msg["From"] = self.AUTH_USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = sbj
        msg.attach(MIMEText(body, _subtype=self._subtype))

        counter = 0
        while not self._conn_check_exists() and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try {counter=}")
                print("=" * 100)
                print()
                time.sleep(self.TIMEOUT_RECONNECT)

        if self._conn_check_exists():
            try:
                print(self._conn.send_message(msg))
            except Exception as exx:
                msg = f"[CRITICAL] unexpected [{exx!r}]"
                print(msg)
                self._clear()
                return

            print("-"*80)
            print(msg)
            print("-"*80)
            self._result = True


# =====================================================================================================================
if __name__ == "__main__":
    thread1 = AlertSmtp("thread1")
    thread2 = AlertSmtp("thread2")

    thread1.join()
    thread2.join()

    assert thread1._result is True
    assert thread2._result is True
