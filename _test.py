import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
import threading

from alerts_msg import *


# =====================================================================================================================
class Test:
    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_single(self, victim):
        assert victim("single").result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    @pytest.mark.parametrize(argnames="subj_suffix, body, _subtype", argvalues=[
        (None, "zero", None),
        ("", "plain123", "plain123"),
        ("plain", "plain", "plain"),
        ("html", "<p><font color='red'>html(red)</font></p>", "html")
    ])
    def test__send_single__parametrized(self, victim, subj_suffix, body, _subtype):
        assert victim(subj_suffix=subj_suffix, body=body, _subtype=_subtype).result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy__result_wait(self, victim):
        assert victim("multy1").result_wait() is True
        assert victim("multy2").result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy__wait_join(self, victim):
        thread1 = victim("thread1")
        thread2 = victim("thread2")

        thread1.join()
        thread2.join()

        assert thread1._result is True
        assert thread2._result is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy_thread__own(self, victim):
        threads = [
            victim("thread1"),
            victim("thread2"),
            victim("thread3"),
        ]

        victim.threads_wait_all()

        for thread in threads:
            assert thread._result is True

    def test__threads_wait_all(self):
        threads = [
            AlertTelegram("thread1"),
            AlertTelegram("thread2"),
            AlertTelegram("thread3"),
            AlertTelegram("thread4"),
        ]

        AlertTelegram.threads_wait_all()

        for thread in threads:
            assert thread._result is True


# =====================================================================================================================
