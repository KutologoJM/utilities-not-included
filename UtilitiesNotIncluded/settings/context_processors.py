from django.conf import settings
import time

def dev_timestamp(request):
    if settings.DEBUG:
        return {"timestamp": int(time.time())}
    return {}
