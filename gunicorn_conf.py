bind='127.0.0.1:8000'
worker_class='sync'
loglevel = 'debug'
accesslog = '/var/log/gunicorn/access_log_monsterdb'
accesslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = '/var/log/gunicorn/error_log_monsterdb'
