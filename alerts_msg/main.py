import time
from typing import *

from PyQt5.QtCore import QThread

import smtplib
import telebot

from private_values import *


# =====================================================================================================================
pass


# =====================================================================================================================
class _AlertInterface:
    """Interface for Alerts

    RULES:
    - if some method cant exists (like for telegram) - just return True!
    - Dont return None!
    - Dont use Try sentences inside - it will be applied in upper logic!
    - Decide inside if it was success or not, and return conclusion True/False only.
    """
    def _connect_unsafe(self) -> Union[bool, NoReturn]:
        """establish connection to source
        """
        return True

    def _login_unsafe(self) -> Union[bool, NoReturn]:
        """authorise to source
        """
        return True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        """send msg
        """
        return True

    def _msg_compose(self) -> Union[str, 'MIMEMultipart']:
        """generate msg from existed data in attributes (passed before on init)
        """
        pass

    def _recipient_self_get(self) -> str:
        """RECIPIENT SelfSending, get from obvious class objects!
        """
        pass


# =====================================================================================================================
class AlertBase(_AlertInterface, QThread):     # REM: DONT ADD SINGLETON!!! SNMP WILL NOT WORK!!! and calling logic will be not simle!
    """Base class for Alert objects.

    FEATURE:
    - send msg,
    - threading
        - daemons
        - collect all active threads
        - wait all spawned threads finished

    :ivar SUBJECT_PREFIX: default prefix for subject
    :ivar SUBJECT_NAME: default name for subject
    :ivar body: actual msg body for alert
    :ivar _subtype: it used to change subtype only in smtp (http)

    :ivar BODY_TIMESTAMP_USE: append timestamp into the body
    :ivar TIMESTAMP: initiation timestamp for created instance

    :ivar RECONNECT_LIMIT: how many times it will try to reconnect, after - just close object
    :ivar RECONNECT_PAUSE: pause between reconnecting in seconds

    :ivar RECIPIENT_SPECIAL: recipient for sending msg
        None - if selfSending!

    :ivar _conn: actual connection object
    :ivar _result: result for alert state
        None - in process,
        False - finished UnSuccess,
        True - finished success!

    :ivar _threads_active: spawned (only active) threads
    """
    # SETTINGS ------------------------------------
    SUBJECT_PREFIX: Optional[str] = "[ALERT]"
    SUBJECT_NAME: Optional[str] = None
    body: Optional[str] = None
    _subtype: Optional[str] = "plain"

    BODY_TIMESTAMP_USE: bool = True
    TIMESTAMP: str = None

    RECONNECT_LIMIT: int = 10
    RECONNECT_PAUSE: int = 60
    # TIMEOUT_RATELIMIT: int = 600    # when EXX 451, b'Ratelimit exceeded

    RECIPIENT_SPECIAL: Optional[Any] = None

    # AUX -----------------------------------------
    _conn: Union[None, smtplib.SMTP_SSL, telebot.TeleBot] = None
    _result: Optional[bool] = None

    _threads_active: Set['AlertBase'] = set()

    # =================================================================================================================
    def __init__(self, body: Optional[Any] = None, _subj_name: Optional[str] = None, _subtype: Optional[str] = None):
        """Send msg

        :param body: define msg body
            None - just for research! (maybe deprecated!)
        :param _subj_name: reuse new subject name instead of default
        :param _subtype: reuse new _subtype instead of default
        """
        super().__init__(daemon=True)
        self.TIMESTAMP = time.strftime("%Y.%m.%d %H:%M:%S")

        # self._mutex: threading.Lock = threading.Lock()
        self.SUBJECT_NAME = _subj_name or self.SUBJECT_NAME
        self._subtype = _subtype or self._subtype

        # BODY ---------------
        if body is not None:
            body = str(body)
            if self.BODY_TIMESTAMP_USE:
                body += f"\n{self.TIMESTAMP}"
            self.body = body

            self.start()

    # =================================================================================================================
    def RECIPIENT(self) -> str:
        """RECIPIENT actual/final
        """
        return self.RECIPIENT_SPECIAL or self._recipient_self_get()

    @property
    def SUBJECT(self) -> str:
        """final msg subject, composed with name and prefix.
        """
        if self.SUBJECT_NAME is None:
            self.SUBJECT_NAME = self.NAME
        return self.SUBJECT_PREFIX + self.SUBJECT_NAME

    @classmethod
    @property
    def NAME(cls) -> str:
        """name for AlertClass.
        Accustom ourselves to name you classes recognisable without adding new one redundant attributes.
        """
        return cls.__name__

    # =================================================================================================================
    def start(self):
        """this is just add ability to collect started threads in class
        """
        self.__class__._threads_active.add(self)
        super().start()

    def _thread_finished(self):
        """del thread object from collection.
        called then thread finished.
        """
        self.__class__._threads_active.discard(self)

    @classmethod
    def threads_wait_all(cls):
        """wait while all spawned active threads will finished.
        """
        try:
            time.sleep(1)
            while cls._threads_active:
                list(cls._threads_active)[0].join()
        except:
            pass

    def result_wait(self) -> Optional[bool]:
        """wait for finish thread and get succession result.
        Created for tests mainly! but you can use!
        """
        self.join()
        return self._result

    # =================================================================================================================
    def _conn__check_exists(self) -> bool:
        """check if connection object exists
        """
        return self._conn is not None

    def _conn__disconnect(self) -> None:
        """disconnect connection object
        """
        if self._conn:
            self._conn.quit()
        self._conn__clear()

    def _conn__clear(self) -> None:
        """del connection object
        """
        self._conn = None

    def _connect(self) -> Optional[bool]:
        """create connection object
        """
        result = None
        if not self._conn__check_exists():
            print(f"TRY _connect {self.__class__.__name__}")
            try:
                if self._connect_unsafe():
                    print("[READY] connect")

            except Exception as exx:
                print(f"[CRITICAL] CONNECT [{exx!r}]")
                self._conn__clear()

        if self._conn__check_exists():
            try:
                result = self._login_unsafe()
                if result:
                    print("[READY] login")
            except Exception as exx:
                print(f"[CRITICAL] LOGIN [{exx!r}]")
                self._conn__clear()

        print("="*100)
        print("="*100)
        print("="*100)
        print()

        return result

    # =================================================================================================================
    def run(self) -> None:
        """main logic which manage started thread
        """
        counter = 0
        while not self._conn__check_exists() and counter <= self.RECONNECT_LIMIT:
            counter += 1
            if not self._connect():
                print(f"[WARNING]try [{counter=}]")
                print("=" * 100)
                print()
                time.sleep(self.RECONNECT_PAUSE)

        print("[Try send", "-" * 80)
        print(self._msg_compose())
        print("Try send]", "-" * 80)

        if self._conn__check_exists():
            try:
                result = self._send_unsafe()
                if result:
                    print("[READY] send")
                    self._result = True
            except Exception as exx:
                msg = f"[CRITICAL]unexpected [{exx!r}]"
                print(msg)
                self._conn__clear()

        print()
        print()
        print()

        if self._result is None:
            self._result = False

        self._thread_finished()


# =====================================================================================================================
