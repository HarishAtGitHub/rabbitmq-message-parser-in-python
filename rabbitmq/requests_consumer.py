from rabbitmq.rabbitmq_util import RabbitMQ
from config.configuration import *
from rabbitmq.consumer import Consumer
from logger.logger_util import *

class RequestsConsumer(Consumer):

    def __init__(self, id):
        logger = getLogger()
        self.connection = RabbitMQ.get_connection()
        self.channel = RabbitMQ.get_channel(self.connection)
        self.id = id
        print('Successfully initialized Requests Consumer : ' + str(self.id))
        logger.info('Successfully initialized Requests Consumer : ' + str(self.id))

    def start(self):
        logger = getLogger()
        self.channel.basic_consume(self.__class__.callback,
                                   queue=MAIN_QUEUE,
                                   no_ack=False)
        print('Requests Consumer : ' + str(self.id) +
              ' Successfully subscribed to queue : ' + MAIN_QUEUE)
        logger.info('Requests Consumer : ' + str(self.id) +
                    ' Successfully subscribed to queue : ' + MAIN_QUEUE)
        self.channel.start_consuming()

    def stop(self):
        RabbitMQ.close_connection(self.connection)

    @staticmethod
    def callback(channel, method, properties, body):
        logger = getLogger()
        logger.debug(" Message received from requests queue : %r" % body)
        string = body.decode('ascii')
        if(string.startswith('s')):
            success = True
        else:
            success = False
        if success:
            logger.debug(" Message processed successfully by 'requests consumer' so sending an ack to rabbitmq")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logger.debug(" Message from requests queue faced failure while processing "
                        " so will post it to rejects queue for reprocessing ")
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            pass