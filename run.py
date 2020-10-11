from app import factory
import app

app = factory.create_app(celery=app.celery)

# if __name__ == "__main__":
#     app = factory.create_app(celery=app.celery)
#     app.run()

#celery worker celery_worker.celery --loglevel=info --pool=solo
#celery -A celery_worker.celery worker --loglevel=INFO --pool=solo

#celery -A celery_worker.celery worker -i info
#celery -A celery_worker.celery flower --address=127.0.0.1 --port=5555
#pip install celery=4.4.7