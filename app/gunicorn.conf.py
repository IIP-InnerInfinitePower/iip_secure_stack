import multiprocessing

bind = "0.0.0.0:5000"
workers = max(2, multiprocessing.cpu_count() * 2 + 1)
threads = 2
timeout = 120
graceful_timeout = 30
keepalive = 10
worker_class = "gthread"
