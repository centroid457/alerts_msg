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
    def _connect_unsafe(self) -> Any:
        return smtplib.SMTP_SSL(self.SERVER.ADDR, self.SERVER.PORT, timeout=5)

    def _login_unsafe(self) -> Any:
        return self._conn.login(self.AUTH_USER, self.AUTH_PWD)

    # MSG =============================================================================================================
    def run(self):
        self._result = False

        # load in thread to release attrs in object - so we can use next thread!!!
        body: Optional[str] = str(self._body)
        subj_suffix: Optional[str] = self._subj_suffix
        _subtype: Optional[str] = self._subtype

        self._mutex.release()

        msg = MIMEMultipart()
        msg["From"] = self.AUTH_USER
        msg["To"] = self.RECIPIENT
        msg['Subject'] = f"{self.SUBJECT_PREFIX}{subj_suffix}"
        msg.attach(MIMEText(body, _subtype=_subtype))

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
