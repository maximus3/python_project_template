from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    SOME_ENV: str = Field(None, env='SOME_ENV')

    class Config:
        env_file: Path = BASE_DIR / '.env'


cfg = ConfigDataClass()
