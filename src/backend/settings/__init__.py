from decouple import config

env = config('ENV', default='development')

if env=='production':
    from .production import *
elif env=='test':
    from .test import *
elif env=='development':
    from .development import *