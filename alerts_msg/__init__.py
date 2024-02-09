from .main import *
from .smtp import *
from .telegram import *
from .http import *


# =====================================================================================================================
# FIXME: move to main!
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
