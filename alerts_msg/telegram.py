from .main import *

import time
from typing import *

import telebot
import random

from private_values import *
from singleton_meta import *


# =====================================================================================================================
class AlertTelegram(AlertsBase):
    _INSTANCE_ID: int = None

    ADDRESS: PrivateJsonTgBotAddress = PrivateJsonTgBotAddress().get_section("TGBOT1")
    RECIPIENT_ID: int = PrivateJson().get("MyTgID")

    MSG_START = "============= START WORKING ============="
    MSG_STOP = "============= STOP WORKING ============="

    # INIT ============================================================================================================
    def __init__(self):
        super().__init__(daemon=True)

        self._INSTANCE_ID = random.randrange(10000)

        self.msg_cmds: Dict[str, Callable] = {
            # dont use slash sign here! is is incorrect!
            "MAIN_MSG": self.tg_msg__send__main,
            "DATETIME": self.tg_msg__send__time,
        }
        self.MSG_CMDS_update()

        self._conn = telebot.TeleBot(token=self.ADDRESS.TOKEN)
        self.handlers_init()
        self.send_start()

    def __del__(self):
        self.tg_msg__send(text=self.MSG_STOP)

    # init HANDLERS ---------------------------------------------------------------------------------------------------
    def MSG_CMDS_update(self) -> None:
        """
        reinit if you need add new cmds!
        :return:
        """
        cmds: Dict[str, Callable] = {}
        if cmds:
            self.msg_cmds.update(cmds)

    def handlers_init(self):
        """
        this is implementation for standart code:
            @bot.message_handler(commands=['start'])
            @bot.message_handler(func=lambda message: True)
            async def echo_message(message):
                await bot.reply_to(message, message.text)

        https://stackoverflow.com/questions/61854767/decorators-in-class-methods
        """
        self._tg_handlers_init__1_commands()
        self._tg_handlers_init__2_any_comment()

    def _tg_handlers_init__1_commands(self) -> None:
        for name, func in self.HANDLERS.items():
            self._conn.register_message_handler(func, commands=[name])

    def _tg_handlers_init__2_any_comment(self) -> None:
        handler_dict = dict(
            function=lambda msg: self.tg_msg__reply(msg, text=None),
            filters=dict(
                # commands=["start"],
            )
        )
        self._conn.add_message_handler(handler_dict)

    def run(self):
        self._conn.infinity_polling()

    # MSG PARTS ========================================================================================================
    def tg_msg__get_active(self, _msg: Optional[telebot.types.Message] = None):
        _msg = _msg or self.TG_MSG__LAST_SEND
        return _msg

    def TG_MSG__LAST_SEND__clear(self) -> None:
        self.TG_MSG__LAST_SEND = None

    # TEXT WORK -------------------------------------------
    def _tg_msg__wrap(self, msg: Union[str, telebot.types.Message], _id: int = None, wrap_line: str = None, _add_footer: bool = None) -> str:
        # input -------------------------------
        if isinstance(msg, telebot.types.Message):
            text = msg.text
            _id = msg.message_id
        elif isinstance(msg, str):
            text = msg
        else:
            text = str(msg)

        wrap_line = wrap_line or self.TG_MSG__LINE__WRAP_MAIN
        # del old ---------------------------
        try:
            text = text.split(wrap_line, 2)[1].strip()
        except:
            pass

        # wrap ---------------------------
        result = f"{wrap_line}\n"
        result += f"{text.strip()}\n"
        result += f"{wrap_line}"

        if _add_footer:
            result += "\n"
            # add cmds ---------------------------
            result += self._tg_msg__create__cmds()

            # add id ---------------------------
            result += f"[{_id}/bot_{self._INSTANCE_ID}]\n"

            # add datetime ---------------------------
            result += f"{self._tg_msg__create__time()}\n"
        return result

    def _tg_msg__wrap_with_footer(self, **kwargs) -> str:
        return self._tg_msg__wrap(**kwargs, _add_footer=True)

    def _tg_msg__create__main(self) -> str:
        result = "MAIN MSG"
        return result

    def _tg_msg__create__cmds(self) -> str:
        result = ""
        for cmd in self.HANDLERS:
            result += f"/{cmd}\n"
        return result

    @staticmethod
    def _tg_msg__create__time() -> str:
        return str(time.strftime("%Y.%m.%d__%H:%M:%S"))

    def _tg_msg__create__separated_from_list(self, text_list: List[str]) -> str:
        result = ""
        count = len(text_list)
        for pos, line in enumerate(text_list, start=1):
            result += line.strip() + "\n"
            if pos != count:
                result += self.TG_MSG__LINE__SEPARATE + "\n"

        return result

    # SEND/REPLY -------------------------------------------
    def tg_msg_last__refresh_footer(self):
        self.tg_msg__edit()

    def tg_msg__send(self, text: Any, forget_last=None, wrap: bool = None) -> None:
        if wrap:
            text = self._tg_msg__wrap(msg=text, _add_footer=True)
        self.TG_MSG__LAST_SEND = self._conn.send_message(chat_id=self.RECIPIENT_ID, text=str(text))
        if forget_last:
            self.TG_MSG__LAST_SEND__clear()

    def tg_msg__send_alert(self, text: str = None, times: int = 1) -> None:
        text = f"{self.TG_MSG__LINE__WRAP_ALERT}\n{text}"
        for i in range(times):
            self.tg_msg__send(text, forget_last=True)
            time.sleep(1)

    def tg_msg__reply(self, msg: telebot.types.Message, text: Optional[str] = None):
        if text is None:
            text = msg.text

        self._conn.reply_to(msg, text)

    def tg_msg__edit(self, text: Optional[str] = None, _msg: Optional[telebot.types.Message] = None):
        _msg = self.tg_msg__get_active(_msg)
        if text:
            text = self._tg_msg__wrap_with_footer(msg=text, _id=_msg.message_id)
        else:
            text = self._tg_msg__wrap_with_footer(msg=_msg)

        try:
            self._conn.edit_message_text(text=text, chat_id=self.RECIPIENT_ID, message_id=self.TG_MSG__LAST_SEND.message_id)
        except:
            self.TG_MSG__LAST_SEND__clear()

    def tg_msg__delete(self, msg_id: int) -> Optional[bool]:
        try:
            self._conn.delete_message(chat_id=self.RECIPIENT_ID, message_id=msg_id)
            return True
        except Exception as exx:
            print(f"{msg_id=}/{exx!r}")

    def tg_msg__delete_all(self, *args, _send_start=True):
        if not self.TG_MSG__LAST_SEND:
            return

        for num in range(self.TG_MSG__LAST_SEND.message_id, 0, -1):
            if not self.tg_msg__delete(num):
                break

        if _send_start:
            self.send_start()
            self.tg_msg__send__time()	# just to ansure it will not overwrite by new monitoring state!

    # special -----------------------------------------------
    def send_start(self):
        self.tg_msg__send(text="delete all on start", forget_last=False)
        self.tg_msg__delete_all(_send_start=False)

        msg = f"{self.TG_MSG__START__TITLE}\n" * 10
        self.tg_msg__send(text=msg)

    def tg_msg__send__time(self, *args):
        text = self._tg_msg__create__time()
        self.tg_msg__send(text)

    def tg_msg__send__main(self, *args):
        text = self._tg_msg__create__main()
        self.tg_msg__send(text)


# =====================================================================================================================
if __name__ == "__main__":
    obj = AlertTelegram()
    while True:
        time.sleep(1)


# =====================================================================================================================
