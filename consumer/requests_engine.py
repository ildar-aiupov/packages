import requests
import backoff

from settings import mylogger


class RequestsEngine:
    """Класс-фасад для работы с requests."""

    def __init__(self) -> None:
        """Создает сессию requests."""
        self.session = requests.Session()

    def _backoff_message(detail) -> None:
        mylogger.error("Временная ошибка при получении данных с сайта Центробанка. Повторная попытка...")

    @backoff.on_exception(
        wait_gen=backoff.constant,
        jitter=None,
        interval=1,
        exception=Exception,
        on_backoff=_backoff_message,
        max_tries=5
    )
    def get(self, url):
        """Получает данные по запросу."""
        return self.session.get(url)
        

requests_engine = RequestsEngine()
