import multiprocessing

# Number of workers (e.g., 2 * CPU cores + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Bind to all interfaces on port 8000
bind = "0.0.0.0:8000"

# Load the Flask app using the factory pattern


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %d)", worker.pid)


def when_ready(server):
    server.log.info("Gunicorn is ready and listening at http://%s", bind)


def init(server):
    from backend.app import create_app  # Import the factory function
    server.app = create_app()          # Call the factory to get the app instance
