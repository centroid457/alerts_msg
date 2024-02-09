import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *

from alerts_msg import *


# =====================================================================================================================
class Test:
    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_single(self, victim):
        assert victim("single").result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy_thread(self, victim):
        threads = [
            victim("thread1"),
            victim("thread2"),
            victim("thread3"),
        ]

        victim.threads_wait_all()

        for thread in threads:
            assert thread._result is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    @pytest.mark.parametrize(argnames="_subj_name, body, _subtype", argvalues=[
        (None, "zero", None),
        ("", "plain123", "plain123"),
        ("plain", "plain", "plain"),
        ("html", "<p><font color='red'>html(red)</font></p>", "html")
    ])
    def test__send_single__parametrized(self, victim, _subj_name, body, _subtype):
        assert victim(_subj_name=_subj_name, body=body, _subtype=_subtype).result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy__result_wait(self, victim):
        assert victim("multy1").result_wait() is True
        assert victim("multy2").result_wait() is True

    @pytest.mark.parametrize(argnames="victim", argvalues=[AlertSmtp, AlertTelegram])
    def test__send_multy__wait_join(self, victim):
        thread1 = victim("thread1")
        thread2 = victim("thread2")

        thread1.wait()
        thread2.wait()

        assert thread1._result is True
        assert thread2._result is True


# =====================================================================================================================
class Test_HTTP:
    def test__send_single(self, victim):
        assert victim("single").result_wait() is True


# =====================================================================================================================
