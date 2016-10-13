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
    channel.confirm_delivery()
    if channel.basic_publish(exchange=MAIN_EXCHANGE,
                          routing_key=MAIN_QUEUE_EXCHANGE_BINDING_ROUTING_KEY,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,)):
        print('SENT the following message : ' + message + ' , to RabbitMQ')
    else:
        print('Message did not successfully reach rabbit mq, so let us make a note here and have it in our local storage')
    connection.close()
except Exception as e:
    print(e)
