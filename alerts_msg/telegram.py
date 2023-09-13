import time
from typing import *

import telebot
import threading
import typing as tp
import random

from private_values import *


# =====================================================================================================================
# TODO: msgs = mark all as readed!


# =====================================================================================================================
class TgBotAddress(NamedTuple):
    TOKEN: str
    NAME: Optional[str] = None  # MyBot - PublicName
    LINK: Optional[str] = None  # @mybot20230913 - uniqName


class TgBotAddresses:
    BOT1: TgBotAddress = TgBotAddress(PrivateIni().get("BOT1"), "BOT1")
    BOT2: TgBotAddress = TgBotAddress(PrivateIni().get("BOT2"), "BOT2")
    BOT3: TgBotAddress = TgBotAddress(PrivateIni().get("BOT3"), "BOT3")


# =====================================================================================================================
class TelegramBot:
    _TG_PYTHON_ID: int = None

    BOT_NAME: str = "BOT1"
    TG_ABONENT_ID: int = 906635346

    TG_MSG__START__TITLE = "============= START WORKING ============="
    TG_MSG__LINE__WRAP_MAIN = "=" * 40
    TG_MSG__LINE__SEPARATE = "-" * 40*2
    TG_MSG__LINE__WRAP_ALERT = f"!" * 30 + f" [[[[ALERT]]]] " + f"!" * 30

    # INIT ============================================================================================================
    def __init__(self):
        super().__init__()
        # INITS --------------------------------------------
        self._TG_PYTHON_ID = random.randrange(10000)
        self.TG_MSG__LAST_SEND: tp.Optional[telebot.types.Message] = None

        self.TG_CMDS_FUNCS: tp.Dict[str, tp.Callable] = {}
        self.TG_CMDS_FUNCS__update()

        # WORK --------------------------------------------
        self._TG_BOT = telebot.TeleBot(token=self._TG_BOT_NAMES_TOKENS[self.BOT_NAME])
        self.tg_msg__send__start()
        self.tg_msg__send(text=self.BOT_NAME, forget_last=False, wrap=True)
        self.tg_handlers_init()

        self.TG_START()

    def __del__(self):
        self.tg_msg__send(text="========== STOP working ==========")

    # init HANDLERS ---------------------------------------------------------------------------------------------------
    def TG_CMDS_FUNCS__update(self, cmds: tp.Optional[tp.Dict[str, tp.Callable]] = None) -> None:
        if cmds is None:
            cmds = {
                # dont use slash sign here! is is incorrect!
                "MAIN_MSG": self.tg_msg__send__main,
                "DATETIME": self.tg_msg__send__time,
            }
            self.TG_CMDS_FUNCS.update(cmds)

    def tg_handlers_init(self):
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
        for name, func in self.TG_CMDS_FUNCS.items():
            self._TG_BOT.register_message_handler(func, commands=[name])

    def _tg_handlers_init__2_any_comment(self) -> None:
        handler_dict = dict(
            function=lambda msg: self.tg_msg__reply(msg, text=None),
            filters=dict(
                # commands=["start"],
            )
        )
        self._TG_BOT.add_message_handler(handler_dict)

    def TG_START(self):
        thread = threading.Thread(target=self._TG_BOT.infinity_polling, daemon=True)
        thread.start()

    # MSG PARTS ========================================================================================================
    def tg_msg__get_active(self, _msg: tp.Optional[telebot.types.Message] = None):
        _msg = _msg or self.TG_MSG__LAST_SEND
        return _msg

    def TG_MSG__LAST_SEND__clear(self) -> None:
        self.TG_MSG__LAST_SEND = None

    # TEXT WORK -------------------------------------------
    def _tg_msg__wrap(self, msg: tp.Union[str, telebot.types.Message], _id: int = None, wrap_line: str = None, _add_footer: bool = None) -> str:
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
            result += f"[{_id}/bot_{self._TG_PYTHON_ID}]\n"

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
        for cmd in self.TG_CMDS_FUNCS:
            result += f"/{cmd}\n"
        return result

    @staticmethod
    def _tg_msg__create__time() -> str:
        return str(time.strftime("%Y.%m.%d__%H:%M:%S"))

    def _tg_msg__create__separated_from_list(self, text_list: tp.List[str]) -> str:
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

    def tg_msg__send(self, text: tp.Any, forget_last=None, wrap: bool = None) -> None:
        if wrap:
            text = self._tg_msg__wrap(msg=text, _add_footer=True)
        self.TG_MSG__LAST_SEND = self._TG_BOT.send_message(chat_id=self.TG_ABONENT_ID, text=str(text))
        if forget_last:
            self.TG_MSG__LAST_SEND__clear()

    def tg_msg__send_alert(self, text: str = None, times: int = 1) -> None:
        text = f"{self.TG_MSG__LINE__WRAP_ALERT}\n{text}"
        for i in range(times):
            self.tg_msg__send(text, forget_last=True)
            time.sleep(1)

    def tg_msg__reply(self, msg: telebot.types.Message, text: tp.Optional[str] = None):
        if text is None:
            text = msg.text

        self._TG_BOT.reply_to(msg, text)

    def tg_msg__edit(self, text: tp.Optional[str] = None, _msg: tp.Optional[telebot.types.Message] = None):
        _msg = self.tg_msg__get_active(_msg)
        if text:
            text = self._tg_msg__wrap_with_footer(msg=text, _id=_msg.message_id)
        else:
            text = self._tg_msg__wrap_with_footer(msg=_msg)

        try:
            self._TG_BOT.edit_message_text(text=text, chat_id=self.TG_ABONENT_ID, message_id=self.TG_MSG__LAST_SEND.message_id)
        except:
            self.TG_MSG__LAST_SEND__clear()

    def tg_msg__delete(self, msg_id: int) -> tp.Optional[bool]:
        try:
            self._TG_BOT.delete_message(chat_id=self.TG_ABONENT_ID, message_id=msg_id)
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
            self.tg_msg__send__start()
            self.tg_msg__send__time()	# just to ansure it will not overwrite by new monitoring state!

    # special -----------------------------------------------
    def tg_msg__send__start(self):
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
    obj = TelegramBot()
    while True:
        time.sleep(1)


# =====================================================================================================================
