from celery import Celery

from infrastructure.environment import env

celery_app = Celery('worker', broker=env.redis.uri, backend=env.redis.uri)

from application.controllers import quotes
