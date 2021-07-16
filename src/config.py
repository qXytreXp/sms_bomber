import os

# Bot configuration
TOKEN = os.getenv('TOKEN', '1821546691:AAHw110aXaePDNM5fUDVEEMPiHuKF-4vgTI')

# Mongodb configuration
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'SMSBombir')
MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
MONGODB_PORT = os.getenv('MONGODB_PORT', 27017)
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'user123')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'user123')

# Redis configuration
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'RedisKeyvaluEStoragePasswordROOT12345432D')
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_URL = f'redis://{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
