from celery import Celery

def make_celery(app_name=__name__):
    sqlite_url = 'db+sqlite:///db.sqlite3'
    rabbitrqm = 'amqps://pzsezhbe:QFxB_1aHBmHeR5jdAN4Yq6LOLyaaKqlM@bonobo.rmq.cloudamqp.com/pzsezhbe'
    return Celery(app_name, backend=sqlite_url, broker=rabbitrqm, )

celery = make_celery()
