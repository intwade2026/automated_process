import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AutomationConfig:
    url: str
    username: str
    password: str


def load_config():
    load_dotenv()

    url = os.getenv("OM_URL")
    username = os.getenv("OM_USERNAME")
    password = os.getenv("OM_PASSWORD")

    missing = [
        name
        for name, value in (
            ("OM_URL", url),
            ("OM_USERNAME", username),
            ("OM_PASSWORD", password),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            "Configuration .env incomplète. Variables manquantes : "
            + ", ".join(missing)
        )

    return AutomationConfig(url=url, username=username, password=password)
