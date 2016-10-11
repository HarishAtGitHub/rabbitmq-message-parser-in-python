from rabbitmq.rabbitmq_util import RabbitMQ
from config.configuration import *
from rabbitmq.consumer import Consumer
from logger.logger_util import *


class RejectsConsumer(Consumer):

    def __init__(self,id):
        logger = getLogger()
        self.connection = RabbitMQ.get_connection()
        self.channel = RabbitMQ.get_channel(self.connection)
        self.id = id
        print('Successfully initialized Rejects Consumer :' + str(self.id))
        logger.info('Successfully initialized Rejects Consumer ' + str(self.id))

    def start(self):
        logger = getLogger()
        self.channel.basic_consume(self.__class__.callback,
                                   queue=DEAD_LETTER_QUEUE,
                                   no_ack=False)
        print('Rejects Consumer : ' + str(self.id) +
              ' Successfully subscribed to queue : ' + DEAD_LETTER_QUEUE)
        logger.info('Rejects Consumer : ' + str(self.id) +
                    ' Successfully subscribed to queue : ' + DEAD_LETTER_QUEUE)
        self.channel.start_consuming()


    def stop(self):
        RabbitMQ.close_connection(self.connection)

    @staticmethod
    def callback(channel, method, properties, body):
        logger = getLogger()
        logger.debug(" Message received from rejects queue : %r" % body)
        string = body.decode('ascii')
        if (string.startswith('fp')):
            success = True
        else:
            success = False
        if success:
            logger.debug(" Message processed successfully by 'rejects consumer' so sending an ack to rabbitmq")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logger.debug(" Message processing failed  even in rejects consumer "
                         " so will log it in slack and then delete it from queue by setting requeue : False")
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
