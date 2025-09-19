QUOTES_SITE_URL: str = 'https://quotes.toscrape.com/'

QUOTES_PARSING_REQUEST_LIMIT: str = '1/10minutes'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '[%(asctime)-15s | %(name)s | %(levelname)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
}