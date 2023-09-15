import time
from typing import *

import threading

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from private_values import *
from singleton_meta import *


# =====================================================================================================================
class AlertsBase(threading.Thread):     # DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simle!
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"

    AUTH_USER: str = None
    AUTH_PWD: str = None
    SERVER: Any = None

    RECONNECT_LIMIT: int = 10
    TIMEOUT_RECONNECT: int = 60
    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: str = None   #leave None if selfSending!

    _conn: Union[None, smtplib.SMTP_SSL] = None
    _result: Optional[bool] = None   # careful!

    def __init__(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None):
        super().__init__(daemon=True)

        # self._mutex: threading.Lock = threading.Lock()

        self._body: Optional[str] = body
        self._subj_suffix:Optional[str] = subj_suffix
        self._subtype: Optional[str] = _subtype or "plain"

        if not self.RECIPIENT:
            self.RECIPIENT = self.AUTH_USER

        self.start()

    def _conn_check_exists(self) -> bool:
        return self._conn is not None

    def _disconnect(self) -> None:
        if self._conn:
            self._conn.quit()
        self._clear()

    def _clear(self) -> None:
        self._conn = None

    def result_wait(self) -> Optional[bool]:
        """
        for tests mainly! but you can use!
        :return:
        """
        self.join()
        return self._result

    def run(self):
        self._send()

    def _send(self):
        raise NotImplementedError()


# =====================================================================================================================
