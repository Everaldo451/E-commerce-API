import multiprocessing
from decouple import config

bind = f"{config('HOST')}:{config('PORT')}"
workers = multiprocessing.cpu_count() * 2 + 1