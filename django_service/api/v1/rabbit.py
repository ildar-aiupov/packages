import json

from django.conf import settings

import pika

from core.logger import mylogger


class RabbitEngine:
    """Класс-фасад работы с RabbitMQ."""

    def __init__(self) -> None:
        """Задает начальные значения, вызывает установку соединения с RabbitMQ."""
        self.credentials = pika.PlainCredentials(
            username=settings.RABBIT["USERNAME"], 
            password=settings.RABBIT["PASSWORD"],
        )
        self.parameters = pika.ConnectionParameters(
            host=settings.RABBIT["HOST"],
            port=settings.RABBIT["PORT"],
            credentials=self.credentials,
        )
        self.set_connection()

    def set_connection(self):
        """Устанавливает соединение с RabbitMQ."""
        try:
            self.connection = pika.BlockingConnection(parameters=self.parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=settings.RABBIT["EXCHANGE"], exchange_type="direct", durable=True)
            self.channel.queue_declare(queue=settings.RABBIT["QUEUE"], durable=True)
            self.channel.queue_bind(
                exchange=settings.RABBIT["EXCHANGE"],
                queue=settings.RABBIT["QUEUE"],
                routing_key=settings.RABBIT["ROUTING_KEY"]
            )
        except:
            mylogger.error("Ошибка подключения к Rabbit")
            self.connected = False
        else:
            mylogger.info("Подключение к Rabbit установлено")
            self.connected = True

    def send(self, data) -> None:
        """Отправляет сообщение в очередь RabbitMQ."""
        if not self.connected or self.connection.is_closed:
            self.set_connection()
        try:
            self.channel.basic_publish(
                exchange=settings.RABBIT["EXCHANGE"],
                routing_key=settings.RABBIT["ROUTING_KEY"],
                body=json.dumps(data),
            )
        except:
            mylogger.error("Ошибка отправки сообщения в очередь Rabbit")
            return False
        else:
            mylogger.info("Успешно отправлено сообщение в очередь Rabbit")
            return True


rabbit_engine = RabbitEngine()
