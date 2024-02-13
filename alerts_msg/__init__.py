from .main import *
from .smtp import *
from .telegram import *


# =====================================================================================================================
# FIXME: move to main!
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
