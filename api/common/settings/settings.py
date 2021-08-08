import ipaddress
from typing import Any, Dict, Final, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, root_validator, HttpUrl, validator

from common.settings.utils import constructUrl


IS_DEV = True

DEFAULT_ENV_FILE = ".env"
DEFAULT_ENV_ENCODING = "utf-8"

load_dotenv(DEFAULT_ENV_FILE, verbose=True)


class EnvConfig:
    case_sensitive = True
    env_file = DEFAULT_ENV_FILE
    env_file_encoding = DEFAULT_ENV_ENCODING


class HttpOnly(HttpUrl):
    allowed_schemes = {"http"}


# Server & System


class SystemSettings(BaseSettings):
    PROJECT_NAME: str = "Socials"
    ENCODING: str = "utf-8"
    UID: int

    class Config(EnvConfig):
        env_prefix = "SYSTEM_"


class DevSettings(BaseSettings):
    IS_DEV: bool = IS_DEV
    PROTO: str = "http"
    IP: ipaddress.IPv4Address
    PORT: int

    # dynamically defied based on proto,ip,port
    URL: Optional[HttpOnly]

    class Config:
        env_prefix: str = "DEV_"

    @root_validator
    def _set_fields(
        cls: "DevSettings",
        values: Dict[Any, Any],
    ) -> Dict[Any, Any]:

        values["URL"] = constructUrl(
            values["IP"],
            values["PORT"],
            values["PROTO"],
        )
        return values


class ServerSettings(BaseSettings):
    SKEY: str

    class Config(EnvConfig):
        env_prefix: str = "SERVER_"


class LoggingSettings(BaseSettings):
    LOGGER_NAME = "gunicorn.error"
    DEV_LOGGER_NAME = "uvicorn.access"


# Services
# (internal abbreviation: SVC)


class ServiceSettings(BaseSettings):

    # only required if ServiceSettings.IS_EXT
    IP: Optional[ipaddress.IPv4Address]
    PORT: Optional[int]
    URL: Optional[str]

    # if service is external
    IS_EXT: bool = False

    # custom service fields allowed for subclass
    ...

    class Config(EnvConfig):
        """subclass parent and override Config(EnvConfig) with env_prefix"""


class ServiceDispatchSettings(ServiceSettings):
    AK_BROKER_IP: ipaddress.IPv4Address
    AK_BROKER_PORT: int
    AK_BROKER_URL: Optional[str]

    class Config(EnvConfig):
        env_prefix = "SVC_DISPATCH_"

    @root_validator
    def _set_fields(
        cls: "ServiceDispatchSettings", values: Dict[Any, Any]
    ) -> Dict[Any, Any]:

        values["AK_BROKER_URL"] = constructUrl(
            values["AK_BROKER_IP"],
            values["AK_BROKER_PORT"],
            str(),
        )
        return values


# Security


class AuthSettings(BaseSettings):
    HMAC_ALGO: str = "SHA256"

    class Config(EnvConfig):
        env_prefix = "AUTH_"


class TokenSettings(BaseSettings):
    TYPE: str = "bearer"
    ENCODING: str = "utf-8"
    ALGO: str

    EXPIRE: int
    REFRESH_EXPIRE: int

    class Config(EnvConfig):
        env_prefix = "TOKEN_"


# Cache


class CacheServerSettings(BaseSettings):
    DB: int
    AUTH: Optional[str]

    IP: ipaddress.IPv4Address
    PORT: int

    class Config:
        """subclass parent and override Config(EnvConfig) with env_prefix"""

    @validator("AUTH")
    def setNone(cls, v) -> Optional[str]:
        if isinstance(v, str):
            if not v.isdigit() and v:
                return v

        return None


class UserCache(CacheServerSettings):
    """Caching for user-related things"""

    class Config(EnvConfig):
        env_prefix = "USER_CACHE_"


class CacheServer(CacheServerSettings):
    class Config(EnvConfig):
        env_prefix = "CACHE_SERVER_"


# Setting instances
DEV_SETTINGS: Final[DevSettings] = DevSettings()
LOGGER_SETTINGS: Final[LoggingSettings] = LoggingSettings()


TOKEN_SETTINGS: Final[TokenSettings] = TokenSettings()
AUTH_SETTINGS: Final[AuthSettings] = AuthSettings()
SERVER_SETTINGS: Final[ServerSettings] = ServerSettings()
SYSTEM_SETTINGS: Final[SystemSettings] = SystemSettings()

USER_CACHE_SETTINGS: Final[UserCache] = UserCache()
CACHE_SERVER_SETTINGS: Final[CacheServer] = CacheServer()

SVC_DISPATCH_SETTINGS = ServiceDispatchSettings()
