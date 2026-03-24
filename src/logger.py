import logging
import logging.config
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path

logs_dir = Path('./logs')
logs_dir.mkdir(exist_ok=True)

log_file = f'./{logs_dir}/app_log_{datetime.now().strftime("%Y-%m-%d")}.log'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file_handler': {
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': str(log_file),
            'when': 'midnight',
            'backupCount': 30,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file_handler'],
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)