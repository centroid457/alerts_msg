import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
import threading

from alerts_msg import *


# =====================================================================================================================
def test__send_single():
    assert AlertSmtp("single")._result_wait is True

@pytest.mark.parametrize(argnames="subj_suffix, body, _subtype", argvalues=[
    (None, "zero", None),
    ("", "plain123", "plain123"),
    ("plain", "plain", "plain"),
    ("html", "<p><font color='red'>html(red)</font></p>", "html")
])
def test__send_single__parametrized(subj_suffix, body, _subtype):
    assert AlertSmtp(subj_suffix=subj_suffix, body=body, _subtype=_subtype)._result_wait is True


def test__send_multy__result_wait():
    assert AlertSmtp("multy1")._result_wait is True
    assert AlertSmtp("multy2")._result_wait is True

def test__send_multy__wait_join():
    thread1 = AlertSmtp("thread1")
    thread2 = AlertSmtp("thread2")

    thread1.join()
    thread2.join()

    assert thread1._result is True
    assert thread2._result is True

def test__send_multy_thread__own():
    threads = [
        AlertSmtp("thread1"),
        AlertSmtp("thread2"),
        AlertSmtp("thread3"),
    ]

    for thread in threads:
        # need wait all!
        thread.join()

    for thread in threads:
        assert thread._result is True


# =====================================================================================================================
