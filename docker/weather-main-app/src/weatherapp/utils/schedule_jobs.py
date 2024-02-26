import time
import schedule

from functools import wraps

def schedule_interval(interval):
    
    def jobs(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def jobs():
                func(*args, **kwargs)
            #schedule.every(interval).seconds.do(jobs)
            schedule.every(interval).hours.do(jobs)
            while True:
                schedule.run_pending()
                time.sleep(1)
            
        return wrapper
    return jobs
