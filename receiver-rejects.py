#!/usr/bin/env python
import pika
import init_rabbitmq

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
queue_name='poc-q-rejects'
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    success = False
    if success:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        pass

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

print('Subscribed to ' + queue_name)
channel.start_consuming()
