import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theater.settings')

app = Celery('theater')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Настройка периодических задач Celery
app.conf.beat_schedule = {
    'send-sessions-reminders-task': {
        'task': 'ticket_buy.tasks.send_sessions_reminders',
        'schedule': crontab(hour=20, minute=0),  # Выполняется каждый день в 23:00
    },
    'send-bookings-reminders-task': {
        'task': 'ticket_buy.tasks.send_bookings_reminders',
        'schedule': crontab(hour=20, minute=0),  # Выполняется каждый день в 23:00
    },
    'collect-daily-performance-statistics-task': {
        'task': 'admin_panel.tasks.collect_daily_performance_statistics',
        'schedule': crontab(hour=20, minute=0),  # Выполняется каждый день в 23:00
    },
    'collect-daily-time-statistics-task': {
        'task': 'admin_panel.tasks.collect_daily_time_statistics',
        'schedule': crontab(hour=20, minute=0),  # Выполняется каждый день в 23:00
    },
    'delete-tomorrow-bookings-task': {
        'task': 'ticket_buy.tasks.delete_tomorrow_bookings',
        'schedule': crontab(hour=20, minute=58),  # Выполняется каждый день в 23:58
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# celery -A theater worker --loglevel=info -P eventlet
# redis-server.exe D:\programs\redis\redis.windows.conf
# celery -A theater beat --loglevel=info
# celery -A theater flower

# 'schedule': timedelta(seconds=60),
