import multiprocessing

# Number of workers (e.g., 2 * CPU cores + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Bind to all interfaces on port 8000
bind = "0.0.0.0:8000"

# Load the Flask app from run.py


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %d)", worker.pid)


def when_ready(server):
    server.log.info("Gunicorn is ready and listening at http://%s", bind)


def init(server):
    from run import app as application  # Import the app instance from run.py
    server.app = application            # Use the pre-created app
