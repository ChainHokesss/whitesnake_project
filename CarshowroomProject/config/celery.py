import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'buy_suppliers_cars': {
        'task': 'src.carshowroom.tasks.buy_suppliers_cars',
        'schedule': crontab(minute = '*/10'),
    },
    'check_suppliers_benefit': {
        'task': 'src.carshowroom.tasks.check_supplier_benefit',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'accept_offer': {
        'task': 'src.carshowroom.tasks.accept_offer',
        'schedule': crontab(minute = '*/10'),
    }
}