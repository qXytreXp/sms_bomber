import __init__
import asyncio

from src.bomber.bomber import Bomber, CountSms
from src.config import REDIS_URL

from celery import Celery
from typing import Union


app = Celery('sms_bomb', broker=REDIS_URL)


@app.task(name='task_bomber')
def task_bomber(
        user_id: int,
        phone_number: str,
        count_services: Union[int, str],
        delay: int,
        end_time_in_minutes: int
) -> None:
    save_count_sms = CountSms(user_id)

    asyncio.run(Bomber(
        phone_number,
        count_services,
        delay,
        end_time_in_minutes,
        save_count_sms=save_count_sms
    ).run())
