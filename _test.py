import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *

from alerts_msg import *


# =====================================================================================================================
for subj, body, _subtype in [
    ("[ALERT]plain123", "plain123", "plain123"),
    ("[ALERT]plain", "plain", "plain"),
    ("[ALERT]html", "<p><font color='red'>html(red)</font></p>", "html")
]:
    AlertSmtp.send(subj, body, _subtype)


@pytest.mark.parametrize(argnames="subj, body, _subtype", argvalues=[
    ("[ALERT]None", "None", None),
    ("[ALERT]plain123", "plain123", "plain123"),
    ("[ALERT]plain", "plain", "plain"),
    ("[ALERT]html", "<p><font color='red'>html(red)</font></p>", "html")
])
def test__send(subj, body, _subtype):
    assert AlertSmtp.send(subj, body, _subtype) is True


# =====================================================================================================================
