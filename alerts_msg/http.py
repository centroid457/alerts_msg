from .main import *

import time
from typing import *
import requests


# =====================================================================================================================
pass


# =====================================================================================================================
class HttpAddress(NamedTuple):
    ADDR: str
    PORT: int
    ROUTE: str = ''


class HttpServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    LIDIA: HttpAddress = HttpAddress("http://192.168.74.20", 8080, "results")


# =====================================================================================================================
class AlertHttp(AlertBase):
    """HTTP realisation for sending msg (POSTs).
    """
    # SETTINGS ------------------------------------
    SERVER_HTTP: HttpAddress = HttpServers.LIDIA

    # AUX -----------------------------------------
    _conn:  'session'       # TODO: FINISH

    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    # TODO: FINISH
    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        """create session ???"""
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
