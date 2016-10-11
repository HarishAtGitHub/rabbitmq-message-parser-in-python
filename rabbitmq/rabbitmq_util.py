#!/usr/bin/env python
import pika

from logger.logger_util import *


class RabbitMQ:

    logger = getLogger()

    @classmethod
    def get_connection(cls):
        connection = pika.BlockingConnection()
        cls.logger.debug('Successfully created RabbitMQ connection')
        return connection

    @classmethod
    def get_channel(cls, connection=None):
        if connection is None:
            return cls.get_connection().channel()
        try:
            channel = connection.channel()
            cls.logger.debug('Successfully created RabbitMQ channel')
            return channel
        except AttributeError as ae:
            cls.logger.error(ae)
            raise ae

    @classmethod
    def close_connection(cls, connection):
        logger = getLogger()
        try:
            connection.close()
            logger.debug('Successfully closed RabbitMQ connection')
        except AttributeError as ae:
            raise ae

    @classmethod
    def bootstrap(cls):
        # TODO: Do exhaustive exception handling
        connection = cls.get_connection()
        channel = cls.get_channel(connection)
        cls.configure_deadletter_q_and_xchange(channel)
        cls.configure_main_q_and_xchange(channel)
        connection.close()
        cls.logger.info('Successfully completed initial setup of rabbitmq')

    @classmethod
    def configure_main_q_and_xchange(cls, channel):
        channel.exchange_declare(exchange=MAIN_EXCHANGE,
                                 durable=True)
        channel.queue_declare(queue=MAIN_QUEUE,
                              durable=True,
                              arguments={
                                  'x-dead-letter-exchange': DEAD_LETTER_EXCHANGE,
                                  'x-dead-letter-routing-key': DEAD_LETTER_QUEUE_EXCHANGE_BINDING_ROUTING_KEY
                              }
                              )
        cls.logger.debug('Successfully bound main queue with dead letter exchange in RabbitMQ')

        channel.queue_bind(queue=MAIN_QUEUE,
                           exchange=MAIN_EXCHANGE,
                           routing_key=MAIN_QUEUE_EXCHANGE_BINDING_ROUTING_KEY)
        cls.logger.debug('Successfully configured main exchange and queue in RabbitMQ')


    @classmethod
    def configure_deadletter_q_and_xchange(cls, channel):
        channel.exchange_declare(exchange=DEAD_LETTER_EXCHANGE,
                                 durable=True)
        channel.queue_declare(queue=DEAD_LETTER_QUEUE,
                              durable=True)
        channel.queue_bind(queue=DEAD_LETTER_QUEUE,
                           exchange=DEAD_LETTER_EXCHANGE,
                           routing_key=DEAD_LETTER_QUEUE_EXCHANGE_BINDING_ROUTING_KEY)
        cls.logger.debug('Successfully configured dead letter exchange and queue in RabbitMQ')

