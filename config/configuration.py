#  RABBITMQ CONFIGURATION
#=============================================================================
COMMON_PREFIX='msgparser'
MAIN_EXCHANGE=COMMON_PREFIX + '-requests-xchange'
MAIN_QUEUE=COMMON_PREFIX + '-requests-q'
MAIN_QUEUE_EXCHANGE_BINDING_ROUTING_KEY=COMMON_PREFIX + '-requests'
DEAD_LETTER_EXCHANGE=COMMON_PREFIX + '-rejects-xchange'
DEAD_LETTER_QUEUE=COMMON_PREFIX + '-rejects-q'
DEAD_LETTER_QUEUE_EXCHANGE_BINDING_ROUTING_KEY=COMMON_PREFIX + '-rejects'



# LOG CONFIGURATION
# ============================================================================
LOGGER_NAME = COMMON_PREFIX + 'log'
LOG_FILE = 'logs/' + COMMON_PREFIX + '.log'
# choose one among  'CRITICAL','ERROR','WARNING','INFO','DEBUG' for LOG_LEVEL
LOG_LEVEL='DEBUG'

# JOB CONFIGURATION
# ============================================================================
NO_OF_REQUESTS_CONSUMERS=3
NO_OF_REJECTS_CONSUMERS=2
POOL_SIZE=5
