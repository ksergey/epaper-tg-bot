__all__ = ('config')

from configparser import ConfigParser
from dataclasses import dataclass, field
from typing import List, Dict

from app.args_reader import args

@dataclass
class TelegramConfig:
    token: str = field(repr=False)
    chat_id: int = field(repr=False)

@dataclass
class KadinskyConfig:
    key: str = field(repr=False)
    secret: int = field(repr=False)

@dataclass
class Config:
    telegram: TelegramConfig
    kadinsky: KadinskyConfig

def load_config() -> Config:
    parser = ConfigParser()
    parser.read(args.config)

    config=Config(
        telegram=TelegramConfig(
            token=parser.get('telegram', 'token'),
            chat_id=int(parser.get('telegram', 'chat_id'))
        ),
        kadinsky=KadinskyConfig(
            key=parser.get('kadinsky', 'key'),
            secret=parser.get('kadinsky', 'secret')
        )
    )

    return config

config = load_config()
