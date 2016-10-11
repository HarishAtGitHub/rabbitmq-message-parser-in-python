#!/usr/bin/env python
from rabbitmq.rabbitmq_util import RabbitMQ
from config.configuration import *
from rabbitmq.consumer import Consumer
from logger.logger_util import *
import pika
import sys

message = sys.argv[1]
try:
    connection = RabbitMQ.get_connection()
    channel = RabbitMQ.get_channel(connection)
    channel.basic_publish(exchange=MAIN_EXCHANGE,
                          routing_key=MAIN_QUEUE_EXCHANGE_BINDING_ROUTING_KEY,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # TODO: make message persistent :tells RabbitMQ to save the message to disk(
                              # being extra cautious - see if it has performance concerns)
                          ))
    print('SENT the following message ' + message)
    connection.close()
except Exception as e:
    print(e)
