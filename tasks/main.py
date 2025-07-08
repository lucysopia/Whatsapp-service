from tasks import huey
from huey import crontab


@huey.periodic_task(crontab(minute="*/10"))
def echo(**kwargs):
    print("Hello from Huey")
