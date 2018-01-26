import requests, zipfile, StringIO
import pandas as pd
import redis
from urllib.parse import urlparse
import redis

url = urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, db=0)

r = requests.get("http://www.bseindia.com/download/BhavCopy/Equity/EQ250118_CSV.ZIP", stream=True)
z = zipfile.ZipFile(StringIO.StringIO(r.content))
z.extractall()

stocks = pd.read_csv('EQ250118.CSV')
#print stocks["OPEN"]
#print stocks["OPEN"].values.tolist()
r.rpush('SC_CODE',*stocks["SC_CODE"].values.tolist())
r.rpush('SC_NAME',*stocks["SC_NAME"].values.tolist())
r.rpush('OPEN',*stocks["OPEN"].values.tolist())
r.rpush('HIGH',*stocks["HIGH"].values.tolist())
r.rpush('LOW',*stocks["LOW"].values.tolist())
r.rpush('CLOSE',*stocks["CLOSE"].values.tolist())


print r.llen('SC_CODE')
print r.llen('SC_NAME')
print r.llen('OPEN')
print r.llen('HIGH')
print r.llen('LOW')
print r.llen('CLOSE')
