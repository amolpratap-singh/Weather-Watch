import sys
import subprocess
import time

# while True:
#     time.sleep(1000)

if __name__ == "__main__":
    sys.exit(subprocess.call([
        'gunicorn', '-b', '0.0.0.0:8000',
        'swagger_server.wsgi:app',
        '--worker-class', 'uvicorn.workers.UvicornWorker'
    ]))