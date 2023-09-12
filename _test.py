import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
import threading

from alerts_msg import *


# =====================================================================================================================
@pytest.mark.parametrize(argnames="subj_suffix, body, _subtype", argvalues=[
    (None, "zero", None),
    ("", "plain123", "plain123"),
    ("plain", "plain", "plain"),
    ("html", "<p><font color='red'>html(red)</font></p>", "html")
])
def test__send_single(subj_suffix, body, _subtype):
    assert AlertSmtp(subj_suffix=subj_suffix, body=body, _subtype=_subtype).result is True


def test__send_multy():
    assert AlertSmtp("multy1").result is True
    assert AlertSmtp("multy2").result is True


def test__send_multy_thread():
    obj1 = AlertSmtp(subj_suffix="obj1")
    obj2 = AlertSmtp(subj_suffix="obj2")
    obj3 = AlertSmtp(subj_suffix="obj3")

    thread1 = threading.Thread(target=obj1._send, kwargs={"body": "thread1"})
    thread2 = threading.Thread(target=obj2._send, kwargs={"body": "thread2"})
    thread3 = threading.Thread(target=obj3._send, kwargs={"body": "thread3"})

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    assert obj1.result is True
    assert obj2.result is True
    assert obj3.result is True

# =====================================================================================================================
