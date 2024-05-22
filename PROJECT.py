from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "alerts_msg"
    KEYWORDS: List[str] = [
        "alerts", "notifications",
        "email alerts", "smtp", "mail", "email",
        "telegram alerts", "telegram",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        "Topic :: Communications",
        "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "All abilities (mail/telegram) to send alert msgs (threading)"
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
    VERSION: Tuple[int, int, int] = (0, 2, 2)
    TODO: List[str] = [
        "test multyStart by one object (QThread)"
    ]
    FIXME: List[str] = [
        "NEED SOLVE ABILITY to work without PV.FILE!!! as just a http client"
    ]
    NEWS: List[str] = [
        "[__INIT__.py] fix import",
        "apply last pypi template",
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
