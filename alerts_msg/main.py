import time
from typing import *
import abc

import threading

import smtplib
import telebot
from email.mime.multipart import MIMEMultipart

from private_values import *


# =====================================================================================================================
class _AlertInterface(abc.ABC):
    """
    if some method dont exists (like for telegram) - return True!
    Dont return None!
    Dont use Try sentences inside - it will be applied in upper logic!
    Decide inside if it was success or not, and return conclusion True/False only.
    """
    @abc.abstractmethod
    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        pass

    @abc.abstractmethod
    def _login_unsafe(self) -> Union[bool, NoReturn]:
        pass

    @abc.abstractmethod
    def _send_unsafe(self) -> Union[bool, NoReturn]:
        pass

    @property
    @abc.abstractmethod
    def MSG(self) -> Union[str, MIMEMultipart]:
        pass


# =====================================================================================================================
class AlertBase(_AlertInterface, threading.Thread):     # DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simle!
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"
    SUBJECT_SUFFIX_DEF: Optional[str] = ""

    AUTH: PrivateAuto = None

    RECONNECT_LIMIT: int = 10
    TIMEOUT_RECONNECT: int = 60
    TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT: Union[str, int] = None   #leave None if selfSending!
    TIMESTAMP_USE: bool = True

    _conn: Union[None, smtplib.SMTP_SSL, telebot.TeleBot] = None
    _result: Optional[bool] = None   # None-in process, False - finished UnSuccess, True - finished success!

    _threads_active: Set['AlertBase'] = set()

    # =================================================================================================================
    def __init__(self, body: Optional[str] = None, subj_suffix: Optional[str] = None, _subtype: Optional[str] = None):
        super().__init__(daemon=True)

        self._thread_started()

        # self._mutex: threading.Lock = threading.Lock()
        self.RECIPIENT = self.RECIPIENT or self.AUTH.USER
        self.TIMESTAMP: str = time.strftime("%Y.%m.%d %H:%M:%S")

        body = str(body or "")
        if self.TIMESTAMP_USE:
            body += f"\n{self.TIMESTAMP}"

        self._body: Optional[str] = body
        self._subj_suffix: Optional[str] = subj_suffix or self.SUBJECT_SUFFIX_DEF or ""
        self._subtype: Optional[str] = _subtype or "plain"

        if body:
            self.start()

    # =================================================================================================================
    def _thread_started(self):
        self.__class__._threads_active.add(self)

    def _thread_finished(self):
        self.__class__._threads_active.discard(self)

    @classmethod
    def threads_wait_all(cls):
        try:
            time.sleep(1)
            while cls._threads_active:
                list(cls._threads_active)[0].join()
        except:
            pass

    # =================================================================================================================
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
        result = None
        if not self._conn_check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                if self._connect_unsafe():
                    print("[READY] connect")

            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._clear()

        if self._conn_check_exists():
            try:
                result = self._login_unsafe()
                if result:
                    print("[READY] login")
            except Exception as exx:
                print(f"[CRITICAL] LOGIN [{exx!r}]")
                self._clear()

        print("="*100)
        print("="*100)
        print("="*100)
        print()

        return result

    # =================================================================================================================
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

        print("[Try send", "-" * 80)
        print(self.MSG)
        print("Try send]", "-" * 80)

        if self._conn_check_exists():
            try:
                result = self._send_unsafe()
                if result:
                    print("[READY] send")
                    self._result = True
            except Exception as exx:
                msg = f"[CRITICAL]unexpected [{exx!r}]"
                print(msg)
                self._clear()

        print()
        print()
        print()

        if self._result is None:
            self._result = False

        self._thread_finished()


# =====================================================================================================================
