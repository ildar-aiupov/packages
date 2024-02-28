import json

import requests

from redis_engine import redis_engine
from requests_engine import requests_engine
from mysql_engine import mysql_engine
from rabbit_engine import rabbit_engine
from settings import settings, mylogger


def get_dollar_rate() -> int:
    """Получает курс доллара."""
    if dollar_rate := redis_engine.get("dollar_rate"):
        return float(dollar_rate)
    try:
        data = requests_engine.get(settings.cbr_api_url)
        dollar_rate = data.json()["Valute"]["USD"]["Value"]
    except requests.exceptions.ConnectionError:
        mylogger.error("Многократная ошибка при получении данных с сайта АПИ ЦБР. "
            "Видимо, ресурс недоступен. Будет использован курс доллара по умолчанию.")
        dollar_rate = settings.default_dollar_rate
    except KeyError:
        mylogger.error("Ошибка при извлечении курса доллара из данных АПИ ЦБР. "
            "Видимо, изменилась структура АПИ ЦБР. Будет использован курс доллара по умолчанию.")
        dollar_rate = settings.default_dollar_rate
    redis_engine.set(name="dollar_rate", value=dollar_rate)
    return dollar_rate


def worker(ch, method, properties, data) -> None:
    """Получает и обрабатывает сообщение из очереди сообщений RabbitMQ."""
    mylogger.info("Получено из очереди сообщений: %r" % (data,))
    data = json.loads(data.decode('utf8'))
    data["delivery_cost"] = (
        data["weight"] * 0.5 + data["content_cost"] * 0.01
    ) * get_dollar_rate()
    mysql_engine.execute("""
        INSERT INTO v1_package (uuid, name, weight, type_id, content_cost, delivery_cost, sessionid)
        VALUES (%(uuid)s, %(name)s, %(weight)s, %(type)s, %(content_cost)s, %(delivery_cost)s, %(sessionid)s);""", data)
    mysql_engine.connection.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """Запускает сервис прослушивания сообщений."""
    mylogger.info('Запуск сервиса прослушивания сообщений RabbitMQ')
    rabbit_engine.begin_consume(on_message_callback=worker)


if __name__ == "__main__":
    main()
