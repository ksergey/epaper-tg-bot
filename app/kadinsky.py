import asyncio
import aiohttp
import ujson
import logging

logger = logging.getLogger(__name__)

class Kadinsky:
    def __init__(self, key: str, secret: str) -> None:
        self._key = key
        self._secret = secret
