from multiprocessing import Process
from multiprocessing import Pool

from config.configuration import *
from logger.logger_util import *
from rabbitmq.rabbitmq_util import RabbitMQ
from rabbitmq.requests_consumer import RequestsConsumer
from rabbitmq.rejects_consumer import RejectsConsumer

def main():
    logger = getLogger()
    RabbitMQ.bootstrap()
    logger.info('Successfully bootstrapped RabbitMQ')
    logger.info('Application Started Successfully !')

    pool = Pool(POOL_SIZE)
    result = ''
    for i in range(1, NO_OF_REQUESTS_CONSUMERS+1):
        result = pool.apply_async(requests_consumer,[i])


    for i in range(1, NO_OF_REJECTS_CONSUMERS+1):
        result = pool.apply_async(rejects_consumer,[i])

    print('Application Started Successfully !')
    result.get()


def requests_consumer(id):
    p = RequestsConsumer(id)
    return p.start()

def rejects_consumer(id):
    p = RejectsConsumer(id)
    return p.start()

if __name__ == "__main__":
    try:
        logger = create_logger(LOGGER_NAME)
        main()
    except Exception as e:
        logger.error(e)
        print("Oops ! Something went wrong. Please check the log file :  %s" % (LOG_FILE))
        print('If you have insufficient information in the log, please change the LOG_LEVEL'
              ' in configuration.py to DEBUG and rerun.')
