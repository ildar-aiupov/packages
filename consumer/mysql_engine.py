import pymysql
import backoff

from settings import settings, mylogger


class MysqlEngine:
    """Класс-фасад работы с MySQL."""

    def __init__(self) -> None:
        """Вызывает установку соединения с MySQL."""
        self.set_connection()

    def _backoff_connect_failure_message(detail):
        mylogger.error("Ошибка при подключении к MySQL. Повторная попытка...")

    @backoff.on_exception(
        wait_gen=backoff.constant,
        jitter=None,
        interval=1,
        exception=Exception,
        on_backoff=_backoff_connect_failure_message,
    )
    def set_connection(self):
        """Устанавливает соединение с MySQL, получает курсор."""
        self.connection = pymysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database
        )
        self.cursor = self.connection.cursor()
        mylogger.info("Подключение к MySQL установлено")

    def execute(self, query: str, args: object = None):
        """Выполняет запрос к базе данных MySQL."""
        while True:
            try:
                self.cursor.execute(query=query, args=args)
            except:
                self.set_connection()
            else:
                mylogger.info("SQL-запрос к MySQL выполнен успешно.")
                break


mysql_engine = MysqlEngine()
