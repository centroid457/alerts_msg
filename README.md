# alerts_msg


## Features
1. send alert msgs
    * emails
    * telegram
2. threading


## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install alerts_msg
```

## Import
```python
from alerts_msg import *
```


## GUIDE
See tests and source for other examples.

### AlertSmtp

#### 1. add new server if not exists

```python
from alerts_msg import *


class SmtpServersMOD(SmtpServers):
    EXAMPLE_RU: SmtpAddress = SmtpAddress("smtp.EXAMPLE.ru", 123)


class AlertSmtpMOD(AlertSmtp):
    SERVER_SMTP: SmtpAddress = SmtpServersMOD.EXAMPLE_RU  # or direct =SmtpAddress("smtp.EXAMPLE.ru", 123)
```

#### 2. change authorisation data (see `private_values` for details)
```python
from alerts_msg import *


class AlertSmtpMOD(AlertSmtp):
    AUTH: PrivateAuto = PrivateAuto(_section="AUTH_EMAIL_MOD")
```

#### 3. change other settings (see source for other not mentioned)
```python
from alerts_msg import *

class AlertSmtpMOD(AlertSmtp):
    TIMEOUT_RECONNECT: int = 60
    RECONNECT_LIMIT: int = 10

    TIMEOUT_RATELIMIT: int = 600

    RECIPIENT: str = "my_address_2@mail.ru"
```

#### 4. send
* if no mods
```python
from alerts_msg import *

AlertSmtp(subj_suffix="Hello", body="World!")
```

* with mods
```python
from alerts_msg import *

class AlertSmtpMOD(AlertSmtp):
    pass    # changed

AlertSmtpMOD(subj_suffix="Hello", body="World!")
```

#### 5. using in class with saving alert object
```python
from alerts_msg import *

class AlertSmtpMOD(AlertSmtp):
    pass    # changed

class MyMonitor:
    ALERT = AlertSmtpMOD

monitor = MyMonitor()
monitor.ALERT("Hello")
```

### AlertTelegram
All idea is similar to AlertSmtp.

* add auth data  
add pv.json or do smth else (for details see private_values.PrivateJsonTgBotAddress)
```json
{
    "TG_ID": {"MyTgID": 1234567890},
    "TGBOT_DEF": {
        "LINK_ID": "@my_bot_20230916",
        "NAME": "my_bot",
        "TOKEN": "9876543210xxxxxxxxxxxxxxxxxxxxxxxxx"
    }
}
```

```python
from alerts_msg import *

class MyMonitor:
    ALERT = AlertTelegram

monitor = MyMonitor()
monitor.ALERT("Hello")
```
