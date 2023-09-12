# private_values


## Features

1. send emails (threading!)


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

See tests for other examples.

### AlertSmtp

#### 1. add new server if not exists

```python
from alerts_msg import *

class SmtpServersMOD(SmtpServers):
    EXAMPLE_RU: SmtpAddress = SmtpAddress("smtp.EXAMPLE.ru", 123)

class AlertSmtpMOD(AlertSmtp):
    SERVER: SmtpAddress = SmtpServersMOD.EXAMPLE_RU   # or direct =SmtpAddress("smtp.EXAMPLE.ru", 123)
```

#### 2. change authorisation data (see module `private_values` for details)

```python
from alerts_msg import *

class AlertSmtpMOD(AlertSmtp):
    SMTP_USER: str = "example@mail.ru"
    SMTP_PWD: str = PrivateEnv.get("myCustomPrivateEnvName")
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
