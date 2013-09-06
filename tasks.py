import eddy
from celery import Celery

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

celery = Celery('perf', backend='amqp', broker=BROKER_URL)

@celery.task
def perftest(appname):
    name = eddy.loadApp(appname)
    results = eddy.testApp(name)
    return results
