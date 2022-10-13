# https://docs.celeryq.dev/en/stable/userguide/configuration.html

broker_url = 'redis://localhost:6379/0'

broker_transport_options = {'visibility_timeout': 3600}

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'

timezone = 'UTC'
enable_utc = True

result_expires = 3600
task_track_started = True
task_time_limit = 30 * 60

beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    }
}
