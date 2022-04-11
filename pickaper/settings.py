
import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

CARS_COUNT = int(os.environ.get('CARS_COUNT', os.cpu_count() or 8))
