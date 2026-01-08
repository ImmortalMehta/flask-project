import os
import ssl
import sys
import certifi
import traceback

print('Python:', sys.version.split()[0])
print('OpenSSL:', ssl.OPENSSL_VERSION)

try:
    import pymongo
    print('pymongo', pymongo.__version__)
except Exception as e:
    print('pymongo not available:', e)

try:
    import dns
    print('dnspython', dns.__version__)
except Exception as e:
    print('dnspython not available:', e)

print('certifi CA bundle:', certifi.where())

MONGO_URI = os.environ.get('MONGODB_URI', "mongodb+srv://immortal:immortalduck@gooner.fnw1yio.mongodb.net/?appName=gooner")
print('Using MONGO_URI:', MONGO_URI)

from pymongo import MongoClient

ca = certifi.where()

print('\nAttempting connection with CA bundle...')
try:
    client = MongoClient(MONGO_URI, tls=True, tlsCAFile=ca, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('Success: connected with CA bundle')
except Exception as e:
    print('Failed (CA bundle):', type(e), e)
    traceback.print_exc()

print('\nAttempting connection allowing invalid certificates (for diagnostics only)...')
try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('Success: connected with invalid certs allowed')
except Exception as e:
    print('Failed (allow invalid):', type(e), e)
    traceback.print_exc()

print('\nDone')
