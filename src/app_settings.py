import os

from dotenv import load_dotenv
from pydantic import BaseModel


class AppSettings(BaseModel):
    director_password: str


class AppSettingsStore(BaseModel):
    app_settings: AppSettings | None


APP_SETTINGS_STORE = AppSettingsStore(app_settings=None)


def get_director_password() -> str:
    env_value = os.getenv("DIRECTOR_PASSWORD")

    if env_value is None or env_value == "":
        raise ValueError("DIRECTOR_PASSWORD is required")

    return env_value


def get_app_settings() -> AppSettings:
    global APP_SETTINGS_STORE

    if APP_SETTINGS_STORE is None:
        APP_SETTINGS_STORE = AppSettingsStore(app_settings=None)

    if APP_SETTINGS_STORE.app_settings is not None:
        return APP_SETTINGS_STORE.app_settings

    load_dotenv()

    settings = AppSettings(director_password=get_director_password())

    APP_SETTINGS_STORE.app_settings = settings

    return settings
