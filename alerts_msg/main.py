import time
from typing import *

import threading

import smtplib
import telebot

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from private_values import *
from singleton_meta import *


# =====================================================================================================================
class AlertsBase(threading.Thread):     # DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simle!
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"

    AUTH_USER: str = None
    AUTH_PWD: str = None

    RECONNECT_LIMIT: int = 10
    TIMEOUT_RECONNECT: int = 60
    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: Union[str, int] = None   #leave None if selfSending!

    _conn: Union[None, smtplib.SMTP_SSL, telebot.TeleBot] = None
    _result: Optional[bool] = None   # None-in process, False - finished UnSuccess, True - finished success!

    MSG: Any = None

    def __init__(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None):
        super().__init__(daemon=True)

        # self._mutex: threading.Lock = threading.Lock()
        self.RECIPIENT = self.RECIPIENT or self.AUTH_USER

        self._body: Optional[str] = body
        self._subj_suffix: Optional[str] = subj_suffix
        self._subtype: Optional[str] = _subtype

        if body:
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

    def _connect(self) -> Optional[bool]:
        # self._mutex.acquire()

        result = None
        response = None

        if not self._conn_check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                self._conn = self._connect_unsafe()
            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._clear()

        if self._conn_check_exists():
            try:
                response = self._login_unsafe()
                print(response)
                print("=" * 100)
            except Exception as exx:
                print(f"[CRITICAL] LOGIN [{exx!r}]")
                self._clear()

        if response and response[0] in [235, 503]:
            print("[READY] connection")
            print("="*100)
            print("="*100)
            print("="*100)
            print()
            result = True

        # self._mutex.release()
        return result

    def run(self) -> None:
        """
        result see in self._result
        :return:
        """
        counter = 0
        while not self._conn_check_exists() and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try [{counter=}]")
                print("=" * 100)
                print()
                time.sleep(self.TIMEOUT_RECONNECT)

        if self._conn_check_exists():
            try:
                print(self._send_unsafe())
            except Exception as exx:
                msg = f"[CRITICAL]unexpected [{exx!r}]"
                print(msg)
                self._clear()
                self._result = False
                return

            print(f"[OK] msg send!")
            print()

            self._result = True

    # OVERWRITE -------------------------------------------------------------------------------------------------------
    def _connect_unsafe(self) -> Any:
        raise NotImplementedError()

    def _login_unsafe(self) -> Any:
        raise NotImplementedError()

    def _send_unsafe(self) -> None:
        raise NotImplementedError()


# =====================================================================================================================
