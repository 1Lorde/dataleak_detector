import logging

from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler

# elk_host = '212.111.196.117'
elk_host = '10.33.33.7'
elk_port = 5000

# management_host = '212.111.196.117'
management_host = 'localhost'
management_port = 5001

local_db_filename = 'hashes.txt'
update_timeout = 5

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

logstash_handler = AsynchronousLogstashHandler(elk_host, elk_port, database_path='data/logstash.db')
logstash_formatter = LogstashFormatter(
    message_type='csd33-logstash',
    extra_prefix='csd33',
    tags='csd33_agent')

logstash_handler.setFormatter(logstash_formatter)
logger.addHandler(logstash_handler)
