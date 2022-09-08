import os
from collections import namedtuple
from pathlib import Path
from types import SimpleNamespace
from typing import Union

from alembic.config import Config
from configargparse import Namespace
from pydantic import BaseModel

PROJECT_PATH = Path(__file__).parent.parent.resolve()


def make_alembic_config(
    cmd_opts: Union[Namespace, SimpleNamespace], base_path: Path = PROJECT_PATH
) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    path_to_folder = cmd_opts.config
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(
            base_path, cmd_opts.config + 'alembic.ini'
        )

    config = Config(
        file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts  # type: ignore
    )

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if alembic_location is None:
        raise ValueError('No script_location in config file')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location',
            os.path.join(base_path, path_to_folder + alembic_location),
        )
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


class UserData(BaseModel):
    username: str
    password: str


DPSClass = namedtuple('DPSClass', 'data proxy schema')
