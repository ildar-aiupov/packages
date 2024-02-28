import pika
import backoff

from settings import settings, mylogger


class RabbitEngine:
    """Класс-фасад работы с RabbitMQ."""

    def __init__(self) -> None:
        """Задает начальные значения, вызывает установку соединения с RabbitMQ."""
        self.credentials = pika.PlainCredentials(
            username=settings.rabbit_username, 
            password=settings.rabbit_password
        )
        self.parameters = pika.ConnectionParameters(
            host=settings.rabbit_hostname, 
            port=settings.rabbit_port, 
            credentials=self.credentials
        )
        self.set_connection()
        
    def _backoff_connect_failure_message(detail):
        mylogger.error("Ошибка при подключении к RabbitMQ. Повторная попытка...")

    @backoff.on_exception(
        wait_gen=backoff.constant,
        jitter=None,
        interval=1,
        exception=pika.exceptions.AMQPConnectionError,
        on_backoff=_backoff_connect_failure_message,
    )
    def set_connection(self):
        """Устанавливает соединение, канал и очередь RabbitMQ."""
        self.connection = pika.BlockingConnection(parameters=self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.rabbit_queue, durable=True)
        mylogger.info("Подключение к Rabbit установлено")

    def begin_consume(self, on_message_callback):
        """Запускает прослушивание очереди сообщений RabbitMQ."""
        while True:
            try:
                self.channel.basic_consume(
                    on_message_callback=on_message_callback, 
                    queue=settings.rabbit_queue
                )
                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                self.set_connection()
            else:
                mylogger.info("Воркер готов к приему сообщений")
                break


rabbit_engine = RabbitEngine()
