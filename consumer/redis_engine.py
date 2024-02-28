from typing import Any

from redis import Redis

from settings import settings, mylogger


class RedisEngine:
    """Класс-фасад для работы с Redis."""

    def __init__(self) -> None:
        """Вызывает установку соединения с Redis."""
        self.set_connection()
    
    def set_connection(self):
        """Устанавливает соединение с Redis."""
        self.connection = Redis(
            host=settings.redis_host, 
            port=settings.redis_port, 
            db=0, 
            decode_responses=True
        )

    def get(self, key) -> Any | None:
        """Получает значение из кэша."""
        try:
            return self.connection.get(key)
        except:
            mylogger.error("Проблема с Редисом при получении значения. Кэш не работает.")

    def set(self, name, value, ex=None) -> None:
        """Задает значение в кэш."""
        if not ex:
            ex = settings.redis_cache_time
        try:
            self.connection.set(name=name, value=value, ex=ex)
        except:
            mylogger.error("Проблема с Редисом при задании значения. Кэш не работает.")


redis_engine = RedisEngine()
