from .main import *

import time
from typing import *
import requests


# =====================================================================================================================
pass


# =====================================================================================================================
class HttpAddress(NamedTuple):
    HOST: str
    PORT: int = 80
    ROUTE: str = ''     # without slashes!

    def url_create(self, route: Optional[str] = None) -> str:
        url = f"http://{self.HOST}:{self.PORT}/{self.ROUTE}"
        return url


class HttpServers:
    """well known servers addresses.

    Here we must collect servers like MilRu/GmailCom, and not to create it in any new project.
    """
    LIDIA: HttpAddress = HttpAddress("http://192.168.74.20", 8080, "results")


# =====================================================================================================================
class AlertHttp(AlertBase):
    """HTTP realisation for sending msg (POSTs).
    """
    # SETTINGS ------------------------------------
    SERVER_HTTP: HttpAddress = HttpServers.LIDIA

    # AUX -----------------------------------------
    _conn: 'session' = True

    def _send_unsafe(self) -> Union[bool, NoReturn]:
        with requests.Session() as session:
            session.post(url=self.SERVER_HTTP.url_create(), json=self._msg_compose(), timeout=self.TIMEOUT_SEND)
        return True

    def _msg_compose(self) -> Dict:
        msg = self.body
        return msg


# =====================================================================================================================
