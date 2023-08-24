import urllib3
import json
from datetime import datetime, timedelta


def request_time() -> datetime:
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://worldtimeapi.org/api/timezone/utc')
    data = json.loads(response.data.decode('utf-8'))
    return datetime.fromisoformat(data['datetime']).replace(tzinfo=None)


def server_time_difference() -> float:
    local_time = datetime.now()
    server_time = request_time()
    if local_time > server_time:
        diff = local_time - server_time
        return timedelta(minutes=round(diff.seconds / 60)).total_seconds() / 60 / 60
    else:
        diff = (server_time - local_time)
        return timedelta(minutes=round(diff.seconds / 60)).total_seconds() / 60 / -60
