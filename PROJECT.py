from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 2)

    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "alerts_msg"
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")
    KEYWORDS: List[str] = [
        "alerts", "notifications",
        "email alerts", "smtp", "mail", "email",
        "telegram alerts", "telegram",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        "Topic :: Communications",
        "Topic :: Communications :: Email",
    ]

    # GIT --------------------------------------------------
    DESCRIPTION_SHORT: str = "All abilities (mail/telegram) to send alert msgs (threading)",

    # README -----------------------------------------------
    pass

    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_LONG: str = """
designed for ...
    """
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["send alert msgs", "emails", "telegram", ],
        "threading",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 2, 1)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "..."
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "apply new pypi template"
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
