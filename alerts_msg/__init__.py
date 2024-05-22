# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorerct
#   from .main import EXACT_OBJECTS     # CORERCT


# =====================================================================================================================
from .main import AlertBase
from .smtp import SmtpAddress, SmtpServers, AlertSmtp
from .telegram import RecipientTgID, AlertTelegram


# =====================================================================================================================
# FIXME: move to main!
class AlertSelect:
    SMTP_DEF = AlertSmtp
    TELEGRAM_DEF = AlertTelegram


# =====================================================================================================================
